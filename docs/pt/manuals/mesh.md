---
title: Malhas 3D no Defold
brief: Este manual descreve como criar malhas 3D em tempo de execução no seu jogo.
---

# Componente Mesh

O Defold é, no seu núcleo, uma engine 3D. Mesmo quando você trabalha apenas com material 2D, toda renderização é feita em 3D, mas projetada ortograficamente na tela. O Defold permite usar conteúdo 3D completo adicionando e criando malhas 3D em tempo de execução nas suas coleções. Você pode criar jogos estritamente 3D com apenas assets 3D, ou misturar conteúdo 3D e 2D como quiser.

## Criando um componente mesh

Componentes Mesh são criados como qualquer outro componente de objeto de jogo. Você pode fazer isso de duas formas:

- Crie um *arquivo Mesh* com <kbd>clique com o botão direito</kbd> em um local no navegador *Conteúdo* e selecione <kbd>Novo... ▸ Malha</kbd>.
- Crie o componente incorporado diretamente em um objeto de jogo com <kbd>clique com o botão direito</kbd> em um objeto de jogo na visualização *Estrutura* e selecione <kbd>Adicionar Componente ▸ Malha</kbd>.

![Mesh in game object](images/mesh/mesh.png)

Com a malha criada, você precisa especificar algumas propriedades:

### Propriedades de mesh

Além das propriedades *Id*, *Position* e *Rotation*, existem as seguintes propriedades específicas do componente:

*Material*
: O material a usar para renderizar a malha.

*Vertices*
: Um arquivo de buffer que descreve os dados da malha por stream.

*Primitive Type*
: Lines, Triangles ou Triangle Strip.

*Position Stream*
: Esta propriedade deve ser o nome do stream *position*. O stream é fornecido automaticamente como entrada para o vertex shader.

*Normal Stream*
: Esta propriedade deve ser o nome do stream *normal*. O stream é fornecido automaticamente como entrada para o vertex shader.

*tex0*
: Defina isto para a textura a usar na malha.

## Manipulação no editor

Com o componente mesh no lugar, você pode editar e manipular livremente o componente e/ou o objeto de jogo que o encapsula com as ferramentas normais do *Scene Editor* para mover, rotacionar e escalar a malha como desejar.

## Manipulação em tempo de execução

Você pode manipular malhas em tempo de execução usando buffers do Defold. Exemplo de criação de um cubo a partir de triangle strips:

```Lua

-- cubo
local vertices = {
	0, 0, 0,
	0, 1, 0,
	1, 0, 0,
	1, 1, 0,
	1, 1, 1,
	0, 1, 0,
	0, 1, 1,
	0, 0, 1,
	1, 1, 1,
	1, 0, 1,
	1, 0, 0,
	0, 0, 1,
	0, 0, 0,
	0, 1, 0
}

-- cria um buffer com um stream de posição
local buf = buffer.create(#vertices / 3, {
	{ name = hash("position"), type=buffer.VALUE_TYPE_FLOAT32, count = 3 }
})

-- obtém o stream de posição e escreve os vértices
local positions = buffer.get_stream(buf, "position")
for i, value in ipairs(vertices) do
	positions[i] = vertices[i]
end

-- define o buffer com os vértices na malha
local res = go.get("#mesh", "vertices")
resource.set_buffer(res, buf)
```

Consulte a [postagem de anúncio no fórum para mais informações](https://forum.defold.com/t/mesh-component-in-defold-1-2-169-beta/65137) sobre como usar o componente Mesh, incluindo projetos de exemplo e trechos de código.

## Frustum culling

Componentes Mesh não são automaticamente descartados por culling devido à sua natureza dinâmica e ao fato de não ser possível saber com certeza como os dados posicionais são codificados. Para fazer culling de uma malha, a caixa delimitadora alinhada aos eixos da malha precisa ser definida como metadados no buffer usando 6 floats (AABB min/max):

```lua
buffer.set_metadata(buf, hash("AABB"), { 0, 0, 0, 1, 1, 1 }, buffer.VALUE_TYPE_FLOAT32)
```

## Constantes de material

{% include shared/material-constants.md component='mesh' variable='tint' %}

`tint`
: O tint de cor da malha (`vector4`). O `vector4` é usado para representar o tint com x, y, z e w correspondendo ao tint vermelho, verde, azul e alfa.

## Espaço local vs espaço de mundo dos vértices
Se a configuração Vertex Space do material da malha estiver definida como Local Space, os dados serão fornecidos como estão para você no shader, e você terá que transformar vértices/normais como de costume na GPU.

Se a configuração Vertex Space do material da malha estiver definida como World Space, você precisa fornecer um stream padrão `position` e `normal`, ou pode selecioná-lo no menu suspenso ao editar a malha. Isso é necessário para que a engine possa transformar os dados para espaço de mundo para batching com outros objetos.
