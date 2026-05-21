---
title: Nodes GUI de texto do Defold
brief: Este manual descreve como adicionar texto a cenas GUI.
---

# Nodes GUI de texto

O Defold oferece suporte a um tipo específico de node GUI que permite renderizar texto em uma cena GUI. Qualquer recurso de fonte adicionado a um projeto pode ser usado para renderização de nodes de texto.

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

