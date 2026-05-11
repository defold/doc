---
title: Tutorial de Shadertoy para Defold
brief: Neste tutorial, você converterá um shader do shadertoy.com para o Defold.
---

# Tutorial Shadertoy

[Shadertoy.com](https://www.shadertoy.com/) é um site que reúne shaders GL contribuídos por usuários. É um ótimo recurso para encontrar código de shader e inspiração. Neste tutorial, vamos pegar um shader do Shadertoy e fazê-lo rodar no Defold. Presume-se algum entendimento básico de shaders. Se você precisar estudar o assunto, [o manual de Shader](/manuals/shader/) é um bom ponto de partida.

O shader que usaremos é [Star Nest](https://www.shadertoy.com/view/XlfGRj), de Pablo Andrioli (usuário "Kali" no Shadertoy). É um fragment shader procedural puramente matemático, quase uma magia negra, que renderiza um efeito de campo estelar muito interessante.

![Star Nest](images/shadertoy/starnest.png)

O shader tem apenas 65 linhas de código GLSL bastante complicado, mas não se preocupe. Vamos tratá-lo como uma caixa-preta que faz seu trabalho com base em algumas entradas simples. Nosso trabalho aqui é modificar o shader para que ele se conecte ao Defold em vez do Shadertoy.

## Algo para texturizar

O shader Star Nest é um fragment shader puro, então precisamos apenas de algo para o shader texturizar. Há várias opções: um sprite, um tilemap, uma GUI ou um modelo. Neste tutorial, usaremos um modelo 3D simples. O motivo é que podemos transformar facilmente a renderização do modelo em um efeito de tela cheia---algo que precisamos fazer se quisermos aplicar pós-processamento visual, por exemplo.

Começamos criando uma malha de plano quadrado no Blender (ou em qualquer outro programa de modelagem 3D). Por conveniência, as 4 coordenadas dos vértices estão em -1 e 1 no eixo X, e -1 e 1 no eixo Y. O Blender usa o eixo Z apontando para cima por padrão, então você precisa girar a malha 90° ao redor do eixo X. Você também deve garantir que gerou coordenadas UV corretas para a malha. No Blender, entre no *Edit Mode* com a malha selecionada e então selecione <kbd>Mesh ▸ UV unwrap... ▸ Unwrap</kbd>.


[Baixar quad.dae](https://github.com/defold/template-basic-3d/blob/master/assets/meshes/quad.dae)


::: sidenote
Blender é um software 3D gratuito e open-source que pode ser baixado em [blender.org](https://www.blender.org).
:::

![quad in Blender](images/shadertoy/quad_blender.png)

1. Abra o arquivo "main.collection" no Defold e crie um novo objeto de jogo "star-nest".
2. Adicione um componente *Model* a "star-nest".
3. Defina a propriedade *Mesh* para o arquivo *`quad.gltf`* encontrado em `builtins/assets/meshes`.
4. O modelo é pequeno (2⨉2 unidades), então precisamos escalar o objeto de jogo "star-nest" para um tamanho razoável. 600⨉600 é um bom tamanho grande, então defina a escala X e Y como 300.

O modelo deve aparecer no editor de cena, mas ele é renderizado todo preto. Isso acontece porque ele ainda não tem material definido:

![quad in Defold](images/shadertoy/quad_no_material.png)

## Criando o material

Crie um novo arquivo de material *`star-nest.material`*, um programa de vertex shader *`star-nest.vp`* e um programa de fragment shader *`star-nest.fp`*:

1. Abra *star-nest.material*.
2. Defina o *Vertex Program* como `star-nest.vp`.
3. Defina o *Fragment Program* como `star-nest.fp`.
4. Adicione uma *Vertex Constant* e nomeie-a como "`view_proj`" (de "view projection").
5. Defina seu *Type* como `CONSTANT_TYPE_VIEWPROJ`.
6. Adicione uma tag "tile" em *Tags*. Isso faz com que o quad seja incluído no render pass quando sprites e tiles forem desenhados.

    ![material](images/shadertoy/material.png)

7. Abra o arquivo do programa de vertex shader *`star-nest.vp`*. Ele deve conter o código a seguir. Deixe o código como está.

    ```glsl
    // star-nest.vp
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

8. Abra o arquivo do programa de fragment shader *`star-nest.fp`* e modifique o código para que a cor do fragmento seja definida com base nas coordenadas X e Y das coordenadas UV (`var_texcoord0`). Fazemos isso para garantir que o modelo esteja configurado corretamente:

    ```glsl
    // star-nest.fp
    varying mediump vec2 var_texcoord0;

    void main()
    {
        gl_FragColor = vec4(var_texcoord0.xy, 0.0, 1.0);
    }
    ```

9. Defina o material no componente de modelo do objeto de jogo "star-nest".

Agora o editor deve renderizar o modelo com o novo shader, e podemos ver claramente se as coordenadas UV estão corretas: o canto inferior esquerdo deve ter cor preta (0, 0, 0), o canto superior esquerdo deve ter cor verde (0, 1, 0), o canto superior direito deve ter cor amarela (1, 1, 0) e o canto inferior direito deve ter cor vermelha (1, 0, 0):

![quad in Defold](images/shadertoy/quad_material.png)

## O shader Star Nest

Agora tudo está pronto para começar a trabalhar no código real do shader. Primeiro, vamos dar uma olhada no código original. Ele consiste em algumas seções:

![Star Nest shader code](images/shadertoy/starnest_code.png)

1. As linhas 5--18 definem várias constantes. Podemos deixá-las como estão.

2. As linhas 21 e 63 contêm as coordenadas X e Y de textura em screen space do fragmento de entrada (`in vec2 fragCoord`) e a cor do fragmento de saída (`out vec4 fragColor`).

    No Defold, as coordenadas de textura de entrada são passadas do vertex shader como coordenadas UV (no intervalo 0--1) por meio de uma variável varying `var_texcoord0`. A cor do fragmento de saída é definida na variável integrada `gl_FragColor`.

3. As linhas 23--27 configuram as dimensões da textura, bem como a direção do movimento e o tempo escalado. A resolução do viewport/textura é passada ao shader como `uniform vec3 iResolution`. O shader calcula coordenadas no estilo UV com a proporção correta a partir das coordenadas do fragmento e da resolução. Também é feito algum deslocamento da resolução para obter um enquadramento melhor.

    A versão para Defold precisa alterar esses cálculos para usar as coordenadas UV de `var_texcoord0`.

    O tempo também é configurado aqui. Ele é passado ao shader como `uniform float iGlobalTime`. Atualmente, o Defold não suporta uniforms `float`, então precisamos fornecer o tempo por meio de um `vec4`.

4. As linhas 29--39 configuram a rotação da renderização volumétrica, com a posição do mouse afetando a rotação. As coordenadas do mouse são passadas ao shader como `uniform vec4 iMouse`.

    Neste tutorial, vamos ignorar a entrada do mouse.

5. As linhas 41--62 são o núcleo do shader. Podemos deixar esse código como está.

## O shader Star Nest modificado

Percorrer as seções acima e fazer as alterações necessárias resulta no código de shader a seguir. Ele foi limpo um pouco para melhorar a legibilidade. As diferenças entre as versões do Defold e do Shadertoy são anotadas:

```glsl
// Star Nest by Pablo Román Andrioli
// This content is under the MIT License.

#define iterations 17
#define formuparam 0.53

#define volsteps 20
#define stepsize 0.1

#define zoom   0.800
#define tile   0.850
#define speed  0.010

#define brightness 0.0015
#define darkmatter 0.300
#define distfading 0.730
#define saturation 0.850

varying mediump vec2 var_texcoord0; // <1>

void main() // <2>
{
    // get coords and direction
    vec2 res = vec2(1.0, 1.0); // <3>
    vec2 uv = var_texcoord0.xy * res.xy - 0.5;
    vec3 dir = vec3(uv * zoom, 1.0);
    float time = 0.0; // <4>

    float a1=0.5; // <5>
    float a2=0.8;
    mat2 rot1=mat2(cos(a1),sin(a1),-sin(a1),cos(a1));
    mat2 rot2=mat2(cos(a2),sin(a2),-sin(a2),cos(a2));
    dir.xz*=rot1;
    dir.xy*=rot2;
    vec3 from = vec3(1.0, 0.5, 0.5);
    from += vec3(time * 2.0, time, -2.0);
    from.xz *= rot1;
    from.xy *= rot2;

    //volumetric rendering
    float s = 0.1, fade = 1.0;
    vec3 v = vec3(0.0);
    for(int r = 0; r < volsteps; r++) {
        vec3 p = from + s * dir * 0.5;
        // tiling fold
        p = abs(vec3(tile) - mod(p, vec3(tile * 2.0)));
        float pa, a = pa = 0.0;
        for (int i=0; i < iterations; i++) {
            // the magic formula
            p = abs(p) / dot(p, p) - formuparam;
            // absolute sum of average change
            a += abs(length(p) - pa);
            pa = length(p);
        }
        //dark matter
        float dm = max(0.0, darkmatter - a * a * 0.001);
        a *= a * a;
        // dark matter, don't render near
        if(r > 6) fade *= 1.0 - dm;
        v += fade;
        // coloring based on distance
        v += vec3(s, s * s, s * s * s * s) * a * brightness * fade;
        fade *= distfading;
        s += stepsize;
    }
    // color adjust
    v = mix(vec3(length(v)), v, saturation);
    gl_FragColor = vec4(v * 0.01, 1.0); // <6>
}
```
1. O vertex shader define uma varying `var_texcoord0` com as coordenadas UV. Precisamos declará-la.
2. O Shadertoy tem um ponto de entrada `void mainImage(out vec4 fragColor, in vec2 fragCoord)`. No Defold, não recebemos parâmetros em `main()`. Então, em vez disso, lemos a varying `var_texcoord0` e escrevemos em `gl_FragColor`.
3. Para este tutorial, definimos uma resolução estática para a renderização. Atualmente, o modelo é quadrado, então podemos usar `vec2 = vec2(1.0, 1.0);`. Com um modelo retangular de tamanho 1280⨉720, em vez disso definimos `vec2 res = vec2(1.78, 1.0);` e multiplicamos as coordenadas uv por isso para obter a proporção correta.
4. Por enquanto, `time` é definido como zero. Adicionaremos tempo na próxima etapa.
5. Manteremos este tutorial simples removendo completamente os valores de `iMouse`. Observe que ainda usamos os cálculos de rotação para reduzir a simetria visual na renderização volumétrica.
6. Por fim, defina a cor de fragmento resultante.

Salve o programa de fragment shader. O modelo agora deve estar bem texturizado com um campo estelar no editor Scene:

![quad with starnest](images/shadertoy/quad_starnest.png)


## Animação

A peça final do quebra-cabeça é introduzir tempo para fazer as estrelas se moverem. Para passar um valor de tempo ao shader, precisamos usar uma constante de shader, uma uniform. Para configurar uma nova constante:

1. Abra *star-nest.material*.
2. Adicione uma *Fragment Constant* e nomeie-a como "time".
3. Defina seu *Type* como `CONSTANT_TYPE_USER`. Deixe os componentes x, y, z e w em 0.

![time constant](images/shadertoy/time_constant.png)

Agora precisamos modificar o código do shader para declarar e usar a nova constante:

```glsl
...
varying mediump vec2 var_texcoord0;
uniform lowp vec4 time; // <1>

void main()
{
    //get coords and direction
    vec2 res = vec2(2.0, 1.0);
    vec2 uv = var_texcoord0.xy * res.xy - 0.5;
    vec3 dir = vec3(uv * zoom, 1.0);
    float time = time.x * speed + 0.25; // <2>
    ...
```
1. Declare uma nova uniform do tipo `vec4` com o nome "time". Deve bastar mantê-la em `lowp` (Low precision).
2. Leia o componente `x` da uniform de tempo e use-o para calcular um valor de tempo.

O passo final é alimentar o shader com um valor de tempo:

1. Crie um novo arquivo de script *`star-nest.script`*.
2. Insira o seguinte código:

```lua
function init(self)
    self.t = 0 -- <1>
end

function update(self, dt)
    self.t = self.t + dt -- <2>
    go.set("#model", "time", vmath.vector4(self.t, 0, 0, 0)) -- <3>
end
```
1. Armazene um valor `t` no componente de script (`self`) e inicialize-o com 0.
2. A cada frame, aumente o valor de `self.t` pelo número de segundos que se passou desde o último frame. Esse valor está disponível pelo parâmetro `dt` (delta time) e é 1/60 (`update()` é chamado 60 vezes por segundo).
3. Defina a constante "time" no componente de modelo. A constante é um `vector4`, então usamos o componente `x` para o valor de tempo.
4. Por fim, adicione *star-nest.script* como componente de script ao objeto de jogo "star-nest":

    ![script component](images/shadertoy/script_component.png)

E é isso! Terminamos!

Um exercício divertido de continuação é adicionar ao shader a entrada original de movimento do mouse. Deve ser bem direto se você entender como lidar com entrada.

Boas criações com Defold!
