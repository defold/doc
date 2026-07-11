---
title: Tutorial de shader de grading
brief: Neste tutorial, você criará um efeito de pós-processamento em tela cheia no Defold.
---

# Tutorial de grading

Neste tutorial, vamos criar um efeito de pós-processamento de color grading em tela cheia. O método básico de renderização usado é amplamente aplicável a vários tipos de pós-efeitos, como blur, trails, glow, ajustes de cor e assim por diante.

Assumimos que você sabe se orientar no editor Defold e que tem entendimento básico de shaders GL e do pipeline de renderização do Defold. Se precisar estudar esses assuntos, confira [nosso manual de Shader](/manuals/shader/) e o [manual de Render](/manuals/render/).

## Render targets

Com o script de renderização padrão, cada componente visual (sprite, tilemap, efeito de partículas, GUI etc.) é renderizado diretamente no *frame buffer* da placa gráfica. O hardware então faz os gráficos aparecerem na tela. O desenho real dos pixels de um componente é feito por um *shader program* GL. O Defold vem com um shader program padrão para cada tipo de componente, que desenha os dados de pixel na tela sem alterações. Normalmente, esse é o comportamento desejado---suas imagens devem aparecer na tela como foram originalmente concebidas.

Você pode substituir o shader program de um componente por outro que modifica os dados de pixel ou cria cores de pixel totalmente novas de forma programática. O [tutorial Shadertoy](/tutorials/shadertoy) ensina como fazer isso.

Agora imagine que você quer renderizar todo o seu jogo em preto e branco. Uma solução possível é modificar o shader program individual para cada tipo de componente, para que cada shader dessature as cores dos pixels. Atualmente, o Defold vem com 6 materiais integrados e 6 pares de programas de vertex e fragment shader, então isso daria uma boa quantidade de trabalho. Além disso, quaisquer alterações ou adições de efeito posteriores teriam que ser feitas em cada shader program.

Uma abordagem muito mais flexível é fazer a renderização em duas etapas separadas:

![Render target](images/grading/render_target.png)

1. Desenhe todos os componentes como de costume, mas desenhe-os em um buffer fora da tela em vez do frame buffer comum. Você faz isso desenhando para algo chamado *render target*.
2. Desenhe um polígono quadrado no frame buffer e use os dados de pixel armazenados no render target como a fonte de textura do polígono. Certifique-se também de que o polígono quadrado seja esticado para cobrir toda a tela.

Com esse método, conseguimos ler os dados visuais resultantes e modificá-los antes que cheguem à tela. Ao adicionar shader programs à etapa 2 acima, podemos obter efeitos de tela cheia com facilidade. Vamos ver como configurar isso no Defold.

## Configurando um renderizador personalizado

Precisamos modificar o script de renderização integrado e adicionar a nova funcionalidade de renderização. O script de renderização padrão é um bom ponto de partida, então comece copiando-o:

1. Copie */builtins/render/default.render_script*: na visualização *Asset*, clique com o botão direito em *default.render_script*, selecione <kbd>Copy</kbd>, depois clique com o botão direito em *main* e selecione <kbd>Paste</kbd>. Clique com o botão direito na cópia, selecione <kbd>Rename...</kbd> e dê a ela um nome adequado, como "grade.render_script".
2. Crie um novo arquivo de renderização chamado */main/grade.render* clicando com o botão direito em *main* na visualização *Asset* e selecionando <kbd>New ▸ Render</kbd>.
3. Abra *grade.render* e defina sua propriedade *Script* como "/main/grade.render_script".

   ![grade.render](images/grading/grade_render.png)

4. Abra *game.project* e defina *Render* como "/main/grade.render".

   ![game.project](images/grading/game_project.png)

Agora o jogo está configurado para rodar com um novo pipeline de renderização que podemos modificar. Para testar se nossa cópia do script de renderização é usada pela engine, execute o jogo, faça uma modificação no script de renderização que gere um resultado visual e então recarregue o script. Por exemplo, você pode desabilitar o desenho de tiles e sprites e então pressionar <kbd>⌘ + R</kbd> para fazer hot reload do script de renderização "quebrado" no jogo em execução:

```lua
...

render.set_projection(vmath.matrix4_orthographic(0, render.get_width(), 0, render.get_height(), -1, 1))

-- render.draw(self.tile_pred) -- <1>
render.draw(self.particle_pred)
render.draw_debug3d()

...
```
1. Comente o desenho do predicado "tile", que inclui todos os sprites e tiles. Esta linha de código pode ser encontrada por volta da linha 33 no arquivo do script de renderização.

Se os sprites e tiles desaparecerem com esse teste simples, você sabe que o jogo está usando seu script de renderização. Se tudo funcionar como esperado, pode desfazer a alteração no script de renderização.

## Desenhando em um alvo fora da tela

Agora vamos modificar o script de renderização para que ele desenhe no render target fora da tela em vez do frame buffer. Primeiro precisamos criar o render target:

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})

    self.clear_color = vmath.vector4(0, 0, 0, 0)
    self.clear_color.x = sys.get_config_number("render.clear_color_red", 0)
    self.clear_color.y = sys.get_config_number("render.clear_color_green", 0)
    self.clear_color.z = sys.get_config_number("render.clear_color_blue", 0)
    self.clear_color.w = sys.get_config_number("render.clear_color_alpha", 0)

    self.view = vmath.matrix4()

    local color_params = { format = graphics.TEXTURE_FORMAT_RGBA,
                       width = render.get_width(),
                       height = render.get_height() } -- <1>
    local target_params = {[render.BUFFER_COLOR_BIT] = color_params }

    self.target = render.render_target("original", target_params) -- <2>
end
```
1. Configure os parâmetros do color buffer para o render target. Usamos a resolução-alvo do jogo.
2. Crie o render target com os parâmetros do color buffer.

Agora só precisamos envolver o código de renderização original com `render.set_render_target()` assim:

```lua
function update(self)
  render.set_render_target(self.target) -- <1>

  render.set_depth_mask(true)
  render.set_stencil_mask(0xff)
  render.clear({[render.BUFFER_COLOR_BIT] = self.clear_color, [render.BUFFER_DEPTH_BIT] = 1, [render.BUFFER_STENCIL_BIT] = 0})

  render.set_viewport(0, 0, render.get_width(), render.get_height()) -- <2>
  render.set_view(self.view)
  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT) -- <3>
