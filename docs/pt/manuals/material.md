---
title: Manual de materiais do Defold
brief: Este manual explica como trabalhar com materiais, constantes de shader e samplers.
---

# Materiais

Materiais são usados para expressar como um componente gráfico (um sprite, tilemap, fonte, node GUI, modelo etc.) deve ser renderizado.

Um material contém _tags_, informações usadas no pipeline de renderização para selecionar objetos que serão renderizados. Ele também contém referências a _programas de shader_, que são compilados pelo driver gráfico disponível, enviados para o hardware gráfico e executados quando o componente é renderizado a cada frame.

* Para mais informações sobre o pipeline de renderização, consulte a [documentação de Render](/manuals/render).
* Para uma explicação aprofundada dos programas de shader, consulte a [documentação de Shader](/manuals/shader).

## Criando um material

Para criar um material, <kbd>clique com o botão direito</kbd> em uma pasta de destino no navegador *Conteúdo* e selecione <kbd>Novo... ▸ Material</kbd>. (Você também pode selecionar <kbd>Arquivo ▸ Novo...</kbd> no menu e então selecionar <kbd>Material</kbd>). Dê um nome ao novo arquivo de material e pressione <kbd>Ok</kbd>.

![Material file](images/materials/material_file.png)

O novo material será aberto no *Material Editor*.

![Material editor](images/materials/material.png)

O arquivo de material contém as seguintes informações:

Name
: A identidade do material. Este nome é usado para listar o material no recurso *Render* e incluí-lo na build. O nome também é usado na função da API de renderização `render.enable_material()`. O nome deve ser único.

Vertex Program
: O arquivo de programa de vertex shader (*`.vp`*) a usar ao renderizar com o material. O programa de vertex shader é executado na GPU para cada vértice primitivo de um componente. Ele calcula a posição de tela de cada vértice e também pode opcionalmente emitir variáveis "varying", que são interpoladas e fornecidas como entrada para o fragment program.

Fragment Program
: O arquivo de programa de fragment shader (*`.fp`*) a usar ao renderizar com o material. O programa é executado na GPU para cada fragmento (pixel) de uma primitiva, e seu objetivo é decidir a cor de cada fragmento. Isso geralmente é feito por consultas de textura e cálculos baseados em variáveis de entrada (variáveis varying ou constantes).

Vertex Constants
: Uniforms que serão passados ao programa de vertex shader. Veja abaixo uma lista de constantes disponíveis.

Fragment Constants
: Uniforms que serão passados ao programa de fragment shader. Veja abaixo uma lista de constantes disponíveis.

Samplers
: Opcionalmente, você pode configurar samplers específicos no arquivo de material. Adicione um sampler, nomeie-o de acordo com o nome usado no programa de shader e defina as configurações de wrap e filtro como preferir.

