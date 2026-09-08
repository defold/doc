---
title: Unity ユーザーのための Defold
brief: このガイドは、Unity の使用経験がある方が Defold にすばやく移行するためのものです。Unity で使われる主な概念を取り上げ、Defold で対応するツールと方法を説明します。
---

# Unity ユーザーのための Defold {#defold-for-unity-users}

このガイドは、Unity の使用経験がある方が Defold ですぐに開発を進められるようにするためのものです。基本事項に焦点を当て、さらに詳しい情報が必要な箇所では Defold の公式マニュアルを案内します。

## はじめに {#introduction}

Defold は完全に無料で、幅広いプラットフォームに対応する 3D ゲームエンジンです。Windows、Linux、macOS 用のエディターを備えています。ソースコード全体は [Github](https://github.com/defold/defold/) で公開されています。

Defold は、低性能のデバイスでもパフォーマンスを発揮することを重視しています。小規模なコンポーネント（component）モデルを採用し、ゲームプレイ中の多くのやり取りをコードと、メッセージによる通信であるメッセージパッシング（message passing）で処理します。

Defold は Unity よりもはるかに小容量です。空のプロジェクトを含むエンジンのサイズは、すべてのプラットフォームで 1-3 MB です。エンジンの一部をさらに削除したり、ゲームコンテンツの一部を [Live Update](/manuals/live-update) に移して、後から別途ダウンロードしたりできます。サイズの比較や、Defold を選ぶその他の理由は、[Defold を選ぶ理由のページ](https://defold.com/why/)で説明しています。

Defold を用途に合わせてカスタマイズするために、次のものを自作するか、既存のものを利用できます。

1. すべてをスクリプトで制御できるレンダリングパイプライン（レンダースクリプト（render script）+ マテリアル/シェーダー）。いくつかのバックエンド（OpenGL、Vulkan など）から選択できます。
2. ネイティブ拡張（native extension）として作成するコードとコンポーネント（C++/C#）。
3. エディターをカスタマイズするエディタースクリプトと UI ウィジェット。
3. エンジンとエディターを改変したビルド。ソースコード全体とビルドパイプラインが公開されているため、作成できます。

Game From Scratch による [Unity 開発者向けの Defold](https://www.youtube.com/watch?v=-3CzCbd4QZ0) の動画もお勧めします。

---

## インストール {#installation}

1. 使用する OS 向けの Defold をダウンロードします。
2. ZIP ファイルを展開して起動します。

これだけです。ハブ、追加の SDK、ツールチェーン、プラットフォーム用バンドルをインストールする必要はありません。このため、Defold はセットアップ不要と説明しています。

詳しくは、この短い[インストールマニュアル](/manuals/install/)をお読みください。

### バージョン {#versions}

Defold は頻繁に更新され、「LTS」のリリース系列はありません。常に最新バージョンを使うことをお勧めします。新しいバージョンは定期的に、通常は毎月リリースされ、約2週間の公開ベータ期間があります。Defold はエディターから直接更新できます。

---

## ウェルカム画面 {#welcome-screen}

Defold を起動すると、Unity Hub に似たウェルカム画面が表示され、最近使ったプロジェクトを開けます。

![ウェルカム画面の比較](images/unity/unity_defold_start.png)

次の項目から新しいプロジェクトを始めることもできます。
- `Templates` - 特定のプラットフォームやジャンル向けのセットアップをすばやく行うための、基本的な空のプロジェクトです。
- `Tutorials` - 最初の一歩を案内する、ガイド付きの学習コースです。
- `Samples` - 公式またはコミュニティが提供する使用例やサンプルです。

![ウェルカム画面の Templates の比較](images/unity/unity_defold_templates.png)

最初のプロジェクトを作成するか、プロジェクトを開くと、Defold エディターに表示されます。

## Hello World

ここでは Defold ですばやく何かを作ってみます。手順に沿って操作した後、マニュアルの続きを読んでください。

1. `Templates` から空のプロジェクトを選択し、`Title` に名前を入力して保存先を選び、`Create New Project` をクリックして作成します。プロジェクトが Defold エディターで開きます。
![Hello World の手順1](images/unity/helloworld_1.png)
2. 左側の `Assets` ペインで `main` フォルダーを開き、`main.collection` をダブルクリックして開きます。
3. 右側の `Outline` ペインで `Collection` を右クリックし、`Add Game Object` を選択します。
![Hello World の手順2](images/unity/helloworld_2.png)
4. 作成した `go` ゲームオブジェクト（game object）を右クリックし、`Add Component`、続いて `Label` を選択します。
![Hello World の手順3](images/unity/helloworld_3.png)
5. その下の左側にある `Properties` ペインで、`Text` プロパティに何か入力します。
6. 中央のメインのシーンビューで、ラベルをドラッグして `(480,320,0)` 付近まで移動し、ドロップします。または、`Properties` の `Position` で位置を変更します。
![Hello World の手順4](images/unity/helloworld_4.png)
7. ラベルの位置を変更したら、`File` -> `Save All` をクリックするか、ショートカット <kbd>Ctrl</kbd>+<kbd>S</kbd>（Mac では <kbd>Cmd</kbd>+<kbd>S</kbd>）でプロジェクトを保存します。
8. `Project` -> `Build` をクリックするか、ショートカット <kbd>Ctrl</kbd>+<kbd>B</kbd>（Mac では <kbd>Cmd</kbd>+<kbd>B</kbd>）でプロジェクトをビルドします。
![Hello World の手順5](images/unity/helloworld_5.png)

これで Defold で最初のプロジェクトをビルドできました。ウィンドウに入力したテキストが表示されるはずです。ゲームオブジェクトとコンポーネントの概念には、すでになじみがあるでしょう。コレクション（collection）、Outline、Properties、そしてラベルを少し右上に移動する必要があった理由については、以下で説明します。

---

## Defold エディターの概要 {#defold-editor-overview}

ここでは、Unity ユーザーが最初に知りたいと思われる点から Defold エディターを紹介します。その後、[エディターの概要マニュアル](/manuals/editor)全体にも目を通すことをお勧めします。

### エディターの比較 {#editors-comparison}

Unity と Defold の違いとして最初に気付くのは、エディターの既定のレイアウトです。ここでは、Defold の既定のレイアウトに合わせて少し変更した Unity エディターを示しています。見慣れた Unity のタブを手掛かりに主要なペインを視覚的に比較しやすいように、両者を並べています。

![エディターの比較](images/unity/defold_unity_editor.png)

既定では、Defold エディターは 2D の正投影プレビューで開きます。3D プロジェクトを作業する場合や、Unity に近い操作感にしたい場合は、ツールバーの `2D` トグルのチェックを外して 2D から 3D に切り替え、`Perspective` トグルにチェックを入れてカメラを透視投影に変更することをお勧めします。

![Defold のツールバー](images/unity/defold_2d.png)

ツールバーの `Grid Settings` を調整して、Unity と同じように `Y` 平面を使うこともできます。

![Defold の 3D 設定](images/unity/defold_3d.png)

### Defold のペインの概要 {#defold-panes-overview}

Defold エディターは6つの主要なペインに分かれています。

![エディター2](images/editor/editor_overview.png)

Defold での名称と機能の違いを以下で比較します。

| Defold | Unity | 違い |
|---|---|---|
| 1. Assets | Project (Assets Browser) | Defold では Assets ペインは左側にドッキングされています。Defold は `meta` ファイルを作成しません。 |
| 2. Main Editor | Scene View | Defold エディターはコンテキストに応じて切り替わります（ファイルの種類ごとに異なるエディターを使用します）。一方、Unity は専用の独立したウィンドウ（Animator、Shader Graph など）を使います。Defold には組み込みのコードエディターもあります。 |
| 3. Outline | Hierarchy | Defold では、全体の階層ではなく、現在開いているファイルまたは選択した要素（ゲームオブジェクトやコンポーネント）だけが表示されます。 |
| 4. Properties | Inspector | Defold では、ゲームオブジェクトのすべてのコンポーネントではなく、Outline で**現在選択しているもの**のプロパティだけが表示されます。 |
| 5. Tools | Console | Defold では、Console、Curve Editor、Build Errors、Search Results、Breakpoints、Debugger などのタブでツールを提供します。 |
| 6. Changed Files | Unity Version Control (Plastic) | Defold では、プロジェクトに Git を統合すると、変更したファイルがここに表示されます。Git を外部で使うこともできます。 |

エディターに関連する、知っておくと便利なその他の名称です。

| Defold | Unity | 違い |
|---|---|---|
| Game Build | Game Preview | エンジンでビルドしたゲームの実行画面です。Defold では、Unity 6 以降の Multiplayer Play Mode と同様に、エディターからゲームの複数のインスタンスを実行できます。Defold のゲームは常に独立したウィンドウで動作し、ドッキングされません。Unity Remote と同様に、外部デバイス（携帯電話など）でゲームを実行することもできます。 |
| タブ | タブ | Defold では、Main Editor ビュー内の2つのペインを並べて編集できます。タブとペインは1つのエディターウィンドウ内にドッキングされており、ペインの表示を切り替えたり（<kbd>F6</kbd>、<kbd>F7</kbd>、<kbd>F8</kbd>）、サイズを調整したりできます。 |
| ツールバー | Toolbar / Scene View Options | Unity では新しいバージョンになって初めて、Defold と同様にトランスフォームツールが Scene ビュー内に移動しました。 |
| Console | Console | Defold の Console は切り離せません。Defold のビルドエラーは、独立した `Build Errors` タブに表示されます。 |
| Build Errors | Console のコンパイルエラー | Lua スクリプトはインタープリターで実行されるため、コンパイルエラーはありません。ただし、プロジェクトはビルドされ、その間にエラーが表示されることがあります。Defold はスクリプトの静的解析に Lua Language Server も使います。 |
| Search Results | Search / Project Search | Defold には、種類やラベルによるフィルタリングはありません。 |
| Curve Editor | Unity Curve Editor | Defold の Curve Editor では、パーティクルエフェクトのプロパティのカーブだけを編集できます。 |
| [Debugger](/manuals/debugging/) | Visual Studio Debugger | Defold には初めからデバッガーが完全に統合されています。ブレークポイントの確認、有効化、無効化を行うための追加のタブもあります。 |

---

## 主な概念 {#key-concepts}

十分に抽象化して考えると、ほとんどのゲームエンジンの主要な概念はよく似ています。複雑な処理やプラットフォームに関する処理を引き受けながら、開発者がブロックを組み立てるように、より簡単にゲームを作れるようにするためのものです。

### 基本構成要素 {#building-blocks}

Defold は、少数の基本構成要素だけで動作します。

![基本構成要素](images/unity/blocks.png)

詳しくは、[Defold の基本構成要素](/manuals/building-blocks/)についてのマニュアル全体をお読みください。

### ゲームオブジェクト {#game-objects}
Defold は、Unity と同様に **「ゲームオブジェクト」** を使います。両エンジンとも、ゲームオブジェクトは ID を持つデータのコンテナーで、すべてに位置、回転、スケールというトランスフォームがあります。ただし Defold では、トランスフォームは独立したコンポーネントではなく、組み込まれています。

ゲームオブジェクトの間に親子関係を作れます。Defold では、これはエディター内の「コレクション」（後述）の中で行うか、スクリプトで動的に行う場合に限られます。ゲームオブジェクトは、Unity のようにほかのゲームオブジェクトを入れ子のオブジェクトとして内部に含めることはできません。

### コンポーネント {#components}
両エンジンとも、ゲームオブジェクトを **「コンポーネント」** で拡張できます。Defold は、必要不可欠なコンポーネントを最小限のセットで提供します。Unity に比べると、たとえばコライダーのように 2D と 3D の区別が少ないため、全体のコンポーネント数も少なく、Unity にあるコンポーネントがなくて物足りなく感じることもあるでしょう。

#### 振る舞いを定義するコンポーネント {#behaviour-components}

Unity では、「コンポーネント」は通常、`MonoBehaviour` を意味し、`GameObject` にアタッチして使います。`MonoBehaviour` を継承して自作することも、Light や物理関連など、さまざまな組み込みコンポーネントを使うこともできます。

Defold でコンポーネントというと、Unity の組み込みコンポーネントなどに相当するものだけを指します。ただし、Defold はスクリプトを monobehaviour として扱わず、ゲームオブジェクトにアタッチするために、イベントのリスナーやコールバックを作る以外の明示的な「印」を付ける必要はありません。

独自のゲームプレイの振る舞いは、通常、同じゲームオブジェクトに多数の独立したスクリプトコンポーネントとして追加することはありません。一般には Lua モジュールに実装して1つのホスト `.script` から使うか、多数のオブジェクトを制御する、より大きなシステムスクリプトで処理します。詳しくは後述の「コードの記述」で説明します。

詳しくは、[Defold のコンポーネント](/manuals/components/)をお読みください。

以下の表では、すばやく参照できるよう、よく似た Unity のコンポーネントを示しています。各 Defold コンポーネントのマニュアルへのリンクもあります。

| Defold | Unity | 違い |
|---|---|---|
| [スプライト](/manuals/sprite/) | Sprite Renderer | Defold では、色調（色のプロパティ）はコードからのみ変更できます。 |
| [タイルマップ](/manuals/tilemap/) | Tilemap / Grid | Defold には正方形のグリッドに対応した組み込みのタイルマップエディターがあります（ただし、たとえば[六角形](https://github.com/selimanac/defold-hexagon/)向けの拡張もあります）。組み込みのオートタイリングルールはありません。[Tiled](https://defold.com/assets/tiled/)、[TileSetter](https://defold.com/assets/tilesetter/)、[Sprite Fusion](https://defold.com/assets/spritefusion/) などのツールには、Defold へのエクスポート機能があります。 |
| [ラベル](/manuals/label/) | Text / TextMeshPro | Defold には、TextMeshPro のような豊富な書式設定に対応する [RichText 拡張](https://defold.com/assets/richtext/)があります。 |
| [サウンド](/manuals/sound/) | AudioSource | Defold には、空間的な音源ではなく、グローバルな音源だけがあります。Defold 向けの公式 [FMOD 拡張](https://github.com/defold/extension-fmod)があります。 |
| [ファクトリー](/manuals/factory/) | Prefab Instantiate() | Defold のファクトリー（factory）は、特定のプロトタイプ（prototype）（プレハブ）を持つコンポーネントです。 |
| [コレクションファクトリー](/manuals/collection-factory/) | -（直接対応するコンポーネントはありません） | Defold のコレクションファクトリー（collection factory）コンポーネントは、親子関係を持つ複数のゲームオブジェクトを一度に生成できます。 |
| [コリジョンオブジェクト](/manuals/physics-objects) | Rigidbody + Collider | Defold では、物理オブジェクトとコリジョン形状が、衝突判定や物理特性を持つ1つのコンポーネントであるコリジョンオブジェクト（collision object）にまとめられています。 |
| [コリジョン形状](/manuals/physics-shapes/)  | BoxCollider / SphereCollider / CapsuleCollider | Defold では、形状（ボックス、球、カプセル）をコリジョンオブジェクトコンポーネント内で設定します。両エンジンとも、タイルマップと凸包データから作るコリジョン形状に対応しています。 |
| [カメラ](/manuals/camera/) | Camera | Unity のカメラには、レンダリングやポストプロセスの組み込み設定がより多くあります。Defold では、レンダースクリプトを使ってユーザー自身が制御をカスタマイズします。 |
| [GUI](/manuals/gui/) | UI Toolkit / Unity UI / uGUI Canvas | Defold の GUI は、完全な UI やテンプレートを構築するための強力なコンポーネントです。Unity には対応する単一の UI コンポーネントはなく、複数の UI フレームワークがあります。Defold には[拡張](https://github.com/britzl/extension-imgui)もあります。 |
| [GUI スクリプト](/manuals/gui-script/) | Unity UI / uGUI スクリプト | Defold の GUI は、専用の `gui` API を使う GUI スクリプトから制御できます。 |
| [モデル](/manuals/model/) | MeshRenderer + Material | Defold のモデルコンポーネントは、3D モデルファイル、テクスチャ、シェーダーを備えたマテリアルをまとめたものです。 |
| [メッシュ](/manuals/mesh/) | MeshRenderer / MeshFilter / Procedural Mesh | Defold のメッシュは、コードで頂点の集合を管理するためのコンポーネントです。Defold のモデルに似ていますが、さらに低水準です。 |
| [ParticleFX](/manuals/particlefx/) | Particle System | Defold のパーティクルエディターは、多くのプロパティを持つ 2D/3D パーティクルエフェクトに対応しており、Curve Editor のカーブを使って時間とともにアニメーションさせられます。Trails や Collisions はありません。 |
| [スクリプト](/manuals/script/) | Script | プログラミングの違いについては、以下で詳しく説明します。 |

#### 拡張とカスタムコンポーネント {#extensions-and-custom-components}

Defold には、拡張として利用できる公式の [Spine](/extension-spine/) および [Rive](/extension-rive/) コンポーネントもあります。

また、ネイティブ拡張を使って独自の[カスタムコンポーネント](https://github.com/defold/extension-simpledata)を作成することもできます。たとえば、コミュニティが作成した[オブジェクト補間コンポーネント](https://github.com/indiesoftby/defold-object-interpolation)があります。

Audio Listener、Light、Terrain、LineRenderer、TrailRenderer、Cloth、Animator など、Unity の一部のコンポーネントには Defold に標準で対応するものがありません。ただし、これらの機能はすべてスクリプトで実装でき、すでに利用できる実装もあります。たとえば、各種ライティングパイプライン、地形を含む任意のメッシュを生成するメッシュコンポーネント、カスタマイズ可能な軌跡エフェクト用の [Hyper Trails](https://defold.com/assets/hypertrails/) などです。今後、ライトなどの新しい組み込みコンポーネントが Defold に追加される可能性もあります。

### リソース {#resources}

Unity と同様に、一部のコンポーネントには **「リソース（resource）」** が必要です。たとえば、スプライトやモデルにはテクスチャが必要です。そのうちのいくつかを以下の表で比較します。

| Defold | Unity | 違い |
|---|---|---|
| [アトラス](/manuals/atlas/) | Sprite Atlas / Texture2D | Defold には [Texture Packer 用の拡張](https://defold.com/extension-texturepacker/)もあります。 |
| [タイルソース](/manuals/tilesource/) | Tile Palette + Asset | Defold のタイルソースは、タイルマップのテクスチャとしてだけでなく、スプライトやパーティクルにも使えます。 |
| [フォント](/manuals/font/) | Font | Unity の Text/TextMeshPro と同様に、Defold のラベルコンポーネントや GUI のテキストノードで使います。 |
| [マテリアル](/manuals/material/) | Material | Defold では、シェーダーを頂点プログラムとフラグメントプログラムと呼びます。 |

### コレクションとシーンの比較 {#collection-vs-scene}

Defold のゲームオブジェクトとコンポーネントは、Unity のプレハブのように個別のファイルに保存することも、それらをまとめる **「コレクション」** ファイル内で定義することもできます。

Defold のコレクションは、基本的には静的なシーンの記述を持つテキストファイルです。実行時のオブジェクトでは**ありません**。ゲーム内でどのゲームオブジェクトをインスタンス化し、それらのオブジェクト間にどのような親子関係を設定するかだけを定義します。

#### ゲームワールド {#game-worlds}

Unity のシーンは、既定では同じグローバルなゲーム状態と物理シミュレーション、つまり実質的に同じ*ワールド*（*ゲームワールド（game world）*）を共有します。Defold には2つの選択肢があります。
1. プレハブのように、単一のゲームオブジェクトファイルから `Factory` を使って、またはコレクションファイルから `Collection Factory` を使って、すでにインスタンス化されている指定の*ワールド*にゲームオブジェクトをインスタンス化します。
2. 起動時に読み込まれるコレクション、またはコレクションプロキシ（collection proxy）である `Collection Proxy` コンポーネントを通じて、専用のゲームオブジェクト、物理ワールド、エンジン処理、アドレス指定の名前空間を持つ独立したゲーム*ワールド*を実行時に作成します。

ファクトリーとプロキシコンポーネントについても以下で説明します。
コレクションの詳細は、[基本構成要素のマニュアル](/manuals/building-blocks/#collections)をお読みください。

---

## プロジェクトのリソースとアセット {#project-resources-and-assets}

Unity と Defold は、どちらもゲームコンテンツをプロジェクトディレクトリに保存しますが、アセットの追跡と準備の方法は異なります。

### アセット {#assets}

Unity はアセットを `Assets/` に保存し、`.meta` ファイルを生成します。Defold には meta ファイルがありません。Defold のプロジェクトは、ディスク上とまったく同じフォルダー構造そのもので、`Assets` ペインは常にそれを反映します。

### リソースの形式 {#resource-formats}

Unity は、内部でアセットをインポートし、別の形式に変換します。Defold では、元のリソース（`.png`、`.gltf`、`.wav`、`.ogg` など）を直接扱い、`Components` に割り当てます。

Unity では、1枚の画像をスプライトとして使えます。Defold では、モデル/メッシュに画像を直接使えますが、スプライト/GUI/タイルマップ/パーティクルには、アトラス（パックされたテクスチャ）またはタイルソース（グリッド状のタイル）が必要です。

Defold のリソースの多くはテキストとして保存されるため、バージョン管理に適しています。

### ライブラリキャッシュ {#library-cache}

Unity は、インポートしたアセット用に `Library/` フォルダーを生成します。Defold にはそのようなディレクトリはありません。アセットはビルド時に処理され、出力のキャッシュはビルドフォルダー内に保存されます（必要に応じてローカル/リモートのビルドキャッシュも使えます）。

---

## コードの記述 {#code-writing}

Defold で `MonoBehaviour` スクリプトに相当するのはスクリプトコンポーネントですが、知っておくとよい違いがいくつかあります。

### Lua

Defold のスクリプトは、動的型付けのマルチパラダイム言語である [Lua](https://www.lua.org/) で記述します。

Lua スクリプトには、`*.script`、`*.gui_script`、`*.render_script`、`*.editor_script`、`*.lua` モジュールといういくつかの種類があります。

### Teal

Defold は、Lua の静的型付けの方言である [Teal](https://teal-language.org/) など、Lua コードを生成するトランスパイラーの使用に対応しています。ただし、この機能には制限が多く、追加のセットアップが必要です。詳しくは、[Teal 拡張のリポジトリ](https://github.com/defold/extension-teal)をご覧ください。

### C++/C# のネイティブ拡張 {#cc-native-extensions}

Defold のネイティブ拡張は、対象プラットフォームに応じて、C、C++、C#、Objective-C、Java、JS など、ほかの言語で記述できます。C# に非常に慣れている場合は、ゲームロジックの大部分を C# の拡張にまとめ、小さな Lua の起動用スクリプトから呼び出す構成も技術的には可能です。ただし、高度な API の知識が必要になるため、初心者にはお勧めしません。

拡張について詳しくは、[Defold のネイティブ拡張マニュアル](/manuals/extensions/)をお読みください。


### MonoBehaviour から Lua モジュールへ {#from-monobehaviours-to-lua-modules}

Unity のスクリプトモデルは自由度の高いものです。エディターで振る舞いを追加する主な方法は `MonoBehaviour` なので、多くの Unity プロジェクトでは、主要な GameObject ごとに制御用のスクリプトを1つ作るところから始めます。たとえば、`PlayerController`、`EnemyController`、`BulletController`、`GameManager`、`EnemyManager` などです。

Defold では、標準的なアーキテクチャがより明確です。ゲームオブジェクトに `.script` を持たせることはできますが、すべてのゲームオブジェクトにスクリプトを作る必要はほとんどありません。Defold の強力なアドレス指定とメッセージパッシングにより、1つのスクリプトから、独自のスクリプトを持たない数百、数千のほかのオブジェクトやそのコンポーネントを制御できるためです。各ゲームオブジェクトに対応するスクリプトを作る必要はほとんどなく、かえって複雑になり、逆効果になることがあります。

ゲームプレイの振る舞いを再利用するために、Unity 開発者はしばしばコンポジションを取り入れるようになります。小さな `MonoBehaviour` スクリプト、たとえば `Health.cs`、`Attack.cs`、`EnemyFinder.cs` などを同じ GameObject にアタッチする方法です。Defold では、通常、アタッチした1つの `.script` をホストまたは調整役にし、再利用するロジックを通常の Lua モジュールに配置します。

Unity でこのように構成すると、次のようになります。

```text
Player
├── PlayerMovement.cs
├── PlayerAttack.cs
├── EnemyFinder.cs
└── Health.cs
```

Defold では、同じ責務を、アタッチした1つのスクリプトと再利用可能なモジュールに分けることがよくあります。

```text
player.go
├── sprite
├── collisionobject
└── player.script

modules/
├── player_movement.lua
├── player_attack.lua
├── enemy_finder.lua
└── health.lua
```

アタッチした `.script` がホストまたは調整役になります。Lua モジュールには再利用可能なロジックを配置します。これは、Unity の小さな `MonoBehaviour` スクリプトが1つの責務を持つことが多いのと似ています。

```lua
local movement = require "modules.player_movement"
local attack = require "modules.player_attack"
local finder = require "modules.enemy_finder"
local health = require "modules.health"

function init(self)
    self.movement = movement.new(self)
    self.attack = attack.new(self)
    self.finder = finder.new(self)
    self.health = health.new(self)
end

function update(self, dt)
    self.movement:update(dt)
    self.attack:update(dt)
    self.finder:update(dt)
end

function on_message(self, message_id, message, sender)
    self.health:on_message(message_id, message, sender)
    self.attack:on_message(message_id, message, sender)
end
```

大きな違いは、Defold でモジュール化されたアーキテクチャを使えないことではなく、どこで組み合わせを行い、ゲームプレイのコードがどのように通信するかにあります。

| Unity | Defold |
|---|---|
| Inspector で複数の `MonoBehaviour` スクリプトをアタッチします | 1つの `.script` をアタッチし、コード内で Lua モジュールを組み合わせます |
| `GetComponent<T>()` やシリアル化したフィールドを使って振る舞いをつなぎます | モジュールのインスタンスを `self` に保存し、オブジェクト間ではアドレス/メッセージを使います |
| 各コンポーネントが独自のライフサイクルメソッドを持てます | ホストスクリプトが `init()`、`update()`、`on_message()`、`final()` などを振り分けます |
| 多くのアーキテクチャのスタイルを選べます | メッセージを中心とし、コードで明示的に組み合わせる方法が一般的です |

特に、Inspector でコンポーネントを追加して振る舞いを設定することに慣れていると、最初は違和感があるかもしれません。Defold では、Unity で視覚的に設定するような多くのものを、コードから作成、接続、有効化、無効化、更新できます。Defold のメッセージングシステムは、ロジック間の結び付きを弱めるのに役立ちます。送信元はアドレスにデータを送信し、受信先がそのデータをどう扱うかを決めます。

この方法は推奨されていますが、強制ではありません。ゲームオブジェクトごとに複数のスクリプトをアタッチしたり、オブジェクト指向のプログラミングスタイルに近づけたりするなど、自由にスクリプトを記述できます。そのためのライブラリ（[defold-oop](https://github.com/xiyoo0812/defold-oop) や [lua-class](https://github.com/d954mas/lua-class)）もあります。

弾、敵、パーティクル、タイル、単純な操作要素など、同じ種類のオブジェクトが多数ある場合は、それぞれに独立したスクリプトを持たせるより、システムスクリプトや管理用スクリプトから制御する方が適していることがよくあります。オブジェクトが独自の意味のある状態と振る舞いを持つ場合は、オブジェクトごとのスクリプトを使います。ロジックを再利用したい場合はモジュールを使います。1つのスクリプトで多数のオブジェクトを効率よく制御できる場合は、システムスクリプトを使います。

Defold のスクリプトプロパティ、ファクトリー、アドレス指定、メッセージングを使って複数のユニットを制御する例は、[こちら](https://defold.com/examples/factory/spawn_manager/)にあります。

コードの記述に役立つマニュアルです。
- [スクリプトマニュアル](/manuals/script/)
- [コードの記述](/manuals/writing-code/)
- [デバッグ](/manuals/debugging/)


### 組み込みのコードエディター {#built-in-code-editor}

Defold エディターには、コード補完、構文の強調表示、すばやいドキュメント参照、lint によるチェック、組み込みのデバッガーを備えたコードエディターが含まれています。

![Defold のコードエディター](/images/editor/code-editor.png)

### VS Code とその他のエディター {#vs-code-and-other-editors}

好みに応じて、外部のエディターを使うこともできます。Defold のコンポーネントと関連ファイルはすべてテキスト形式なので、任意のテキストエディターで編集できます。ただし、Protobuf を基にしているため、正しい書式と要素の構造に従う必要があります。

VS Code に慣れていて、ゲームのコードを書くために使いたい場合は、Visual Studio Marketplace から [Defold Kit](https://marketplace.visualstudio.com/items?itemName=astronachos.defold) または [Defold Buddy](https://marketplace.visualstudio.com/items?itemName=mikatuo.vscode-defold-ide) をインストールすることをお勧めします。

Defold エディターの環境設定で、テキストファイルを既定で VS Code（またはほかの外部エディター）で開くように設定することもできます。詳しくは、[エディターの環境設定](/manuals/editor-preferences/)をご覧ください。

### シェーダー - GLSL {#shaders-glsl}

Defold は Unity と同様に、シェーダー（`Vertex Programs` と `Fragment Programs`）に GLSL（OpenGL Shading Language）を使います。Defold には Unity のような Shader Graph がないため、不便に感じるかもしれませんが、コードを記述して同等のシェーダーを作成できます。

シェーダーについて詳しくは、[シェーダーマニュアル](/manuals/shader)をお読みください。

#### マテリアル {#materials}

Defold は `Material` という概念を使い、`.fp` と `.vp` のシェーダー、サンプラー（テクスチャ）、頂点属性や定数などを結び付けます。

マテリアルについて詳しくは、[マテリアルマニュアル](/manuals/material)をお読みください。

---

## メッセージングシステム {#messaging-system}

Defold では、オブジェクトは互いを直接参照しません。`GetComponent` も、スクリプト間でオブジェクトをまたぐメソッド呼び出しも、Unity のようなシーン全体へのアクセスもありません。

代わりに、スクリプトはメッセージパッシングで通信します。メソッドを呼び出したり、コンポーネントに直接アクセスしたりするのではなく、ほかのスクリプトにメッセージを送信します。受け取ったメッセージをどう扱うかは、そのオブジェクトが決めます。

最初はなじみにくいかもしれませんが、この仕組みは疎結合を促し、強い相互依存を減らします。


### メッセージの送信 {#sending-a-message}

Unity では、通信は通常、次のようになります。

```c#
var enemy = GameObject.Find("Enemy");
enemy.GetComponent<EnemyAI>().TakeDamage(10);
```

このように、オブジェクトは互いを直接参照し、ほかのスクリプトのメソッドを呼び出せます。すべてが1つの共有されたシーン空間に存在します。

Defold では、あるスクリプトから別のスクリプト（またはほかのコンポーネント）へメッセージを送信します。

```lua
msg.post("#my_component", "my_message", { my_name = "Defold" })
```

そして、スクリプトでそのメッセージを処理できます。

```lua
function on_message(self, message_id, messsage)
    if message_id == hash("my_message") then
        print("Hello ", message.my_name)
    end
end
```

`#` と `hash` は後で説明するので、今は気にしないでください。残りの部分は分かりやすいはずです。インスタンス化された任意のゲームオブジェクトの任意のコンポーネントに、同じスクリプト自身も含めてメッセージを送信できます。

#### スクリプト以外のコンポーネント {#components-other-than-scripts}

たとえば、有効化や無効化のために、`Sprite` や `Collision` コンポーネントにメッセージを送信することがあります。逆に、衝突が起きたときなどに、`Components` がスクリプトにメッセージを送信し、それを処理できる場合もあります。Defold は内部でも、エンジンのイベントとゲームプレイ中の通信に同じメッセージングシステムを使います。 

メッセージングシステムは、アドレス指定や規約は異なるものの、Unity の SendMessage やイベントシステムにやや似ています。

詳しくは、[メッセージパッシングマニュアル](/manuals/message-passing/)をお読みください。

### アドレス指定 {#addressing}

Defold のオブジェクトとコンポーネントは、URL と呼ばれるアドレスで識別されます。

インスタンス化されたすべてのオブジェクトとコンポーネントには、それぞれ一意のアドレスがあり、見つけるためにシーングラフをたどる必要はありません。これにより、アドレス指定が明示的かつ直接的になります。

Defold の単純な URL は、次のようになります。
```lua
"/player"
```

これは、*概念的には*次のものに似ています。
```c#
GameObject.Find("player")
```

ここで、アドレスに `"/"` や `"#"` を使っていた理由を説明します。

Defold の URL は、[URL](https://en.wikipedia.org/wiki/URL) と同様に、3つの部分から構成されます。

```yaml
socket: /path #fragment
```

Defold の名称で表すと、次のようになります。

```yaml
collection: /gameobject #component 
```
上の記述の空白は、3つの部分を視覚的に区切るためだけに追加しています。

つまり、それぞれ次のものを表します。
1. `collection:` はコレクションのコンテキストを識別し、末尾に `:` が付きます。
2. `/path` はゲームオブジェクトを識別し、ID の前に `/` が付きます。
3. `#fragment` は、そのオブジェクト上の特定のコンポーネント（スクリプト、スプライト、コリジョンコンポーネントなど）を識別し、ID の前に `#` が付きます。

#### 静的なアドレス {#static-address}

これらの識別子は、それぞれを作成したときに決まり、親子関係を変更しても変わりません。ファイルの `Id` プロパティで設定するか、実行時にインスタンス化する際の `factory.create` や `collectionfactory.create` の呼び出しから取得できます。

#### 相対アドレス指定 {#relative-addressing}

常に完全な URL を使う必要があるわけではありません。

同じコレクション（同じ*ワールド*）内でメッセージを送信する場合は、ソケット部分を省略できます。

```yaml
/gameobject #component
```
同じゲームオブジェクト内のコンポーネントに送信する場合は、ゲームオブジェクト部分も省略できます。

```yaml
#component
```

便利な省略形が2つあります。
- `#` は、この*スクリプト*コンポーネントに送信します。
- `.` は、この*ゲームオブジェクト*内のすべてのコンポーネントに送信します。

相対アドレス指定と省略形を使うと、完全なパスを指定せずに、異なるコンテキストやゲームオブジェクトでも再利用できる URL を記述できます。

### GUI とレンダリングへのメッセージ送信 {#messaging-to-gui-and-render}

Defold では GUI の世界とゲームオブジェクトの世界が分かれているため、ゲームオブジェクトの `.scripts` から `.gui_scripts` へメッセージを送信することもできます。

`@` で始まる識別子を使って、特別なシステム名前空間にメッセージを送信することもできます。たとえば、レンダリングシステムには `@render` でアドレス指定できます。これを使うと、既定のレンダースクリプトでの投影の変更など、一部の組み込みレンダリング機能を制御できます。

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

詳しくは、[アドレス指定マニュアル](/manuals/addressing/)をご覧ください。

---

## プレハブとインスタンス {#prefabs-and-instances}

Unity はシーン内のあらゆるものを静的または動的にインスタンス化でき、Defold でも同じことができます。Unity では、プレハブを取得して `Instantiate(prefab)` を呼び出します。Defold には、コンテンツをインスタンス化するための3つのコンポーネントがあります。

- `Factory` - 指定されたプロトタイプである `*.go` ファイル（プレハブ）から、**1つのゲームオブジェクト**をインスタンス化します。
- `Collection Factory` - 指定されたプロトタイプである `*.collection` ファイルから、親子関係を持つ**ゲームオブジェクトの集合**をインスタンス化します。
- `Collection Proxy` - `*.collection` ファイルから新しい*ワールド*を**読み込み**、インスタンス化します。

### ファクトリー {#factory}

`Factory` コンポーネントを定義し、その `Prototype` プロパティに適切なゲームオブジェクトファイルを設定したら、コードから次のように呼び出すだけで生成できます。

```lua
factory.create("#my_factory")
```

ここではコンポーネントのアドレスを使っています。この場合は、識別子 `"#my_factory"` を使った相対パスです。

新しく作成したインスタンスの識別子が返されるため、後で使う必要がある場合は、変数に保存しておくとよいでしょう。

```lua
local new_instance_id = factory.create("#my_factory")
```

Defold では、手動でオブジェクトをプールする必要がないことを覚えておいてください。エンジン自身が内部でプール処理を行います。

詳しくは、[ファクトリーマニュアル](/manuals/factory/)をご覧ください。 

### コレクションファクトリー {#collection-factory}

`Factory` と `Collection Factory` コンポーネントの違いは、コレクションファクトリーは**複数**のゲームオブジェクトを一度に生成し、`*.collection` ファイルの定義に従って、生成時に親子関係を設定できることです。

Unity にはこのような区別はなく、Defold のコレクションファクトリーに対応する専用の概念はありません。最も近いものは、オブジェクトの階層を含む入れ子のプレハブです。

生成されたすべてのインスタンスの ID を含む**テーブル**が返されます。

```lua
local spawned_instances = collectionfactory.create("#my_collectionfactory")
```

詳しくは、[コレクションファクトリーマニュアル](/manuals/collection-factory/)をご覧ください。

#### インスタンスのカスタムプロパティ {#custom-properties-of-instances}

`factory.create()` や `collectionfactory.create()` を呼び出す際には、位置、回転、スケール、スクリプトプロパティなどの省略可能なパラメーターも指定できます。これにより、インスタンスをどこに、どのように出現させ、どのように振る舞わせるかを細かく制御できます。たとえば、次のようにします。

```lua
local scale_2d = vmath.vector3(0.5, 0.5, 1.0)
factory.create("#my_factory", my_position, my_rotation, my_properties, scale_2d)
```

省略可能な引数は、プロパティ、スケールの順に並びます。2D オブジェクトの X 軸と Y 軸だけを拡大縮小する場合は、`vector3` を使い、Z を明示的に `1.0` に設定します。数値でスケールを指定すると、3つの軸すべてに均等に適用されます。

#### 動的な読み込み {#dynamic-loading}

`Factory` と `Collection Factory` のどちらのコンポーネントでも、プロトタイプでリソースの動的な読み込みを指定できます。これにより、容量の大きいアセットは必要なときだけメモリに読み込まれ、使わなくなったらアンロードされます。

詳しくは、[リソース管理マニュアル](/manuals/resource/)をご覧ください。 

### コレクションプロキシ {#collection-proxy}

`Collection Proxy` は特定の `*.collection` ファイルを参照しますが、ファクトリーのように*現在のワールド*にオブジェクトを追加するのではなく、**新しいゲームワールドを読み込んでインスタンス化します**。Unity でシーン全体を読み込むことにやや似ていますが、より厳密に分離されます。

Unity では、次のようにシーンを追加で読み込むことがあります。

```c#
SceneManager.LoadSceneAsync("Level2", LoadSceneMode.Additive);
```

Defold では、`Collection Proxy` コンポーネントにメッセージを送信するだけで、新しいコレクションを読み込めます。

```lua
msg.post("#myproxy", "load")
```

1. プロキシに `"load"` メッセージ（非同期に読み込む場合は `"async_load"`）を送信すると、エンジンは新しいワールドを割り当て、そのコレクション内のすべてをそこにインスタンス化し、ほかから分離した状態に保ちます。
2. 読み込みが終わると、プロキシはワールドの準備ができたことを示す `"proxy_loaded"` メッセージを返します。
3. その後、通常は `"init"` と `"enable"` メッセージを送信し、新しいワールド内のオブジェクトが通常のライフサイクルを開始するようにします。

読み込んだワールド間で通信するには、ワールド名（URL の最初の部分である `collection:`）を含む URL を使って、明示的にメッセージを送信する必要があります。

この分離は、レベルの切り替え、ミニゲーム、大規模なモジュール式システムを実装するときに大きな利点となり得ます。意図しない相互作用を防ぎ、必要に応じて、一時停止やスローモーションなどのために更新タイミングを個別に制御することもできるためです。

Unity で複数のシーンを使い、それぞれを独立して動作させる必要があったなら、`Collection Proxy` は、その概念を Defold に直接取り入れるための方法と考えてください。

詳しくは、[コレクションプロキシマニュアル](/manuals/collection-proxy/)をご覧ください。

---

## アプリケーションのライフサイクル {#application-lifecycle}

Unity のライフサイクルイベントである `Awake`、`Start`、`Update`、`FixedUpdate`、`LateUpdate`、`OnDestroy`、`OnApplicationQuit` には、なじみがあるでしょう。

Defold にも明確に定義されたアプリケーションのライフサイクルがありますが、概念と用語は異なります。Defold は、初期化時、各フレーム、終了処理時にエンジンが呼び出す、定義済みの Lua コールバック群を通じてライフサイクルの各段階を提供します。

以下で比較します。

| Defold | Unity | 説明 |
|-|-|-|
| `init()` | `Awake()` / `Start()` / `OnEnable()`| Defold の初期化のエントリーポイントとコールバックは、init() の1つです。各コンポーネントが作成されたときに呼び出されます。 |
| `on_input` | 入力メソッド | Defold は、[スクリプトに入力フォーカスが設定されている](/manuals/input/#input-focus)ときに入力を受け取ります。更新ループ内で最初に処理されます。 |
| `fixed_update()` | `FixedUpdate()` | 更新やシミュレーションの時間刻みであるタイムステップが固定された間隔で呼び出されます。Defold で有効にするには、`Use Fixed Timestep` を設定する必要があります。[詳細](https://defold.com/manuals/project-settings/#use-fixed-timestep)をご覧ください。1.12.0 以降は `update()` より前に実行されます。 |
| `update()` | `Update()` | 経過時間を引数として、1フレームに1回呼び出されます。 |
| `late_update()` | `LateUpdate()` | `update()` の後、フレームが描画される直前に呼び出されます。1.12.0 以降で利用できます。 |
| `on_message` | メッセージの受信処理 | メッセージを受信するための Defold の中心的なコールバックです。キューにメッセージがあるときに処理されます。 |
| `final` | `OnDisable` / `OnDestroy` / `OnApplicationQuit` | Defold は、各コンポーネントの `final()` コールバックを、実行時にそのゲームオブジェクトが `go.delete()` で破棄されるとき、またはワールド/コレクションがアンロードされるときに呼び出します。また、アプリケーションの終了時にも、残っているすべてのオブジェクトに対して呼び出します。 |

::: sidenote
複数のコンポーネントが一度に初期化、更新、削除される場合、Defold はコンポーネント間の実行順序を保証しないことを覚えておいてください。結び付きの弱い設計を推奨します。
:::

### 初期化 {#initialization}

Defold の `init()` は、Unity の `Awake()`、`Start()`、`OnEnable()` の要素を1つのエントリーポイントにまとめたものと考えてください。この時点では、エンジンがすべての準備を終えており、安全にコンポーネントの状態を準備できます。

### メッセージはいつ処理されますか？ {#when-messages-are-handled}

`init()` の中ですでにメッセージを送信できるため、メッセージの最初の配送は初期化の直後に行われます。

その後は、内部の各処理ループの後で、キューに何かあるたびにメッセージが処理されます。そのため、たとえば1つの更新ループ内で `on_message()` が数回呼び出されることもあります。

### 更新ループ {#update-loop}

Defold は毎フレーム、入力の処理、メッセージの配送、スクリプトと GUI の更新、物理処理とトランスフォームの適用、最後にグラフィックスの描画という一連の処理を行います。

### 終了処理 {#finalization}

Defold の後片付けは、常に削除またはワールドのアンロードに結び付いており、コンポーネントごとの終了フックは `final()` だけです。

Unity のモデルとの細かな違いとして、コンポーネントの無効化とアプリケーション全体の終了が区別されません。

### レンダリング {#rendering}

レンダースクリプト（`*.render_script`）はレンダリングパイプラインの一部であり、独自の `init()`、`update()`、`on_message()` コールバックによってライフサイクルにも参加します。ただし、これらはレンダースレッドで動作し、ゲームオブジェクトや GUI スクリプトのロジックとは分かれています。

さらに詳しくは、[アプリケーションのライフサイクルマニュアル](/manuals/application-lifecycle/)をお読みください。

---

## GUI

Defold の GUI は、メニュー、オーバーレイ、ダイアログなどのユーザーインターフェース向けに用意された、単一の専用フレームワークです。UI Toolkit や Canvas を使う uGUI に似ています。

GUI はコンポーネントであり、ゲームオブジェクトやコレクションとは分かれています。ゲームオブジェクトの代わりに、階層状に配置し、GUI スクリプトで駆動する GUI ノード（GUI node）を扱います。

### GUI ノード {#gui-nodes}

Defold で `*.gui` コンポーネントファイルを開くと、`"GUI nodes"` を配置するキャンバスが表示されます。これらが GUI の基本構成要素です。次の種類の GUI ノードを追加できます。

- Box（テクスチャを持つ矩形）
- Text（任意のフォントを使ったテキスト）
- Pie（テクスチャを持ち、放射状に塗りつぶす扇形の要素）
- ParticleFX
- Template（GUI のプレハブのように、別の `.gui` ファイル全体を入れ子にしたもの）
- Spine 拡張を使う場合は、Spine ノードも追加できます。

### GUI スクリプト {#gui-script}

GUI コンポーネントには、GUI スクリプト用の特別なプロパティがあります。コンポーネントごとに1つの `*.gui_script` ファイルを割り当てて、コンポーネントの振る舞いを変更できます。通常のスクリプトによく似ていますが、ゲームオブジェクトのスクリプト用の `go.*` 名前空間は使いません。代わりに、特別な `gui.*` 名前空間の API を使います。この API は GUI スクリプト（`*.gui_script`）内でのみ動作します。独立したシーン、あるいは Canvas を使う Unity UI（uGUI）のようなものと考えることができます。

### GUI のレンダリング {#gui-rendering}

GUI 要素はゲームのカメラとは独立して、通常はスクリーン空間で描画されますが、この動作はカスタムのレンダリングパイプラインで変更できます。

さらに詳しくは、[GUI マニュアル](/manuals/gui/)をお読みください。

## Sorting Layers はどこにありますか？ {#where-are-sorting-layers}

これは、Unity から移行するときによく混乱する点です。

GUI コンポーネントには `Layers` があり、Unity の「Sorting Layers」とほぼ同じように動作します。しかし、`Sprites`、`Tilemaps`、`Models` などのほかのコンポーネントには、直接対応するものはありません。

代わりに、通常は次の方法を組み合わせます。
- 既定のカメラを使う場合は Z 軸、カメラコンポーネントを使う場合は深度によって、細かな描画順序を決めます。
- レンダースクリプトのレンダー述語を使い、マテリアルタグに基づいて描画対象を選択することで、大まかな描画順序を決めます。

ただし、多数のタグで Unity の Sorting Layers を再現しようとすることはお勧めしません。Defold のタグはレンダリングの水準で使う仕組みであり、多用するとバッチ処理が分断され、描画の負荷が増えることがあるためです。

---

## 次のステップ {#where-to-go-from-here}

- [Defold のサンプル](/examples)
- [チュートリアル](/tutorials)
- [マニュアル](/manuals)
- [API リファレンス](/ref/go)
- [よくある質問](/faq/faq)

質問がある場合や行き詰まった場合は、[Defold フォーラム](//forum.defold.com)や [Discord](https://defold.com/discord/) で相談できます。