end
```
1. Habilite o render target. A partir de agora, cada chamada a `render.draw()` desenhará nos buffers do nosso render target fora da tela.
2. Todo o código de desenho original em `update()` é mantido como está, exceto pelo viewport, que é definido para a resolução do render target.
3. Neste ponto, todos os gráficos do jogo foram desenhados no render target. Então é hora de desabilitá-lo definindo o render target padrão.

Isso é tudo de que precisamos. Se você executar o jogo agora, ele desenhará tudo no render target. Mas, como agora não desenhamos nada no frame-buffer, veremos apenas uma tela preta.

## Algo para preencher a tela

Para desenhar os pixels do color buffer do render target na tela, precisamos configurar algo que possamos texturizar com esses dados de pixel. Para isso, usaremos um modelo 3D plano e quadrado.

1. Abra *`main.collection`* e crie um novo objeto de jogo chamado "`grade`".
2. Adicione um componente Model ao objeto de jogo "`grade`".
3. Defina a propriedade *Mesh* do componente de modelo para o arquivo *`quad.gltf`* encontrado em `builtins/assets/meshes`.

Deixe o objeto de jogo sem escala e na origem. Mais tarde, ao renderizar o quad, vamos projetá-lo para que preencha a tela inteira. Mas primeiro precisamos de um material e de shader programs para o quad:

1. Crie um novo material e chame-o de *`grade.material`* clicando com o botão direito em *main* na visualização *Asset* e selecionando <kbd>New ▸ Material</kbd>.
2. Crie um programa de vertex shader chamado *`grade.vp`* e um programa de fragment shader chamado *`grade.fp`* clicando com o botão direito em *main* na visualização *Asset* e selecionando <kbd>New ▸ Vertex program</kbd> e <kbd>New ▸ Fragment program</kbd>.
3. Abra *grade.material* e defina as propriedades *Vertex program* e *Fragment program* para os novos arquivos de shader program.
4. Adicione uma *Vertex constant* chamada "`view_proj`" do tipo `CONSTANT_TYPE_VIEWPROJ`. Essa é a matriz de view e projeção usada no vertex program para os vértices do quad.
5. Adicione um *Sampler* chamado "`original`". Ele será usado para amostrar pixels do color buffer do render target fora da tela.
6. Adicione uma *Tag* chamada "`grade`". Criaremos um novo *render predicate* no script de renderização que corresponda a essa tag para desenhar o quad.

   ![grade.material](images/grading/grade_material.png)

7. Abra *`main.collection`*, selecione o componente de modelo no objeto de jogo "`grade`" e defina sua propriedade *Material* como "`/main/grade.material`".

   ![model properties](images/grading/model_properties.png)

8. O programa de vertex shader pode ser deixado como foi criado a partir do template base:

    ```glsl
    // grade.vp
    uniform mediump mat4 view_proj;

    // positions are in world space
    attribute mediump vec4 position;
    attribute mediump vec2 texcoord0;

    varying mediump vec2 var_texcoord0;

    void main()
    {
      gl_Position = view_proj * vec4(position.xyz, 1.0);
      var_texcoord0 = texcoord0;
    }
    ```

9. No programa de fragment shader, em vez de definir `gl_FragColor` diretamente para o valor de cor amostrado, vamos realizar uma manipulação de cor simples. Fazemos isso principalmente para garantir que tudo funcione como esperado até aqui:

    ```glsl
    // grade.fp
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;

    void main()
    {
      vec4 color = texture2D(original, var_texcoord0.xy);
      // Dessatura a cor amostrada da textura original
      float grey = color.r * 0.3 + color.g * 0.59 + color.b * 0.11;
      gl_FragColor = vec4(grey, grey, grey, 1.0);
    }
    ```

Agora temos o modelo quad no lugar com seu material e shaders. Só precisamos desenhá-lo no frame buffer da tela.

## Texturizando com o buffer fora da tela

Precisamos adicionar um render predicate ao script de renderização para podermos desenhar o modelo quad. Abra *`grade.render_script`* e edite a função `init()`:

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})
    self.grade_pred = render.predicate({"grade"}) -- <1>

    ...
end
```
1. Adicione um novo predicado correspondente à tag "grade" que definimos em *`grade.material`*.

Depois que o color buffer do render target for preenchido em `update()`, configuramos uma view e uma projeção que fazem o modelo quad preencher a tela inteira. Então usamos o color buffer do render target como textura do quad:

```lua
function update(self)
  render.set_render_target(self.target)

  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT)

  render.clear({[render.BUFFER_COLOR_BIT] = self.clear_color}) -- <1>

  render.set_viewport(0, 0, render.get_window_width(), render.get_window_height()) -- <2>
  render.set_view(vmath.matrix4()) -- <3>
  render.set_projection(vmath.matrix4())

  render.enable_texture(0, self.target, render.BUFFER_COLOR_BIT) -- <4>
  render.draw(self.grade_pred) -- <5>
  render.disable_texture(0, self.target) -- <6>
end
```
1. Limpe o frame buffer. Observe que a chamada anterior a `render.clear()` afeta o render target, não o frame buffer da tela.
2. Defina o viewport para corresponder ao tamanho da janela.
3. Defina a view como a matriz identidade. Isso significa que a câmera está na origem olhando diretamente ao longo do eixo Z. Também defina a projeção como a matriz identidade, fazendo com que o quad seja projetado plano por toda a tela.
4. Defina o slot de textura 0 para o color buffer do render target. Temos o sampler "original" no slot 0 em nosso *`grade.material`*, então o fragment shader amostrará a partir do render target.
5. Desenhe o predicado que criamos, correspondente a qualquer material com a tag "grade". O modelo quad usa *`grade.material`*, que define essa tag---assim, o quad será desenhado.
6. Depois de desenhar, desabilite o slot de textura 0, já que terminamos de desenhar com ele.

