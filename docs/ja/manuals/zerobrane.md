---
title: ZeroBrane Studio によるデバッグ
brief: このマニュアルでは、ZeroBrane Studio を使って Defold の Lua コードをデバッグする方法を説明します。
---

# ZeroBrane Studio による Lua スクリプトのデバッグ {#debugging-lua-scripts-with-zerobrane-studio}

Defold にはデバッガーが組み込まれていますが、無料でオープンソースの Lua IDE である _ZeroBrane Studio_ を外部デバッガーとして実行することもできます。デバッグ機能を使うには、ZeroBrane Studio をインストールする必要があります。このプログラムはクロスプラットフォームに対応し、macOS と Windows の両方で動作します。

http://studio.zerobrane.com から「ZeroBrane Studio」をダウンロードします。

## ZeroBrane の設定 {#zerobrane-configuration}

ZeroBrane がプロジェクト内のファイルを見つけられるようにするには、Defold プロジェクトのディレクトリの場所を指定する必要があります。この場所を調べるには、Defold プロジェクトのルートにあるファイルで <kbd>Show in Desktop</kbd> オプションを使うと便利です。

1. *game.project* を右クリックします。
2. <kbd>Show in Desktop</kbd> を選択します。

![Finder で表示](images/zerobrane/show_in_desktop.png)

## ZeroBrane のセットアップ {#to-set-up-zerobrane}

ZeroBrane をセットアップするには、<kbd>Project ▸ Project Directory ▸ Choose...</kbd> を選択します。

![セットアップ](images/zerobrane/setup.png)

現在の Defold プロジェクトのディレクトリに合わせて設定すると、ZeroBrane で Defold プロジェクトのディレクトリツリーを確認し、ファイルをたどって開けるようになるはずです。

必須ではありませんが推奨するその他の設定変更については、このドキュメントの後半で説明します。

## デバッグサーバーの起動 {#starting-the-debugging-server}

デバッグセッションを開始する前に、ZeroBrane に組み込まれたデバッグサーバーを起動する必要があります。起動用のメニュー項目は <kbd>Project</kbd> メニューにあります。<kbd>Project ▸ Start Debugger Server</kbd> を選択するだけで起動できます。

![デバッガーの起動](images/zerobrane/startdebug.png)

## アプリケーションをデバッガーに接続する {#connecting-your-application-to-the-debugger}

デバッグは Defold アプリケーションの生存期間中のどの時点でも開始できますが、Lua スクリプトから明示的に開始する必要があります。デバッグセッションを開始する Lua コードは次のとおりです。

::: sidenote
`dbg.start()` を呼び出したときにゲームが終了する場合、ZeroBrane が問題を検出し、ゲームに終了コマンドを送信している可能性があります。理由は不明ですが、ZeroBrane でデバッグセッションを開始するにはファイルが開かれている必要があり、そうでない場合は次のメッセージが出力されます。
"Can't start debugging without an opened file or with the current file not being saved 'untitled.lua')."
このエラーを解消するには、`dbg.start()` を追加したファイルを ZeroBrane で開きます。
:::

```lua
dbg = require "builtins.scripts.mobdebug"
dbg.start()
```

上記のコードをアプリケーションに挿入すると、ZeroBrane のデバッグサーバーに接続し（デフォルトでは "localhost" 経由）、次に実行する文で一時停止します。

```txt
Debugger server started at localhost:8172.
Mapped remote request for '/' to '/Users/my_user/Documents/Projects/Defold_project/'.
Debugging session started in '/Users/my_user/Documents/Projects/Defold_project'.
```

これで ZeroBrane のデバッグ機能を使えるようになります。ステップ実行、状態の確認、ブレークポイントの追加や削除などができます。

::: sidenote
デバッグは、デバッグを開始した Lua コンテキストに対してのみ有効になります。*game.project* で "shared_state" を有効にすると、どこでデバッグを開始したかにかかわらず、アプリケーション全体をデバッグできます。
:::

![ステップ実行](images/zerobrane/code.png)

接続に失敗した場合（デバッグサーバーが起動していない場合など）、接続の試行後、アプリケーションは通常どおり実行を続けます。

## リモートデバッグ {#remote-debugging}

デバッグには通常のネットワーク接続（TCP）を使うため、リモートでデバッグできます。つまり、モバイルデバイス上で実行中のアプリケーションをデバッグできます。

変更が必要なのは、デバッグを開始するコマンドだけです。デフォルトでは `start()` は localhost への接続を試みますが、リモートデバッグでは、次のように ZeroBrane のデバッグサーバーのアドレスを手動で指定する必要があります。

```lua
dbg = require "builtins.scripts.mobdebug"
dbg.start("192.168.5.101")
```

そのため、リモートデバイスからネットワークに接続できることと、ファイアウォールなどのソフトウェアがポート 8172 の TCP 接続を許可していることを確認することも重要です。そうしないと、アプリケーションが起動時にデバッグサーバーへの接続を試みる際、処理が止まってしまう可能性があります。

## その他の推奨する ZeroBrane 設定 {#other-recommended-zerobrane-setting}

デバッグ中に ZeroBrane が Lua スクリプトファイルを自動で開くように設定できます。これにより、ほかのソースファイルを手動で開くことなく、その中の関数にステップインできます。

最初にエディターの設定ファイルを開きます。このファイルのユーザー版を変更することをお勧めします。

- <kbd>Edit ▸ Preferences ▸ Settings: User</kbd> を選択します。
- 設定ファイルに次の内容を追加します。

  ```txt
  - to automatically open files requested during debugging
  editor.autoactivate = true
  ```

- ZeroBrane を再起動します。

![その他の推奨設定](images/zerobrane/otherrecommended.png)
