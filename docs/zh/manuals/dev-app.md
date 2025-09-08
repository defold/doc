---
title: 在设备上运行开发应用
brief: 本手册解释了如何在设备上放置开发应用，以便在设备上进行迭代开发。
---

# 移动开发应用

开发应用允许您通过wifi将内容推送到它。这将大大减少迭代时间，因为您不必在每次希望测试更改时都进行打包和安装。您在设备上安装开发应用，启动应用，然后从编辑器中选择设备作为构建目标。

## 安装开发应用

任何以Debug模式打包的iOS或Android应用程序都可以作为开发应用。事实上，这是推荐的解决方案，因为开发应用将具有正确的项目设置，并使用与您正在处理的项目相同的[原生扩展](/manuals/extensions/)。

从Defold 1.4.0开始，可以打包项目的Debug变体而不包含任何内容。使用此选项创建带有原生扩展的应用程序版本，适用于本手册中描述的迭代开发。

![content less bundle](images/dev-app/contentless-bundle.png)

### 在iOS上安装

按照[iOS手册中的说明](/manuals/ios/#creating-an-ios-application-bundle)为iOS打包。确保选择Debug作为变体！

### 在Android上安装

按照[Android手册中的说明](https://defold.com/manuals/android/#creating-an-android-application-bundle)为Android打包。

## 启动您的游戏

要在设备上启动游戏，开发应用和编辑器必须能够通过相同的wifi网络或使用USB（见下文）进行连接。

1. 确保编辑器已启动并正在运行。
2. 在设备上启动开发应用。
3. 在编辑器中的<kbd>Project ▸ Targets</kbd>下选择您的设备。
4. 选择<kbd>Project ▸ Build</kbd>来运行游戏。游戏启动可能需要一段时间，因为游戏内容通过网络流式传输到设备。
5. 游戏运行时，您可以照常使用[热重载](/manuals/hot-reload/)。

### 在Windows上使用USB连接iOS设备

在Windows上通过USB连接到运行在iOS设备上的开发应用时，首先需要[安装iTunes](https://www.apple.com/lae/itunes/download/)。安装iTunes后，您还需要从设置菜单中[在iOS设备上启用个人热点](https://support.apple.com/en-us/HT204023)。如果您看到提示点击"Trust This Computer?"的警报，请点击Trust。当开发应用运行时，设备现在应该会显示在<kbd>Project ▸ Targets</kbd>下。

### 在Linux上使用USB连接iOS设备

在Linux上，当使用USB连接时，您需要从设置菜单中在设备上启用个人热点。如果您看到提示点击"Trust This Computer?"的警报，请点击Trust。当开发应用运行时，设备现在应该会显示在<kbd>Project ▸ Targets</kbd>下。

### 在macOS上使用USB连接iOS设备

在较新的iOS版本上，当在macOS上使用USB连接时，设备会自动在设备和计算机之间打开一个新的以太网接口。当开发应用运行时，设备应该会显示在<kbd>Project ▸ Targets</kbd>下。

在较旧的iOS版本上，当在macOS上使用USB连接时，您需要从设置菜单中在设备上启用个人热点。如果您看到提示点击"Trust This Computer?"的警报，请点击Trust。当开发应用运行时，设备现在应该会显示在<kbd>Project ▸ Targets</kbd>下。

### 在macOS上使用USB连接Android设备

在macOS上，当设备处于USB网络共享模式时，可以通过USB连接到运行在Android设备上的开发应用。在macOS上，您需要安装第三方驱动程序，如[HoRNDIS](https://joshuawise.com/horndis#available_versions)。安装HoRNDIS后，您还需要通过安全性与隐私设置允许它运行。一旦启用USB网络共享，当开发应用运行时，设备将显示在<kbd>Project ▸ Targets</kbd>下。

### 在Windows或Linux上使用USB连接Android设备

在Windows和Linux上，当设备处于USB网络共享模式时，可以通过USB连接到运行在Android设备上的开发应用。一旦启用USB网络共享，当开发应用运行时，设备将显示在<kbd>Project ▸ Targets</kbd>下。

## 故障排除

无法下载应用程序
: 确保您的设备UDID包含在用于签署应用程序的移动配置中。

您的设备没有出现在Targets菜单中
: 确保您的设备连接到与计算机相同的wifi网络。确保开发应用是以Debug模式构建的。

游戏没有启动，并显示有关版本不匹配的消息
: 当您将编辑器升级到最新版本时会发生这种情况。您需要构建并安装新版本。