Tags
: As tags associadas ao material. Tags são representadas na engine como uma _bitmask_ usada por [`render.predicate()`](/ref/render#render.predicate) para coletar componentes que devem ser desenhados juntos. Veja a [documentação de Render](/manuals/render) para saber como fazer isso. O número máximo de tags que você pode usar em um projeto é 32.

## Atributos

Atributos de shader (também chamados de vertex streams ou atributos de vértice) são um mecanismo que define como a GPU recupera vértices da memória para renderizar geometria. O vertex shader especifica um conjunto de streams usando a palavra-chave `attribute` e, na maioria dos casos, o Defold produz e vincula os dados automaticamente por baixo dos panos com base nos nomes dos streams. No entanto, em alguns casos, talvez você queira encaminhar mais dados por vértice para obter um efeito específico que a engine não produz. Um atributo de vértice pode ser configurado com os seguintes campos:

Name
: O nome do atributo. Semelhante às constantes de shader, a configuração do atributo só será usada se corresponder a um atributo especificado no vertex program.

Semantic type
: Um tipo semântico indica o significado semântico de *o que* o atributo é e/ou *como* ele deve ser mostrado no editor. Por exemplo, especificar um atributo com `SEMANTIC_TYPE_COLOR` mostrará um seletor de cor no editor, enquanto os dados ainda serão passados como estão da engine para o shader.

  - `SEMANTIC_TYPE_NONE` O tipo semântico padrão. Não tem nenhum outro efeito no atributo além de passar os dados do material para o atributo diretamente ao vertex buffer (padrão)
  - `SEMANTIC_TYPE_POSITION` Produz dados de posição por vértice para o atributo. Pode ser usado junto com espaço de coordenadas para dizer à engine como as posições serão calculadas
  - `SEMANTIC_TYPE_TEXCOORD` Produz coordenadas de textura por vértice para o atributo
  - `SEMANTIC_TYPE_PAGE_INDEX` Produz índices de página por vértice para o atributo
  - `SEMANTIC_TYPE_COLOR` Afeta como o editor interpreta o atributo. Se um atributo for configurado com semântica de cor, um widget seletor de cor será mostrado no inspetor
  - `SEMANTIC_TYPE_NORMAL` Produz dados de normal por vértice para o atributo
  - `SEMANTIC_TYPE_TANGENT` Produz dados de tangente por vértice para o atributo
  - `SEMANTIC_TYPE_WORLD_MATRIX` Produz dados de matriz de mundo por vértice para o atributo
  - `SEMANTIC_TYPE_NORMAL_MATRIX` Produz dados de matriz normal por vértice para o atributo
  - `SEMANTIC_TYPE_TEXTURE_TRANSFORM_2D` Produz uma matriz de transformação de textura 3x3 por vértice para o atributo. Para componentes de partículas, a engine fornece uma matriz que transforma coordenadas para o espaço do atlas da propriedade de imagem no componente. Para componentes sprite, a engine fornece uma matriz para cada imagem que o componente está usando (ao usar multi-texturing). Para componentes model, uma matriz identidade é fornecida.

Data type
: O tipo de dados dos dados de apoio para o atributo.

  - `TYPE_BYTE` Valores byte com sinal de 8 bits
  - `TYPE_UNSIGNED_BYTE` Valores byte sem sinal de 8 bits
  - `TYPE_SHORT` Valores short com sinal de 16 bits
  - `TYPE_UNSIGNED_SHORT` Valores short sem sinal de 16 bits
  - `TYPE_INT` Valores inteiros com sinal
  - `TYPE_UNSIGNED_INT` Valores inteiros sem sinal
  - `TYPE_FLOAT` Valores de ponto flutuante (padrão)

Normalize
: Se true, os valores do atributo serão normalizados pelo driver da GPU. Isso pode ser útil quando você não precisa de precisão total, mas quer calcular algo sem conhecer os limites específicos. Por exemplo, um vetor de cor normalmente só precisa de valores byte de 0..255, ainda sendo tratado como um valor 0..1 no shader.

Coordinate space
: Alguns tipos semânticos aceitam fornecer dados em diferentes espaços de coordenadas. Para implementar um efeito de billboarding com sprites, normalmente você quer um atributo de posição em espaço local, bem como uma posição totalmente transformada em espaço de mundo para batching mais eficiente.

Vector type
: O tipo de vetor do atributo.

  - `VECTOR_TYPE_SCALAR` Valor escalar único
  - `VECTOR_TYPE_VEC2` Vetor 2D
  - `VECTOR_TYPE_VEC3` Vetor 3D
  - `VECTOR_TYPE_VEC4` Vetor 4D (padrão)
  - `VECTOR_TYPE_MAT2` Matriz 2D
  - `VECTOR_TYPE_MAT3` Matriz 3D
  - `VECTOR_TYPE_MAT4` Matriz 4D

Step function
: Especifica como os dados do atributo devem ser apresentados à função de vértice. Isto só é relevante para instancing.

  - `Vertex` Uma vez por vértice, por exemplo um atributo de posição normalmente será dado à função de vértice por vértice na malha (padrão)
  - `Instance` Uma vez por instância, por exemplo um atributo de matriz de mundo normalmente será dado à função de vértice uma vez por instância

Value
: O valor do atributo. Valores de atributo podem ser sobrescritos por componente, mas, caso contrário, isto atuará como o valor padrão do atributo de vértice. Observação: para atributos *padrão* (posição, coordenadas de textura e índices de página), o valor será ignorado.

::: sidenote
Atributos personalizados também podem ser usados para reduzir a pegada de memória na CPU e GPU, reconfigurando os streams para usar um tipo de dado menor ou uma contagem diferente de elementos.
:::

### Semânticas de atributo padrão

O sistema de materiais atribuirá automaticamente um tipo semântico padrão com base no nome do atributo em tempo de execução para um conjunto específico de nomes:

  - `position` - tipo semântico: `SEMANTIC_TYPE_POSITION`
  - `texcoord0` - tipo semântico: `SEMANTIC_TYPE_TEXCOORD`
  - `texcoord1` - tipo semântico: `SEMANTIC_TYPE_TEXCOORD`
  - `page_index` - tipo semântico: `SEMANTIC_TYPE_PAGE_INDEX`
  - `color` - tipo semântico: `SEMANTIC_TYPE_COLOR`
  - `normal` - tipo semântico: `SEMANTIC_TYPE_NORMAL`
  - `tangent` - tipo semântico: `SEMANTIC_TYPE_TANGENT`
  - `mtx_world` - tipo semântico: `SEMANTIC_TYPE_WORLD_MATRIX`
  - `mtx_normal` - tipo semântico: `SEMANTIC_TYPE_NORMAL_MATRIX`
  - `mtx_texture_transform_2d` - tipo semântico: `SEMANTIC_TYPE_TEXTURE_TRANSFORM_2D`

Se você tiver entradas para esses atributos no material, o tipo semântico padrão será sobrescrito pelo que você tiver configurado no editor de material.

### Definindo dados personalizados de atributo de vértice

Semelhante às constantes de shader definidas pelo usuário, você também pode atualizar atributos de vértice em tempo de execução chamando go.get, go.set e go.animate:

![Custom material attribute](images/materials/set_custom_attribute.png)

```lua
go.set("#sprite", "tint", vmath.vector4(1,0,0,1))

go.animate("#sprite", "tint", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```

Há algumas ressalvas ao atualizar atributos de vértice, no entanto: se um componente pode ou não usar o valor depende do tipo semântico do atributo. Por exemplo, um componente sprite oferece suporte a `SEMANTIC_TYPE_POSITION`, então se você atualizar um atributo que tem esse tipo semântico, o componente ignorará o valor sobrescrito, pois o tipo semântico dita que os dados devem sempre ser produzidos pela posição do sprite.

Nos casos em que um atributo de vértice é um escalar ou um tipo de vetor diferente de `Vec4`, você ainda pode definir os dados usando `go.set`:

```lua
-- Os dois últimos componentes no vec4 não serão usados!
go.set("#sprite", "sprite_position_2d", vmath.vector4(my_x,my_y,0,0))
go.animate("#sprite", "sprite_position_2d", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,2,0,0), go.EASING_LINEAR, 2)
```

O mesmo vale para atributos de matriz: se o atributo for um tipo de matriz diferente de `Mat4`, você ainda poderá definir os dados usando `go.set`.

### Exemplos de uso de atributos de vértice personalizados

Usando um atributo de transformação de textura para converter coordenadas UV para espaço de atlas:

```glsl
#version 140

in vec3 position;
in vec4 texcoord0;
in mat3 texture_transform_2d;

out vec2 var_texcoord0;

void main()
{
  // Extrai a posição da transformação
  vec2 atlas_pos = texture_transform_2d[2].xy;
  // Extrai a escala da transformação
  vec2 atlas_size = vec2(
      length(texture_transform_2d[0].xy),
      length(texture_transform_2d[1].xy)
  );
  // converte para UV local (0..1)
  vec2 localUV = (texcoord0 - atlas_pos) / atlas_size;

  // Como alternativa, se as coordenadas UV já estiverem no intervalo 0..1,
  // você pode transformar diretamente para espaço de atlas multiplicando a transformação:
  vec2 transformedUv = texture_transform_2d * texcoord0;

  // Passa o valor para o fragment shader
  var_texcoord0 = localUV;

  // ... restante do vertex shader
}
```

### Instancing

Instancing é uma técnica usada para desenhar com eficiência várias cópias do mesmo objeto em uma cena. Em vez de criar uma cópia separada do objeto cada vez que ele é usado, instancing permite que a engine gráfica crie um único objeto e depois o reutilize várias vezes. Por exemplo, em um jogo com uma floresta grande, em vez de criar um modelo de árvore separado para cada árvore, instancing permite criar um modelo de árvore e então posicioná-lo centenas ou milhares de vezes com posições e escalas diferentes. A floresta pode então ser renderizada com uma única draw call em vez de draw calls individuais para cada árvore.

::: sidenote
Atualmente, instancing está disponível apenas para componentes Model.
:::

Instancing é habilitado automaticamente quando possível. O Defold depende bastante de batching do estado de desenho tanto quanto possível; para instancing funcionar, alguns requisitos devem ser atendidos:

- O mesmo material deve ser usado para todas as instâncias. Instancing ainda funcionará se um material personalizado tiver sido definido por `render.enable_material`)
- O material deve estar configurado para usar o espaço de vértice 'local'
- O material deve ter pelo menos um atributo de vértice repetido por instância
- Valores de constantes devem ser os mesmos para todas as instâncias. Valores de constantes podem ser colocados em atributos de vértice personalizados ou em algum outro método de apoio (por exemplo, uma textura)
- Recursos de shader, como texturas ou storage buffers, devem ser os mesmos para todas as instâncias

