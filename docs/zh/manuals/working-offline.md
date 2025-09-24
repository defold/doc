---
title: 离线工作
brief: 本手册介绍了如何在包含依赖项（特别是原生扩展）的项目中离线工作
---

# 离线工作

Defold 在大多数情况下不需要网络连接即可工作。然而，在少数情况下需要网络连接：

* 自动更新
* 报告问题
* 获取依赖项
* 构建原生扩展


## 自动更新

Defold 会定期检查是否存在新更新。Defold 的更新检查会连接到 [官方下载站点](https://d.defold.com)。如果检测到更新，它将自动下载。

如果您的网络连接时间有限，且不希望等待自动更新触发，您可以从 [官方下载站点](https://d.defold.com) 手动下载新版本的 Defold。


## 报告问题

如果在编辑器中检测到问题，您可以选择将问题报告给 Defold 问题跟踪器。问题跟踪器 [托管在 GitHub 上](https://www.github.com/defold/editor2-issues)，这意味着您需要网络连接才能报告问题。

如果您在离线时遇到问题，可以稍后使用编辑器 [帮助菜单中的报告问题选项](/manuals/getting-help/#report-a-problem-from-the-editor) 手动报告。


## 获取依赖项

Defold 支持一个系统，开发者可以通过称为 [库项目](/manuals/libraries/) 的功能共享代码和资源。库是可以在任何地方在线托管的 zip 文件。您通常可以在 GitHub 和其他在线代码存储库中找到 Defold 库项目。

项目可以在 [项目设置中将库添加为项目依赖项](/manuals/project-settings/#dependencies)。依赖项在项目打开时或任何时候从 *项目* 菜单中选择 *获取库* 选项时进行下载/更新。

如果您需要离线工作并且在多个项目中工作，您可以提前下载依赖项，然后使用本地服务器共享它们。GitHub 上的依赖项通常可以从项目存储库的发布选项卡中找到：

![GitHub Library URL](images/libraries/libraries_library_url_github.png)

您可以使用 Python 轻松创建本地服务器：

    python -m SimpleHTTPServer

这将在当前目录中创建一个服务器，在 `localhost:8000` 上提供文件。如果当前目录包含下载的依赖项，您可以将它们添加到您的 *game.project* 文件中：

    http://localhost:8000/extension-fbinstant-4.1.1.zip


## 构建原生扩展

Defold 支持一个系统，开发者可以通过称为 [原生扩展](/manuals/extensions/) 的功能添加原生代码来扩展引擎的功能。Defold 通过基于云的构建解决方案为原生扩展提供了零设置入口点。

当您第一次构建包含原生扩展的项目时，原生代码将在 Defold 构建服务器上编译成自定义的 Defold 游戏引擎，然后发送回您的 PC。只要您不添加、删除或更改任何原生扩展，并且只要您不更新编辑器，自定义引擎将在您的项目中缓存并用于后续构建。

如果您需要离线工作，并且您的项目包含原生扩展，您必须确保至少成功构建一次，以确保您的项目包含自定义引擎的缓存副本。
