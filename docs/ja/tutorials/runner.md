---
title: エンドレスランナーのチュートリアル
brief: このチュートリアルでは、空のプロジェクトから始めて、キャラクターのアニメーション、物理衝突、アイテムの収集、得点の機能を備えたランナーゲームを完成させます。
---

# ランナーのチュートリアル {#runner-tutorial}

このチュートリアルでは、空のプロジェクトから始めて、キャラクターのアニメーション、物理衝突、アイテムの収集、得点の機能を備えたランナーゲームを完成させます。

新しいゲームエンジンを学ぶときには、覚えることがたくさんあります。そこで、最初の一歩を踏み出せるように、このチュートリアルを用意しました。エンジンとエディターの仕組みを順に説明する、かなり充実したチュートリアルです。プログラミングの基礎知識があることを前提としています。

Lua プログラミングの入門が必要な場合は、[Defold での Lua のマニュアル](/manuals/lua)を参照してください。

最初に取り組むにはこのチュートリアルは少し難しすぎると感じた場合は、さまざまな難易度のチュートリアルを揃えた[チュートリアルのページ](//www.defold.com/tutorials)を参照してください。

動画のチュートリアルを見たい場合は、[Youtube の動画版](https://www.youtube.com/playlist?list=PLXsXu5srjNlxtYPQ_YJQSxJG2AN9OVS5b)を参照してください。

ここでは、ほかの2つのチュートリアルのゲームアセットに少し変更を加えて使用します。チュートリアルはいくつかのステップに分かれており、各パートを進めるたびにゲームの完成に大きく近づきます。

最終的には、主人公のキャラクターを操作して、コインを集め、障害物を避けながらステージを走り抜けるゲームになります。主人公は一定の速度で走り、プレイヤーは1つのボタンを押すだけで（モバイルデバイスでは画面をタッチして）主人公のジャンプだけを操作します。レベルには、飛び乗るための足場と収集するコインが途切れることなく現れます。

このチュートリアルやゲーム作りの途中で行き詰まったら、遠慮なく [Defold フォーラム](//forum.defold.com)で質問してください。フォーラムでは Defold について話し合ったり、Defold チームに助けを求めたり、ほかのゲーム開発者の問題解決方法を調べたり、新しいアイデアのヒントを見つけたりできます。さっそく利用してみましょう。

::: sidenote
このチュートリアルでは、概念や特定の操作方法についての詳しい説明を、この段落のように示しています。詳しすぎると感じる場合は、読み飛ばしてください。
:::

それでは始めましょう。このチュートリアルを楽しみながら進め、Defold を使い始めるきっかけにしていただければ幸いです。

> このチュートリアルのアセットは[こちら](https://github.com/defold/sample-runner/tree/main/def-runner)からダウンロードできます。

## ステップ1 - インストールとセットアップ {#step-1-installation-and-setup}

まず、[次のファイルをダウンロードします](https://github.com/defold/sample-runner/tree/main/def-runner)。

Defold エディターをまだダウンロードしてインストールしていない場合は、ここで行います。

:[install](../shared/install.md)

エディターをインストールして起動したら、新しいプロジェクトを作成して準備します。「Empty Project」テンプレートから[新しいプロジェクト](/manuals/project-setup/#creating-a-new-project)を作成します。

::: sidenote
このチュートリアルでは、[Spine Extension](https://github.com/defold/extension-spine) が提供する Spine の機能を使います。*game.project* の依存関係のセクションに、この拡張を追加します。
:::

## エディター {#the-editor}

初めてエディターを起動すると、プロジェクトが開かれていない空の状態になります。メニューから <kbd>Open Project</kbd> を選択し、先ほど作成したプロジェクトを選びます。プロジェクトの「ブランチ」の作成も求められます。

*Assets pane* には、プロジェクトに含まれるすべてのファイルが表示されます。「main/main.collection」ファイルをダブルクリックすると、中央のエディタービューにファイルが開きます。

![エディターの概要](images/runner/1/editor2_overview.png)

エディターは、主に次の領域で構成されています。

Assets pane
: プロジェクト内のすべてのファイルを表示するビューです。ファイルの種類ごとに異なるアイコンが使われます。ファイルをダブルクリックすると、その種類に対応したエディターで開きます。読み取り専用の特別なフォルダー *builtins* はすべてのプロジェクトで共通です。既定のレンダースクリプト、フォント、各種コンポーネント（component）を描画するためのマテリアルなど、便利なものが含まれています。

Main Editor View
: 編集するファイルの種類に応じたエディターが、このビューに表示されます。最もよく使うのは、ここに表示されているシーンエディターです。開いたファイルは、それぞれ個別のタブに表示されます。

Changed Files
: 現在の Git コミットと比較して、ローカルで追加、変更、名前変更、削除されたファイルが表示されます。変更または名前変更されたテキストファイルは、1つずつ差分を表示できます。選択したローカルの変更を元に戻すこともできます。リモートリポジトリとの同期には、外部の Git クライアントまたはコマンドラインを使います。

Outline
: 編集中のファイルの内容を階層表示します。このビューからオブジェクトやコンポーネントを追加、削除、変更、選択できます。

Properties
: 選択中のオブジェクトやコンポーネントに設定されているプロパティです。

Console
: ゲームの実行中に、このビューにはゲームエンジンからの出力（ログ、エラー、デバッグ情報など）や、スクリプト内の独自の `print()`、`pprint()` によるデバッグメッセージが表示されます。アプリケーションやゲームが起動しないときは、まずコンソールを確認してください。コンソールの背後には、エラー情報を表示するタブや、パーティクルエフェクトの作成に使うカーブエディターのタブがあります。

## ゲームの実行 {#running-the-game}

「Empty」プロジェクトテンプレートは、文字どおり完全に空です。それでも、<kbd>Project ▸ Build</kbd> を選択すれば、プロジェクトをビルドしてゲームを起動できます。

![ビルド](images/runner/1/build_and_launch.png)

黒い画面だけではあまり面白くないかもしれませんが、これは実際に動作している Defold のゲームアプリケーションです。少し変更するだけで、もっと面白いものにできます。さっそく取り組みましょう。

::: sidenote
Defold エディターはファイルを対象に作業します。*Assets pane* でファイルをダブルクリックすると、適切なエディターで開き、ファイルの内容を編集できます。

ファイルの編集が終わったら、保存する必要があります。メインメニューで <kbd>File ▸ Save</kbd> を選択します。保存していない変更があるファイルは、タブのファイル名にアスタリスク「\*」が付くので見分けられます。

![未保存の変更があるファイル](images/runner/1/file_changed.png)
:::

## プロジェクトの設定 {#setting-up-the-project}

作業を始める前に、プロジェクトの設定をいくつか行います。`Assets Pane` から *game.project* アセットを開き、Display セクションまで下にスクロールします。プロジェクトの `width` と `height` を、それぞれ `1280` と `720` に設定します。

主人公をアニメーションさせるために、プロジェクトに Spine 拡張を追加する必要もあります。インストールした Defold エディターのバージョンと互換性がある Spine 拡張のバージョンを追加してください。利用できる Spine のバージョンは、次のページで確認できます。

[https://github.com/defold/extension-spine/releases](https://github.com/defold/extension-spine/releases)

使いたいリリースの zip ファイルへのリンクを右クリックします。

![右クリックしてリリースへのリンクをコピー](images/runner/extension-spine-releases.png)

リリースへのリンクを [game.project の依存関係](/manuals/libraries/#setting-up-library-dependencies)のリストに追加します。Spine 拡張を追加したら、拡張に含まれるエディター連携を有効にするため、エディターを再起動する必要があります。


## ステップ2 - 地面の作成 {#step-2-creating-the-ground}

最初の小さな一歩として、キャラクターの舞台となる場所、具体的にはスクロールする地面を作成しましょう。いくつかの手順で進めます。

1. 画像ファイル「ground01.png」と「ground02.png」（アセットパッケージのサブフォルダー「level-images」にあります）を、プロジェクト内の適切な場所にドラッグしてインポートします。たとえば、「main」フォルダー内の「images」フォルダーに配置します。
2. 地面のテクスチャをまとめる新しい *Atlas* ファイルを作成します（*Assets pane* で *main* フォルダーなどの適切なフォルダーを右クリックし、<kbd>New ▸ Atlas File</kbd> を選択します）。アトラスファイルの名前を *level.atlas* にします。

  ::: sidenote
  *アトラス（atlas）* は、複数の個別の画像を1つの大きな画像ファイルにまとめるファイルです。これにより、容量を節約し、パフォーマンスを向上させます。アトラスやほかの 2D グラフィックス機能について詳しくは、[2D グラフィックスのドキュメント](/manuals/2dgraphics)を参照してください。
  :::

3. *Outline* でアトラスのルートを右クリックし、<kbd>Add Images</kbd> を選択して、新しいアトラスに地面の画像を追加します。インポートした画像を選択し、*OK* をクリックします。これで、アトラス内の各画像を1フレームのアニメーション（静止画）として、スプライトやパーティクルエフェクトなどの表示要素に使えます。ファイルを保存します。

  ![新しいアトラスを作成](images/runner/1/new_atlas.png)

  ![アトラスに画像を追加](images/runner/1/add_images_to_atlas.png)

  ::: sidenote
  *どうして動かないのでしょう！？* Defold を使い始めた人によくあるのが、保存のし忘れです！アトラスに画像を追加したら、その画像を利用する前にファイルを保存する必要があります。
  :::

4. 地面用のコレクション（collection）ファイル *ground.collection* を作成し、7つのゲームオブジェクト（game object）を追加します（*Outline* ビューでコレクションのルートを右クリックし、<kbd>Add Game Object</kbd> を選択します）。*Properties* ビューで *Id* プロパティを変更し、オブジェクトの名前を「ground0」「ground1」「ground2」などにします。Defold は、新しいゲームオブジェクトに一意の識別子を自動的に割り当てます。

5. 各オブジェクトにスプライトコンポーネントを追加します（*Outline* ビューでゲームオブジェクトを右クリックして <kbd>Add Component</kbd> を選択し、*Sprite* を選んで *OK* をクリックします）。スプライトコンポーネントの *Image* プロパティを、先ほど作成したアトラスに設定し、スプライトの既定のアニメーションを2つの地面画像のどちらかに設定します。ゲームオブジェクトではなく、_スプライトコンポーネント_ の X 位置を190、Y 位置を40に設定します。画像の幅は380ピクセルで、その半分だけ横にずらすため、ゲームオブジェクトのピボットはスプライト画像の左端に位置します。

  ![地面のコレクションを作成](images/runner/1/ground_collection.png)

6. 使用する画像は少し大きすぎるため、各ゲームオブジェクトを60%に縮小します（X と Y のスケールを0.6にすると、地面の各パーツの幅が228ピクセルになります）。

  ![地面を拡大縮小](images/runner/1/scale_ground.png)

7. すべての _ゲームオブジェクト_ を横一列に配置します。スプライトコンポーネントではなく、_ゲームオブジェクト_ の X 位置を0、228、456、684、912、1140、1368（幅228ピクセルの倍数）に設定します。

  ::: sidenote
  スプライトコンポーネントを持ち、スケールの調整も済んだゲームオブジェクトを1つ作成してからコピーするのがおそらく最も簡単です。*Outline* ビューで選択し、<kbd>Edit ▸ Copy</kbd>、続いて <kbd>Edit ▸ Paste</kbd> を選択します。

  タイルを大きくしたり小さくしたりするには、スケールを変更するだけで済みます。ただし、その場合は地面のすべてのゲームオブジェクトの X 位置も、新しい幅の倍数に変更する必要があります。
  :::

8. ファイルを保存し、*ground.collection* を *main.collection* ファイルに追加します。まず *main.collection* ファイルをダブルクリックし、*Outline* ビューでルートオブジェクトを右クリックして <kbd>Add Collection From File</kbd> を選択します。ダイアログで *ground.collection* を選択し、*OK* をクリックします。*ground.collection* は位置0, 0, 0に配置してください。そうしないと表示位置がずれます。ファイルを保存します。

9. ゲームを起動して（<kbd>Project ▸ Build</kbd>）、すべてが正しく配置されていることを確認します。

  ![静止した地面](images/runner/1/still_ground.png)

ここまでに作成したものが何なのか、少し混乱しているかもしれません。ここで一度、Defold のすべてのプロジェクトに共通する、最も基本的な構成要素を見てみましょう。

ゲームオブジェクト
: 実行中のゲームに存在するものです。各ゲームオブジェクトは、3D 空間での位置、回転、スケールを持ちます。画面に表示されるとは限りません。ゲームオブジェクトには、グラフィックス（スプライト、タイルマップ、モデル、Spine モデル、パーティクルエフェクト）、サウンド、物理、生成に使うファクトリー（factory）などの機能を追加する _コンポーネント_ を任意の数だけ含められます。Lua の _スクリプトコンポーネント_ を追加して、ゲームオブジェクトに振る舞いを与えることもできます。ゲーム内の各ゲームオブジェクトには *id* があり、メッセージによる通信であるメッセージパッシング（message passing）でやり取りする際に必要になります。

コレクション
: コレクションそのものが実行中のゲームに存在するわけではありません。ゲームオブジェクトに静的な名前を付けると同時に、同じゲームオブジェクトの複数のインスタンスを使えるようにするためのものです。実際には、ゲームオブジェクトやほかのコレクションを格納する入れ物として使います。ゲームオブジェクトやコレクションの複雑な階層のプロトタイプ（ほかのエンジンでは「プレハブ」や「ブループリント」とも呼ばれます）のように使えます。起動時に、エンジンはメインコレクションを読み込み、その中に配置したすべてを動作させます。既定では、プロジェクトの *main* フォルダーにある *main.collection* ファイルですが、プロジェクト設定で変更できます。

今のところは、この説明で十分でしょう。さらに詳しい説明は、[基本構成要素のマニュアル](/manuals/building-blocks)にあります。後でこのマニュアルを読んで、Defold の仕組みへの理解を深めることをお勧めします。

## ステップ3 - 地面を動かす {#step-3-making-the-ground-move}

地面のパーツをすべて配置できたので、動かすのは比較的簡単です。パーツを右から左へ移動し、画面の左端の外側に達したパーツを、一番右の位置へ移します。これらのゲームオブジェクトをすべて動かすには Lua スクリプトが必要なので、作成しましょう。

1. *Assets pane* で *main* フォルダーを右クリックし、<kbd>New ▸ Script File</kbd> を選択します。新しいファイルの名前を *ground.script* にします。
2. 新しいファイルをダブルクリックして、Lua スクリプトエディターを開きます。
3. ファイルの既定の内容を削除し、次の Lua コードをコピーしてから保存します。

```lua
-- ground.script
local pieces = { "ground0", "ground1", "ground2", "ground3",
                    "ground4", "ground5", "ground6" } -- <1>

function init(self) -- <2>
    self.speed = 360  -- Speed in pixels/s
end

function update(self, dt) -- <3>
    for i, p in ipairs(pieces) do -- <4>
        local pos = go.get_position(p)
        if pos.x <= -228 then -- <5>
            pos.x = 1368 + (pos.x + 228)
        end
        pos.x = pos.x - self.speed * dt -- <6>
        go.set_position(pos, p) -- <7>
    end
end
```
1. 地面のゲームオブジェクトを順に処理できるように、それぞれの識別子を Lua テーブルに格納します。
2. `init()` 関数は、ゲームオブジェクトがゲーム内で動作し始めるときに呼び出されます。ここでは、地面の速度を格納する、そのオブジェクト固有のメンバー変数を初期化します。
3. `update()` は毎フレーム1回、通常は毎秒60回呼び出されます。`dt` には、前回の呼び出しから経過した秒数が格納されています。
4. 地面のすべてのゲームオブジェクトを順に処理します。
5. 現在の位置をローカル変数に格納し、対象のオブジェクトが左端にある場合は右端へ移動します。
6. 設定した速度に応じて、現在の X 位置を減らします。`dt` を掛けることで、フレームレートに依存しない、ピクセル/秒での速度にします。
7. 新しい速度でオブジェクトの位置を更新します。

::: sidenote
Defold は、データとゲームオブジェクトを管理する高速なエンジンコアです。ゲームに必要なロジックや振る舞いは、すべて Lua 言語で作成します。Lua は高速で軽量なプログラミング言語で、ゲームロジックの記述に適しています。書籍 [Programming in Lua](http://www.lua.org/pil/) や公式の [Lua リファレンスマニュアル](http://www.lua.org/manual/5.3/)など、言語を学ぶための優れた資料があります。

Defold は Lua に各種 API を追加し、ゲームオブジェクト間の通信をプログラムできる _メッセージパッシング_ の仕組みも提供します。仕組みの詳細は、[メッセージパッシングのマニュアル](/manuals/message-passing)を参照してください。
:::

::: sidenote
エディターの Assets Pane、Console、Outline は、それぞれ <kbd>F6</kbd>、<kbd>F7</kbd>、<kbd>F8</kbd> キーで表示と非表示を切り替えられます。
:::

スクリプトファイルを作成できたので、ゲームオブジェクト内のコンポーネントに、そのファイルへの参照を追加します。これにより、スクリプトはゲームオブジェクトのライフサイクルの一部として実行されます。*ground.collection* に新しいゲームオブジェクトを作成し、先ほど作成した Lua スクリプトファイルを参照する *Script* コンポーネントを追加します。

1. コレクションのルートを右クリックし、<kbd>Add Game Object</kbd> を選択します。オブジェクトの *id* を「controller」に設定します。
2. 「controller」オブジェクトを右クリックし、<kbd>Add Component from file</kbd> を選択して、*ground.script* ファイルを選びます。

![地面のコントローラー](images/runner/1/ground_controller.png)

ゲームを実行すると、「controller」ゲームオブジェクトが *Script* コンポーネントのスクリプトを実行し、地面が画面を滑らかにスクロールします。

## ステップ4 - 主人公の作成 {#step-4-creating-a-hero-character}

主人公は、次のコンポーネントで構成されるゲームオブジェクトになります。

*Spine Model*
: 体の各パーツを滑らかに、かつ低い処理負荷でアニメーションさせられる、紙人形のような小さな主人公を表現します。

*Collision Object*
: このコリジョンオブジェクト（collision object）は、衝突判定を行うコンポーネントです。主人公と、レベル内の走れる場所、危険なもの、収集できるものとの衝突を検出します。

*Script*
: ユーザーの入力を受け取り、それに応答して主人公をジャンプさせたり、アニメーションさせたり、衝突を処理したりします。

まず、体の各パーツの画像をインポートし、*hero.atlas* という新しいアトラスに追加します。

1. *Assets pane* で右クリックし、<kbd>New ▸ Folder</kbd> を選択して、新しいフォルダーを作成します。右クリックする前にフォルダーを選択しないようにしてください。選択していると、そのフォルダーの中に新しいフォルダーが作成されます。フォルダーの名前を「hero」にします。
2. *hero* フォルダーを右クリックし、<kbd>New ▸ Atlas File</kbd> を選択して、新しいアトラスファイルを作成します。ファイルの名前を *hero.atlas* にします。
3. *hero* フォルダーの中に、新しいサブフォルダー *images* を作成します。*hero* フォルダーを右クリックし、<kbd>New ▸ Folder</kbd> を選択します。
4. アセットパッケージの *hero-images* フォルダーから、体の各パーツの画像を、*Assets pane* で先ほど作成した *images* フォルダーへドラッグします。
5. *hero.atlas* を開き、*Outline* でルートノードを右クリックして <kbd>Add Images</kbd> を選択します。体の各パーツの画像をすべて選択し、*OK* をクリックします。
6. アトラスファイルを保存します。

![主人公のアトラス](images/runner/2/hero_atlas.png)

Spine のアニメーションデータをインポートし、それに対応する *Spine Scene* を設定する必要もあります。

1. *hero.spinejson* ファイル（アセットパッケージに含まれています）を、*Assets pane* の *hero* フォルダーへドラッグします。
2. *Spine Scene* ファイルを作成します。*hero* フォルダーを右クリックし、<kbd>New ▸ Spine Scene File</kbd> を選択します。ファイルの名前を *hero.spinescene* にします。
3. 新しいファイルをダブルクリックして、*Spine Scene* を開いて編集します。
4. *spine_json* プロパティを、インポートした JSON ファイル *hero.spinejson* に設定します。プロパティをクリックし、ファイル選択ボタン *...* をクリックすると、リソースブラウザーが開きます。
5. *atlas* プロパティが *hero.atlas* ファイルを参照するように設定します。
6. ファイルを保存します。

![主人公の Spine シーン](images/runner/2/hero_spinescene.png)

::: sidenote
*hero.spinejson* ファイルは、Spine JSON 形式でエクスポートされています。このようなファイルを作成するには、アニメーションソフトウェアの Spine が必要です。ほかのアニメーションソフトウェアを使いたい場合は、アニメーションをスプライトシートとしてエクスポートし、*Tile Source* または *Atlas* リソースから、連続した画像を切り替えるフリップブックアニメーション（flip-book animation）として使えます。詳しくは、[アニメーション](/manuals/animation)のマニュアルを参照してください。
:::

### ゲームオブジェクトの組み立て {#building-the-game-object}

これで、主人公のゲームオブジェクトを組み立てられます。

1. 新しいファイル *hero.go* を作成します（*hero* フォルダーを右クリックし、<kbd>New ▸ Game Object File</kbd> を選択します）。
2. ゲームオブジェクトファイルを開きます。
3. *Spine Model* コンポーネントを追加します（*Outline* でルートを右クリックし、<kbd>Add Component</kbd> を選択して、「Spine Model」を選びます）。
4. コンポーネントの *Spine Scene* プロパティを、先ほど作成した *hero.spinescene* ファイルに設定し、既定のアニメーションに「run_right」を選択します（アニメーションは後で適切に設定します）。
5. ファイルを保存します。

![Spine モデルのプロパティ](images/runner/2/spinemodel_properties.png)

次に、衝突が機能するように物理を追加します。

1. 主人公のゲームオブジェクトに *Collision Object* コンポーネントを追加します（*Outline* でルートを右クリックし、<kbd>Add Component</kbd> を選択して、「Collision Object」を選びます）。
2. 新しいコンポーネントを右クリックし、<kbd>Add Shape</kbd> を選択します。キャラクターの体を覆うように2つの形状を追加します。球とボックスで十分です。
3. 形状をクリックし、*Move Tool*（<kbd>Scene ▸ Move Tool</kbd>）を使って、適切な位置へ移動します。
4. *Collision Object* コンポーネントを選択し、*Type* プロパティを「Kinematic」に設定します。

::: sidenote
「Kinematic」の衝突では、衝突は検出されますが、物理エンジンによる自動的な衝突の解決やオブジェクトのシミュレーションは行われません。物理エンジンは、さまざまな種類のコリジョンオブジェクトをサポートしています。詳しくは、[物理のドキュメント](/manuals/physics)を参照してください。
:::

このコリジョンオブジェクトが、何と相互作用するかを指定することが重要です。

1. *Group* プロパティを、「hero」という新しいコリジョングループに設定します。
2. *Mask* プロパティを、このコリジョンオブジェクトが衝突を検出する相手のグループ「geometry」に設定します。「geometry」グループはまだ存在しませんが、このグループに属するコリジョンオブジェクトを後ほど追加します。

最後に、新しい *hero.script* ファイルを作成し、ゲームオブジェクトに追加します。

1. *Assets pane* で *hero* フォルダーを右クリックし、<kbd>New ▸ Script File</kbd> を選択します。新しいファイルの名前を *hero.script* にします。
2. 新しいファイルを開き、次のコードをスクリプトファイルにコピーして貼り付け、保存します（コードは、主人公のコリジョン形状を衝突相手から分離するソルバーを除けば、とても単純です。この分離処理は `handle_geometry_contact()` 関数で行います）。

![主人公のゲームオブジェクト](images/runner/2/hero_game_object.png)

::: sidenote
衝突を自分で処理するのには理由があります。キャラクターのコリジョンオブジェクトの種類を動的オブジェクトにすると、エンジンは関係する物体に対してニュートン力学に基づくシミュレーションを行います。このようなゲームでは、そのシミュレーションは最適とは言えません。さまざまな力を加えて物理エンジンと格闘する代わりに、すべての制御を自分で行います。

そのために衝突を正しく処理するには、少しだけベクトルの数学が必要です。キネマティックな衝突を解決する方法については、[物理のドキュメント](/manuals/physics-resolving-collisions/)で詳しく説明しています。
:::

```lua
-- gravity pulling the player down in pixel units/sˆ2
local gravity = -20

-- take-off speed when jumping in pixel units/s
local jump_takeoff_speed = 900

function init(self)
    -- this tells the engine to send input to on_input() in this script
    msg.post(".", "acquire_input_focus")

    -- save the starting position
    self.position = go.get_position()

    -- keep track of movement vector and if there is ground contact
    self.velocity = vmath.vector3(0, 0, 0)
    self.ground_contact = false
end

function final(self)
    -- Return input focus when the object is deleted
    msg.post(".", "release_input_focus")
end

function update(self, dt)
    local gravity = vmath.vector3(0, gravity, 0)

    if not self.ground_contact then
        -- Apply gravity if there's no ground contact
        self.velocity = self.velocity + gravity
    end

    -- apply velocity to the player character
    go.set_position(go.get_position() + self.velocity * dt)

    -- reset volatile state
    self.correction = vmath.vector3()
    self.ground_contact = false
end

local function handle_geometry_contact(self, normal, distance)
    -- project the correction vector onto the contact normal
    -- (the correction vector is the 0-vector for the first contact point)
    local proj = vmath.dot(self.correction, normal)
    -- calculate the compensation we need to make for this contact point
    local comp = (distance - proj) * normal
    -- add it to the correction vector
    self.correction = self.correction + comp
    -- apply the compensation to the player character
    go.set_position(go.get_position() + comp)
    -- check if the normal points enough up to consider the player standing on the ground
    -- (0.7 is roughly equal to 45 degrees deviation from pure vertical direction)
    if normal.y > 0.7 then
        self.ground_contact = true
    end
    -- project the velocity onto the normal
    proj = vmath.dot(self.velocity, normal)
    -- if the projection is negative, it means that some of the velocity points towards the contact point
    if proj < 0 then
        -- remove that component in that case
        self.velocity = self.velocity - proj * normal
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("contact_point_response") then
        -- check if we received a contact point message. One message for each contact point
        if message.group == hash("geometry") then
            handle_geometry_contact(self, message.normal, message.distance)
        end
    end
end

local function jump(self)
    -- only allow jump from ground
    if self.ground_contact then
        -- set take-off speed
        self.velocity.y = jump_takeoff_speed
    end
end

local function abort_jump(self)
    -- cut the jump short if we are still going up
    if self.velocity.y > 0 then
        -- scale down the upwards speed
        self.velocity.y = self.velocity.y * 0.5
    end
end

function on_input(self, action_id, action)
    if action_id == hash("jump") or action_id == hash("touch") then
        if action.pressed then
            jump(self)
        elseif action.released then
            abort_jump(self)
        end
    end
end
```

1. スクリプトを *Script* コンポーネントとして主人公のオブジェクトに追加します（*Outline* で *hero.go* のルートを右クリックし、<kbd>Add Component from File</kbd> を選択して、*hero.script* ファイルを選びます）。

試してみたい場合は、主人公を一時的にメインコレクションに追加してゲームを実行すると、ワールドをすり抜けて落ちていく様子を確認できます。

主人公を機能させるために最後に必要なのは入力です。上のスクリプトには、「jump」と「touch」（タッチスクリーン用）のアクションに応答する `on_input()` 関数がすでに含まれています。これらのアクションに入力バインディング（input binding）を追加しましょう。

1. 「input/game.input_bindings」を開きます。
2. 「KEY_SPACE」のキートリガーを追加し、アクションの名前を「jump」にします。
3. 「TOUCH_MULTI」のタッチトリガーを追加し、アクションの名前を「touch」にします（アクション名は自由に付けられますが、スクリプト内の名前と一致させる必要があります。複数のトリガーに同じアクション名を使うことはできません）。
4. ファイルを保存します。

![入力バインディング](images/runner/2/input_bindings.png)

## ステップ5 - レベルのリファクタリング {#step-5-refactoring-the-level}

衝突を含む主人公の設定ができたので、主人公が衝突する相手（つまり、走る場所）となるように、地面にも衝突を追加する必要があります。その作業の前に、少しリファクタリングを行い、レベルに関するものをすべて別のコレクションにまとめて、ファイル構成を整理しましょう。

1. 新しい *level.collection* ファイルを作成します（*Assets pane* で *main* を右クリックし、<kbd>New ▸ Collection File</kbd> を選択します）。
2. 新しいファイルを開き、*Outline* でルートを右クリックして <kbd>Add Collection from File</kbd> を選択し、*ground.collection* を選びます。
3. *level.collection* の *Outline* でルートを右クリックし、<kbd>Add Game Object File</kbd> を選択して、*hero.go* を選びます。
4. プロジェクトのルートに *level* という新しいフォルダーを作成します（*game.project* の下の余白を右クリックし、<kbd>New ▸ Folder</kbd> を選択します）。これまでに作成したレベルのアセット、つまり *level.collection*、*level.atlas*、レベルのアトラス用画像が入った「images」フォルダー、*ground.collection*、*ground.script* を、そのフォルダーに移動します。
5. *main.collection* を開き、*ground.collection* を削除します。代わりに、*ground.collection* を含む *level.collection* を追加します（右クリックして <kbd>Add Collection from File</kbd> を選択します）。コレクションは位置0, 0, 0に配置してください。

::: sidenote
すでに気付いたかもしれませんが、*Assets pane* に表示されるファイル階層と、コレクション内で構築するコンテンツの構造は独立しています。各ファイルはコレクションファイルやゲームオブジェクトファイルから参照されますが、ファイルの配置場所は自由です。

ファイルを別の場所へ移動すると、Defold はそのファイルへの参照を自動的に更新して支援します（リファクタリング）。ゲームのような複雑なソフトウェアを作る際には、規模の拡大や内容の変化に応じてプロジェクトの構造を変更できることが大いに役立ちます。Defold はその変更を勧め、作業が円滑に進むようにしています。ためらわずにファイルを移動してください！
:::

レベルのコレクションに、スクリプトコンポーネントを持つコントローラー用ゲームオブジェクトも追加します。

1. 新しいスクリプトファイルを作成します。*Assets pane* で *level* フォルダーを右クリックし、<kbd>New ▸ Script File</kbd> を選択します。ファイルの名前を *controller.script* にします。
2. スクリプトファイルを開き、次のコードをコピーして、ファイルを保存します。

    ```lua
    -- controller.script
    go.property("speed", 360) -- <1>

    function init(self)
        msg.post("ground/controller#ground", "set_speed", { speed = self.speed })
    end
    ```
    1. これはスクリプトプロパティです。ここでは既定値を設定していますが、配置したスクリプトの各インスタンスで、エディターのプロパティビューから直接この値を上書きできます。

3. *level.collection* ファイルを開きます。
4. *Outline* でルートを右クリックし、<kbd>Add Game Object</kbd> を選択します。
5. *Id* を「controller」に設定します。
6. *Outline* で「controller」ゲームオブジェクトを右クリックし、<kbd>Add Component from File</kbd> を選択して、*level* フォルダー内の *controller.script* ファイルを選びます。
7. ファイルを保存します。

![スクリプトプロパティ](images/runner/2/script_property.png)

::: sidenote
「controller」ゲームオブジェクトは、独立したファイルとしては存在せず、レベルのコレクション内にその場で追加（in-place）されています。つまり、ゲームオブジェクトのインスタンスは、その場で定義したデータから作成されます。このように用途が1つのゲームオブジェクトには、それで問題ありません。あるゲームオブジェクトのインスタンスが複数必要で、各インスタンスの作成に使うプロトタイプ/テンプレートを変更できるようにしたい場合は、ゲームオブジェクトファイルを作成し、そのファイルからゲームオブジェクトをコレクションに追加します。これにより、ファイルをプロトタイプ/テンプレートとして参照するゲームオブジェクトが作成されます。

この「controller」ゲームオブジェクトの目的は、実行中のレベルに関するすべてを制御することです。このスクリプトは、後ほど主人公が触れる足場やコインの生成を担当しますが、今のところはレベルの速度を設定するだけです。
:::

レベルのコントローラースクリプトの `init()` 関数では、地面のコントローラーオブジェクトのスクリプトコンポーネントに、その識別子を宛先としてメッセージを送信します。

```lua
msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
```

コントローラーのゲームオブジェクトは「ground」コレクション内にあるため、識別子は `"ground/controller"` になります。コンポーネントの識別子 `"controller"` を、オブジェクトの識別子とコンポーネントの識別子を区切るハッシュ記号 `"#"` の後に追加します。地面のスクリプトには、まだ `set_speed` メッセージに応答するコードがありません。*ground.script* に `on_message()` 関数を追加し、そのためのロジックを記述する必要があります。

1. *ground.script* を開きます。
2. 次のコードを追加し、ファイルを保存します。

```lua
-- ground.script
function on_message(self, message_id, message, sender)
    if message_id == hash("set_speed") then -- <1>
        self.speed = message.speed -- <2>
    end
end
```
1. すべてのメッセージは、送信時に内部でハッシュ化されます。比較にはハッシュ化した値を使う必要があります。
2. メッセージデータは、メッセージと一緒に送信するデータを含む Lua テーブルです。

![地面のコードを追加](images/runner/insert_ground_code.png)

## ステップ6 - 地面の物理と足場 {#step-6-ground-physics-and-platforms}

ここで、地面に物理衝突を追加します。

1. *ground.collection* ファイルを開きます。
2. 適切なゲームオブジェクトに、新しい *Collision Object* コンポーネントを追加します。地面のスクリプトは衝突に応答しないため（そのロジックはすべて主人公のスクリプトにあります）、_静止している_ ゲームオブジェクトであれば、どれに追加してもかまいません（地面のタイルオブジェクトは動いているので避けてください）。「controller」ゲームオブジェクトがよい候補ですが、別のオブジェクトを作成してもかまいません。ゲームオブジェクトを右クリックし、<kbd>Add Component</kbd> を選択して、*Collision Object* を選びます。
3. *Collision Object* コンポーネントを右クリックし、<kbd>Add Shape</kbd>、続いて *Box* を選択して、ボックス形状を追加します。
4. *Move Tool* と *Scale Tool*（<kbd>Scene ▸ Move Tool</kbd> と <kbd>Scene ▸ Scale Tool</kbd>）を使って、ボックスが地面のすべてのタイルを覆うようにします。
5. 地面の物理形状は動かないため、コリジョンオブジェクトの *Type* プロパティを「Static」に設定します。
6. コリジョンオブジェクトの *Group* プロパティを「geometry」、*Mask* を「hero」に設定します。これで、主人公のコリジョンオブジェクトと、このコリジョンオブジェクトとの衝突が検出されます。
7. ファイルを保存します。

![地面の衝突判定](images/runner/2/ground_collision.png)

ここでゲームを実行してみましょう（<kbd>Project ▸ Build</kbd>）。主人公が地面の上を走り、<kbd>Space</kbd> キーでジャンプできるはずです。モバイルデバイスでゲームを実行する場合は、画面をタップするとジャンプできます。

ゲームワールドをもう少し面白くするため、飛び乗れる足場を追加しましょう。

1. アセットパッケージの画像ファイル *rock_planks.png* を、*level/images* サブフォルダーへドラッグします。
2. *level.atlas* を開き、新しい画像をアトラスに追加します（*Outline* でルートを右クリックし、<kbd>Add Images</kbd> を選択します）。
3. ファイルを保存します。
4. *level* フォルダーに、*platform.go* という新しい *Game Object* ファイルを作成します（*Assets pane* で *level* を右クリックし、<kbd>New ▸ Game Object File</kbd> を選択します）。
5. ゲームオブジェクトに *Sprite* コンポーネントを追加します（*Outline* ビューでルートを右クリックし、<kbd>Add Component</kbd> を選択して、*Sprite* を選びます）。
6. *Image* プロパティが *level.atlas* ファイルを参照するように設定し、*Default Animation* を「rock_planks」に設定します。扱いやすいように、レベルのオブジェクトは「level/objects」サブフォルダーにまとめます。
7. 足場のゲームオブジェクトに *Collision Object* コンポーネントを追加します（*Outline* ビューでルートを右クリックし、<kbd>Add Component</kbd> を選択します）。
8. コンポーネントの *Type* を「Kinematic」、*Group* を「geometry」、*Mask* を「hero」に設定してください。
9. *Collision Object* コンポーネントに *Box Shape* を追加します（*Outline* でコンポーネントを右クリックし、<kbd>Add Shape</kbd> を選択して、*Box* を選びます）。
10. *Move Tool* と *Scale Tool*（<kbd>Scene ▸ Move Tool</kbd> と <kbd>Scene ▸ Scale Tool</kbd>）を使って、*Collision Object* コンポーネントの形状が足場を覆うようにします。
11. *Script* ファイル *platform.script* を作成します（*Assets pane* で右クリックし、<kbd>New ▸ Script File</kbd> を選択します）。次のコードをファイルに記述し、保存します。

    ```lua
    -- platform.script
    function init(self)
        self.speed = 540      -- Default speed in pixels/s
    end

    function update(self, dt)
        local pos = go.get_position()
        if pos.x < -500 then
            go.delete() -- <1>
        end
        pos.x = pos.x - self.speed * dt
        go.set_position(pos)
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("set_speed") then
            self.speed = message.speed
        end
    end
    ```
    1. 足場が画面の右端の外へ移動したら、その足場を削除します。

12. *platform.go* を開き、新しいスクリプトをコンポーネントとして追加します（*Outline* ビューでルートを右クリックし、<kbd>Add Component From File</kbd> を選択して、*platform.script* を選びます）。
13. *platform.go* を新しいファイルにコピーし（*Assets pane* でファイルを右クリックして <kbd>Copy</kbd> を選択し、再び右クリックして <kbd>Paste</kbd> を選択します）、新しいファイルの名前を *platform_long.go* にします。
14. *platform_long.go* を開き、2つ目の *Sprite* コンポーネントを追加します（*Outline* ビューでルートを右クリックし、<kbd>Add Component</kbd> を選択します）。既存の *Sprite* をコピーしてもかまいません。
15. *Move Tool*（<kbd>Scene ▸ Move Tool</kbd>）を使って、*Sprite* コンポーネントを横に並べて配置します。
16. *Move Tool* と *Scale Tool* を使って、*Collision Object* コンポーネントの形状が両方の足場を覆うようにします。

![足場](images/runner/2/platform_long.png)

::: sidenote
*platform.go* と *platform_long.go* の *Script* コンポーネントは、同じスクリプトファイルを参照しています。スクリプトファイルへの変更が、通常の足場と長い足場の両方の動作に反映されるため、便利です。
:::

## 足場の生成 {#spawning-platforms}

このゲームは、単純なエンドレスランナーを目指しています。そのため、足場のゲームオブジェクトをエディターでコレクション内に配置しておくことはできません。代わりに、動的に生成する必要があります。

1. *level.collection* を開きます。
2. 「controller」ゲームオブジェクトに、2つの *Factory* コンポーネントを追加します（右クリックして <kbd>Add Component</kbd> を選択し、*Factory* を選びます）。
3. コンポーネントの *Id* プロパティを、それぞれ「platform_factory」と「platform_long_factory」に設定します。
4. 「platform_factory」の *Prototype* プロパティを、*/level/objects/platform.go* ファイルに設定します。
5. 「platform_long_factory」の *Prototype* プロパティを、*/level/objects/platform_long.go* ファイルに設定します。
6. ファイルを保存します。
7. レベルを管理する *controller.script* ファイルを開きます。
8. 次の内容になるようにスクリプトを変更し、ファイルを保存します。

```lua
-- controller.script
go.property("speed", 360)

local grid = 460
local platform_heights = { 100, 200, 350 } -- <1>

function init(self)
    msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
    self.gridw = 0
end

function update(self, dt) -- <2>
    self.gridw = self.gridw + self.speed * dt

    if self.gridw >= grid then
        self.gridw = 0

        -- Maybe spawn a platform at random height
        if math.random() > 0.2 then
            local h = platform_heights[math.random(#platform_heights)]
            local f = "#platform_factory"
            if math.random() > 0.5 then
                f = "#platform_long_factory"
            end

            local p = factory.create(f, vmath.vector3(1600, h, 0), nil, {}, vmath.vector3(0.6, 0.6, 1))
            msg.post(p, "set_speed", { speed = self.speed })
        end
    end
end
```
1. 足場を生成する Y 位置として、あらかじめ定義した値です。
2. `update()` 関数は毎フレーム1回呼び出されます。これを使い、一定の間隔（重なりを避けるため）と高さで、通常の足場または長い足場を生成するかどうかを決めます。さまざまな生成アルゴリズムを試して、異なるゲームプレイを作るのは簡単です。

ゲームを実行します（<kbd>Project ▸ Build</kbd>）。

おお、（ほとんど）遊べるゲームになってきました……。

![ゲームの実行](images/runner/2/run_game.png)

## ステップ7 - アニメーションと死亡 {#step-7-animation-and-death}

まず、主人公に動きの変化を与えましょう。今の主人公は走る動作を繰り返すだけで、ジャンプなどにうまく反応できません。アセットパッケージから追加した Spine ファイルには、実はそうした動作に使うアニメーションが含まれています。

1. *hero.script* ファイルを開き、既存の `update()` 関数の _前_ に、次の関数を追加します。

```lua
    -- hero.script
    local function play_animation(self, anim)
        -- only play animations which are not already playing
        if self.anim ~= anim then
            -- tell the spine model to play the animation
            local anim_props = { blend_duration = 0.15 }
            spine.play_anim("#spinemodel", anim, go.PLAYBACK_LOOP_FORWARD, anim_props)
            -- remember which animation is playing
            self.anim = anim
        end
    end

    local function update_animation(self)
        -- make sure the right animation is playing
        if self.ground_contact then
            play_animation(self, hash("run"))
        else
            play_animation(self, hash("jump"))

        end
    end
```

2. `update()` 関数を探し、`update_animation` の呼び出しを追加します。

```lua
    ...
    -- apply it to the player character
    go.set_position(go.get_position() + self.velocity * dt)

    update_animation(self)
    ...
  ```

![主人公のコードを挿入](images/runner/insert_hero_code.png)

::: sidenote
Lua のローカル変数には「レキシカルスコープ」があり、`local` 関数を配置する順序が影響します。`update()` 関数はローカル関数 `update_animation()` と `play_animation()` を呼び出すため、それらを呼び出す前に、ランタイムがローカル関数の定義を読み込んでいる必要があります。そのため、これらの関数を `update()` の前に配置しなければなりません。関数の順序を入れ替えるとエラーになります。これは `local` 変数にだけ当てはまります。Lua のスコープの規則とローカル関数について詳しくは、http://www.lua.org/pil/6.2.html を参照してください。
:::

主人公にジャンプと落下のアニメーションを追加する作業は、これだけです。ゲームを実行すると、操作感がかなりよくなったことが分かります。ただし、足場に押されて主人公が画面の外へ出てしまうことにも気付くかもしれません。これは衝突処理の副作用ですが、解決方法は簡単です。少し過激にして、足場の端を危険な場所にしましょう！

1. アセットパッケージの *spikes.png* を、*Assets pane* の「level/images」フォルダーへドラッグします。
2. *level.atlas* を開き、画像を追加します（右クリックして <kbd>Add Images</kbd> を選択します）。
3. *platform.go* を開き、*Sprite* コンポーネントをいくつか追加します。*Image* を *level.atlas*、*Default Animation* を「spikes」に設定します。
4. *Move Tool* と *Rotate Tool* を使って、足場の端に沿ってトゲを配置します。
5. トゲが足場の後ろに描画されるように、トゲのスプライトの *Z* 位置を-0.1に設定します。
6. 足場に新しい *Collision Object* コンポーネントを追加します（*Outline* でルートを右クリックし、<kbd>Add Component</kbd> を選択します）。*Group* プロパティを「danger」に設定します。*Mask* も「hero」に設定します。
7. *Collision Object* にボックス形状を追加します（右クリックして <kbd>Add Shape</kbd> を選択します）。*Move Tool*（<kbd>Scene ▸ Move Tool</kbd>）と *Scale Tool* を使い、主人公が足場の側面や下側からぶつかったときに「danger」オブジェクトと衝突するように形状を配置します。
8. ファイルを保存します。

    ![足場のトゲ](images/runner/3/danger_edges.png)

9. *hero.go* を開き、*Collision Object* を選択して、*Mask* プロパティに「danger」を追加します。ファイルを保存します。

    ![主人公の衝突判定](images/runner/3/hero_collision.png)

10. *hero.script* を開き、主人公が「danger」の端に衝突したときに反応するように、`on_message()` 関数を変更します。

    ```lua
    -- hero.script
    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then
            self.velocity = vmath.vector3(0, 0, 0)
            self.correction = vmath.vector3()
            self.ground_contact = false
            self.anim = nil
            go.set(".", "euler.z", 0)
            go.set_position(self.position)
            msg.post("#collisionobject", "enable")

        elseif message_id == hash("contact_point_response") then
            -- check if we received a contact point message
            if message.group == hash("danger") then
                -- Die and restart
                play_animation(self, hash("death"))
                msg.post("#collisionobject", "disable")
                -- <1>
                go.animate(".", "euler.z", go.PLAYBACK_ONCE_FORWARD, 160, go.EASING_LINEAR, 0.7)
                go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
                    function()
                        msg.post("#", "reset")
                    end)
            elseif message.group == hash("geometry") then
                handle_geometry_contact(self, message.normal, message.distance)
            end
        end
    end
    ```
    1. 主人公が死亡するときに、回転と落下の動きを加えます。この部分には、まだ大きく改善できる余地があります！

11. オブジェクトを初期化するために「reset」メッセージを送るよう、`init()` 関数を変更し、ファイルを保存します。

    ```lua
    -- hero.script
    function init(self)
        -- this lets us handle input in this script
        msg.post(".", "acquire_input_focus")
        -- save position
        self.position = go.get_position()
        msg.post("#", "reset")
    end
    ```

## ステップ8 - レベルのリセット {#step-8-resetting-the-level}

ここでゲームを試すと、リセットの仕組みがうまく動かないことがすぐに分かります。主人公自体は正しくリセットされますが、リセット直後に足場の端へ落ち、また死亡してしまう状況が起こりやすくなっています。実現したいのは、死亡時にレベル全体を正しくリセットすることです。レベルは生成された一連の足場で構成されているだけなので、生成したすべての足場を管理し、リセット時に削除すれば済みます。

1. *controller.script* ファイルを開き、生成したすべての足場の識別子を格納するようにコードを編集します。

    ```lua
    -- controller.script
    go.property("speed", 360)

    local grid = 460
    local platform_heights = { 100, 200, 350 }

    function init(self)
        msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
        self.gridw = 0
        self.spawns = {} -- <1>
    end

    function update(self, dt)
        self.gridw = self.gridw + self.speed * dt

        if self.gridw >= grid then
            self.gridw = 0

            -- Maybe spawn a platform at random height
            if math.random() > 0.2 then
                local h = platform_heights[math.random(#platform_heights)]
                local f = "#platform_factory"
                if math.random() > 0.5 then
                    f = "#platform_long_factory"
                end

                local p = factory.create(f, vmath.vector3(1600, h, 0), nil, {}, vmath.vector3(0.6, 0.6, 1))
                msg.post(p, "set_speed", { speed = self.speed })
                table.insert(self.spawns, p) -- <1>
            end
        end
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then -- <2>
            -- Tell the hero to reset.
            msg.post("hero#hero", "reset")
            -- Delete all platforms
            for i,p in ipairs(self.spawns) do
                go.delete(p)
            end
            self.spawns = {}
        elseif message_id == hash("delete_spawn") then -- <3>
            for i,p in ipairs(self.spawns) do
                if p == message.id then
                    table.remove(self.spawns, i)
                    go.delete(p)
                end
            end
        end
    end
    ```
    1. 生成したすべての足場を格納するために、テーブルを使います。
    2. 「reset」メッセージで、テーブルに格納されているすべての足場を削除します。
    3. 「delete_spawn」メッセージで、特定の足場を削除し、テーブルからも取り除きます。

2. ファイルを保存します。
3. *platform.script* を開き、左端に達した足場をそのまま削除する代わりに、レベルのコントローラーに足場の削除を依頼するメッセージを送るように変更します。

    ```lua
    -- platform.script
    ...
    if pos.x < -500 then
        msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
    end
    ...
    ```

    ![足場のコードを挿入](images/runner/insert_platform_code.png)

4. ファイルを保存します。
5. *hero.script* を開きます。最後に必要なのは、レベルにリセットを指示することです。主人公にリセットを求めるメッセージは、レベルのコントローラースクリプトへ移しました。このようにリセットの制御を一か所にまとめると、たとえば、より長い時間をかける死亡シーケンスを導入しやすくなるため、理にかなっています。

```lua
-- hero.script
...
go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
    function()
        msg.post("controller#controller", "reset")
    end)
...
```

![主人公のコードを挿入](images/runner/insert_hero_code_2.png)

これで、再開と死亡を繰り返す基本的なループができました！

次は、生き残る目的になるもの、コインです！

## ステップ9 - 収集するコイン {#step-9-coins-to-collect}

プレイヤーが収集できるコインをレベルに配置します。まず考えるのは、レベルにどう配置するかです。たとえば、足場の生成アルゴリズムに何らかの形で合わせた生成方法を作れます。ただし、ここでは最終的にもっと簡単な方法を選び、足場自体からコインを生成することにしました。

1. アセットパッケージの *coin.png* 画像を、*Assets pane* の「level/images」へドラッグします。
2. *level.atlas* を開き、画像を追加します（右クリックして <kbd>Add Images</kbd> を選択します）。
3. *level* フォルダーに、*coin.go* という名前の *Game Object* ファイルを作成します（*Assets pane* で *level* を右クリックし、<kbd>New ▸ Game Object File</kbd> を選択します）。
4. *coin.go* を開き、*Sprite* コンポーネントを追加します（*Outline* で右クリックし、<kbd>Add Component</kbd> を選択します）。*Image* を *level.atlas*、*Default Animation* を「coin」に設定します。
5. *Collision Object* を追加し（*Outline* で右クリックし、<kbd>Add Component</kbd> を選択します）、
画像を覆う *Sphere* 形状を追加します（コンポーネントを右クリックし、<kbd>Add Shape</kbd> を選択します）。
6. *Move Tool*（<kbd>Scene ▸ Move Tool</kbd>）と *Scale Tool* を使って、球がコインの画像を覆うようにします。
7. コリジョンオブジェクトの *Type* を「Kinematic」、*Group* を「pickup」、*Mask* を「hero」に設定します。
8. *hero.go* を開き、*Collision Object* コンポーネントの *Mask* プロパティに「pickup」を追加して、ファイルを保存します。
9. 新しいスクリプトファイル *coin.script* を作成します（*Assets pane* で *level* を右クリックし、<kbd>New ▸ Script File</kbd> を選択します）。テンプレートのコードを、次の内容に置き換えます。

    ```lua
    -- coin.script
    function init(self)
        self.collected = false
    end

    function on_message(self, message_id, message, sender)
        if self.collected == false and message_id == hash("collision_response") then
            self.collected = true
            msg.post("#sprite", "disable")
        elseif message_id == hash("start_animation") then
            pos = go.get_position()
            go.animate(go.get_id(), "position.y", go.PLAYBACK_LOOP_PINGPONG, pos.y + 24, go.EASING_INOUTSINE, 0.75, message.delay)
        end
    end
    ```

10. スクリプトファイルを *Script* コンポーネントとして、コインのオブジェクトに追加します（*Outline* でルートを右クリックし、<kbd>Add Component from File</kbd> を選択します）。

    ![コインのゲームオブジェクト](images/runner/3/coin.png)

足場のオブジェクトからコインを生成するため、*platform.go* と *platform_long.go* にコイン用のファクトリーを配置します。

1. *platform.go* を開き、*Factory* コンポーネントを追加します（*Outline* で右クリックし、<kbd>Add Component</kbd> を選択します）。
2. *Factory* の *Id* を「coin_factory」に設定し、*Prototype* を *coin.go* ファイルに設定します。
3. *platform_long.go* を開き、同じ *Factory* コンポーネントを作成します。
4. 2つのファイルを保存します。

![コインのファクトリー](images/runner/3/coin_factory.png)

次に、コインを生成、削除するように *platform.script* を変更します。

```lua
-- platform.script
function init(self)
    self.speed = 540     -- Default speed in pixels/s
    self.coins = {}
end

function final(self)
    for i,p in ipairs(self.coins) do
        go.delete(p)
    end
end

function update(self, dt)
    local pos = go.get_position()
    if pos.x < -500 then
        msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
    end
    pos.x = pos.x - self.speed * dt
    go.set_position(pos)
end

function create_coins(self, params)
    local spacing = 56
    local pos = go.get_position()
    local x = pos.x - params.coins * (spacing*0.5) - 24
    for i = 1, params.coins do
        local coin = factory.create("#coin_factory", vmath.vector3(x + i * spacing , pos.y + 64, 1))
        msg.post(coin, "set_parent", { parent_id = go.get_id() }) -- <1>
        msg.post(coin, "start_animation", { delay = i/10 }) -- <2>
        table.insert(self.coins, coin)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("set_speed") then
        self.speed = message.speed
    elseif message_id == hash("create_coins") then
        create_coins(self, message)
    end
end
```
1. 生成したコインの親を足場に設定することで、コインが足場と一緒に移動します。
2. このアニメーションによって、コインは親となった足場に対して上下に弾むように動きます。

::: sidenote
親子関係による変更は、あくまでも _シーングラフ（scene graph）_ に対するものです。子は、親と一緒に変換（移動、拡大縮小、回転）されます。ゲームオブジェクト間に別の「所有」関係が必要な場合は、コードでその関係を明示的に管理する必要があります。
:::

このチュートリアルの最後の手順として、*controller.script* に数行追加します。

```lua
-- controller.script
...
local platform_heights = { 100, 200, 350 }
local coins = 3 -- <1>
...
```
1. 通常の足場に生成するコインの数です。

```lua
-- controller.script
...
local coins = coins
if math.random() > 0.5 then
    f = "#platform_long_factory"
    coins = coins * 2 -- Twice the number of coins on long platforms
end
...
```

```lua
-- controller.script
...
msg.post(p, "set_speed", { speed = self.speed })
msg.post(p, "create_coins", { coins = coins })
table.insert(self.spawns, p)
...
```

![コントローラーのコードを挿入](images/runner/insert_controller_code.png)

これで、単純ですが機能するゲームができました！ここまで進められたら、自分で次の機能を追加してみたくなるかもしれません。

1. 得点と残りライフのカウンター
2. アイテムの収集時と死亡時のパーティクルエフェクト
3. 見栄えのよい背景画像

> 完成版のプロジェクトは[こちら](images/runner/sample-runner.zip)からダウンロードできます。

入門チュートリアルはこれで終わりです。ここからは、Defold をさらに使ってみましょう。学習を支援する[マニュアルとチュートリアル](//www.defold.com/learn)を多数用意しています。行き詰まったら、[フォーラム](//forum.defold.com)へどうぞ。

Defold を楽しんでください！
