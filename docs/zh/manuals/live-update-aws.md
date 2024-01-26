---
title: Live update content uploads to AWS
brief: This section will explain how to create a new user with limited access on Amazon Web Services that can be used together with the Defold editor to automatically upload Live update resources when you bundle your game.
---

# 创建 Amazon 网络服务器

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

    ::: important
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
