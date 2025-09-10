---
title: Android 平台调试
brief: 本手册描述了如何使用 Android Studio 调试构建版本。
---

# Android 平台调试

这里我们描述如何使用 [Android Studio](https://developer.android.com/studio/)（Google 的 Android 操作系统的官方 IDE）来调试构建版本。


## Android Studio

* 通过在 *game.project* 中设置 `android.debuggable` 选项来准备捆绑包

	![android.debuggable](images/extensions/debugging/android/game_project_debuggable.png)

* 在调试模式下将应用程序捆绑到您选择的文件夹中

	![bundle_android](images/extensions/debugging/android/bundle_android.png)

* 启动 [Android Studio](https://developer.android.com/studio/)

* 选择 `Profile or debug APK`

	![debug_apk](images/extensions/debugging/android/android_profile_or_debug.png)

* 选择您刚刚创建的 apk 捆绑包

	![select_apk](images/extensions/debugging/android/android_select_apk.png)

* 选择主要的 `.so` 文件，并确保它具有调试符号

	![select_so](images/extensions/debugging/android/android_missing_symbols.png)

* 如果没有，上传一个未剥离的 `.so` 文件。（大小约为 20mb）

* 路径映射帮助您重新映射从可执行文件构建位置（在云端）到本地驱动器上的实际文件夹的各个路径。

* 选择 .so 文件，然后向您的本地驱动器添加映射

	![path_mapping1](images/extensions/debugging/android/path_mappings_android.png)

	![path_mapping2](images/extensions/debugging/android/path_mappings_android2.png)

* 如果您有权访问引擎源代码，也为其添加路径映射。

* 确保检出您当前正在调试的版本

	defold$ git checkout 1.2.148

* 按 `Apply changes`

* 您现在应该在项目中看到映射的源代码

	![source](images/extensions/debugging/android/source_mappings_android.png)

* 添加断点

	![breakpoint](images/extensions/debugging/android/breakpoint_android.png)

* 按 `Run` -> `Debug "Appname"` 并调用您打算中断进入的代码

	![breakpoint](images/extensions/debugging/android/callstack_variables_android.png)

* 您现在可以在调用堆栈中步进以及检查变量


## 注意事项

### 原生扩展作业文件夹

目前，工作流程对开发来说有点麻烦。这是因为作业文件夹名称对于每个构建都是随机的，使得每次构建的路径映射都无效。

然而，它对于调试会话工作得很好。

路径映射存储在 Android Studio 项目的项目 `.iml` 文件中。

可以从可执行文件获取作业文件夹

```sh
$ arm-linux-androideabi-readelf --string-dump=.debug_str build/armv7-android/libdmengine.so | grep /job
```

作业文件夹的命名类似于 `job1298751322870374150`，每次都有不同的随机数。


