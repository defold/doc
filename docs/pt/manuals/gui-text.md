---
title: Nodes GUI de texto do Defold
brief: Este manual descreve como adicionar texto a cenas GUI.
---

# Nodes GUI de texto

O Defold oferece suporte a um tipo específico de node GUI que permite renderizar texto em uma cena GUI. Qualquer recurso de fonte adicionado a um projeto pode ser usado para renderização de nodes de texto.

A prévia do editor oferece suporte à modelagem de texto e ao layout da direita para a esquerda usando o renderizador de fontes da engine. Consulte [suporte a layout de texto](/manuals/font/#text-layout-support-eg-right-to-left) para conhecer as configurações de fonte e App Manifest necessárias.

## Adicionando nodes de texto

As fontes que você deseja usar em nodes GUI de texto devem ser adicionadas ao componente GUI. Clique com o botão direito na pasta *Fonts*, use o menu superior <kbd>GUI</kbd> ou pressione o atalho de teclado correspondente.

![Fontes](images/gui-text/fonts.png)

Nodes de texto têm um conjunto de propriedades especiais:

*Font*
: Qualquer node de texto que você criar deve ter a propriedade *Font* definida.

*Text*
: Esta propriedade contém o texto exibido.

*Line Break*
: O alinhamento do texto segue a configuração de pivô, e definir esta propriedade permite que o texto flua por várias linhas. A largura do node determina onde o texto quebrará.

## Fontes vetoriais e emojis coloridos {#vector-fonts-and-color-emoji}

Siga a [configuração de fontes vetoriais](/manuals/font/#vector-fonts), adicione o recurso `.font` a *Fonts* da cena de GUI e selecione-o no nó de texto. Defina o *Material* do recurso de fonte como `/builtins/fonts/font-vector.material`. Use *Font Size* do nó para controlar o tamanho exibido.

Para emojis coloridos, conclua também a [configuração do fallback COLRv1 e de inclusão no bundle](/manuals/font/#color-emoji). Crie um nó de texto com o id `text`, deixe seu *Text* vazio e adicione o seguinte ao `.gui_script` da cena de GUI:

```lua
function init(self)
    local node = gui.get_node("text")
    local text = "Hello 😀 🍎 🚀"
    local font_resource = gui.get_font_resource(gui.get_font(node))
    -- Adicione o fallback uma única vez para este recurso de fonte compartilhado.
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

[`gui.get_font()`](/ref/gui/#gui.get_font) retorna o nome da fonte na cena de GUI; [`gui.get_font_resource()`](/ref/gui/#gui.get_font_resource) resolve esse nome para o recurso de fonte usado por `font.add_font()`. Outros nós e Labels que compartilham esse recurso também recebem o fallback, portanto inicialize-o apenas uma vez. O texto é definido depois que a preparação é concluída com sucesso.

## Alinhamento

Ao definir o pivô do node, você pode alterar o modo de alinhamento do texto.

*Center*
: Se o pivô estiver definido como `Center`, `North` ou `South`, o texto será alinhado ao centro.

*Left*
: Se o pivô estiver definido como qualquer um dos modos `West`, o texto será alinhado à esquerda.

*Right*
: Se o pivô estiver definido como qualquer um dos modos `East`, o texto será alinhado à direita.

![Alinhamento de texto](images/gui-text/align.png)

## Modificando nodes de texto em runtime

Nodes de texto respondem a qualquer função genérica de manipulação de nodes para definir tamanho, pivô, cor e assim por diante. Existem algumas funções exclusivas de nodes de texto:

* Para alterar a fonte de um node de texto, use a função [`gui.set_font()`](/ref/gui/#gui.set_font).
* Para alterar o comportamento de quebra de linha de um node de texto, use a função [`gui.set_line_break()`](/ref/gui/#gui.set_line_break).
* Para alterar o conteúdo de um node de texto, use a função [`gui.set_text()`](/ref/gui/#gui.set_text).

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("set_score") then
        local s = gui.get_node("score")
        gui.set_text(s, message.score)
    end
end
```
