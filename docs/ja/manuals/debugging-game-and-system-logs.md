---
title: デバッグ - ゲームログとシステムログ
brief: このマニュアルでは、ゲームログとシステムログの確認方法を説明します。
---

# ゲームログとシステムログ {#game-and-system-log}

ゲームログには、エンジン、ネイティブ拡張（native extension）、ゲームロジックからのすべての出力が表示されます。スクリプトや Lua モジュールから [print()](/ref/stable/base/#print:...) コマンドと [pprint()](/ref/stable/builtins/?q=pprint#pprint:v) コマンドを使って、ゲームログに情報を表示できます。ネイティブ拡張からゲームログに書き込むには、[`dmLog` 名前空間](/ref/stable/dmLog/) の関数を使えます。ゲームログは、エディター、ターミナルウィンドウ、プラットフォーム固有のツール、またはログファイルで確認できます。

システムログはオペレーティングシステムが生成するもので、問題の特定に役立つ追加情報を得られる場合があります。システムログには、クラッシュ時のスタックトレースやメモリ不足の警告が含まれることがあります。

::: important
コンソールや画面上へのログ出力は、デバッグビルド（Debug）でのみ情報を表示します。リリースビルド（Release）ではコンソールログは空ですが、プロジェクト設定の「Write Log File」を「Always」に設定すると、リリースビルドでもファイルへのログの記録を有効にできます。詳しくは後述します。
:::

## エディターでゲームログを確認する {#reading-the-game-log-from-the-editor}

エディターからローカルでゲームを実行するか、[モバイル開発用アプリ](/manuals/dev-app) に接続して実行すると、すべての出力がエディターのコンソールペインに表示されます。

![エディター 2](images/editor/editor2_overview.png)

## ターミナルでゲームログを確認する {#reading-the-game-log-from-the-terminal}

ターミナルから Defold のゲームを実行すると、そのターミナルウィンドウにログが表示されます。Windows と Linux では、ターミナルに実行ファイルの名前を入力してゲームを起動します。macOS では、.app ファイル内からエンジンを起動する必要があります。

```
$ > ./mygame.app/Contents/MacOS/mygame
```

## プラットフォーム固有のツールでゲームログとシステムログを確認する {#reading-game-and-system-logs-using-platform-specific-tools}

### HTML5

ほとんどのブラウザーが提供する開発者ツールでログを確認できます。

* [Chrome](https://developers.google.com/web/tools/chrome-devtools/console) - Menu > More Tools > Developer Tools
* [Firefox](https://developer.mozilla.org/en-US/docs/Tools/Browser_Console) - Tools > Web Developer > Web Console
* [Edge](https://docs.microsoft.com/en-us/microsoft-edge/devtools-guide/console)
* [Safari](https://support.apple.com/guide/safari-developer/log-messages-with-the-console-dev4e7dedc90/mac) - Develop > Show JavaScript Console

### Android

Android Debug Bridge（ADB）ツールを使って、ゲームログとシステムログを表示できます。

:[Android ADB](../shared/android-adb.md)

インストールと設定が完了したら、デバイスを USB で接続し、ターミナルを開いて次のコマンドを実行します。

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat
```

デバイスからのすべての出力が、ゲームからの出力とともに現在のターミナルに表示されます。

Defold アプリケーションからの出力のみを表示したい場合は、次のコマンドを使います。

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat -s defold
--------- beginning of /dev/log/system
--------- beginning of /dev/log/main
I/defold  ( 6210): INFO:ENGINE: Defold Engine 1.2.50 (8d1b912)
I/defold  ( 6210): INFO:ENGINE: Loading data from:
I/defold  ( 6210): INFO:ENGINE: Initialized sound device 'default'
I/defold  ( 6210):
D/defold  ( 6210): DEBUG:SCRIPT: Hello there, log!
...
```

### iOS

iOS でゲームログとシステムログを確認するには、複数の方法があります。

1. [Console ツール](https://support.apple.com/guide/console/welcome/mac) を使って、ゲームログとシステムログを確認できます。
2. LLDB デバッガーを、デバイスで実行中のゲームに接続できます。ゲームをデバッグするには、デバッグに使うデバイスを含む「Apple Developer Provisioning Profile」でゲームに署名する必要があります。エディターからゲームのバンドル（bundle）を作成し、バンドル作成ダイアログでプロビジョニングプロファイルを指定します（iOS 向けのバンドル作成は macOS でのみ利用できます）。

ゲームを起動してデバッガーを接続するには、[ios-deploy](https://github.com/phonegap/ios-deploy) というツールが必要です。ターミナルで次のコマンドを実行して、ゲームをインストールし、デバッグします。

```txt
$ ios-deploy --debug --bundle <path_to_game.app> # NOTE: not the .ipa file
```

これにより、デバイスにアプリがインストールされ、起動し、LLDB デバッガーが自動的に接続されます。LLDB を初めて使う場合は、[LLDB 入門](https://developer.apple.com/library/content/documentation/IDEs/Conceptual/gdb_to_lldb_transition_guide/document/lldb-basics.html) をお読みください。


## ログファイルでゲームログを確認する {#reading-the-game-log-from-the-log-file}

ファイルへのログの記録を制御するには、*game.project* のプロジェクト設定「Write Log File」を使います。

- 「Never」: ログファイルを書き込みません。
- 「Debug」: デバッグビルドでのみログファイルを書き込みます。
- 「Always」: デバッグビルドとリリースビルドの両方でログファイルを書き込みます。

有効にすると、ゲームのすべての出力がディスク上の「`log.txt`」という名前のファイルに書き込まれます。デバイスでゲームを実行している場合、このファイルを取り出す方法は次のとおりです。

iOS
: デバイスを、macOS と Xcode がインストールされたコンピューターに接続します。

  Xcode を開き、<kbd>Window ▸ Devices and Simulators</kbd> に移動します。

  一覧でデバイスを選択し、*Installed Apps* 一覧で該当するアプリを選択します。

  一覧の下にある歯車アイコンをクリックし、<kbd>Download Container...</kbd> を選択します。

  ![コンテナーのダウンロード](images/debugging/download_container.png)

  コンテナーを取り出すと、*Finder* に表示されます。コンテナーを右クリックし、<kbd>Show Package Content</kbd> を選択します。「`log.txt`」ファイルを探します。このファイルは「`AppData/Documents/`」にあるはずです。

Android(
: 「`log.txt`」を取り出せるかどうかは、OS のバージョンとメーカーによって異なります。短く簡潔な[手順ガイド](https://stackoverflow.com/a/48077004/129360)を参照してください。
