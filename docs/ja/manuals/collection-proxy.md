---
title: コレクションプロキシのマニュアル
brief: このマニュアルでは、新しいゲームワールドを動的に作成し、それらを切り替える方法を説明します。
---

# コレクションプロキシ {#collection-proxy}

コレクションプロキシ（collection proxy）コンポーネント（component）は、コレクション（collection）ファイルの内容に基づいて、新しい「ゲームワールド」（game world）を動的に読み込み、アンロード（読み込んだデータの解放）するために使います。ゲームのレベルや GUI 画面の切り替え、レベル内での物語の「シーン」の読み込みとアンロード、ミニゲームの読み込みとアンロードなどを実装できます。

Defold はすべてのゲームオブジェクト（game object）をコレクションにまとめます。コレクションには、ゲームオブジェクトやほかのコレクション（サブコレクション）を含めることができます。コレクションプロキシを使うと、コンテンツを個別のコレクションに分割し、スクリプトでそれらの読み込みとアンロードを動的に管理できます。

コレクションプロキシは、[コレクションファクトリー（collection factory）コンポーネント](/manuals/collection-factory/)とは異なります。コレクションファクトリーは、コレクションの内容を現在のゲームワールドにインスタンス化します。コレクションプロキシは実行時に新しいゲームワールドを作成するため、用途が異なります。

## コレクションプロキシコンポーネントの作成 {#creating-a-collection-proxy-component}

1. ゲームオブジェクトを <kbd>右クリック</kbd> し、コンテキストメニューから <kbd>Add Component ▸ Collection Proxy</kbd> を選択して、ゲームオブジェクトにコレクションプロキシコンポーネントを追加します。

2. *Collection* プロパティに、あとでランタイムに動的に読み込むコレクションを指定します。これはビルド時の静的な依存関係です。参照したコレクションとその依存リソースはコンパイルされます。*Exclude* にチェックを入れない限り、それらはメインバンドルに含まれます。*Exclude* にチェックを入れると、除外したプロキシからのみ参照されるリソースを Live Update 用にメインバンドルから省略できます。また、後述する方法で、読み込まれていないプロキシの参照先を実行時に別のコンパイル済みコレクションへ変更できます。

![プロキシコンポーネントの追加](images/collection-proxy/create_proxy.png)

（*Exclude* チェックボックスにチェックを入れ、[Live Update 機能](/manuals/live-update/)を使うと、コンテンツをビルドから除外し、代わりにコードでダウンロードできます。）

## ブートストラップ {#bootstrap}

