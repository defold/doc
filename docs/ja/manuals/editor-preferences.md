---
title: エディターの環境設定
brief: Preferences ウィンドウからエディターの設定を変更できます。
---

# エディターの環境設定 {#editor-preferences}

Preferences ウィンドウからエディターの設定を変更できます。環境設定ウィンドウは <kbd>File -> Preferences</kbd> メニューから開きます。

## General

![](images/editor/preferences_general.png)

Load External Changes on App Focus
: エディターにフォーカスが移ったときに、外部で行われた変更をスキャンする機能を有効にします。

Open Bundle Target Folder
: バンドル（bundle）の作成処理が完了した後に、バンドルの出力先フォルダーを開く機能を有効にします。

Enable Texture Compression
: エディターから実行するすべてのビルドで [テクスチャ圧縮](/manuals/texture-profiles) を有効にします。

Escape Quits Game
: <kbd>Esc</kbd> キーで、実行中のゲームのビルドを終了します。

Track Active Tab in Asset Browser
: *Editor* ペインで選択したタブで編集中のファイルを、Asset Browser（*Asset* ペインとも呼ばれます）で選択します。

Lint Code on Build
: プロジェクトをビルドするときに [コードの静的解析](/manuals/writing-code/#linting-configuration) を有効にします。このオプションは既定で有効ですが、大規模なプロジェクトで静的解析に時間がかかりすぎる場合は無効にできます。

Engine Arguments
: エディターでビルドして実行するときに、dmengine 実行ファイルに渡す引数です。
 引数は1行に1つずつ指定します。例:
 ```
--config=bootstrap.main_collection=/my dir/1.collectionc
--verbose
--graphics-adapter=vulkan
```


## Code

![](images/editor/preferences_code.png)

Custom Editor
: 外部エディターへの絶対パスです。macOS では、.app 内の実行ファイルへのパスを指定します（例: `/Applications/Atom.app/Contents/MacOS/Atom`）。

Open File
: カスタムエディターで開くファイルを指定するためのパターンです。パターン内の `{file}` は、開くファイルの名前に置き換えられます。

Open File at Line
: カスタムエディターで開くファイルと行番号を指定するためのパターンです。パターン内の `{file}` は開くファイルの名前に、`{line}` は行番号に置き換えられます。

Code editor font
: コードエディターで使用する、システムにインストールされたフォントの名前です。

Zoom on Scroll
: コードエディターで Cmd/Ctrl キーを押しながらスクロールしたときに、フォントサイズを変更するかどうかを指定します。

Auto-insert closing parens
: コードの編集中に、対応する閉じ文字を自動的に挿入します。このオプションは既定で有効です。

Format on save
: 保存時に、開いている変更済みのコードファイルに言語サーバーのフォーマッターを実行します。既定では無効です。言語サーバーが整形をサポートしている必要があります。ドキュメントや選択範囲を手動で整形するには、[コードの整形](/manuals/writing-code/#formatting-code)を参照してください。


### スクリプトファイルを Visual Studio Code で開く {#open-script-files-in-visual-studio-code}

![](images/editor/preferences_vscode.png)

Defold エディターからスクリプトファイルを Visual Studio Code で直接開くには、次の実行ファイルのパスを指定して設定する必要があります。

- MacOS: `/Applications/Visual Studio Code.app/Contents/MacOS/Electron`
- Linux: `/usr/bin/code`
- Windows: `C:\Program Files\Microsoft VS Code\Code.exe`

 特定のファイルと行を開くには、次のパラメーターを設定します。

- Open File: `. {file}`
- Open File at Line: `. -g {file}:{line}`

ここで `.` という文字は、個別のファイルではなくワークスペース全体を開くために必要です。


## Extensions

![](images/editor/preferences_extensions.png)

Build Server
: [ネイティブ拡張（native extension）](/manuals/extensions) を含むプロジェクトのビルド時に使用するビルドサーバーの URL です。ビルドサーバーへのアクセス時に認証するため、URL にユーザー名とアクセストークンを追加できます。ユーザー名とアクセストークンは `username:token@build.defold.com` という形式で指定します。Nintendo Switch 向けのビルドや、認証を有効にした独自のビルドサーバーインスタンスを実行する場合には、認証付きのアクセスが必要です（詳しくは [ビルドサーバーのドキュメント](https://github.com/defold/extender/blob/dev/README_SECURITY.md) を参照してください）。ユーザー名とパスワードは、システムの環境変数 `DM_EXTENDER_USERNAME` と `DM_EXTENDER_PASSWORD` でも設定できます。

Build Server Username
: 認証に使用するユーザー名です。

Build Server Password
: 認証に使用するパスワードです。環境設定ファイルに暗号化して保存されます。

Build Server Headers
: ネイティブ拡張のビルド時にビルドサーバーに送信する追加のヘッダーです。extender で CloudFlare などのサービスを使用する際に重要です。

## Tools

![](images/editor/preferences_tools.png)

ADB path
: このシステムにインストールされた [ADB](https://developer.android.com/tools/adb) コマンドラインツールへのパスです。システムに ADB がインストールされている場合、Defold エディターはそれを使用して、バンドルとして作成した Android APK を接続中の Android デバイスにインストールして実行します。既定では、エディターは一般的な場所に ADB がインストールされているかどうかを確認するため、独自の場所に ADB をインストールしている場合にのみパスを指定する必要があります。

ios-deploy path
: このシステムにインストールされた [ios-deploy](https://github.com/ios-control/ios-deploy) コマンドラインツールへのパスです（macOS のみに該当します）。ADB path と同様に、Defold エディターはこのツールを使用して、バンドルとして作成した iOS アプリケーションを接続中の iPhone にインストールして実行します。既定では、エディターは一般的な場所に ios-deploy がインストールされているかどうかを確認するため、ios-deploy を独自の方法でインストールしている場合にのみパスを指定する必要があります。

## Keymap

![](images/editor/preferences_keymap.png)

Keymap タブでは、エディターのキーボードショートカットとマウス操作を設定できます。コマンドを変更するには、そのコマンドをダブルクリックするか、<kbd>Enter</kbd> または <kbd>Space</kbd> を押すか、行のコンテキストメニューを使用します。

キーボードショートカットは、*Shortcuts* 列にキーの組み合わせとして表示されます。マウス操作も同じ一覧に表示され、バッジが付きます。

- <kbd>MB</kbd> はマウスボタンのバインディングを表し、<kbd>Shift</kbd>、<kbd>Ctrl</kbd>/<kbd>Control</kbd>、<kbd>Alt</kbd> と組み合わせることもできます。
- <kbd>MM</kbd> はマウス操作で使用する修飾キーを表します。

一部のマウス操作は既定の Scene 2D Camera のバインディングを再利用するため、カスタマイズする前から行にバインディングが表示される場合があります。通常、これらは暗めの色で表示されます。その行にカスタムバインディングを設定すると、Defold は代わりにそのバインディングを使用します。変更を削除し、組み込みの動作または継承した動作に戻すには、*Reset to Defaults* を使用します。

警告はオレンジ色で表示されます。警告にマウスポインターを重ねると詳細を確認できます。通常、警告は次のことを意味します。
- ショートカットでテキストを入力できるため、テキストフィールドでの入力を妨げる可能性があります。
- 同じショートカットまたはマウスのバインディングが、別のコマンドですでに使用されています。
