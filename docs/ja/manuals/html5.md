---
title: Defold での HTML5 プラットフォーム向け開発
brief: このマニュアルでは、HTML5 ゲームの作成手順と、既知の問題や制限事項を説明します。
---

# HTML5 向け開発 {#html5-development}

Defold は、ほかのプラットフォームと同様に、通常のバンドル（bundle）作成メニューから HTML5 プラットフォーム向けのゲームをビルドできます。また、作成されたゲームは通常の HTML ページに埋め込まれ、シンプルなテンプレートシステムでそのスタイルを設定できます。

*game.project* ファイルには、HTML5 固有の設定があります。

![プロジェクト設定](images/html5/html5_project_settings.png)

## ヒープサイズ {#heap-size}

Defold の HTML5 サポートには Emscripten を使用しています（http://en.wikipedia.org/wiki/Emscripten を参照してください）。簡単に言うと、アプリケーションが動作するヒープ用のメモリをサンドボックスとして作成します。デフォルトでは、エンジンは余裕を持った量のメモリ（256 MB）を割り当てます。一般的なゲームには、十分な余裕があるはずです。最適化の一環として、より小さい値を使用することもできます。その場合は、次の手順に従います。

1. *heap_size* を希望する値に設定します。単位はメガバイトです。
2. HTML5 バンドルを作成します（以下を参照してください）。

## HTML5 ビルドのテスト {#testing-html5-build}

HTML5 ビルドをテストするには、HTTP サーバーが必要です。<kbd>Project ▸ Build HTML5</kbd> を選択すると、Defold が HTTP サーバーを作成します。

![HTML5 のビルド](images/html5/html5_build_launch.png)

バンドルをテストするには、リモートの HTTP サーバーにアップロードするか、ローカルサーバーを作成します。たとえば、バンドルのフォルダー内で Python を使って作成できます。
Python 2 の場合:

```sh
python -m SimpleHTTPServer
```

Python 3 の場合:

```sh
python -m http.server
```

または

```sh
python3 -m http.server
```

::: important
`index.html` ファイルをブラウザーで開くだけでは、HTML5 バンドルをテストできません。HTTP サーバーが必要です。
:::

::: important
コンソールに `"wasm streaming compile failed: TypeError: Failed to execute ‘compile’ on ‘WebAssembly’: Incorrect response MIME type. Expected ‘application/wasm’."` というエラーが表示される場合は、サーバーが `.wasm` ファイルに `application/wasm` MIME タイプを使用していることを確認する必要があります。
:::

## HTML5 バンドルの作成 {#creating-html5-bundle}

Defold での HTML5 コンテンツの作成は簡単で、サポートされているほかのすべてのプラットフォームと同じ手順で行えます。メニューから <kbd>Project ▸ Bundle... ▸ HTML5 Application...</kbd> を選択します。

![HTML5 バンドルの作成](images/html5/html5_bundle.png)

HTML5 バンドルは、2つの WebAssembly アーキテクチャをサポートしています。

* `wasm-web` - スレッドを使用しない通常の WebAssembly エンジンです。
* `wasm_pthread-web` - スレッドを使用できる WebAssembly エンジンです。

