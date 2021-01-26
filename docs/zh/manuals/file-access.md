---
title: 处理文件
brief: 本教程介绍了保存和加载文件等处理文件的方法.
---

# 处理文件
存取文件有很多种方式. 文件的路径和文件类型决定了采取何种方式.

## 文件/文件夹存取函数
Defold 提供如下函数用以存取文件/文件夹:

* 标准输入输出库 [`io.*` functions](https://defold.com/ref/stable/io/). 用于文件/文件夹存取, 底层高效细致灵活.
* 操作系统库 [`os.rename()`](https://defold.com/ref/stable/os/#os.rename:oldname-newname) 和 [`os.remove()`](https://defold.com/ref/stable/os/#os.remove:filename) 用于文件改名和删除.
* 游戏引擎系统库 [`sys.save()`](https://defold.com/ref/stable/sys/#sys.save:filename-table) 和 [`sys.load()`](https://defold.com/ref/stable/sys/#sys.load:filename) 用于存取 Lua 表. 其他 [`sys.*`](https://defold.com/ref/stable/sys/) 下的函数用于不同操作系统文件路径的解析.

## 文件/文件夹位置
有三个文件/文件夹位置可供游戏应用存取使用:

* 游戏应用所在位置下的文件
* 游戏应用打包进去的文件
* 操作系统所管理的文件

### 游戏指定位置的文件处理
像最高分数, 用户设置和游戏状态等信息建议如此处理. 用 [`sys.get_save_file()`](https://defold.com/ref/stable/sys/#sys.get_save_file:application_id-file_name) 函数得到操作系统指定的文件绝对路径. 然后用 `sys.*`, `io.*` 和 `os.*` 函数处理文件/文件夹 (见上文).

[Check the example showing how to use sys.save() and sys.load()](/examples/file/sys_save_load/).

### 游戏应用打包进去的文件处理
把文件打包进游戏应用有两种方法:

1. **用户资源文件** - 在 *game.project* 配置文件的 [*Custom Resources* 项](https://defold.com/manuals/project-settings/#project) 进行设置. 然后可以使用 [`sys.load_resource()`](https://defold.com/ref/sys/#sys.load_resource) 函数进行访问. 注意这些文件实际上并不存在于用户的操作系统之中. 这样打包的文件作为游戏包的一部分只可以使用 `sys.load_resource()` 进行访问.
2. **打包资源文件** - 在 *game.project* 配置文件的 [*Bundle Resources* 项](https://defold.com/manuals/project-settings/#project) 进行设置. 然后可以使用 [`sys.get_application_path()`](https://defold.com/ref/stable/sys/#sys.get_application_path:) 得到应用的实际路径. 再基于应用路径得到资源文件的完整路径. 之后就可以使用 `io.*` 和 `os.*` 的功能函数进行访问 (参见上文).

 ::: 注意
 基于安全考虑浏览器 (及浏览器里运行的 JavaScript 插件) 不允许访问本地文件. 虽然 HTML5 游戏也能运行, 但是只能用浏览器提供的 IndexedDB API 在 "虚拟文件系统" 中存取数据. 也就是说不允许使用 `io.*` 和 `os.*` 下的函数. 但是可以用 `http.request()` 请求在线资源文件.
 :::

#### 用户资源与打包资源对比

| 特点              | 用户资源                          | 打包资源                              |
|-----------------------------|-------------------------------------------|------------------------------------------------|
| 加载速度               | 快 - 从应用二进制包内加载 | 慢 - 从文件系统中加载          |
| 加载单个文件的功能          | 无 - 只能加载全部资源                    | 有 - 基于文件的字节读取           |
| 应用打包后修改资源文件 | 无 - 所有资源保存为一个二进制资源包 | 有 - 文件存储基于文件操作系统    |
| HTML5 支持               | 有                                       | 有 - 但是这里的访问基于 http 而不是文件 I/O |


### 操作系统文件处理
基于安全考虑操作系统所管理的文件存取被严格限制. 可以使用 [`extension-directiories`](https://defold.com/assets/extensiondirectories/) 原生扩展来存取某些地方的绝对路径 (例如 documents, resource, temp). 然后用 `sys.*`, `io.*` 和 `os.*` 函数处理文件/文件夹 (见上文).


## 相关原生扩展
在 [资源中心](https://defold.com/assets/) 里有些原生扩展能简化文件存取的工作. 例如:

* [Lua File System (LFS)](https://defold.com/assets/luafilesystemlfs/) - 提供操作文件夹, 文件权限之类的功能.
* [DefSave](https://defold.com/assets/defsave/) - 一个用于保存/加载游戏设置和玩家数据档的模块.
