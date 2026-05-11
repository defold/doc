---
title: Programas de shader no Defold
brief: Este manual descreve vertex shaders e fragment shaders em detalhes e como usá-los no Defold.
---

# Shaders

Programas de shader estão no centro da renderização gráfica. Eles são programas escritos em uma linguagem parecida com C chamada GLSL (GL Shading Language), que o hardware gráfico executa para realizar operações nos dados 3D subjacentes (os vértices) ou nos pixels que acabam na tela (os "fragmentos"). Shaders são usados para desenhar sprites, iluminar modelos 3D, criar efeitos de pós-processamento em tela cheia e muito, muito mais.

Este manual descreve como o pipeline de renderização do Defold se comunica com shaders na GPU. Para criar shaders para seu conteúdo, você também precisa entender o conceito de materiais, assim como o funcionamento do pipeline de renderização.

* Veja o [manual de Render](/manuals/render) para detalhes sobre o pipeline de renderização.
* Veja o [manual de Material](/manuals/material) para detalhes sobre materiais.
* Veja o [manual de Compute](/manuals/compute) para detalhes sobre programas de compute.

As especificações de OpenGL ES 2.0 (OpenGL for Embedded Systems) e OpenGL ES Shading Language podem ser encontradas em [Khronos OpenGL Registry](https://www.khronos.org/registry/gles/).

Observe que, em computadores desktop, é possível escrever shaders usando recursos não disponíveis no OpenGL ES 2.0. O driver da sua placa de vídeo pode compilar e executar sem problemas código de shader que não funcionará em dispositivos móveis.


## Conceitos

Vertex shader
: Um vertex shader não pode criar nem excluir vértices; ele só pode alterar a posição de um vértice. Vertex shaders são comumente usados para transformar as posições dos vértices do espaço 3D do mundo para o espaço 2D da tela.

  A entrada de um vertex shader são dados de vértice (na forma de `attributes`) e constantes (`uniforms`). Constantes comuns são as matrizes necessárias para transformar e projetar a posição de um vértice para o espaço da tela.

  A saída do vertex shader é a posição calculada do vértice na tela (`gl_Position`). Também é possível passar dados do vertex shader para o fragment shader por meio de variáveis `varying`.

Fragment shader
: Depois que o vertex shader termina, cabe ao fragment shader decidir a coloração de cada fragmento (ou pixel) das primitivas resultantes.

  A entrada de um fragment shader são constantes (`uniforms`), além de quaisquer variáveis `varying` definidas pelo vertex shader.

  A saída do fragment shader é o valor de cor do fragmento específico (`gl_FragColor`).

Compute shader
: Um compute shader é um shader de propósito geral que pode ser usado para realizar qualquer tipo de trabalho em uma GPU. Ele não faz parte do pipeline gráfico; compute shaders executam em um contexto de execução separado e não dependem de entrada de nenhum outro shader.

  A entrada de um compute shader são buffers de constantes (`uniforms`), imagens de textura (`image2D`), samplers (`sampler2D`) e buffers de armazenamento (`buffer`).

  A saída do compute shader não é definida explicitamente; não há uma saída específica que precise ser produzida, ao contrário dos vertex shaders e fragment shaders. Como compute shaders são genéricos, cabe ao programador definir que tipo de resultado o compute shader deve produzir.

Matriz world
: As posições dos vértices da forma de um modelo são armazenadas em relação à origem do modelo. Isso é chamado de "model space". O mundo do jogo, porém, é um "world space" onde a posição, orientação e escala de cada vértice são expressas em relação à origem do mundo. Ao manter essas coisas separadas, a engine do jogo consegue mover, rotacionar e escalar cada modelo sem destruir os valores originais de vértice armazenados no componente de modelo.

  Quando um modelo é colocado no mundo do jogo, as coordenadas locais dos vértices do modelo precisam ser traduzidas para coordenadas de mundo. Essa tradução é feita por uma *matriz de transformação world*, que informa qual translação (movimento), rotação e escala devem ser aplicadas aos vértices de um modelo para que ele seja posicionado corretamente no sistema de coordenadas do mundo do jogo.

  ![World transform](images/shader/world_transform.png)

Matriz de visualização e projeção
: Para colocar os vértices do mundo do jogo na tela, as coordenadas 3D de cada matriz são primeiro traduzidas para coordenadas relativas à câmera. Isso é feito com uma _matriz de visualização_. Em seguida, os vértices são projetados no espaço 2D da tela com uma _matriz de projeção_:

  ![Projection](images/shader/projection.png)

Attributes
: Um valor associado a um vértice individual. Attributes são passados para o shader pela engine e, se você quiser acessar um atributo, basta declará-lo no seu programa de shader. Diferentes tipos de componente têm conjuntos diferentes de attributes:
  - Sprite tem `position` e `texcoord0`.
  - Tilegrid tem `position` e `texcoord0`.
  - Nó de GUI tem `position`, `textcoord0` e `color`.
  - ParticleFX tem `position`, `texcoord0` e `color`.
  - Model tem `position`, `texcoord0` e `normal`.
  - Font tem `position`, `texcoord0`, `face_color`, `outline_color` e `shadow_color`.

Constants
: Constantes de shader permanecem constantes durante a chamada de desenho de renderização. Constantes são adicionadas às seções *Constants* do arquivo de material e depois declaradas como `uniform` no programa de shader. Uniforms de sampler são adicionados à seção *Samplers* do material e depois declarados como `uniform` no programa de shader. As matrizes necessárias para realizar transformações de vértices em um vertex shader ficam disponíveis como constantes:

  - `CONSTANT_TYPE_WORLD` é a *matriz world* que mapeia do espaço de coordenadas local de um objeto para o espaço de mundo.
  - `CONSTANT_TYPE_VIEW` é a *matriz de visualização* que mapeia do espaço de mundo para o espaço da câmera.
  - `CONSTANT_TYPE_PROJECTION` é a *matriz de projeção* que mapeia da câmera para o espaço da tela.
  - Matrizes pré-multiplicadas $world * view$, $view * projection$ e $world * view$ também estão disponíveis.
  - `CONSTANT_TYPE_USER` é uma constante do tipo `vec4` que você pode usar como quiser.

  O [manual de Material](/manuals/material) explica como especificar constantes.

Samplers
: Shaders podem declarar variáveis uniform do tipo *sampler*. Samplers são usados para ler valores de uma fonte de imagem:

  - `sampler2D` amostra de uma textura de imagem 2D.
  - `sampler2DArray` amostra de uma textura de array de imagens 2D. Isso é usado principalmente para atlas paginados.
  - `samplerCube` amostra de uma textura cubemap com 6 imagens.
  - `image2D` carrega (e potencialmente armazena) dados de textura em um objeto de imagem. Isso é usado principalmente por compute shaders para armazenamento.

  Você só pode usar um sampler nas funções de consulta de textura da biblioteca padrão GLSL. O [manual de Material](/manuals/material) explica como especificar configurações de sampler.

Coordenadas UV
: Uma coordenada 2D é associada a um vértice e mapeia para um ponto em uma textura 2D. Uma parte, ou a totalidade, da textura pode então ser pintada sobre a forma descrita por um conjunto de vértices.

  ![UV coordinates](images/shader/uv_map.png)

  Um UV-map normalmente é gerado no programa de modelagem 3D e armazenado na malha. As coordenadas de textura de cada vértice são fornecidas ao vertex shader como um atributo. Uma variável varying é então usada para encontrar a coordenada UV de cada fragmento, interpolada a partir dos valores dos vértices.

Variáveis varying
: Variáveis do tipo varying são usadas para passar informações entre a etapa de vértice e a etapa de fragmento.

  1. Uma variável varying é definida no vertex shader para cada vértice.
  2. Durante a rasterização, esse valor é interpolado para cada fragmento da primitiva renderizada. A distância do fragmento aos vértices da forma determina o valor interpolado.
  3. A variável é definida para cada chamada ao fragment shader e pode ser usada nos cálculos de fragmento.

  ![Varying interpolation](images/shader/varying_vertex.png)

  Por exemplo, definir um varying para um valor de cor RGB `vec3` em cada canto de um triângulo interpolará as cores por toda a forma. De modo semelhante, definir coordenadas de consulta de mapa de textura (ou *coordenadas UV*) em cada vértice de um retângulo permite que o fragment shader consulte valores de cor da textura para toda a área da forma.

  ![Varying interpolation](images/shader/varying.png)

## Escrevendo shaders GLSL modernos

Como a engine Defold suporta várias plataformas e APIs gráficas, precisa ser simples para desenvolvedores escrever shaders que funcionem em todos os lugares. O pipeline de assets consegue isso principalmente de duas formas (chamadas de `shader pipelines` daqui em diante):

1. O pipeline legado, em que shaders são escritos em código GLSL compatível com ES2.
2. O pipeline moderno, em que shaders são escritos em código GLSL compatível com SPIR-v.

A partir do Defold 1.9.2, recomenda-se escrever shaders que usem o novo pipeline. Para isso, a maioria dos shaders precisa ser migrada para shaders escritos em pelo menos a versão 140 (OpenGL 3.1). Para migrar um shader, certifique-se de que estes requisitos sejam atendidos:

### Declaração de versão
Coloque pelo menos #version 140 no topo do shader:

```glsl
#version 140
```

É assim que o pipeline de shader é escolhido no processo de build, por isso você ainda pode usar shaders antigos. Se nenhum pré-processador de versão for encontrado, o Defold usará o pipeline legado.

### Attributes
Em vertex shaders, substitua a palavra-chave `attribute` por `in`:

```glsl
// em vez de:
// attribute vec4 position;
// faça:
in vec4 position;
```

Observação: fragment shaders (e compute shaders) não recebem entradas de vértice.

### Varyings
Em vertex shaders, varyings devem receber o prefixo `out`. Em fragment shaders, varyings se tornam `in`:

```glsl
// Em um vertex shader, em vez de:
// varying vec4 var_color;
// faça:
out vec4 var_color;

// Em um fragment shader, em vez de:
// varying vec4 var_color;
// faça:
in vec4 var_color;
```

### Uniforms (chamados de constantes no Defold)

Tipos uniform opacos (samplers, images, atomics, SSBOs) não precisam de migração; você pode usá-los como usa hoje:

```glsl
uniform sampler2D my_texture;
uniform image2D my_image;
```

Para tipos uniform não opacos, você precisa colocá-los em um `uniform block`. Um uniform block é simplesmente uma coleção de variáveis uniform, declarada com a palavra-chave `uniform`:

```glsl
uniform vertex_inputs
{
    mat4 mtx_world;
    mat4 mtx_proj;
    mat4 mtx_view;
    mat4 mtx_normal;
    ...
};

void main()
{
    // Membros individuais do uniform block podem ser usados diretamente
    gl_Position = mtx_proj * mtx_view * mtx_world * vec4(position, 1.0);
}
```

Todos os membros no uniform block são expostos a materiais e componentes como constantes individuais. Nenhuma migração é necessária para usar buffers de constantes de renderização, ou `go.set` e `go.get`.

### Variáveis integradas

Em fragment shaders, `gl_FragColor` está obsoleto a partir da versão 140. Use `out` em vez disso:

```glsl
// em vez de:
// gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
// faça:
out vec4 color_out;

void main()
{
    color_out = vec4(1.0, 0.0, 0.0, 1.0);
}
```

### Funções de textura

Funções específicas de amostragem de textura, como `texture2D` e `texture2DArray`, não existem mais. Em vez disso, use apenas a função `texture`:

```glsl
uniform sampler2D my_texture;
uniform sampler2DArray my_texture_array;

// em vez de:
// vec4 sampler_2d = texture2D(my_texture, uv);
// vec4 sampler_2d_array = texture2DArray(my_texture_array, vec3(uv, slice));
// faça:
vec4 sampler_2d = texture(my_texture, uv);
vec4 sampler_2d_array = texture(my_texture_array, vec3(uv, slice));
```

### Precisão

Definir precisão explícita para variáveis, entradas, saídas e assim por diante era necessário anteriormente para compatibilidade com contextos OpenGL ES. Isso não é mais necessário; a precisão agora é definida automaticamente para plataformas que a suportam.

### Juntando tudo

Como exemplo final onde todas essas regras são aplicadas, aqui estão os shaders de sprite integrados convertidos para o novo formato:

```glsl
#version 140

uniform vx_uniforms
{
    mat4 view_proj;
};

// posições estão em espaço de mundo
in vec4 position;
in vec2 texcoord0;

out vec2 var_texcoord0;

void main()
{
    gl_Position = view_proj * vec4(position.xyz, 1.0);
    var_texcoord0 = texcoord0;
}
```

```glsl
#version 140

in vec2 var_texcoord0;

out vec4 color_out;

uniform sampler2D texture_sampler;

uniform fs_uniforms
{
    vec4 tint;
};

void main()
{
    // Pré-multiplica alpha, pois todas as texturas de runtime já são assim
    vec4 tint_pm = vec4(tint.xyz * tint.w, tint.w);
    color_out = texture(texture_sampler, var_texcoord0.xy) * tint_pm;
}

```

## Incluindo trechos em shaders

Shaders no Defold suportam incluir código-fonte de arquivos dentro do projeto que tenham a extensão `.glsl`. Para incluir um arquivo glsl a partir de um shader, use a pragma `#include` com aspas duplas ou colchetes. Includes precisam ter caminhos relativos ao projeto ou um caminho relativo ao arquivo que os inclui:

```glsl
// No arquivo /main/my-shader.fp

// Caminho absoluto
#include "/main/my-snippet.glsl"
// O arquivo está na mesma pasta
#include "my-snippet.glsl"
// O arquivo está em uma subpasta no mesmo nível de 'my-shader'
#include "sub-folder/my-snippet.glsl"
// O arquivo está em uma subpasta no diretório pai, isto é /some-other-folder/my-snippet.glsl
#include "../some-other-folder/my-snippet.glsl"
// O arquivo está no diretório pai, isto é /root-level-snippet.glsl
#include "../root-level-snippet.glsl"
```

Há algumas ressalvas sobre como includes são encontrados:

  - Arquivos precisam ser relativos ao projeto, ou seja, você só pode incluir arquivos localizados dentro do projeto. Qualquer caminho absoluto deve ser especificado com uma `/` inicial
  - Você pode incluir código em qualquer lugar do arquivo, mas não pode incluir um arquivo inline dentro de uma instrução. Por exemplo, `const float #include "my-float-name.glsl" = 1.0` não funcionará

### Header guards

Trechos podem eles mesmos incluir outros arquivos `.glsl`, o que significa que o shader final produzido pode potencialmente incluir o mesmo código várias vezes. Dependendo do conteúdo dos arquivos, você pode acabar com problemas de compilação por ter os mesmos símbolos declarados mais de uma vez. Para evitar isso, você pode usar *header guards*, um conceito comum em várias linguagens de programação. Exemplo:

```glsl
// Em my-shader.vs
#include "math-functions.glsl"
#include "pi.glsl"

// Em math-functions.glsl
#include "pi.glsl"

// Em pi.glsl
const float PI = 3.14159265359;
```

Neste exemplo, a constante `PI` será definida duas vezes, o que causará erros de compilador ao executar o projeto. Em vez disso, você deve proteger o conteúdo com header guards:

```glsl
// Em pi.glsl
#ifndef PI_GLSL_H
#define PI_GLSL_H

const float PI = 3.14159265359;

#endif // PI_GLSL_H
```

O código de `pi.glsl` será expandido duas vezes em `my-shader.vs`, mas como você o envolveu em header guards, o símbolo PI será definido apenas uma vez e o shader compilará com sucesso.

No entanto, isso nem sempre é estritamente necessário, dependendo do caso de uso. Se, em vez disso, você quiser reutilizar código localmente em uma função ou em outro lugar onde não precisa que os valores estejam disponíveis globalmente no código do shader, provavelmente não deve usar header guards. Exemplo:

```glsl
// Em red-color.glsl
vec3 my_red_color = vec3(1.0, 0.0, 0.0);

// Em my-shader.fp
vec3 get_red_color()
{
  #include "red-color.glsl"
  return my_red_color;
}

vec3 get_red_color_inverted()
{
  #include "red-color.glsl"
  return 1.0 - my_red_color;
}
```

## Código de shader específico do editor

Quando shaders são renderizados no viewport do Defold Editor, uma definição de pré-processador `EDITOR` fica disponível. Isso permite escrever código de shader que se comporta de forma diferente ao rodar no editor e ao rodar na engine real do jogo.

Isso é particularmente útil para:
  - Adicionar visualizações de debug que devem aparecer apenas no editor.
  - Implementar recursos específicos do editor, como modos wireframe ou pré-visualizações de material.
  - Fornecer renderização fallback para materiais que talvez não funcionem corretamente no viewport do editor.

Use a diretiva de pré-processador `#ifdef EDITOR` para compilar condicionalmente código que deve rodar apenas no editor:

```glsl
#ifdef EDITOR
    // Este código só será executado quando o shader for renderizado no Defold Editor
    color_out = vec4(1.0, 0.0, 1.0, 1.0); // Cor magenta para pré-visualização no editor
#else
    // Este código será executado ao rodar no jogo
    color_out = texture(texture_sampler, var_texcoord0) * tint_pm;
#endif
```

## O processo de renderização

Antes de acabar na tela, os dados que você cria para seu jogo passam por uma série de etapas:

![Render pipeline](images/shader/pipeline.png)

Todos os componentes visuais (sprites, nós de GUI, efeitos de partículas ou modelos) consistem em vértices, pontos no mundo 3D que descrevem a forma do componente. O bom disso é que é possível ver a forma de qualquer ângulo e distância. O trabalho do programa de vertex shader é pegar um único vértice e traduzi-lo para uma posição no viewport para que a forma possa aparecer na tela. Para uma forma com 4 vértices, o programa de vertex shader roda 4 vezes, cada execução em paralelo.

![vertex shader](images/shader/vertex_shader.png)

A entrada do programa é a posição do vértice (e outros dados de atributo associados ao vértice), e a saída é uma nova posição de vértice (`gl_Position`), além de quaisquer variáveis `varying` que devem ser interpoladas para cada fragmento.

O programa de vertex shader mais simples apenas define a posição da saída para um vértice zero (o que não é muito útil):

```glsl
void main()
{
    gl_Position = vec4(0.0,0.0,0.0,1.0);
}
```

Um exemplo mais completo é o vertex shader de sprite integrado:

```glsl
-- sprite.vp
uniform mediump mat4 view_proj;             // [1]

attribute mediump vec4 position;            // [2]
attribute mediump vec2 texcoord0;

varying mediump vec2 var_texcoord0;         // [3]

void main()
{
  gl_Position = view_proj * vec4(position.xyz, 1.0);    // [4]
  var_texcoord0 = texcoord0;                            // [5]
}
```
1. Um uniform (constante) contendo as matrizes de visualização e projeção multiplicadas.
2. Attributes para o vértice do sprite. `position` já está transformado em espaço de mundo. `texcoord0` contém a coordenada UV do vértice.
3. Declara uma variável de saída varying. Essa variável será interpolada para cada fragmento entre os valores definidos para cada vértice e enviada ao fragment shader.
4. `gl_Position` é definido como a posição de saída do vértice atual no espaço de projeção. Esse valor tem 4 componentes: `x`, `y`, `z` e `w`. O componente `w` é usado para calcular interpolação correta em perspectiva. Esse valor normalmente é 1.0 para cada vértice antes de qualquer matriz de transformação ser aplicada.
5. Define a coordenada UV varying para esta posição de vértice. Após a rasterização, ela será interpolada para cada fragmento e enviada ao fragment shader.




Após o vertex shading, a forma na tela do componente é decidida: formas primitivas são geradas e rasterizadas, o que significa que o hardware gráfico divide cada forma em *fragmentos*, ou pixels. Ele então executa o programa de fragment shader, uma vez para cada fragmento. Para uma imagem na tela com tamanho de 16x24 pixels, o programa roda 384 vezes, cada execução em paralelo.

![fragment shader](images/shader/fragment_shader.png)

A entrada do programa é tudo o que o pipeline de renderização e o vertex shader enviam, normalmente as *coordenadas uv* do fragmento, cores de tint etc. A saída é a cor final do pixel (`gl_FragColor`).

O programa de fragment shader mais simples apenas define a cor de cada pixel como preto (novamente, não é um programa muito útil):

```glsl
void main()
{
    gl_FragColor = vec4(0.0,0.0,0.0,1.0);
}
```

Novamente, um exemplo mais completo é o fragment shader de sprite integrado:

```glsl
// sprite.fp
varying mediump vec2 var_texcoord0;             // [1]

uniform lowp sampler2D DIFFUSE_TEXTURE;         // [2]
uniform lowp vec4 tint;                         // [3]

void main()
{
  lowp vec4 tint_pm = vec4(tint.xyz * tint.w, tint.w);          // [4]
  lowp vec4 diff = texture2D(DIFFUSE_TEXTURE, var_texcoord0.xy);// [5]
  gl_FragColor = diff * tint_pm;                                // [6]
}
```
1. A variável varying de coordenada de textura é declarada. O valor dessa variável será interpolado para cada fragmento entre os valores definidos para cada vértice da forma.
2. Uma variável uniform `sampler2D` é declarada. O sampler, junto com as coordenadas de textura interpoladas, é usado para realizar uma consulta de textura para que o sprite receba textura corretamente. Como este é um sprite, a engine atribuirá este sampler à imagem definida na propriedade *Image* do sprite.
3. Uma constante do tipo `CONSTANT_TYPE_USER` é definida no material e declarada como `uniform`. Seu valor é usado para permitir tingimento de cor no sprite. O padrão é branco puro.
4. O valor de cor do tint é pré-multiplicado pelo valor alpha, pois todas as texturas em runtime já contêm alpha pré-multiplicado.
5. Amostra a textura na coordenada interpolada e retorna o valor amostrado.
6. `gl_FragColor` é definido para a cor de saída do fragmento: a cor difusa da textura multiplicada pelo valor de tint.

O valor de fragmento resultante então passa por testes. Um teste comum é o *depth test*, em que o valor de profundidade do fragmento é comparado ao valor do depth buffer para o pixel que está sendo testado. Dependendo do teste, o fragmento pode ser descartado ou um novo valor é escrito no depth buffer. Um uso comum desse teste é permitir que gráficos mais próximos da câmera bloqueiem gráficos mais distantes.

Se o teste concluir que o fragmento deve ser escrito no frame buffer, ele será *misturado* com os dados de pixel já presentes no buffer. Parâmetros de blending definidos no script de renderização permitem que a cor de origem (o valor escrito pelo fragment shader) e a cor de destino (a cor da imagem no framebuffer) sejam combinadas de várias formas. Um uso comum de blending é permitir a renderização de objetos transparentes.

## Estudos adicionais

- [Shadertoy](https://www.shadertoy.com) contém um número enorme de shaders contribuídos por usuários. É uma ótima fonte de inspiração onde você pode aprender sobre várias técnicas de shading. Muitos shaders apresentados no site podem ser portados para o Defold com muito pouco trabalho. O [tutorial Shadertoy](https://www.defold.com/tutorials/shadertoy/) percorre as etapas de conversão de um shader existente para o Defold.

- O [tutorial Grading](https://www.defold.com/tutorials/grading/) mostra como criar um efeito de gradação de cor em tela cheia usando texturas de tabela de consulta de cores para a gradação.

- [The Book of Shaders](https://thebookofshaders.com/00/) ensinará como usar e integrar shaders aos seus projetos, melhorando o desempenho e a qualidade gráfica deles.
