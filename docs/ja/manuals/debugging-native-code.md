---
title: Defold でのネイティブコードのデバッグ
brief: このマニュアルでは、Defold でネイティブコードをデバッグする方法を説明します。
---

# ネイティブコードのデバッグ {#debugging-native-code}

Defold は十分にテストされており、通常の状況でクラッシュすることはほとんどないはずです。ただし、特にゲームがネイティブ拡張（native extension）を使用している場合は、絶対にクラッシュしないと保証することはできません。クラッシュが発生したり、ネイティブコードが期待どおりに動作しなかったりする場合は、いくつかの方法で調査を進められます。

* デバッガーを使ってコードをステップ実行します
* プリントデバッグを使います
* クラッシュログを解析します
* コールスタックをシンボル化します


## デバッガーの使用 {#use-a-debugger}

最も一般的な方法は、デバッガー（`debugger`）を介してコードを実行することです。コードをステップ実行したり、ブレークポイント（`breakpoints`）を設定したりでき、クラッシュが発生すると実行が停止します。

各プラットフォームには複数のデバッガーがあります。

* Visual studio - Windows
* VSCode - Windows, macOS, Linux
* Android Studio - Windows, macOS, Linux
* Xcode - macOS
* WinDBG - Windows
* lldb / gdb - macOS, Linux, (Windows)
* ios-deploy - macOS

各ツールでデバッグできるプラットフォームは次のとおりです。

* Visual studio - Windows + gdbserver をサポートするプラットフォーム（例: Linux/Android）
* VSCode - Windows, macOS (lldb), Linux (lldb/gdb) + gdbserver をサポートするプラットフォーム
* Xcode -  macOS, iOS（[詳細はこちら](/manuals/debugging-native-code-ios)）
* Android Studio - Android（[詳細はこちら](/manuals/debugging-native-code-android)）
* WinDBG - Windows
* lldb/gdb - macOS, Linux, (iOS)
* ios-deploy - iOS（lldb 経由）


## プリントデバッグの使用 {#use-print-debugging}

