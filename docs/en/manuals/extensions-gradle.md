---
title: Using Gradle dependencies in Android builds
brief: This manual explains how to use Gradle to resolve dependencies in Android builds.
---

# Gradle for Android

Contrary to how Android applications are typically built, Defold does not use [Gradle](https://gradle.org/) for the entire build process. Instead Defold uses Android command line tools such as `aapt2` and `bundletool` directly in the local build and only leverages Gradle while resolving dependencies on the build server.


## Resolving dependencies

Native extensions can include a `build.gradle` file in the `manifests/android` folder to specify the extension dependencies. Example:

```
repositories {
    mavenCentral()
}

dependencies {
    implementation 'com.google.firebase:firebase-installations:17.2.0'
    implementation 'com.google.android.gms:play-services-base:18.2.0'
}
```

The build server will collect the `build.gradle` files from all the extensions and use these to resolve all dependencies and include them when building the native code.

Examples:

* https://github.com/defold/extension-firebase/blob/master/firebase/manifests/android/build.gradle
* https://github.com/defold/extension-facebook/blob/master/facebook/manifests/android/build.gradle