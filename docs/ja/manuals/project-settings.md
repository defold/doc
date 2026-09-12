---
title: Defold のプロジェクト設定
brief: このマニュアルでは、Defold のプロジェクト固有の設定について説明します。
---

# プロジェクト設定 {#project-settings}

*game.project* ファイルには、プロジェクト全体の設定がすべて含まれています。このファイルはプロジェクトのルートフォルダーに置き、名前を *game.project* にする必要があります。エンジンが起動してゲームを開始するときは、最初にこのファイルを探します。

ファイル内の各設定は、いずれかのカテゴリーに属します。ファイルを開くと、Defold はすべての設定をカテゴリー別に表示します。

![プロジェクト設定](images/project-settings/settings.jpg)


## ファイル形式 {#file-format}

*game.project* の設定は通常 Defold 内で変更しますが、一般的なテキストエディターでもファイルを編集できます。このファイルは INI ファイル形式の標準に従い、次のように記述します。

```ini
[category1]
setting1 = value
setting2 = value
[category2]
...
```

実際の例を示します。

```ini
[bootstrap]
main_collection = /main/main.collectionc
```

これは、*main_collection* 設定が *bootstrap* カテゴリーに属することを意味します。上の例のようにファイル参照を使用するときは、パスの末尾に 'c' を付ける必要があります。これは、コンパイル済みのファイルを参照することを示します。また、*game.project* があるフォルダーがプロジェクトのルートになるため、設定のパスの先頭には '/' が付きます。


## 実行時のアクセス {#runtime-access}

