---
title: Defold のアドレス指定
brief: このマニュアルでは、Defold がアドレス指定の問題をどのように解決しているかを説明します。
---

# アドレス指定 {#addressing}

実行中のゲームを制御するコードは、プレイヤーが見たり聞いたりするものを移動、拡大縮小、アニメーション、削除、操作するために、すべてのゲームオブジェクト（game object）とコンポーネント（component）にアクセスできる必要があります。Defold のアドレス指定（addressing）の仕組みがこれを可能にします。

## 識別子 {#identifiers}

Defold はアドレス（URL とも呼びますが、ここではいったん置いておきます）を使ってゲームオブジェクトとコンポーネントを参照します。これらのアドレスは識別子（identifier）で構成されます。以下はいずれも、Defold でのアドレスの使い方を示す例です。このマニュアルでは、その仕組みを詳しく見ていきます。

```lua
local id = factory.create("#enemy_factory")
label.set_text("my_gameobject#my_label", "Hello World!")

local pos = go.get_position("my_gameobject")
go.set_position(pos, "/level/stuff/other_gameobject")

msg.post("#", "hello_there")
local id = go.get_id(".")
```

まずはごく簡単な例から始めましょう。1つのスプライト（sprite）コンポーネントを持つゲームオブジェクトがあるとします。また、そのゲームオブジェクトを制御するスクリプトコンポーネント（script component）もあります。エディターでの構成は次のようになります。

![エディターの bean](images/addressing/bean_editor.png)

ここで、後からスプライトを表示できるように、ゲーム開始時にはスプライトを無効にしたいとします。これは、"controller.script" に次のコードを記述するだけで簡単に実現できます。

```lua
function init(self)
    msg.post("#body", "disable") -- <1>
end
```
1. '#' という文字が分からなくても、心配はいりません。これについてはすぐ後で説明します。

このコードは期待どおりに動作します。ゲームが開始すると、スクリプトコンポーネントは識別子 "body" を使ってスプライトコンポーネントの *アドレスを指定* し、そのアドレスを使って "disable" という *メッセージ（message）* を送信します。この特別なエンジンメッセージにより、スプライトコンポーネントはスプライトのグラフィックスを非表示にします。この構成を図にすると、次のようになります。

![bean の構成](images/addressing/bean.png)

この構成の識別子は開発者が定義するもので、それぞれの命名コンテキスト（naming context）内で一意である必要があります。ここでは、ゲームオブジェクトに "bean" という識別子を付け、そのスプライトコンポーネントを "body"、キャラクターを制御するスクリプトコンポーネントを "controller" と名付けています。文字列形式の URL アドレスで使う識別子には、`:` や `#` を含めないでください。URL 構文では、`:` はソケット（socket）の区切り文字、`#` はゲームオブジェクトとコンポーネントの区切り文字として予約されているためです。それ以外の記号は URL パーサーによって拒否されません。

::: sidenote
名前を指定しなければ、エディターが指定します。エディターで新しいゲームオブジェクトやコンポーネントを作成するたびに、一意の *Id* プロパティが自動的に設定されます。

- ゲームオブジェクトには、"go"、およびそれに連番を付けた識別子（"go2"、"go3" など）が自動的に設定されます。
- コンポーネントには、コンポーネントの種類に対応する識別子（"sprite"、"sprite2" など）が設定されます。

自動的に割り当てられた名前をそのまま使ってもかまいませんが、内容がよく分かる適切な名前に識別子を変更することをお勧めします。
:::

次に、もう1つスプライトコンポーネントを追加して、bean に盾を持たせてみましょう。

![bean の構成](images/addressing/bean_shield_editor.png)

新しいコンポーネントは、ゲームオブジェクト内で一意に識別できる必要があります。これに "body" という名前を付けると、スクリプトコードでどちらのスプライトに "disable" メッセージを送信すべきかが曖昧になります。そこで、一意で内容も分かる "shield" という識別子を選びます。これで、"body" と "shield" のスプライトを自由に有効化、無効化できます。

