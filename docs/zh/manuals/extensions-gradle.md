---
title: 在Android构建中使用Gradle依赖
brief: 本手册解释了如何在Android构建中使用Gradle解析依赖项。
---

# Android的Gradle

与Android应用程序的典型构建方式不同，Defold在整个构建过程中不使用[Gradle](https://gradle.org/)。相反，Defold在本地构建中直接使用Android命令行工具，如`aapt2`和`bundletool`，仅在构建服务器上解析依赖项时利用Gradle。

## 解析依赖项

原生扩展可以在`manifests/android`文件夹中包含一个`build.gradle`文件来指定扩展依赖项。示例：

```
repositories {
    mavenCentral()
}

dependencies {
    implementation 'com.google.firebase:firebase-installations:17.2.0'
    implementation 'com.google.android.gms:play-services-base:18.2.0'
}
```

构建服务器将收集所有扩展中的`build.gradle`文件，并使用这些文件解析所有依赖项，并在构建原生代码时包含它们。

示例：

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/android/)build.gradle
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/android/build.gradle)