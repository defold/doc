## ダウンロード {#downloading}

[Defold のダウンロードページ](https://defold.com/download/)を開きます。macOS、Windows、Linux（Ubuntu）向けの Download ボタンがあります。

![エディターのダウンロード](../shared/images/editor_download.png)

## インストール {#installation}

macOS へのインストール
: ダウンロードしたファイルは、プログラムを含む DMG イメージです。

  1. ファイル「Defold-x86_64-macos.dmg」を見つけ、ダブルクリックしてイメージを開きます。
  2. アプリケーション「Defold」を「Applications」フォルダーへのリンクにドラッグします。

  エディターを起動するには、「Applications」フォルダーを開き、ファイル「Defold」を <kbd>ダブルクリック</kbd>します。

  ![macOS 版 Defold](../shared/images/macos_content.png)

Windows へのインストール
: ダウンロードしたファイルは ZIP アーカイブなので、展開する必要があります。

  1. アーカイブファイル「Defold-x86_64-win32.zip」を見つけ、フォルダーを <kbd>押し続けて</kbd>（または <kbd>右クリック</kbd>して）*Extract All* を選択し、指示に従って「Defold」という名前のフォルダーにアーカイブを展開します。
  2. フォルダー「Defold」を任意の場所（たとえば `D:\Defold`）に移動します。Defold を `C:\Program Files (x86)\` や `C:\Program Files\` に移動すると、エディターを更新できなくなるため、これらの場所への移動は避けてください。

  エディターを起動するには、フォルダー「Defold」を開き、ファイル「Defold.exe」を <kbd>ダブルクリック</kbd>します。

  ![Windows 版 Defold](../shared/images/windows_content.png)

Linux へのインストール
: ダウンロードしたファイルは ZIP アーカイブなので、展開する必要があります。

  1. ターミナルでアーカイブファイル「Defold-x86_64-linux.zip」を見つけ、「Defold」という名前の展開先ディレクトリに展開します。

     ```bash
     $ unzip Defold-x86_64-linux.zip -d Defold
     ```

  エディターを起動するには、アプリケーションを展開したディレクトリに移動して実行可能ファイル `Defold` を実行するか、デスクトップでそのファイルを <kbd>ダブルクリック</kbd>します。

  ```bash
  $ cd Defold
  $ ./Defold
  ```

  `Help > Create Desktop Entry` メニューには、デスクトップエントリをインストールするための補助機能があります。

  エディターの起動、プロジェクトを開く操作、Defold のゲームの実行で問題が発生した場合は、[FAQ の Linux に関するセクション](/faq/faq#linux-questions)を参照してください。

## 古いバージョンのインストール {#install-an-old-version}

Defold のすべてのベータ版と安定版は、[GitHub からも入手できます](https://github.com/defold/defold/releases)。