![bean の構成](images/addressing/bean_shield.png)

::: sidenote
同じ識別子を複数回使おうとすると、エディターがエラーを表示するため、実際にこれが問題になることはありません。

![bean の構成](images/addressing/name_collision.png)
:::

次に、ゲームオブジェクトを増やすとどうなるかを見てみましょう。2体の「豆」を組み合わせて小さなチームを作りたいとします。一方の豆のゲームオブジェクトを "bean"、もう一方を "buddy" と名付けます。さらに、"bean" がしばらく何もしていないときに、"buddy" にダンスを始めるよう伝えるものとします。これは、"bean" の "controller" スクリプトコンポーネントから "buddy" の "controller" スクリプトに、"dance" というカスタムメッセージを送信して実現します。

![bean の構成](images/addressing/bean_buddy.png)

::: sidenote
"controller" という名前のコンポーネントが、各ゲームオブジェクトに1つずつ、合わせて2つあります。それぞれのゲームオブジェクトが新しい命名コンテキストを作るため、これはまったく問題ありません。
:::

メッセージの受信先は、メッセージを送信するゲームオブジェクト（"bean"）の外にあるため、コードではどちらの "controller" がメッセージを受信すべきかを指定する必要があります。対象のゲームオブジェクトの識別子とコンポーネントの識別子の両方を指定する必要があります。コンポーネントへの完全なアドレスは `"buddy#controller"` となり、このアドレスは2つの部分で構成されます。

- 最初に、対象のゲームオブジェクトの識別子（"buddy"）を記述します。
- 次に、ゲームオブジェクトとコンポーネントの区切り文字（"#"）を記述します。
- 最後に、対象のコンポーネントの識別子（"controller"）を記述します。

ゲームオブジェクトが1つだけの前の例に戻ると、送信先アドレスのゲームオブジェクト識別子の部分を省略することで、コードから *現在のゲームオブジェクト* 内のコンポーネントを指定できることが分かります。

たとえば、`"#body"` は現在のゲームオブジェクト内の "body" コンポーネントへのアドレスを表します。これはとても便利です。"body" コンポーネントさえあれば、このコードは *どの* ゲームオブジェクトでも動作するためです。

## コレクション {#collections}

コレクション（collection）を使うと、ゲームオブジェクトのグループや階層を作成し、管理しながら再利用できます。エディターでゲームにコンテンツを配置するときは、コレクションファイルをテンプレート（「プロトタイプ（prototype）」や「プレハブ（prefab）」とも呼びます）として使います。

bean と buddy のチームを大量に作りたいとします。そのためのよい方法は、新しい *コレクションファイル* にテンプレートを作成することです（"team.collection" と名付けます）。コレクションファイル内にチームのゲームオブジェクトを構成し、保存します。次に、そのコレクションファイルの内容のインスタンス（instance）をメインのブートストラップコレクション（bootstrap collection、起動時に読み込まれるコレクション）に配置し、インスタンスに識別子を付けます（"team_1" と名付けます）。

![bean の構成](images/addressing/team_editor.png)

この構造でも、"bean" ゲームオブジェクトは引き続き `"buddy#controller"` というアドレスで、"buddy" 内の "controller" コンポーネントを参照できます。

![bean の構成](images/addressing/collection_team.png)

さらに "team.collection" の2つ目のインスタンスを追加しても（"team_2" と名付けます）、"team_2" のスクリプトコンポーネント内で実行されるコードは同じように動作します。"team_2" コレクションの "bean" ゲームオブジェクトのインスタンスは、引き続き `"buddy#controller"` というアドレスで、"buddy" 内の "controller" コンポーネントを指定できます。

![bean の構成](images/addressing/teams_editor.png)

## 相対アドレス指定 {#relative-addressing}

