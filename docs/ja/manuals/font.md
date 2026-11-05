---
title: Defold のフォントマニュアル
brief: このマニュアルでは、Defold でのフォントの扱いと、ゲームの画面にフォントを表示する方法を説明します。
---

# フォントファイル {#font-files}

フォントは、ラベル（Label）コンポーネント（component）と GUI のテキストノード（text node）でテキストを描画するために使います。Defold は、次のフォントファイル形式をサポートしています。

- TrueType
- OpenType
- BMFont

従来のテキストレイアウトエンジンと完全なテキストレイアウトエンジンは、どちらも TrueType の輪郭と OpenType CFF1/CFF2 の輪郭に対応し、`.ttf` と `.otf` リソースからの実行時生成もサポートします。

個々のテキストスパンにスタイルを適用する方法や、リンクとインラインのスプライトの扱いについては、[リッチテキストマークアップのマニュアル](/manuals/font-richtext)を参照してください。

TrueType と OpenType のフォントでは、*Mode* プロパティでグリフの描画方法を選択します。

- **Bitmap** は、ラスタライズされたグリフ画像を使います。
- **SDF**（符号付き距離場）は、グリフの縁までの距離をテクスチャに格納し、Bitmap より柔軟に拡大縮小できます。
- **Vector** は、曲線データからグリフの本体を描画し、拡大縮小しても鮮明さを保ちます。輪郭線と影のエフェクトは引き続きビットマップデータを使います。

新しく作成したフォントリソースでは、**Vector** モードと **Dynamic** グリフ生成を使います。既存のフォントリソースは Bitmap または SDF モードを保持します。BMFont ソースは、常に付属のビットマップを使います。

