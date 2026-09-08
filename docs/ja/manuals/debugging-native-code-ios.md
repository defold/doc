---
title: iOS/macOS でのデバッグ
brief: このマニュアルでは、Xcode を使用してビルド成果物をデバッグする方法を説明します。
---

# iOS/macOS でのデバッグ {#debugging-on-iosmacos}

ここでは、Apple が macOS と iOS 向けの開発に推奨する IDE である [Xcode](https://developer.apple.com/xcode/) を使用して、ビルド成果物をデバッグする方法を説明します。

## Xcode

* bob を使用し、`--with-symbols` オプションを付けてアプリのバンドル（bundle）を作成します（[詳細](/manuals/debugging-native-code/#symbolicate-a-callstack)）：

```sh
$ cd myproject
$ wget http://d.defold.com/archive/<sha1>/bob/bob.jar
$ java -jar bob.jar --platform armv7-darwin build --with-symbols --variant debug --archive bundle -bo build/ios -mp <app>.mobileprovision --identity "iPhone Developer: Your Name (ID)"
```

* `Xcode`、`iTunes`、[ios-deploy](https://github.com/ios-control/ios-deploy) のいずれかでアプリをインストールします。

```sh
$ ios-deploy -b <AppName>.ipa
```

* `.dSYM` フォルダー（デバッグシンボル）を取得します。

	* ネイティブ拡張（native extension）を使用していない場合は、[d.defold.com](http://d.defold.com) から `.dSYM` ファイルをダウンロードできます。

	* ネイティブ拡張を使用している場合は、[bob.jar](https://www.defold.com/manuals/bob/) でビルドすると `.dSYM` フォルダーが生成されます。ビルドだけで十分です（アーカイブやバンドルの作成は不要です）：

```sh
$ cd myproject
$ unzip .internal/cache/arm64-ios/build.zip
$ mv dmengine.dSYM <AppName>.dSYM
$ mv <AppName>.dSYM/Contents/Resources/DWARF/dmengine <AppName>.dSYM/Contents/Resources/DWARF/<AppName>
```

### プロジェクトの作成 {#create-project}

適切にデバッグするには、プロジェクトを用意し、ソースコードのマッピングを設定する必要があります。
このプロジェクトはビルドには使用せず、デバッグだけに使用します。

* 新しい Xcode プロジェクトを作成し、`Game` テンプレートを選択します。

	![プロジェクトテンプレート](images/extensions/debugging/ios/project_template.png)

* 名前（例：`debug`）を指定し、デフォルトの設定を選択します。

* プロジェクトを保存するフォルダーを選択します。

* アプリにコードを追加します。

	![ファイルの追加](images/extensions/debugging/ios/add_files.png)

* 「Copy items if needed」のチェックが外れていることを確認します。

	![ソースの追加](images/extensions/debugging/ios/add_source.png)

* 最終的に次のようになります。

	![追加されたソース](images/extensions/debugging/ios/added_source.png)


* `Build` ステップを無効にします。

	![スキームの編集](images/extensions/debugging/ios/edit_scheme.png)

	![ビルドの無効化](images/extensions/debugging/ios/disable_build.png)

* `Deployment target` のバージョンを、デバイスの iOS バージョンより大きくなるように設定します。

	![デプロイの対象バージョン](images/extensions/debugging/ios/deployment_version.png)

* 対象デバイスを選択します。

	![デバイスの選択](images/extensions/debugging/ios/select_device.png)


### デバッガーの起動 {#launch-the-debugger}

アプリをデバッグするには、いくつかの方法があります。

1. `Debug` -> `Attach to process...` を選択し、そこからアプリを選択します。

2. または、`Attach to process by PID or Process name` を選択します。

	![デバイスの選択](images/extensions/debugging/ios/attach_to_process_name.png)

3. デバイスでアプリを起動します。

4. `Edit Scheme` で <AppName>.app フォルダーを実行ファイルとして追加します。

### デバッグシンボル {#debug-symbols}

**lldb を使用するには、実行を一時停止する必要があります**

* `.dSYM` のパスを lldb に追加します。

```
(lldb) add-dsym <PathTo.dSYM>
```

	![dSYM の追加](images/extensions/debugging/ios/add_dsym.png)

* `lldb` がシンボルを正常に読み込んだことを確認します。

```
(lldb) image list <AppName>
```

### パスのマッピング {#path-mappings}

* エンジンのソースを追加します（必要に応じて変更してください）。

```
(lldb) settings set target.source-map /Users/builder/ci/builds/engine-ios-64-master/build /Users/mathiaswesterdahl/work/defold
(lldb) settings append target.source-map /private/var/folders/m5/bcw7ykhd6vq9lwjzq1mkp8j00000gn/T/job4836347589046353012/upload/videoplayer/src /Users/mathiaswesterdahl/work/projects/extension-videoplayer-native/videoplayer/src
```

* 実行ファイルからジョブフォルダーを取得できます。ジョブフォルダーの名前は `job1298751322870374150` のようになり、毎回ランダムな数値が使われます。

```sh
$ dsymutil -dump-debug-map <executable> 2>&1 >/dev/null | grep /job

```

* ソースのマッピングを確認します。

```
(lldb) settings show target.source-map
```

次のコマンドを使用して、シンボルがどのソースファイルに由来するかを確認できます。

```
(lldb) image lookup -va <SymbolName>
```

### ブレークポイント {#breakpoints}

* プロジェクトビューでファイルを開き、ブレークポイントを設定します。

	![ブレークポイント](images/extensions/debugging/ios/breakpoint.png)

## 注意事項 {#notes}

### バイナリの UUID の確認 {#check-uuid-of-binary}

デバッガーが `.dSYM` フォルダーを受け付けるには、その UUID がデバッグ対象の実行ファイルの UUID と一致する必要があります。次のように UUID を確認できます：

```sh
$ dwarfdump -u <PathToBinary>
```