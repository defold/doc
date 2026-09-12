---
title: アプリケーションマニフェスト
brief: このマニュアルでは、アプリケーションマニフェストを使ってエンジンから機能を除外する方法を説明します。
---

# アプリケーションマニフェスト {#app-manifest}

アプリケーションマニフェスト（application manifest）は、エンジンにリンクする機能とバックエンドを制御します。使用していない機能を除外すると、ゲームの最終的なバイナリサイズを小さくできるため、除外することをお勧めします。アプリケーションマニフェストには、HTML5 でサポートするブラウザーの最小バージョンや WebAssembly のメモリ設定など、ビルド時のオプションも含まれています。

![](images/app_manifest/create-app-manifest.png)

![](images/app_manifest/app-manifest.png)

# マニフェストの適用 {#applying-the-manifest}

`game.project` で、`Native Extensions` -> `App Manifest` にマニフェストを割り当てます。

## Physics 2D

組み込む Box2D の実装を選択します。

* **Box2D Version 3** - Box2D 3 を組み込みます。明示的に選択した場合に有効になり、従来の実装とは異なるシミュレーション結果になる可能性があるため、既存のプロジェクトでは物理設定の再調整が必要になることがあります。
* **Box2D (Legacy Defold version)** - 従来の Defold の Box2D 実装を組み込みます。これが既定値です。
* **None** - 2D 物理を除外します。

