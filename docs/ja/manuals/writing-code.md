---
title: コードの記述
brief: このマニュアルでは、Defold でコードを扱う方法を簡単に説明します。
---

# コードの記述 {#writing-code}

Defold では、タイルマップ（tilemap）やパーティクルエフェクト（particle effect）のエディターなどのビジュアルツールを使って、ゲームコンテンツの多くを作成できますが、ゲームロジックはコードエディターで記述します。ゲームロジックは [Lua プログラミング言語](https://www.lua.org/)で記述し、エンジン自体の拡張は対象プラットフォームのネイティブ言語で記述します。

## Lua コードの記述 {#writing-lua-code}

Defold は、対象プラットフォームに応じて Lua 5.1 と LuaJIT を使用します。ゲームロジックを記述する際は、これらの特定バージョンの Lua の言語仕様に従う必要があります。Defold で Lua を扱う方法の詳細については、[Defold での Lua のマニュアル](/manuals/lua)を参照してください。

## Lua にトランスパイルするほかの言語の使用 {#using-other-languages-that-transpile-to-lua}

Defold は、Lua コードを出力するトランスパイラーの使用をサポートしています。トランスパイラー拡張（transpiler extension）をインストールすると、[Teal](https://github.com/defold/extension-teal) などの別の言語を使って、静的チェックを受ける Lua コードを記述できます。これは制約のあるプレビュー機能です。現在のトランスパイラーのサポートでは、Defold の Lua ランタイムで定義されているモジュールや関数の情報は公開されません。そのため、`go.animate` などの Defold API を使用するには、外部定義を自分で記述する必要があります。

## ネイティブコードの記述 {#writing-native-code}

Defold では、ネイティブコードでゲームエンジンを拡張し、エンジン自体では提供されていないプラットフォーム固有の機能にアクセスできます。また、Lua のパフォーマンスでは不十分な場合（リソースを大量に消費する計算、画像処理など）にもネイティブコードを使用できます。詳細については、[ネイティブ拡張（Native Extensions）のマニュアル](/manuals/extensions/)を参照してください。

## 組み込みのコードエディターの使用 {#using-the-built-in-code-editor}

Defold にはコードエディターが組み込まれています。Lua ファイル（.lua）、Defold のスクリプト（script）ファイル（.script、.gui_script、.render_script）に加え、エディターが標準で扱わない拡張子のファイルも開いて編集できます。また、Lua ファイルとスクリプトファイルのシンタックスハイライトに対応しています。

![](/images/editor/code-editor.png)

### コード補完 {#code-completion}

組み込みのコードエディターは、コードの記述中に関数の補完候補を表示します。

![](/images/editor/codecompletion.png)

<kbd>CTRL</kbd> + <kbd>Space</kbd> を押すと、関数、引数、戻り値に関する追加情報が表示されます。

![](/images/editor/apireference.png)

同梱の Lua 言語サーバーには、Defold API の型アノテーションが含まれます。補完、ホバー情報、診断は、ハッシュ、URL、ベクトル、クォータニオンなどの Defold の型に加え、関数の引数と戻り値を理解します。エディターは、ゲームスクリプトと、`.editor_script` ファイルで使う `editor.*` API のアノテーションを提供します。Defold のコードエディターを使う場合、組み込み API 用に別のアノテーションライブラリを用意する必要はありません。

サードパーティーの拡張 API には、独自のアノテーションが必要な場合があります。

### コードの整形 {#formatting-code}

<kbd>Edit ▸ Format Document/Selection</kbd> を選択するか、<kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>F</kbd> を押すと、言語サーバーのフォーマッターが実行されます。選択範囲がある場合は選択した行を、ない場合はドキュメントを整形します。整形には、対応する整形操作をサポートする言語サーバーが必要です。

保存時に、開いている変更済みのファイルを整形するには、<kbd>Preferences ▸ Code</kbd> で **Format on save** を有効にします。この設定は既定で無効であり、ドキュメントの整形をサポートする言語サーバーが必要です。[Code の環境設定](/manuals/editor-preferences/#code)を参照してください。

### シンボルへの移動 {#jump-to-symbol}

組み込みのコードエディターでは、現在のコードファイル内の関数、オブジェクト、変数などのシンボルを、検索可能な一覧で表示できます。<kbd>View ▸ Jump to Symbol…</kbd> を選択するか、Windows と Linux では <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>O</kbd>、macOS では <kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd> + <kbd>O</kbd> を押します。

入力を始めるとシンボルをあいまい検索できます。矢印キーで検索結果を移動すると、エディターでそれぞれの位置をプレビューできます。<kbd>Enter</kbd> を押すと、選択したシンボルに移動します。<kbd>Esc</kbd> を押すとダイアログを閉じ、元のカーソル位置とスクロール位置に戻ります。

![](/images/editor/jump-to-symbol.png)

### リントの設定 {#linting-configuration}

組み込みのコードエディターは、[Luacheck](https://luacheck.readthedocs.io/en/stable/index.html) と [Lua language server](https://luals.github.io/wiki/diagnostics/) を使用してコードのリントを行います。Luacheck を設定するには、プロジェクトのルートに `.luacheckrc` ファイルを作成します。利用できるオプションの一覧は、[Luacheck の設定ページ](https://luacheck.readthedocs.io/en/stable/config.html)で確認できます。Defold では、Luacheck の設定に次の既定値を使用します。

```lua
unused_args = false      -- don't warn on unused arguments (common for .script files)
max_line_length = false  -- don't warn on long lines
ignore = {
    "611",               -- line contains only whitespace
    "612",               -- line contains trailing whitespace
    "614"                -- trailing whitespace in a comment
},
```

## 外部コードエディターの使用 {#using-an-external-code-editor}

Defold のコードエディターには、コードの記述に必要な基本機能が備わっていますが、より高度な用途や、お気に入りのコードエディターを持つ上級ユーザー向けに、外部エディターでファイルを開くよう Defold を設定することもできます。[Preferences ウィンドウの Code タブ](/manuals/editor-preferences/#code)で、コードの編集に使用する外部エディターを指定できます。

### Visual Studio Code - Defold Kit

Defold Kit は、次の機能を備えた Visual Studio Code のプラグインです。

* 推奨拡張機能のインストール
* Lua のハイライト、自動補完、リント
* 関連する設定のワークスペースへの適用
* Defold API 用の Lua アノテーション
* 依存関係用の Lua アノテーション
* ビルドと起動
* ブレークポイントを使用したデバッグ
* すべてのプラットフォーム向けのバンドル作成
* 接続されたモバイルデバイスへのデプロイ

詳細の確認と Defold Kit のインストールは、[Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=astronachos.defold)から行えます。


## ドキュメント閲覧ソフトウェア {#documentation-software}

コミュニティが作成した [Dash と Zeal](https://forum.defold.com/t/defold-docset-for-dash/2417) 用の API リファレンスパッケージを利用できます。