`"buddy#controller"` というアドレスが両方のコレクションのゲームオブジェクトで動作するのは、これが *相対* アドレスだからです。"team_1" と "team_2" の各コレクションは、新しい命名コンテキスト、言い換えれば「名前空間（namespace）」を作ります。Defold は、アドレス指定の際にコレクションが作る命名コンテキストを考慮することで、名前の衝突を回避します。

![相対識別子](images/addressing/relative_same.png)

- "team_1" という命名コンテキスト内では、ゲームオブジェクト "bean" と "buddy" は一意に識別されます。
- 同様に、"team_2" という命名コンテキスト内でも、ゲームオブジェクト "bean" と "buddy" は一意に識別されます。

相対アドレス指定では、対象のアドレスを解決するときに、現在の命名コンテキストを先頭に自動的に付加します。これも非常に便利で強力な仕組みです。コードを備えたゲームオブジェクトのグループを作成し、ゲーム全体で効率よく再利用できるためです。

### 省略形 {#shorthands}

Defold には、完全な URL を指定せずにメッセージを送信できる、便利な2つの省略形があります。

:[Shorthands](../shared/url-shorthands.md)

## ゲームオブジェクトのパス {#game-object-paths}

命名の仕組みを正しく理解するために、プロジェクトをビルドして実行するときに何が起こるかを見てみましょう。

1. エディターがブートストラップコレクション（"main.collection"）と、その内容すべて（ゲームオブジェクトと他のコレクション）を読み込みます。
2. コンパイラーが、静的なゲームオブジェクトごとに識別子を作成します。これらは、ブートストラップのルートを起点として、コレクション階層を下り、オブジェクトに至る「パス」として構成されます。各階層に '/' という文字が追加されます。

上の例では、ゲームは次の4つのゲームオブジェクトを持って実行されます。

- /team_1/bean
- /team_1/buddy
- /team_2/bean
- /team_2/buddy

::: sidenote
識別子はハッシュ値として格納されます。ランタイムは、各コレクションの識別子についてハッシュの状態も格納します。この状態を使って相対文字列のハッシュ計算を続け、絶対識別子を生成します。
:::

実行時には、コレクションによるグループ分けは存在しません。特定のゲームオブジェクトが、コンパイル前にどのコレクションに属していたかを調べる方法はありません。また、コレクション内のすべてのオブジェクトを一度に操作することもできません。このような操作が必要なら、コード内で自分で追跡情報を管理することで簡単に対応できます。各オブジェクトの識別子は静的であり、オブジェクトの生存期間中は変わらないことが保証されます。そのため、オブジェクトの識別子を安全に保存し、後で使えます。

## 絶対アドレス指定 {#absolute-addressing}

アドレス指定では、上で説明した完全な識別子を使うこともできます。コンテンツを再利用できるため、ほとんどの場合は相対アドレス指定が適していますが、絶対アドレス指定が必要になる場合もあります。

たとえば、各 bean オブジェクトの状態を追跡する AI マネージャーを作りたいとします。bean は活動状態をマネージャーに報告し、マネージャーはその状態に基づいて戦術的な判断を下し、bean に指示を出します。この場合は、スクリプトコンポーネントを持つマネージャーのゲームオブジェクトを1つ作成し、ブートストラップコレクション内でチームのコレクションと並べて配置するのが理にかなっています。

![マネージャーオブジェクト](images/addressing/manager_editor.png)

そして、各 bean がマネージャーへの状態メッセージの送信を担当します。敵を見つけたら "contact"、攻撃を受けてダメージを負ったら "ouch!" を送信します。これを機能させるために、bean のコントローラースクリプトは絶対アドレス指定を使って、"manager" の "controller" コンポーネントにメッセージを送信します。

'/' で始まるアドレスは、ゲームワールド（game world）のルートから解決されます。これは、ゲーム開始時に読み込まれる *ブートストラップコレクション* のルートに対応します。

マネージャースクリプトの絶対アドレスは `"/manager#controller"` です。この絶対アドレスは、どこで使っても正しいコンポーネントに解決されます。

