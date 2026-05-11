---
title: Manual de templates de GUI
brief: Este manual explica o sistema de templates de GUI do Defold, usado para criar componentes visuais de GUI reutilizáveis com base em templates compartilhados ou 'prefabs'.
---

# Nodes template de GUI

Nodes template de GUI fornecem um mecanismo poderoso para criar componentes GUI reutilizáveis com base em templates compartilhados ou "prefabs". Este manual explica o recurso e como usá-lo.

Um template de GUI é uma cena GUI instanciada, node por node, em outra cena GUI. Qualquer valor de propriedade nos nodes do template original pode então ser sobrescrito.

## Criando um template

Um template de GUI é uma cena GUI comum, então é criado como qualquer outra cena GUI. Clique com o botão direito em um local no painel *Assets* e selecione <kbd>New... ▸ Gui</kbd>.

![Criar template](images/gui-templates/create.png)

Crie o template e salve-o. Observe que os nodes da instância serão colocados em relação à origem, então é uma boa ideia criar o template na posição 0, 0, 0.

## Criando instâncias de um template

Você pode criar qualquer número de instâncias baseadas no template. Crie ou abra a cena GUI onde deseja colocar o template, então clique com o botão direito na seção *Nodes* no *Outline* e selecione <kbd>Add ▸ Template</kbd>.

![Criar instância](images/gui-templates/create_instance.png)

Defina a propriedade *Template* para o arquivo de cena GUI do template.

Você pode adicionar qualquer número de instâncias de template e, para cada instância, pode sobrescrever as propriedades de cada node e alterar a posição, coloração, tamanho, textura e assim por diante dos nodes da instância.

![Instâncias](images/gui-templates/instances.png)

Qualquer propriedade que você alterar é marcada em azul no editor. Pressione o botão de reset ao lado da propriedade para definir seu valor de volta ao valor do template:

![Propriedades](images/gui-templates/properties.png)

Qualquer node com propriedades sobrescritas também é colorido em azul no *Outline*:

![Outline](images/gui-templates/outline.png)

A instância de template é listada como uma entrada recolhível na visualização *Outline*. Porém, é importante observar que esse item no outline *não é um node*. A instância de template também não existe em runtime, mas todos os nodes que fazem parte da instância existem.

Nodes que fazem parte de uma instância de template são nomeados automaticamente com um prefixo e uma barra (`"/"`) anexados ao seu *Id*. O prefixo é o *Id* definido na instância de template.

## Modificando templates em runtime

Scripts que manipulam ou consultam nodes adicionados pelo mecanismo de templates só precisam considerar a nomenclatura dos nodes de instância e incluir o *Id* da instância de template como prefixo do nome do node:

```lua
if gui.pick_node(gui.get_node("button_1/button"), x, y) then
    -- Faça algo...
end
```

Não há node correspondente à instância de template em si. Se você precisar de um node raiz para uma instância, adicione-o ao template.

Se um script estiver associado a uma cena GUI de template, o script não fará parte da árvore de nodes da instância. Você pode anexar um único script a cada cena GUI, então sua lógica de script precisa ficar na cena GUI em que você instanciou seus templates.