Box2D のソルバー設定はバージョンごとに異なります。詳細は [Box2D のプロジェクト設定](/manuals/project-settings/#box2d)を参照してください。

## Physics 3D

Bullet の 3D 物理実装を組み込みます。既定で組み込まれています。3D 物理を除外するには、この設定を無効にします。

## Rig + Model

リグ（rig）とモデル（model）の機能を制御します。None を選択すると、モデルとリグを完全に除外します（[`Model`](https://defold.com/manuals/model/#model-component) のドキュメントを参照してください）。


## Exclude Record

エンジンから動画の録画機能を除外します（[`start_record`](https://defold.com/ref/stable/sys/#start_record) メッセージのドキュメントを参照してください）。


## Profiler

プロファイラーの機能をエンジンにリンクする条件を制御します。

* **Debug Only** - デバッグビルドにのみプロファイラーを組み込みます。これが既定値です。
* **None** - すべてのビルドバリアントからプロファイラーの機能を除外します。
* **Always** - デバッグビルドとリリースビルドの両方にプロファイラーを組み込みます。

アプリケーションマニフェストの設定は、ビルドにプロファイラーのコードをリンクするかどうかを制御します。*game.project* の `profiler` にある設定は、実行時のプロファイラーの動作を制御します。利用できる機能の使い方は、[プロファイリングのマニュアル](/manuals/profiling/)を参照してください。


## Sound

サウンドの設定は、エンジンにリンクするサウンドシステムとデコーダーを決定します。

### Exclude Sound

エンジンからサウンド再生機能をすべて除外します。

### Exclude Sound Decoder: WAV

WAV サウンドリソースのサポートを除外します。

### Exclude Sound Decoder: OGG

Ogg Vorbis サウンドリソースのサポートを除外します。

### Include Sound Decoder: Opus

Ogg Opus サウンドリソースのサポートを組み込みます。Opus デコーダーは既定で除外されているため、`.opus` リソースを再生するには、事前にこのオプションを有効にする必要があります。サポートされている形式については、[サウンドのマニュアル](/manuals/sound/)を参照してください。


## Exclude Input

エンジンから入力処理をすべて除外します。


## Exclude GUI

エンジンから GUI リソース、コンポーネント、および Lua サポートを除外します。プロジェクトが GUI シーンや GUI スクリプトを使わない場合にのみ有効にしてください。ラベルコンポーネントは引き続き利用できます。このオプションは既定で無効です。


## Exclude Particle FX

パーティクルエフェクトのリソース、コンポーネント、および `particlefx` Lua モジュールを除外します。GUI シーン内のパーティクルノードのサポートも除外されますが、パーティクルノードのない GUI シーンは引き続きサポートされます。このオプションを有効にする前に、パーティクルエフェクトへの参照とその API 呼び出しを削除してください。既定では無効です。


## Exclude Tilemaps

タイルマップのリソース、コンポーネント、および `tilemap` Lua モジュールを除外します。プロジェクトがタイルマップコンポーネントやその API を使わない場合にのみ有効にしてください。他のコンポーネントが使うタイルソースは引き続き利用できます。このオプションは既定で無効です。


## Exclude Live Update

エンジンから [Live Update の機能](/manuals/live-update)を除外します。


## Exclude Image

エンジンから `image` スクリプトモジュールを除外します。[リンク](https://defold.com/ref/stable/image/)


## Exclude Types

エンジンから `types` スクリプトモジュールを除外します。[リンク](https://defold.com/ref/stable/types/)


## Exclude Basis Transcoder

エンジンから Basis Universal の[テクスチャ圧縮ライブラリ](/manuals/texture-profiles)を除外します。


## Use Android Support Lib

Android X の代わりに、非推奨の Android Support Library を使用します。[詳細情報](https://defold.com/manuals/android/#using-androidx)。


## Graphics

各プラットフォームに組み込むグラフィックスバックエンドを選択します。2つを組み合わせた選択肢では両方のバックエンドが組み込まれるため、優先するバックエンドが利用できない場合に、もう一方にフォールバックできます。

| フィールド | プラットフォーム | 選択肢 | 既定値 |
|---|---|---|---|
| **Graphics** | Windows と Linux | OpenGL, Vulkan, OpenGL & Vulkan | OpenGL |
| **Graphics (macOS)** | macOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | Vulkan |
| **Graphics (iOS)** | iOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | OpenGL |
| **Graphics (Android)** | Android | OpenGL+Vulkan, OpenGL, Vulkan | OpenGL+Vulkan |
| **Graphics (HTML5)** | HTML5 | WebGL, WebGPU, WebGL & WebGPU | WebGL |

Linux ARM64 では、**OpenGL** を選択すると OpenGL ES バックエンドを使用します。Android の既定値である組み合わせでは、Vulkan が利用できれば優先し、利用できない場合は OpenGL ES にフォールバックします。

## Use full text layout system

有効（`true`）にすると、右から左へ書く言語を含むテキストの字形形成のために、完全なテキストレイアウトシステムを組み込みます。このオプションを *game.project* の `font.runtime_generation` とともに有効にすると、TrueType（`.ttf`）または OpenType（`.otf`）リソースから SDF フォントを実行時に生成できます。`.otf` リソースからの実行時生成は Defold 1.13.2 以降でサポートされています。詳細は[フォントのマニュアル](/manuals/font/#enabling-runtime-fonts)を参照してください。


## Use Rich Text

ラベルと GUI テキストのリッチテキスト解析およびスタイルエフェクトを組み込みます。このオプションは既定で有効です。プロジェクトでプレーンテキストだけが必要な場合は、無効にしてエンジンサイズを削減できます。ラベルと GUI テキストは引き続きサポートされますが、マークアップは書式やエフェクトを適用せずにプレーンテキストとして描画されます。


## ブラウザーの最小バージョン {#minimum-browser-versions}

YAML フィールドの **`minSafariVersion`**、**`minFirefoxVersion`**、**`minChromeVersion`** は、Emscripten が対象とするブラウザーの最小バージョンを指定します。現在の既定値とサポートされる最小バージョンは、スレッドを使用しないターゲットとスレッドを使用するターゲットで異なります。

| ターゲット | Safari | Firefox | Chrome |
|---|---:|---:|---:|
| `wasm-web` | `101000` | `40` | `45` |
| `wasm_pthread-web` | `150000` | `79` | `75` |

該当するターゲットのコンテキスト内で、上書きする値を指定します。スレッドを使用するターゲットには、追加の[ホスティング要件](/manuals/html5/#creating-html5-bundle)もあります。Emscripten の設定リファレンスの [`MIN_SAFARI_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-safari-version)、[`MIN_FIREFOX_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-firefox-version)、[`MIN_CHROME_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-chrome-version) を参照してください。

## Initial memory (HTML5)
YAML フィールド名: **`initialMemory`**
既定値: **33554432**

Web アプリケーションに最初に割り当てるメモリ量をバイト単位で指定します。値は WebAssembly のページサイズ（64 KiB）の倍数である必要があります。Emscripten の [`INITIAL_MEMORY`](https://emscripten.org/docs/tools_reference/settings_reference.html#initial-memory) 設定を参照してください。

このオプションはコンパイル時の既定値を指定します。実行時には、*game.project* の [`html5.heap_size`](/manuals/html5/#heap-size) の値がこれを上書きします。

## Stack size (HTML5)
YAML フィールド名: **`stackSize`**
既定値: **5242880**

アプリケーションのスタックサイズをバイト単位で指定します。Emscripten の [`STACK_SIZE`](https://emscripten.org/docs/tools_reference/settings_reference.html#stack-size) 設定を参照してください。
