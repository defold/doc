---
title: エディターのスタイル設定
brief: カスタムスタイルシートを使って、エディターの色、タイポグラフィ、そのほかの外観を変更できます。
---

# エディターのスタイル設定 {#editor-styling}

カスタムスタイルシートを使って、エディターの色、タイポグラフィ、そのほかの外観を変更できます。

* ユーザーのホームディレクトリに `.defold` という名前のフォルダーを作成します。
  * Windows の場合は `C:\Users\**Your Username**\.defold`
  * macOS の場合は `/Users/**Your Username**/.defold`
  * Linux の場合は `~/.defold`
* `.defold` フォルダーに `editor.css` ファイルを作成します。

エディターは起動時にカスタムスタイルシートを読み込み、既定のスタイルに重ねて適用します。エディターはユーザーインターフェースに JavaFX を使用しており、スタイルシートは、ブラウザーでウェブページの要素にスタイル属性を適用する CSS ファイルとほぼ同じです。エディターの既定のスタイルシートは [GitHub で確認できます](https://github.com/defold/defold/tree/editor-dev/editor/styling/stylesheets/base)。

## 色の変更 {#changing-color}

既定の色は [`_palette.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_palette.scss) に定義されており、次のようになっています。

```
* {
	// Background
	-df-background-darker:    derive(#212428, -10%);
	-df-background-dark:      derive(#212428, -5%);
	-df-background:           #212428;
	-df-background-light:     derive(#212428, 10%);
	-df-background-lighter:   derive(#212428, 20%);

	// Component
	-df-component-darker:     derive(#464c55, -20%);
	-df-component-dark:       derive(#464c55, -10%);
	-df-component:            #464c55;
	-df-component-light:      derive(#464c55, 10%);
	-df-component-lighter:    derive(#464c55, 20%);

	// Text & icons
	-df-text-dark:            derive(#b4bac1, -10%);
	-df-text:                 #b4bac1;
	-df-text-selected:        derive(#b4bac1, 20%);

  and so on...
```

基本テーマの色は3つのグループに分かれています（それぞれに暗い色と明るい色のバリエーションがあります）。

* 背景色 - パネル、ウィンドウ、ダイアログの背景色
* コンポーネントの色 - ボタン、スクロールバーのつまみ、テキストフィールドの枠線
* テキストの色 - テキストとアイコン

たとえば、ユーザーのホームディレクトリの `.defold` フォルダーにあるカスタムスタイルシート `editor.css` に次を追加します。

```
* {
	-df-background-darker:    derive(#0a0a42, -10%);
	-df-background-dark:      derive(#0a0a42, -5%);
	-df-background:           #0a0a42;
	-df-background-light:     derive(#0a0a42, 10%);
	-df-background-lighter:   derive(#0a0a42, 20%);
}
```

エディターの外観が次のようになります。

![](images/editor/editor-styling-color.png)


## フォントの変更 {#changing-fonts}

エディターは2つのフォントを使用します。コードと等幅のテキスト（エラー）には `Dejavu Sans Mono` を、それ以外の UI には `Source Sans Pro` を使用します。フォントの定義は主に [`_typography.scss`](https://github.com/defold/defold/blob/editor-dev/editor/styling/stylesheets/base/_typography.scss) にあり、次のようになっています。

```
@font-face {
  src: url("SourceSansPro-Light.ttf");
}

@font-face {
  src: url("DejaVuSansMono.ttf");
}

$default-font-mono: 'Dejavu Sans Mono';
$default-font: 'Source Sans Pro';
$default-font-bold: 'Source Sans Pro Semibold';
$default-font-italic: 'Source Sans Pro Italic';
$default-font-light: 'Source Sans Pro Light';

.root {
    -fx-font-size: 13px;
    -fx-font-family: $default-font;
}

Text.strong {
  -fx-font-family: $default-font-bold;
}

and so on...
```

メインのフォントはルート要素に定義されているため、ほとんどの箇所のフォントを容易に置き換えられます。`editor.css` に次を追加します。

```
@import url('https://fonts.googleapis.com/css2?family=Architects+Daughter&display=swap');

.root {
    -fx-font-family: "Architects Daughter";
}
```

エディターの外観が次のようになります。

![](images/editor/editor-styling-fonts.png)

ウェブフォントの代わりにローカルのフォントを使用することもできます。

```
@font-face {
  font-family: 'Comic Sans MS';
  src: local("cs.ttf");
}

.root {
  -fx-font-family: 'Comic Sans MS';
}
```

::: sidenote
コードエディターのフォントは、エディターの Preferences で個別に定義されています。
:::
