---
title: エディターの概要
brief: このマニュアルでは、Defold エディターの外観や動作、各画面の移動方法を紹介します。
---

# エディターの概要 {#editor-overview}

エディターでは、ゲームプロジェクト内のすべてのファイルとフォルダーを効率よく閲覧、操作できます。ファイルを編集すると、そのファイルに適したエディターが開き、関連するすべての情報が個別のビューに表示されます。

## エディターの起動 {#starting-the-editor}

Defold エディターを実行すると、プロジェクトを選択、作成する画面が表示されます。実行したい操作をクリックして選択します。

MY PROJECTS
: 最近開いたプロジェクトが表示され、すぐにアクセスできます。起動画面の既定のビューです。

  これまでにプロジェクトを開いていない場合（またはすべて削除した場合）は、2つのボタンが表示されます。`Open From Disk…` をクリックすると、システムのファイルブラウザーでプロジェクトを探して開けます。`Create New Project` ボタンをクリックすると、`TEMPLATES` タブに切り替わります。

  ![自分のプロジェクト](images/editor/start_no_projects.png)


  以前にプロジェクトを開いたことがある場合は、次の画像のようにプロジェクトの一覧が表示されます。

  ![自分のプロジェクト](images/editor/start_my_projects.png)

TEMPLATES
: 特定のプラットフォーム向け、または特定の拡張を使う新しい Defold プロジェクトをすぐに始められるように作られた、空またはほぼ空の基本的なプロジェクトが用意されています。


TUTORIALS
: チュートリアルに沿って進めたい場合に、手順を見ながら学び、遊び、変更できるチュートリアル付きのプロジェクトが用意されています。


SAMPLES
: 特定の使用例を紹介するためのプロジェクトが用意されています。

  ![新しいプロジェクト](images/editor/start_templates.png)

新しいプロジェクトを作成すると、ローカルドライブに保存され、編集内容もすべてローカルに保存されます。