Agora vamos executar o jogo e ver o resultado:

![desaturated game](images/grading/desaturated_game.png)

## Color grading

Cores são expressas como valores de três componentes, em que cada componente determina a quantidade de vermelho, verde ou azul de uma cor. O espectro completo de cores, do preto, passando por vermelho, verde, azul, amarelo e rosa até o branco, pode caber em uma forma de cubo:

![color cube](images/grading/color_cube.png)

Qualquer cor que pode ser exibida na tela pode ser encontrada nesse cubo de cores. A ideia básica do color grading é usar esse cubo de cores, mas com cores alteradas, como uma *lookup table* 3D.

Para cada pixel:

1. Procure a posição da sua cor no cubo de cores (com base nos valores de vermelho, verde e azul).
2. *Leia* qual cor o cubo com grading armazenou nessa localização.
3. Desenhe o pixel na cor lida em vez da cor original.

Podemos fazer isso em nosso fragment shader:

1. Amostre o valor de cor de cada pixel no buffer fora da tela.
2. Procure a posição da cor do pixel amostrado em um cubo de cores com color grading.
3. Defina a cor do fragmento de saída para o valor encontrado.

![render target grading](images/grading/render_target_grading.png)

## Representando a lookup table

Open GL ES 2.0 não suporta texturas 3D, então precisamos encontrar outra forma de representar o cubo de cores 3D. Uma forma comum de fazer isso é fatiar o cubo ao longo do eixo Z (azul) e colocar cada fatia lado a lado em uma grade bidimensional. Cada uma das 16 fatias contém uma grade de 16⨉16 pixels. Armazenamos isso em uma textura que podemos ler no fragment shader com um sampler:

![lookup texture](images/grading/lut.png)

A textura resultante contém 16 células (uma para cada intensidade de cor azul) e, dentro de cada célula, 16 cores vermelhas ao longo do eixo X e 16 cores verdes ao longo do eixo Y. A textura representa todo o espaço de cores RGB de 16 milhões de cores em apenas 4096 cores---meros 4 bits de profundidade de cor. Pela maioria dos padrões, isso é ruim, mas graças a um recurso do hardware gráfico GL podemos recuperar uma precisão de cor muito alta. Vamos ver como.

## Procurando cores

Procurar uma cor é uma questão de verificar o componente azul e descobrir de qual célula pegar os valores vermelho e verde. A fórmula para encontrar a célula com o conjunto correto de cores vermelho-verde é simples:

```math
cell = \left \lfloor{B \times (N - 1)} \right \rfloor
```

Aqui, `B` é o valor do componente azul entre 0 e 1, e `N` é o número total de células. No nosso caso, o número da célula ficará no intervalo `0`--`15`, em que a célula `0` contém todas as cores com o componente azul em `0` e a célula `15` contém todas as cores com o componente azul em `1`.

Por exemplo, o valor RGB `(0.63, 0.83, 0.4)` é encontrado na célula que contém todas as cores com valor azul de `0.4`, que é a célula número 6. Sabendo disso, a busca das coordenadas finais de textura com base nos valores verde e vermelho é direta:

![lookup table](images/grading/lut_lookup.png)

Observe que precisamos tratar os valores vermelho e verde `(0, 0)` como estando no *centro* do pixel inferior esquerdo, e os valores `(1.0, 1.0)` como estando no *centro* do pixel superior direito.

::: sidenote
O motivo de lermos começando no centro do pixel inferior esquerdo e indo até o centro do pixel superior direito é que não queremos que pixels fora da célula atual afetem o valor amostrado. Veja abaixo sobre filtragem.
:::

Ao amostrar nessas coordenadas específicas na textura, vemos que acabamos exatamente entre 4 pixels. Então que valor de cor o GL nos dirá que esse ponto tem?

![lookup table filtering](images/grading/lut_filtering.png)

A resposta depende de como especificamos a *filtering* do sampler no material.

