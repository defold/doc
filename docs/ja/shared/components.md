コンポーネント（component）は、ゲームオブジェクト（game object）に特定の表現や機能を与えるために使用します。コンポーネントはゲームオブジェクト内に含まれている必要があり、コンポーネントを含むゲームオブジェクトの位置、回転、スケールの影響を受けます:

![コンポーネント](../shared/images/components.png)

多くのコンポーネントには、操作できる種類固有のプロパティがあります。また、実行時にコンポーネントを操作するための、種類ごとの関数が用意されています:

```lua
-- disable the can "body" sprite
msg.post("can#body", "disable")

-- play "hoohoo" sound on "bean" in 1 second
sound.play("bean#hoohoo", { delay = 1, gain = 0.5 } )
```

コンポーネントは、ゲームオブジェクト内にその場で追加（in-place）するか、コンポーネントファイルへの参照としてゲームオブジェクトに追加します:

*Outline* ビューでゲームオブジェクトを <kbd>右クリック</kbd> し、<kbd>Add Component</kbd>（その場で追加）または <kbd>Add Component File</kbd>（ファイルへの参照として追加）を選択します。

ほとんどの場合、コンポーネントはその場で作成するのが最も適しています。ただし、次の種類のコンポーネントは、ゲームオブジェクトに参照として追加する前に、別のリソースファイルで作成する必要があります:

* スクリプト（Script）
* GUI
* パーティクルエフェクト（Particle FX）
* タイルマップ（Tile Map）
