---
title: Componentes de texto Label no Defold
brief: Este manual explica como usar componentes label para usar texto com objetos de jogo no mundo do jogo.
---

# Label

Um componente *Label* renderiza um trecho de texto na tela, no espaço do jogo. Por padrão, ele é ordenado e desenhado junto com todos os gráficos de sprite e tiles. O componente tem um conjunto de propriedades que controla como o texto é renderizado. A GUI do Defold oferece suporte a texto, mas pode ser trabalhoso posicionar elementos GUI no mundo do jogo. Labels facilitam isso.

## Criando um label

Para criar um componente Label, <kbd>clique com o botão direito</kbd> no objeto de jogo e selecione <kbd>Adicionar Componente ▸ Rótulo</kbd>.

![Add label](images/label/add_label.png)

(Se quiser instanciar vários labels a partir do mesmo template, você também pode criar um novo arquivo de componente label: <kbd>clique com o botão direito</kbd> em uma pasta no navegador *Conteúdo* e selecione <kbd>Novo... ▸ Rótulo</kbd>, depois adicione o arquivo como componente a qualquer objeto de jogo)

![New label](images/label/label.png)

Defina a propriedade *Font* para a fonte que deseja usar e certifique-se de definir a propriedade *Material* para um material que corresponda ao tipo de fonte:

![Font and material](images/label/font_material.png)

## Propriedades de label

Além das propriedades *Id*, *Position*, *Rotation* e *Scale*, existem as seguintes propriedades específicas do componente:

*Text*
: O conteúdo de texto do label.

*Size*
: O tamanho da caixa delimitadora do texto. Se *Line Break* estiver definido, a largura especifica em que ponto o texto deve quebrar.

*Color*
: A cor do texto.

*Outline*
: A cor do contorno.

*Shadow*
: A cor da sombra.

::: sidenote
Observe que o material padrão tem a renderização de sombra desativada por motivos de desempenho.
:::

*Leading*
: Um número de escala para o espaçamento entre linhas. Um valor de 0 não dá espaçamento entre linhas. O padrão é 1.

*Tracking*
: Um número de escala para o espaçamento entre letras. O padrão é 0.

*Pivot*
: O pivô do texto. Use isto para alterar o alinhamento do texto (veja abaixo).

*Blend Mode*
: O modo de blend a usar ao renderizar o label.

*Line Break*
: O alinhamento do texto segue a configuração de pivô, e definir esta propriedade permite que o texto flua por várias linhas. A largura do componente determina onde o texto será quebrado. Observe que precisa haver um espaço no texto para que ele quebre.

*Font*
: O recurso de fonte a usar para este label.

*Material*
: O material a usar para renderizar este label. Certifique-se de selecionar um material criado para o tipo de fonte que você usa (bitmap, distance field ou BMFont).

### Modos de blend
:[blend-modes](../shared/blend-modes.md)

### Pivô e alinhamento

Ao definir a propriedade *Pivot*, você pode alterar o modo de alinhamento do texto.

*Center*
: Se o pivô for definido como `Center`, `North` ou `South`, o texto será centralizado.

*Left*
: Se o pivô for definido para qualquer um dos modos `West`, o texto será alinhado à esquerda.

*Right*
: Se o pivô for definido para qualquer um dos modos `East`, o texto será alinhado à direita.

![Text alignment](images/label/align.png)

## Manipulação em tempo de execução

Você pode manipular labels em tempo de execução obtendo e definindo o texto do label, bem como várias outras propriedades.

`color`
: A cor do label (`vector4`)

`outline`
: A cor do contorno do label (`vector4`)

`shadow`
: A cor da sombra do label (`vector4`)

`scale`
: A escala do label, seja um `number` para escala uniforme ou um `vector3` para escala individual ao longo de cada eixo.

`size`
: O tamanho do label (`vector3`)

```lua
function init(self)
    -- Define o texto do componente "my_label" no mesmo objeto de jogo
    -- que este script.
    label.set_text("#my_label", "New text")
end
```

```lua
function init(self)
    -- Define a cor do componente "my_label" no mesmo objeto de jogo
    -- que este script. A cor é um valor RGBA armazenado em um vector4.
    local grey = vmath.vector4(0.5, 0.5, 0.5, 1.0)
    go.set("#my_label", "color", grey)

    -- ...e remove o contorno, definindo seu alfa como 0...
    go.set("#my_label", "outline.w", 0)

    -- ...e escala 2x ao longo do eixo x.
    local scale_x = go.get("#my_label", "scale.x")
    go.set("#my_label", "scale.x", scale_x * 2)
end
```

## Configuração do projeto

O arquivo *game.project* tem algumas [configurações do projeto](/manuals/project-settings#label) relacionadas a labels.
