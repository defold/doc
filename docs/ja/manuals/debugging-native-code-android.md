---
title: Android でのデバッグ
brief: このマニュアルでは、Android Studio を使用してビルドをデバッグする方法を説明します。
---

# Android でのデバッグ {#debugging-on-android}

ここでは、Google の Android オペレーティングシステム向けの公式 IDE である [Android Studio](https://developer.android.com/studio/) を使用して、ビルドをデバッグする方法を説明します。


## Android Studio

* *game.project* の `android.debuggable` オプションを設定して、バンドル（bundle）の準備をします。

	![android.debuggable](images/extensions/debugging/android/game_project_debuggable.png)

* デバッグモードでアプリのバンドルを作成し、任意のフォルダーに保存します。

	![Android のバンドル作成](images/extensions/debugging/android/bundle_android.png)

* [Android Studio](https://developer.android.com/studio/) を起動します。

* `Profile or debug APK` を選択します。

	![APK のデバッグ](images/extensions/debugging/android/android_profile_or_debug.png)

* 作成した apk バンドルを選択します。

	![apk の選択](images/extensions/debugging/android/android_select_apk.png)

* メインの `.so` ファイルを選択し、デバッグシンボルが含まれていることを確認します。

	![.so ファイルの選択](images/extensions/debugging/android/android_missing_symbols.png)

* 含まれていない場合は、シンボルを削除していない `.so` ファイルをアップロードします。（サイズは約 20mb です）

* パスマッピングを使うと、実行ファイルがビルドされた場所（クラウド内）の各パスを、ローカルドライブ上の実際のフォルダーに対応付けられます。

* .so ファイルを選択し、ローカルドライブへのマッピングを追加します。

	![パスマッピングの設定1](images/extensions/debugging/android/path_mappings_android.png)

	![パスマッピングの設定2](images/extensions/debugging/android/path_mappings_android2.png)

* エンジンのソースコードにアクセスできる場合は、そのパスマッピングも追加します。

* 現在デバッグしているバージョンを必ずチェックアウトします。

	defold$ git checkout 1.2.148

* `Apply changes` をクリックします。

* これで、マッピングされたソースコードがプロジェクトに表示されるはずです。

	![ソースコードのマッピング](images/extensions/debugging/android/source_mappings_android.png)

* ブレークポイントを追加します。

	![ブレークポイント](images/extensions/debugging/android/breakpoint_android.png)

* `Run` -> `Debug "Appname"` を選択し、ブレークポイントで停止させたいコードを実行します。

	![ブレークポイント](images/extensions/debugging/android/callstack_variables_android.png)

* これで、コールスタック内をステップ実行したり、変数を調べたりできます。


## 注意事項 {#notes}

### ネイティブ拡張のジョブフォルダー {#native-extension-job-folder}

現在、ネイティブ拡張（native extension）の開発では、このワークフローに少し手間がかかります。これは、ジョブフォルダーの名前が
ビルドごとにランダムになり、ビルドのたびにパスマッピングが無効になるためです。

ただし、1回のデバッグセッションでは問題なく機能します。

パスマッピングは、Android Studio プロジェクトの `.iml` ファイルに保存されます。

ジョブフォルダーは実行ファイルから取得できます。

```sh
$ arm-linux-androideabi-readelf --string-dump=.debug_str build/armv7-android/libdmengine.so | grep /job
```

ジョブフォルダーの名前は `job1298751322870374150` のような形式で、毎回ランダムな数字が使われます。

