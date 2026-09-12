---
title: Defold のフォントマニュアル
brief: このマニュアルでは、Defold でのフォントの扱いと、ゲームの画面にフォントを表示する方法を説明します。
---

# フォントファイル {#font-files}

フォントは、ラベル（Label）コンポーネント（component）と GUI のテキストノード（text node）でテキストを描画するために使います。Defold は、次のフォントファイル形式をサポートしています。

- TrueType
- OpenType
- BMFont

Defold 1.13.2 以降では、従来のテキストレイアウトエンジンと完全なテキストレイアウトエンジンの両方が、TrueType のアウトラインと OpenType CFF1/CFF2 のアウトラインをサポートします。`.ttf` および `.otf` リソースからの実行時生成にも対応しています。

個々のテキストスパンにスタイルを適用する方法や、リンクとインラインのスプライトの扱いについては、[リッチテキストマークアップのマニュアル](/manuals/font-richtext)を参照してください。

プロジェクトに追加したフォントは、Defold が描画できるテクスチャ（texture）形式に自動的に変換されます。フォントの描画方式には次の2種類があり、それぞれに利点と欠点があります。

- ビットマップ（Bitmap）
- 距離フィールド（Distance field）

## オフラインフォントとランタイムフォント {#offline-or-runtime-fonts}

デフォルトでは、ラスタライズされたグリフ（glyph）の画像への変換はビルド時（オフライン）に行われます。この方式には、各フォントが使用する可能性のあるすべてのグリフをビルド段階でラスタライズする必要があるという欠点があります。そのため、非常に大きなテクスチャが生成され、メモリを消費するとともに、バンドルサイズも増大する可能性があります。

「ランタイムフォント（runtime font）」を使うと、`.ttf` および `.otf` フォントはそのままバンドルに同梱され、実行時に必要に応じてラスタライズされます。これにより、実行時のメモリ使用量とバンドルサイズの両方を最小限に抑えられます。

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

![新しいフォント](images/font/new_font.png)

使用するフォントを *Assets* ブラウザーにドラッグし、適切な場所にドロップします。

*Font* プロパティにフォントファイルを設定し、必要に応じてフォントのプロパティを設定します。

## プロパティ {#properties}

*Font*
: フォントデータの生成に使う TTF、OTF、または *`.fnt`* ファイルです。

*Material*
: このフォントの描画に使うマテリアル（material）です。距離フィールドフォントと BMFont の場合は、この設定を変更してください（詳細は後述します）。

*Output Format*
: 生成するフォントデータの種類です。

  - `TYPE_BITMAP` は、インポートした OTF または TTF ファイルをフォントシートテクスチャに変換し、そのビットマップデータを使ってテキストノードを描画します。カラーチャンネルには、文字本体の形状、アウトライン、ドロップシャドウがエンコードされます。*`.fnt`* ファイルの場合は、元のテクスチャビットマップをそのまま使います。
  - `TYPE_DISTANCE_FIELD` は、インポートしたフォントをフォントシートテクスチャに変換します。このテクスチャのピクセルデータは、画面のピクセルではなく、フォントの輪郭までの距離を表します。詳細は後述します。

*Render Mode*
: グリフの描画に使うレンダーモードです。

  - `MODE_SINGLE_LAYER` は、各文字に1つの四角形ポリゴンを生成します。
  - `MODE_MULTI_LAYER` は、グリフの形状、アウトライン、影にそれぞれ別の四角形ポリゴンを生成します。レイヤーは奥から手前の順に描画されるため、アウトラインの幅がグリフ間の距離より大きくても、先に描画した文字を後の文字が覆い隠すのを防げます。このレンダーモードでは、フォントリソースの Shadow X/Y プロパティに従って、ドロップシャドウの位置を適切にずらすこともできます。

*Size*
: グリフの目標サイズ（ピクセル単位）です。

*Antialias*
: 対象のビットマップに焼き込む際に、フォントにアンチエイリアスを適用するかどうかです。ピクセルパーフェクトなフォント描画が必要な場合は、0に設定します。

*Alpha*
: グリフの透明度です。範囲は 0.0--1.0 で、0.0は透明、1.0は不透明を意味します。

*Outline Alpha*
: 生成するアウトラインの透明度です。範囲は 0.0--1.0 です。

*Outline Width*
: 生成するアウトラインの幅（ピクセル単位）です。アウトラインを付けない場合は、0に設定します。