ネイティブコードをデバッグする最も簡単な方法は、[プリントデバッグ](http://en.wikipedia.org/wiki/Debugging#Techniques)を使うことです。[`dmLog` 名前空間](/ref/stable/dmLog/)の関数を使って、変数を監視したり、実行の流れを示したりできます。いずれのログ関数を使っても、エディターの *Console* ビューと[ゲームログ](/manuals/debugging-game-and-system-logs)に出力されます。


## クラッシュログの解析 {#analyze-a-crash-log}

Defold エンジンは、異常終了を伴うクラッシュが発生すると `_crash` ファイルを保存します。このクラッシュファイルには、システムとクラッシュに関する情報が含まれます。[ゲームログの出力](/manuals/debugging-game-and-system-logs)には、クラッシュファイルの保存場所が記録されます（オペレーティングシステム、デバイス、アプリケーションによって異なります）。

[crash モジュール](https://www.defold.com/ref/crash/)を使って、次のセッションでこのファイルを読み取れます。ファイルを読み取って情報を収集し、コンソールに出力するとともに、クラッシュログの収集に対応した[分析サービス](/tags/stars/analytics/)に送信することをお勧めします。

::: important
Windows では `_crash.dmp` ファイルも生成されます。このファイルはクラッシュのデバッグに役立ちます。
:::

### デバイスからのクラッシュログの取得 {#getting-the-crash-log-from-a-device}

モバイルデバイスでクラッシュが発生した場合は、クラッシュファイルを自分のコンピューターにダウンロードし、ローカルで解析することもできます。

#### Android

アプリが[デバッグ可能](/manuals/project-settings/#android)であれば、[Android Debug Bridge（ADB）ツール](https://developer.android.com/studio/command-line/adb.html)と `adb shell` コマンドを使ってクラッシュログを取得できます。

```
$ adb shell "run-as com.defold.example sh -c 'cat /data/data/com.defold.example/files/_crash'" > ./_crash
```

#### iOS

iTunes では、アプリのコンテナーを表示したり、ダウンロードしたりできます。

`Xcode -> Devices` ウィンドウでも、クラッシュログを選択できます。


## コールスタックのシンボル化 {#symbolicate-a-callstack}

`_crash` ファイルまたは[ログファイル](/manuals/debugging-game-and-system-logs)からコールスタックを取得した場合は、それをシンボル化（symbolicate）できます。これは、コールスタック内の各アドレスをファイル名と行番号に変換することで、根本原因を突き止めるのに役立ちます。

コールスタックに対応する正しいエンジンを使うことが重要です。対応していないと、誤った箇所をデバッグしてしまう可能性が非常に高くなります。[bob](https://www.defold.com/manuals/bob/) でバンドル（bundle）を作成するときは [`--with-symbols`](https://www.defold.com/manuals/bob/) フラグを使うか、エディターのバンドル作成ダイアログで「Generate debug symbols」チェックボックスをオンにします。

* iOS - `build/arm64-ios` 内の `dmengine.dSYM.zip` フォルダーに、iOS ビルドのデバッグシンボルが含まれています。
* macOS - `build/x86_64-macos` 内の `dmengine.dSYM.zip` フォルダーに、macOS ビルドのデバッグシンボルが含まれています。
* Android - バンドル出力フォルダー `projecttitle.apk.symbols/lib/` に、対象アーキテクチャのデバッグシンボルが含まれています。
* Linux - 実行ファイルにデバッグシンボルが含まれています。
* Windows - `build/x86_64-win32` 内の `dmengine.pdb` ファイルに、Windows ビルドのデバッグシンボルが含まれています。
* HTML5 - HTML5 バンドルと同じ場所にある `<project_name>_symbols` ディレクトリには、`<project_name>_wasm.js.symbols` が含まれています。`wasm_pthread-web` アーキテクチャを選択した場合は、`<project_name>_pthread_wasm.js.symbols` も含まれます。

::: important
ゲームを一般公開するたびに、そのリリースのデバッグシンボルをどこかに保存し、どのリリースに対応するかを把握しておくことが非常に重要です。デバッグシンボルがなければ、ネイティブコードのクラッシュをデバッグできません。また、エンジンのシンボルを削除していない（`unstripped`）バージョンも保存しておくことをお勧めします。これにより、コールスタックを最も適切にシンボル化できます。
:::


### Google Play へのシンボルのアップロード {#uploading-symbols-to-google-play}
[デバッグシンボルを Google Play にアップロード](https://developer.android.com/studio/build/shrink-code#android_gradle_plugin_version_40_or_earlier_and_other_build_systems)すると、Google Play に記録されたクラッシュでシンボル化されたコールスタックを表示できます。バンドル出力フォルダー `projecttitle.apk.symbols/lib/` の内容を Zip 圧縮します。このフォルダーには、`arm64-v8a`、`armeabi-v7a`、`x86_64` などのアーキテクチャ名が付いたサブフォルダーが1つ以上含まれています。


### Android のコールスタックのシンボル化 {#symbolicate-an-android-callstack}

1. ビルドフォルダーからエンジンを取得します

```sh
	$ ls <project>/build/<platform>/[lib]dmengine[.exe|.so]
```

2. フォルダーに展開します。

```sh
	$ unzip dmengine.apk -d dmengine_1_2_105
```

3. コールスタックのアドレスを見つけます

	たとえば、シンボル化されていないコールスタックは次のようになります。

	`#00 pc 00257224 libmy_game_name.so`

	ここでは *`00257224`* がアドレスです。

4. アドレスを解決します

```sh
    $ arm-linux-androideabi-addr2line -C -f -e dmengine_1_2_105/lib/armeabi-v7a/libdmengine.so _address_
```

注: [Android のログ](/manuals/debugging-game-and-system-logs)からスタックトレースを取得できた場合は、[ndk-stack](https://developer.android.com/ndk/guides/ndk-stack.html) を使ってシンボル化できる可能性があります。

### iOS のコールスタックのシンボル化 {#symbolicate-an-ios-callstack}

1. ネイティブ拡張を使用している場合は、サーバーからシンボル（.dSYM）を取得できます（bob.jar に `--with-symbols` を渡します）。

```sh
	$ unzip <project>/build/arm64-darwin/build.zip
	# it will produce a Contents/Resources/DWARF/dmengine
```

2. ネイティブ拡張を使用していない場合は、標準のシンボルをダウンロードします。

```sh
	$ wget http://d.defold.com/archive/<sha1>/engine/arm64-darwin/dmengine.dSYM
```

3. ロードアドレスを使ってシンボル化します

	何らかの理由で、コールスタックのアドレスをそのまま指定しても動作しません（ロードアドレスが 0x0 の場合です）。

```sh
		$ atos -arch arm64 -o Contents/Resources/DWARF/dmengine 0x1492c4
```

	# Neither does specifying the load address directly

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp -l0x100000000 0x1492c4
```

	アドレスにロードアドレスを加算すると動作します。

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp 0x1001492c4
		dmCrash::OnCrash(int) (in MyApp) (backtrace_execinfo.cpp:27)
```