いずれか一方のアーキテクチャ、または両方を含めることができます。両方を含めた場合、ブラウザーとホスティング環境が対応していればローダーは `wasm_pthread-web` を選択し、対応していなければ `wasm-web` にフォールバックします。正式なターゲット名については、[Bob マニュアル](/manuals/bob/#usage)を参照してください。

::: important
スレッド対応エンジンには、安全な[オリジン間分離](https://developer.mozilla.org/en-US/docs/Web/API/Window/crossOriginIsolated)状態のページで `SharedArrayBuffer` を使用できることが必要です。HTTPS（または localhost）でバンドルを配信し、対応するオリジン間分離用のヘッダーをサーバーに設定します。一般的には、次のヘッダーを使用します。

```txt
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

ページが読み込む異なるオリジンのリソースにも、対応する CORS または Cross-Origin-Resource-Policy ヘッダーが必要です。`wasm_pthread-web` だけを含むバンドルは、これらの要件が満たされていないと実行できません。オリジン間分離に対応していないサイトでゲームをホストする可能性がある場合は、フォールバックとして `wasm-web` を含めてください。
:::

Defold の HTML5 バンドルには、WebAssembly をサポートする新しいブラウザーが必要です。Internet Explorer 11 はサポートされていません。

<kbd>Create bundle</kbd> ボタンをクリックすると、アプリケーションを作成するフォルダーの選択を求められます。エクスポート処理が完了すると、アプリケーションの実行に必要なすべてのファイルがそのフォルダーに作成されます。

## 既知の問題と制限事項 {#known-issues-and-limitations}

* ホットリロード（hot reload） - HTML5 ビルドではホットリロードは動作しません。Defold アプリケーションは、エディターからの更新を受信するために独自の小型ウェブサーバーを実行する必要がありますが、HTML5 ビルドでは実行できないためです。
* Chrome
  * デバッグビルドの動作が遅い - HTML5 のデバッグビルドでは、エラーを検出するためにすべての WebGL グラフィックス呼び出しを検証します。残念ながら、Chrome でテストする場合、この検証は非常に遅くなります。*game.project* の *Engine Arguments* フィールドを `--verify-graphics-calls=false` に設定すると無効にできます。
* ゲームパッドのサポート - HTML5 固有の注意事項と、必要になる可能性のある手順については、[ゲームパッドのドキュメント](/manuals/input-gamepads/#gamepads-in-html5)を参照してください。

## HTML5 バンドルのカスタマイズ {#customizing-html5-bundle}

HTML5 版のゲームを生成すると、Defold はデフォルトのウェブページを用意します。このページは、ゲームの表示方法を決めるスタイルとスクリプトのリソースを参照しています。

アプリケーションをエクスポートするたびに、このコンテンツは新しく作成されます。これらの要素をカスタマイズするには、プロジェクト設定を変更する必要があります。Defold エディターで *game.project* を開き、*html5* セクションまでスクロールします。

![HTML5 セクション](images/html5/html5_section.png)

各オプションの詳細については、[プロジェクト設定マニュアル](/manuals/project-settings/#html5)を参照してください。

::: important
`builtins` フォルダーにあるデフォルトの HTML/CSS テンプレートのファイルは変更できません。変更を適用するには、`builtins` から必要なファイルをコピーして貼り付け、そのファイルを *game.project* に設定します。
:::

::: important
キャンバスにボーダーやパディングを設定しないでください。設定すると、マウス入力の座標が正しくなくなります。
:::

*game.project* では、`Fullscreen` ボタンと `Made with Defold` リンクを無効にできます。
Defold は、`index.html` 用にダークテーマとライトテーマを用意しています。デフォルトはライトテーマですが、`Custom CSS` ファイルを変更すると切り替えられます。また、`Scale Mode` フィールドでは、あらかじめ定義された4つのスケールモードから選択できます。

::: important
*game.project* の `High Dpi` オプション（`Display` セクション）を有効にすると、すべてのスケールモードの計算で現在の画面の DPI が考慮されます。
:::

### Downscale Fit と Fit {#downscale-fit-and-fit}

`Fit` モードでは、元の縦横比を保ちながらゲームのキャンバス全体を画面に表示するように、キャンバスのサイズを変更します。`Downscale Fit` は、ウェブページの内側のサイズがゲームの元のキャンバスより小さい場合にのみサイズを変更する点だけが異なり、ウェブページがゲームの元のキャンバスより大きくても拡大しません。

![HTML5 セクション](images/html5/html5_fit.png)

### Stretch

`Stretch` モードでは、ウェブページの内側全体を埋めるようにキャンバスのサイズを変更します。

![HTML5 セクション](images/html5/html5_stretch.png)

### No Scale
`No Scale` モードでは、キャンバスのサイズは *game.project* ファイルの `[display]` セクションであらかじめ定義したサイズとまったく同じになります。

![HTML5 セクション](images/html5/html5_no_scale.png)

## トークン {#tokens}

`index.html` ファイルの作成には、[Mustache テンプレート言語](https://mustache.github.io/mustache.5.html)を使用します。ビルドまたはバンドル作成時に、HTML と CSS のファイルはコンパイラーで処理されます。このコンパイラーは、特定のトークンをプロジェクト設定に応じた値に置き換えられます。トークンは、文字列をエスケープするかどうかに応じて、常に二重または三重の波括弧（`{{TOKEN}}` または `{{{TOKEN}}}`）で囲みます。この機能は、プロジェクト設定を頻繁に変更する場合や、ほかのプロジェクトでも素材を再利用する場合に便利です。

::: sidenote
Mustache テンプレート言語の詳細については、[マニュアル](https://mustache.github.io/mustache.5.html)を参照してください。
:::

*game.project* のどの設定もトークンとして使用できます。たとえば、`Display` セクションの `Width` の値を使用する場合は、次のようにします。

![Display セクション](images/html5/html5_display.png)

*game.project* をテキストとして開き、`[section_name]` と使用するフィールドの名前を確認します。これらを、`{{section_name.field}}` または `{{{section_name.field}}}` というトークンとして使用できます。

![Display セクション](images/html5/html5_game_project.png)

たとえば、HTML テンプレート内の JavaScript では次のように記述します。

```javascript
function doSomething() {
    var x = {{display.width}};
    // ...
}
```

また、次のカスタムトークンも用意されています。

DEFOLD_SPLASH_IMAGE
: スプラッシュ画像ファイルの名前を出力します。*game.project* の `html5.splash_image` が空の場合は `false` を出力します。


```css
{{#DEFOLD_SPLASH_IMAGE}}
		background-image: url("{{DEFOLD_SPLASH_IMAGE}}");
{{/DEFOLD_SPLASH_IMAGE}}
```

exe-name
: 使用できない記号を除いたプロジェクト名です。


DEFOLD_CUSTOM_CSS_INLINE
: *game.project* の設定で指定した CSS ファイルを、この位置にインラインで挿入します。


```html
<style>
{{{DEFOLD_CUSTOM_CSS_INLINE}}}
</style>
```

::: important
このインラインブロックは、メインのアプリケーションスクリプトが読み込まれる前に配置する必要があります。HTML タグを含むため、このマクロは三重の波括弧 `{{{TOKEN}}}` で囲み、文字列がエスケープされないようにしてください。
:::

DEFOLD_SCALE_MODE_IS_DOWNSCALE_FIT
: `html5.scale_mode` が `Downscale Fit` の場合、このトークンは `true` になります。

DEFOLD_SCALE_MODE_IS_FIT
: `html5.scale_mode` が `Fit` の場合、このトークンは `true` になります。

DEFOLD_SCALE_MODE_IS_NO_SCALE
: `html5.scale_mode` が `No Scale` の場合、このトークンは `true` になります。

DEFOLD_SCALE_MODE_IS_STRETCH
: `html5.scale_mode` が `Stretch` の場合、このトークンは `true` になります。

DEFOLD_HEAP_SIZE
: *game.project* の `html5.heap_size` で指定したヒープサイズをバイト単位に変換した値です。

DEFOLD_ENGINE_ARGUMENTS
: *game.project* の `html5.engine_arguments` で指定したエンジン引数を `,` 記号で区切ったものです。

build-timestamp
: 現在のビルドのタイムスタンプ（秒単位）です。


## 追加パラメーター {#extra-parameters}

カスタムテンプレートを作成する場合は、グローバルな `CUSTOM_PARAMETERS` オブジェクトに値を代入して、エンジンローダーのパラメーターを変更できます。組み込みテンプレートには、このカスタマイズのために意図的に空にした `<script id="engine-setup">` ブロックが用意されています。
::: important
`engine-setup` ブロックは、`dmloader.js` を読み込むスクリプトの後、かつ `EngineLoader.load()` を呼び出す `engine-start` ブロックの前に配置してください。
:::
例:

```html
    <script id="engine-setup" type="text/javascript">
        CUSTOM_PARAMETERS.disable_context_menu = false;
        CUSTOM_PARAMETERS.unsupported_webgl_callback = function() {
            console.log("Oh-oh. WebGL not supported...");
        };
    </script>
```

`CUSTOM_PARAMETERS` には、次のようなフィールドを含めることができます。

```
'archive_location_filter':
    Filter function that will run for each archive path.

'unsupported_webgl_callback':
    Function that is called if WebGL is not supported.

'engine_arguments':
    List of arguments (strings) that will be passed to the engine.

'custom_heap_size':
    Number of bytes specifying the memory heap size.

'disable_context_menu':
    Disables the right-click context menu on the canvas element if true.

'retry_time':
    Pause in seconds before retry file loading after error.

'retry_count':
    How many attempts we do when trying to download a file.

'can_not_download_file_callback':
    Function that is called if you can't download file after 'retry_count' attempts.

'resize_window_callback':
    Function that is called when resize/orientationchanges/focus events happened

'start_success':
    Function that is called just before main is called upon successful load.

'update_progress':
    Function that is called as progress is updated. Parameter progress is updated 0-100.
```

## HTML5 でのファイル操作 {#file-operations-in-html5}

HTML5 ビルドは `sys.save()`、`sys.load()`、`io.open()` などのファイル操作をサポートしていますが、内部での処理方法はほかのプラットフォームと異なります。ブラウザーで JavaScript を実行する場合、実際のファイルシステムという概念はなく、セキュリティ上の理由でローカルファイルへのアクセスが禁止されています。代わりに、Emscripten（したがって Defold も）は、データを永続的に保存するブラウザー内のデータベースである [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB) を使用して、ブラウザー内に仮想ファイルシステムを作成します。ほかのプラットフォームでのファイルシステムへのアクセスとの重要な違いは、ファイルに書き込んでから、その変更が実際にデータベースに保存されるまで、わずかな遅延が生じることがある点です。通常、ブラウザーの開発者コンソールで IndexedDB の内容を確認できます。


## HTML5 ゲームへの引数の受け渡し {#passing-arguments-to-an-html5-game}

ゲームの起動前または起動時に、追加の引数を渡す必要がある場合があります。たとえば、ユーザー ID、セッショントークン、ゲーム開始時に読み込むレベルなどです。これにはさまざまな方法があり、ここではそのいくつかを紹介します。

### エンジン引数 {#engine-arguments}

エンジンの設定と読み込みの際に、追加のエンジン引数を指定できます。これらの追加引数は、実行時に `sys.get_config_string()` で取得できます。`index.html` の `engine-setup` ブロック内で、`CUSTOM_PARAMETERS.engine_arguments` に引数を直接代入します。


```html
    <script id="engine-setup" type="text/javascript">
        CUSTOM_PARAMETERS.engine_arguments = [
            "--config=example.foo1=bar1",
            "--config=example.foo2=bar2"
        ];
    </script>
```

新しい配列を代入すると、*game.project* で設定したエンジン引数はすべて置き換えられます。設定済みの引数を保持しながら別の引数を追加するには、代わりに `CUSTOM_PARAMETERS.engine_arguments.push("--config=example.foo3=bar3")` を使用します。

*game.project* の HTML5 セクションにある *Engine Arguments* フィールドに、`--config=example.foo1=bar1, --config=example.foo2=bar2` を追加することもできます。カンマで区切った値は、生成された `dmloader.js` の `CUSTOM_PARAMETERS.engine_arguments` に追加されます。

実行時には、次のように値を取得します。

```lua
local foo1 = sys.get_config_string("example.foo1")
local foo2 = sys.get_config_string("example.foo2")
print(foo1) -- bar1
print(foo2) -- bar2
```


### URL のクエリー引数 {#query-arguments-in-the-url}

ページ URL のクエリーパラメーターとして引数を渡し、実行時に読み取ることができます。

```
https://www.mygame.com/index.html?foo1=bar1&foo2=bar2
```

```lua
local url = html5.run("window.location")
print(url)
```

すべてのクエリーパラメーターを Lua テーブルとして取得するヘルパー関数の全体を以下に示します。

```lua
local function get_query_parameters()
    local url = html5.run("window.location")
    -- get the query part of the url (the bit after ?)
    local query = url:match(".*?(.*)")
    if not query then
        return {}
    end

    local params = {}
    -- iterate over all key value pairs
    for kvp in query:gmatch("([^&]+)") do
        local key, value = kvp:match("(.+)=(.+)")
        params[key] = value
    end
    return params
end

function init(self)
    local params = get_query_parameters()
    print(params.foo1) -- bar1
end
```

## 最適化 {#optimizations}
HTML5 ゲームには通常、初回ダウンロードサイズ、起動時間、メモリ使用量について厳しい要件があります。性能の低いデバイスや低速のインターネット接続でも、ゲームを素早く読み込み、快適に動作させるためです。HTML5 ゲームの最適化では、次の項目に重点を置くことをお勧めします。

* [メモリ使用量](/manuals/optimization-memory)
* [エンジンのサイズ](/manuals/optimization-size)
* [ゲームのサイズ](/manuals/optimization-size)

## よくある質問 {#faq}
:[HTML5 FAQ](../shared/html5-faq.md)
