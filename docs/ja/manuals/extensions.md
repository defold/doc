---
title: Defold のネイティブ拡張の作成
brief: このマニュアルでは、Defold ゲームエンジンのネイティブ拡張を作成し、セットアップ不要のクラウドビルダーでコンパイルする方法を説明します。
---

# ネイティブ拡張 {#native-extensions}

Lua では対応できない低レベルで、外部のソフトウェアやハードウェアと独自に連携する必要がある場合は、Defold SDK を使ってエンジンの拡張を作成できます。対象プラットフォームに応じて、C、C++、C#、Objective-C、Java、JavaScript を使用できます。ネイティブ拡張（native extension）の代表的な用途は次のとおりです。

- 携帯電話のカメラなど、特定のハードウェアとの連携。
- 外部の低レベル API との連携。たとえば、Luasocket を利用できるネットワーク API を通じた連携に対応していない広告ネットワーク API などです。
- 高速な計算とデータ処理。

::: sidenote
C# のサポートは実験的なもので、Defold のスクリプトコンポーネント（script component）ではなく、ネイティブ拡張を対象としています。.NET 9 NativeAOT を使って静的ライブラリを生成します。拡張の `src` フォルダーに `.cs` ソースファイルを追加すると、ビルドサービスがプロジェクトファイルを生成します。対象プラットフォームのサポート範囲は、現在の NativeAOT とビルドサービスの対応状況に従います。現在のワークフローとテスト済みの構成については、公式の[ネイティブ拡張の言語サンプル](https://github.com/defold/example-languages)を参照してください。
:::

## ビルドサーバー {#the-build-server}

Defold はクラウドベースのビルド機能により、セットアップ不要でネイティブ拡張を使い始められる仕組みを提供しています。作成したネイティブ拡張は、直接、または[ライブラリプロジェクト（Library Project）](/manuals/libraries/)を通じてゲームプロジェクトに追加すると、通常のプロジェクトコンテンツの一部になります。特別なバージョンのエンジンをビルドしてチームメンバーに配布する必要はありません。これは自動的に処理され、プロジェクトをビルドして実行するチームメンバーは、すべてのネイティブ拡張が組み込まれた、そのプロジェクト専用のエンジン実行ファイルを取得できます。

![クラウドビルド](images/extensions/cloud_build.png)

