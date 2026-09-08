---
title: Defold エンジンとエディターの FAQ
brief: Defold ゲームエンジン、エディター、プラットフォームに関するよくある質問です。
---

# よくある質問 {#frequently-asked-questions}

## 一般的な質問 {#general-questions}

#### Q: Defold は本当に無料ですか？ {#q-is-defold-really-free}

A: はい、Defold のエンジンとエディターは、すべての機能を完全に無料で利用できます。隠れた費用、手数料、ロイヤリティはありません。純粋に無料です。


#### Q: Defold Foundation が Defold を無料で提供するのはなぜですか？ {#q-why-on-earth-would-the-defold-foundation-give-defold-away}

A: [Defold Foundation](/foundation) の目的の1つは、世界中の開発者が Defold ソフトウェアを利用でき、ソースコードを無料で入手できるようにすることです。


#### Q: Defold はいつまでサポートされますか？ {#q-how-long-will-you-support-defold}

A: Defold の支援に強く取り組んでいます。[Defold Foundation](/foundation) は、今後長年にわたり Defold の責任ある所有者として存続することが保証されるように設立されています。なくなることはありません。


#### Q: Defold はプロの開発業務でも信頼して使えますか？ {#q-can-i-trust-defold-for-professional-development}

A: はい。Defold を使うプロのゲーム開発者やゲームスタジオは増え続けています。Defold で制作されたゲームの例は、[ゲームショーケース](/showcase) をご覧ください。


#### Q: どのようなユーザー追跡を行っていますか？ {#q-what-kind-of-user-tracking-are-you-doing}

A: サービスと製品を改善するため、ウェブサイトと Defold エディターから匿名の利用データを記録しています。制作したゲームでは、ユーザー追跡は行われません（自分で分析サービスを追加した場合を除きます）。詳しくは、[プライバシーポリシー](/privacy-policy) をご覧ください。


#### Q: Defold を作ったのは誰ですか？ {#q-who-made-defold}

A: Defold は Ragnar Svensson と Christian Murray によって作られました。2人は2009年にエンジン、エディター、サーバーの開発を始めました。2013年に King と Defold が提携し、2014年に King が Defold を買収しました。詳しい経緯は [こちら](/about) をご覧ください。


## ゲーム開発に関する質問 {#game-development-questions}

#### Q: Defold で 3D ゲームを作れますか？ {#q-can-i-do-3d-games-in-defold}

A: はい！エンジンは本格的な 3D エンジンです。ただし、ツールセットは 2D 向けに作られているため、多くの作業を自分で行う必要があります。3D サポートの強化を予定しています。


## プログラミング言語に関する質問 {#programming-language-questions}

#### Q: Defold ではどのプログラミング言語を使いますか？ {#q-what-programming-language-do-i-work-with-in-defold}

