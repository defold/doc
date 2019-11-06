---
title: Android调试
brief: 此手册介绍了如何调试运行在 Android 设备上的应用.
---

# Android调试

这里列举了一些在 Android 设备上调试应用的方法.

## Android Studio

* 打包前在  `game.project` 打开 `android.debuggable` 选项

	![android.debuggable](images/extensions/debugging/android/game_project_debuggable.png)

* 编译时选择 debug 模式.

	![bundle_android](images/extensions/debugging/android/bundle_android.png)

* 启动 [Android Studio](https://developer.android.com/studio/)

* 选择 `Profile or debug APK`

	![debug_apk](images/extensions/debugging/android/android_profile_or_debug.png)

* 选择刚打包好的apk文件

	![select_apk](images/extensions/debugging/android/android_select_apk.png)

* 选择主 `.so` 文件, 确保其包含调试信息

	![select_so](images/extensions/debugging/android/android_missing_symbols.png)

* 如果没有调试信息, 提交一个带调试信息的 `.so` 文件. (文件大概 20mb 左右)

* 路径映射帮助你重新把应用的各个路径从编译的地方 (在云端) 映射到你的本地目录下.

* 选择 .so 文件, 再添加一个到本地的映射

	![path_mapping1](images/extensions/debugging/android/path_mappings_android.png)

	![path_mapping2](images/extensions/debugging/android/path_mappings_android2.png)

* 如果你访问了引擎代码, 同样要添加一个对引擎代码的路径映射

		* 确定checkout的是你正在调试的版本

			defold$ git checkout 1.2.148

* 点击 `Apply changes`

* 现在你应该可以看到你的项目的代码映射了

	![source](images/extensions/debugging/android/source_mappings_android.png)

* 加入断点

	![breakpoint](images/extensions/debugging/android/breakpoint_android.png)

* 点击 `Run` -> `Debug "Appname"` 然后调用加入断点代码

	![breakpoint](images/extensions/debugging/android/callstack_variables_android.png)

* 现在你就可以在调用栈中步进调试和查看变量状态了


## 注意

### 原生扩展 job 目录

目前, 工作流对于项目开发有点麻烦. 这是因为job目录名是随机的, 没法进行路径映射.

但是对于调试来说还是可行的.

路径映射保存在 Android Studio 项目的 <project>.iml 文件中.

这样就能获得当前应用的job目录名

	$ arm-linux-androideabi-readelf --string-dump=.debug_str build/armv7-android/libdmengine.so | grep /job

job目录命名类似 `job1298751322870374150`, 每次编译都随机命名.