Vector モードには `RGBA16F` と `R32UI` テクスチャへの対応が必要で、OpenGL ES 2 と WebGL 1 では利用できません。非対応のグラフィックスアダプターを対象とする場合は、Bitmap または SDF フォントと、それに合うマテリアルを使ってください。Vector から SDF への自動フォールバックはありません。設定については、[ベクターフォント](#vector-fonts)を参照してください。

## オフラインフォントとランタイムフォント {#offline-or-runtime-fonts}

*Glyph Generation* プロパティでは、各フォントのグリフデータを生成するタイミングを選択します。

- **Static** は、選択したグリフをビルド時（オフライン）に生成します。*Characters* と *All Chars* で、含めるグリフを指定します。実行時生成用のソース `.ttf` または `.otf` ファイルはバンドルしません。
- **Dynamic** は、ソースの `.ttf` または `.otf` ファイルをバンドルし、実行時に必要に応じてグリフを生成します。*Prewarm Text* は、フォントを読み込むときにグリフを準備します。ほかのグリフは後から必要に応じて生成できます。

SDF フォントと Vector フォントは、どちらの選択肢にも対応します。Bitmap フォントと BMFont ソースは Static 生成を使います。各フォントリソースを個別に設定するため、プロジェクト内で Static フォントと Dynamic フォントを混在させられます。

動的生成は、特に文字集合の大きなフォントで、バンドルサイズと実行時のメモリ使用量を削減できます。エンジンの完全なテキストレイアウトシステムが必要です。[ランタイムフォントの有効化](#enabling-runtime-fonts)を参照してください。

## テキストレイアウトのサポート（右から左への表示など） {#text-layout-support-eg-right-to-left}

ランタイムフォントには、右から左への表示など、完全なテキストレイアウトをサポートするという利点もあります。
現在は、[HarfBuzz](https://github.com/harfbuzz/harfbuzz)、[SheenBidi](https://github.com/Tehreer/SheenBidi)、[libunibreak](https://github.com/adah1972/libunibreak)、[SkriBidi](https://github.com/memononen/Skribidi) ライブラリを使用しています。

[ランタイムフォントの有効化](/manuals/font#enabling-runtime-fonts)を参照してください。

エディターは、フォントとシーン内のテキストのプレビューにエンジンのフォントレンダラーを使います。テキストの字形形成と右から左へのレイアウトには、[ランタイムフォント](#enabling-runtime-fonts)と App Manifest の **Use full text layout system** オプションが必要です。オフラインフォントの場合、プレビューはフォントの **Characters** と **All Chars** 設定に従います。

## フォントコレクション {#font-collection}

`.fontc` ファイル形式は、フォントコレクション（font collection）とも呼ばれます。オフラインモードでは、1つのフォントだけが関連付けられます。
ランタイムフォントを使うと、複数のフォントファイル（`.ttf` または `.otf`）をフォントコレクションに関連付けられます。

これにより、異なる言語の複数のテキストを描画するときに、メモリ占有量を低く抑えながらフォントコレクションを使用できます。
たとえば、日本語フォントを含むコレクション（collection）を読み込み、そのフォントを現在のメインフォントに関連付けた後、日本語フォントのコレクションをアンロードします。

## フォントの作成 {#creating-a-font}

Defold で使うフォントを作成するには、メニューから <kbd>File ▸ New...</kbd> を選択し、続いて <kbd>Font</kbd> を選択して、新しい Font ファイルを作成します。*Assets* ブラウザーの任意の場所を <kbd>右クリック</kbd> し、<kbd>New... ▸ Font</kbd> を選択することもできます。

![新しいフォントの名前](images/font/new_font_name.png)

新しいフォントファイルに名前を付けて <kbd>Ok</kbd> をクリックします。新しいフォントファイルがエディターで開きます。

使用するフォントを *Assets* ブラウザーにドラッグし、適切な場所にドロップします。

*Font* プロパティにフォントファイルを設定します。`.ttf` または `.otf` ソースでは、*Mode* と *Glyph Generation* を選択し、残りのプロパティを必要に応じて設定します。Dynamic 生成では、[ランタイムフォントの設定](#enabling-runtime-fonts)も完了してください。

![Vector モードと Dynamic グリフ生成を選択したフォントのプロパティ](images/font/font_properties.png)

Vector フォントでは、Label コンポーネントまたは GUI テキストノードの *Font Size* で、表示する文字のサイズを変更します。*Outline/Shadow Bitmap Size* は、表示サイズとは独立して、エフェクト用ビットマップの解像度を制御します。

Bitmap フォントと SDF フォントでは、フォントリソースの *Size* で、生成するグリフのサイズを選択します。BMFont のサイズはソースの `.fnt` ファイルから取得します。これらのフォントの表示サイズを変更するには、Label コンポーネントまたは GUI テキストノードを拡大縮小します。

## プロパティ {#properties}

*Font*
: フォントデータの生成に使う TTF、OTF、または *`.fnt`* ファイルです。

*Material*
: このフォントを描画する際のマテリアルです。フォントのモードと一致する必要があります。[フォントのマテリアル](#font-materials)を参照してください。

*Mode*
: `.ttf` または `.otf` ソースの描画方法で、**Bitmap**、**SDF**、**Vector** から選びます。以前の *Output Format* プロパティを置き換えるものです。BMFont ソースでは表示しません。

*Glyph Generation*
: **Static** はビルド時にグリフデータを生成します。**Dynamic** は実行時に生成し、[完全なテキストレイアウトシステム](#enabling-runtime-fonts)を必要とします。このプロパティは SDF フォントと Vector フォントで利用できます。Bitmap モードでは Static に固定され、BMFont ソースでは表示しません。

*Render Mode*
: 生成する Bitmap フォントのレイヤー構成です。`.ttf` または `.otf` ソースの Bitmap モードでのみ表示します。SDF、Vector、BMFont ソースでは、Defold がレイヤー構成を自動的に選択します。

  - **Single Layer** は、各文字に1つの四角形を生成します。
  - **Multi Layer** は、グリフの形、輪郭線、影に別々の四角形を生成します。レイヤーは奥から手前の順に描画するため、輪郭線の幅がグリフ間の距離より大きい場合も、先に描画した文字を別の文字が覆うのを防げます。*Shadow X/Y* プロパティによる影のオフセットも有効になります。

*Size*
: Bitmap または SDF のフォントデータを生成するときの、グリフのピクセル単位のサイズです。BMFont ソースでは `.fnt` ファイルからサイズを読み取り、ここでは編集できません。

*Outline/Shadow Bitmap Size*
: Vector モードでは *Size* に代わって表示されます。Static と Dynamic の両方で、有効な輪郭線と影のエフェクトのビットマップ解像度を制御します。グリフ本体は曲線データを使うため、どちらのエフェクトも有効でない場合は無効になります。Label や GUI テキストノードの *Font Size* を変更しても、この共有ビットマップの解像度は変わりません。

*Antialias*
: Bitmap フォントデータの生成時に、グリフにアンチエイリアスを適用するかどうかです。ピクセル単位で正確に描画するには無効にします。`.ttf` または `.otf` ソースの Bitmap モードでのみ表示します。

*Alpha*
: グリフの透明度です。範囲は 0.0--1.0 で、0.0は透明、1.0は不透明を意味します。

*Outline Alpha*
: 生成するアウトラインの透明度です。範囲は 0.0--1.0 です。

*Outline Width*
: 生成するアウトラインの幅（ピクセル単位）です。アウトラインを付けない場合は、0に設定します。

*Shadow Alpha*
: 生成する影の透明度です。範囲は 0.0--1.0 です。

::: sidenote
組み込みの Bitmap フォントシェーダーは、*Single Layer* と *Multi Layer* の両方の描画モードで影に対応します。*Single Layer* で描画し、影が不要な生成 Bitmap フォントでは、カスタムマテリアルに `/builtins/fonts/font-singlelayer.fp` を使えます。SDF と Vector のフォントには、モードに合うシェーダーが必要です。[フォントのマテリアル](#font-materials)を参照してください。
:::

*Shadow Blur*
: 生成する影に適用するぼかしの量です。鮮明な影にするには 0 に設定します。

*Shadow X/Y*
: 生成する影の、ピクセル単位の水平および垂直オフセットです。生成 Bitmap フォントでは、これらを適用するために *Multi Layer* 描画モードを使います。SDF と Vector フォントでは、Defold が適切なレイヤーを自動選択します。

*Characters*
: Static 生成で、ビルドするフォントに含める文字です。デフォルトでは ASCII の印字可能文字（文字コード 32～126）が含まれます。文字を追加または削除して、実行時に利用できるグリフを制御します。

*Prewarm Text*
: Dynamic 生成では、*Characters* に代わって表示されます。このテキストを使い、フォントを読み込むときにグリフを生成してキャッシュを事前準備します。後で生成できる文字を制限するものではありません。[`font.prewarm_text()`](/ref/font/#font.prewarm_text) で、スクリプトからテキストを事前準備することもできます。

::: sidenote
ASCII の印字可能文字は次のとおりです。
スペース ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ \` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
:::

*All Chars*
: Static 生成で、*Characters* に限定せず、ソース内のすべてのグリフを含めます。Dynamic フォントでは、このプロパティは表示しません。

*Cache Width/Height*
: Bitmap と SDF フォント、および Vector の輪郭線と影に使うグリフキャッシュのビットマップサイズを制限します。エンジンは文字を描画するとき、キャッシュビットマップからグリフを検索します。存在しない場合は、描画前にキャッシュへ追加します。要求されたすべてのグリフを収めるにはキャッシュビットマップが小さすぎる場合、エラーになります（`ERROR:RENDER: Out of available cache cells! Consider increasing cache_width or cache_height for the font.`）。

  0に設定するとキャッシュサイズは自動で設定され、最大 2048x4096 まで拡大します。

## フォントのマテリアル {#font-materials}

フォントのモードに合うマテリアルを使います。フォントリソースの *Material* は GUI テキストノードが使います。Label コンポーネントには独自の *Material* プロパティがあり、こちらもフォントと一致する必要があります。

| フォントのモードまたはソース | GUI テキスト用のフォントマテリアル | Label コンポーネントのマテリアル |
| --- | --- | --- |
| Bitmap | `/builtins/fonts/font.material` | `/builtins/fonts/label.material` |
| SDF | `/builtins/fonts/font-df.material` | `/builtins/fonts/label-df.material` |
| Vector | `/builtins/fonts/font-vector.material` | `/builtins/fonts/label-vector.material` |
| BMFont (`.fnt`) | `/builtins/fonts/font-fnt.material` | `/builtins/fonts/label-fnt.material` |

フォントエディターで *Mode* を変更すると、対応する組み込みの Bitmap、SDF、Vector マテリアルのいずれかが割り当てられている場合は、マテリアルも切り替わります。カスタムマテリアルは自動では置き換えません。そのフォントを使う Label コンポーネントの *Material* プロパティも確認してください。

## ベクターフォント {#vector-fonts}

ベクターフォントは曲線からグリフ本体を描画するため、表示サイズを変更しても鮮明さを保ちます。実行時にグリフを生成するフォントは、次のように設定します。

1. `/fonts/ui.font` などの `.font` リソースを作成し、*Font* プロパティに TrueType または OpenType ソースを選択します。通常のテキストには、組み込みの `/builtins/fonts/vera_mo_bd.ttf` を使えます。
2. *Mode* を **Vector**、*Glyph Generation* を **Dynamic**、*Material* を `/builtins/fonts/font-vector.material` に設定します。これらは新しいフォントリソースのデフォルト値です。
3. プロジェクトに割り当てた App Manifest で **Use full text layout system** を有効にします。[ランタイムフォントの有効化](#enabling-runtime-fonts)に従い、カスタムエンジンを設定します。
4. *game.project* で [Shader ▸ Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20) を有効にします。
5. フォントを [Label](/manuals/label/) に割り当てるか、GUI シーンの *Fonts* に追加して[テキストノード](/manuals/gui-text/)で選択します。Label では、コンポーネントの *Material* も `/builtins/fonts/label-vector.material` に設定します。コンポーネントまたはノードの *Font Size* に、表示したいサイズを設定します。

Vector のグリフ本体は曲線テクスチャを使いますが、有効な輪郭線と影は引き続き SDF ビットマップデータを生成し、グリフキャッシュのテクスチャメモリを消費します。*Outline/Shadow Bitmap Size* は、そのビットマップの解像度を Label や GUI テキストノードの *Font Size* とは独立して設定します。エフェクトが不要な場合は、*Outline Alpha* と *Shadow Alpha* を `0` にすると、ビットマップデータの生成を避けられます。

### カラー絵文字 {#color-emoji}

Vector フォントは、パレットの色や線形・放射状グラデーションを含む COLRv1 カラー絵文字を描画できます。Bitmap と SDF のモードは、COLRv1 の色を描画しません。上記の Dynamic Vector の設定を行い、フォントコレクションに COLRv1 絵文字フォントをフォールバックとして追加します。通常のテキストは引き続き元のフォントを使います。

たとえば COLRv1 の [Noto Color Emoji フォント](https://github.com/google/fonts/blob/main/ofl/notocoloremoji/NotoColorEmoji-Regular.ttf)を、プロジェクトに `/fonts/NotoColorEmoji-Regular.ttf` としてコピーします。COLRv1 版を選んでください。ほかの絵文字フォントは、ファイル名が `.ttf` で終わっていても、異なるカラー形式を使う場合があります。

*game.project* の **Project ▸ Custom Resources** に `/fonts/NotoColorEmoji-Regular.ttf` を追加します。ほかのカスタムリソースがない場合、設定は次のようになります。

```ini
[project]
custom_resources = /fonts/NotoColorEmoji-Regular.ttf
```

Lua にフォントパスを書くだけでは、フォントファイルはバンドルされません。[Custom Resources](/manuals/project-settings/#custom-resources) に設定すると、リソースシステム経由で読み込む [`font.add_font()`](/ref/font/#font.add_font) から、このソースフォントを利用できます。バンドルから読み込む際は、ソースフォントのパスを文字列で渡します。

フォールバックの追加は、共有フォントリソースごとに1回だけ行います。この変更は、そのフォントを使うすべての Label と GUI テキストノードに反映され、同じフォールバックを2回追加するとエラーになります。同じ `.font` で [Label の例](/manuals/label/#vector-fonts-and-color-emoji)と [GUI の例](/manuals/gui-text/#vector-fonts-and-color-emoji)を併用する場合は、どちらかが事前準備や表示を行う前に、フォールバックを1回だけ追加するよう初期化を調整します。これらの例は、フォールバック追加後にテキスト全体を事前準備し、コールバックが成功してから表示します。

## 距離フィールドフォント {#distance-field-fonts}

距離フィールドフォントは、ビットマップデータの代わりに、グリフの輪郭までの距離をテクスチャに格納します。エンジンがフォントを描画するには、距離データを解釈し、それを使ってグリフを描画する専用のシェーダーが必要です。距離フィールドフォントはビットマップフォントより多くのリソースを消費しますが、サイズ変更の自由度が高くなります。

![距離フィールドフォント](images/font/df_font.png)

*Mode* で **SDF** を選択し、*Glyph Generation* で **Static** または **Dynamic** を選びます。フォントには *`/builtins/fonts/font-df.material`*、Label コンポーネントには *`/builtins/fonts/label-df.material`*、または距離場データを処理するカスタムマテリアルを使います。

## ビットマップの BMFont {#bitmap-bmfonts}

Defold は、生成したビットマップに加え、あらかじめ焼き込まれたビットマップの「BMFont」形式のフォントをサポートしています。この形式のフォントは、すべてのグリフを含む PNG フォントシートで構成されます。さらに、*`.fnt`* ファイルには、各グリフのシート上の位置と、サイズやカーニングの情報が含まれています。（Defold は、Phaser などのツールが使用する *`.fnt`* 形式の XML 版をサポートしていません。）

この形式のフォントには、TrueType や OpenType フォントファイルから生成したビットマップフォントに対するパフォーマンス上の利点はありませんが、任意のグラフィックス、色、影を画像に直接含められます。

生成した *`.fnt`* と *`.png`* ファイルを Defold プロジェクトに追加します。これらは同じフォルダーに配置してください。新しいフォントファイルを作成し、*Font* プロパティに *`.fnt`* ファイルを設定します。Defold は付属のビットマップを使い、`.fnt` ファイルからサイズを読み取ります。BMFont ソースでは *Mode* と *Glyph Generation* は表示されません。

::: sidenote
BMFont を作成するには、適切なファイルを生成できるツールを使う必要があります。次のような選択肢があります。

* [Bitmap Font Generator](http://www.angelcode.com/products/bmfont/) は、AngelCode が提供する Windows 専用のツールです。
* [Shoebox](http://renderhjs.net/shoebox/) は、Windows と macOS 向けの、Adobe Air を基盤とする無料アプリです。
* [Hiero](https://libgdx.com/wiki/tools/hiero) は、Java を基盤とするオープンソースのツールです。
* [Glyph Designer](https://71squared.com/glyphdesigner) は、71 Squared が提供する macOS 向けの有料ツールです。
* [bmGlyph](https://www.bmglyph.com) は、Sovapps が提供する macOS 向けの有料ツールです。
:::

![BMFont](images/font/bm_font.png)

フォントの *Material* を *`/builtins/fonts/font-fnt.material`* に設定します。Label コンポーネントでは *`/builtins/fonts/label-fnt.material`* を使います。

## 描画の乱れとベストプラクティス {#artifacts-and-best-practices}

一般に、拡大縮小せずにフォントを描画する場合は、ビットマップフォントが最適です。距離フィールドフォントより高速に画面へ描画できます。

距離フィールドフォントは、拡大しても良好な表示を維持できます。一方、ビットマップフォントはピクセルで構成された画像なので、フォントを拡大するとピクセルも大きくなり、ブロック状の乱れが生じます。次は、フォントサイズ48ピクセルのサンプルを4倍に拡大したものです。

![拡大したフォント](images/font/scale_up.png)

縮小する場合、ビットマップテクスチャは GPU によってきれいかつ効率よく縮小され、アンチエイリアスを適用できます。ビットマップフォントは、距離フィールドフォントよりも色をよく維持します。次は、同じサイズ48ピクセルのサンプルフォントを1/5のサイズに縮小したものの拡大表示です。

![縮小したフォント](images/font/scale_down.png)

距離フィールドフォントは、グリフの曲線を表現できる距離情報を保持するのに十分な目標サイズで描画する必要があります。次は、上と同じフォントを18ピクセルのサイズで作成し、10倍に拡大したものです。この書体の形状をエンコードするには、このサイズが小さすぎることがはっきりと分かります。

![距離フィールドの描画の乱れ](images/font/df_artifacts.png)

影や輪郭線が不要な場合は、それぞれのアルファ値をゼロにします。そうしないと影と輪郭線のデータも生成され、不要なメモリを消費します。Vector モードでは、両方を無効にするとビットマップデータの生成を避けられます。グリフ本体は引き続き曲線データを使います。

## フォントキャッシュ {#font-cache}
Bitmap と SDF のフォントリソースは、実行時にグリフキャッシュテクスチャとフォントデータを使います。Vector フォントはグリフ本体を曲線データとして格納し、有効な輪郭線と影にビットマップキャッシュを使います。以下のテクスチャ配置の説明は、Bitmap と SDF フォントに適用されます。

* フォントデータはグリフエントリーのリストで構成され、各エントリーには基本的なカーニング情報と、そのグリフのビットマップデータが含まれます。
* テクスチャは内部的には「グリフキャッシュテクスチャ」と呼ばれ、特定のフォントでテキストを描画するときに使われます。

実行時にテキストを描画するとき、エンジンはまず描画対象のグリフを順に調べ、どのグリフがテクスチャキャッシュにあるか確認します。グリフテクスチャキャッシュにないグリフごとに、フォントデータに格納されたビットマップデータからテクスチャへのアップロードが行われます。

各グリフは内部的にフォントのベースラインに合わせてキャッシュ内に配置されるため、シェーダーで、そのグリフに対応するキャッシュセル内のローカルテクスチャ座標を計算できます。これにより、グラデーションやテクスチャの重ね合わせなど、特定のテキストエフェクトを動的に実現できます。エンジンは、`texture_size_recip` という特別なシェーダー定数を通じて、キャッシュに関する指標をシェーダーに提供します。この定数のベクトル成分には、次の情報が含まれます。

* `texture_size_recip.x` は、キャッシュの幅の逆数です。
* `texture_size_recip.y` は、キャッシュの高さの逆数です。
* `texture_size_recip.z` は、キャッシュの幅に対するキャッシュセルの幅の比率です。
* `texture_size_recip.w` は、キャッシュの高さに対するキャッシュセルの高さの比率です。

たとえば、フラグメントシェーダーでグラデーションを生成するには、次のように記述します。

`float horizontal_gradient = fract(var_texcoord0.y / texture_size_recip.w);`

シェーダーのユニフォーム（uniform）の詳細は、[シェーダーマニュアル](/manuals/shader)を参照してください。

## ランタイムフォントの有効化 {#enabling-runtime-fonts}

実行時生成は、フォントリソースごとに設定します。

1. `.font` リソースを開き、TrueType（`.ttf`）または OpenType（`.otf`）ソースを選択します。
2. *Mode* を **SDF** または **Vector**、*Glyph Generation* を **Dynamic** に設定します。
3. 対応する[フォント用と Label 用のマテリアル](#font-materials)を選択します。
4. [App Manifest](/manuals/app-manifest) を追加し、*game.project* の *Native Extensions ▸ App Manifest* に割り当て、**Use full text layout system** を有効にします。これにより、実行時フォント生成と完全なテキストレイアウトに対応したカスタムエンジンをビルドします。
5. フォントの読み込み直後に表示するテキストを *Prewarm Text* に設定します。後で必要になるテキストには [`font.prewarm_text()`](/ref/font/#font.prewarm_text) を使い、コールバックを待ってから表示します。

新しいフォントリソースは、すでに Vector モードと Dynamic 生成を使いますが、上記の App Manifest の設定は引き続き必要です。

### フォントのスクリプティング {#font-scripting}

#### グリフキャッシュの事前準備 {#prewarming-glyph-cache}

Dynamic フォントは、フォント読み込み時に *Prewarm Text* に必要なグリフを生成します。このフィールドはレイアウトするテキストとして解釈され、そのテキストに必要なグリフをキャッシュに準備します。Dynamic フォントでは *All Chars* は利用できません。

Dynamic フォントには、`font.prewarm_text(font_collection, text, callback)` も呼び出せます。コールバックは、不足するすべてのグリフがキャッシュに追加され、テキストを表示してよくなったことを通知します。Static フォントでは、この関数を使えません。

### フォントコレクションへのフォントの追加と削除 {#addingremoving-fonts-to-a-font-collection}

Dynamic フォントでは、フォントコレクションにソースフォント（`.ttf` または `.otf`）を追加したり、削除したりできます。
これは、大きなフォントが異なる文字セット（CJK など）ごとに複数のファイルに分割されている場合に便利です。

::: important
フォントコレクションにフォントを追加しても、すべてのグリフが自動的に読み込まれたり、描画されたりするわけではありません。
:::

```lua
function init(self)
    -- Get the target font collection.
    self.font_collection = go.get("#label", "font")

    -- Get the first font assigned to the selected language collection.
    local language_collection = go.get("localization_japanese#label", "font")
    local font_info = font.get_info(language_collection)
    self.language_ttf_hash = font_info.fonts[1].path_hash

    -- Associate it with the target collection and increase its reference count.
    font.add_font(self.font_collection, self.language_ttf_hash)
end
```

```lua
function final(self)
    -- Remove the association and release the font reference.
    font.remove_font(self.font_collection, self.language_ttf_hash)
end
```

### グリフの事前準備 {#prewarming-glyphs}

ランタイムフォントでテキストを正しく表示するには、グリフを解決する必要があります。`font.prewarm_text()` がこの処理を行います。
これは非同期処理であり、処理が完了してコールバックを受け取ると、それらのグリフを含むメッセージの表示に進めます。

::: important
グリフキャッシュがいっぱいになると、キャッシュ内の最も古いグリフが追い出されます。
:::

```lua
font.prewarm_text(self.font_collection, info.text, function (self, request_id, result, err)
    if result then
      print("PREWARMING OK!")
      go.set(self.label, "text", info.text)
    else
      print("Error prewarming text:", err)
    end
  end)
```
