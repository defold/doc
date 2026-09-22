---
title: Defold ゲームの実行時パフォーマンスの最適化
brief: このマニュアルでは、Defold ゲームが安定した高いフレームレートで動作するように最適化する方法を説明します。
---

# 実行時の速度を最適化する {#optimizing-runtime-speed}
安定した高いフレームレートで動作させることを目指してゲームを最適化する前に、ボトルネックがどこにあるかを把握する必要があります。ゲームの1フレームで、実際に最も時間がかかっているのは何でしょうか。レンダリングでしょうか。ゲームロジックでしょうか。シーングラフ（scene graph）でしょうか。これを調べるには、組み込みのプロファイリングツールを使うことをお勧めします。[画面上のプロファイラーまたは Web プロファイラー](/manuals/profiling/)でゲームのパフォーマンスをサンプリングし、最適化が必要かどうか、何を最適化するかを判断します。何に時間がかかっているかをよく理解できたら、問題への対処を始められます。

## スクリプトの実行時間を短縮する {#reduce-script-execution-time}
プロファイラーの `Script` スコープに高い値が表示される場合は、スクリプト（script）の実行時間を短縮する必要があります。一般的な目安として、毎フレームに実行するコードはできるだけ少なくすることを心がけてください。毎フレーム `update()` や `on_input()` で大量のコードを実行すると、特に性能の低いデバイスではゲームのパフォーマンスに影響する可能性が高くなります。次のような指針があります。

### 変化に反応するコードパターンを使う {#use-reactive-code-patterns}
コールバックを受け取れる場合は、変更をポーリングしないでください。アニメーションや、エンジンに任せられる処理を手動で実装しないでください（たとえば、手動でアニメーションさせる代わりに `go.animate)()` を使います）。

### ガベージコレクションを減らす {#reduce-garbage-collection}
毎フレーム、Lua テーブルなどの生存期間が短いオブジェクトを大量に作成すると、いずれ Lua のガベージコレクターが起動します。これが起きると、フレーム時間の小さな引っかかりや急増として現れることがあります。可能な場合はテーブルを再利用し、ループなどの構造の中で Lua テーブルを作成することはできる限り避けてください。

### メッセージ ID とアクション ID を事前にハッシュ化する {#prehash-message-and-action-ids}
大量のメッセージを処理する場合や、処理すべき入力イベントが多い場合は、文字列を事前にハッシュ化することをお勧めします。次のコードを見てみましょう。

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("message1") then
        msg.post(sender, hash("message3"))
    elseif message_id == hash("message2") then
        msg.post(sender, hash("message4"))
    end
end
```

上の例では、メッセージを受信するたびにハッシュ化された文字列が再作成されます。ハッシュ化された文字列を一度だけ作成し、メッセージを処理するときにそのハッシュ値を使うことで改善できます。

```lua
local MESSAGE1 = hash("message1")
local MESSAGE2 = hash("message2")
local MESSAGE3 = hash("message3")
local MESSAGE4 = hash("message4")

function on_message(self, message_id, message, sender)
    if message_id == MESSAGE1 then
        msg.post(sender, MESSAGE3)
    elseif message_id == MESSAGE2 then
        msg.post(sender, MESSAGE4)
    end
end
```

### URL を優先して使い、キャッシュする {#prefer-and-cache-urls}
メッセージパッシング（message passing、メッセージによる通信）やその他の方法でゲームオブジェクト（game object）またはコンポーネント（component）をアドレス指定する際は、ID を文字列やハッシュとして渡すことも、URL として渡すこともできます。文字列やハッシュを使った場合は、内部で URL に変換されます。そのため、システムから可能な限り高いパフォーマンスを引き出すには、頻繁に使う URL をキャッシュすることをお勧めします。次の例を見てみましょう。

```lua
    local pos = go.get_position("enemy")
    local pos = go.get_position(hash("enemy"))
    local pos = go.get_position(msg.url("enemy"))
    -- do something with pos
```

3つの例はいずれも、ID が `enemy` のゲームオブジェクトの位置を取得します。1つ目と2つ目の例では、ID（文字列またはハッシュ）が使用前に URL に変換されます。したがって、可能な限り高いパフォーマンスを得るには、URL をキャッシュして使う方がよいことが分かります。

```lua
    function init(self)
        self.enemy_url = msg.url("enemy")
    end

    function update(self, dt)
        local pos = go.get_position(self.enemy_url)
        -- do something with pos
    end
```

## フレームのレンダリングにかかる時間を短縮する {#reduce-time-it-takes-to-render-a-frame}
プロファイラーの `Render` および `Render Script` スコープに高い値が表示される場合は、フレームのレンダリングにかかる時間を短縮する必要があります。フレームのレンダリングにかかる時間を短縮する際には、いくつか考慮すべきことがあります。

* ドローコールを減らします - ドローコールを減らす方法の詳細は、[こちらのフォーラム投稿](https://forum.defold.com/t/draw-calls-and-defold/4674)を参照してください。
* オーバードローを減らします
* シェーダーの複雑さを減らします - GLSL の最適化については、[こちらの Khronos の記事](https://www.khronos.org/opengl/wiki/GLSL_Optimizations)を参照してください。Defold が使う既定のシェーダー（`builtins/materials` にあります）を変更し、`highp` が不要な箇所で低い精度を選ぶこともできます。クロスコンパイルされた GLSL ES シェーダーでは、浮動小数点値の既定の精度は `mediump`、整数の既定の精度は `highp` です。これらの既定値はプロジェクト設定の Shader で変更できます。変数ごとに明示的に指定した精度修飾子が優先されます。[シェーダーの精度に関するドキュメント](/manuals/shader/#precision)を参照してください。

## シーングラフの複雑さを減らす {#reduce-scene-graph-complexity}
プロファイラーの `GameObject` スコープ、特に `UpdateTransform` サンプルに高い値が表示される場合は、シーングラフの複雑さを減らす必要があります。次のような対策があります。

* カリング（culling） - 現在表示されていないゲームオブジェクトとそのコンポーネントを無効にします。表示されているかどうかの判定方法は、ゲームの種類に大きく依存します。2D ゲームでは、矩形領域の外にあるゲームオブジェクトを常に無効にするだけで済むこともあります。物理のトリガーを使ってこれを検出したり、オブジェクトをバケットに分割したりできます。どのオブジェクトを無効または有効にするかが分かったら、各ゲームオブジェクトに `disable` または `enable` メッセージを送信して切り替えます。

## 視錐台カリング {#frustum-culling}
レンダースクリプト（render script）は、定義された境界ボックス（視錐台、frustum）の外にあるゲームオブジェクトのコンポーネントを、自動的にレンダリング対象から除外できます。視錐台カリング（frustum culling）の詳細は、[レンダリングパイプラインのマニュアル](/manuals/render/#frustum-culling)を参照してください。

# プラットフォーム固有の最適化 {#platform-specific-optimizations}

## Android Device Performance Framework
Android Dynamic Performance Framework は、ゲームが Android デバイスの電源システムや温度管理システムとより直接的に連携できるようにする API 群です。Android システム上での動的な挙動を監視し、デバイスが過熱せずに持続できる水準にゲームのパフォーマンスを最適化できます。[Android Dynamic Performance Framework 拡張](https://defold.com/extension-adpf/)を使うと、Android デバイス向けの Defold ゲームのパフォーマンスを監視して最適化できます。
