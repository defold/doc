Componentes são usados para dar expressão e/ou funcionalidade específica aos objetos de jogo. Componentes precisam estar contidos dentro de objetos de jogo e são afetados pela posição, rotação e escala do objeto de jogo que contém o componente:

![Componentes](../shared/images/components.png)

Muitos componentes têm propriedades específicas do tipo que podem ser manipuladas, e há funções específicas do tipo de componente disponíveis para interagir com eles em tempo de execução:

```lua
-- desabilita o sprite "body" da lata
msg.post("can#body", "disable")

-- toca o som "hoohoo" em "bean" em 1 segundo
sound.play("bean#hoohoo", { delay = 1, gain = 0.5 } )
```

Componentes são adicionados no local em um objeto de jogo ou adicionados a um objeto de jogo como referência a um arquivo de componente:

Use <kbd>Right-click</kbd> no objeto de jogo na visualização *Outline* e selecione <kbd>Add Component</kbd> (adicionar no local) ou <kbd>Add Component File</kbd> (adicionar como referência de arquivo).

Na maioria dos casos, faz mais sentido criar componentes no local, mas os seguintes tipos de componente precisam ser criados em arquivos de recurso separados antes de serem adicionados por referência a um objeto de jogo:

* Script
* GUI
* Particle FX
* Tile Map
