---
title: Godot ユーザーのための Defold
brief: Godot でおなじみの概念と比較しながら、Defold で対応するツールや API の使い方を紹介します。
---

# Godot ユーザーのための Defold {#defold-for-godot-users}

Godot でゲームを作った経験があれば、その知識の多くを Defold でも活かせます。このガイドでは、Godot での経験を活かして Defold でゲームを作り始める方法と、つまずきやすい両者の違いを説明します。比較には Godot 4.7 を使用しました。

## はじめに {#introduction}

Defold は、2D と 3D のゲームを開発できる無料のクロスプラットフォームゲームエンジンです。エディターは Windows、Linux、macOS で動作します。エンジンとエディターのソースコードはすべて [GitHub](https://github.com/defold/defold/) で公開されています。自分でビルドすることも、使用する OS 向けのビルドをダウンロードすることもできます。

一見すると、Defold と Godot はよく似ています。どちらも再利用できる部品を組み合わせてゲームを作り、スクリプトで振る舞いを加えます。Godot には用途に特化したノードが多数あります。Defold では、より汎用的な少数のコンポーネント（component）を組み合わせ、Lua スクリプトやモジュールでゲームの振る舞いを記述します。たとえばプレイヤーキャラクターは、ゲームオブジェクト（game object）にスプライトまたはモデル、コリジョンオブジェクト、スクリプトを追加して作れます。

Defold は、ランタイムを小さく保ち、リソースを効率よく使うことを重視しています。この特長は Web ゲームやモバイルゲームで特に役立ちます。エンジンが扱う要素の一部は、メモリをあらかじめ確保できるように上限を事前に設定します。

Godot よりもゲームプレイや UI にそのまま使える部品は少ないかもしれませんが、Defold の基本コンポーネントを組み合わせたり拡張したりすれば、同じ結果を得られます。Defold のエンジン本体はできる限り軽量に設計されています。不要な機能を除いてさらに小さくすることも、ネイティブ拡張や Lua モジュールで機能を追加することもできます。[Defold Asset Portal](https://defold.com/assets/) には数百のモジュール、ライブラリ、拡張があり、複雑な UI や高度なレンダリングパイプラインの構築、開発作業の簡略化などに役立ちます。

Defold の機能については、[製品の紹介ページ](https://defold.com/product/)をご覧ください。

## インストール {#installation}

1. [ダウンロードページ](https://defold.com/download/)から、使用する OS 向けの Defold をダウンロードします。
2. ファイルを展開し、エディターを起動します。

別途ハブやエクスポートテンプレートをインストールせずに、最初のプロジェクトを作成して実行できます。プラットフォーム別の手順は[インストールマニュアル](/manuals/install/)を参照してください。

Defold はエディターから更新できます。既存のプロジェクトを更新する際は、リリースノートを確認し、対象プラットフォームでゲームをテストしてください。

## ウェルカム画面 {#welcome-screen}

Defold を起動するとウェルカム画面が開きます。ここで最近使ったプロジェクトを開いたり、新しいプロジェクトを作成したりできます。Godot のプロジェクトマネージャーにあたる画面です。

![Godot のプロジェクトマネージャーと Defold のウェルカム画面](images/godot/godot_1.png)

Defold では、次の項目から新しいプロジェクトを始められます。

- **Templates** では、空のプロジェクトや特定のプラットフォーム向けの基本プロジェクトを選べます。
- **Tutorials** では、手順に沿って作業を進める入門プロジェクトを選べます。
- **Samples** では、実際に動かして仕組みを調べられるサンプルやスターターキットを選べます。

![Godot のプロジェクトマネージャーと Defold のウェルカム画面](images/godot/godot_2.png)

Defold の Samples には、Godot の Asset Store にあるスターターキットやサンプルに相当するプロジェクトや作例が用意されています。

![Godot のプロジェクトマネージャーと Defold のウェルカム画面](images/godot/godot_3.png)

:[Hello World](../shared/hello-world.md)

---

## Defold エディターの概要 {#defold-editor-overview}

名前や配置は違いますが、主要なペインは Godot ユーザーにとって見慣れたものでしょう。比較しやすいように、下の図では Godot エディターのパネルを Defold の既定の配置に合わせています。

![Godot エディターの概要](images/godot/godot_4.png)
![Defold エディターの概要](images/godot/godot_5.png)

| Godot | Defold | Defold エディターでの役割 |
|---|---|---|
| FileSystem ドック | Assets | プロジェクトのファイルやフォルダーを管理します。ディスク上のプロジェクトディレクトリと一対一で対応します。 |
| 2D/3D ビューとリソースエディター | Main editor | コレクション（collection）、GUI、アトラス、スクリプトなど、開いたファイルに応じて表示が変わります。2つのペインに分割できます。 |
| Scene ドック | Outline | 現在のリソースの構造を表示します。実行中のゲーム全体のシーンツリーとは異なります。 |
| Inspector | Properties | 選択したオブジェクト、コンポーネント、リソースのプロパティを表示します。 |
| Output と Debugger | Tools | Console、Build Errors、Search Results、デバッガーなどを備えています。 |
| バージョン管理との統合 | Changed Files | プロジェクトで Git を使用している場合に、変更を表示します。 |

Defold の 3D エディターには右上にツールバーもあります。詳しくは[シーン編集マニュアルのツールバーの概要](/manuals/scene-editing/#toolbar-overview)を参照してください。

### 2D と 3D のシーンの向き {#2d-and-3d-scene-orientation}

:[2D and 3D scene orientation](../shared/2d-and-3d-scene-orientation.md)

### ペイン {#panes}

Defold のペインは別のウィンドウに切り離せませんが、境界をドラッグしてサイズを変更できます。`F6`、`F7`、`F8` キー、または `View` メニューで表示と非表示を切り替えられます。

![ペインの表示と非表示](images/editor/editor_panes.png)

### 座標 {#coordinates}

Defold のコレクションで既定のレンダースクリプトを使い、カメラコンポーネントを配置していない場合、2D の座標 `(0, 0)` はゲームウィンドウの左下にあります。Y 軸の正の向きは**上**、X 軸の正の向きは右です。

Godot の通常の 2D スクリーン座標では、Y 軸の正の向きは**下**です。位置や移動のコードを移植するときは、この違いに注意してください。

![Defold と Godot の 2D 座標の違い](images/godot/godot_6.png)

Godot の 3D 座標系では、Defold と同じく Y 軸の正の向きは上です。Defold は 2D と 3D のゲームを共通の 3D 座標系で扱います。一般的な 2D の設定では XY 平面を正投影で表示します。必要に応じてカメラの設定を変えることもできます。

![Defold と Godot に共通する 3D 座標の向き](images/godot/godot_7.png)

Defold エディターの詳しい説明は、[エディターの概要マニュアル](/manuals/editor/)を参照してください。

---

## 主な概念 {#key-concepts}

Godot では、ノードを組み合わせて**シーン**を作ります。Defold では、コンポーネント、ゲームオブジェクト、そしてゲームオブジェクトをまとめるコレクションを使います。

たとえば Godot でプレイヤーを作るなら、`Node2D` の子に `Sprite2D` を追加し、ルートにスクリプトをアタッチして、最初の `Scene` に配置します。
Defold では、`Sprite` コンポーネントと `Script` コンポーネントを持つゲームオブジェクトとしてプレイヤーを作り、コレクションに配置します。

![Godot のノード構成と Defold のゲームオブジェクトおよびコンポーネントの比較](images/godot/key_concepts.png)

これらの概念については、[基本構成要素マニュアル](/manuals/building-blocks/)で詳しく説明しています。

### ゲームオブジェクト {#game-objects}

Defold の**ゲームオブジェクト**は、コンポーネントを格納する*コンテナー*で、次のものを持ちます。

- **識別子**
- **トランスフォーム**（位置、回転、スケール）

ゲームオブジェクトは、Godot の `Node2D` や `Node3D` と似た役割を果たせます。Defold には 2D 専用のゲームオブジェクト型はありません。2D ゲームでも、すべてのゲームオブジェクトが 3D のトランスフォームを使います。

Defold では、別のゲームオブジェクトの子になると親のトランスフォームを継承します。この親子関係は、コレクション内で設定することも実行時に変更することもできます。親子関係を変更しても、ゲームオブジェクトのアドレスは変わりません。

コレクションには、`.collection` ファイル内に直接定義する**埋め込み**ゲームオブジェクトを置く方法と、再利用可能な `.go` プロトタイプへの参照を追加する方法があります。埋め込みオブジェクトの定義を編集した場合、変更されるのはそのコレクションで、別途定義したオブジェクトには影響しません。`.go` プロトタイプを編集すると、それを参照するすべてのインスタンスに変更が反映されますが、インスタンスごとに上書きした値は優先されます。コンポーネントが参照するリソースは埋め込みオブジェクト同士でも共有できるため、そのリソースを編集すると、ほかの使用箇所にも影響が及ぶことがあります。コレクション自体を再利用している場合は、埋め込みオブジェクトへの変更が、そのコレクションを参照するすべての箇所に反映されます。

### コンポーネント {#components}

コンポーネントは、ゲームオブジェクトの外観、物理、音声、振る舞いなど、それぞれの機能を担う基本構成要素です。

ゲームオブジェクトに `Sprite` コンポーネントを追加すると画像を表示でき、`Sound` コンポーネントを追加すると音声を再生でき、`Script` コンポーネントを追加すると Lua コードを実行できます。

コンポーネントはゲームオブジェクトに属し、子コンポーネントを持つことはできません。階層を作るには、コレクション内でゲームオブジェクト同士に親子関係を設定します。

また、Godot のようにコンポーネントにスクリプトをアタッチして、その振る舞いを変更することはできません。Properties でコンポーネントを調整したり、Godot の GDExtension と同様にネイティブ拡張で独自のコンポーネントを作成したりできます。カスタムコンポーネントの例としては、公式の [Rive](https://github.com/defold/extension-rive) や [Spine](https://github.com/defold/extension-spine)、コミュニティが提供する [Sprite Loop](https://github.com/Balkan-Ram-Games/spriteloop-defold) や [Object Interpolation](https://github.com/indiesoftby/defold-object-interpolation) があります。

Defold のスクリプトは独立したコンポーネントで、どのゲームオブジェクトにも追加できます。1つのゲームオブジェクトに、スクリプトを含む複数のコンポーネントをアタッチできます。

コンポーネント同士は階層を持たず、独自のスクリプトからも切り離されています。この構造により、Defold はデータ指向設計を活かしてコンポーネントをメモリ上に効率よく配置できます。

| Godot のノード | Defold のコンポーネント | 説明 |
|---|---|---|
| `Sprite2D` / `AnimatedSprite2D` | [スプライト](/manuals/sprite/) | アトラス（複数の画像をまとめたテクスチャ）やタイルソースを使って、2D テクスチャやフリップブックアニメーションを描画します。 |
| `Area2D` / `RigidBody2D` / `StaticBody2D` と、それぞれに対応する 3D ノード | [コリジョンオブジェクト](/manuals/physics-objects/) | 物理やトリガーを処理します。コリジョン形状は個別の子ノードとして追加せず、コンポーネント内で直接定義します。種類は静的、動的、キネマティック、トリガーから選べます。 |
| ノードにアタッチした `.gd` スクリプト | Script | Lua コードでゲームロジックや入力を処理し、ほかのコンポーネントやゲームオブジェクトを制御します。 |
| `TileMapLayer` | [タイルマップ](/manuals/tilemap/) | タイルソースとタイルマップのレイヤーを使い、グリッド状のマップを描画します。 |
| `Label` | [GUI テキストノード](/manuals/gui-text/) | UI に表示する文字には GUI テキストを、ゲームワールド内に表示する文字には[ラベルコンポーネント](/manuals/label/)を使います。 |
| `AudioStreamPlayer` | [サウンド](/manuals/sound/) | 音声を再生します。Speed、Pan、Gain を設定できます。 |
| `Camera2D` / `Camera3D` | [カメラ](/manuals/camera/) | 正投影と透視投影に対応します。 |
| `Control` の階層 / `CanvasLayer` | [GUI](/manuals/gui/) | GUI コンポーネント内には Box、Text、Pie などのノードからなる独立した階層があり、専用の `.gui_script` で制御します。 |
| `MeshInstance3D` | [モデル](/manuals/model/)または[メッシュ](/manuals/mesh/) | Model はインポートした 3D コンテンツに対応し、Mesh はバッファーを使って独自のジオメトリを扱えます。 |
| `CPUParticles2D` / `GPUParticles2D` と、それぞれに対応する 3D ノード | [ParticleFX](/manuals/particlefx/) | Defold のパーティクルエディターで設定した 2D/3D のパーティクルを放出します。 |
| `PackedScene.instantiate()` | Factory / Collection Factory | 実行時に生成するゲームオブジェクトやコレクションを定義します。それぞれに専用のコンポーネントがあります。 |

### コレクションとワールド {#collections-and-worlds}

**コレクション**は、ゲームオブジェクトとそのコンポーネント、ゲームオブジェクト同士の親子関係を記述します。別のコレクションの中にコレクションを入れると、一群のオブジェクトを再利用できます。これは Godot でシーンを入れ子にするのと似ています。Defold には、Godot のようにシーンを継承して広く利用できる仕組みはありません。代わりにプロトタイプやコレクションを再利用し、プロパティやスクリプトでインスタンスをカスタマイズします。

コレクションファイル自体は、実行時のオブジェクトではありません。メソッドを呼び出せるコレクションオブジェクトも、コレクション自体に対応するルートノードもありません。コレクションファイルには、Defold が実行時にゲームオブジェクトとコンポーネントを作成し、階層を構築するための定義が含まれています。

ゲームの起動時に Defold は `game.project` ファイルを読み込みます。このファイルの **Bootstrap ▸ Main Collection** で最初に読み込むコレクションを指定すると、それをもとに最初のゲームワールドが作成されます。入れ子にしたコレクションに配置したオブジェクトも、同じワールドに属します。

**コレクションファクトリー**（collection factory）コンポーネントは、ファクトリー（factory）がある**既存の**ワールドに、一群のゲームオブジェクトとそのコンポーネントを生成します。

一方、**コレクションプロキシ**（collection proxy）は、別のコレクションを読み込み、独自のアドレス名前空間と物理シミュレーションを持つ**新しいワールド**を作成します。たとえば、敵を既存のレベルに生成してその地形と衝突させたいのか、まったく新しいレベルを必要に応じて非同期に読み込みたいのかで、使う仕組みが異なります。これらの操作は後ほど説明します。

Godot では、インスタンスの生成にもシーンの切り替えにも `PackedScene` を使います。そのうち `SceneTree` を介したシーンの切り替えは、コレクションプロキシで別のワールドを読み込む操作に似ています。

対応関係を表にまとめます。

| Godot | Defold | 説明 |
|---|---|---|
| 子ノードを持つ `Node3D` | コンポーネントを持つゲームオブジェクト | コンポーネントは機能や振る舞いを、ゲームオブジェクトはトランスフォームと識別子を提供します。 |
| `Node2D` / `Node3D` のトランスフォーム | ゲームオブジェクトのトランスフォーム | すべてのゲームオブジェクトに組み込まれています。 |
| シーン / `PackedScene` | ゲームオブジェクトのプロトタイプ（`.go`）またはコレクション（`.collection`） | プロトタイプは1つのオブジェクトを記述します。コレクションは複数のオブジェクトとその階層を記述します。 |
| `PackedScene.instantiate()` | ファクトリーまたはコレクションファクトリー | 現在のワールドに1つまたは複数のゲームオブジェクトを生成し、それらの識別子を返します。 |
| `SceneTree` と `PackedScene.instantiate()` を使ったシーンの切り替え | コレクションプロキシ | 独立した新しいワールドを読み込んで作成し、その中にゲームオブジェクトを生成します。 |

---

## コードの記述 {#code-writing}

Defold エディターには、すべてのテキストファイルやスクリプトを編集できるテキストエディターが組み込まれています。自動補完、整形、データや関数の構成を一覧表示する Structure などが使えます。詳しくは[組み込みのコードエディターの使用](/manuals/writing-code/#using-the-built-in-code-editor)を参照してください。

Defold のテキスト形式のファイルやスクリプトは、すべて外部エディターでも開けます。VS Code などの外部ツールと連携し、そこから Defold を使いやすくする機能もあります。詳しくは[外部コードエディターの使用](/manuals/writing-code/#using-an-external-code-editor)を参照してください。

### Lua とスクリプト {#lua-and-scripts}

Defold ではゲームプレイ用のスクリプトを Lua で記述します。GDScript と似ている部分もありますが、重要な違いもあります。Lua に静的型付けを導入した言語 Teal も使用できます。また、対象プラットフォームに応じて C、C++、C#、Objective-C、Java、JavaScript で記述したネイティブ拡張も利用できます。これは Godot の GDExtension に相当し、後ほど取り上げます。

Defold で主に使用する Lua ファイルは次のとおりです。

| ファイル | 用途 |
|---|---|
| `.script` | ゲームのロジックと振る舞いを記述します。`go`、`factory`、`sprite`、`tilemap`、`physics` などの API で、ほかのゲームオブジェクトやコンポーネントを制御します。 |
| `.gui_script` | GUI 専用のスクリプトです。`gui` API で振る舞いを定義します。 |
| `.render_script` | `render` API を使ってレンダリングを制御します。 |
| `.lua` | `require()` で読み込む再利用可能な Lua モジュールです。コードライブラリやユーティリティースクリプトなどに使います。 |

Lua のテーブルには、データも関数も格納でき、両方を混在させることもできます。コードを整理するために GDScript のクラス階層を再現する必要はありません。再利用したいロジックをモジュールにまとめ、その振る舞いを担当するスクリプトから呼び出します。

Defold のスクリプトは Lua 5.1 と互換性があります。言語上の違いやプラットフォームごとの詳細は、[Defold の Lua](/manuals/lua/) を参照してください。

### アプリケーションのライフサイクル {#application-lifecycle}

通常、Defold のゲームは初期化フェーズで始まり、終了処理フェーズで終わります。その間はフレームごとに更新ループが実行され、トランスフォームとコンポーネントの更新、コードの実行、メッセージの処理が行われます。

![Defold アプリケーションのライフサイクル](images/application_lifecycle/application_lifecycle.png)

Godot などのゲームエンジンと同じように、Defold のスクリプトでは、アプリケーションのライフサイクルに応じて Lua のコールバック関数が呼び出されます。名前は異なりますが、役割には共通する部分があります。

| Godot | Defold | 用途 |
|---|---|---|
| `_ready()` | `init(self)` | インスタンスデータを初期化し、必要に応じて入力フォーカスを取得します。 |
| `_process(delta)` | `update(self, dt)` | フレームごとに1回更新します。 |
| `_physics_process(delta)` | `fixed_update(self, dt)` | 有効にすると、一定の時間間隔で更新します。 |
| `_input(event)` | `on_input(self, action_id, action)` | オブジェクトの入力リスナーに届いた入力を処理します。 |
| シグナルのコールバック | `on_message(self, message_id, message, sender)` | スクリプトやエンジンのコンポーネントからのメッセージを受け取ります。 |
| `_exit_tree()` | `final(self)` | スクリプトインスタンスの終了時に後片付けをします。 |

Godot は親より先に子の `_ready()` を呼び出します。Defold では、ゲームオブジェクトやコンポーネント間の初期化順序や更新順序は保証されません。特定のオブジェクトの `init()` が先に実行されることに依存せず、メッセージでオブジェクト間の処理を調整してください。

`fixed_update()` を使うには、`game.project` の **Engine ▸ Fixed Update Frequency** を 60 などの正の値に設定し、**Physics ▸ Use Fixed Timestep** を有効にします。

通常の更新が終わってから描画が始まるまでにカメラを調整する、といった処理には `late_update(self, dt)` を使えます。必要に応じて、その後にトランスフォームの最終更新が行われることがあります。

コンポーネントの無効化と削除は別の操作です。

処理順序の全体像と、各スクリプトの種類で使用できるコールバックは、[アプリケーションのライフサイクルマニュアル](/manuals/application-lifecycle/)を参照してください。

### インスタンスデータとローカルデータ {#instance-data-vs-local-data}

スクリプトコンポーネントの各インスタンスは、コールバックの引数として専用の `self` を受け取ります。`self.health` や `self.target` のように、インスタンスごとの状態をここに保存します。同じゲームオブジェクトに2つのスクリプトコンポーネントを追加した場合でも、それぞれの `self` は別のものです。`self` はテーブルと同じ書き方でフィールドにアクセスできる userdata であり、Lua のテーブルではないため、`pairs(self)` などの操作はできません。Godot のインスタンス変数（`var`）と同じような用途に使います。

Godot はそれぞれの `.gd` ファイルをクラスの定義として扱います。1つの `.gd` ファイルを10体の敵にアタッチすると、個別のクラスインスタンスが10個作られ、トップレベルで var 宣言した変数もインスタンスごとに用意されます。

Defold は、スクリプトリソースの読み込み時に `.script` ファイルを Lua のコードのまとまり（チャンク）として実行します。スクリプトコンポーネントの各インスタンスは、`init(self)` や `update(self, dt)` などのライフサイクルコールバックで個別の `self` を受け取ります。

これに対し、Defold の `.script` ファイルのトップレベルで宣言したローカル変数は、そのスクリプトの**すべてのインスタンス**で共有されます。このファイル単位のローカル変数に相当するのが、Godot の静的変数（`static var`）です。

![Defold のインスタンスデータとローカルデータの違い](images/lua/self_local.png)

上の例で1つのインスタンスの `self.has_shield` を `true` に変更しても、ほかのインスタンスには影響しません。一方、ローカル変数 `color` はこのスクリプトファイルを使うインスタンス間で共有されているため、変更するとすべてのインスタンスに影響する可能性があります。

### プロパティ {#properties}

インスタンスごとに編集できる**プロパティ**は `go.property()` で定義し、`self` を通じてアクセスします。Godot の `@export` と同じように値がエディターに公開され、Defold では `Properties` に表示されます。

![Defold エディターの Properties ペイン](images/script-properties/properties.png)

Godot で `Node3D` にアタッチした **GDScript** と比較してみましょう。

```gdscript
extends Node3D

@export var speed: float = 100.0

func _process(delta):
    position.x += speed * delta
```

Defold でスクリプトコンポーネントとしてアタッチした **Lua** は次のようになります。

```lua
go.property("speed", 100)

function update(self, dt)
    local position = go.get_position()
    position.x = position.x + self.speed * dt
    go.set_position(position)
end
```

この Lua プロパティは `self.speed` として参照でき、オブジェクトの生成時に値を渡すこともできます。Defold のトランスフォームは 2D でも `vector3` を使うため、Z 座標も指定します。

対応するプロパティの型は[スクリプトプロパティ](/manuals/script-properties/)を参照してください。[スクリプト](/manuals/script/)には、ほかの使用例もあります。

---

## メッセージとアドレス指定 {#messages-and-addressing}

Godot のシグナルは、オブジェクトのイベントを接続先のリスナーに通知します。Defold のスクリプトでは通常、ゲームオブジェクトやコンポーネントのアドレスにメッセージを送って通信します。

Defold ではどのスクリプトからでも `msg.post()` 関数でメッセージを送信できます。受信側のスクリプトでは `on_message()` コールバックでメッセージを受け取り、処理します。

![Defold のメッセージ](images/message_passing/messages_overview.png)

例として、プレイヤーから HUD にスコアの変更を通知してみましょう。

Godot では `Player`（`Node2D`）に `player.gd` をアタッチします。その兄弟ノードの `GUI`（`CanvasLayer`）には `gui.gd` をアタッチし、子に `ScoreText` という Label を置きます。

![Godot でシグナルを使用する構成](images/godot/godot_signals.png)

Defold では `player` ゲームオブジェクトに `player.script` を追加します。`hud` ゲームオブジェクトに追加した `gui` コンポーネントは、`score` というテキストノードを持ち、`hud.gui_script` を使います。

![Defold でメッセージを使用する構成](images/godot/defold_messages.png)

### メッセージの送信 {#sending-messages}

Godot では Player と GUI は兄弟ノードです。Player は自身の `score_changed` シグナルを GUI スクリプトのメソッドに接続し、そのメソッドで Label を更新します。

**GDScript** の `player.gd` では次のようになります。

```gdscript
extends Node2D

signal score_changed(value: int)
var score: int = 0

func _ready() -> void:
    score_changed.connect(get_node("../GUI").set_score)

func collect() -> void:
    score += 1
    score_changed.emit(score)

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventKey and event.pressed and not event.echo:
        if event.keycode == KEY_SPACE:
            collect()
```

Godot の `Player` は `score_changed` というシグナルを定義し、`_ready()` で GUI スクリプトの `set_score()` メソッドに接続します。`collect()` が呼び出されるたびにスコアが増え、新しい値とともにシグナルが送出されます。

Defold では、入力バインディング（input binding）で **Space** キーを `collect` アクションに割り当てます。`player` は `init()` でスコアを初期化し、入力イベントを受け取るために入力フォーカスを取得します。`collect(self)` が呼び出されると、スコアを1増やし、新しいスコアをメッセージのテーブルに入れて `score_changed` メッセージを `/hud#gui` に送ります。

**Lua** の `player.script` では次のようになります。

```lua
function init(self)
    self.score = 0
    msg.post(".", "acquire_input_focus")
end

local function collect(self)
    self.score = self.score + 1
    msg.post("/hud#gui", "score_changed", { value = self.score })
end

function on_input(self, action_id, action)
    if action_id == hash("collect") and action.pressed then
        collect(self)
    end
end
```

Defold では、Godot のように Player のシグナルをあらかじめ GUI に接続する必要はありません。受信側のアドレスにメッセージを送るだけです。Defold の相対アドレス指定と組み合わせると、再利用可能な関数やスクリプトを書けます。

### メッセージの受信と処理 {#receiving-and-handling-messages}

続いて、GUI が値を受け取り、スコアの表示を更新します。

**GDScript** では、`GUI`（`CanvasLayer`）に次の `gui.gd` をアタッチします。

```gdscript
extends CanvasLayer

func set_score(value: int) -> void:
    $ScoreText.text = str(value)
```

GUI スクリプトは送出された値を `set_score()` で受け取り、子ノードの `ScoreText` Label を更新します。Player が Label に直接アクセスしたり、その値を書き換えたりすることはありません。

Defold の GUI スクリプトは、最初に `gui.get_node()` でスコアのテキストノードを取得します。GUI コンポーネントにメッセージが届くと、`on_message()` でその識別子を確認します。`score_changed` であれば、`message.value` を読み取り、`gui.set_text()` でテキストを更新します。

**Lua** では、次の `hud.gui_script` を GUI コンポーネントに割り当てます。

```lua
function init(self)
    self.score_node = gui.get_node("score")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("score_changed") then
        gui.set_text(self.score_node, tostring(message.value))
    end
end
```

Defold のメッセージの宛先は、スコアのテキストノードではなく GUI **コンポーネント**です。メッセージを受け取った GUI スクリプトが、その内容をどう使い、どのテキストノードを更新するかを決めます。

どちらの画面にも、初期状態では `Score: 0` と表示されています。これらのスクリプト例では、スコアが変わると文字列全体を新しい数値で置き換えます。

`msg.post()` はメッセージをキューに入れます。受信側をその場で呼び出すわけではなく、受信側のスクリプトからの戻り値もありません。多くのメッセージは同じフレーム内に配信されますが、フレーム内の配信処理の回数には上限があり、長いメッセージチェーンが次のフレームにまたがることもあります。返信するには、`on_message()` に渡された送信元 URL に新しいメッセージを送ります。詳しくは[メッセージチェーン](/manuals/message-passing/#message-chains)を参照してください。

複数のリスナーに通知する場合も仕組みが異なります。Godot では1つのシグナルを複数のメソッドに接続でき、シグナルを送出すると接続先のリスナーすべてに通知されます。Defold のメッセージは特定のアドレスに届きます。複数の宛先に通知するには、送信側から個別にメッセージを送るか、ゲームに購読の仕組みを実装します。

### オブジェクトを見つけるための Defold のアドレス指定 {#finding-an-object-addressing-in-defold}

別のスクリプトインスタンスを表す Lua オブジェクトを取得する、汎用的な `get_node()` 相当の関数はありません。`go.get_position()`、`go.set()`、`msg.post()` などのエンジン API に識別子や **URL** を渡して操作します。

Defold の URL は3つの部分で構成されます。

```lua
socket:/path#component
```

- **ソケット（Socket）**は、起動時に読み込まれたメインコレクションのワールドや、コレクションプロキシで読み込まれたワールドを特定します。
- **パス（Path）**は、そのワールド内のゲームオブジェクトを特定します。
- **コンポーネント（Component）**は、そのゲームオブジェクトのコンポーネントを特定します。

URL 全体を指定することも、一部を省略して相対アドレスにすることもできます。たとえば、同じゲームオブジェクト上のコンポーネントを指定するには、スクリプトからコンポーネント部分だけを指定できます。よく使う指定方法は次のとおりです。

| アドレス | 意味 |
|---|---|
| `"#sprite"` | 現在のゲームオブジェクト上の sprite コンポーネントです。 |
| `"/player#controller"` | 現在のワールドにある player 上の controller コンポーネントです。 |
| `"level:/player#controller"` | 読み込まれた level という名前のワールドにある controller コンポーネントです。 |
| `"."` | 現在のゲームオブジェクト（`Game Object`）を表す省略形です。そのオブジェクトのコンポーネントにメッセージが届きます。 |
| `"#"` | 現在の `Script` コンポーネントを表す省略形です。 |

入れ子にしたコレクションの名前はオブジェクトのパスの接頭辞になる場合がありますが、トランスフォームを継承するために親子関係を設定しても、オブジェクトのアドレスは変わりません。

動的に生成したオブジェクトは、`factory.create()` または `collectionfactory.create()` が返す識別子をコード内に保持して参照します。

Godot のグループはゲーム内のオブジェクトを検索したり、`call_group()` でまとめて呼び出したりするときに使います。Defold に相当する組み込み機能はないので、オブジェクトを登録する仕組みや、メッセージの配信先を決める仕組みを自分で用意します。

Defold のコリジョンオブジェクトの物理グループは、どのグループと衝突するかをマスクで指定するためのフィルターであり、メッセージ通信とは関係ありません。

[アドレス指定](/manuals/addressing/)と[メッセージパッシング](/manuals/message-passing/)のマニュアルは早めに読んでおくことをお勧めします。最初のプロジェクトでよく出てくる疑問の多くが、そこで解決できます。

---

## Autoload と状態の共有 {#autoloads-and-shared-state}

Defold のメッセージシステムを介さず、Lua モジュールの関数を直接呼び出す方法もあります。

Godot の **Autoload** に共有データを持たせる用途には、Defold の Lua モジュールが使えます。たとえば `modules/game_state.lua` にモジュールを保存し、`require "modules.game_state"` で読み込みます。

**GDScript** では、`game_state.gd` を `GameState` という名前の Autoload として登録します。

```gdscript
extends Node
var score: int = 0
```

**Lua** で同じ役割を果たす `modules/game_state.lua` は次のとおりです。

```lua
local M = { score = 0 }
return M
```

ほかのスクリプトから共有データを利用できます。

**GDScript** の例です。

```gdscript
func add_point():
    GameState.score += 1
```

**Lua** の例です。

```lua
local game_state = require "modules.game_state"

local function add_point()
    game_state.score = game_state.score + 1
end
```

`require()` 関数はモジュールをキャッシュするため、呼び出し元はそのモジュールが返すテーブルを共有します。ゲームオブジェクトのスクリプト、GUI スクリプト、レンダースクリプトは Lua の状態を共有します。コレクションプロキシをアンロードしてもモジュールのデータはリセットされません。新しいゲームを始めるときに明示的にリセットできます。

Defold の Lua モジュールはゲームオブジェクトではなく、ライフサイクル、メッセージ、入力のコールバックを受け取りません。Godot の Autoload で毎フレームの処理、サウンドの再生、レベルの切り替えを行っていた場合は、その処理をコレクション内のゲームオブジェクトのスクリプトに記述します。モジュールに関数を定義し、スクリプトのライフサイクルコールバックから明示的に呼び出すこともできます。

Lua モジュール `my_module` の例です。

```lua
local M = {}

function M.init(self)
    print("My init")
end

return M
```

Lua スクリプトから次のように呼び出します。
```lua
local my_module = require "my_module"

function init(self)
    my_module.init(self)
end
```

インスタンスごとにデータを持たせる場合は、新しいテーブルを作成する関数をモジュールから返し、そのテーブルを `self` に保存できます。詳しい説明とホットリロード時の注意点は、[モジュールマニュアル](/manuals/modules/)を参照してください。

---

## オブジェクトの生成とレベルの読み込み {#spawning-objects-and-loading-levels}

### ファクトリー {#factories}

Defold でゲームオブジェクトを1つ生成するには、**Factory** コンポーネントを追加し、その **Prototype** に使用する `.go` ファイルを設定します。

コレクションから生成する場合も同様に、**Collection Factory** を追加して `.collection` ファイルを指定します。複数のオブジェクトを親子関係を保ったまま生成できます。

たとえば次の Godot の例では、シーンの原点に配置した `Node2D` にスクリプトをアタッチし、そこから弾を生成します。

**GDScript** の例です。

```gdscript
extends Node2D

const BULLET = preload("res://bullet.tscn")

func spawn_bullet():
    var bullet = BULLET.instantiate()
    bullet.position = Vector2(200, 100)
    add_child(bullet)
    return bullet
```

Defold では、ゲームオブジェクトに ID が `bullet_factory` のファクトリーコンポーネントを追加します。`factory.create()` を呼び出すと、そのファクトリーの `Prototype` が参照するゲームオブジェクトを生成できます。

![Defold でファクトリーを使用する構成](images/godot/defold_factory.png)

上の画面では `init()` でファクトリーを呼び出しています。生成位置を指定して識別子を返すヘルパー関数は、次のように書けます。

**Lua** の例です。

```lua
local function spawn_bullet()
    local position = vmath.vector3(200, 100, 0)
    local id = factory.create("#bullet_factory", position)
    return id
end
```

Defold の関数が返すのはオブジェクトの**識別子**で、メソッドを持つオブジェクトではありません。識別子を `go` の関数に渡して使います。また、生成したオブジェクトに `controller` というスクリプトコンポーネントがあれば、`msg.url(nil, id, "controller")` でその URL を組み立てられます。

コレクションファクトリーは、プロトタイプ内のオブジェクト ID と、生成したオブジェクトの ID を対応付けるテーブルを返します。後で生成したオブジェクトを削除できるよう、このテーブルを保持しておきます。

```lua
local ids = collectionfactory.create("#collection_factory")
-- Later, when the spawned objects are no longer needed:
go.delete(ids)
```

Godot の `queue_free()` と異なり、`go.delete(id)` は既定では子を再帰的に削除しません。オブジェクトとその時点での子孫をまとめて削除するには `go.delete(id, true)` を使います。ファクトリーが返したテーブルを `go.delete(ids)` に渡すと、テーブルに含まれるオブジェクトだけが削除され、後からその子にした別のオブジェクトは再帰的には削除されません。一方、ルートを指定して再帰的に削除すると、その時点でその配下にあるほかのオブジェクトも削除されます。詳しくは [`go.delete()`](/ref/go/#go.delete) を参照してください。

Defold は、ゲームオブジェクトとコンポーネントに必要な領域をあらかじめ確保します。上限に達して生成に失敗した場合は、`game.project` の **Collection ▸ Max Instances** と該当するコンポーネントの上限を確認してください。すべての上限を引き上げると、メモリ使用量も増えます。

プロパティ、トランスフォーム、動的な読み込みの詳細は、[ファクトリー](/manuals/factory/)と[コレクションファクトリー](/manuals/collection-factory/)のマニュアルを参照してください。

### コレクションプロキシ {#collection-proxies}

Defold でレベルなどのコレクションを読み込むには、レベルが切り替わっても残るオブジェクトに **Collection Proxy** コンポーネントを追加し、**Collection** プロパティに対象の `.collection` ファイルを設定します。

![Defold でコレクションプロキシを使用する構成](images/godot/defold_proxy.png)

`msg.post()` で `"load"` または `"async_load"` を送って読み込みを要求します。完了すると、プロキシから `"proxy_loaded"` メッセージが返ってきます。次に、読み込んだコレクションのアドレス（on_message の `sender` に渡されます）に `"init"` と `"enable"` を送信すると、そのワールドを初期化して起動できます。

これにより、どのワールドを読み込み、どれを実行するかを明示的に制御できます。Godot のシーン切り替えのように現在のシーンが自動的に置き換わるわけではありません。ほかのコレクションをアンロードしてそのワールドを取り除くには、`"unload"` メッセージを送ります。プロキシが自動的に無効化と終了処理を行ってからワールドをアンロードし、`"proxy_unloaded"` で応答します。各段階を個別に制御する場合は、`"disable"` と `"final"` を別々に送ることもできます。

異なるプロキシワールドのコリジョンオブジェクト同士は、同時に読み込まれて画面に表示されていても、互いに衝突しません。ただし、宛先のソケットを含む URL を使えば、ワールドをまたいでゲームオブジェクトやコンポーネントがメッセージをやり取りできます。

レベルの切り替えを実装する前に、[コレクションプロキシマニュアル](/manuals/collection-proxy/)をお読みください。読み込みとアンロード、入力の転送、読み込んだワールドの更新レートの制御について説明しています。

## プロジェクトのリソースとアセット {#project-resources-and-assets}

Defold のプロジェクトは `game.project` とスクリプト、リソースを含むフォルダーです。**Assets** ペインには、そのフォルダー構成がそのまま表示されます。Defold のリソース定義の多くはテキストファイルなので、バージョン管理システムで変更内容を確認できます。

ゲームをビルドまたはバンドルすると、Defold は元のリソースを実行時に使う形式に変換します。メインコレクション、ファクトリー、コレクションプロキシが参照するリソースは依存関係ツリーを構成します。プロジェクトフォルダーにファイルを置いても、どこからも参照されていなければバンドルには含まれません。

Godot のカスタム `Resource` クラスや `.tres` ファイルと同じ用途をすべてカバーする仕組みは、Defold にはありません。エンジンで扱うコンテンツには Defold のリソース型を、独自のゲームデータには Lua テーブルやデータファイルを使います。[`resource` API](/ref/resource/) を使うと、対応するリソースを実行時に作成、変更できます。

通常のファクトリーが使うリソースは、ファクトリーと同時に読み込まれます。後で読み込みたい場合は **Load Dynamically** を有効にし、`factory.load()` または `collectionfactory.load()` を使って非同期に準備します。コレクションプロキシのコンテンツは、読み込みを要求した時点で読み込まれます。

バンドル内にあるコンテンツを後から読み込むことと、後からダウンロードすることは別の操作です。Defold の [Live Update](/manuals/live-update/) を使うと、最初のバンドルから一部のコンテンツを除き、別途配布できます。

詳しくは[リソース管理マニュアル](/manuals/resource/)を参照してください。

---

## 入力 {#input}

Godot の `InputMap` に相当するのが Defold の `.input_binding` ファイルです。キーボード、ゲームパッド、マウス、タッチ、テキスト入力などからのトリガーにアクション名を割り当てます。使うバインディングファイルは `game.project` の **Input ▸ Game Binding** で選択します。

![入力バインディング](images/input/defold_input.png)

Defold で入力を受け取るには、ゲームオブジェクトが**入力フォーカスを取得**する必要があります。これによりオブジェクトが入力スタックに積まれ、そのスクリプトと GUI コンポーネントに `on_input()` コールバックが届くようになります。

上の画面では Space キーを `collect` に割り当てています。次の例では別のアクション `fire` を使うので、これも入力バインディングに追加してください。

**GDScript** の例です。

```gdscript
extends Node

func _input(event):
    if event.is_action_pressed("fire"):
        print("Fire")
```

**Lua** の例です。

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end

function on_input(self, action_id, action)
    if action_id == hash("fire") and action.pressed then
        print("Fire")
    end
end
```

`action` テーブルには、入力の種類に応じて `pressed`、`released`、`value` などの値が入ります。

入力は、最後にフォーカスを取得したリスナーから順にスタックを伝わります。たとえばメニューでクリックを処理した後、それ以降のリスナーに渡さないようにするには、`on_input()` から `true` を返してアクションを消費します。

プロキシで読み込んだワールドでは、そのワールド内のリスナーに加え、プロキシを持つオブジェクトも入力フォーカスを取得する必要があります。それまで動いていた入力スクリプトがレベル切り替え後に入力を受け取れない場合は、どちらかの取得が抜けていることがよくあります。

詳しくは[入力マニュアル](/manuals/input/)、[マウスとタッチ](/manuals/input-mouse-and-touch/)、[ゲームパッド](/manuals/input-gamepads/)を参照してください。

---

## 物理と衝突 {#physics-and-collisions}

Defold の**コリジョンオブジェクト**は、Godot の物理ボディに相当します。物理設定とコリジョン形状の**両方**を1つのコンポーネントで扱います。`game.project` では 2D 物理と 3D 物理のどちらを使うかを選べます。また、App Manifest では物理エンジンのバージョンを選択したり、物理を完全に無効にしたりできます。

Defold には4種類のコリジョンオブジェクトがあります。

| Godot | Defold の種類 | 説明 |
|---|---|---|
| `StaticBody2D` / `3D` | `Static` | 動きません。動的オブジェクトはこれに衝突すると反応します。 |
| `RigidBody2D` / `3D` | `Dynamic` | 物理エンジンが運動をシミュレーションし、衝突を解決します。 |
| `CharacterBody2D` / `3D` | `Kinematic` | 衝突に関するデータは物理エンジンが提供します。衝突への応答と解決は自分のコードで処理します。 |
| `Area2D` | `Trigger` | 進入と退出のイベントだけを通知し、物理的な応答は発生しません。 |

Defold のキネマティックオブジェクトの動作は、`move_and_slide()` を使う `CharacterBody2D` と同じではありません。Defold は接触を検出し、衝突応答メッセージでデータを渡しますが、移動と応答はスクリプトに実装します。キャラクターコントローラーを作るときは、[衝突の解決マニュアル](/manuals/physics-resolving-collisions/)を参照してください。

グループとマスクでは、番号付きの衝突レイヤーの代わりに名前を使います。衝突が検出されるには、**両方のオブジェクトがそれぞれのマスクに相手のグループを含める必要があります**。

![Defold の衝突グループとマスク](images/physics/collision_groups.png)

この画面では、`danger` という名前のゲームオブジェクトが `player` グループに、`player` という名前のゲームオブジェクトが `danger` グループに属しています。グループ名はオブジェクト ID と一致する必要はありません。このマスクの設定で、両グループ間の衝突が検出されます。

既定では、コリジョンオブジェクトは、それと同じゲームオブジェクトにあるスクリプトにメッセージを送ります。`on_message()` で `"collision_response"`、`"contact_point_response"`、`"trigger_response"` を処理してください。トリガーメッセージでは `enter` フィールドで進入と退出を区別できます。オブジェクトが接触し続けている間は衝突や接触のメッセージが繰り返し届くことがあるため、メッセージごとに新たな衝突が発生したとは限りません。

[衝突イベントリスナー](/manuals/physics-events/)で物理イベントを受け取ることもできます。リスナーを使うと、既定の物理メッセージ配信が置き換えられ、メッセージは送られなくなります。どちらの方法を使うかを決めてください。

基本的な形状から複雑な形状まで、さまざまなコリジョン形状を使えます。詳しくは[コリジョン形状マニュアル](/manuals/physics-shapes)を参照してください。

![メッシュ形状](images/physics/mesh.png)

詳しい仕組みや API は、[物理の概要](/manuals/physics/)、[コリジョンオブジェクト](/manuals/physics-objects/)、[衝突メッセージ](/manuals/physics-messages/)、[レイキャスト](/manuals/physics-ray-casts/)を参照してください。

---

## GUI {#gui}

Defold の UI は、`.gui` ファイルから作成する **GUI コンポーネント**に定義します。その中にボックス、テキスト、円形（Pie）などの GUI ノードを配置できます。専用の `.gui_script` で GUI コンポーネントを制御する仕組みは、Godot の `CanvasLayer` にスクリプトをアタッチするのと似ています。

これらのノードは GUI に属し、ゲームオブジェクトのトランスフォーム階層には入りません。既定では GUI はゲーム画面の上に重ねて描画されます。ゲームのカメラや GUI コンポーネントを持つオブジェクトが移動しても、GUI は移動しません。

`.gui_script` を割り当てると、`gui.get_node()`、`gui.set_text()` などの `gui` 関数でノードを操作できます。`gui` API を使えるのは GUI スクリプトだけで、`go` API を使えるのはゲームオブジェクトのスクリプトだけです。上のスコアの例のように、両者の間はメッセージでやり取りします。

テンプレートを使うと、ほかの GUI のノード階層を再利用できます。これは Godot でノードを再利用するのと似ています。

Defold では、Godot の Button やレイアウト用の Container のような完成済みのウィジェットの代わりに、単純なノードを組み合わせて UI を作ります。たとえばボタンを作るには、ボックスとテキストを組み合わせ、GUI スクリプトで入力を処理します。ポインターがボタンに重なっているかどうかは `gui.pick_node()` で判定できます。

Defold の GUI では、Godot の `CanvasLayer` のレイヤーに似た **Layers** を使用できます。Defold のレイヤーは番号ではなく名前で指定し、Layers での並び順が描画順序を決めます。

アンカー、ピボット、調整モード、[GUI レイアウト](/manuals/gui-layouts/)を使うと、画面の違いに合わせて UI を調整できます。役割は Godot のレイアウト用 Container に似ていますが、まったく同じではありません。

大規模または複雑な UI には、独自のレイアウトやウィジェットのコードを追加するか、[Druid](https://defold.com/assets/druid/) などのコミュニティライブラリを使えます。

詳しくは、[GUI](/manuals/gui/) と [GUI スクリプト](/manuals/gui-script/)のマニュアルを参照してください。

## アニメーション {#animation}

Defold には `AnimationPlayer` に相当する単一の機能の代わりに、用途に応じた複数のアニメーション機能があります。

- **フリップブックアニメーション**は、スプライトや GUI のボックスで一連の画像を順に再生します。
- **モデルアニメーション**は、インポートしたスケルタルアニメーションを 3D モデルで再生します。
- **プロパティアニメーション**は、`go.animate()` または `gui.animate()` で値を補間します。
- 拡張を使うと、**[Spine](https://github.com/defold/extension-spine)**、**[Rive](https://github.com/defold/extension-rive)**、**[SpriteLoop](https://github.com/Balkan-Ram-Games/spriteloop-defold)** などのアニメーション形式も利用できます。

### Tween に相当する Defold のプロパティアニメーション {#tweens-defold-property-animations}

Godot の単純な Tween は、Defold のプロパティアニメーションに置き換えられます。次の2つの例はどちらも、0.5秒かけてオブジェクトを `X = 200` まで移動します。

`Node2D` にアタッチした **GDScript** の例です。

```gdscript
func move_to_target():
    var tween = create_tween()
    tween.set_trans(Tween.TRANS_QUAD)
    tween.set_ease(Tween.EASE_OUT)
    tween.tween_property(self, "position:x", 200.0, 0.5)
```

ゲームオブジェクトのスクリプトに記述する **Lua** の例です。

```lua
local function move_to_target()
    go.animate(".", "position.x", go.PLAYBACK_ONCE_FORWARD,
        200, go.EASING_OUTQUAD, 0.5)
end
```

複数のプロパティを変更したり、サウンドを再生したり、ゲームプレイのイベントを発生させたりする一連の処理は、Lua で順序を制御します。現在、Defold にはアニメーション専用のタイムラインエディターはありません。Tools ペインの Curve Editor は、ParticleFX のパーティクルが生成されてから消えるまでのプロパティの変化を曲線で編集するためのものです。

[アニメーション](/manuals/animation/)、[プロパティアニメーション](/manuals/property-animation/)、[フリップブックアニメーション](/manuals/flipbook-animation/)、[モデルアニメーション](/manuals/model-animation/)を参照してください。概要ページには Spine と Rive の拡張へのリンクもあります。

## タイルマップ {#tilemaps}

Defold の `Tilemap` コンポーネントは、タイルを格子状に並べた**タイルソース**を使います。組み込みのタイルマップエディターでレイヤーにタイルを描き、実行時に `tilemap` API で変更できます。

Defold の組み込みタイルマップでは長方形のグリッドを使います。Godot の地形セットやオートタイルのルールは、現時点では Defold にそのまま移せません。必要な動作をコードで再現するか、[Tiled](https://doc.mapeditor.org/en/stable/manual/export-defold/?utm_source=defold&utm_medium=referral&utm_campaign=defold&utm_content=defold-website) や [TileSetter](https://www.tilesetter.org/docs/exporting?utm_source=defold&utm_medium=referral&utm_campaign=defold&utm_content=defold-website#defold) など、Defold にエクスポートできる外部のマップ編集ツールを使用できます。

詳しくは[タイルマップマニュアル](/manuals/tilemap/)を参照してください。

---

## レンダリングパイプライン {#rendering-pipeline}

Defold のレンダリングパイプラインは、独自の `.render` ファイル、`.render_script`、シェーダーを使ってスクリプトで全面的に制御できます。多くのゲームでそのまま使える既定のレンダリングパイプラインも組み込まれています。

Defold の既定のレンダースクリプトは、一般的な 2D と 3D のコンテンツに対応します。独自の `.render_script` を記述すれば、描画パスやレンダーターゲットなどの描画処理を制御できます。マテリアルのタグをレンダー述語で指定して、対象のコンポーネントをまとめて選択できます。Defold は標準で物理ベースレンダリング（PBR）にも対応しています。コミュニティが作成したレンダリングパイプラインやシェーダーも多数あります。


Defold では GLSL シェーダーを使い、頂点シェーダーとフラグメントシェーダーを別々のファイルに記述します。Godot は GLSL に似た独自のシェーディング言語とエンジン固有の組み込み機能を使うため、Godot のシェーダーや Shadertoy などのシェーダーは、Defold に合わせて書き換える必要がある場合があります。要件は[シェーダーマニュアル](/manuals/shader/)を参照してください。

Defold の**マテリアル**は、頂点プログラムとフラグメントプログラム（シェーダー）、テクスチャ、シェーダーの定数や属性を結び付けます。`builtins` フォルダーにある既定のマテリアルを出発点にできます。

既定の動作を変更する際は、[レンダリング](/manuals/render/)、[マテリアル](/manuals/material/)、[シェーダー](/manuals/shader/)を参照してください。

### 描画順序とレイヤー {#draw-order-and-layers}

Godot では整数の `z_index` で 2D の描画順序を指定しますが、これに直接対応する Defold のプロパティはありません。Defold は内部的には 3D エンジンで、実際の空間の Z 座標を使います。Z 方向に移動したときにどう奥行きが変わるかはレンダリングの設定に依存します。

Defold の**既定の**正投影では、Z 座標が -1.0 から 1.0 の範囲にあるオブジェクトだけを描画します。レイヤーを分けるには 0.1 や 0.2 といった小数値を使います。この範囲は、レンダースクリプトにメッセージを送って変更できます。既定の単純な設定では、この範囲内のゲームオブジェクトやスプライトコンポーネントは実際の Z 座標で並べ替えられ、Z 値の大きいものが小さいものの上に描画されます。そのため、Godot の `z_index` に似た感覚で使えます。ただし、透視投影のカメラに切り替えたり `.render_script` を変更したりすると、この動作も変わることがあります。

Defold の GUI ノードはワールドの Z 座標を使いません。既定では、GUI コンポーネントはワールド内のスプライトの後に別のパスで描画されるため、GUI ノードの Z 座標を変更しても描画順序は変わりません。描画順序は、Outline に表示される GUI の階層でのノード順（上から下へ）と GUI の `Layers` で決まります。レイヤーを指定すると、描画呼び出しをまとめるためにノード順よりもレイヤー順が優先されます。この点は Godot の `CanvasLayer` のレイヤーに似ています。

### カメラと座標 {#cameras-and-coordinates}

ゲームオブジェクトに `Camera` コンポーネントをアタッチし、そのオブジェクトを動かすことでカメラを移動します。一般的な 2D ビューには正投影を、3D の表示には透視投影を設定します。

既定のレンダースクリプトは、最後に有効にしたカメラを自動的に使用します。カメラが1つもない場合は 2D の正投影で描画し、カメラが1つであればそのカメラを使います。まずはこの設定で始めて、ゲームに必要な段階でレンダリングをカスタマイズできます。

カメラによって、ワールド座標が画面上のどこに対応するかは変わります。ワールド内でポインター入力を扱うときは、ポインター座標をそのままワールド座標として使わず、[Camera API](/ref/camera/) の変換関数を使ってください。GUI ノードのヒットテストには、既定では GUI 座標を使います。

投影、ズーム、座標変換については、[カメラマニュアル](/manuals/camera/)を参照してください。

---

## ゲームのエクスポート {#exporting-a-game}

Defold ではエクスポートを**バンドル**と呼びます。**Project ▸ Bundle** を選択して対象プラットフォームを指定し、バンドルのオプションを設定します。ビルドに必要なツールはエディターに揃っているので、Godot のエクスポートテンプレートに相当するものを別途インストールする必要はありません。

`game.project` には、メインコレクション、入力バインディング、表示サイズなど、プロジェクトやプラットフォームの設定が格納されています。プラットフォームごとの署名やストアの要件への対応が必要な場合もあります。ネイティブ拡張を使うプロジェクトでは、クラウドビルドサービスでカスタムエンジンをビルドするためにネットワーク接続が必要です。手動で環境を構築すれば、ローカルでビルドすることもできます。

最終的なバンドルサイズは、アセット、拡張、ビルド設定によって変わります。`Build Report` を生成すると、ゲームに何が含まれているかを確認できます。

[バンドル](/manuals/bundling/)、[プロジェクト設定](/manuals/project-settings/)、[HTML5](/manuals/html5/) を参照してください。シェーダー、ネイティブ拡張、プラットフォーム固有のサービスを使う場合は特に、早い段階でバンドルを対象プラットフォームでテストしてください。

## ライブラリと拡張 {#libraries-and-extensions}

Defold のプロジェクトには、共有のスクリプトやリソースを含む**ライブラリへの依存関係**を追加できます。`game.project` にアーカイブの URL を追加し、ライブラリを取得します。ライブラリを探すには Defold の [Asset Portal](https://defold.com/assets/) がお勧めです。エディター拡張 **Asset Store** を使えば、Godot と同じように Defold エディター内でアセットを検索し、直接ダウンロードできます。

**エディタースクリプトと UI** を使えば、コマンドの追加、作業の自動化、独自のエディター UI の作成ができます。レベル編集、リソース作成、オートタイルの配置など、よく行う開発作業を効率化できます。Godot の `EditorPlugin` や `@tool` と用途の一部が共通しますが、使用するのは Defold 独自の `editor` API とライフサイクルです。

Lua で扱える範囲を超えてエンジンを拡張するには、**ネイティブ拡張**を使います。ネイティブコードをスクリプトに公開したり、コンポーネントやプラットフォームとの連携機能を追加したりできます。GDExtension と役割は似ていますが、API とビルド手順が異なります。

[ライブラリ](/manuals/libraries/)、[エディタースクリプト](/manuals/editor-scripts/)、[ネイティブ拡張](/manuals/extensions/)を参照してください。

## ホットリロード {#hot-reload}

Defold では、実行中のゲームに変更を反映するホットリロードができます。ゲームをビルドして実行し、対応するリソースを編集、保存してから **File ▸ Hot Reload** を選択します。実機上で動作するデバッグビルドを対象にしている場合も、ホットリロードを使えます。

スクリプトを再読み込みしても `init()` は再度呼び出されません。既存のインスタンスデータは保持されるため、新しい初期値が `self` に自動で反映されることはありません。既存の状態を調整するには `on_reload(self)` を使い、最初から実行し直すには再ビルドしてください。新しいテーブルを返す Lua モジュールを再読み込みしても、ほかのスクリプトが保持する古いテーブルへの参照は置き換わりません。詳しくは[モジュールマニュアル](/manuals/modules/)を参照してください。

[ホットリロードマニュアル](/manuals/hot-reload/)も参照してください。

## ブレークポイントとデバッグ {#breakpoints-and-debugging}

エディターに組み込まれたデバッガーで、ブレークポイントの設定、ステップ実行、値の確認ができます。実行時の出力は Console で、ビルド時の問題は Build Errors で確認します。プロファイラーではフレーム時間、メモリ、描画を調べられます。バンドルサイズにどのリソースが影響しているかは、ビルドレポートで確認できます。

[ゲームロジックのデバッグ](/manuals/debugging-game-logic/)と[プロファイリング](/manuals/profiling/)を参照してください。

## ワークフローの自動化 {#automated-workflows}

Defold には、開発作業の自動化や AI を活用した開発に使えるインターフェースがいくつかあります。エディタースクリプトは繰り返し作業の自動化に使えます。OpenAPI で仕様が記述されたエディターの HTTP API を使えば、外部ツールや AI エージェントからプロジェクトを調べ、コマンドを実行し、ビルドを開始できます。エンジンの HTTP サービスと Automation Bridge 拡張は、実行時の状態の検査、入力のシミュレーション、スクリーンショットの取得に使えます。これらを組み合わせると、Codex、Claude Code、Cursor などの AI コーディングエージェントが、プロジェクトの編集、ゲームのビルド、動作テスト、問題の修正を繰り返すことができます。

詳しくは[自動化](/manuals/automation/)、[エディターの HTTP API](/manuals/editor-http-api/)、[エンジンサービス](/manuals/engine-service/)、[自動テスト](/manuals/automated-testing/)を参照してください。

---

## よくある落とし穴 {#common-pitfalls}

### コレクションをルートノードとして扱う {#treating-a-collection-as-a-root-node}

Defold のコレクションはゲームオブジェクトとその関係を記述しますが、それ自体が実行時のルートオブジェクトになるわけではありません。レベル内のオブジェクトをまとめて制御するには、専用のスクリプトを持つゲームオブジェクトを追加してください。[コレクションとワールド](#collections-and-worlds)を参照してください。

### 階層を削除する {#deleting-a-hierarchy}

Godot では、`queue_free()` でノードの子孫も削除されます。Defold の `go.delete(id)` は、再帰的な削除を指定しない限り子のゲームオブジェクトを残します。削除の例と、コレクションファクトリーで生成したオブジェクトの後片付けについては、[ファクトリー](#factories)を参照してください。

### シーンの継承を前提にする {#expecting-scene-inheritance}

Defold には Godot と同じシーン継承の仕組みがないため、派生シーンの構造を同じように自由に上書きすることはできません。プロトタイプやコレクションを再利用し、プロパティやスクリプトでインスタンスをカスタマイズできます。[コレクションとワールド](#collections-and-worlds)を参照してください。

### オブジェクトへの参照を通じて別のスクリプトを呼び出す {#calling-another-script-through-an-object-reference}

Defold のゲームオブジェクトの識別子から、別のスクリプトインスタンスの関数を自由に呼び出すことはできません。コンポーネント間ではメッセージを使い、共有したい関数は Lua モジュールにまとめてください。[メッセージとアドレス指定](#messages-and-addressing)、[Autoload と状態の共有](#autoloads-and-shared-state)を参照してください。

### インスタンスの状態をトップレベルのローカル変数に保存する {#keeping-instance-state-in-a-top-level-local}

スクリプトファイルのトップレベルにあるローカル変数は、そのファイルを使うインスタンス間で共有されます。そのため、あるインスタンスのために値を変更すると、ほかのインスタンスにも影響する可能性があります。インスタンスごとの状態は `self` に保存します。[インスタンスデータとローカルデータ](#instance-data-vs-local-data)を参照してください。

### 自動で入力を受け取れると思い込む {#assuming-input-is-enabled-automatically}

Defold のゲームオブジェクトは、コンポーネントで入力を受け取る前に入力フォーカスを取得する必要があります。プロキシで読み込んだワールドでは、そのプロキシを持つオブジェクトにも入力フォーカスが必要です。バインディング、フォーカス、入力スタックの動作については[入力](#input)を参照してください。

### キネマティックオブジェクトが自動で壁に沿って滑ると思い込む {#expecting-automatic-sliding-from-a-kinematic-collider}

Defold はキネマティックオブジェクトの接触を検出しますが、Godot の `move_and_slide()` に相当する動作は自動では行いません。移動と衝突への応答をスクリプトで実装する必要があります。[物理と衝突](#physics-and-collisions)を参照してください。

### 片方の衝突マスクだけを設定する {#configuring-only-one-collision-mask}

一方のオブジェクトだけが相手と衝突する設定になっていても、衝突は検出されません。それぞれのマスクに相手のグループを含める必要があります。[物理と衝突](#physics-and-collisions)を参照してください。

### 2D 座標をそのまま移す {#copying-2d-coordinates-unchanged}

Godot と Defold の一般的な 2D 設定では Y 軸の向きが逆なので、移動のコードをそのままコピーすると、意図した方向と反対に動くことがあります。カメラを使う場合はスクリーン座標とワールド座標も異なります。[座標](#coordinates)と[カメラと座標](#cameras-and-coordinates)を参照してください。

### ワールドの Z 座標で GUI ノードの描画順序を決めようとする {#using-world-z-to-sort-gui-nodes}

Defold では GUI ノードの Z 座標を変更しても、その描画順序は変わりません。[描画順序とレイヤー](#draw-order-and-layers)で説明したように、GUI ノードの順序とレイヤーを使ってください。

### ホットリロードでオブジェクトが再初期化されると思い込む {#expecting-hot-reload-to-restart-the-object}

スクリプトをホットリロードしても `init()` は再実行されず、既存のインスタンスの状態は以前の値を保持することがあります。状態の調整やモジュールの再読み込みについては、[ホットリロード](#hot-reload)を参照してください。

### レベルをアンロードすると共有状態も消えると思い込む {#expecting-a-level-unload-to-clear-shared-state}

Godot の Autoload の状態も、キャッシュされた Lua モジュールの状態も、レベルを切り替えた後に残ることがあります。必要に応じて共有データを明示的にリセットしてください。Autoload ノードと異なり、Lua モジュールが自動的にコールバックを受け取ることはありません。[Autoload と状態の共有](#autoloads-and-shared-state)を参照してください。

## 次のステップ {#where-to-go-from-here}

[Defold Learn Hub](https://defold.com/learn/) には、すべてのマニュアル、サンプル、チュートリアル、動画、コースなどがまとまっています。開発を始めるときにも、Defold の理解を深めたいときにも役立ちます。まずは次の資料を参照してください。

- [基本構成要素](/manuals/building-blocks/)
- [アドレス指定](/manuals/addressing/)
- [メッセージパッシング](/manuals/message-passing/)
- [Defold のサンプル](/examples/)
- [チュートリアル](/tutorials/)
- [API リファレンス](/ref/go/)

困ったときは、[Defold フォーラム](https://forum.defold.com/)や [Discord](https://defold.com/discord/) で質問してください。小さなサンプルプロジェクトを添え、再現したい Godot の動作を説明すると、ほかの人が回答しやすくなります。