*Shadow Alpha*
: 生成する影の透明度です。範囲は 0.0--1.0 です。

::: sidenote
組み込みのフォントマテリアルのシェーダー（shader）が影のサポートを提供しており、単一レイヤーと複数レイヤーの両方のレンダーモードに対応しています。レイヤーを使ったフォント描画や影のサポートが不要な場合は、*`builtins/font-singlelayer.fp`* などの、より単純なシェーダーを使うことをお勧めします。
:::

*Shadow Blur*
: ビットマップフォントの場合、この設定は各グリフに小さなぼかしカーネルを適用する回数を示します。距離フィールドフォントの場合、この設定はぼかしの実際の幅（ピクセル単位）に相当します。

*Shadow X/Y*
: 生成する影の水平方向と垂直方向のオフセット（ピクセル単位）です。この設定は、Render Mode が `MODE_MULTI_LAYER` の場合にのみ、グリフの影に影響します。

*Characters*
: フォントに含める文字です。デフォルトでは、このフィールドに ASCII の印字可能文字（文字コード32-126）が含まれています。このフィールドの文字を追加または削除すると、フォントに含める文字を増減できます。

ランタイムフォントの場合、このテキストを使って、必要なグリフをキャッシュに事前に用意します。この処理は読み込み時に行われます。`font.prewarm_text()` を参照してください。

