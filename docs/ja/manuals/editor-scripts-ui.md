---
title: "エディタースクリプト: UI"
brief: このマニュアルでは、Lua を使用してエディターに UI 要素を作成する方法を説明します。
---

# エディタースクリプトと UI {#editor-scripts-and-ui}

このマニュアルでは、Lua で記述したエディタースクリプト（editor script）を使用して、エディターに操作可能なダイアログを作成し、リソースを開く方法を説明します。エディタースクリプトを使い始めるには、[エディタースクリプトのマニュアル](/manuals/editor-scripts)を参照してください。エディター API の完全なリファレンスは[こちら](/ref/stable/editor-lua/)にあります。

## 最初の例 {#hello-world}

UI に関するすべての機能は `editor.ui` モジュールにあります。まずは、カスタム UI を持つエディタースクリプトの最も単純な例を示します。
```lua
local M = {}

function M.get_commands()
    return {
        {
            label = "Do with confirmation",
            locations = {"View"},
            run = function()
                local result = editor.ui.show_dialog(editor.ui.dialog({
                    title = "Perform action?",
                    buttons = {
                        editor.ui.dialog_button({
                            text = "Cancel",
                            cancel = true,
                            result = false
                        }),
                        editor.ui.dialog_button({
                            text = "Perform",
                            default = true,
                            result = true
                        })
                    }
                }))
                print('Perform action:', result)
            end
        }
    }
end

return M

```

このコード例は **View → Do with confirmation** コマンドを定義します。実行すると、次のダイアログが表示されます。

![最初の例のダイアログ](images/editor_scripts/perform_action_dialog.png)

最後に、<kbd>Enter</kbd> を押すか、`Perform` ボタンをクリックすると、エディターのコンソールに次の行が表示されます。
```
Perform action:	true
```

## リソースを開く {#opening-resources}

コマンドの `run` 関数から `editor.ui.open_resource()` を呼び出すと、プロジェクトのリソースを開けます。パスは `/` で始まります。ビューを省略すると、リソースの主ビューが選択されます。

```lua
editor.ui.open_resource("/main/main.script")
```

`code` ビューと `text` ビューでは、第3引数にカーソル位置または選択範囲を指定できます。行番号と列番号は `1` から始まり、列を省略すると `1` になります。これらの引数を渡す場合はビューを指定してください。

```lua
editor.ui.open_resource("/main/main.script", "code", { line = 10 })
editor.ui.open_resource("/main/main.script", "code", { line = 10, column = 5 })
```

範囲を選択するには、代わりに `from` と `to` のカーソル位置を指定します。

```lua
editor.ui.open_resource("/main/main.script", "code", {
    from = { line = 10, column = 1 },
    to = { line = 12, column = 1 }
})
```