各選択肢について詳しくは、[プロジェクトのセットアップマニュアル](https://www.defold.com/manuals/project-setup/)を参照してください。

## エディターの言語 {#editor-language}

起動画面の左下には言語の選択欄があり、現在利用できる言語から選択できます。エディター内の `File ▸ Preferences ▸ General ▸ Editor Language` からも選択できます。

![言語](images/editor/languages.png)

## エディターのペイン {#the-editor-views}

Defold エディターは、特定の情報を表示する複数のペイン（ビュー）に分かれています。

![エディター 2](images/editor/editor_overview.png)

### 1. Assets ペイン {#1-assets-pane}
プロジェクトに含まれるすべてのファイルとフォルダーを、ディスク上と同じツリー構造で一覧表示します。クリックやスクロールで一覧を移動できます。このビューでは、ファイルに関するすべての操作を実行できます。

   - <kbd>左クリック</kbd>でファイルやフォルダーを選択します。<kbd>⇧ Shift</kbd> を押しながら操作すると選択範囲を広げられ、<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> を押しながら操作すると、クリックした項目の選択と選択解除を切り替えられます。
   - ファイルを<kbd>ダブルクリック</kbd>すると、そのファイル形式専用のエディターで開きます。
   - <kbd>ドラッグ＆ドロップ</kbd>で、ディスク上のほかの場所からプロジェクトにファイルを追加したり、プロジェクト内でファイルやフォルダーを別の場所に移動したりできます。
   - <kbd>右クリック</kbd>で _コンテキストメニュー_ を開き、新しいファイルやフォルダーの作成、名前の変更、削除、ファイルの依存関係の確認などを実行できます。

*Assets* ペインから削除したファイルやフォルダーは、プラットフォームが対応している場合、システムのごみ箱に移動します。ごみ箱への移動に対応していない場合や移動に失敗した場合、エディターはその項目を完全に削除します。

### 2. シーンエディターペイン {#the-scene-editor}

コレクション（collection）、ゲームオブジェクト（game object）、または視覚的なコンポーネント（component）のファイルをダブルクリックすると、シーンの構築と編集に使うビジュアルエディター、*Scene Editor*（シーンエディター）が開きます。スクリプトファイルや、視覚的な要素を持たないその他のリソースは、それぞれの専用エディターで開きます。

![シーンエディター](images/editor/2d_scene.png)

シーンエディターが提供する主な機能には、次のものがあります。

- 正投影と透視投影のカメラモードによる [2D および 3D シーンのナビゲーション](/manuals/scene-editing/#2d-and-3d-scene-orientation)
- オブジェクトの移動、回転、スケール変更に使う[トランスフォームツール](/manuals/scene-editing/#manipulating-objects)
- 一人称視点で 3D 空間を移動するための[フリーカメラモード](/manuals/scene-editing/#free-camera-mode)
- サイズ、平面、外観を変更できる[グリッド設定](/manuals/scene-editing/#grid-settings)
- コンポーネントの種類やガイドの表示を切り替える[表示フィルター](/manuals/scene-editing/#visibility-filters)

詳しくは、[シーンエディターのマニュアル](/manuals/scene-editing/)を参照してください。

### 3. Outline ペイン {#3-outline-pane}

このビューは、現在編集中のファイルの内容を階層的なツリー構造で表示します。Outline はエディタービューの内容を反映し、項目に対して次の操作を実行できます。

   - <kbd>左クリック</kbd>で項目を選択します。<kbd>⇧ Shift</kbd> を押しながら操作すると選択範囲を広げられ、<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> を押しながら操作すると、クリックした項目の選択と選択解除を切り替えられます。
   - <kbd>ドラッグ＆ドロップ</kbd>で項目を移動します。コレクション内のゲームオブジェクトを別のゲームオブジェクトにドロップすると、親子関係を作成できます。
   - <kbd>右クリック</kbd>で _コンテキストメニュー_ を開き、項目の追加、選択した項目の削除などを実行できます。

一覧の各要素の右側にある小さな `👁` の目のアイコンをクリックすると、ゲームオブジェクトや視覚的なコンポーネントの表示を切り替えられます。

![アウトライン](images/editor/outline.png)

### 4. Properties ペイン {#4-properties-pane}

このビューは、現在選択されている項目に関連するプロパティを表示します。Id、URL、Position、Rotation、Scale のほか、コンポーネント固有のプロパティや、スクリプトのカスタムプロパティも表示します。

`↕` の上下矢印を<kbd>ドラッグ</kbd>してマウスを動かすと、対応する数値プロパティの値を変更できます。

![プロパティ](images/editor/properties.png)

### 5. Tools ペイン {#5-tools-pane}

このビューには複数のタブがあります。

*Console* タブ : ゲームの実行中にエンジンが出力するエラー、警告、情報、および自分で意図的に出力した内容を表示します。

*Build Errors* : ビルド処理のエラーを表示します。

*Search Results* : プロジェクト全体を検索（<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd> + <kbd>F</kbd>）したときに、`Keep Results` をクリックすると検索結果を表示します。

*Curve Editor* : [パーティクルエディター](/manuals/particlefx/)でカーブを編集するときに使用します。

Tools ペインは、統合デバッガーの操作にも使用します。詳しくは、[デバッグマニュアル](/manuals/debugging/)を参照してください。

### 6. Changed Files ペイン {#6-changed-files-pane}

プロジェクトで Git を使用している場合、このビューは現在のコミット（`HEAD`）と比較して、ローカルで変更、追加、名前の変更、削除が行われたファイルを一覧表示します。リモートリポジトリとの同期には、外部の Git クライアントまたはコマンドラインを使用します。詳しくは、[バージョン管理マニュアル](/manuals/version-control/)を参照してください。このビューでは、ファイルに関する次の操作を実行できます。

   - <kbd>左クリック</kbd> - ファイルを選択します。<kbd>⇧ Shift</kbd> を押しながら操作すると選択範囲を広げられ、<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> を押しながら操作すると、クリックした項目の選択と選択解除を切り替えられます。変更されたファイルを1つ選択している場合、`Diff` をクリックすると差分を表示できます。`Revert` をクリックすると、選択したすべてのファイルの変更を元に戻せます。
   - ファイルを<kbd>左ダブルクリック</kbd>すると、ファイルのビューが開きます。エディターは Assets ビューと同様に、そのファイルに適したエディターで開きます。
   - ファイルを<kbd>右クリック</kbd>するとポップアップメニューが開き、差分ビューを開く、ファイルへのすべての変更を元に戻す、ファイルシステム上でファイルを見つけるなどの操作ができます。

### メニューバー {#menu-bar}

エディタービューの上部、または Mac のシステムバーには、`File`、`Edit`、`View`、`Project`、`Debug`、`Help` の6つのメニューを含むメニューバーがあります。各機能については、それぞれのマニュアルで説明します。

### ステータスバー {#status-bar}

エディターの下部には、次のような状態を表示する細い領域があります。
- 新しい更新が利用できる場合は、クリックできる `Update Available` ボタンが表示されます。このマニュアルの後半にある「エディターの更新」の節を参照してください。
- ビルド中やバンドル作成中は、ここに進行状況が表示されます。

## ペインのサイズと表示 {#panes-size-and-visibility}

エディター内で、上記の6つのペインを区切る境界線を<kbd>ドラッグ</kbd>すると、ペインのサイズを調整できます。

エディターの `View` メニューの項目、または次のショートカットを使うと、ペインの表示を切り替えられます。
- `Toggle Assets Pane`（<kbd>F6</kbd>）で、Assets ペインと Changed Files ペインの表示を切り替えます。
- `Toggle Changed Files` で、Changed Files ペインだけの表示を切り替えます。
- `Toggle Tools Pane`（<kbd>F7</kbd>）で、Tools ペインの表示を切り替えます。
- `Toggle Properties Pane`（<kbd>F8</kbd>）で、Outline ペインと Properties ペインの表示を切り替えます。

![ペインの表示](images/editor/editor_panes.png)

`View` メニューでは、Grid、Guides、Camera などの表示に関するほかの設定の切り替えや変更、選択内容にビューを合わせる操作（`Frame Selection` または <kbd>F</kbd> キー）、既定の 2D ビューと 3D ビューの切り替え（`Realign Camera` または <kbd>.</kbd> キー）もできます。これらの多くは、ツールバーやショートカットからも操作できます。

## タブ {#tabs}

複数のファイルを開いている場合、エディタービューの上部にファイルごとのタブが表示されます。同じペイン内のタブは、<kbd>ドラッグ＆ドロップ</kbd>でタブバー内の位置を入れ替えられます。また、次の操作もできます。

- タブを<kbd>右クリック</kbd>して _コンテキストメニュー_ を開きます。
- `Close`（<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>W</kbd>）をクリックして、1つのタブを閉じます。
- `Close Others` をクリックして、選択したタブ以外をすべて閉じます。
- `Close All`（<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd>+<kbd>W</kbd>）をクリックして、アクティブなペイン内のすべてのタブを閉じます。
- `➝| Open As` を選択して、既定以外のエディター、または `File ▸ Preferences ▸ Code ▸ Custom Editor` で設定した関連付け済みの外部ツールを使用します。詳しくは、[環境設定マニュアル](/manuals/editor-preferences)を参照してください。

![タブ](images/editor/tabs_custom.png)

## 左右に並べて編集する {#side-by-side-editing}

2つのエディタービューを左右に並べて開けます。

- 移動したいエディターのタブを<kbd>右クリック</kbd>し、`Move to Other Tab Pane` を選択します。

![2つのペイン](images/editor/2-panes.png)

タブのメニューで `Swap with Other Tab Pane` を使用してタブをペイン間で移動したり、`Join Tab Panes` を使用して1つのペインにまとめたりすることもできます。

## 新しいプロジェクトファイルの作成 {#creating-new-project-files}

新しいリソースファイルを作成するには、`File ▸ New…` を選択してからメニューでファイル形式を選択するか、コンテキストメニューを使用します。

`Assets` ブラウザー内の作成先を<kbd>右クリック</kbd>し、`New… ▸ [file type]` を選択します。

![ファイルの作成](images/editor/create_file.png)

新しいファイルの適切な名前を *Name* に入力し、必要に応じて *Location* を変更します。ダイアログの *Preview* に、ファイル形式の拡張子を含む完全なファイル名が表示されます。

![作成するファイルの名前](images/editor/create_file_name.png)

## テンプレート {#templates}

プロジェクトごとにカスタムテンプレートを指定できます。プロジェクトのルートディレクトリに `templates` という名前の新しいフォルダーを作成し、必要な拡張子を使った `default.*` という名前の新しいファイルを追加します。たとえば、`/templates/default.gui` や `/templates/default.script` です。また、これらのファイル内で `{{NAME}}` トークンを使用すると、ファイル作成ウィンドウで指定したファイル名に置き換えられます。

あるファイル形式のテンプレートが用意されている場合、その形式のファイルを新しく作成するたびに、`templates` 内のファイルの内容で初期化されます。


![テンプレート](images/editor/templates.png)

## プロジェクトへのファイルのインポート {#importing-files-to-your-project}

アセット（asset）のファイル（画像、音声、モデルなど）をプロジェクトに追加するには、*Assets* ブラウザー内の適切な場所にドラッグ＆ドロップします。プロジェクトのファイル構造内で選択した場所に、ファイルの _コピー_ が作成されます。詳しくは、[アセットのインポート方法を説明するマニュアル](/manuals/importing-assets/)を参照してください。

![ファイルのインポート](images/editor/import.png)

## エディターの更新 {#updating-the-editor}

エディターは、インターネットに接続していると自動的に更新を確認します。更新が見つかると、プロジェクト選択画面の左下、またはエディターウィンドウの右下に、クリックできる青い `Update Available` リンクが表示されます。

![プロジェクト選択画面からの更新](images/editor/update_start.png)
![エディターからの更新](images/editor/update_available.png)

`Update Available` リンクをクリックして、ダウンロードと更新を行います。情報を記載した確認ウィンドウが開くので、`Download Update` をクリックして続行します。

![エディター更新のポップアップ](images/editor/update.png)

下部のステータスバーにダウンロードの進行状況が表示されます。

![ダウンロードの進行状況](images/editor/download_status.png)

更新のダウンロードが完了すると、青いリンクが `Restart to Update` に変わります。クリックすると、再起動して更新後のエディターが開きます。

![再起動して更新](images/editor/restart_to_update.png)

## 環境設定 {#preferences}

`Preferences` ウィンドウでエディターの設定を変更できます。開くには、`File ▸ Preferences…` をクリックするか、ショートカット <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>,</kbd> を使用します。

詳しくは、[環境設定マニュアル](/manuals/editor-preferences)を参照してください。

![環境設定](images/editor/preferences.png)

## エディターのログ {#editor-logs}
エディターで問題が発生し、問題を報告（`Help  ▸ Report Issue`）する必要がある場合は、エディター自身のログファイルを添えることをお勧めします。システムのファイルブラウザーでログの保存場所を開くには、`Help ▸ Show Logs` をクリックします。

詳しくは、[ヘルプを得るためのマニュアル](/manuals/getting-help/#getting-help)を参照してください。

![ログの表示](images/editor/show_logs.png)

エディターのログファイルは、次の場所にあります。

  * Windows: `C:\Users\ **Your Username** \AppData\Local\Defold`
  * macOS: `/Users/ **Your Username** /Library/Application Support/` または `~/Library/Application Support/Defold`
  * Linux: `$XDG_STATE_HOME/Defold` または `~/.local/state/Defold`

ターミナルやコマンドプロンプトからエディターを起動した場合は、エディターの実行中にもログを確認できます。エディターを起動するには、次のコマンドを使用します。

```shell
# Linux:
$ ./path/to/Defold/Defold

# macOS:
$ > ./path/to/Defold.app/Contents/MacOS/Defold
```

## エディターサーバー {#editor-server}

エディターはプロジェクトを開くと、ランダムなポートで Web サーバーを起動します。このサーバーを使用して、ほかのアプリケーションからエディターを操作できます。ポートは `.internal/editor.port` ファイルに書き込まれます。

サーバーは `http://localhost:$(cat .internal/editor.port)/openapi.json` で OpenAPI 仕様を提供します。これは、エージェントを活用したワークフローを始める際の最小限の出発点として役立ちます。

また、エディターの実行ファイルには、起動時にポートを指定できるコマンドラインオプション `--port`（または `-p`）があります。たとえば次のように指定します::
```shell
# Windows
.\path\to\Defold\Defold.exe --port 8181

# Linux:
./path/to/Defold/Defold --port 8181

# macOS:
./path/to/Defold/Defold.app/Contents/MacOS/Defold --port 8181
```

## エディターのインストールメタデータ {#editor-installation-metadata}

エディターは起動時に、ランチャーとインストール先のパスに関する情報を、定められた場所に書き込みます。サードパーティーの IDE 連携機能やほかのツールは、この情報を使ってインストール済みの Defold エディターを見つけられます。

| OS      | 場所 |
|---------|----------|
| macOS   | `~/Library/Application Support/Defold/installations.json` |
| Linux   | `${XDG_STATE_HOME:-~/.local/state}/Defold/installations.json` |
| Windows | `%LOCALAPPDATA%\Defold\installations.json` |

ファイルには、既知のインストールごとに1つのオブジェクトを含む JSON 配列が格納されます。

```json
[
  {
    "launcherPath": "/Applications/Defold.app/Contents/MacOS/Defold",
    "installPath": "/Applications/Defold.app",
    "lastLaunchedAt": "2026-07-06T12:34:56.789Z"
  }
]
```

## エディターのスタイル設定 {#editor-styling}

カスタムのスタイル設定で、エディターの外観を変更できます。詳しくは、[エディターのスタイル設定マニュアル](/manuals/editor-styling)を参照してください。

## よくある質問 {#faq}
:[Editor FAQ](../shared/editor-faq.md)
