---
title: Defold 的热更新
brief: 热更新允许游戏运行时获取和存储编译时并不存在的资源. 本教程介绍了热更新的用法.
---

#### 目前热更新机制正在升级, 本教程可能随时变化

# 热更新

打包游戏时, Defold 把所有游戏资源装进游戏包当中. 多数情况下这样做很好因为游戏运行时引擎要快速找到加载所需要的各种资源. 但是, 有一些情况下需要将资源加载推迟到后续阶段. 比如:

- 你的游戏设计了好几个章节但是只免费提供第一章节给玩家试玩以便让玩家决定是否购买游戏的后续章节.
- 你做了个 HTML5 游戏. 在浏览器里, 一个程序的所有内容全部加载完成这个程序才能运行. 可以用一个小程序让游戏先展示出来, 大量自由数据下载留到后面再说.
- 你的游戏包含大量资源数据 (图片, 视频之类的) 所以需要一种按需求的下载和加载机制. 这样就能保证游戏包不会太大.

热更新扩展了集合代理的概念允许引擎在运行时获取和存储未被打入游戏包的资源数据.

## 准备工作

假设我们有个很大的, 高分辨率的图片. 图片放在sprite里, sprite放在游戏对象里, 游戏对象放在集合里:

![Mona Lisa collection](images/live-update/mona-lisa.png)

动态加载这个集合, 只需使用集合代理组件并将它指向 *monalisa.collection* 即可. 集合里的资源合适加载入内存取决于发给集合代理的 `load` 消息. 如果要进一步控制资源文件的话,

勾选集合代理属性 *Exclude* 即可, 打包时会把 *monalisa.collection* 的内容排除于包外.

![Collection proxy excluded](images/live-update/proxy-excluded.png)

## 热更新配置

游戏打包时需要知道把包外的资源保存在哪里了. 项目设置里的热更新配置明确了这个保存位置. 点击 <kbd>Project ▸ Live update Settings...</kbd> 来创建热更新配置文件. 在 *game.project* 里, 指定打包时所使用的热更新配置文件. 不同运行环境可以对于不同配置, 比如游戏环境, 测试环境, 开发环境等.

![Live update settings](images/live-update/aws-settings.png)

目前 Defold 支持两种包外资源的保存模式. 可以在设置窗口里的 *Mode* 下拉菜单中选择:

