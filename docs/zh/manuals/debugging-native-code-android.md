---
title: Android 平台调试
brief: 本教程介绍了在使用 Android Studio 调试游戏的方法.
---

# Android 平台调试

下面介绍了如何使用 [Android Studio](https://developer.android.com/studio/), 即 Google 的 Android 操作系统的官方 IDE, 来调试游戏的方法.


## Android Studio

* 在 *game.project* 中设置 `android.debuggable`

	![android.debuggable](images/extensions/debugging/android/game_project_debuggable.png)

* 在 debug 模式下打包游戏

	![bundle_android](images/extensions/debugging/android/bundle_android.png)

* 启动 [Android Studio](https://developer.android.com/studio/)

* 选择 `Profile or debug APK`

	![debug_apk](images/extensions/debugging/android/android_profile_or_debug.png)

* 选择刚刚输出的apk文件

	![select_apk](images/extensions/debugging/android/android_select_apk.png)

* 选择主 `.so` 文件, 确保里面含有调试信息

	![select_so](images/extensions/debugging/android/android_missing_symbols.png)

* 没有的话可以上传完整 `.so` 文件. (文件大约 20mb)

* 路径映射帮助建立从编译 (在云端) 到本地文件夹的文件对应关系.

* 选择 .so 文件, 添加路径映射

	![path_mapping1](images/extensions/debugging/android/path_mappings_android.png)

	![path_mapping2](images/extensions/debugging/android/path_mappings_android2.png)

* 要是动过引擎源码, 也要对引擎代码添加路径映射

* 注意一定要获取与你所用版本完全一致的引擎版本

	defold$ git checkout 1.2.148

* 点击 `Apply changes`

* 这时路径映射已经生效

	![source](images/extensions/debugging/android/source_mappings_android.png)

* 加断点

	![breakpoint](images/extensions/debugging/android/breakpoint_android.png)

* 点击 `Run` -> `Debug "Appname"` 然后运行断点处的程序

	![breakpoint](images/extensions/debugging/android/callstack_variables_android.png)

* 步进可用, 变量和调用堆栈一目了然


## 注意

### 原生扩展 job 文件夹

目前, 开发流程有点麻烦. 因为job文件夹名是随机的, 每次编译都不一样.

但是还是有办法使用的.

路径映射保存于 Android Studio 项目的 <project>.iml 文件中.

运行下列命令就能得到job文件夹名

	$ arm-linux-androideabi-readelf --string-dump=.debug_str build/armv7-android/libdmengine.so | grep /job

类似 `job1298751322870374150` 这样的名字, 后面的数字每次编译都不相同.