設定されたリソースビューは、エディターまたは外部アプリケーションで開く場合があります。組み込みの Code ビューと Text ビューは、カーソル位置と選択範囲の引数をサポートします。サポートされるビュー名については、[`editor.ui.open_resource()`](/ref/beta/editor/#editor.ui.open_resource:resource_path-view-args) を参照してください。

## 基本的な概念 {#basic-concepts}

### コンポーネント {#components}

エディターには、組み合わせて目的の UI を作成できるさまざまな UI **コンポーネント（component）** が用意されています。慣例として、すべてのコンポーネントは **プロップス（props）** と呼ばれる1つのテーブルで設定します。コンポーネント自体はテーブルではなく、エディターが UI の作成に使用する **不変のユーザーデータ（immutable userdata）** です。

### プロップス {#props}

**プロップス** は、コンポーネントへの入力を定義するテーブルです。プロップスは不変として扱うことを推奨します。プロップスのテーブルを直接変更してもコンポーネントは再レンダリングされませんが、別のテーブルを使用すると再レンダリングされます。コンポーネントのインスタンスが、前のテーブルと浅い比較で等しくないプロップスのテーブルを受け取ると、UI が更新されます。

### 配置 {#alignment}

コンポーネントに UI 内の領域が割り当てられると、その空間全体を使用します。ただし、コンポーネントの見える部分が引き伸ばされるわけではありません。見える部分は必要な空間を占め、割り当てられた領域内で位置を揃えて配置されます。そのため、ほとんどの組み込みコンポーネントには `alignment` プロップが定義されています。

たとえば、次のラベルコンポーネントを考えます。
```lua
editor.ui.label({
    text = "Hello",
    alignment = editor.ui.ALIGNMENT.RIGHT
})
```
見える部分は `Hello` というテキストで、コンポーネントに割り当てられた領域内で位置を揃えて配置されます。

![配置](images/editor_scripts/alignment.png)

## 組み込みコンポーネント {#built-in-components}

エディターには、組み合わせて UI を構築できるさまざまな組み込みコンポーネントが定義されています。コンポーネントは、レイアウト、データ表示、入力の3つに大きく分類できます。

### レイアウトコンポーネント {#layout-components}

レイアウトコンポーネントは、ほかのコンポーネントを隣り合わせに配置するために使用します。主なレイアウトコンポーネントは **`horizontal`**、**`vertical`**、**`grid`** です。これらのコンポーネントには、**パディング（padding）** や **間隔（spacing）** などのプロップも定義されています。パディングは割り当てられた領域の端からコンテンツまでの空白で、間隔は子同士の間の空白です。

![パディングと間隔](images/editor_scripts/padding_and_spacing.png)

エディターには、パディングと間隔の定数として `small`、`medium`、`large` が定義されています。間隔では、`small` は1つの UI 要素を構成する部分同士の間隔、`medium` は個々の UI 要素同士の間隔、`large` は要素のグループ同士の間隔に使用することを想定しています。間隔の既定値は `medium` です。パディングの値では、`large` はウィンドウの端からコンテンツまでの余白、`medium` は主要な UI 要素の端からの余白、`small` はコンテキストメニューやツールチップ（まだ実装されていません）などの小さな UI 要素の端からの余白を意味します。

**`horizontal`** コンテナーは、子を水平方向に順番に配置し、すべての子の高さを常に利用可能な空間いっぱいに広げます。既定では、各子の幅は最小限に保たれますが、子の `grow` プロップを `true` に設定すると、可能な限り広い空間を占めるようにできます。

**`vertical`** コンテナーは horizontal と同様ですが、軸が入れ替わっています。

最後に、**`grid`** は、表のような2D グリッドに子を配置するコンテナーコンポーネントです。グリッドの `grow` 設定は行や列に適用されるため、子ではなく列の設定テーブルに設定します。また、グリッド内の子は、`row_span` と `column_span` プロップで複数の行や列にまたがるように設定できます。グリッドは、複数の入力項目を持つフォームの作成に便利です。
```lua
editor.ui.grid({
    padding = editor.ui.PADDING.LARGE, -- add padding around dialog edges
    columns = {{}, {grow = true}}, -- make 2nd column grow
    children = {
        {
            editor.ui.label({ 
                text = "Level Name",
                alignment = editor.ui.ALIGNMENT.RIGHT
            }),
            editor.ui.string_field({})
        },
        {
            editor.ui.label({ 
                text = "Author",
                alignment = editor.ui.ALIGNMENT.RIGHT
            }),
            editor.ui.string_field({})
        }
    }
})
```
上記のコードで、次のダイアログフォームが作成されます。

![新しいレベルのダイアログ](images/editor_scripts/new_level_dialog.png)

### データ表示コンポーネント {#data-presentation-components}

エディターには、次のデータ表示コンポーネントが定義されています。

- **`label`** — フォームの入力項目とともに使用することを想定したテキストラベルです。
- **`icon`** — アイコンです。現在表示できるのは、あらかじめ定義された少数のアイコンだけですが、今後はより多くのアイコンを使用できるようにする予定です。
- **`image`** — `/` で始まるプロジェクトリソースのパス、または外部 URL から読み込む画像です。省略可能な `width` と `height` プロップを使用すると、アスペクト比を維持しながら指定した寸法内に画像を収めます。
- **`heading`** — フォームやダイアログなどで、見出しの行を表示するためのテキスト要素です。`editor.ui.HEADING_STYLE` 列挙型には、HTML の `H1`-`H6` 見出しや、エディター固有の `DIALOG` と `FORM` など、さまざまな見出しスタイルが定義されています。
- **`paragraph`** — 段落を表示するためのテキスト要素です。`label` との主な違いは、段落が単語の折り返しに対応していることです。割り当てられた領域の横幅が小さすぎるとテキストが折り返され、ビューに収まらない場合は `"..."` で省略されることがあります。

たとえば、UI にはプロジェクト内の画像とウェブ上の画像の両方を表示できます。

```lua
editor.ui.vertical({
    children = {
        editor.ui.image({
            image = "/builtins/assets/images/logo/logo_256.png",
            width = 64,
            height = 64
        }),
        editor.ui.image({
            image = "https://defold.com/images/assets/monarch-hero.jpg"
        })
    }
})
```

### 入力コンポーネント {#input-components}

入力コンポーネントは、ユーザーが UI を操作するためのものです。すべての入力コンポーネントは、操作の有効・無効を制御する `enabled` プロップをサポートし、操作時にエディタースクリプトへ通知するさまざまなコールバックプロップを定義しています。

静的な UI を作成する場合は、ローカル変数を変更するだけのコールバックを定義すれば十分です。動的な UI や、より高度な操作については、[リアクティビティ](#reactivity)を参照してください。

たとえば、単純で静的な新規ファイル作成ダイアログは、次のように作成できます。
```lua
-- initial file name, will be replaced by the dialog
local file_name = ""
local create_file = editor.ui.show_dialog(editor.ui.dialog({
    title = "Create New File",
    content = editor.ui.horizontal({
        padding = editor.ui.PADDING.LARGE,
        spacing = editor.ui.SPACING.MEDIUM,
        children = {
            editor.ui.label({
                text = "New File Name",
                alignment = editor.ui.ALIGNMENT.CENTER
            }),
            editor.ui.string_field({
                grow = true,
                text = file_name,
                -- Typing callback:
                on_value_changed = function(new_text)
                    file_name = new_text
                end
            })
        }
    }),
    buttons = {
        editor.ui.dialog_button({ text = "Cancel", cancel = true, result = false }),
        editor.ui.dialog_button({ text = "Create File", default = true, result = true })
    }
}))
if create_file then
    print("create", file_name)
end
```
組み込みの入力コンポーネントは次のとおりです。
- **`string_field`**、**`integer_field`**、**`number_field`** は、文字列、整数、数値を編集できる単一行テキストフィールドの種類です。
- **`select_box`** は、あらかじめ定義された選択肢の配列から、ドロップダウンコントロールで選択するために使用します。
- **`check_box`** は、`on_value_changed` コールバックを持つ真偽値の入力フィールドです。
- **`button`** は、ボタンが押されたときに呼び出される `on_press` コールバックを持ちます。
- **`external_file_field`** は、コンピューター上のファイルパスを選択するためのコンポーネントです。テキストフィールドと、ファイル選択ダイアログを開くボタンで構成されます。
- **`resource_field`** は、プロジェクト内のリソースを選択するためのコンポーネントです。

ボタン以外のすべてのコンポーネントでは、コンポーネントに関する問題を表示する `issue` プロップを設定できます。重大度は `editor.ui.ISSUE_SEVERITY.ERROR` または `editor.ui.ISSUE_SEVERITY.WARNING` で、たとえば次のように指定します。
```lua
issue = {severity = editor.ui.ISSUE_SEVERITY.WARNING, message = "This value is deprecated"}
```
問題を指定すると、入力コンポーネントの外観が変わり、問題のメッセージを表示するツールチップが追加されます。

すべての入力コンポーネントと、問題がある場合の各表示のデモを次に示します。

![入力コンポーネント](images/editor_scripts/inputs_demo.png)

### ダイアログ関連のコンポーネント {#dialog-related-components}

ダイアログを表示するには、`editor.ui.show_dialog` 関数を使用する必要があります。この関数には **`dialog`** コンポーネントを渡します。これは、Defold のダイアログの基本構造である `title`、`header`、`content`、`buttons` を定義します。ダイアログコンポーネントは少し特殊です。UI 要素ではなくウィンドウを表すため、ほかのコンポーネントの子として使用できません。ただし、`header` と `content` は通常のコンポーネントです。

ダイアログボタンも特殊で、**`dialog_button`** コンポーネントを使用して作成します。通常のボタンとは異なり、ダイアログボタンには `on_pressed` コールバックがありません。代わりに `result` プロップを定義し、その値がダイアログを閉じたときに `editor.ui.show_dialog` 関数から返されます。ダイアログボタンには、真偽値の `cancel` と `default` プロップも定義されています。`cancel` プロップを持つボタンは、ユーザーが <kbd>Escape</kbd> を押すか、OS の閉じるボタンでダイアログを閉じると作動し、`default` ボタンは、ユーザーが <kbd>Enter</kbd> を押すと作動します。1つのダイアログボタンの `cancel` と `default` プロップを、同時にどちらも `true` に設定してもかまいません。

### ユーティリティコンポーネント {#utility-components}

さらに、エディターには次のユーティリティコンポーネントが定義されています。 
- **`separator`** は、コンテンツのブロックを区切るための細い線です。
- **`scroll`** は、内側のコンポーネントが割り当てられた空間に収まらないときにスクロールバーを表示するラッパーコンポーネントです。

## リアクティビティ {#reactivity}

コンポーネントは **不変のユーザーデータ** なので、作成した後に変更することはできません。では、UI を時間の経過に合わせて変化させるにはどうすればよいでしょうか。それを可能にするのが **リアクティブコンポーネント（reactive component）** です。 

::: sidenote
エディタースクリプトの UI は [React](https://react.dev/) ライブラリから着想を得ているため、リアクティブ UI と React のフックについて知っていると役立ちます。 
:::

最も簡単にいうと、リアクティブコンポーネントは、データ（プロップス）を受け取ってビュー（別のコンポーネント）を返す Lua 関数を持つコンポーネントです。リアクティブコンポーネントの関数は、**フック（hook）** を使用できます。フックは、コンポーネントにリアクティブな機能を追加する、`editor.ui` モジュール内の特別な関数です。慣例として、すべてのフックの名前は `use_` で始まります。

リアクティブコンポーネントを作成するには、`editor.ui.component()` 関数を使用します。 

次の例を見てみましょう。これは、入力したファイル名が空でない場合にだけファイルを作成できる、新規ファイル作成ダイアログです。

```lua
-- 1. dialog is a reactive component
local dialog = editor.ui.component(function(props)
    -- 2. the component defines a local state (file name) that defaults to empty string
    local name, set_name = editor.ui.use_state("")

    return editor.ui.dialog({ 
        title = props.title,
        content = editor.ui.vertical({
            padding = editor.ui.PADDING.LARGE,
            children = { 
                editor.ui.string_field({ 
                    value = name,
                    -- 3. typing + Enter updates the local state
                    on_value_changed = set_name 
                }) 
            }
        }),
        buttons = {
            editor.ui.dialog_button({ 
                text = "Cancel", 
                cancel = true 
            }),
            editor.ui.dialog_button({ 
                text = "Create File",
                -- 4. creation is enabled when the name exists
                enabled = name ~= "",
                default = true,
                -- 5. result is the name
                result = name
            })
        }
    })
end)

-- 6. show_dialog will either return non-empty file name or nil on cancel
local file_name = editor.ui.show_dialog(dialog({ title = "New File Name" }))
if file_name then 
    print("create " .. file_name)
else
    print("cancelled")
end
```

このコードを実行するメニューコマンドを選択すると、エディターは最初に `"Create File"` が無効なダイアログを表示しますが、名前を入力して <kbd>Enter</kbd> を押すと有効になります。

![新規ファイル作成ダイアログ](images/editor_scripts/reactive_new_file_dialog.png)

これはどのように動作するのでしょうか。最初のレンダリングでは、`use_state` フックがコンポーネントに関連付けられたローカル状態を作成し、その状態を設定するセッターとともに返します。セッター関数を呼び出すと、コンポーネントの再レンダリングが予約されます。以降の再レンダリングでは、コンポーネント関数が再び呼び出され、`use_state` が更新された状態を返します。その後、コンポーネント関数が返した新しいビューコンポーネントを古いものと比較し、変更が検出された部分の UI が更新されます。

このリアクティブな手法により、操作可能な UI の構築と、その同期の維持が大幅に簡単になります。ユーザーの入力時に影響を受けるすべての UI コンポーネントを明示的に更新する代わりに、ビューを入力（プロップスとローカル状態）の純粋関数として定義し、エディター自身がすべての更新を処理します。

### リアクティビティの規則 {#rules-of-reactivity}

エディターでリアクティブな関数コンポーネントを動作させるには、次の規則に従う必要があります。

1. コンポーネント関数は純粋でなければなりません。コンポーネント関数がいつ、どのくらいの頻度で呼び出されるかは保証されません。すべての副作用は、コールバック内など、レンダリングの外で処理することを推奨します。
2. プロップスとローカル状態は不変でなければなりません。プロップスを変更しないでください。ローカル状態がテーブルの場合は、状態を変更する必要が生じても直接変更せず、新しいテーブルを作成してセッターに渡してください。
3. コンポーネント関数は、呼び出されるたびに同じフックを同じ順序で呼び出す必要があります。ループ内、条件付きブロック内、早期リターンの後などでフックを呼び出さないでください。コンポーネント関数の先頭で、ほかのコードより前にフックを呼び出すことを推奨します。
4. フックはコンポーネント関数からだけ呼び出してください。フックはリアクティブコンポーネントのコンテキストで動作するため、コンポーネント関数内、またはコンポーネント関数が直接呼び出す別の関数内でだけ呼び出せます。

### フック {#hooks}

::: sidenote
[React](https://react.dev/) に詳しい場合は、エディターのフックでは、フックの依存関係に関する挙動が少し異なることに気付くでしょう。
:::

エディターには、**`use_memo`** と **`use_state`** の2つのフックが定義されています。

### **`use_state`**

ローカル状態は、既定値を指定する方法と、初期化関数を指定する方法の2通りで作成できます。
```lua
-- default value
local enabled, set_enabled = editor.ui.use_state(true)
-- initializer function + args
local id, set_id = editor.ui.use_state(string.lower, props.name)
```
同様に、セッターは新しい値、または更新関数を指定して呼び出せます。
```lua
-- updater function
local function increment_by(n, by)
    return n + by
end

local counter = editor.ui.component(function(props)
    local count, set_count = editor.ui.use_state(0)
    
    return editor.ui.horizontal({
        spacing = editor.ui.SPACING.SMALL,
        children = {
            editor.ui.label({
                text = tostring(count),
                alignment = editor.ui.ALIGNMENT.LEFT,
                grow = true
            }),
            editor.ui.text_button({
                text = "+1",
                on_pressed = function() set_count(increment_by, 1) end
            }),
            editor.ui.text_button({
                text = "+5",
                on_pressed = function() set_count(increment_by, 5) end
            })
        }
    })
end)
```

最後に、状態は **リセット** されることがあります。`editor.ui.use_state()` の引数のいずれかが変わると、状態がリセットされます。変更の有無は `==` で確認します。このため、`use_state` フックの引数にテーブルリテラルや初期化関数のリテラルを使用してはいけません。使用すると、再レンダリングのたびに状態がリセットされます。例を示します。
```lua
-- ❌ BAD: literal table initializer causes state reset on every re-render
local user, set_user = editor.ui.use_state({ first_name = props.first_name, last_name = props.last_name})

-- ✅ GOOD: use initializer function outside of component function to create table state
local function create_user(first_name, last_name) 
    return { first_name = first_name, last_name = last_name}
end
-- ...later, in component function:
local user, set_user = editor.ui.use_state(create_user, props.first_name, props.last_name)


-- ❌ BAD: literal initializer function causes state reset on every re-render
local id, set_id = editor.ui.use_state(function() return string.lower(props.name) end)

-- ✅ GOOD: use referenced initializer function to create the state
local id, set_id = editor.ui.use_state(string.lower, props.name)
```

### **`use_memo`**

パフォーマンスを改善するために `use_memo` フックを使用できます。レンダリング関数内で、ユーザー入力が有効かどうかの確認などの計算を行うことはよくあります。`use_memo` フックは、計算関数を呼び出すよりも、その引数が変わったかどうかの確認にかかるコストが低い場合に使用できます。このフックは最初のレンダリング時に計算関数を呼び出し、以降の再レンダリングでは `use_memo` のすべての引数が変わっていなければ、計算済みの値を再利用します。
```lua
-- validation function outside of component function
local function validate_password(password)
    if #password < 8 then
        return false, "Password must be at least 8 characters long."
    elseif not password:match("%l") then
        return false, "Password must include at least one lowercase letter."
    elseif not password:match("%u") then
        return false, "Password must include at least one uppercase letter."
    elseif not password:match("%d") then
        return false, "Password must include at least one number."
    else
        return true, "Password is valid."
    end
end

-- ...later, in component function
local username, set_username = editor.ui.use_state('')
local password, set_password = editor.ui.use_state('')
local valid, message = editor.ui.use_memo(validate_password, password)
```
この例では、パスワードの検証は、パスワードフィールドへの入力などでパスワードが変わるたびに実行されますが、ユーザー名が変わったときには実行されません。

`use_memo` は、入力コンポーネントで使用するコールバックを作成するときや、ローカルで作成した関数を別のコンポーネントのプロップ値として使用するときにも利用できます。これにより、不要な再レンダリングを防ぎます。