Configurar um atributo de vértice para ser repetido por instância exige que `Step function` seja definido como `Instance`. Isso é feito automaticamente para certos tipos semânticos com base no nome (veja a tabela `Default attribute semantics` acima), mas também pode ser definido manualmente no editor de material definindo `Step function` como `Instance`.

Como exemplo simples, a cena a seguir tem quatro objetos de jogo, cada um com um componente model:

![Instancing setup](images/materials/instancing-setup.png)

O material é configurado assim, com um único atributo de vértice personalizado repetido por instância:

![Instancing material](images/materials/instancing-material.png)

O vertex shader tem vários atributos por instância especificados:

```glsl
// Atributos por vértice
attribute highp vec4 position;
attribute mediump vec2 texcoord0;
attribute mediump vec3 normal;

// Atributos por instância
attribute mediump mat4 mtx_world;
attribute mediump mat4 mtx_normal;
attribute mediump vec4 instance_color;
```

Observe que `mtx_world` e `mtx_normal` serão configurados para usar a step function `Instance` por padrão. Isso pode ser alterado no editor de material adicionando uma entrada para eles e definindo `Step function` como `Vertex`, o que fará o atributo ser repetido por vértice em vez de por instância.

Para verificar que o instancing funciona neste caso, você pode olhar o perfilador web. Neste caso, como a única coisa que muda entre as instâncias da caixa são os atributos por instância, ela pode ser renderizada com uma única draw call:

![Instancing draw calls](images/materials/instancing-draw-calls.png)

#### Compatibilidade retroativa

Em adaptadores gráficos baseados em OpenGL, instancing exige pelo menos OpenGL 3.1 para desktop e OpenGL ES 3.0 para mobile. Isso significa que dispositivos muito antigos usando OpenGL ES2 ou versões mais antigas de OpenGL podem não oferecer suporte a instancing. Nesse caso, a renderização ainda funcionará por padrão sem nenhum cuidado especial do desenvolvedor, mas talvez não tenha o mesmo desempenho que teria se instancing real fosse usado. Atualmente, não há como detectar se instancing é suportado ou não, mas essa funcionalidade será adicionada no futuro para que um material mais barato possa ser usado, ou para que coisas como folhagem ou clutter, que normalmente seriam boas candidatas a instancing, possam ser puladas completamente.

## Constantes de vértice e fragmento

Constantes de shader, ou "uniforms", são valores passados da engine para programas de vertex e fragment shader. Para usar uma constante, você a define no arquivo de material como uma propriedade *Vertex Constant* ou *Fragment Constant*. Variáveis `uniform` correspondentes precisam ser definidas no programa de shader. As seguintes constantes podem ser definidas em um material:

`CONSTANT_TYPE_WORLD`
: A matriz de mundo. Use para transformar vértices para o espaço de mundo. Para alguns tipos de componente, os vértices já estão em espaço de mundo quando chegam ao vertex program (devido ao batching). Nesses casos, multiplicar pela matriz de mundo no shader produzirá resultados incorretos.

