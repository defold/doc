---
title: Entrada de teclas e texto no Defold
brief: Este manual explica como funciona a entrada de teclas e texto.
---

::: sidenote
Recomenda-se que você se familiarize com a forma geral como a entrada funciona no Defold, como receber entrada e em que ordem ela é recebida nos seus arquivos de script. Saiba mais sobre o sistema de entrada no [manual Visão geral de entrada](/manuals/input).
:::

# Key Triggers
Key triggers permitem mapear a entrada de uma única tecla do teclado para ações do jogo. Cada tecla é mapeada separadamente para uma ação correspondente. Key triggers são usados para vincular botões específicos a funções específicas, como o movimento de personagem com as setas ou teclas WASD. Se você precisar ler entrada arbitrária de teclado, use text triggers (veja abaixo).

![](images/input/key_bindings.png)

```lua
function on_input(self, action_id, action)
    if action_id == hash("left") then
        if action.pressed then
            -- começar a mover para a esquerda
        elseif action.released then
            -- parar de mover para a esquerda
        end
    end
end
```

# Text Triggers
Text triggers são usados para ler entrada de texto arbitrária. Há dois tipos de text triggers: `text` e `marked-text`.

![](images/input/text_bindings.png)

## Text
O `text` captura entrada de texto normal. Ele define o campo `text` da tabela de ação para uma string contendo o caractere digitado. A ação é disparada apenas no pressionamento do botão; nenhuma ação `release` ou `repeated` é enviada.

```lua
function on_input(self, action_id, action)
    if action_id == hash("text") then
        -- Concatena o caractere digitado ao node "user"...
        local node = gui.get_node("user")
        local name = gui.get_text(node)
        name = name .. action.text
        gui.set_text(node, name)
    end
end
```

## Marked text
O `marked-text` é usado principalmente para teclados asiáticos, nos quais várias teclas pressionadas podem corresponder a uma única entrada. Por exemplo, com o teclado iOS "Japanese-Kana", o usuário pode digitar combinações e a parte superior do teclado exibirá símbolos disponíveis ou sequências de símbolos que podem ser inseridos.

![Input marked text](images/input/marked_text.png)

- Cada tecla pressionada gera uma ação separada e define o campo de ação `text` para a sequência de símbolos inserida atualmente (o "marked text").
- Quando o usuário seleciona um símbolo ou combinação de símbolos, uma ação de trigger separada do tipo `text` é enviada (desde que uma esteja configurada na lista de mapeamentos de entrada). A ação separada define o campo de ação `text` para a sequência final de símbolos.