![チームとマネージャー](images/addressing/teams_manager.png)

![絶対アドレス指定](images/addressing/absolute.png)

## ハッシュ化された識別子 {#hashed-identifiers}

エンジンは、すべての識別子をハッシュ値として格納します。コンポーネントやゲームオブジェクトを引数として取る関数は、すべて文字列、ハッシュ値、URL オブジェクトを受け付けます。アドレス指定に文字列を使う方法は、すでに上で見てきました。

ゲームオブジェクトの識別子を取得すると、エンジンは常にハッシュ化された絶対パスの識別子を返します。

```lua
local my_id = go.get_id()
print(my_id) --> hash: [/path/to/the/object]

local spawned_id = factory.create("#some_factory")
print(spawned_id) --> hash: [/instance42]
```

このような識別子は、文字列の識別子の代わりに使うことも、自分で構築することもできます。ただし、ハッシュ化された識別子はオブジェクトのパス、つまり絶対アドレスに対応する点に注意してください。

::: sidenote
相対アドレスを文字列で指定する必要があるのは、エンジンが現在の命名コンテキスト（コレクション）のハッシュ状態に指定された文字列を加えて、新しいハッシュ識別子を計算するためです。
:::

```lua
local spawned_id = factory.create("#some_factory")
local pos = vmath.vector3(100, 100, 0)
go.set_position(pos, spawned_id)

local other_id = hash("/path/to/the/object")
go.set_position(pos, other_id)

-- This will not work! Relative addresses must be given as strings.
local relative_id = hash("my_object")
go.set_position(pos, relative_id)
```

## URL {#urls}

全体像を理解するために、Defold のアドレスの完全な形式である URL を見てみましょう。

URL はオブジェクトであり、通常は特別な形式の文字列として記述します。一般的な URL は、次の3つの部分で構成されます。

`[socket:][path][#fragment]`

socket
: 対象のゲームワールドを識別します。これは [コレクションプロキシ（collection proxy）](/manuals/collection-proxy) を扱う場合に重要で、その場合は _動的に読み込まれるコレクション_ を識別するために使います。

path
: URL のこの部分には、対象のゲームオブジェクトの完全な識別子が含まれます。

fragment
: 指定したゲームオブジェクト内の対象コンポーネントの識別子です。

上で見てきたように、ほとんどの場合はこの情報の一部、または大部分を省略できます。ソケットを指定する必要はほぼなく、パスは指定することが多いものの、常に必要なわけではありません。別のゲームワールド内の対象を指定する必要がある場合は、URL のソケット部分を指定する必要があります。たとえば、上の "manager" ゲームオブジェクトにある "controller" スクリプトの完全な URL 文字列は次のとおりです。

`"main:/manager#controller"`

また、team_2 内の buddy のコントローラーは次のとおりです。

`"main:/team_2/buddy#controller"`

これらにメッセージを送信できます。

```lua
-- Send "hello" to the manager script and team buddy bean
msg.post("main:/manager#controller", "hello_manager")
msg.post("main:/team_2/buddy#controller", "hello_buddy")
```

## URL オブジェクトの構築 {#constructing-url-objects}

URL オブジェクトは、Lua コードでプログラムから構築することもできます。

```lua
-- Construct URL object from a string:
local my_url = msg.url("main:/manager#controller")
print(my_url) --> url: [main:/manager#controller]
print(my_url.socket) --> 786443 (internal numeric value)
print(my_url.path) --> hash: [/manager]
print(my_url.fragment) --> hash: [controller]

-- Construct URL from parameters:
local my_url = msg.url("main", "/manager", "controller")
print(my_url) --> url: [main:/manager#controller]

-- Build from empty URL object:
local my_url = msg.url()
my_url.socket = "main" -- specify by valid name
my_url.path = hash("/manager") -- specify as string or hash
my_url.fragment = "controller" -- specify as string or hash

-- Post to target specified by URL
msg.post(my_url, "hello_manager!")
```