`CONSTANT_TYPE_VIEW`
: A matriz de visualização. Use para transformar vértices para o espaço de visualização (câmera).

`CONSTANT_TYPE_PROJECTION`
: A matriz de projeção. Use para transformar vértices para o espaço de tela.

`CONSTANT_TYPE_VIEWPROJ`
: Uma matriz com as matrizes de visualização e projeção já multiplicadas.

`CONSTANT_TYPE_WORLDVIEW`
: Uma matriz com as matrizes de mundo e visualização já multiplicadas.

`CONSTANT_TYPE_WORLDVIEWPROJ`
: Uma matriz com as matrizes de mundo, visualização e projeção já multiplicadas.

`CONSTANT_TYPE_NORMAL`
: Uma matriz para calcular a orientação das normais. A transformação de mundo pode incluir escala não uniforme, o que quebra a ortogonalidade da transformação mundo-visualização combinada. A matriz normal é usada para evitar problemas com a direção ao transformar normais. (A matriz normal é a transposta inversa da matriz mundo-visualização).

`CONSTANT_TYPE_USER`
: Uma constante vector4 que você pode usar para qualquer dado personalizado que queira passar aos seus programas de shader. Você pode definir o valor inicial da constante na definição da constante, mas ela é mutável pelas funções [go.set()](/ref/stable/go/#go.set) / [go.animate()](/ref/stable/go/#go.animate). Você também pode recuperar o valor com [go.get()](/ref/stable/go/#go.get). Alterar uma constante de material de uma única instância de componente [quebra o batching de renderização e resultará em draw calls adicionais](/manuals/render/#draw-calls-and-batching).

Exemplo:

```lua
go.set("#sprite", "tint", vmath.vector4(1,0,0,1))

go.animate("#sprite", "tint", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```

`CONSTANT_TYPE_USER_MATRIX4`
: Uma constante matrix4 que você pode usar para qualquer dado personalizado que queira passar aos seus programas de shader. Você pode definir o valor inicial da constante na definição da constante, mas ela é mutável pelas funções [go.set()](/ref/stable/go/#go.set) / [go.animate()](/ref/stable/go/#go.animate). Você também pode recuperar o valor com [go.get()](/ref/stable/go/#go.get). Alterar uma constante de material de uma única instância de componente [quebra o batching de renderização e resultará em draw calls adicionais](/manuals/render/#draw-calls-and-batching).

Exemplo:

```lua
go.set("#sprite", "m", vmath.matrix4())
```

::: sidenote
Para que uma constante de material do tipo `CONSTANT_TYPE_USER` ou `CONSTANT_TYPE_MATRIX4` esteja disponível usando `go.get()` e `go.set()`, ela precisa ser usada no programa de shader. Se a constante for definida no material, mas não usada no programa, ela será removida do material e não ficará disponível em tempo de execução.
:::

## Samplers

Samplers são usados para amostrar as informações de cor de uma textura (um tile source ou atlas). As informações de cor podem então ser usadas para cálculos no programa de shader.

Componentes Sprite, tilemap, GUI e efeito de partículas recebem automaticamente um `sampler2D` definido. O primeiro `sampler2D` declarado no programa de shader é vinculado automaticamente à imagem referenciada no componente gráfico. Portanto, atualmente não há necessidade de especificar samplers no arquivo de materiais para esses componentes. Além disso, esses tipos de componente atualmente oferecem suporte a apenas uma textura. (Se você precisar de várias texturas em um shader, pode usar [`render.enable_texture()`](/ref/render/#render.enable_texture) e definir samplers de textura manualmente a partir do seu script de renderização.)

![Sprite sampler](images/materials/sprite_sampler.png)

```glsl
-- mysprite.fp
varying mediump vec2 var_texcoord0;
uniform lowp sampler2D MY_SAMPLER;
void main()
{
    gl_FragColor = texture2D(MY_SAMPLER, var_texcoord0.xy);
}
```

Você pode especificar as configurações de sampler de um componente adicionando o sampler pelo nome no arquivo de materiais. Se você não configurar seu sampler no arquivo de materiais, as configurações globais de projeto *graphics* serão usadas.

![Sampler settings](images/materials/my_sampler.png)

Para componentes model, você precisa especificar seus samplers no arquivo de material com as configurações desejadas. O editor então permitirá definir texturas para qualquer componente model que use o material:

![Model samplers](images/materials/model_samplers.png)

```glsl
-- mymodel.fp
varying mediump vec2 var_texcoord0;
uniform lowp sampler2D TEXTURE_1;
uniform lowp sampler2D TEXTURE_2;
void main()
{
    lowp vec4 color1 = texture2D(TEXTURE_1, var_texcoord0.xy);
    lowp vec4 color2 = texture2D(TEXTURE_2, var_texcoord0.xy);
    gl_FragColor = color1 * color2;
}
```

![Model](images/materials/model.png)

## Configurações de sampler

Name
: O nome do sampler. Esse nome deve corresponder ao `sampler2D` declarado no fragment shader.

Wrap U/W
: O modo de wrap para os eixos U e V:

  - `WRAP_MODE_REPEAT` repetirá dados de textura fora do intervalo [0,1].
  - `WRAP_MODE_MIRRORED_REPEAT` repetirá dados de textura fora do intervalo [0,1], mas cada segunda repetição será espelhada.
  - `WRAP_MODE_CLAMP_TO_EDGE` definirá dados de textura para valores maiores que 1.0 como 1.0, e quaisquer valores menores que 0.0 serão definidos como 0.0; ou seja, os pixels da borda serão repetidos até a borda.

Filter Min/Mag
: A filtragem para magnificação e minificação. Filtragem nearest exige menos computação que interpolação linear, mas pode resultar em artefatos de aliasing. Interpolação linear frequentemente produz resultados mais suaves:

  - `Default` usa a opção de filtro padrão especificada no arquivo `game.project` em `Graphics` como `Default Texture Min Filter` e `Default Texture Mag Filter`.
  - `FILTER_MODE_NEAREST` usa o texel com coordenadas mais próximas do centro do pixel.
  - `FILTER_MODE_LINEAR` define uma média linear ponderada do array 2x2 de texels que ficam mais próximos do centro do pixel.
  - `FILTER_MODE_NEAREST_MIPMAP_NEAREST` escolhe o valor de texel mais próximo dentro de um mipmap individual.
  - `FILTER_MODE_NEAREST_MIPMAP_LINEAR` seleciona o texel mais próximo nas duas melhores escolhas de mipmaps mais próximas e então interpola linearmente entre esses dois valores.
  - `FILTER_MODE_LINEAR_MIPMAP_NEAREST` interpola linearmente dentro de um mipmap individual.
  - `FILTER_MODE_LINEAR_MIPMAP_LINEAR` usa interpolação linear para calcular o valor em cada um de dois mapas e então interpola linearmente entre esses dois valores.

Max Anisotropy
: Filtragem anisotrópica é uma técnica avançada de filtragem que usa várias amostras, misturando os resultados. Esta configuração controla o nível de anisotropia para os samplers de textura. Se a filtragem anisotrópica não for suportada pela GPU, o parâmetro não fará nada e será definido como 1 por padrão.

## Buffers de constantes

Quando o pipeline de renderização desenha, ele obtém valores de constantes de um buffer padrão de constantes do sistema. Você pode criar um buffer de constantes personalizado para sobrescrever as constantes padrão e, em vez disso, definir programaticamente uniforms do programa de shader no script de renderização:

```lua
self.constants = render.constant_buffer() -- <1>
self.constants.tint = vmath.vector4(1, 0, 0, 1) -- <2>
...
render.draw(self.my_pred, {constants = self.constants}) -- <3>
```
1. Crie um novo buffer de constantes
2. Defina a constante `tint` para vermelho vivo
3. Desenhe o predicado usando nossas constantes personalizadas

Observe que os elementos constantes do buffer são referenciados como uma tabela Lua comum, mas você não pode iterar sobre o buffer com `pairs()` ou `ipairs()`.
