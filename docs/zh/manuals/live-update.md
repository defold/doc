---
title: Defold 的热更新
brief: 热更新允许游戏运行时获取和存储编译时并不存在的资源. 本教程介绍了热更新的用法.
---

# 热更新

打包游戏时, Defold 把所有游戏资源装进游戏包当中. 多数情况下这样做很好因为游戏运行时引擎要快速找到加载所需要的各种资源. 但是, 有一些情况下需要将资源加载推迟到后续阶段. 比如:

- 你的游戏设计了好几个章节但是只免费提供第一章节给玩家试玩以便让玩家决定是否购买游戏的后续章节.
- 你做了个 HTML5 游戏. 在浏览器里, 一个程序的所有内容全部加载完成这个程序才能运行. 可以用一个小程序让游戏先展示出来, 大量自由数据下载留到后面再说.
- 你的游戏包含大量资源数据 (图片, 视频之类的) 所以需要一种按需求的下载和加载机制. 这样就能保证游戏包不会太大.

热更新扩展了集合代理的概念允许引擎在运行时获取和存储未被打入游戏包的资源数据.

它可以把你的内容分成多个卷:

* _基础卷_
* Level 公共文件
* Level 卷 1
* Level 卷 2
* ...

## 准备工作

假设我们有个很大的, 高分辨率的图片. 图片放在sprite里, sprite放在游戏对象里, 游戏对象放在集合里:

![Mona Lisa collection](images/live-update/mona-lisa.png)

动态加载这个集合, 只需使用集合代理组件并将它指向 *monalisa.collection* 即可. 集合里的资源合适加载入内存取决于发给集合代理的 `load` 消息. 如果要进一步控制资源文件的话,

勾选集合代理属性 *Exclude* 即可, 打包时会把 *monalisa.collection* 的内容排除于包外.

::: important
基础游戏包所引用的任何资源都不会被排除.
:::

![Collection proxy excluded](images/live-update/proxy-excluded.png)

## 热更新配置

游戏打包时需要知道把包外的资源保存在哪里了. 项目设置里的热更新配置明确了这个保存位置. 点击 <kbd>Project ▸ Live update Settings...</kbd> 来创建热更新配置文件. 在 *game.project* 里, 指定打包时所使用的热更新配置文件. 不同运行环境可以对于不同配置, 比如游戏环境, 测试环境, 开发环境等.

![Live update settings](images/live-update/aws-settings.png)

目前 Defold 支持两种包外资源的保存模式. 可以在设置窗口里的 *Mode* 下拉菜单中选择:

`Zip`
: 让 Defold 把包外资源打成 zip 包. 并且在配置里 *Export path* 项指定存放路径.