`Amazon`
: 让 Defold 自动把包外资源上传到 Amazon Web Service (AWS) S3 服务器上. 填写 AWS *凭证* 名, 选择合适的 *服务器* 在提供一个 *前缀* 名. [关于 AWS 账户注册请见下文](#setting_up_amazon_web_service).

`Zip`
: 让 Defold 把包外资源打成 zip 包. 并且在配置里 *Export path* 项指定存放路径.


## 热更新脚本

热更新集合代理和普通集合代理差不多, 只是有一个重要区别. 如果在资源还没下载好的时候发送 `load` 消息的话就会导致失败报错.

所以发送 `load` 之前, 一定要确保资源的完整性. 把完整的资源下载并保存好. 一下代码假设资源保存在 Amazon S3, 一个叫做 "my-game-bucket" 的服务器上, 前缀为 `my-resources`.

```lua
function init(self)
    self.resources_pending = 0 -- <1>
    msg.post("#", "attempt_load_resources")
end

-- 下载热更新用到的包外资源进行本地保存时会调用此函数
local function resource_store_response(self, hexdigest, status)
    if status == true then
        -- 加载成功
        print("Resource data stored: " .. hexdigest)

        -- 还差一个资源
        self.resources_pending = self.resources_pending - 1

        -- 全部保存好了, 可以开始加载了
        if self.resources_pending == 0 then
            msg.post("#proxy", "load") -- <8>
        end
    else
        -- 错误! 资源数据保存失败.
        print("Failed to store resource data: " .. hexdigest)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("attempt_load_resources") then
        local missing_resources = collectionproxy.missing_resources("#proxy") -- <2>

        -- 为缺失的而且没被尝试下载过的资源初始化下载请求.
        for _,resource_hash in ipairs(missing_resources) do
            msg.post("#", "attempt_download", { resource_hash = resource_hash})
        end

        self.resources_pending = #missing_resources -- <3>

        -- 如果游戏是从编辑器运行的, 那么全部资源都存在本地.
        if self.resources_pending == 0 then
            msg.post("#proxy", "load")
        end
    elseif message_id == hash("attempt_download") then
        local manifest = resource.get_current_manifest() -- <4>
        local base_url = "https://my-game-bucket.s3.amazonaws.com/my-resources/" -- <5>
        http.request(base_url .. message.resource_hash, "GET", function(self, id, response)
            if response.status == 200 or response.status == 304 then -- <6>
                -- 得到ok响应.
                print("storing " .. message.resource_hash)
                resource.store_resource(manifest, response.response, message.resource_hash, resource_store_response) -- <7>
            else
                -- 错误! 资源下载失败.
                print("Failed to download resource: " .. message.resource_hash)
            end
        end)
    elseif message_id == hash("proxy_loaded") then
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```
1. 一个计数器记录了还剩多少资源需要下载保存. 注意此处未做错误处理, 产品级游戏要跟踪好下载和保存的各种情况.
2. 得到需要下载保存的资源.
3. 计数器更新.
4. 资源需求清单.
5. 本例中资源保存于 Amazon S3. 如果使用zip包保存资源, 需要调用 `http.request()` 连同资源托管地址进行下载.
6. 文件缓存好之后 Amazon 返回状态 304.
7. 下载完成, 开始保存.
8. 保存成功, 资源计数器清零. 此时可以放心发送 "load" 消息给集合代理. 注意如果下载保存任何地方出错, 计数器都不会清零.

一切准备就绪, 我们可以尝试启动这个程序. 但是从编辑器运行并不会下载任何东西. 因为热更新是游戏包的功能. 编辑器运行时游戏未打包. 所以, 要测试热更新必须先给游戏打包.

## 热更新应用打包

打包很简单. 选择 <kbd>Project ▸ Bundle ▸ ...</kbd> 然后选择目标平台. 此时会弹出对话框:

![Bundle Live application](images/live-update/bundle-app.png)

打包时, 指定资源被排除在包外. 勾选 *Publish Live update content*, 来让 Defold 把包外资源自动上传给 Amazon 或者打成zip包, 取决于热更新配置 (见上文). 资源清单也会被生成出来.

点击 *Package* 然后指定保存位置. 打包好之后就能测试热更新功能了.

## 清单文件

清单是一种内部数据结构用来保存编译所需的所有资源列表连同每个资源的哈希值. 热更新使用清单来确定哪些资源是游戏的一部分, 哪些资源不在本地需要下载, 还要确定下载的资源是否完整.

从用户角度来看, 清单是一个数字句柄, 将如何管理资源的细节留给引擎去做.

## 清单更新

每次热更新都会在本地保存一份更新的清单. 应用启动时会使用最新的清单代替包内的清单. 这对于游戏后续通过热更新来修改增添资源很重要, 尤其是第一版游戏打包时并不知道的资源.

当把资源上传到 Amazon 服务器或打包成zip资源包的时候, 清单也会被加入到那些资源当中. 名称为 `liveupdate.game.dmanifest`.

保存清单后首次启动引擎时会生成一个游戏包版本文件 `bundle.ver`. 用来判断保存清单之后游戏有无改动, 比如说一次完整的 app store 更新. 如果是这样的话清单将从文件系统中删除并使用更新版本游戏包中的清单代替. 也就是说完整 app store 更新会清除上次保存的清单. 而通过热更新下载到本地的资源不被清除.

### 清单验证
保存新版清单之前会对其进行验证. 验证包括如下内容:

* 二进制文件格式是否正确.
* 引擎版本是否正确.
* 清单签名是否正确.
* 新旧文件签名所用的公钥私钥是否一致.
* 清单列出的资源是否齐全.

从用户角度来看, 验证过程不必深入了解, 但是要知道验证内容, 以便遇到错误时可以及时修复.

::: sidenote
如果遇到 "ERROR:RESOURCE: Byte mismatch in decrypted manifest signature. Different keys used for signing?" 错误很有可能是因为你的服务器对包外资源和清单文件的 MIME 类型设置错误. 确保 MIME 类型为 `application/octet-stream`. 可以使用 `.htaccess` 文件加上一条 `AddType application/octet-stream .` 关联到资源和清单文件所在文件夹.
:::

### 引擎版本
清单文件支持生成它的 Defold 版本. 如果希望它支持更多版本, 需要在热更新配置里手动添加. 如果你的游戏需要多版本客户端同时在线, 这一步设定很重要.

![Manifest supported engine versions](images/live-update/engine-versions-settings.png)

### 签名密钥
清单签名用来保证游戏内容没有被恶意篡改, 还要确保新旧清单文件签名所用的密钥是相同的. 编译时签名自动生成.
清单签名使用一对公私密钥. 用户需要提供 `.der` 格式 512/1024/2048-bit RSA 密钥. 可以使用 `openssl` 工具生成密钥:

```sh
$ openssl genrsa -out private_raw.key 1024
$ openssl pkcs8 -topk8 -inform pem -in private_raw.key -outform der -nocrypt -out private.der
$ openssl rsa -in private_raw.key -outform DER -RSAPublicKey_out -pubout -out public.der
```
输出文件为 `private_raw.key` (可以删除), `private.der` 和 `public.der`. 然后在热更新配置里指定密钥位置.

![Manifest signature key-pair](images/live-update/manifest-keys.png)

### 热更新清单脚本
接上文热更新脚本, 加入以下回调函数:

```lua
local function store_manifest_cb(self, status)
    if status == resource.LIVEUPDATE_OK then
        print("Successfully stored manifest!")
    else
        print("Failed to store manifest, status: ", status)
    end
end
```

然后在 ```on_message``` 里加入处理 ```attempt_download_manifest``` 的代码:

```lua
...
elseif message_id == hash("attempt_download_manifest") then
    local base_url = "https://my-game-bucket.s3.amazonaws.com/my-resources/" -- <1>
    http.request(base_url .. MANIFEST_FILENAME, "GET", function(self, id, response)
        if response.status == 200 or response.status == 304 then
            -- 响应 ok.
            print("verifying and storing manifest " .. MANIFEST_FILENAME)
            resource.store_manifest(response.response, store_manifest_cb) -- <2>
        else
            -- 错误! 清单下载失败.
            print("Failed to download manifest: " .. MANIFEST_FILENAME)
        end
    end)
end
```
1. 清单文件要跟热更新资源保存在一起. 无论是保存在S3服务器还是打zip包.
2. 跟资源文件下载保存类似, 调用 `resource.store_manifest` 下载清单数据传入回调函数. 下载验证后保存在本地.

如果 `resource.store_manifest` 成功, 清单已保存在本地. 下次游戏启动会自动使用新清单文件代替包内旧清单文件.

### 注意事项
更新清单文件要注意几个事项.

* 只能添加或修改集合代理中被设置为 `Exclude` 的资源. 包内资源和集合代理未设置排除的资源不可更改. 比如清单列表要更新包内脚本, 但是因为包内资源不变 (只有清单更新了), 无法在包内找到新脚本, 更新肯定不会成功.

* 热更新方便快捷, 但是使用时要多加留意. 热更新也是更新, 发布前也要做测试等工作.

## 创建 Amazon 网络服务器

要使用 Defold 配合 Amazon 服务器进行热更新首先要有 Amazon Web Services 账户. 没有的话请在这里注册: https://aws.amazon.com/.

这里介绍一下如何开通 Amazon 服务以配合 Defold 进行热更新, 在 Amazon S3 需要那些配置. 更多关于 Amazon S3 的信息, 请参考 [Amazon S3 文档](http://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html).

1. 开通服务

    在 _Storage_ 类目 ([Amazon S3 Console](https://console.aws.amazon.com/s3)) 下打开 `Services` 菜单选择 `S3`. 页面上会列出已存在的所有服务器与开通新服务器的选项. 使用已存在的服务器是可以的, 但是建议为热更新资源创建一个新服务器,以便设置访问限制.
    
    ![Create a bucket](images/live-update/01-create-bucket.png)

2. 服务配置

    开通服务器, 打开 *Properties* 面板展开折叠的 *Permissions* 选项. 点击 *Add bucket policy* 按钮添加配置文件. 本例中的配置是允许任何客户端访问服务器资源, 以便热更新顺利工作. 更多配置信息, 请参考 [Amazon 文档](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-iam-policies.html).

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AddPerm",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::defold-liveupdate-example/*"
            }
        ]
    }
    ```

    ![Bucket policy](images/live-update/02-bucket-policy.png)

3. 添加 CORS 配置 (可选)

    [Cross-Origin Resource Sharing (CORS)](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) 是一种能让服务器使用 JavaScript 访问另一服务器资源的机制. 如果你发布的是 HTML5 游戏, 就需要给服务器添加 CORS 配置.

    选择服务器, 打开 *Properties* 面板展开折叠的 *Permissions* 选项. 点击 *Add CORS Configuration* 按钮添加 CORS 配置. 本例中的配置是允许任何服务器访问本服务器资源, 如果需要可以做详细的限制. 更多 Amazon CORS 配置信息, 请参考 [Amazon 文档](https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html).

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
        <CORSRule>
            <AllowedOrigin>*</AllowedOrigin>
            <AllowedMethod>GET</AllowedMethod>
        </CORSRule>
    </CORSConfiguration>
    ```

    ![CORS configuration](images/live-update/03-cors-configuration.png)

4. 创建 IAM 配置

    打开 *Services* 菜单, 在 _Security, Identity & Compliance_ 类目 ([Amazon IAM Console](https://console.aws.amazon.com/iam)) 下打开 *IAM*. 选择左边的 *Policies*, 页面会列出已存在的所有 IAM 配置与创建新配置的选项.

    点击 *Create Policy* 按钮, 选择 _Create Your Own Policy_. 本例中的配置是允许用户获得服务器列表, 这是 Defold 热更新的必要配置. 这里还可以允许用户获得 Access Control List (ACL) 和把资源文件上传至服务器的权力. 关于 Amazon Identity and Access Management (IAM) 的更多信息, 详见 [Amazon 文档](http://docs.aws.amazon.com/IAM/latest/UserGuide/access.html).

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:ListAllMyBuckets"
                ],
                "Resource": "arn:aws:s3:::*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetBucketAcl"
                ],
                "Resource": "arn:aws:s3:::defold-liveupdate-example"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject"
                ],
                "Resource": "arn:aws:s3:::defold-liveupdate-example/*"
            }
        ]
    }
    ```

    ![IAM policy](images/live-update/04-create-policy.png)

5. 创建管理账户

    打开 *Services* 菜单, 在 _Security, Identity & Compliance_ 类目 ([Amazon IAM Console](https://console.aws.amazon.com/iam)) 下打开 *IAM*. 选择左边的 *Users*, 页面会列出已存在的所有用户与创建新用户的选项. 使用已存在的用户是可以的, 但是建议为热更新资源创建一个新用户,以便设置访问限制.

    点击 *Add User* 按钮, 输入用户名选择 *Programmatic access* 作为 *Access type*, 然后点击 *Next: Permissions*. 选择 *Attach existing policies directly* 然后选择第4步中所作的配置.

    完成之后你会得到 *Access key ID* 和 *Secret access key*.

    ::: sidenote
    保存好密匙 *非常重要* 因为离开 Amazon 页面后就无法再次获得密匙了.
    :::

6. 创建档案文件

    此时你已经开启了服务器, 做好了客户端访问配置, 添加了服务端方位配置, 新建了用户权限和一个新用户. 剩下的最后一件事是创建 [档案文件](https://aws.amazon.com/blogs/security/a-new-and-standardized-way-to-manage-credentials-in-the-aws-sdks) 以便让 Defold 也能访问服务器.

    在本地新建一个 *.aws* 文件夹, 在里面新建一个 *credentials* 文件.

    ```bash
    $ mkdir ~/.aws
    $ touch ~/.aws/credentials
    ```

    文件 *~/.aws/credentials* 要包含访问 Amazon 服务所需的凭证即标准 AWS 证书. 打开文件按照如下格式输入你的 *Access key ID* 和 *Secret access key*.

    ```ini
    [defold-liveupdate-example]
    aws_access_key_id = <Access key ID>
    aws_secret_access_key = <Secret access key>
    ```

    服务器名, 本例中是 _defold-liveupdate-example_, 在 Defold 编辑器热更新配置里也要提供.

    ![Live update settings](images/live-update/05-liveupdate-settings.png)

## 开发注意事项

调试
: 运行打包游戏, 不要直接接入控制台. 这在调试时会产生错误. 但是当你使用命令行或者双击启动的方式启动游戏:

  ![Running a bundle application](images/live-update/run-bundle.png)

  这样游戏里的 `print()` 语句输出都会被打印到控制台上:

  ![Console output](images/live-update/run-bundle-console.png)

强制重新下载资源
: 游戏保存资源时, 文件被保存在设备本地硬盘上. 重启游戏, 资源文件并不消失. 开发阶段可能会希望删掉这些文件然后强制重新下载.

  Defold 在设备上的应用文件夹下创建了一个以游戏包哈希值为名字的文件夹. 如果删除这个文件夹下的文件, 游戏会自动把清单资源作废然后就可以重新下载重新保存了.

  ![Local storage](images/live-update/local-storage.png)

  这个应用文件夹的位置基于操作系统有所不同. 可以运行 `print(sys.get_save_file("", ""))` 脚本查看其路径.
  