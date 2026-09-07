---
title: コレクションファクトリーマニュアル
brief: このマニュアルでは、コレクションファクトリーコンポーネントを使ってゲームオブジェクトの階層を生成する方法を説明します。
---

# コレクションファクトリー {#collection-factories}

コレクションファクトリー（collection factory）コンポーネント（component）は、コレクション（collection）ファイルに保存されたゲームオブジェクト（game object）のグループや階層を、実行中のゲーム内に生成するために使います。

コレクションは、Defold で再利用可能なテンプレート、つまり「プレハブ（prefab）」を作成するための強力な仕組みです。コレクションの概要については、[基本要素のドキュメント](/manuals/building-blocks#collections)を参照してください。コレクションはエディターで配置することも、ゲーム内に動的に挿入することもできます。

コレクションファクトリーコンポーネントを使うと、コレクションファイルの内容をゲームワールド（game world）内に生成できます。これは、コレクション内のすべてのゲームオブジェクトをファクトリー（factory）で生成し、その後でオブジェクト間の親子階層を構築することに相当します。典型的な用途は、複数のゲームオブジェクトで構成された敵（たとえば、敵と武器）を生成することです。

## コレクションの生成 {#spawning-a-collection}

キャラクターのゲームオブジェクトと、その子となる別の盾のゲームオブジェクトが必要だとします。コレクションファイルでゲームオブジェクトの階層を構築し、`bean.collection` として保存します。

::: sidenote
*コレクションプロキシ（collection proxy）* コンポーネントは、コレクションに基づいて、独立した物理ワールドを含む新しいゲームワールドを作成するために使います。新しいワールドには、新しいソケットを通じてアクセスします。プロキシに読み込み開始のメッセージを送信すると、コレクションに含まれるすべてのアセットがプロキシを通じて読み込まれます。このため、たとえばゲームのレベルを切り替える際に非常に便利です。ただし、新しいゲームワールドにはかなりのオーバーヘッドがあるため、小さなものを動的に読み込むためには使わないでください。詳しくは、[コレクションプロキシのドキュメント](/manuals/collection-proxy)を参照してください。
:::

![生成するコレクション](images/collection_factory/collection.png)

次に、生成を担当するゲームオブジェクトに *Collection factory* を追加し、コンポーネントの *Prototype* に `bean.collection` を設定します。

![コレクションファクトリー](images/collection_factory/factory.png)

これで、`collectionfactory.create()` 関数を呼び出すだけで `bean` と盾を生成できます。

```lua
local bean_ids = collectionfactory.create("#bean_factory")
```

この関数は5つのパラメーターを受け取ります。

`url`
: 新しいゲームオブジェクトのセットを生成するコレクションファクトリーコンポーネントの識別子です。

`[position]`
: （省略可能）生成されるゲームオブジェクトのワールド座標での位置です。`vector3` を指定します。位置を指定しない場合、オブジェクトはコレクションファクトリーコンポーネントの位置に生成されます。

`[rotation]`
: （省略可能）新しいゲームオブジェクトのワールド空間での回転です。`quat` を指定します。

`[properties]`
: （省略可能）生成されるゲームオブジェクトを初期化するための `id`-`table` のペアを持つ Lua テーブルです。このテーブルの構築方法は後述します。

`[scale]`
: （省略可能）生成されるゲームオブジェクトのスケールです。スケールは、すべての軸に沿った均一な拡大縮小を指定する `number`（0より大きい値）で表せます。各成分が対応する軸に沿った拡大縮小を指定する `vector3` を渡すこともできます。

`collectionfactory.create()` は、生成されたゲームオブジェクトの識別子をテーブルとして返します。このテーブルは、各オブジェクトのコレクション内での識別子のハッシュ値をキーとして、各オブジェクトの実行時の識別子に対応付けます。

::: sidenote
`bean` と `shield` の親子関係は、返されるテーブルに *反映されません*。この関係は、実行時のシーングラフ、つまりオブジェクトがどのように一緒に変換されるかという関係にのみ存在します。オブジェクトの親を変更しても、その識別子が変わることはありません。
:::

```lua
local bean_ids = collectionfactory.create("#bean_factory")
go.set_scale_xy(0.5, bean_ids[hash("/bean")])
pprint(bean_ids)
-- DEBUG:SCRIPT:
-- {
--   hash: [/shield] = hash: [/collection0/shield], -- <1>
--   hash: [/bean] = hash: [/collection0/bean],
-- }
```
1. 各インスタンスを一意に識別するために、識別子に `/collection[N]/` という接頭辞が追加されます。ここで `[N]` はカウンターです。

## プロパティ {#properties}

コレクションを生成するとき、キーがオブジェクトの識別子、値が設定するスクリプトプロパティを持つテーブルになるようにテーブルを構築すると、各ゲームオブジェクトにプロパティのパラメーターを渡せます。

```lua
local props = {}
props[hash("/bean")] = { shield = false }
local ids = collectionfactory.create("#bean_factory", nil, nil, props)
```

`bean.collection` 内のゲームオブジェクト `bean` が `shield` プロパティを定義しているとします。スクリプトプロパティについては、[スクリプトプロパティマニュアル](/manuals/script-properties)で説明しています。

```lua
-- bean/controller.script
go.property("shield", true)

function init(self)
    if not self.shield then
        go.delete("shield")
    end     
end
```

## ファクトリーリソースの動的な読み込み {#dynamic-loading-of-factory-resources}

コレクションファクトリーのプロパティで *Load Dynamically* チェックボックスをオンにすると、エンジンはファクトリーに関連するリソースの読み込みを遅らせます。

![動的な読み込み](images/collection_factory/load_dynamically.png)

チェックボックスがオフの場合、エンジンはコレクションファクトリーコンポーネントが読み込まれるときにプロトタイプ（prototype）のリソースを読み込むため、すぐに生成できる状態になります。

チェックボックスがオンの場合は、次の2つの使い方があります。

同期読み込み
: オブジェクトを生成したいときに [`collectionfactory.create()`](/ref/collectionfactory/#collectionfactory.create:url-[position]-[rotation]-[properties]-[scale]) を呼び出します。これによりリソースが同期的に読み込まれ、その後で新しいインスタンスが生成されます。同期読み込みによって一時的に処理が止まることがあります。

  ```lua
  function init(self)
      -- No factory resources are loaded when the collection factory’s
      -- parent collection is loaded. Calling create without
      -- having called load will create the resources synchronously.
      self.go_ids = collectionfactory.create("#collectionfactory")
  end

  function final(self)  
      -- Delete game objects. Will decref resources.
      -- In this case resources are deleted since the collection
      -- factory component holds no reference.
      go.delete(self.go_ids)

      -- Calling unload will do nothing since factory holds
      -- no references
      collectionfactory.unload("#factory")
  end
  ```

非同期読み込み
: [`collectionfactory.load()`](/ref/collectionfactory/#collectionfactory.load:[url]-[complete_function]) を呼び出して、リソースを明示的に非同期で読み込みます。リソースを生成に使える状態になると、コールバックが呼び出されます。

  ```lua
  function load_complete(self, url, result)
      -- Loading is complete, resources are ready to spawn
      self.go_ids = collectionfactory.create(url)
  end

  function init(self)
      -- No factory resources are loaded when the collection factory’s
      -- parent collection is loaded. Calling load will load the resources.
      collectionfactory.load("#factory", load_complete)
  end

  function final(self)
      -- Delete game object. Will decref resources.
      -- In this case resources aren’t deleted since the collection factory
      -- component still holds a reference.
      go.delete(self.go_ids)

      -- Calling unload will decref resources held by the factory component,
      -- resulting in resources being destroyed.
      collectionfactory.unload("#factory")
  end
  ```


## 動的なプロトタイプ {#dynamic-prototype}

コレクションファクトリーのプロパティで *Dynamic Prototype* チェックボックスをオンにすると、コレクションファクトリーが生成する *Prototype* を変更できます。

![動的なプロトタイプ](images/collection_factory/dynamic_prototype.png)

*Dynamic Prototype* オプションがオンの場合、コレクションファクトリーコンポーネントは `collectionfactory.set_prototype()` 関数を使ってプロトタイプを変更できます。例:

```lua
collectionfactory.unload("#factory") -- unload the previous resources
collectionfactory.set_prototype("#factory", "/main/levels/level1.collectionc")
local ids = collectionfactory.create("#factory")
```

::: important
*Dynamic Prototype* オプションが設定されている場合、コレクションのコンポーネント数を最適化できず、このコンポーネントを所有するコレクションは *game.project* ファイルの既定のコンポーネント数を使います。
:::
