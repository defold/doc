---
title: Windows プラットフォーム向けの Defold 開発
brief: このマニュアルでは、Windows で Defold アプリケーションをビルドして実行する方法を説明します
---

# Windows 向けの開発 {#windows-development}

Windows プラットフォーム向けの Defold アプリケーション開発では、考慮すべき点はごく少なく、手順もシンプルです。

## プロジェクト設定 {#project-settings}

Windows 固有のアプリケーション設定は、*game.project* 設定ファイルの [Windows セクション](/manuals/project-settings/#windows)で行います。

## アプリケーションアイコン {#application-icon}

Windows ゲームで使用するアプリケーションアイコンは、.ico 形式である必要があります。[ICOConvert](https://www.icoconverter.com/) や [AConvert](https://www.aconvert.com/icon/png-to-ico/) などのオンラインツールを使うと、.png ファイルから .ico ファイルを簡単に作成できます。画像をアップロードし、少なくとも次のアイコンサイズを使用します: 16x16、24x24、32x32、48x48、256x256。

出典: [Microsoft - Windows アプリのアイコンの作成](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-construction#icon-sizes-win32)

### ImageMagick ソフトウェアスイートで .ico ファイルをローカルに作成する {#creating-ico-file-locally-using-imagemagick-software-suite}
[ImageMagick](https://www.imagemagick.org/) は、デジタル画像の編集や加工に使用する、無料のオープンソースソフトウェアスイートです。

1. ImageMagick をインストールします
  * Linux: `apt` を使ってインストールします
```
sudo apt install imagemagick
```
  * Windows: [https://imagemagick.org/script/download.php#windows](https://imagemagick.org/script/download.php#windows) からダウンロードします:
  * macOS: `brew` を使ってインストールします:
```
brew install imagemagick
```

2. PNG アイコンを用意します。
3. [convert](https://www.imagemagick.org/script/convert.php) ツールを使って PNG を ICO に変換します:
```bash
magick icon_256x256px.png -compress None -define icon:auto-resize=256,128,96,64,48,32,24,16 favicon.ico
```



## よくある質問 {#faq}
:[Windows FAQ](../shared/windows-faq.md)
