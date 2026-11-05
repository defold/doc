---
title: Defold の GUI テキストノード
brief: このマニュアルでは、GUI シーンにテキストを追加する方法を説明します。
---

# GUI テキストノード {#gui-text-nodes}

Defold は、GUI シーン（GUI scene）にテキストを描画できる専用の GUI ノード（GUI node）をサポートしています。プロジェクトに追加した任意のフォントリソースを、テキストノード（text node）の描画に使用できます。

エディターのプレビューは、エンジンのフォントレンダラーを使って、テキストの字形形成と右から左へのレイアウトをサポートします。必要なフォントと App Manifest の設定については、[テキストレイアウトのサポート](/manuals/font/#text-layout-support-eg-right-to-left)を参照してください。

## テキストノードの追加 {#adding-text-nodes}

GUI テキストノードで使用するフォントは、GUI コンポーネント（GUI component）に追加する必要があります。*Fonts* フォルダーを右クリックするか、上部の <kbd>GUI</kbd> メニューを使用するか、対応するキーボードショートカットを押します。

![フォント](images/gui-text/fonts.png)

テキストノードには、次の専用プロパティがあります。

*Font*
: 作成するすべてのテキストノードには、*Font* プロパティを設定する必要があります。

*Text*
: このプロパティには、表示するテキストを指定します。

*Line Break*
: テキストの揃え方はピボット（pivot）の設定に従います。このプロパティを設定すると、テキストを複数行にわたって表示できます。テキストの折り返し位置はノードの幅によって決まります。

## ベクターフォントとカラー絵文字 {#vector-fonts-and-color-emoji}

[ベクターフォントの設定](/manuals/font/#vector-fonts)に従い、GUI シーンの *Fonts* に `.font` リソースを追加して、テキストノードで選択します。フォントリソースの *Material* を `/builtins/fonts/font-vector.material` に設定します。表示サイズは、ノードの *Font Size* で制御します。

カラー絵文字では、[COLRv1 のフォールバックとバンドルの設定](/manuals/font/#color-emoji)も完了してください。ID が `text` のテキストノードを作成し、*Text* を空にしたまま、GUI シーンの `.gui_script` に以下を追加します。

```lua
function init(self)
    local node = gui.get_node("text")
    local text = "Hello 😀 🍎 🚀"
    local font_resource = gui.get_font_resource(gui.get_font(node))
    -- Add the fallback once for this shared font resource.
    font.add_font(font_resource, "/fonts/NotoColorEmoji-Regular.ttf")
    font.prewarm_text(font_resource, text, function(self, request_id, result, err)
        if result then
            gui.set_text(node, text)
        else
            print("Could not prepare GUI text:", err)
        end
    end)
end
```

[`gui.get_font()`](/ref/gui/#gui.get_font) は GUI シーン内のフォント名を返し、[`gui.get_font_resource()`](/ref/gui/#gui.get_font_resource) は、その名前を `font.add_font()` で使うフォントリソースに解決します。そのリソースを共有するほかのノードや Label にもフォールバックが追加されるため、初期化は1回だけ行います。テキストは、事前準備が成功してから設定します。

## テキストの揃え方 {#alignment}

ノードのピボットを設定すると、テキストの揃え方を変更できます。

*中央揃え*
: ピボットを `Center`、`North`、`South` のいずれかに設定すると、テキストは中央揃えになります。

*左揃え*
: ピボットを `West` のいずれかのモードに設定すると、テキストは左揃えになります。

*右揃え*
: ピボットを `East` のいずれかのモードに設定すると、テキストは右揃えになります。

![テキストの揃え方](images/gui-text/align.png)

## 実行時のテキストノードの変更 {#modifying-text-nodes-in-runtime}

テキストノードには、サイズ、ピボット、色などを設定する汎用のノード操作関数をすべて使用できます。テキストノード専用の関数もいくつかあります。

* テキストノードのフォントを変更するには、[`gui.set_font()`](/ref/gui/#gui.set_font) 関数を使用します。
* テキストノードの改行動作を変更するには、[`gui.set_line_break()`](/ref/gui/#gui.set_line_break) 関数を使用します。
* テキストノードの内容を変更するには、[`gui.set_text()`](/ref/gui/#gui.set_text) 関数を使用します。

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("set_score") then
        local s = gui.get_node("score")
        gui.set_text(s, message.score)
    end
end
```
