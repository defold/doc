---
title: Defold ゲームのメモリ使用量の最適化
brief: このマニュアルでは、Defold ゲームのメモリ使用量を最適化する方法を説明します。
---

# メモリ使用量の最適化 {#optimizing-memory-usage}

## テクスチャ圧縮 {#texture-compression}
テクスチャ圧縮を使うと、ゲームアーカイブ内のリソース（resource）のサイズを削減できるだけでなく、圧縮されたテクスチャによって必要な GPU メモリの量も削減できる場合があります。

## 動的な読み込み {#dynamic-loading}
ほとんどのゲームには、少なくとも一部に使用頻度の低いコンテンツがあります。メモリ使用量の観点では、そのようなコンテンツを常にメモリに読み込んでおくのは合理的ではなく、必要に応じて読み込みとアンロード（読み込んだデータの解放）を行うほうが適切です。当然ながら、これには、実行時のメモリを消費してすぐにアクセスできる状態にしておくことと、読み込み時間をかけて読み込むこととのトレードオフがあります。

Defold には、コンテンツを動的に読み込むための方法がいくつかあります。

* [コレクションプロキシ（collection proxy）](/manuals/collection-proxy/)
* [動的なコレクションファクトリー（collection factory）](/manuals/collection-factory/#dynamic-loading-of-factory-resources)
* [動的なファクトリー（factory）](/manuals/factory/#dynamic-loading-of-factory-resources)
* [Live Update](/manuals/live-update/)

## コンポーネントカウンターの最適化 {#optimize-component-counters}
Defold はメモリの断片化を抑えるため、コレクション（collection）の作成時に、コンポーネント（component）とリソースのためのメモリを一度だけ割り当てます。割り当てられるメモリの量は、*game.project* 内の各種コンポーネントカウンターの設定によって決まります。[プロファイラー](/manuals/profiling/) を使ってコンポーネントとリソースの正確な使用状況を把握し、実際のコンポーネント数とリソース数に近い最大値を使うようにゲームを設定します。これにより、ゲームのメモリ使用量を削減できます（コンポーネントの[最大数の最適化](/manuals/project-settings/#component-max-count-optimizations)に関する情報を参照してください）。

## GUI ノード数の最適化 {#optimize-gui-node-count}
GUI ファイル内のノードの最大数を必要な数だけに設定して、GUI ノード（GUI node）数を最適化します。[GUI コンポーネントのプロパティ](https://defold.com/manuals/gui/#gui-properties) の `Current Nodes` フィールドには、その GUI コンポーネントが使用しているノード数が表示されます。

:[HTML5 Optimizations](../shared/optimization-memory-html5.md)