- Se a filtragem do sampler for `NEAREST`, o GL retornará o valor de cor do pixel mais próximo (valor de posição arredondado para baixo). No caso acima, o GL retornará o valor de cor na posição `(0.60, 0.80)`. Para nossa textura de lookup de 4 bits, isso significa que quantizaremos os valores de cor em apenas 4096 cores no total.

- Se a filtragem do sampler for `LINEAR`, o GL retornará o valor de cor *interpolado*. O GL misturará uma cor com base na distância até os pixels ao redor da posição de amostra. No caso acima, o GL retornará uma cor composta por 25% de cada um dos 4 pixels ao redor do ponto de amostra.

Assim, ao usar filtragem linear, eliminamos a quantização de cores e obtemos precisão de cor muito boa a partir de uma lookup table relativamente pequena.

## Implementando a busca

Vamos implementar a busca na textura no fragment shader:

1. Abra *`grade.material`*.
2. Adicione um segundo sampler chamado "`lut`" (de lookup table).
3. Defina a propriedade *`Filter min`* como `FILTER_MODE_MIN_LINEAR` e a propriedade *`Filter mag`* como `FILTER_MODE_MAG_LINEAR`.

    ![lookup table sampler](images/grading/material_lut_sampler.png)

4. Baixe a textura de lookup table a seguir (*`lut16.png`*) e adicione-a ao seu projeto.

    ![16 colors lookup table](images/grading/lut16.png)

5. Abra *`main.collection`* e defina a propriedade de textura *`lut`* para a textura de lookup baixada.

    ![quad model lookup table](images/grading/quad_lut.png)

6. Por fim, abra *`grade.fp`* para adicionarmos suporte a busca de cor:

    ```glsl
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;
    uniform lowp sampler2D lut; // <1>

    #define MAXCOLOR 15.0 // <2>
    #define COLORS 16.0
    #define WIDTH 256.0
    #define HEIGHT 16.0

    void main()
    {
        vec4 px = texture2D(original, var_texcoord0.xy); // <3>

        float cell = floor(px.b * MAXCOLOR); // <4>

        float half_px_x = 0.5 / WIDTH; // <5>
        float half_px_y = 0.5 / HEIGHT;

        float x_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
        float y_offset = half_px_y + px.g * (MAXCOLOR / COLORS); // <6>

        vec2 lut_pos = vec2(cell / COLORS + x_offset, y_offset); // <7>

        vec4 graded_color = texture2D(lut, lut_pos); // <8>

        gl_FragColor = graded_color; // <9>
    }
    ```
    1. Declare o sampler `lut`.
    2. Constantes para a cor máxima (15, já que começamos em 0), número de cores por canal e largura e altura da textura de lookup.
    3. Amostre uma cor de pixel (chamada `px`) da textura original (o color buffer do render target fora da tela).
    4. Calcule de qual célula ler a cor com base no valor do canal azul de `px`.
    5. Calcule deslocamentos de meio pixel para lermos a partir dos centros dos pixels.
    6. Calcule o deslocamento X e Y na textura com base nos valores vermelho e verde de `px`.
    7. Calcule a posição final da amostra na textura de lookup.
    8. Amostre a cor resultante da textura de lookup.
    9. Defina a cor na textura do quad para a cor resultante.

Atualmente, a textura de lookup table apenas retorna os mesmos valores de cor que procuramos. Isso significa que o jogo deve ser renderizado com sua coloração original:

![world original look](images/grading/world_original.png)

Até aqui, parece que fizemos tudo certo, mas há um problema escondido sob a superfície. Veja o que acontece quando adicionamos um sprite com uma textura de teste em gradiente:

![blue banding](images/grading/blue_banding.png)

O gradiente azul mostra um banding bem feio. Por quê?

## Interpolando o canal azul

O problema do banding no canal azul é que o GL não consegue realizar nenhuma interpolação do canal azul ao ler a cor da textura. Pré-selecionamos uma célula específica para ler com base no valor da cor azul, e pronto. Por exemplo, se o canal azul contiver um valor em qualquer ponto do intervalo `0.400`--`0.466`, o valor não importa---sempre amostraremos a cor final da célula número 6, onde o canal azul está definido como `0.400`.