::: sidenote
ASCII の印字可能文字は次のとおりです。
スペース ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ \` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
:::

*All Chars*
: このプロパティにチェックを入れると、元のファイルにあるすべてのグリフが出力に含まれます。

*Cache Width/Height*
: グリフキャッシュのビットマップのサイズを制限します。エンジンはテキストを描画するときに、キャッシュのビットマップからグリフを検索します。そこに存在しなければ、描画前にキャッシュへ追加します。描画を要求されたすべてのグリフを格納するにはキャッシュのビットマップが小さすぎる場合、エラーが通知されます（`ERROR:RENDER: Out of available cache cells! Consider increasing cache_width or cache_height for the font.`）。

  0に設定するとキャッシュサイズは自動で設定され、最大 2048x4096 まで拡大します。

## 距離フィールドフォント {#distance-field-fonts}

距離フィールドフォントは、ビットマップデータの代わりに、グリフの輪郭までの距離をテクスチャに格納します。エンジンがフォントを描画するには、距離データを解釈し、それを使ってグリフを描画する専用のシェーダーが必要です。距離フィールドフォントはビットマップフォントより多くのリソースを消費しますが、サイズ変更の自由度が高くなります。

![距離フィールドフォント](images/font/df_font.png)

フォントを作成する際は、フォントの *Material* プロパティを *`builtins/fonts/font-df.material`*（または距離フィールドデータを扱える別のマテリアル）に変更してください。変更しないと、画面への描画時に正しいシェーダーが使われません。

## ビットマップの BMFont {#bitmap-bmfonts}

Defold は、生成したビットマップに加え、あらかじめ焼き込まれたビットマップの「BMFont」形式のフォントをサポートしています。この形式のフォントは、すべてのグリフを含む PNG フォントシートで構成されます。さらに、*`.fnt`* ファイルには、各グリフのシート上の位置と、サイズやカーニングの情報が含まれています。（Defold は、Phaser などのツールが使用する *`.fnt`* 形式の XML 版をサポートしていません。）

この形式のフォントには、TrueType や OpenType フォントファイルから生成したビットマップフォントに対するパフォーマンス上の利点はありませんが、任意のグラフィックス、色、影を画像に直接含められます。

生成した *`.fnt`* ファイルと *`.png`* ファイルを Defold プロジェクトに追加します。これらのファイルは同じフォルダーに配置してください。新しいフォントファイルを作成し、*font* プロパティに *`.fnt`* ファイルを設定します。*output_format* が `TYPE_BITMAP` に設定されていることを確認してください。Defold はビットマップを生成せず、PNG で提供されたものを使います。

::: sidenote
BMFont を作成するには、適切なファイルを生成できるツールを使う必要があります。次のような選択肢があります。

* [Bitmap Font Generator](http://www.angelcode.com/products/bmfont/) は、AngelCode が提供する Windows 専用のツールです。
* [Shoebox](http://renderhjs.net/shoebox/) は、Windows と macOS 向けの、Adobe Air を基盤とする無料アプリです。
* [Hiero](https://libgdx.com/wiki/tools/hiero) は、Java を基盤とするオープンソースのツールです。
* [Glyph Designer](https://71squared.com/glyphdesigner) は、71 Squared が提供する macOS 向けの有料ツールです。
* [bmGlyph](https://www.bmglyph.com) は、Sovapps が提供する macOS 向けの有料ツールです。
:::

![BMFont](images/font/bm_font.png)

フォントが正しく描画されるように、フォントを作成する際は、マテリアルプロパティを *`builtins/fonts/font-fnt.material`* に設定することを忘れないでください。

## 描画の乱れとベストプラクティス {#artifacts-and-best-practices}

一般に、拡大縮小せずにフォントを描画する場合は、ビットマップフォントが最適です。距離フィールドフォントより高速に画面へ描画できます。

距離フィールドフォントは、拡大しても良好な表示を維持できます。一方、ビットマップフォントはピクセルで構成された画像なので、フォントを拡大するとピクセルも大きくなり、ブロック状の乱れが生じます。次は、フォントサイズ48ピクセルのサンプルを4倍に拡大したものです。

![拡大したフォント](images/font/scale_up.png)

縮小する場合、ビットマップテクスチャは GPU によってきれいかつ効率よく縮小され、アンチエイリアスを適用できます。ビットマップフォントは、距離フィールドフォントよりも色をよく維持します。次は、同じサイズ48ピクセルのサンプルフォントを1/5のサイズに縮小したものの拡大表示です。

![縮小したフォント](images/font/scale_down.png)

距離フィールドフォントは、グリフの曲線を表現できる距離情報を保持するのに十分な目標サイズで描画する必要があります。次は、上と同じフォントを18ピクセルのサイズで作成し、10倍に拡大したものです。この書体の形状をエンコードするには、このサイズが小さすぎることがはっきりと分かります。

![距離フィールドの描画の乱れ](images/font/df_artifacts.png)

影やアウトラインのサポートが不要な場合は、それぞれのアルファ値を0に設定します。そうしないと、影やアウトラインのデータが生成され、不要なメモリを消費します。

## フォントキャッシュ {#font-cache}
Defold のフォントリソースは、実行時にテクスチャとフォントデータの2つになります。

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

TrueType（`.ttf`）または OpenType（`.otf`）フォントを使用する場合、SDF 形式のフォントを実行時に生成できます。`.otf` リソースからの実行時生成は Defold 1.13.2 以降でサポートされています。
この方式により、Defold ゲームのダウンロードサイズと実行時のメモリ消費量を大幅に削減できます。
小さな欠点として、各グリフの生成が非同期処理になることが挙げられます。

* game.project の `font.runtime_generation` を設定して、この機能を有効にします。

* [アプリケーションマニフェスト（App Manifest）](/manuals/app-manifest)を追加し、`Use full text layout system` オプションを有効にします。
これにより、この機能を有効にしたカスタムエンジンがビルドされます。

::: sidenote
この機能は現在実験的なものですが、将来はデフォルトのワークフローとして使用することを意図しています。
:::

::: important
`font.runtime_generation` 設定は、プロジェクト内のすべての `.ttf` および `.otf` フォントに影響します。
:::


### フォントのスクリプティング {#font-scripting}

#### グリフキャッシュの事前準備 {#prewarming-glyph-cache}

ランタイムフォントを使いやすくするため、グリフキャッシュを事前に準備する機能をサポートしています。
これは、フォントの *Characters* に列挙されたグリフを生成するということです。

::: sidenote
`All Chars` が選択されている場合は、事前準備を行いません。すべてのグリフを同時に生成せずに済むという目的に反するためです。
:::

`Characters` フィールドが `.fontc` ファイルで設定されている場合は、その内容をテキストとして使い、グリフキャッシュ内で更新する必要があるグリフを判定します。

`font.prewarm_text(font_collection, text, callback)` を呼び出して、グリフキャッシュを手動で更新することもできます。この関数は、不足しているグリフがすべてグリフキャッシュに追加され、テキストを画面に表示できる状態になったことを通知するコールバックを提供します。

### フォントコレクションへのフォントの追加と削除 {#addingremoving-fonts-to-a-font-collection}

ランタイムフォントでは、フォントコレクションにフォント（`.ttf`）を追加したり、そこから削除したりできます。
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
