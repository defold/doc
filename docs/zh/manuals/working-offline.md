---
title: 断网工作
brief: 本教程介绍了在离线状态下使用依赖库尤其是使用原生扩展的方法
---

# 断网工作

Defold 在大多数情况下不需要网络连接. 然而下面几种情况下必须有网络连接:

* 自动更新
* 问题反馈
* 下载依赖库
* 编译原生扩展


## 自动更新

Defold 定期查找是否存在更新版本. Defold 查找新版本时会连接 [官方下载地址](https://d.defold.com). 如果找到更新版本会给与用户提示以方便下载.

要是你的网络流量吃紧或者不太关心最新版本, 也可以手动从 [官方下载地址](https://d.defold.com) 下载 Defold.


## 问题反馈

如果编辑器发现了错误就会弹出错误报告框让用户选择是否把错误内容回报给 Defold 官方. 错误跟踪表 [存储在 GitHub 上](https://www.github.com/defold/editor2-issues), 所以回报问题时需要联网.

如果在离线状态下遇到错误还可以使用编辑器的 [帮助菜单下的回报错误按钮](/manuals/getting-help/#从编辑器里汇报问题) 提交错误报告.


## 下载依赖

Defold 支持通过一个叫做 [库项目](/manuals/libraries/) 的功能共享代码和资源. 库被保存为zip文件存放在网络上. 一般 Defold 库项目都保存在 GitHub 和各个代码托管平台上.

在项目设置里可以添加库 [作为项目依赖](/manuals/project-settings/#Dependencies). 当项目开启或者 *Project* 菜单栏下的 *Fetch Libraries* 被点选时, Defold 会自动进行项目依赖的下载/更新.

如果必须团队离线工作, 建议把共享依赖存放在本地共享服务器上. GitHub 上的依赖库文件一般都在其发布页面:

![GitHub Library URL](images/libraries/libraries_library_url_github.png)

可以使用 Python 方便地创建简单的本地服务器:

    python -m SimpleHTTPServer

这条命令会在当前文件夹建立本地服务器并且在 `localhost:8000` 地址进行共享服务. 如果这个目录下存放了共享库文件, 就可以在 *game.project* 文件里像这样添加依赖:

    http://localhost:8000/extension-fbinstant-4.1.1.zip


## 编译原生扩展

Defold 支持开发者通过一个叫做 [Native Extensions](/manuals/extensions/) 的功能, 使用原生代码扩展引擎功能. Defold 使用云端构建方案以方便开发者编译自己的原生扩展程序.

当第一次编译带原生扩展代码的项目时, 代码会被传送至云端编译服务器编译成用户自定义 Defold 游戏引擎然后再发回给你的电脑. 这个自定义引擎会被缓存在你的项目中随时调用, 直到原生代码被修改需要重新编译.

如果必须离线工作而你的项目又包含原生扩展就要确保至少通过云端编译成功一次, 在你的本地缓存了自定义引擎才能正常工作.