[`sys.get_config_string(key)`](/ref/sys/#sys.get_config_string)、[`sys.get_config_number(key)`](/ref/sys/#sys.get_config_number)、[`sys.get_config_int(key)`](/ref/sys/#sys.get_config_int)、[`sys.get_config_boolean(key)`](/ref/sys/#sys.get_config_boolean) を使うと、実行時に *game.project* から値を読み取れます。次に例を示します。

```lua
local title = sys.get_config_string("project.title")
local gravity_y = sys.get_config_number("physics.gravity_y")
local fullscreen = sys.get_config_boolean("display.fullscreen", false)
```

::: sidenote
キーはカテゴリー名と設定名をドットで区切って組み合わせ、小文字で記述し、空白文字をすべてアンダースコアに置き換えたものです。たとえば、「Project」カテゴリーの「Title」フィールドは `project.title`、「Physics」カテゴリーの「Gravity Y」フィールドは `physics.gravity_y` になります。
:::


## セクションと設定 {#sections-and-settings}

利用できるすべての設定を、カテゴリー別に示します。

### Project

#### Title
アプリケーションのタイトルです。

#### Version
アプリケーションのバージョンです。

#### Publisher
パブリッシャー名です。

#### Developer
開発者名です。

#### Write Log File
エンジンがログファイルを書き込む条件を制御します。次の選択肢があります。

- "Never": ログファイルを書き込みません。
- "Debug": Debug ビルドでのみログファイルを書き込みます。
- "Always": Debug ビルドと Release ビルドの両方でログファイルを書き込みます。

エディターから複数のインスタンスを実行している場合、ファイル名は *instance_2_log.txt* になります。`2` はインスタンスのインデックスです。インスタンスを1つだけ実行している場合や、バンドルから実行している場合、ファイル名は *log.txt* になります。ログファイルの保存先は次のいずれかのパスです（記載順に試します）。

1. *project.log_dir* で指定したパス（非表示の設定）
2. システムのログパス:
  * macOS/iOS: `NSDocumentDirectory`
  * Android: `Context.getExternalFilesDir()`
  * その他: アプリケーションのルート
3. アプリケーションサポートのパス
  * macOS/iOS: `NSApplicationSupportDirectory`
  * Windows: `CSIDL_APPDATA`（例: `C:\Users\<username>\AppData\Roaming`）
  * Android: `Context.getFilesDir()`
  * Linux: `HOME` 環境変数

#### Minimum Log Level
ログシステムの最小ログレベルを指定します。このレベル以上のログのみが表示されます。

#### Compress Archive
バンドル作成時のアーカイブ圧縮を有効にします。現在、これは Android 以外のすべてのプラットフォームに適用されます。Android では、apk 内のすべてのデータがすでに圧縮されています。

#### Dependencies
プロジェクトの *Library URL* の URL リストです。詳しくは、[ライブラリのマニュアル](/manuals/libraries/)を参照してください。

#### Custom Resources
`custom_resources`
:[Custom Resources](../shared/custom-resources.md)

カスタムリソースの読み込みについて詳しくは、[ファイルアクセスのマニュアル](/manuals/file-access/#how-to-access-files-bundled-with-the-application)で説明しています。

拡張が `ext.properties` の `custom_resources.default` を通じて提供するパスは、この設定と統合されます。例については、[拡張のカスタムリソース](/manuals/extensions/#custom-resources)を参照してください。

#### Bundle Resources
`bundle_resources`
:[Bundle Resources](../shared/bundle-resources.md)

バンドルリソースの読み込みについて詳しくは、[ファイルアクセスのマニュアル](/manuals/file-access/#how-to-access-files-bundled-with-the-application)で説明しています。

#### Bundle Exclude Resources
`bundle_exclude_resources`
バンドルに含めないリソースの、カンマ区切りのリストです。これらのリソースは、`bundle_resources` ステップで収集したリソースから除外されます。

---

### Bootstrap

#### Main Collection
アプリケーションの起動に使用するコレクション（collection）のファイル参照です。既定値は `/logic/main.collection` です。

#### Render
レンダリングパイプラインを定義するレンダー設定ファイルを指定します。既定値は `/builtins/render/default.render` です。

---

### Library

#### Include Dirs
ライブラリ共有を通じてプロジェクトから共有するディレクトリの、スペース区切りのリストです。詳しくは、[ライブラリのマニュアル](/manuals/libraries/)を参照してください。

---

### Script

#### Shared State
チェックすると、すべてのスクリプトの種類で1つの Lua ステートを共有します。

---

### Engine

#### Run While Iconified
アプリケーションのウィンドウを最小化している間も、エンジンの実行を継続できるようにします（デスクトッププラットフォームのみ）。

#### Fixed Update Frequency
`fixed_update(self, dt)` ライフサイクル関数の更新頻度です。単位はヘルツです。

#### Max Time Step
1フレーム中のタイムステップ（更新やシミュレーションの時間刻み）が大きくなりすぎた場合、この最大値に制限します。単位は秒です。

---

### Display

#### Width
アプリケーションウィンドウの幅です。単位はピクセルです。

#### Height
アプリケーションウィンドウの高さです。単位はピクセルです。

#### High Dpi
対応するディスプレイで高 DPI のバックバッファーを作成します。通常、ゲームは *Width* と *Height* の設定値の2倍の解像度で描画されます。これらの設定値は、引き続きスクリプトやプロパティで使用する論理解像度になります。

#### Samples
スーパーサンプリングアンチエイリアシングで使用するサンプル数です。ウィンドウヒント `GLFW_FSAA_SAMPLES` を設定します。値が `0` の場合、アンチエイリアシングは無効になります。

この設定はウィンドウを制御します。オフスクリーンの[マルチサンプリングを使うレンダーターゲット](/manuals/render/#multisampled-render-targets)には、独自のサンプル数があります。

#### Fullscreen
アプリケーションをフルスクリーンで起動する場合はチェックします。チェックしない場合は、ウィンドウモードで実行されます。

#### Update Frequency
目標のフレームレートです。単位はヘルツです。可変フレームレートにするには 0 に設定します。0 より大きい値にすると固定フレームレートになり、実行時には実際のフレームレートが上限になります（つまり、エンジンの1フレーム内でゲームループを2回更新することはできません）。実行時にこの値を変更するには、[`sys.set_update_frequency(hz)`](https://defold.com/ref/stable/sys/?q=set_update_frequency#sys.set_update_frequency:frequency) を使用します。この設定は、画面表示を伴わずに実行するヘッドレスビルドでも機能します。

#### Swap interval
この整数値は、アプリケーションでの垂直同期（vsync）の扱いを制御します。0 にすると垂直同期が無効になり、既定値は 1 です。OpenGL アダプターを使用する場合、この値は[バッファーの交換間にウィンドウを更新する](https://www.khronos.org/opengl/wiki/Swap_Interval)フレーム数を設定します。Vulkan にはスワップ間隔という組み込みの概念がないため、この値は垂直同期を有効にするかどうかを制御します。

#### Vsync
従来との互換性のための設定です。この設定は非推奨です。新しいプロジェクトでは **Swap Interval** を使用してください。無効にすると、実効スワップ間隔は強制的に `0` になります。有効にすると、**Swap Interval** によって実効値が決まります。

#### Display Profiles
使用するディスプレイプロファイルファイルを指定します。既定値は `/builtins/render/default.display_profilesc` です。詳しくは、[GUI レイアウトのマニュアル](/manuals/gui-layouts/#creating-display-profiles)を参照してください。

#### Dynamic Orientation
デバイスの回転に合わせて、アプリを縦向きと横向きの間で動的に切り替える場合はチェックします。現在、開発用アプリにはこの設定が反映されません。

#### Display Device Info
起動時に GPU 情報をコンソールに出力します。

---

### Render

#### Clear Color Red
クリアカラーの赤チャンネルです。レンダースクリプトとウィンドウ作成時に使用されます。

#### Clear Color Green
クリアカラーの緑チャンネルです。レンダースクリプトとウィンドウ作成時に使用されます。

#### Clear Color Blue
クリアカラーの青チャンネルです。レンダースクリプトとウィンドウ作成時に使用されます。

#### Clear Color Alpha
クリアカラーのアルファチャンネルです。レンダースクリプトとウィンドウ作成時に使用されます。

---

### Font

#### Runtime Generation
実行時のフォント生成を使用します。

---

### Physics

#### Max Collision Object Count
コリジョンオブジェクト（collision object）の最大数です。コリジョンオブジェクトは、衝突判定や物理特性を持つコンポーネント（component）です。

#### Type
使用する物理シミュレーションの種類を `2D` または `3D` から選びます。

#### Gravity X
ワールドの x 軸方向の重力です。単位はメートル毎秒です。

#### Gravity Y
ワールドの y 軸方向の重力です。単位はメートル毎秒です。

#### Gravity Z
ワールドの z 軸方向の重力です。単位はメートル毎秒です。

#### Debug
デバッグのために物理シミュレーションを可視化する場合はチェックします。

#### Debug Alpha
可視化した物理シミュレーションのアルファ成分の値です。範囲は `0`--`1` です。

#### World Count
同時に存在できる物理ワールドの最大数です。既定値は `4` です。コレクションプロキシ（collection proxy）を通じて4つを超えるワールドを同時に読み込む場合は、この値を増やす必要があります。各物理ワールドはかなりの量のメモリを確保することに注意してください。

#### Scale
数値精度を確保するため、ゲームワールドに対する物理ワールドのスケールを物理エンジンに指定します。範囲は `0.01`--`1.0` です。値を `0.02` に設定すると、物理エンジンは50単位を1メートルとして扱います（$1 / 0.02$）。

#### Allow Dynamic Transforms
ゲームオブジェクト（game object）のトランスフォームを、取り付けられているすべてのコリジョンオブジェクトコンポーネントに物理エンジンが適用する場合はチェックします。これにより、動的なものも含めてコリジョン形状を移動、拡大縮小、回転できます。

#### Use Fixed Timestep
物理エンジンで、フレームレートに依存しない固定時間間隔の更新を使用する場合はチェックします。この設定を `fixed_update(self, dt)` ライフサイクル関数と `engine.fixed_update_frequency` プロジェクト設定と組み合わせると、一定間隔で物理エンジンとやり取りできます。新しいプロジェクトでは `true` を推奨します。

#### Debug Scale
物理シミュレーションの3軸表示や法線などの単位オブジェクトを描画する大きさです。

#### Max Collisions
スクリプトに報告する衝突の数です。

#### Max Contacts
スクリプトに報告する接触点の数です。

#### Contact Impulse Limit
この設定値より小さい接触力積を無視します。

#### Ray Cast Limit 2d
1フレームあたりの 2d レイキャストリクエストの最大数です。

#### Ray Cast Limit 3d
1フレームあたりの 3d レイキャストリクエストの最大数です。

#### Trigger Overlap Capacity
重なり合う物理トリガーの最大数です。

#### Velocity Threshold
弾性衝突が発生する最小速度です。

#### Max Fixed Timesteps
固定タイムステップを使用する場合の、シミュレーションの最大ステップ数です（3D のみ）。

---

### Graphics

#### Default Texture Min Filter
縮小フィルタリングに使用するフィルタリング方法を指定します。

#### Default Texture Mag Filter
拡大フィルタリングに使用するフィルタリング方法を指定します。

#### Max Draw Calls
レンダリング呼び出しの最大数です。

#### Max Characters:
テキスト描画バッファーで事前に確保する文字数です。つまり、各フレームで表示できる文字数です。

#### Max Font Batches
各フレームで表示できるテキストバッチの最大数です。

#### Max Debug Vertices
デバッグ用頂点の最大数です。物理形状の描画などに使用します。

#### Texture Profiles
このプロジェクトで使用するテクスチャプロファイルファイルです。既定値は `/builtins/graphics/default.texture_profiles` です。

#### Verify Graphics Calls
各グラフィックス呼び出しの後で戻り値を検証し、エラーがあればログに報告します。

#### WebGL Version Hint
`graphics.webgl_version_hint` は、HTML5 で要求する WebGL コンテキストのバージョンを選択します。有効な値は `1`（WebGL 1）と `2`（WebGL 2、既定値）です。WebGL 2 をサポートするブラウザーでも WebGL 1 を対象にしたりテストしたりするには、`1` に設定します。WebGL 1 を対象にする場合は、必要なシェーダーが含まれるよう、[Exclude GLES 2.0](#exclude-gles-20) を無効のままにしてください。

#### OpenGL Version Hint
OpenGL コンテキストのバージョンヒントです。特定のバージョンを選択すると、そのバージョンが必要な最小バージョンとして使用されます（OpenGL ES には適用されません）。

#### OpenGL Core Profile Hint
コンテキスト作成時に、OpenGL プロファイルヒントを 'core' に設定します。コアプロファイルでは、即時モードレンダリングなどの非推奨機能がすべて OpenGL から除外されます。OpenGL ES には適用されません。

#### Vulkan Version Major
`graphics.vulkan_version_major` は、Vulkan コンテキスト/API のメジャーバージョンヒントです。Vulkan グラフィックスバックエンドが選択されている場合にのみ適用されます。既定値は `1` です。

#### Vulkan Version Minor
`graphics.vulkan_version_minor` は、Vulkan コンテキスト/API のマイナーバージョンヒントです。Vulkan グラフィックスバックエンドが選択されている場合にのみ適用されます。既定値は `0` です。

---

### Shader

#### Exclude GLES 2.0
OpenGLES 2.0 / WebGL 1.0 を実行するデバイス向けのシェーダーをコンパイルしません。

#### GLSL ES Default Precision Float
`shader.glsl_es_default_precision_float` は、クロスコンパイルされた GLSL ES シェーダー内の浮動小数点値に対する、既定のグローバル精度修飾子を設定します。有効な値は `mediump` と `highp` で、既定値は `mediump` です。

#### GLSL ES Default Precision Int
`shader.glsl_es_default_precision_int` は、クロスコンパイルされた GLSL ES シェーダー内の整数値に対する、既定のグローバル精度修飾子を設定します。有効な値は `mediump` と `highp` で、既定値は `highp` です。

---

### Input

#### Repeat Delay
押し続けた入力のリピートが始まるまでの待ち時間です。単位は秒です。

#### Repeat Interval
押し続けた入力の、各リピートの間の待ち時間です。単位は秒です。

#### Gamepads
ゲームパッドの信号を OS に対応付ける、ゲームパッド設定ファイルのファイル参照です。既定値は `/builtins/input/default.gamepads` です。

#### Game Binding
ハードウェア入力をアクションに対応付ける、入力設定ファイルのファイル参照です。既定値は `/input/game.input_binding` です。

#### Use Accelerometer
チェックすると、エンジンが各フレームで加速度センサーの入力イベントを受信します。加速度センサーの入力を無効にすると、パフォーマンスが多少向上する可能性があります。

---

### Resource

#### Http Cache
チェックすると HTTP キャッシュが有効になり、ネットワーク経由でデバイス上の実行中のエンジンへリソースをより速く読み込めます。

#### Uri
プロジェクトのビルドデータの場所を URI 形式で指定します。

#### Max Resources
同時に読み込めるリソースの最大数です。

---

### Network

#### Http Timeout
HTTP のタイムアウトです。単位は秒です。タイムアウトを無効にするには `0` に設定します。

#### Http Thread Count
HTTP サービスのワーカースレッド数です。

#### Http Cache Enabled
チェックすると、ネットワークリクエスト（`http.request()` を使用）の HTTP キャッシュが有効になります。HTTP キャッシュはリクエストに対応するレスポンスを保存し、以降のリクエストで保存したレスポンスを再利用します。HTTP キャッシュは、HTTP レスポンスヘッダーの `ETag` と `Cache-Control: max-age` をサポートしています。

#### SSL Certificates
SSL ハンドシェイク中に証明書チェーンを検証するための、SSL ルート証明書を含むファイルです。

---

### Collection

#### Max Instances
コレクション内のゲームオブジェクトのインスタンスの最大数です。既定値は `1024` です。[（コンポーネントの最大数の最適化について参照）](#component-max-count-optimizations)。

#### Max Input Stack Entries
入力スタック内のゲームオブジェクトの最大数です。

---

### Sound

#### Gain
グローバルなゲイン（音量）です。範囲は `0`--`1` です。

#### Use Linear Gain
有効にすると、ゲインは線形になります。無効にすると、指数曲線を使用します。

#### Max Sound Data
サウンドリソースの最大数です。つまり、実行時の固有のサウンドファイル数です。

#### Max Sound Buffers
（現在は使用されていません）同時に存在できるサウンドバッファーの最大数です。

#### Max Sound Sources
（現在は使用されていません）同時に再生できるサウンドの最大数です。

#### Max Sound Instances
同時に存在できるサウンドインスタンスの最大数です。つまり、実際に同時再生されるサウンドの数です。

#### Max Component Count
コレクションあたりのサウンドコンポーネントの最大数です。

#### Sample Frame Count
各オーディオ更新で使用するサンプル数です。0 は自動を意味します（48 kHz では1024、44.1 kHz では768）。

#### Use Thread
チェックすると、サウンドシステムはスレッドを使用してサウンドを再生し、メインスレッドの負荷が高いときの音切れのリスクを低減します。

#### Stream Enabled
チェックすると、サウンドシステムはストリーミングを使用してソースファイルを読み込みます。

#### Stream Cache Size
_すべての_ チャンクを含むサウンドチャンクキャッシュの最大サイズです。既定値は `2097152` バイトです。
この値は、読み込まれているサウンドファイル数にストリームチャンクサイズを掛けた値より大きくすることをお勧めします。
そうしないと、各フレームで新しいチャンクがキャッシュから追い出される可能性があります。

#### Stream Chunk Size
ストリーミングされる各チャンクのサイズです。単位はバイトです。

#### Stream Preload Size
アーカイブから読み込むサウンドファイルの、最初のチャンクのサイズをバイト単位で指定します。

---

### Sprite

#### Max Count
コレクションあたりのスプライトの最大数です。[（コンポーネントの最大数の最適化について参照）](#component-max-count-optimizations)。

#### Subpixels
チェックすると、ピクセルに整列しない位置にスプライトを表示できるようになります。

---

### Tilemap

#### Max Count
コレクションあたりのタイルマップの最大数です。[（コンポーネントの最大数の最適化について参照）](#component-max-count-optimizations)。

#### Max Tile Count
コレクションあたりの、同時に表示できるタイルの最大数です。

---

### Spine

#### Max Count
Spine モデルコンポーネントの最大数です。[（コンポーネントの最大数の最適化について参照）](#component-max-count-optimizations)。

---

### Mesh

#### Max Count
コレクションあたりのメッシュコンポーネントの最大数です。[（コンポーネントの最大数の最適化について参照）](#component-max-count-optimizations)。

---

### Model

#### Max Count
コレクションあたりのモデルコンポーネントの最大数です。[（コンポーネントの最大数の最適化について参照）](#component-max-count-optimizations)。

#### Split Meshes
頂点数が65536を超えるメッシュを、新しいメッシュに分割します。

#### Max Bone Matrix Texture Width
ボーン行列テクスチャの最大幅です。アニメーションに必要なサイズを、それ以上で最も近い2の累乗に切り上げたサイズだけ使用します。

#### Max Bone Matrix Texture Height
ボーン行列テクスチャの最大高さです。アニメーションに必要なサイズを、それ以上で最も近い2の累乗に切り上げたサイズだけ使用します。

---

### GUI

#### Max Count
GUI コンポーネントの最大数です。[（コンポーネントの最大数の最適化について参照）](#component-max-count-optimizations)。

#### Max Particle Count
GUI 内に同時に存在できるパーティクルの最大数です。

#### Max Animation Count
GUI 内のアクティブなアニメーションの最大数です。

---

### Label

#### Max Count
ラベルの最大数です。[（コンポーネントの最大数の最適化について参照）](#component-max-count-optimizations)。

#### Subpixels
チェックすると、ピクセルに整列しない位置にラベルを表示できるようになります。

---

### Particle FX

#### Max Count
同時に存在できるエミッターの最大数です。[（コンポーネントの最大数の最適化について参照）](#component-max-count-optimizations)。

#### Max Particle Count
同時に存在できるパーティクルの最大数です。

---

### Box2D

#### Velocity Iterations
Box2D 2.2 物理ソルバーの速度反復回数です。

#### Position Iterations
Box2D 2.2 物理ソルバーの位置反復回数です。

#### Sub Step Count
Box2D 3.x 物理ソルバーのサブステップ数です。

---

### Collection proxy

#### Max Count
コレクションプロキシの最大数です。[（コンポーネントの最大数の最適化について参照）](#component-max-count-optimizations)。

---

### Collection factory

#### Max Count
コレクションファクトリー（collection factory）の最大数です。[（コンポーネントの最大数の最適化について参照）](#component-max-count-optimizations)。

---

### Factory

#### Max Count
ゲームオブジェクトのファクトリー（factory）の最大数です。[（コンポーネントの最大数の最適化について参照）](#component-max-count-optimizations)。

---

### iOS

#### App Icon 57x57--180x180
指定した幅と高さ `W` &times; `H` のアプリケーションアイコンとして使用する画像ファイル（.png）です。

#### Launch Screen
ストーリーボードファイル（.storyboard）です。作成方法について詳しくは、[iOS のマニュアル](/manuals/ios/#creating-a-storyboard)を参照してください。

#### Icons Asset
アプリのアイコンを含むアイコンアセットファイル（.car）です。

#### Prerendered Icons
（iOS 6 以前）アイコンが事前に描画済みである場合はチェックします。チェックしない場合、アイコンに光沢のハイライトが自動的に追加されます。

#### Bundle Identifier
バンドル識別子により、iOS はアプリの更新を認識できます。バンドル ID は Apple に登録し、アプリ固有のものにする必要があります。iOS アプリと macOS アプリで同じ識別子を使用することはできません。識別子は、ドットで区切った2つ以上のセグメントで構成する必要があります。各セグメントは英字で始める必要があります。各セグメントには、英数字、アンダースコア、ハイフン（-）のみを使用できます（[`CFBundleIdentifier`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430) を参照）。

#### Bundle Name
バンドルの短い名前（15文字）です（[`CFBundleName`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430) を参照）。

#### Bundle Version
バンドルのバージョンです。数値または x.y.z 形式で指定します（[`CFBundleVersion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430) を参照）。

#### Info.plist
指定すると、アプリのバンドル作成時に、組み込みの iOS ベースマニフェストの代わりにこの *`Info.plist`* ファイルを使用します。組み込みマニフェストには、リリース以外のビルドでエディターがターゲットを検出するために必要な、ローカルネットワークと Bonjour のエントリーが含まれています。カスタムマニフェストを使用し、デバイス上でターゲット検出、プロファイリング、ホットリロード、ログストリーミングが必要な場合は、[iOS のマニュアル](/manuals/ios/#creating-an-ios-application-bundle)の説明に従い、それらのエントリーを保持してください。

#### Privacy Manifest
アプリケーションの Apple プライバシーマニフェストです。このフィールドの既定値は `/builtins/manifests/ios/PrivacyInfo.xcprivacy` です。

#### Custom Entitlements
指定すると、指定したプロビジョニングプロファイル（`.entitlements`、`.xcent`、`.plist`）のエンタイトルメントが、アプリケーションのバンドル作成時に指定するプロビジョニングプロファイルのエンタイトルメントとマージされます。

#### Default Language
アプリケーションの `Localizations` リストにユーザーの優先言語がない場合に使用する言語です（[`CFBundleDevelopmentRegion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430) を参照）。優先言語が2文字の ISO 639-1 規格に含まれている場合はそのコードを、それ以外の場合は3文字の ISO 639-2 コードを使用してください。

#### Localizations
このフィールドには、サポートするローカライズの言語名または ISO 言語コードを示す文字列を、カンマ区切りで指定します（[`CFBundleLocalizations`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552) を参照）。

---

### Android

#### App Icon 36x36--192x192
指定した幅と高さ `W` &times; `H` のアプリケーションアイコンとして使用する画像ファイル（.png）です。

#### Push Icon Small--LargeXxxhdpi
Android のカスタムプッシュ通知アイコンとして使用する画像ファイル（.png）です。このアイコンは、ローカルとリモートの両方のプッシュ通知に自動的に使用されます。設定しない場合は、既定でアプリケーションアイコンを使用します。

#### Push Field Title
通知タイトルに使用するペイロードの JSON フィールドを指定します。この設定を空にすると、プッシュ通知は既定でアプリケーション名をタイトルとして使用します。

#### Push Field Text
通知テキストに使用するペイロードの JSON フィールドを指定します。空にすると、iOS と同様に `alert` フィールドのテキストを使用します。

#### Version Code
アプリのバージョンを示す整数値です。以後、更新するたびにこの値を増やしてください。

#### Minimum SDK Version
アプリケーションの実行に必要な最小 API レベルです（`android:minSdkVersion`）。

#### Target SDK Version
アプリケーションが対象とする API レベルです（`android:targetSdkVersion`）。

#### Package
パッケージ識別子です。ドットで区切った2つ以上のセグメントで構成する必要があります。各セグメントは英字で始める必要があります。各セグメントには、英数字またはアンダースコアのみを使用できます。

#### GCM Sender Id
Google Cloud Messaging の Sender Id です。プッシュ通知を有効にするには、Google が割り当てた文字列を設定します。

#### FCM Application Id
Firebase Cloud Messaging の Application Id です。

#### Manifest
設定すると、バンドル作成時に指定した Android マニフェスト XML ファイルを使用します。カスタムマニフェストは、Defold の組み込みベースマニフェストを置き換えます。ネイティブ拡張のマニフェストフラグメントは引き続きマージされますが、組み込みベースマニフェストへの以後の変更は自動的には反映されません。そのため、アップグレード時にはカスタムマニフェストと現在の組み込みマニフェストを比較してください。ゲームの場合は、`android:appCategory="game"` を `<application>` 要素に設定します。ゲーム以外のアプリケーションの場合、`android:appCategory` は、Android が定義する[アプリケーションカテゴリー](https://developer.android.com/guide/topics/manifest/application-element#appCategory)のいずれかがアプリを正確に表している場合にのみ設定してください。

#### Iap Provider
使用するストアを指定します。有効な選択肢は `Amazon` と `GooglePlay` です。詳しくは、[extension-iap](/extension-iap/) を参照してください。

#### Input Method
Android デバイスでキーボード入力を取得する方法を指定します。有効な選択肢は `KeyEvent`（従来の方法）と `HiddenInputField`（新しい方法）です。

#### Immersive Mode
設定すると、ナビゲーションバーとステータスバーを非表示にし、画面上のすべてのタッチイベントをアプリで取得できるようにします。

#### Display Cutout
ディスプレイのカットアウトまで表示領域を広げます。

#### Debuggable
[GAPID](https://github.com/google/gapid) や [Android Studio](https://developer.android.com/studio/profile/android-profiler) などのツールを使用して、アプリケーションをデバッグできるかどうかを指定します。Android マニフェストの `android:debuggable` フラグを設定します（[公式ドキュメント](https://developer.android.com/guide/topics/manifest/application-element#debug)）。

<a id="proguard-config"></a>

#### R8 Keep Rules
`android.r8_keep_rules` で `.keep` ファイルを選択すると、Android ビルドで Java コードの R8 による縮小、最適化、難読化が有効になります。縮小を行わない D8 を使うには、設定を空にします。

Defold の既定のルールを直接使うには、`/builtins/manifests/android/dmengine.keep` を選択します。拡張は独自の[保持ルール](/manuals/extensions/#r8-keep-rules-for-android)を提供し、このファイルと統合されます。

プロジェクト固有のルールを追加する必要がある場合にのみ、組み込みファイルをプロジェクトにコピーしてください。コピーには組み込みのルールを保持してください。カスタムファイルを選択すると、プロジェクトのルールセット全体が置き換えられます。

R8 を有効にし、リリースバンドルとともに難読化マッピングを保持する方法については、[Android のマニュアル](/manuals/android/#shrinking-java-code-with-r8)を参照してください。

#### Extract Native Libraries
パッケージインストーラーが APK からファイルシステムへネイティブライブラリを展開するかどうかを指定します。`false` に設定すると、ネイティブライブラリは APK 内に非圧縮で格納されます。APK が大きくなる可能性はありますが、実行時にライブラリを APK から直接読み込むため、アプリケーションの読み込みが速くなります。Android マニフェストの `android:extractNativeLibs` フラグを設定します（[公式ドキュメント](https://developer.android.com/guide/topics/manifest/application-element#extractNativeLibs)）。

---

### macOS

#### App Icon
macOS のアプリケーションアイコンとして使用するバンドルアイコンファイル（.icns）です。

#### Info.plist
設定すると、バンドル作成時に指定した info.plist ファイルを使用します。

#### Privacy Manifest
アプリケーションの Apple プライバシーマニフェストです。このフィールドの既定値は `/builtins/manifests/osx/PrivacyInfo.xcprivacy` です。

#### Bundle Identifier
バンドル識別子により、macOS はアプリの更新を認識できます。バンドル ID は Apple に登録し、アプリ固有のものにする必要があります。iOS アプリと macOS アプリで同じ識別子を使用することはできません。識別子は、ドットで区切った2つ以上のセグメントで構成する必要があります。各セグメントは英字で始める必要があります。各セグメントには、英数字、アンダースコア、ハイフン（-）のみを使用できます。

#### Default Language
アプリケーションの `Localizations` リストにユーザーの優先言語がない場合に使用する言語です（[`CFBundleDevelopmentRegion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430) を参照）。優先言語が2文字の ISO 639-1 規格に含まれている場合はそのコードを、それ以外の場合は3文字の ISO 639-2 コードを使用してください。

#### Localizations
このフィールドには、サポートするローカライズの言語名または ISO 言語コードを示す文字列を、カンマ区切りで指定します（[`CFBundleLocalizations`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552) を参照）。

---

### Windows

#### App Icon
Windows のアプリケーションアイコンとして使用する画像ファイル（.ico）です。.ico ファイルの作成方法について詳しくは、[Windows のマニュアル](/manuals/windows)を参照してください。

---

### HTML5

これらの選択肢の多くについて詳しくは、[HTML5 プラットフォームのマニュアル](/manuals/html5/)を参照してください。

#### Heap Size
Emscripten が使用するヒープサイズです。単位はメガバイトです。

#### .html Shell
バンドル作成時に、指定したテンプレート HTML ファイルを使用します。既定値は `/builtins/manifests/web/engine_template.html` です。

#### Custom .css
バンドル作成時に、指定したテーマ CSS ファイルを使用します。既定値は `/builtins/manifests/web/light_theme.css` です。

#### Splash Image
設定すると、作成したバンドルの起動時に、Defold ロゴの代わりに指定したスプラッシュ画像を使用します。

#### Archive Location Prefix
HTML5 向けにバンドルを作成すると、ゲームデータは1つ以上のアーカイブデータファイルに分割されます。エンジンがゲームを開始するときに、これらのアーカイブファイルをメモリに読み込みます。この設定を使用して、データの場所を指定します。

#### Archive Location Suffix
アーカイブファイルに追加するサフィックスです。たとえば、CDN からキャッシュされていないコンテンツを強制的に取得する場合に便利です（例: `?version2`）。

#### Engine Arguments
エンジンに渡す引数のリストです。

#### Wasm Streaming
wasm ファイルのストリーミングを有効にします（より高速でメモリ使用量も少なくなりますが、MIME タイプ `application/wasm` が必要です）。

#### Show Fullscreen Button
`index.html` ファイルの Fullscreen Button を有効にします。

#### Show Made With Defold
`index.html` ファイルの Made With Defold リンクを有効にします。

#### Show Console Banner
この選択肢を有効にすると、エンジン起動時に、エンジンとそのバージョンに関する情報をブラウザーのコンソールへ出力します（`console.log()` を使用）。

#### Scale Mode
ゲームのキャンバスを拡大縮小する方法を指定します。

#### Retry Count
起動中にダウンロードが失敗した後の再試行回数です。エンジンの JavaScript または WebAssembly ファイルでのネットワークエラー、失敗を示す HTTP ステータス、サイズの不一致を含みます。最初のリクエストは別に数えます。アーカイブファイルの検証には独自の再試行上限があります。[ダウンロードの検証](/manuals/html5/#download-verification)と `Retry Time` を参照してください。

#### Retry Time
ダウンロードに失敗した場合に、次のファイルダウンロードの試行まで待機する秒数です（`Retry Count` を参照）。

#### Verify Downloaded File Size
`html5.verify_downloaded_file_size` は、ダウンロードしたエンジンファイルとアーカイブファイルのサイズを期待するサイズと照合します。既定で有効（`true`）です。サーバー、プロキシ、CDN がファイルを意図的に書き換えてサイズを変更する場合にのみ、`false` に設定してください。検証に失敗すると、起動に失敗する前にダウンロードを再試行します。再試行上限はエンジンのダウンロードとアーカイブファイルの検証で異なります。[ダウンロードの検証](/manuals/html5/#download-verification)を参照してください。

#### Transparent Graphics Context
グラフィックスコンテキストの背景を透明にする場合はチェックします。

---

### IAP

#### Auto Finish Transactions
IAP トランザクションを自動的に完了する場合はチェックします。チェックしない場合、トランザクションの成功後に `iap.finish()` を明示的に呼び出す必要があります。

---

### Live update

#### Settings
バンドル作成時に使用する Live Update 設定リソースファイルです。

---

### Native extension

#### _App Manifest_
設定すると、アプリケーションマニフェストを使用してエンジンのビルドをカスタマイズします。これにより、エンジンから使用しない部分を削除して、最終的なバイナリのサイズを小さくできます。使用しない機能の除外方法については、[アプリケーションマニフェストのマニュアル](/manuals/app-manifest)を参照してください。

---

### Profiler

App Manifest の **Profiler** 設定は、デバッグビルドとリリースビルドにプロファイラーのコードをリンクするかどうかを制御します。以下の設定は、選択したビルドに含まれるプロファイラーのコードの実行時の動作を制御します。詳しくは、[プロファイリングのマニュアル](/manuals/profiling/)を参照してください。

#### Enabled
ゲーム内のプロファイラーを有効にします。

#### Track Cpu
デバッグビルドでは、CPU 使用率のサンプリングが既定で有効になります。App Manifest を通じてプロファイラー対応を含めたリリースビルドでも CPU サンプリングが必要な場合は、この設定を有効にします。

#### Sleep Between Server Updates
サーバー更新の間にスリープするミリ秒数です。

#### Performance Timeline Enabled
ブラウザー内のパフォーマンスタイムラインを有効にします（HTML5 のみ）。

#### Max Sample Count
`profiler.max_sample_count` は、1フレーム内に各スレッドで記録するプロファイラーサンプルの最大数です。既定値は `4096`、最小値は `128` です。正当なプロファイルがこの上限を超える場合にのみ値を増やしてください。まず、ネイティブ拡張のプロファイリングコードで、スコープの開始と終了の呼び出しに不一致がないか確認してください。

---

## エンジン起動時の設定値の指定 {#setting-config-values-on-engine-startup}

エンジン起動時に、*game.project* の設定を上書きする設定値をコマンドラインから渡せます。

```bash
# Specify a bootstrap collection
$ dmengine --config=bootstrap.main_collection=/my.collectionc

# Set two custom config values
$ dmengine --config=test.my_value=4711 --config=test2.my_value2=foobar
```

カスタム値は、他の設定値と同様に、[実行時のアクセス](#runtime-access)で説明した対応する関数で読み取れます。

```lua
local my_value = sys.get_config_number("test.my_value")
local my_value2 = sys.get_config_string("test.my_value2")
local my_flag = sys.get_config_boolean("test.my_flag", false)
```


:[Component max count optimizations](../shared/component-max-count-optimizations.md)


## カスタムプロジェクト設定 {#custom-project-settings}

メインプロジェクトまたは[ネイティブ拡張](/manuals/extensions/)のカスタム設定を定義できます。メインプロジェクトのカスタム設定は、プロジェクトのルートにある `game.properties` ファイルで定義する必要があります。`ext.properties` という名前のファイルは、プロジェクト内と取得済みの依存ライブラリ内のどこにあっても検出されます。同じ場所に `ext.manifest` がある必要はありません。検出されたすべての拡張メタデータがマージされた後、ルートの `game.properties` ファイルが適用され、その内容を上書きできます。

設定ファイルは *game.project* と同じ INI 形式を使用し、プロパティの属性はサフィックス付きのドット記法で定義します。

```
[my_category]
my_property.private = 1
...
```

常に適用される既定のメタファイルは、[こちら](https://github.com/defold/defold/blob/dev/com.dynamo.cr/com.dynamo.cr.bob/src/com/dynamo/bob/meta.properties)で確認できます。

現在、次の属性を使用できます。

```
[my_extension]
// `type` - used for the value string parsing
my_property.type = string // one of the following values: bool, string, number, integer, string_array, resource

// `help` - displayed as a help tooltip in the editor
my_property.help = string

// `default` - value used as default if user didn't set value manually
my_property.default = string

// `private` - private value used during the bundle process but will be removed from the bundle itself
my_property.private = 1 // boolean value 1 or 0

// `label` - editor input label
my_property.label = My Awesome Property

// `minimum` and/or `maximum` - valid range for numeric properties, validated in the editor UI
my_property.minimum = 0
my_property.maximum = 255

// `options` - drop-down choices for the editor UI, comma-separated value[:label] pairs
my_property.options = android: Android, ios: iOS

// `resource` type only:
my_property.filter = jpg,png // allowed file extensions for resource selector dialog
my_property.preserve-extension = 1 // use original resource extension instead of a built one

// deprecation
my_property.deprecated = 1 // mark property as deprecated
my_property.severity-default = warning // if deprecated property is specified, but set to a default value
my_property.severity-override = error  // if deprecated property is specified and set to a non-default value

```
さらに、設定カテゴリーには次の属性を設定できます。
```
[my_extension]
// `group` - game.project category group, e.g. Main, Platforms, Components, Runtime, Distribution
group = Runtime
// `title` - displayed category title
title = My Awesome Extension
// `help` - displayed category help
help = Settings for My Awesome Extension
```


Bob とエディターの両方が、これらのメタデータファイルを解析します。エディターはそれらを使用して、*game.project* ビューアー内に対応するフィールド、選択肢、検証、ヘルプツールチップを作成します。