Defold は、使用制限のないクラウドビルドサーバーを無料で提供しています。サーバーはヨーロッパに設置されています。ネイティブコードの送信先 URL は、[エディターの環境設定ウィンドウ](/manuals/editor-preferences/#extensions)、または [bob](/manuals/bob/#usage) の `--build-server` コマンドラインオプションで設定します。独自のサーバーをセットアップする場合は、[こちらの手順](/manuals/extender-local-setup)に従ってください。

## プロジェクトの構成 {#project-layout}

新しい拡張を作成するには、プロジェクトのルートにフォルダーを作成します。このフォルダーには、拡張に関連するすべての設定、ソースコード、ライブラリ、リソース（resource）を格納します。拡張ビルダーはフォルダー構造を認識し、ソースファイルとライブラリを収集します。

```
 myextension/
 │
 ├── ext.manifest
 │
 ├── src/
 │
 ├── include/
 │
 ├── lib/
 │   └──[platforms]
 │
 ├── manifests/
 │   └──[platforms]
 │
 └── res/
     └──[platforms]

```
*ext.manifest*
: 拡張フォルダーには *ext.manifest* ファイルを _必ず_ 格納する必要があります。この設定ファイルには、個々の拡張をビルドする際に使うフラグと定義を記述します。ファイル形式の定義は、[拡張マニフェストのマニュアル](https://defold.com/manuals/extensions-ext-manifests/)を参照してください。

*src*
: このフォルダーには、すべてのソースコードファイルを格納します。

*include*
: この任意のフォルダーには、インクルードファイルを格納します。

*lib*
: この任意のフォルダーには、拡張が依存するコンパイル済みライブラリを格納します。ライブラリファイルは、ライブラリが対応するアーキテクチャに応じて、`platform` または `architecture-platform` という名前のサブフォルダーに配置します。

  :[platforms](../shared/platforms.md)

*manifests*
: この任意のフォルダーには、ビルドまたはバンドル作成の処理で使う追加ファイルを格納します。詳しくは後述します。

*res*
: この任意のフォルダーには、拡張が依存する追加リソースを格納します。リソースファイルは、`lib` のサブフォルダーと同様に、`platform` または `architecture-platform` という名前のサブフォルダーに配置します。すべてのプラットフォームに共通するリソースファイルを格納する `common` サブフォルダーも使用できます。

### マニフェストファイル {#manifest-files}

拡張の任意の *manifests* フォルダーには、ビルドとバンドル作成の処理で使う追加ファイルを格納します。ファイルは、`platform` という名前のサブフォルダーに配置します。

* `android` - このフォルダーには、メインアプリケーションにマージするマニフェストのスタブファイルを配置できます（[こちらで説明しています](/manuals/extensions-manifest-merge-tool)）。
  * このフォルダーには、[Gradle で解決する](/manuals/extensions-gradle)依存関係を記述した `build.gradle` ファイルも配置できます。
  * Java コードを持つ拡張には、実行時に必要なクラスの [R8 保持ルールファイル](#r8-keep-rules-for-android)（`.keep`）を含めることをお勧めします。
* `ios` - このフォルダーには、メインアプリケーションにマージするマニフェストのスタブファイルを配置できます（[こちらで説明しています](/manuals/extensions-manifest-merge-tool)）。
  * このフォルダーには、[Cocoapods で解決する](/manuals/extensions-cocoapods)依存関係を記述した `Podfile` ファイルも配置できます。
* `osx` - このフォルダーには、メインアプリケーションにマージするマニフェストのスタブファイルを配置できます（[こちらで説明しています](/manuals/extensions-manifest-merge-tool)）。
* `web` - このフォルダーには、メインアプリケーションにマージするマニフェストのスタブファイルを配置できます（[こちらで説明しています](/manuals/extensions-manifest-merge-tool)）。


### Android の R8 保持ルール {#r8-keep-rules-for-android}

拡張の `manifests/android` ディレクトリ内の、`build.gradle` と同じ場所に `.keep` ファイルを追加します。たとえば、`/myextension/manifests/android/myextension.keep` に以下を記述すると、拡張の Java クラスを保持できます。

```proguard
-keep,allowoptimization class com.example.myextension.** { *; }
```

`com.example.myextension` を、拡張の Java クラスが含まれるパッケージに置き換えます。このルールはクラスとそのメンバーを保持しながら、R8 によるコードの最適化を許可します。Java Native Interface（JNI）やリフレクションを通じてアクセスする他のクラスのルールも追加してください。R8 はそれらの使用を自動的に検出できない場合があります。

実行時にアノテーションに依存する拡張では、次も含めます。

```proguard
-keepattributes *Annotation*
```

これらのルールは、[R8 が有効な場合](/manuals/android/#enabling-r8)に、プロジェクトで選択した保持ルールファイルと統合されます。


## カスタムリソース {#custom-resources}

拡張は、`ext.manifest` と同じ場所にある `ext.properties` ファイルでカスタムリソースを宣言することにより、ゲームのアーカイブにデータを含められます。

```ini
[project]
custom_resources.default = /myextension/data
```

たとえば、`/myextension/data/settings.json` に JSON ファイルを配置します。パスは拡張フォルダーを含む、プロジェクトルートからの相対パスです。拡張をライブラリとして共有する場合は、ライブラリの [Include Dirs](/manuals/libraries/#setting-up-library-sharing) に `myextension` を含めて、利用するプロジェクトが拡張とそのデータを受け取れるようにします。

これらのパスは、*game.project* の `project.custom_resources` および他の拡張が提供するパスと統合されます。プロジェクトでカスタムリソースを設定しても、拡張が提供する設定は置き換えられません。エディターのビルドと Bob のアーカイブの両方にファイルが含まれ、実行時に読み込めます。

```lua
local data, err = sys.load_resource("/myextension/data/settings.json")
if data then
    local settings = json.decode(data)
    pprint(settings)
else
    print(err)
end
```

カスタムリソースとバンドルリソースの違いについては、[ファイルアクセス](/manuals/file-access/#custom-resources)を参照してください。

## 拡張の共有 {#sharing-an-extension}

拡張はプロジェクト内のほかのアセット（asset）と同じように扱われ、同じ方法で共有できます。ネイティブ拡張のフォルダーを Library フォルダーとして追加すると、プロジェクトの依存関係としてほかのユーザーと共有し、利用してもらえます。詳しくは、[ライブラリプロジェクトのマニュアル](/manuals/libraries/)を参照してください。


## 単純な拡張の例 {#a-simple-example-extension}

とても単純な拡張をビルドしてみましょう。まず、ルートに新しいフォルダー *`myextension`* を作成し、拡張の名前「`MyExtension`」を記述したファイル *`ext.manifest`* を追加します。この名前は C++ のシンボルであり、`DM_DECLARE_EXTENSION` の最初の引数と一致する必要がある点に注意してください（後述します）。

![マニフェスト](images/extensions/manifest.png)

```yaml
# C++ symbol in your extension
name: "MyExtension"
```

この拡張は、「`src`」フォルダーに作成する1つの C++ ファイル *`myextension.cpp`* で構成されます。

![C++ ファイル](images/extensions/cppfile.png)

拡張のソースファイルには、次のコードを記述します。

```cpp
// myextension.cpp
// Extension lib defines
#define LIB_NAME "MyExtension"
#define MODULE_NAME "myextension"

// include the Defold SDK
#include <dmsdk/sdk.h>

static int Reverse(lua_State* L)
{
    // The number of expected items to be on the Lua stack
    // once this struct goes out of scope
    DM_LUA_STACK_CHECK(L, 1);

    // Check and get parameter string from stack
    char* str = (char*)luaL_checkstring(L, 1);

    // Reverse the string
    int len = strlen(str);
    for(int i = 0; i < len / 2; i++) {
        const char a = str[i];
        const char b = str[len - i - 1];
        str[i] = b;
        str[len - i - 1] = a;
    }

    // Put the reverse string on the stack
    lua_pushstring(L, str);

    // Return 1 item
    return 1;
}

// Functions exposed to Lua
static const luaL_reg Module_methods[] =
{
    {"reverse", Reverse},
    {0, 0}
};

static void LuaInit(lua_State* L)
{
    int top = lua_gettop(L);

    // Register lua names
    luaL_register(L, MODULE_NAME, Module_methods);

    lua_pop(L, 1);
    assert(top == lua_gettop(L));
}

dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
    return dmExtension::RESULT_OK;
}

dmExtension::Result InitializeMyExtension(dmExtension::Params* params)
{
    // Init Lua
    LuaInit(params->m_L);
    printf("Registered %s Extension\n", MODULE_NAME);
    return dmExtension::RESULT_OK;
}

dmExtension::Result AppFinalizeMyExtension(dmExtension::AppParams* params)
{
    return dmExtension::RESULT_OK;
}

dmExtension::Result FinalizeMyExtension(dmExtension::Params* params)
{
    return dmExtension::RESULT_OK;
}


// Defold SDK uses a macro for setting up extension entry points:
//
// DM_DECLARE_EXTENSION(symbol, name, app_init, app_final, init, update, on_event, final)

// MyExtension is the C++ symbol that holds all relevant extension data.
// It must match the name field in the `ext.manifest`
DM_DECLARE_EXTENSION(MyExtension, LIB_NAME, AppInitializeMyExtension, AppFinalizeMyExtension, InitializeMyExtension, 0, 0, FinalizeMyExtension)
```

拡張コードへの各エントリーポイントを宣言するマクロ `DM_DECLARE_EXTENSION` に注目してください。最初の引数 `symbol` は、*ext.manifest* で指定した名前と一致する必要があります。この単純な例では、`update` と `on_event` のエントリーポイントは不要なので、マクロのそれらの位置には `0` を指定しています。

あとはプロジェクトをビルドするだけです（<kbd>Project ▸ Build</kbd>）。拡張が拡張ビルダーにアップロードされ、新しい拡張を組み込んだカスタムエンジンが生成されます。ビルダーでエラーが発生すると、ビルドエラーを表示するダイアログが開きます。

拡張をテストするには、ゲームオブジェクト（game object）を作成し、テストコードを記述したスクリプトコンポーネントを追加します。

```lua
local s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
local reverse_s = myextension.reverse(s)
print(reverse_s) --> ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba
```

これで完成です！完全に動作するネイティブ拡張を作成できました。


## 拡張のライフサイクル {#extension-lifecycle}

前述のとおり、`DM_DECLARE_EXTENSION` マクロは、拡張コードへの各エントリーポイントを宣言するために使います。

`DM_DECLARE_EXTENSION(symbol, name, app_init, app_final, init, update, on_event, final)`

これらのエントリーポイントを使うと、拡張のライフサイクルのさまざまな時点でコードを実行できます。

* エンジンの起動
  * エンジンの各システムが起動します。
  * 拡張の `app_init`
  * 拡張の `init` - すべての Defold API の初期化が完了しています。拡張コードへの Lua バインディングは、拡張のライフサイクルのこの時点で作成することをお勧めします。
  * スクリプトの初期化 - スクリプトファイルの `init()` 関数が呼び出されます。
* エンジンのループ
  * エンジンの更新
    * 拡張の `update`
    * スクリプトの更新 - スクリプトファイルの `update()` 関数が呼び出されます。
  * エンジンのイベント（ウィンドウの最小化、最大化など）
    * 拡張の `on_event`
* エンジンの終了（または再起動）
  * スクリプトの終了処理 - スクリプトファイルの `final()` 関数が呼び出されます。
  * 拡張の `final`
  * 拡張の `app_final`

## 定義されるプラットフォーム識別子 {#defined-platform-identifiers}

各プラットフォームでは、ビルダーによって対応する次の識別子が定義されます。

* `DM_PLATFORM_WINDOWS`
* `DM_PLATFORM_OSX`
* `DM_PLATFORM_IOS`
* `DM_PLATFORM_ANDROID`
* `DM_PLATFORM_LINUX`
* `DM_PLATFORM_HTML5`

## ビルドサーバーのログ {#build-server-logs}

プロジェクトでネイティブ拡張を使用している場合は、ビルドサーバーのログを利用できます。ビルドサーバーのログ（`log.txt`）は、プロジェクトのビルド時にカスタムエンジンとともにダウンロードされます。ファイル `.internal/%platform%/build.zip` 内に格納されるほか、プロジェクトのビルドフォルダーにも展開されます。

## 拡張のサンプル {#example-extensions}

* [基本的な拡張のサンプル](https://github.com/defold/template-native-extension)（このマニュアルの拡張）
* [Android 拡張のサンプル](https://github.com/defold/extension-android)
* [HTML5 拡張のサンプル](https://github.com/defold/extension-html5)
* [macOS、iOS、Android 用の動画プレーヤー拡張](https://github.com/defold/extension-videoplayer)
* [macOS と iOS 用のカメラ拡張](https://github.com/defold/extension-camera)
* [iOS と Android 用のアプリ内購入拡張](https://github.com/defold/extension-iap)
* [iOS と Android 用の Firebase Analytics 拡張](https://github.com/defold/extension-firebase-analytics)

[Defold Asset Portal](https://www.defold.com/assets/) にも、いくつかのネイティブ拡張があります。
