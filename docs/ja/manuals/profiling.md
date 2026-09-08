---
title: Defold のプロファイリング
brief: このマニュアルでは、Defold に用意されているプロファイリング機能について説明します。
---

# プロファイリング {#profiling}

Defold には、エンジンとビルドパイプラインに統合されたプロファイリングツールが含まれています。パフォーマンス、メモリ、リソース使用量の問題を見つけるのに役立ちます。実行時のプロファイリングデータは、いくつかの機能で利用できます。

* 基本プロファイラーとゲーム内ビジュアルプロファイラーは、すべてのプラットフォームで利用できます。
* [Remotery プロファイラー](https://github.com/Celtoys/Remotery)と対話型 Web フレームプロファイラーは、デスクトップとモバイルのプラットフォームで利用できます。
* HTML5 ビルドでは、Defold のスコープをブラウザーの Web Performance API に出力できます。

[アプリケーションマニフェスト（App Manifest）](/manuals/app-manifest/#profiler)の **Profiler** 設定で、プロファイラーのコードをビルドにリンクするかどうかを制御します。既定値は **Debug Only** で、**None** はコードを除外し、**Always** はデバッグビルドとリリースビルドの両方にコードを含めます。*game.project* の `profiler` 設定は実行時の動作を制御しますが、除外されたプロファイラーのコードをビルドに再びリンクすることはありません。特に、**Track CPU** は CPU 使用率のサンプリングを制御する設定で、App Manifest の選択とは別です。

## 実行時のビジュアルプロファイラー {#the-runtime-visual-profiler}

プロファイラーのサポートを含むビルドには、実行中のアプリケーションにリアルタイムの情報を重ねて表示する、実行時のビジュアルプロファイラーが用意されています。

```lua
function on_reload(self)
    -- Toggle the visual profiler on hot reload.
    profiler.enable_ui(true)
end
```

![ビジュアルプロファイラー](images/profiling/visual_profiler.png)

ビジュアルプロファイラーには、データの表示方法を変更できる関数がいくつか用意されています。

```lua

profiler.set_ui_mode()
profiler.set_ui_view_mode()
profiler.view_recorded_frame()
```

プロファイラーの関数について詳しくは、[profiler API リファレンス](/ref/stable/profiler/)を参照してください。

## Web プロファイラー {#the-web-profiler}
プロファイラーのサポートを含むデスクトップまたはモバイル向けビルドの実行中は、ブラウザーから対話型のフレームプロファイラーとリソースプロファイラーにアクセスできます。

### Remotery フレームプロファイラー {#remotery-frame-profiler}
フレームプロファイラーでは、実行中のゲームをサンプリングし、個々のフレームを詳しく分析できます。プロファイラーにアクセスする手順は次のとおりです。

1. 対象デバイスでゲームを起動します。
2. <kbd> Debug ▸ Open Web Profiler</kbd> メニューを選択します。

フレームプロファイラーはいくつかのセクションに分かれており、それぞれが実行中のゲームを異なる観点から表示します。右上の Pause ボタンを押すと、プロファイラーによるビューの更新を一時停止できます。

![Web プロファイラー](images/profiling/webprofiler_page.png)

::: sidenote
複数のターゲットを同時に使用している場合は、ページ上部の Connection Address フィールドを変更して、手動でターゲットを切り替えられます。このフィールドには、ターゲットの起動時にコンソールに表示された Remotery プロファイラーの URL を指定します。

```
INFO:ENGINE: Defold Engine 1.3.4 (80b1b73)
INFO:DLIB: Initialized Remotery (ws://127.0.0.1:17815/rmt)
INFO:ENGINE: Loading data from: build/default
```
:::

Sample Timeline
: Sample Timeline には、エンジンで取得したフレームのデータが、スレッドごとに1本の水平なタイムラインとして表示されます。Main は、すべてのゲームロジックとエンジンコードの大部分を実行するメインスレッドです。Remotery はプロファイラー自体のスレッドで、Sound はサウンドのミキシングと再生を行うスレッドです。マウスホイールで拡大・縮小でき、個々のフレームを選択すると、Frame Data ビューでそのフレームの詳細を確認できます。

  ![サンプルタイムライン](images/profiling/webprofiler_sample_timeline.png)


Frame Data
: Frame Data ビューは、現在選択しているフレームのすべてのデータを詳しく分類して表示する表です。エンジンの各スコープに何ミリ秒かかっているかを確認できます。

  ![フレームデータ](images/profiling/webprofiler_frame_data.png)


Global Properties
: Global Properties ビューには、カウンターの表が表示されます。たとえば、ドローコール数や特定の種類のコンポーネント（component）の数を簡単に追跡できます。

  ![グローバルプロパティ](images/profiling/webprofiler_global_properties.png)

::: sidenote
LuaMem の値は、Lua ガベージコレクターが報告する、Lua VM のメモリ使用量をキロバイト単位で示したものです。Memory は、エンジンのメモリ使用量をキロバイト単位で示します。
:::

::: important
[Max Sample Count 設定](/manuals/project-settings/#max-sample-count)は、1フレームでスレッドごとに記録するプロファイラーのサンプル数を制限します。プロファイラーが上限を超えたことを報告した場合は、まずネイティブ拡張（native extension）のプロファイリングコードで、スコープの開始と終了が対になっているかを確認してください。正常なフレームに含まれるスコープ数が設定された上限を超える場合に限り、上限を引き上げてください。
:::

### リソースプロファイラー {#resource-profiler}
リソースプロファイラーでは、実行中のゲームを調べ、リソースの使用状況を詳しく分析できます。プロファイラーにアクセスする手順は次のとおりです。

1. 対象デバイスでゲームを起動します。
2. ブラウザーを開き、http://localhost:8002 にアクセスします。

リソースプロファイラーは2つのセクションに分かれています。一方は現在ゲーム内でインスタンス化されているコレクション（collection）、ゲームオブジェクト（game object）、コンポーネントの階層を表示し、もう一方は現在読み込まれているすべてのリソースを表示します。

![リソースプロファイラー](images/profiling/webprofiler_resources_page.png)

コレクションビュー
: コレクションビューには、現在ゲーム内でインスタンス化されているすべてのゲームオブジェクトとコンポーネントが階層リストとして表示され、それらがどのコレクションから生成されたかも示されます。任意の時点でゲーム内に何のインスタンスが存在し、それらのオブジェクトがどこから生成されたかを詳しく調べて理解するのに、とても便利なツールです。

リソースビュー
: リソースビューには、現在メモリに読み込まれているすべてのリソースと、そのサイズ、各リソースの参照数が表示されます。アプリケーションのメモリ使用量を最適化する際に、任意の時点で何がメモリに読み込まれているかを把握するのに役立ちます。

## HTML5 ブラウザーのパフォーマンスタイムライン {#html5-browser-performance-timeline}

HTML5 では、ブラウザーのタイムラインに Remotery の代わりに Web Performance API を使用します。Defold のスコープを記録する手順は次のとおりです。

1. 選択した App Manifest のプロファイラーモードが、実行するビルドバリアントにプロファイラーのサポートを含むことを確認します。
2. *game.project* で **Performance Timeline Enabled**（`profiler.performance_timeline_enabled`）を有効にします。
3. HTML5 ビルドを起動し、ブラウザーの開発者ツールを開きます。
4. ブラウザーの **Performance** パネルでセッションを記録し、生成されたタイムラインで Defold のスコープを調べます。

このブラウザーのタイムラインは、ゲーム内のビジュアルプロファイラーとも、対話型の Remotery Web プロファイラーとも別の機能です。


## ビルドレポート {#build-reports}
ゲームのバンドルを作成するときに、ビルドレポートを作成するオプションがあります。ゲームのバンドルに含まれるすべてのアセットのサイズを把握するのに、とても役立ちます。ゲームのバンドルを作成するときに、*Generate build report* チェックボックスをオンにするだけです。

![ビルドレポート](images/profiling/build_report.png)

ビルダーは、ゲームのバンドルと同じ場所に `report.html` というファイルを生成します。このファイルを Web ブラウザーで開いて、レポートを確認します。

![ビルドレポート](images/profiling/build_report_html.png)

*Overview* は、リソースの種類別にプロジェクトサイズ全体の内訳を視覚的に表示します。

*Resources* は、リソースの詳細なリストを表示します。このリストは、サイズ、圧縮率、暗号化、種類、ディレクトリ名で並べ替えられます。「search」フィールドを使用すると、表示するリソースの項目を絞り込めます。

*Structure* セクションは、プロジェクトのファイル構造におけるリソースの配置に基づいてサイズを表示します。各項目は、ファイルとディレクトリの内容の相対的なサイズに応じて、緑（小さい）から青（大きい）まで色分けされます。


## 外部ツール {#external-tools}
組み込みツールに加えて、無料で高品質なトレースツールやプロファイリングツールが数多くあります。以下にその一部を紹介します。

ProFi (Lua)
: Defold には Lua プロファイラーが組み込まれていませんが、手軽に利用できる外部ライブラリがあります。スクリプトのどこに時間がかかっているかを調べるには、コードに自分で時間計測を挿入するか、[ProFi](https://github.com/jgrahamc/ProFi)のような Lua プロファイリングライブラリを使用します。

  純粋な Lua で実装されたプロファイラーは、設定するフックごとにかなりのオーバーヘッドが発生する点に注意してください。そのため、このようなツールで得られた時間の計測結果は、少し慎重に扱う必要があります。ただし、回数の計測結果には十分な精度があります。

Instruments（macOS と iOS）
: Xcode の一部として提供される、パフォーマンスの分析・可視化ツールです。1つ以上のアプリケーションやプロセスの動作をトレースして調べたり、Wi-Fi や Bluetooth などのデバイス固有の機能を調べたりと、さまざまなことができます。

  ![Instruments](images/profiling/instruments.png)

OpenGL プロファイラー（macOS）
: Apple からダウンロードできる「Additional Tools for Xcode」パッケージの一部です（Xcode のメニューで <kbd>Xcode ▸ Open Developer Tool ▸ More Developer Tools...</kbd> を選択します）。

  このツールでは、実行中の Defold アプリケーションを調べ、OpenGL の使用状況を確認できます。OpenGL 関数呼び出しのトレース、OpenGL 関数へのブレークポイントの設定、アプリケーションのリソース（テクスチャ、プログラム、シェーダーなど）の調査、バッファーの内容の確認、その他の OpenGL の状態の確認ができます。

  ![OpenGL プロファイラー](images/profiling/opengl.png)

Android Profiler (Android)
: https://developer.android.com/studio/profile/android-profiler.html

  ゲームの CPU、メモリ、ネットワークの動作に関するリアルタイムデータを取得する、プロファイリングツール群です。コードの実行をサンプルベースでメソッドトレースしたり、ヒープダンプを取得したり、メモリ割り当てを表示したり、ネットワーク経由で送信されたファイルの詳細を調べたりできます。このツールを使用するには、`AndroidManifest.xml` で `android:debuggable="true"` を設定する必要があります。

  ![Android プロファイラー](images/profiling/android_profiler.png)

  注: Android Studio 4.1 以降では、[Android Studio を起動せずにプロファイリングツールを実行する](https://developer.android.com/studio/profile/android-profiler.html#standalone-profilers)こともできます。

Graphics API Debugger (Android)
: https://github.com/google/gapid

  アプリケーションからグラフィックスドライバーへの呼び出しを調査、調整、再実行できるツール群です。このツールを使用するには、`AndroidManifest.xml` で `android:debuggable="true"` を設定する必要があります。

  ![グラフィックス API デバッガー](images/profiling/gapid.png)
