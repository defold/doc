---
title: Android ビルドで Gradle の依存関係を使用する
brief: このマニュアルでは、Gradle を使用して Android ビルドの依存関係を解決する方法を説明します。
---

# Android 向けの Gradle {#gradle-for-android}

一般的な Android アプリケーションのビルド方法とは異なり、Defold ではビルド処理全体に [Gradle](https://gradle.org/) を使用しません。Defold はローカルでのビルドでは `aapt2` や `bundletool` などの Android コマンドラインツールを直接使用し、ビルドサーバーで依存関係を解決する際にのみ Gradle を利用します。


## 依存関係の解決 {#resolving-dependencies}

ネイティブ拡張（native extension）では、`manifests/android` フォルダーに `build.gradle` ファイルを含めて、拡張の依存関係を指定できます。例:

```
repositories {
    mavenCentral()
}

dependencies {
    implementation 'com.google.firebase:firebase-installations:17.2.0'
    implementation 'com.google.android.gms:play-services-base:18.2.0'
}
```

ビルドサーバーは、すべての拡張から `build.gradle` ファイルを収集し、これらを使用してすべての依存関係を解決し、ネイティブコードのビルド時にそれらを含めます。

例:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/android/)build.gradle
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/android/build.gradle)
