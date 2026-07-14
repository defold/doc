---
brief: Neste tutorial você converterá um shader do shadertoy.com para o Defold.
layout: tutorial
locale: pt
title: Tutorial Shadertoy para Defold
---

# Tutorial Shadertoy

[Shadertoy.com](https://www.shadertoy.com/) é um site que reúne shaders GL contribuídos por usuários. É um ótimo recurso para encontrar código de shader e inspiração. Neste tutorial, vamos pegar um shader do Shadertoy e fazê-lo rodar no Defold. Presume-se algum entendimento básico de shaders. Se você precisar estudar o assunto, [o manual de Shader](/manuals/shader/) é um bom ponto de partida.

O shader que usaremos é [Star Nest](https://www.shadertoy.com/view/XlfGRj), de Pablo Andrioli (usuário "Kali" no Shadertoy). É um fragment shader procedural puramente matemático que renderiza um efeito de campo estelar muito interessante.

![Star Nest](../images/shadertoy/starnest.png)

O shader tem apenas 65 linhas de código GLSL bastante complicado, mas não se preocupe. Vamos tratá-lo como uma caixa-preta que faz seu trabalho com base em algumas entradas simples. Nosso trabalho aqui é modificar o shader para que ele se conecte ao Defold em vez do Shadertoy.

## Algo para texturizar

O shader Star Nest é um fragment shader puro, então precisamos apenas de algo para o shader texturizar. Há várias opções: um sprite, um tilemap, uma GUI ou um modelo. Neste tutorial, usaremos um modelo 3D simples. O motivo é que podemos transformar facilmente a renderização do modelo em um efeito de tela cheia---algo que precisamos fazer se quisermos aplicar pós-processamento visual, por exemplo.

Podemos começar a partir de um projeto vazio.

1. Abra o Defold e selecione Create From *Templates*.
2. Selecione *Empty Project*.
3. Defina o *Title* e selecione uma *Location* no seu disco.
4. Clique em <kbd>Create New Project</kbd>.

![start](../images/shadertoy/empty_project.png)

Você pode usar uma malha `quad.gltf` embutida em `builtins/assets/meshes`.

Opcionalmente, você também pode criar uma malha de plano quadrado no Blender, ou em qualquer outro programa de modelagem 3D --- por conveniência, as 4 coordenadas dos vértices ficam em -1 e 1 no eixo X, e -1 e 1 no eixo Y. O Blender usa o eixo Z apontando para cima por padrão, então você precisa girar a malha 90° ao redor do eixo X. Você também deve garantir que as coordenadas UV corretas sejam geradas para a malha. No Blender, entre no *Edit Mode* com a malha selecionada e então selecione <kbd>Mesh ▸ UV unwrap... ▸ Unwrap</kbd>.

<div class='sidenote' markdown='1'>
Blender é um software 3D gratuito e open-source que pode ser baixado em [blender.org](https://www.blender.org).
</div>

![quad in Blender](../images/shadertoy/quad_blender.png)

1. Abra o arquivo "main.collection" no Defold e crie um novo objeto de jogo "star-nest".
2. Adicione um componente *Model* ao objeto de jogo "star-nest".
3. Defina a propriedade *Mesh* para nosso `quad.gltf`.
4. Precisamos definir o material do modelo, então por enquanto selecione o `model.material` embutido.

O modelo deve aparecer no editor de cena, mas é renderizado todo preto. Isso acontece porque ele ainda não tem textura definida:

![quad in Defold](../images/shadertoy/quad_default_material.png)

## Criando o material

1. Crie um novo arquivo de material *`star-nest.material`* clicando com <kbd>Right Mouse Button</kbd> na pasta `main` no painel `Assets`, selecionando <kbd>New</kbd>-><kbd>Material</kbd> e nomeando-o `star-nest`.

 ![material](../images/shadertoy/new_material.png)

2. Da mesma forma, crie um programa de vertex shader `star-nest.vp` e um programa de fragment shader `star-nest.fp`:
3. Abra o *star-nest.material*.
4. Defina o *Vertex Program* como `star-nest.vp`.
5. Defina o *Fragment Program* como `star-nest.fp`.
6. Adicione uma *Vertex Constant* e nomeie-a como "`view_proj`", do tipo `Viewproj` (de "view projection").
8. Adicione uma tag "tile" em *Tags*. Isso faz com que o quad seja incluído no render pass quando sprites e tiles forem desenhados.

 ![material](../images/shadertoy/material.png)

### Programa de vertex

1. Abra o arquivo do programa de vertex shader `star-nest.vp`. Ele deve conter o código a seguir:

    ```glsl
    #version 140

    // positions are in world space
    in vec4 position;
    in vec2 texcoord0;

    out vec2 var_texcoord0;

    uniform vertex_inputs
    {
        mat4 view_proj;
    };

    void main()
    {
        gl_Position = view_proj * vec4(position.xyz, 1.0);
        var_texcoord0 = texcoord0;
    }
    ```

### Programa de fragment

1. Abra o arquivo do programa de fragment shader `star-nest.fp` e modifique o código para que a cor do fragmento seja definida com base nas coordenadas X e Y das coordenadas UV (`var_texcoord0`). Fazemos isso para garantir que o modelo esteja configurado corretamente:

    ```glsl
    #version 140

    in vec2 var_texcoord0;

    out vec4 out_fragColor;

    void main()
    {
        out_fragColor = vec4(var_texcoord0.xy, 0.0, 1.0);
    }
    ```

2. Defina a propriedade `Material` para o material `star-nest` recém-criado no componente de modelo do objeto de jogo `star-nest` na `main.collection`.

Agora o editor deve renderizar o modelo com o novo shader e podemos ver claramente se as coordenadas UV estão corretas: o canto inferior esquerdo deve ter cor preta (0, 0, 0), o canto superior esquerdo deve ter cor verde (0, 1, 0), o canto superior direito deve ter cor amarela (1, 1, 0) e o canto inferior direito deve ter cor vermelha (1, 0, 0):

![quad in Defold](../images/shadertoy/quad_material.png)

## Câmera

Agora podemos executar nosso projeto (<kbd>Project</kbd>-><kbd>Build</kbd> ou o atalho <kbd>Ctrl</kbd>/<kbd>Cmd</kbd> + <kbd>B</kbd>), mas veremos uma tela preta (bem, quase, exceto talvez por um pixel minúsculo no canto inferior esquerdo). Isso acontece porque não há câmera, e o script de renderização padrão usa um fallback simples, mostrando um espaço 2D enorme, enquanto nosso modelo está na posição (0,0,0) com apenas 1 de largura.

Vamos adicionar um objeto de jogo com um componente de câmera para definir o que veremos no jogo.

1. Adicione um objeto de jogo chamado `camera` com posição (0,0,1). (É importante definir a coordenada Z como 1, para que esse objeto de jogo fique à frente do nosso modelo, já que o eixo Z agora aponta para nós na configuração 2D padrão).
2. Adicione um componente `Camera` e você verá uma prévia da câmera com nosso quad dentro. Com as propriedades padrão, temos sorte suficiente nesse cenário para não precisar alterar nada e já devemos ver o resultado correto, exceto por uma coisa - não precisamos de um frustum de câmera tão grande, então podemos reduzir o `Far Z` para `2`.

![camera](../images/shadertoy/camera.png)

Opcionalmente, podemos alterar o tipo da câmera definindo `Orthographic Projection` como `true`, e então também ajustar o `Orthographic Zoom` para algo como 600, mas nesse caso não teremos proporção automática, então nosso modelo não preencherá a tela.

## O shader Star Nest

Agora que tudo está no lugar, vamos começar a trabalhar no código real do shader. Primeiro, vamos olhar o código original. Ele consiste em algumas seções:

![Star Nest shader code](../images/shadertoy/starnest_code.png)

Usaremos um pipeline moderno com GLSL na versão 140 - para isso, declaramos a versão no topo do arquivo com `#version 140`.

1. As linhas 5--18 definem várias constantes. Podemos deixá-las como estão. Elas são constantes GLSL simples e não dependem especificamente do Shadertoy ou do Defold.

2. As linhas 21 e 63 contêm as coordenadas X e Y em espaço de tela do fragmento de entrada (`in vec2 fragCoord`) e a cor do fragmento de saída (`out vec4 fragColor`).

    O Defold passa coordenadas de textura do vertex shader para o fragment shader por meio de uma variável interpolada como coordenadas UV (no intervalo 0--1). Em nosso vertex shader isso é declarado com um qualificador `out`:

    ```glsl
    // in star-nest.vp
    out vec2 var_texcoord0;
    ```

     No fragment shader, o mesmo valor é recebido com um qualificador `in`:

    ```glsl
    // in star-nest.fp
    in vec2 var_texcoord0;
    ```

    Então, no GLSL 140, declaramos uma saída explícita do fragmento com o qualificador `out`:

    ```glsl
    // in star-nest.fp
    out vec4 out_fragColor;
    ```

    Portanto, onde o código original do Shadertoy escreve em `fragColor`, nosso shader Defold escreve em `out_fragColor`.

3. As linhas 23--27 configuram as dimensões da textura, além da direção de movimento e do tempo escalado. No Shadertoy, o shader recebe a posição do pixel por `fragCoord` e a resolução do viewport/textura é passada ao shader como `uniform vec3 iResolution`. O shader calcula coordenadas no estilo UV com a proporção correta a partir das coordenadas do fragmento e da resolução. Também é feito algum deslocamento da resolução para obter um enquadramento melhor.

    No Defold, não partimos de coordenadas de pixel. Em vez disso, já recebemos coordenadas UV normalizadas do vertex shader por meio de `var_texcoord0`. Essas coordenadas estão no intervalo de `0.0` a `1.0` ao longo do quad renderizado.

    A versão para Defold precisa alterar esses cálculos para usar as coordenadas UV de `var_texcoord0`.
    Uma conversão típica se parece com isto:

    ```glsl
    vec2 uv = var_texcoord0.xy;
    uv = uv * 2.0 - 1.0;
    uv.x *= aspect;
    ```
    O valor exato de `aspect` depende de como o exemplo está configurado. Se o efeito for renderizado em um quad de tela cheia com tamanho de display conhecido, a proporção pode ser codificada diretamente para o tutorial. Se o efeito precisar suportar tamanhos de janela arbitrários, passe a resolução como uma constante de fragmento e coloque-a dentro de um bloco uniform GLSL 140.

    O tempo também é configurado aqui. Ele é passado ao shader como `uniform float iGlobalTime`. O Defold (desde 1.12.3) fornece tempo aos shaders por meio de uma constante especial `Time`, que usaremos.

    No Defold moderno, uniforms não opacos são declarados dentro de blocos uniform.
    No fragment shader, nós o declaramos assim:

    ```glsl
    uniform fragment_inputs
    {
        vec4 time;
    };
    ```

    Então, no `star-nest.material`, adicionaremos uma Fragment Constant chamada `time` e definiremos seu tipo como `Time`.

    O valor pode então ser usado assim:

    ```glsl
    float iGlobalTime = time.x;
    float dt = time.y;
    ```
    onde `time.x` é o tempo desde o início da engine, e `time.y` é o delta time do frame anterior.

4. As linhas 29--39 configuram a rotação da renderização volumétrica, com a posição do mouse afetando a rotação. As coordenadas do mouse são passadas ao shader como `uniform vec4 iMouse`.

    Neste tutorial, vamos ignorar a entrada do mouse.

5. As linhas 41--62 são o núcleo do shader. Podemos deixar esse código como está.

## O shader Star Nest modificado

Percorrer as seções acima e fazer as alterações necessárias resulta no código de shader a seguir. Ele foi limpo um pouco para melhorar a legibilidade. As diferenças entre as versões do Defold e do Shadertoy são anotadas:

```glsl
#version 140 // <1>

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

in vec2 var_texcoord0; // <2>

out vec4 out_fragColor; // <3>

uniform fragment_inputs // <4>
{
	vec4 time;
};

void main() // <5>
{
	// get coords and direction
	vec2 res = vec2(1.0, 1.0); // <6>
	vec2 uv = var_texcoord0.xy * res.xy - 0.5;
	vec3 dir = vec3(uv * zoom, 1.0);

	float iGlobalTime = time.x; // <7>
	float shader_time = iGlobalTime * speed;

	float a1 = 0.5; // <8>
	float a2 = 0.8;
	mat2 rot1 = mat2(cos(a1), sin(a1), -sin(a1), cos(a1));
	mat2 rot2 = mat2(cos(a2), sin(a2), -sin(a2), cos(a2));

	dir.xz *= rot1;
	dir.xy *= rot2;

	vec3 from = vec3(1.0, 0.5, 0.5);
	from += vec3(shader_time * 2.0, shader_time, -2.0);
	from.xz *= rot1;
	from.xy *= rot2;

	// volumetric rendering
	float s = 0.1;
	float fade = 1.0;
	vec3 v = vec3(0.0);

	for (int r = 0; r < volsteps; r++) {
		vec3 p = from + s * dir * 0.5;

		// tiling fold
		p = abs(vec3(tile) - mod(p, vec3(tile * 2.0)));

		float pa = 0.0;
		float a = 0.0;

		for (int i = 0; i < iterations; i++) {
			// the magic formula
			p = abs(p) / dot(p, p) - formuparam;

			// absolute sum of average change
			a += abs(length(p) - pa);
			pa = length(p);
		}

		// dark matter
		float dm = max(0.0, darkmatter - a * a * 0.001);

		a *= a * a;

		// dark matter, don't render near
		if (r > 6) {
			fade *= 1.0 - dm;
		}

		v += fade;

		// coloring based on distance
		v += vec3(s, s * s, s * s * s * s) * a * brightness * fade;

		fade *= distfading;
		s += stepsize;
	}

	// color adjust
	v = mix(vec3(length(v)), v, saturation);

	out_fragColor = vec4(v * 0.01, 1.0); // <9>
}
```

1. Declaramos #version 140 no topo do arquivo para usar o pipeline GLSL moderno do Defold. Em seguida, deixamos os defines como estão.
2. O vertex shader passa coordenadas UV para o fragment shader por meio de var_texcoord0. No GLSL 140, o fragment shader recebe esse valor interpolado com o qualificador in.
3. No GLSL 140, o fragment shader deve declarar uma variável de saída explícita em vez de escrever em gl_FragColor. Aqui usamos out vec4 out_fragColor.
4. A constante de material Time do Defold é exposta ao shader por meio de um bloco uniform. Em star-nest.material, adicione uma Fragment Constant chamada time e defina seu tipo como Time.
5. O Shadertoy usa mainImage(out vec4 fragColor, in vec2 fragCoord). No Defold usamos o ponto de entrada normal void main(), lemos as coordenadas UV interpoladas de var_texcoord0 e escrevemos a cor final em out_fragColor.
6. Para este tutorial definimos um valor estático de resolução/proporção para a renderização. Atualmente o modelo é quadrado, então podemos usar vec2 res = vec2(1.0, 1.0);. Com um modelo retangular de tamanho 1280×720, poderíamos usar vec2 res = vec2(1.78, 1.0); e multiplicar as coordenadas UV por isso para preservar a proporção correta.
7. O shader original do Shadertoy usa iGlobalTime. Nesta versão para Defold, time.x contém o tempo desde o início da engine, então o atribuímos a uma variável local iGlobalTime e o usamos para animar o movimento da câmera pelo campo estelar.
8. Mantemos este tutorial simples removendo completamente os valores de iMouse. A rotação em si ainda é mantida, porque reduz a simetria visual na renderização volumétrica.
9. Por fim, o shader escreve a cor de fragmento resultante em out_fragColor.

Salve o programa de fragment shader. O modelo agora deve estar bem texturizado com um campo estelar no editor Scene e em runtime:

![quad with starnest](../images/shadertoy/quad_starnest.png)


## Animação {#animation}

A peça final do quebra-cabeça é introduzir tempo para fazer as estrelas se moverem. O Defold (desde 1.12.3) fornece isso automaticamente por meio de uma constante de fragmento do tipo `Time`.

1. Abra *star-nest.material*.
2. Adicione uma *Fragment Constant* e nomeie-a como "time".
3. Defina seu *Type* como `Time`.

![time constant](../images/shadertoy/time_constant.png)

E é isso! Já lidamos com esse `time` no fragment shader. Terminamos!

## Exercícios

Um exercício divertido de continuação é adicionar ao shader a entrada original de movimento do mouse. Você precisará criar uma nova Fragment Constant, desta vez do tipo `User`, e atualizá-la em `on_input` em algum script que detecte movimento do mouse usando a função `go.set()` e definindo as coordenadas de entrada nessa nova constante.

Boas criações com Defold!
