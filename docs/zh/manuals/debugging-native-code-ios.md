---
title: 在 iOS/macOS 中调试
brief: 本教程介绍了如何使用 Xcode 进行调试.
---

# 在 iOS/macOS 中调试

这里我们介绍如何使用 [Xcode](https://developer.apple.com/Xcode/), Apple的 macOS 和 iOS 首选开发环境来调试应用.

## Xcode

* 使用 bob, 加上 `--with-symbols` 选项打包应用

		$ cd myproject
		$ wget http://d.defold.com/archive/<sha1>/bob/bob.jar
		$ java -jar bob.jar --platform armv7-darwin build --with-symbols debug --archive bundle -bo build/ios -mp <app>.mobileprovision --identity "iPhone Developer: Your Name (ID)"

* 安装应用, 可以通过 `Xcode`, `iTunes` 或者 [ios-deploy](https://github.com/ios-control/ios-deploy)

		$ ios-deploy -b <AppName>.ipa

* 得到 `.dSYM` 文件夹 (即调试 symbols)

	* 如果没使用原生扩展, 可以从 [d.defold.com](http://d.defold.com) 下载 `.dSYM` 文件

	* 如果使用了原生扩展, 可以使用 [bob.jar](https://www.defold.com/manuals/bob/) 生成 `.dSYM` 文件夹. 只需要 building (不需要 archive 和 bundling):

			$ cd myproject
			$ unzip .internal/cache/arm64-ios/build.zip
			$ mv dmengine.dSYM <AppName>.dSYM
			$ mv <AppName>.dSYM/Contents/Resources/DWARF/dmengine <AppName>.dSYM/Contents/Resources/DWARF/<AppName>


### 创建项目

要正确的调试, 我们需要一个项目, 以及一个代码映射（source map）.
这次项目不是用来编译的, 只是调试举例.

*新建 Xcode 项目, 选择 `Game` 模板

	![project_template](images/extensions/debugging/ios/project_template.png)

* 指定一个名字 (例如 `debug`) 并且使用默认设置

* 选择一个存放项目的目录

* 为应用加入代码文件

	![add_files](images/extensions/debugging/ios/add_files.png)

* 确保 "Copy items if needed" 未选中.

	![add_source](images/extensions/debugging/ios/add_source.png)

* 结果是这样

	![added_source](images/extensions/debugging/ios/added_source.png)


* 关闭 `Build` 步骤

	![edit_scheme](images/extensions/debugging/ios/edit_scheme.png)

	![disable_build](images/extensions/debugging/ios/disable_build.png)

* 设置 `Deployment target` 版本

	![deployment_version](images/extensions/debugging/ios/deployment_version.png)

* 设置目标设备

	![select_device](images/extensions/debugging/ios/select_device.png)


### 启动调试器

调试应用有如下方法

* 可以使用 `Debug` -> `Attach to process...` 然后选择要调试应用

* 也可以选择 `Attach to process by PID or Process name`

	![select_device](images/extensions/debugging/ios/attach_to_process_name.png)

	然后在设备上启动应用

* 在 `Edit Scheme` 中加入 <AppName>.app 作为可运行文件夹

### 调试 symbols

**要使用 lldb, 运行必须先暂停**

* 把 `.dSYM` 目录加入到 lldb 中

		(lldb) add-dsym <PathTo.dSYM>

	![add_dsym](images/extensions/debugging/ios/add_dsym.png)

* 确认 `lldb` 成功读取 symbols

		(lldb) image list <AppName>

### 路径映射

* 加入引擎路径 (根据你的安装目录自行调整)

		(lldb) settings set target.source-map /Users/builder/ci/builds/engine-ios-64-master/build /Users/mathiaswesterdahl/work/defold
		(lldb) settings append target.source-map /private/var/folders/m5/bcw7ykhd6vq9lwjzq1mkp8j00000gn/T/job4836347589046353012/upload/videoplayer/src /Users/mathiaswesterdahl/work/projects/extension-videoplayer-native/videoplayer/src

	* 从可运行文件夹里可以得到 job 文件夹.
	job 文件夹命名类似这样 `job1298751322870374150`, 每次都是随机数字.

			$ dsymutil -dump-debug-map <executable> 2>&1 >/dev/null | grep /job

* 验证路径映射

		(lldb) settings show target.source-map

可以使用如下命令确定 symbol 的源代码文件

	(lldb) image lookup -va <SymbolName>


### 断点

* 从 project 视图打开一个文件, 然后设置断点

	![breakpoint](images/extensions/debugging/ios/breakpoint.png)

## 注意

### 检查二进制文件 UUID

为了让调试器接受 `.dSYM` 文件夹, UUID 需要与可运行文件的 UUID 相匹配. 你可以这样检查 UUID:

	$ dwarfdump -u <PathToBinary>