Para obter melhor resolução no canal azul, podemos implementar a interpolação nós mesmos. Se o valor azul estiver entre os valores de duas células adjacentes, podemos amostrar de ambas e então misturar as cores. Por exemplo, se o valor azul for `0.420`, devemos amostrar da célula número 6 *e* da célula número 7, e então misturar as cores.

Então, devemos ler de duas células:

```math
cell_{low} = \left \lfloor{B \times (N - 1)} \right \rfloor
```

e:

```math
cell_{high} = \left \lceil{B \times (N - 1)} \right \rceil
```

Depois amostramos valores de cor de cada uma dessas células e interpolamos as cores linearmente, de acordo com a fórmula:

```math
color = color_{low} \times (1 - C_{frac}) + color_{high} \times C_{frac}
```

Aqui `color`~low~ é a cor amostrada da célula menor (mais à esquerda) e `color`~high~ é a cor amostrada da célula maior (mais à direita). A função GLSL `mix()` realiza essa interpolação linear para nós.

O valor `C~frac~` acima é a parte fracionária do valor do canal azul escalado para o intervalo de cores `0`--`15`:

```math
C_{frac} = B \times (N - 1) - \left \lfloor{B \times (N - 1)} \right \rfloor
```

Novamente, há uma função GLSL que nos dá a parte fracionária de um valor. Ela se chama `frac()`. A implementação final no fragment shader (*`grade.fp`*) é bem direta:

```glsl
varying mediump vec4 position;
varying mediump vec2 var_texcoord0;

uniform lowp sampler2D original;
uniform lowp sampler2D lut;

#define MAXCOLOR 15.0
#define COLORS 16.0
#define WIDTH 256.0
#define HEIGHT 16.0

void main()
{
  vec4 px = texture2D(original, var_texcoord0.xy);

    float cell = px.b * MAXCOLOR;

    float cell_l = floor(cell); // <1>
    float cell_h = ceil(cell);

    float half_px_x = 0.5 / WIDTH;
    float half_px_y = 0.5 / HEIGHT;
    float r_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
    float g_offset = half_px_y + px.g * (MAXCOLOR / COLORS);

    vec2 lut_pos_l = vec2(cell_l / COLORS + r_offset, g_offset); // <2>
    vec2 lut_pos_h = vec2(cell_h / COLORS + r_offset, g_offset);

    vec4 graded_color_l = texture2D(lut, lut_pos_l); // <3>
    vec4 graded_color_h = texture2D(lut, lut_pos_h);

    // <4>
    vec4 graded_color = mix(graded_color_l, graded_color_h, fract(cell));

    gl_FragColor = graded_color;
}
```

1. Calcule as duas células adjacentes das quais ler.
2. Calcule duas posições de lookup separadas, uma para cada célula.
3. Amostre as duas cores a partir das posições das células.
3. Misture as cores linearmente de acordo com a fração de `cell`, que é o valor da cor azul escalado.

Executar o jogo novamente com a textura de teste agora produz resultados muito melhores. O banding no canal azul desapareceu:

![blue no banding](images/grading/blue_no_banding.png)

## Aplicando grading à textura de lookup

Certo, foi muito trabalho para desenhar algo que parece exatamente igual ao mundo original do jogo. Mas essa configuração nos permite fazer algo muito interessante. Aguente firme!

1. Tire uma captura de tela do jogo em sua forma não afetada.
2. Abra a captura de tela no seu programa favorito de manipulação de imagens.
3. Aplique qualquer número de ajustes de cor (brilho, contraste, curvas de cor, balanço de branco, exposição etc.).

![world in Affinity](images/grading/world_graded_affinity.png)

4. Aplique os mesmos ajustes de cor ao arquivo de textura da lookup table (*`lut16.png`*).
5. Salve o arquivo de textura da lookup table com os ajustes de cor.
6. Substitua a textura *`lut16.png`* usada no seu projeto Defold pela versão com ajustes de cor.
7. Execute o jogo!

![world graded](images/grading/world_graded.png)

Pronto!