`Amazon`
: 让 Defold 自动把包外资源上传到 Amazon Web Service (AWS) S3 服务器上. 填写 AWS *凭证* 名, 选择合适的 *服务器* 在提供一个 *前缀* 名. [关于 AWS 账户注册请见下文](#setting_up_amazon_web_service).

## 热更新应用打包

::: important
编辑器的编译运行 (<kbd>Project ▸ Build</kbd>) 不支持热更新. 要想测试热更新必须把项目打包.
:::

打包很简单. 选择 <kbd>Project ▸ Bundle ▸ ...</kbd> 然后选择目标平台. 此时会弹出对话框:

![Bundle Live application](images/live-update/bundle-app.png)

打包时, 指定资源被排除在包外. 勾选 *Publish Live update content*, 来让 Defold 把包外资源自动上传给 Amazon 或者打成zip包, 取决于热更新配置 (见上文). 资源清单也会被生成出来.

点击 *Package* 然后指定保存位置. 打包好之后就能测试热更新功能了.

## .zip 卷

热更新的 .zip 文件包含了基础游戏包排除掉的文件.

我们目前的方法只支持单个 .zip 文件, 但是实际上把它分成若干小 .zip 文件是可行的. 这会让游戏下载更小的卷: level 包, 特典包等等. 每个 .zip 文件包含 manifest 文件描述了 .zip 文件里包含的资源的元数据.

## 拆分 .zip 卷

通常希望将被排除的内容拆分为几个较小的卷, 以便更精细地控制资源的使用. 一个实例就是把基于关卡的游戏拆分成多个关卡包. 另一个例子是将不同节日主题的 UI 装饰放入单独的存档中, 并仅加载和挂载当前节日的主题.

资源表保存在 `build/default/game.graph.json` 中, 该文件在项目打包时自动生成. 该文件包含项目中所有资源的列表及每个资源的依赖情况. 例如:

```json
{
  "path" : "/game/player.goc",
  "hexDigest" : "caa342ec99794de45b63735b203e83ba60d7e5a1",
  "children" : [ "/game/ship.spritec", "/game/player.scriptc" ]
}
```

每个条目都有一个 `path` 代表项目中资源的唯一路径. `hexDigest` 代表资源加密指纹, 它在热更新 .zip 卷里作为文件名使用. 最后 `children` 项是该资源所依赖的其他资源的列表. 上例中 `/game/player.goc` 依赖于一个 sprite 和一个脚本文件.

你可以解析 `game.graph.json` 文件, 并以此来标识资源表中的条目组, 并将其相应的资源与原始清单文件一起存储在单独的卷中 (清单文件将在运行时进行修剪, 以便它仅包含卷中的文件).

## 内容验证

热更新系统的一大特性, 是可以使用多个数据卷, 而不管它来自哪个版本的 Defold.

方法 `liveupdate.add_mount()` 的默认行为, 是添加 mount 时加入引擎版本校验.
这意味着游戏基础卷和热更新卷需要用相同引擎版本同时建立, 使用一致的打包选项. 这将使客户端将以前下载的内容无效化, 强制重新下载内容.

这个行为可以用一个可选参数关掉.
关掉的话, 内容验证责任完全由开发者承担, 以保证每个热更新卷都能在当前运行的引擎下可用.

我们建议给每个 mount 保存一些元数据, 以便 _在启动时_, 开发者能决定 mount/archive 是否应该删除.
一个办法就是在游戏打包后给 zip 包里加入文件. 比如插入一个存有相关信息的 `metadata.json`. 然后, 在启动时, 游戏能用 `sys.load_resource("/metadata.json")` 取回信息. _注意每个 mount 的自定义数据要有唯一的名字, 否则 mount 将使用最高优先级的文件_

如果没做好, 你将面对内容与引擎不匹配的局面, 这将导致强制自动退出.

## Mounts

热更新同时使用多个内容卷.
每个卷是 "挂载" 到引擎的资源系统的, 连同名字和优先级.

如果两个卷都有 `sprite.texturec` 文件, 则引擎将加载最高优先级的 mount 里的文件.

引擎并不索引 mount 里的资源. 当资源被载入内存, 卷可能会被卸载. 资源会保留在内存中直到它们被卸载.

mounts 在引擎重启时会被自动重新读取.

::: sidenote
挂在卷不会拷贝或移动文件包. 引擎只保存包的路径. 这样, 开发者可以任意删除卷, mount 会在下次启动时被删除.
:::

## 热更新脚本

使用热更新更新内容, 必须下载并挂载游戏数据.
参见 [这里的热更新脚本教程](/manuals/live-update-scripting.md).

## 开发警告

调试
: 当运行游戏的某个版本, 没有对控制台的直接访问权. 这在调试时会出问题. 然而, 你可以用命令行启动游戏或者双击游戏的可执行文件:

  ![Running a bundle application](images/live-update/run-bundle.png)

  此时游戏连同控制台窗口启动并能显示所有 `print()` 内容:

  ![Console output](images/live-update/run-bundle-console.png)

强制重新下载资源
: 开发者可以把内容下载到任意文件/文件夹里, 但是通常是保存在游戏目录. 游戏目录取决于操作系统. 可以用 `print(sys.get_save_file("", ""))` 找到.

  文件 liveupdate.mounts 放在 "local storage" 下, 这个目录显示在控制台开头 "INFO:LIVEUPDATE: Live update folder located at: ..."

  ![Local storage](images/live-update/local-storage.png)