A: Defold プロジェクトのゲームロジックは、主に Lua 言語で記述します（具体的には Lua 5.1/LuaJIT です。詳しくは [Lua マニュアル](/manuals/lua) を参照してください）。Lua は軽量な動的言語で、高速かつ非常に強力です。Defold は、Lua コードを出力するトランスパイラーをサポートしています。トランスパイラー拡張をインストールすると、[Teal](https://github.com/defold/extension-teal) などの別の言語を使って、静的な検査を受ける Lua コードを記述できます。また、ネイティブコード（プラットフォームに応じて C/C++、Objective-C、Java、JavaScript）を使って、[Defold エンジンを拡張して新しい機能を追加する](/manuals/extensions/) こともできます。[カスタムマテリアル（material）](/manuals/material/) を作成する場合は、OpenGL ES SL シェーダー言語を使って頂点シェーダーとフラグメントシェーダーを記述します。


#### Q: C++ でゲームロジックを記述できますか？ {#q-can-i-use-c-to-write-game-logic}

A: Defold の C++ サポートは、主にサードパーティーの SDK やプラットフォーム固有の API と連携するネイティブ拡張（native extension）を記述するためのものです。[dmSDK](https://defold.com/ref/stable/dmGameObject/)（ネイティブ拡張で使用する Defold の C++ API）には段階的に機能を追加し、開発者が希望すればゲームロジック全体を C++ で記述できるようにする予定です。ゲームロジックに使う主な言語は引き続き Lua ですが、C++ API の拡充により、C++ でもゲームロジックを記述できるようになります。C++ API を拡充する作業は、主に既存の非公開ヘッダーファイルを公開部分に移し、公開利用に向けて API を整理することです。


#### Q: Defold で TypeScript を使えますか？ {#q-can-i-use-typescript-with-defold}

A: TypeScript は公式にはサポートされていません。コミュニティが、TypeScript を記述して VSCode から直接 Lua にトランスパイルするためのツールキット [ts-defold](https://ts-defold.dev/) を保守しています。


#### Q: Defold で Haxe を使えますか？ {#q-can-i-use-haxe-with-defold}

A: Haxe は公式にはサポートされていません。コミュニティが、Haxe を記述して Lua にトランスパイルするための [hxdefold](https://github.com/hxdefold/hxdefold) を保守しています。


#### Q: Defold で C# を使えますか？ {#q-can-i-use-c-with-defold}

A: Defold Foundation は C# サポートを追加し、ライブラリへの依存関係として利用できるようにしました。C# は広く採用されているプログラミング言語であり、C# に多くの投資をしてきたスタジオや開発者の Defold への移行に役立ちます。


#### Q: C# サポートの追加が Defold に悪影響を与えないか気になります。心配する必要はありますか？ {#q-i-am-concerned-that-adding-c-support-will-have-a-negative-impact-on-defold-should-i-be-worried}

Defold は、主なスクリプト言語としての Lua から離れることはありません。C# サポートは、拡張機能のための新しい言語として追加されます。プロジェクトで C# 拡張を使うことを選ばない限り、エンジンに影響はありません。

C# サポートには代償（実行ファイルのサイズ、実行時のパフォーマンスなど）が伴いますが、採用するかどうかは個々の開発者やスタジオが判断することです。

C# 自体については、拡張システムがすでに多くの言語（C/C++/Java/Objective-C/Zig）をサポートしているため、比較的小さな変更です。C# バインディングを生成することで、SDK 間の同期を保ちます。これにより、最小限の作業でバインディングを最新の状態に保てます。

Defold Foundation は以前、Defold への C# サポートの追加に反対していましたが、いくつかの理由から考えを変えました。

* スタジオや開発者から、C# サポートへの要望が引き続き寄せられています。
* C# サポートの対象を拡張機能のみに絞りました（つまり、必要な作業量が少なくなりました）。
* コアエンジンには影響しません。
* C# API を生成すれば、最小限の作業で同期を保てます。
* C# サポートは NativeAOT を使う DotNet 9 を基盤とし、既存のビルドパイプラインでリンクできる静的ライブラリを生成します（ほかの Defold 拡張と同様です）。


## プラットフォームに関する質問 {#platform-questions}

#### Q: Defold はどのプラットフォームで動作しますか？ {#q-what-platforms-does-defold-run-on}

A: エディターとツール、およびエンジンのランタイムでは、次のプラットフォームをサポートしています。

  | システム             | バージョン            | アーキテクチャ      | サポート対象          |
  | ------------------ | ------------------ | ------------------ | ------------------ |
  | macOS              | 11 Big Sur         | `x86-64`, `arm-64` | エディターとエンジン  |
  | Windows            | Vista              | `x86-32`, `x86-64` | エディターとエンジン  |
  | Ubuntu (1)         | 22.04 LTS          | `x86-64`           | エディター             |
  | Linux (2)          | 任意                | `x86-64`, `arm-64` | エンジン             |
  | iOS                | 15.0               | `arm-64`  `x86_64` | エンジン             |
  | Android            | 5.0 (API レベル 21) | `arm-32`, `arm-64` | エンジン             |
  | HTML5              |                    | `wasm-web`, `wasm_pthread-web` | エンジン       |

  (1 エディターは 64-bit の Ubuntu 向けにビルドし、テストしています。ほかのディストリビューションでも動作するはずですが、保証はしていません。)

  (2 エンジンのランタイムは、グラフィックスドライバーが最新であれば、ほとんどの 64-bit Linux ディストリビューションで動作するはずです。グラフィックス API について詳しくは、以下を参照してください。)


#### Q: Defold では、どのプラットフォーム向けにゲームを開発できますか？ {#q-what-target-platforms-can-i-develop-games-for-with-defold}

A: ワンクリックで、PS4™、PS5™、Nintendo Switch、iOS（64-bit）、Android（32-bit と 64-bit）、HTML5 に加え、macOS（x86-64 と arm64）、Windows（32-bit と 64-bit）、Linux（x86-64 と arm64）向けに公開できます。1つのコードベースで複数のプラットフォームをサポートできます。


#### Q: Defold はどのレンダリング API を使っていますか？ {#q-what-rendering-api-does-defold-rely-on}

A: 開発者は、[すべてをスクリプトで制御できるレンダリングパイプライン](/manuals/render/) を使う、単一のレンダリング API だけを扱えば十分です。Defold のレンダースクリプト（render script）API は、描画操作を次のグラフィックス API に変換します。

:[Graphics API](../shared/graphics-api.md)

#### Q: 使用中のバージョンを確認する方法はありますか？ {#q-is-there-a-way-to-know-what-version-im-running}

A: はい、Help メニューの「About」を選択します。ポップアップには、Defold のベータバージョンと、さらに重要な、そのリリース固有の SHA1 が明示されます。ランタイムのバージョンを調べるには、[`sys.get_engine_info()`](/ref/sys/#sys.get_engine_info) を使います。

[http://d.defold.com/beta](http://d.defold.com/beta) からダウンロードできる最新のベータ版は、[http://d.defold.com/beta/info.json](http://d.defold.com/beta/info.json) を開いて確認できます（安定版にも同じファイルがあります: [http://d.defold.com/stable/info.json](http://d.defold.com/stable/info.json)）。


#### Q: 実行時に、ゲームが動作しているプラットフォームを確認する方法はありますか？ {#q-is-there-a-way-to-know-what-platform-the-game-is-running-on-at-runtime}

A: はい、[`sys.get_sys_info()`](/ref/sys#sys.get_sys_info) を参照してください。


## エディターに関する質問 {#editor-questions}
:[Editor FAQ](../shared/editor-faq.md)


## Linux に関する質問 {#linux-questions}
:[Linux FAQ](../shared/linux-faq.md)


## Android に関する質問 {#android-questions}
:[Android FAQ](../shared/android-faq.md)


## HTML5 に関する質問 {#html5-questions}
:[HTML5 FAQ](../shared/html5-faq.md)


## iOS に関する質問 {#ios-questions}
:[iOS FAQ](../shared/ios-faq.md)


## Windows に関する質問 {#windows-questions}
:[Windows FAQ](../shared/windows-faq.md)


## ゲーム機に関する質問 {#console-questions}
:[Consoles FAQ](../shared/consoles-faq.md)


## ゲームの公開 {#publishing-games}

#### Q: ゲームを AppStore で公開しようとしています。IDFA についてはどう回答すればよいですか？ {#q-im-trying-to-publish-my-game-to-appstore-how-should-i-respond-to-idfa}

A: 申請時に、Apple は IDFA の3つの有効な用途に対応する3つのチェックボックスを提示します。

  1. アプリ内での広告の配信
  2. 広告経由のインストールのアトリビューション
  3. 広告経由のユーザー行動のアトリビューション

  選択肢1をチェックすると、アプリの審査担当者はアプリ内に広告が表示されるかを確認します。ゲームに広告が表示されない場合、却下される可能性があります。Defold 自体は広告 ID を使用しません。


#### Q: ゲームを収益化するにはどうすればよいですか？ {#q-how-do-i-monetize-my-game}

A: Defold は、アプリ内購入やさまざまな広告ソリューションをサポートしています。利用できる収益化の選択肢の最新の一覧は、[Asset Portal の Monetization カテゴリ](https://defold.com/tags/stars/monetization/) をご覧ください。


## Defold 使用時のエラー {#errors-using-defold}

#### Q: ビルドエラーは出ていないのにゲームを起動できません。何が問題ですか？ {#q-i-cant-start-the-game-and-there-is-no-build-error-whats-wrong}

A: 以前に発生したビルドエラーを修正した後でも、まれにビルド処理でファイルが再ビルドされないことがあります。メニューから *Project > Rebuild And Launch* を選択して、強制的に全体を再ビルドします。



## ゲームのコンテンツ {#game-content}

#### Q: Defold はプレハブをサポートしていますか？ {#q-does-defold-support-prefabs}

A: はい、サポートしています。Defold では [コレクション（collection）](/manuals/building-blocks/#collections) と呼びます。複雑なゲームオブジェクト（game object）の階層を作成し、個別の基本構成要素として保存できます。これらは、エディター内や実行時（コレクションの生成による）にインスタンス化できます。GUI ノード（GUI node）については、GUI テンプレートをサポートしています。


#### Q: ゲームオブジェクトを別のゲームオブジェクトの子として追加できないのはなぜですか？ {#q-i-cant-add-a-game-object-as-a-child-to-another-game-object-why}

A: ゲームオブジェクトファイル内で子を追加しようとしている可能性がありますが、それはできません。子を追加できるのはコレクションファイル内だけです。その理由を理解するには、親子階層が厳密には _シーングラフ_（scene graph）のトランスフォーム階層であることを思い出してください。シーン（コレクション）に配置（または生成）されていないゲームオブジェクトは、シーングラフの一部ではないため、シーングラフ階層の一部にもなれません。ゲームオブジェクトの親の ID は、[`go.get_parent()`](https://defold.com/ref/stable/go-lua/#go.get_parent:id) で取得できます。


#### Q: ゲームオブジェクトのすべての子にメッセージをブロードキャストできないのはなぜですか？ {#q-why-cant-i-broadcast-messages-to-all-children-of-a-game-object}

A: 親子関係はシーングラフのトランスフォームの関係だけを表しており、オブジェクト指向の集約と混同しないでください。ゲームのデータと、ゲームの状態が変わるときにそのデータをどう変換するのが最適かに注目すると、状態データを含むメッセージを多数のオブジェクトに常時送る必要性は少なくなるでしょう。データの階層が必要な場合は、Lua で簡単に構築して扱えます。


#### Q: スプライトの縁に表示の乱れが生じるのはなぜですか？ {#q-why-am-i-experiencing-visual-artifacts-around-the-edges-of-my-sprites}

A: これは「エッジブリーディング（edge bleeding）」と呼ばれる表示の乱れです。アトラス（atlas）内で隣り合うピクセルの縁が、スプライト（sprite）に割り当てられた画像ににじみ込みます。解決するには、アトラス内の画像の縁に、同じピクセルの行と列を追加して余白を設けます。幸い、Defold のアトラスエディターで自動的に行えます。アトラスを開き、*Extrude Borders* の値を1に設定します。


#### Q: スプライトの色調を変えたり透明にしたりできますか？そのために独自のシェーダーを記述する必要がありますか？ {#q-can-i-tint-my-sprites-or-make-them-transparent-or-do-i-have-to-write-my-own-shader-for-it}

A: すべてのスプライトでデフォルトで使用される組み込みのスプライトシェーダーには、「tint」という定数が定義されています。

  ```lua
  local red = 1
  local green = 0.3
  local blue = 0.55
  local alpha = 1
  go.set("#sprite", "tint", vmath.vector4(red, green, blue, alpha))
  ```


#### Q: スプライトの z 座標を100に設定すると描画されません。なぜですか？ {#q-if-i-set-the-z-coordinate-of-a-sprite-to-100-then-its-not-rendered-why}

A: ゲームオブジェクトの Z 位置は、描画順序を制御します。小さい値のものが、大きい値のものより先に描画されます。デフォルトのレンダースクリプトでは、深度が -1 から1の範囲にあるゲームオブジェクトが描画され、それより小さいものや大きいものは描画されません。レンダースクリプトについて詳しくは、公式の [レンダリングドキュメント](/manuals/render) をご覧ください。GUI ノードでは Z 値は無視され、描画順序にまったく影響しません。代わりに、ノードはリストに並んでいる順序と子の階層（およびレイヤー構成）に従って描画されます。GUI の描画と、レイヤーを使ったドローコールの最適化について詳しくは、公式の [GUI ドキュメント](/manuals/gui) をご覧ください。


#### Q: ビュープロジェクションの Z 範囲を -100 から100に変更すると、パフォーマンスに影響しますか？ {#q-would-changing-the-view-projection-z-range-to-100-to-100-impact-performance}

A: いいえ。影響するのは精度だけです。Z バッファーは対数的で、0に近い z 値の分解能は非常に高く、0から遠くなるほど分解能が低くなります。たとえば、24 bit バッファーでは10.0と10.000005を区別できますが、10000と10005は区別できません。


#### Q: 角度の表し方に一貫性がないのはなぜですか？ {#q-there-is-no-consistency-to-how-angles-are-represented-why}

A: 実際には一貫性があります。エディターとゲーム API では、角度はどこでも度で表します。数学ライブラリではラジアンを使います。現在、この規則の例外は物理プロパティの `angular_velocity` で、ラジアン/秒で表されます。これは変更される予定です。


#### Q: 色だけを設定した（テクスチャのない）GUI ボックスノードを作成すると、どのように描画されますか？ {#q-when-creating-a-gui-box-node-with-only-color-no-texture-how-will-it-be-rendered}

A: 頂点カラーを使った形状として描画されます。この場合でもフィルレートを消費することに留意してください。


#### Q: 実行中にアセットを変更すると、エンジンは自動的にアンロードしますか？ {#q-if-i-change-assets-on-the-fly-will-the-engine-automatically-unload-them}

A: すべてのリソースは内部で参照カウントにより管理されています。参照カウントが0になるとすぐに、そのリソースは解放されます。


#### Q: ゲームオブジェクトにアタッチされた音声コンポーネントを使わずに、音声を再生できますか？ {#q-is-it-possible-to-play-audio-without-the-use-of-an-audio-component-attached-to-a-game-object}

A: すべてがコンポーネント（component）を基にしています。複数のサウンドを持ち、画面に表示されないヘッドレスのゲームオブジェクトを作成して、このサウンド制御用オブジェクトにメッセージを送ることでサウンドを再生できます。


#### Q: 音声コンポーネントに関連付けられた音声ファイルを、実行時に変更できますか？ {#q-is-it-possible-to-change-the-audio-file-associated-with-an-audio-component-at-run-time}

A: 一般に、すべてのリソースは静的に宣言されているため、リソース管理を自分で行う必要がないという利点があります。[リソースプロパティ](/manuals/script-properties/#resource-properties) を使って、コンポーネントに割り当てるリソースを変更できます。


#### Q: 物理のコリジョン形状のプロパティにアクセスする方法はありますか？ {#q-is-there-a-way-to-access-the-physics-collision-shape-properties}

A: はい、物理 API、特に [`physics.get_shape()`](https://defold.com/ref/stable/physics-lua/#physics.get_shape:url-shape) と [`physics.set_shape()`](https://defold.com/ref/stable/physics-lua/#physics.set_shape:url-shape-table) を参照してください。 


#### Q: シーン内のコリジョンオブジェクトを手早く描画する方法はありますか？（Box2D のデバッグ描画のように） {#q-is-there-any-quick-way-to-render-the-collision-objects-in-my-scene-like-box2ds-debug-draw}

A: はい、*physics.debug* フラグを *game.project* で設定します。（公式の [プロジェクト設定ドキュメント](/manuals/project-settings/#debug) を参照してください。）


#### Q: 接触や衝突が多い場合、パフォーマンス上の負荷はどの程度ですか？ {#q-what-are-the-performance-costs-of-having-many-contactscollisions}

A: Defold は内部で Box2D の修正版を実行しており、パフォーマンス上の負荷はかなり近いはずです。[プロファイラー](/manuals/debugging) を開けば、エンジンが物理処理に費やしている時間をいつでも確認できます。使用するコリジョンオブジェクト（collision object）の種類も考慮する必要があります。たとえば、静的オブジェクトはパフォーマンス上の負荷が小さくなります。詳しくは、Defold の公式 [物理ドキュメント](/manuals/physics) を参照してください。


#### Q: パーティクルエフェクトのコンポーネントが多いと、パフォーマンスにどのような影響がありますか？ {#q-whats-the-performance-impact-of-having-many-particle-effect-components}

A: 再生中かどうかによって異なります。再生していない ParticleFx のパフォーマンス上の負荷はゼロです。再生中の ParticleFx がパフォーマンスに与える影響は設定によって異なるため、プロファイラーを使って評価する必要があります。ほとんどのほかの要素と同様に、*game.project* の max_count で定義された ParticleFx の数だけ、メモリがあらかじめ確保されます。


#### Q: コレクションプロキシで読み込んだコレクション内のゲームオブジェクトで、入力を受け取るにはどうすればよいですか？ {#q-how-do-i-receive-input-to-a-game-object-inside-a-collection-loaded-via-a-collection-proxy}

A: コレクションプロキシ（collection proxy）で読み込んだコレクションは、それぞれ独自の入力スタックを持ちます。入力は、メインコレクションの入力スタックからプロキシコンポーネントを経由して、コレクション内のオブジェクトへ送られます。つまり、読み込んだコレクション内のゲームオブジェクトが入力フォーカスを取得するだけでは不十分で、プロキシコンポーネントを _持つ_ ゲームオブジェクトも入力フォーカスを取得する必要があります。詳しくは、[入力ドキュメント](/manuals/input) をご覧ください。


#### Q: 文字列型のスクリプトプロパティを使えますか？ {#q-can-i-use-string-type-script-properties}

A: いいえ。Defold は [hash](/ref/builtins#hash) 型のプロパティをサポートしています。これらは、種類、状態の識別子、あらゆる種類のキーを表すために使えます。ハッシュはゲームオブジェクトの ID（パス）の格納にも使えますが、エディターが関連する URL をドロップダウンに自動で列挙するため、[url](/ref/msg#msg.url) プロパティのほうが適していることがよくあります。詳しくは、[スクリプトプロパティのドキュメント](/manuals/script-properties) をご覧ください。


#### Q: 行列（[`vmath.matrix4()`](/ref/vmath/#vmath.matrix4:m1) などで作成したもの）の個々の要素にアクセスするにはどうすればよいですか？ {#q-how-do-i-access-the-individual-cells-of-a-matrix-created-using-vmathmatrix4refvmathvmathmatrix4m1-or-similar}

A: `mymatrix.m11`、`mymatrix.m12`、`mymatrix.m21` などを使って、要素にアクセスします。


#### Q: `Not enough resources to clone the node` というエラーが [gui.clone()](/ref/gui/#gui.clone:node) や [gui.clone_tree()](/ref/gui/#gui.clone_tree:node) を使うと出るのですが？ {#q-i-am-getting-not-enough-resources-to-clone-the-node-when-using-guiclonerefguiguiclonenode-or-guiclone_treerefguiguiclone_treenode}

A: GUI コンポーネントの `Max Nodes` の値を増やします。Outline でコンポーネントのルートを選択すると、Properties パネルでこの値を確認できます。


## フォーラム {#the-forum}

#### Q: 自分の仕事を宣伝するスレッドを投稿してもよいですか？ {#q-can-i-post-a-thread-where-i-advertise-my-work}

A: もちろんです！そのための専用の [「Work for hire」カテゴリ](https://forum.defold.com/c/work-for-hire) があります。コミュニティの役に立つ活動は常に歓迎しており、報酬の有無を問わずコミュニティにサービスを提供することは、そのよい例です。


#### Q: スレッドを作成して自分の作品を掲載しました。さらに追加してもよいですか？ {#q-i-made-a-thread-and-added-my-workcan-i-add-more}

A: 「Work for hire」スレッドを上位に押し上げる投稿を減らすため、自分のスレッドへの投稿は14日ごとに1回までとします（ただし、スレッド内のコメントへの直接の返信は可能です）。14日間のうちにスレッドへ作品を追加したい場合は、既存の投稿を編集して追加してください。


#### Q: Work for Hire カテゴリに求人を投稿してもよいですか？ {#q-can-i-use-the-work-for-hire-category-to-post-job-offerings}

A: はい、ぜひご利用ください！仕事の申し出にも依頼にも使えます。たとえば、「プログラマーです。2D ピクセルアーティストを探しています。資金は豊富なので、十分な報酬をお支払いします」といった投稿ができます。