Defold エンジンが起動すると、起動時に読み込まれる *ブートストラップコレクション（bootstrap collection）* からすべてのゲームオブジェクトをランタイムに読み込み、インスタンス化します。その後、ゲームオブジェクトとそのコンポーネントを初期化して有効にします。エンジンが使うブートストラップコレクションは、[プロジェクト設定](/manuals/project-settings/#main-collection)で指定します。慣例として、このコレクションファイルには通常 `main.collection` という名前を付けます。

![ブートストラップ](images/collection-proxy/bootstrap.png)

ゲームオブジェクトとそのコンポーネントを格納するため、エンジンは、ブートストラップコレクションの内容がインスタンス化される「ゲームワールド」全体に必要なメモリを割り当てます。衝突判定や物理特性を持つコンポーネントであるコリジョンオブジェクト（collision object）と物理シミュレーションのために、個別の物理ワールド（physics world）も作成されます。

スクリプトコンポーネントは、ブートストラップのワールドの外側からでもゲーム内のすべてのオブジェクトをアドレス指定できる必要があります。そのため、このワールドには一意の名前が付けられます。その名前は、コレクションファイルで設定する *Name* プロパティです。

![ブートストラップ](images/collection-proxy/collection_id.png)

読み込まれるコレクションにコレクションプロキシコンポーネントが含まれている場合、それらが参照するコレクションは自動的には読み込まれ*ません*。これらのリソースの読み込みは、スクリプトで制御する必要があります。

## コレクションの読み込み {#loading-a-collection}

プロキシ経由でコレクションを動的に読み込むには、スクリプトからプロキシコンポーネントに `"load"` というメッセージを送信します。

```lua
-- Tell the proxy "myproxy" to start loading.
msg.post("#myproxy", "load")
```

![読み込み](images/collection-proxy/proxy_load.png)

プロキシコンポーネントは、新しいワールドのための領域を割り当てるようエンジンに指示します。個別のランタイム物理ワールドも作成され、「`mylevel.collection`」コレクション内のすべてのゲームオブジェクトがインスタンス化されます。

新しいワールドの名前には、コレクションファイルの *Name* プロパティが使われます。この例では「`mylevel`」に設定されています。名前は一意である必要があります。コレクションファイルで設定した *Name* が、読み込み済みのワールドですでに使われていると、エンジンは名前の衝突エラーを出力します。

```txt
ERROR:GAMEOBJECT: The collection 'default' could not be created since there is already a socket with the same name.
WARNING:RESOURCE: Unable to create resource: build/default/mylevel.collectionc
ERROR:GAMESYS: The collection /mylevel.collectionc could not be loaded.
```

エンジンがコレクションの読み込みを完了すると、コレクションプロキシコンポーネントは、`"load"` メッセージを送信したスクリプトに `"proxy_loaded"` というメッセージを返します。スクリプトは、このメッセージに応じてコレクションを初期化し、有効にできます。

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        -- New world is loaded. Init and enable it.
        msg.post(sender, "init")
        msg.post(sender, "enable")
        ...
    end
end
```

`"load"`
: このメッセージは、コレクションを新しいワールドに読み込み始めるよう、コレクションプロキシコンポーネントに指示します。完了すると、プロキシは `"proxy_loaded"` というメッセージを返します。

`"async_load"`
: このメッセージは、コレクションを新しいワールドにバックグラウンドで読み込み始めるよう、コレクションプロキシコンポーネントに指示します。完了すると、プロキシは `"proxy_loaded"` というメッセージを返します。

`"init"`
: このメッセージは、インスタンス化されたすべてのゲームオブジェクトとコンポーネントを初期化するよう、コレクションプロキシコンポーネントに指示します。この段階で、すべてのスクリプトの `init()` 関数が呼び出されます。

`"enable"`
: このメッセージは、すべてのゲームオブジェクトとコンポーネントを有効にするよう、コレクションプロキシコンポーネントに指示します。たとえば、すべてのスプライトコンポーネントは有効になると描画を始めます。

## 除外したプロキシのコレクションの変更 {#changing-an-excluded-proxys-collection}

[`collectionproxy.set_collection()`](/ref/collectionproxy/#collectionproxy.set_collection) を使うと、除外されていて読み込まれていないプロキシの参照先を、コンパイル済みコレクションへ変更できます。これは、Live Update パッケージをマウントしたあとに役立ちます。プロキシは *Exclude* にチェックが入っている必要があり、読み込み済みでも読み込み中でもあってはいけません。パスの末尾は `.collectionc` である必要があります。プロキシを読み込むときには、コレクションとそのすべての依存リソースがリソースシステムで利用できる必要があります。

プロキシを読み込む前に戻り値を確認してください。新しいワールドの初期化と有効化は、`proxy_loaded` を受信してから行ってください。

```lua
local function load_mounted_level()
    local ok, result = collectionproxy.set_collection(
        "#level_proxy",
        "/level_pack/level_3.collectionc"
    )

    if ok then
        msg.post("#level_proxy", "load")
    else
        print("Unable to change proxy collection", result)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

エディターで割り当てたコレクションに戻すには、プロキシが読み込み済みでも読み込み中でもない状態で `collectionproxy.set_collection("#level_proxy", nil)` を呼び出します。コンテンツのダウンロードとマウントについては [Live Update スクリプティングマニュアル](/manuals/live-update-scripting/)を、`collectionproxy.RESULT_*` の失敗コードについては API リファレンスを参照してください。

## 新しいワールド内のアドレス指定 {#addressing-into-the-new-world}

コレクションファイルのプロパティで設定した *Name* は、読み込まれたワールド内のゲームオブジェクトとコンポーネントのアドレス指定に使われます。たとえば、ブートストラップコレクションにローダーオブジェクトを作成した場合、読み込まれた任意のコレクションからそのオブジェクトと通信する必要があるかもしれません。

```lua
-- tell the loader to load the next level:
msg.post("main:/loader#script", "load_level", { level_id = 2 })
```

![読み込み](images/collection-proxy/message_passing.png)

ローダーから、読み込まれたコレクション内のゲームオブジェクトと通信する必要がある場合は、[オブジェクトへの完全な URL](/manuals/addressing/#urls) を使ってメッセージを送信できます。

```lua
msg.post("mylevel:/myobject", "hello")
```

::: important
読み込まれたコレクション内のゲームオブジェクトには、コレクションの外側から直接アクセスできません。

```lua
local position = go.get_position("mylevel:/myobject")
-- loader.script:42: function called can only access instances within the same collection.
```
:::


## ワールドのアンロード {#unloading-a-world}

読み込んだコレクションをアンロードするには、読み込みとは逆の手順に対応するメッセージを送信します。

```lua
-- unload the level
msg.post("#myproxy", "disable")
msg.post("#myproxy", "final")
msg.post("#myproxy", "unload")
```

`"disable"`
: このメッセージは、ワールド内のすべてのゲームオブジェクトとコンポーネントを無効にするよう、コレクションプロキシコンポーネントに指示します。この段階で、スプライトの描画が停止します。

`"final"`
: このメッセージは、ワールド内のすべてのゲームオブジェクトとコンポーネントの終了処理を行うよう、コレクションプロキシコンポーネントに指示します。この段階で、すべてのスクリプトの `final()` 関数が呼び出されます。

`"unload"`
: このメッセージは、ワールドをメモリから完全に削除するよう、コレクションプロキシに指示します。

細かな制御が必要なければ、コレクションを先に無効にしたり終了処理を行ったりせずに、`"unload"` メッセージを直接送信できます。その場合、プロキシはコレクションをアンロードする前に、自動的に無効にして終了処理を行います。

コレクションプロキシがコレクションのアンロードを完了すると、`"unload"` メッセージを送信したスクリプトに `"proxy_unloaded"` メッセージを返します。

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_unloaded") then
        -- Ok, the world is unloaded...
        ...
    end
end
```


## タイムステップ {#time-step}

コレクションプロキシの更新速度は、更新やシミュレーションの時間刻みである _タイムステップ（time step）_ を変更することで調整できます。つまり、ゲームが一定の 60 FPS で進んでいても、プロキシはより速い、または遅いペースで更新でき、次のようなものに影響します。

* 物理シミュレーションの速度
* `update()` に渡される `dt`
* [ゲームオブジェクトと GUI のプロパティアニメーション](https://defold.com/manuals/animation/#property-animation-1)
* [フリップブックアニメーション（flipbook animation、連続した画像を切り替える方式）](https://defold.com/manuals/animation/#flip-book-animation)
* [パーティクルエフェクトのシミュレーション](https://defold.com/manuals/particlefx/)
* タイマーの速度

更新モードも設定できます。これにより、速度の調整を離散的に行うか（スケール係数が 1.0 未満の場合にのみ意味があります）、連続的に行うかを制御できます。

プロキシに `set_time_step` メッセージを送信して、スケール係数と調整モードを制御します。

```lua
-- update loaded world at one-fifth-speed.
msg.post("#myproxy", "set_time_step", {factor = 0.2, mode = 1}
```

タイムステップを変更すると何が起こるかを確認するため、スクリプトコンポーネントに次のコードを持つオブジェクトを作成し、タイムステップを変更するコレクションに配置します。

```lua
function update(self, dt)
    print("update() with timestep (dt) " .. dt)
end
```

タイムステップを 0.2 にすると、コンソールに次の結果が表示されます。

```txt
INFO:ENGINE: Defold Engine 1.2.37 (6b3ae27)
INFO:ENGINE: Loading data from: build/default
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
```

`update()` は引き続き1秒あたり60回呼び出されますが、`dt` の値が変わります。`update()` の呼び出しのうち、`dt` が 1/60（60 FPS に相当）になるのは 1/5（0.2）だけで、残りはゼロです。すべての物理シミュレーションもこの `dt` に従って更新され、5フレームに1回だけ進みます。

::: sidenote
コレクションのタイムステップ機能を使うと、たとえばポップアップを表示している間や、ウィンドウがフォーカスを失ったときに、ゲームを一時停止できます。一時停止するには `msg.post("#myproxy", "set_time_step", {factor = 0, mode = 0})` を、再開するには `msg.post("#myproxy", "set_time_step", {factor = 1, mode = 1})` を使います。
:::

詳細は [`set_time_step`](/ref/collectionproxy#set_time_step) を参照してください。

## 注意点とよくある問題 {#caveats-and-common-issues}

物理
: コレクションプロキシを使うと、複数の最上位コレクション、つまり *ゲームワールド* をエンジンに読み込めます。その際、それぞれの最上位コレクションが個別の物理ワールドであることを理解しておく必要があります。物理的な相互作用（衝突、トリガー、レイキャスト）は、同じワールドに属するオブジェクト間でのみ起こります。そのため、2つのワールドのコリジョンオブジェクトが見た目には完全に重なっていても、それらの間で物理的な相互作用は起こりません。

メモリ
: 読み込まれたコレクションはそれぞれ新しいゲームワールドを作成するため、比較的大きなメモリ使用量を伴います。プロキシを使って数十個のコレクションを同時に読み込む場合は、設計を見直すことを検討してください。ゲームオブジェクト階層のインスタンスを多数生成するには、[コレクションファクトリー](/manuals/collection-factory)のほうが適しています。

入力
: 読み込んだコレクション内に入力アクションを必要とするオブジェクトがある場合は、コレクションプロキシを含むゲームオブジェクトが入力を取得するようにする必要があります。ゲームオブジェクトが入力メッセージを受信すると、そのオブジェクトのコンポーネント、つまりコレクションプロキシにメッセージが伝播します。入力アクションはプロキシを経由して、読み込まれたコレクションに送信されます。
