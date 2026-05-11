---
title: Shader de rolagem de textura
brief: Neste tutorial, você aprenderá a usar um shader para rolar uma textura repetida.
---

Créditos: Este tutorial foi contribuído pelo usuário do fórum MasterMind ([post original no fórum](https://forum.defold.com/t/texture-scrolling-shader-tutorial-example/71553)).

# Tutorial de shader de rolagem de textura

Rolar texturas via shader é um recurso básico em muitos efeitos de shader. Vamos criar um! Use o [projeto de exemplo](https://github.com/FlexYourBrain/Texture_Scrolling_Example) para acompanhar e experimentar por conta própria. O método usado será deslocamento de UV usando uma constante no shader.

Também há uma [demo do projeto de exemplo no itch.io](https://flexyourbrain.itch.io/texture-scrolling-in-defold) para quem quiser ver o resultado deste breve tutorial/guia:


## Configuração

O projeto é configurado assim:

* Um plano 3D subdividido (.dae), que será usado para exibir a textura rolando.
* Um componente de modelo com o plano 3D (arquivo .dae) atribuído.
* Duas imagens de textura 64x64 (`water_bg.png` e `water_wave.png`), criadas para tilear sem emendas, atribuídas nas propriedades do .model.
* Um shader (Material + Vertex Program + Fragment Program) atribuído ao modelo do plano.
* Uma constante definida nos materiais e no shader.
* Um componente de script anexado ao objeto de jogo do modelo para iniciar o loop de animação.

![](images/texture-scrolling/model_setup.png)

_Observação: `water_bg` é atribuído ao slot `tex0`, e `water_wave` é definido no slot `tex1`. Dois slots de sampler são atribuídos nas propriedades de sampler do material, mostradas abaixo._

![](images/texture-scrolling/material_setup.png)

_Atualmente, `tex1` será a textura que vai rolar, então Wrap U e V são definidos como Repeat._

Essa é a configuração básica. Agora podemos passar para os programas `water_scroll.vp` (vertex) e `water_scroll.fp` (fragment). Você pode ver na imagem acima que eles são definidos no material.


## Código do shader

É uma boa prática evitar fazer cálculos demais no fragment program quando possível, então calculamos o deslocamento de UV no vertex program antes que as coordenadas sejam enviadas ao fragment program. Também criamos uma constante "animation_time" com tipo user nas propriedades de constantes de vértice definidas no material (como visto acima). A constante é um vector 4, mas usamos apenas o primeiro valor. Se representarmos esse vector 4 como `vector4(x,y,z,w)`, usaremos apenas o valor x no shader, como mostrado abaixo.


```glsl
// water_scroll.vp

// UV / Texture Scroll
attribute highp vec4 position;
attribute mediump vec2 texcoord0;

uniform mediump mat4 mtx_worldview;
uniform mediump mat4 mtx_proj;
uniform mediump vec4 animation_time; // constante de vertice definida no material como tipo user.

varying mediump vec2 var_texcoord0; // configura var texcoord 0
varying mediump vec2 var_texcoord1; // configura var texcoord 1

void main()
{
    vec4 p = mtx_worldview * vec4(position.xyz, 1.0);
    var_texcoord0 = texcoord0;
    var_texcoord1 = vec2(texcoord0.x - animation_time.x, texcoord0.y); // Calcula o deslocamento uv de var texcoord 1 no eixo U(x) para o fragment program 
    gl_Position = mtx_proj * p;
}
```

O modelo fornece o atributo `texcoord0`, que são as nossas coordenadas UV de textura. Declaramos nossa uniform `vec4` chamada animation_time e também temos duas varying `vec2`, `var_texcoord0` e `var_texcoord1`, que passamos ao fragment program depois de atribuir a elas as coordenadas UV do atributo `texcoord0` em `void main()`. Como você pode ver, `var_texcoord1` é diferente porque estamos deslocando esse valor antes que ele seja enviado ao fragment program. Atribuímos um `vec2` para que possamos aplicar `animation_time` ao x e ao y separadamente, se quisermos. Neste caso, usamos apenas `texcoord0.x` e subtraímos nossa constante `animation_time.x`, que, quando animada, deslocará no eixo U negativo (horizontal para a esquerda); mantemos `texcoord0.y` na posição do atributo.


```glsl
// water_scroll.fp

varying mediump vec2 var_texcoord0; // var texcoord 0 usado com o sampler water_bg
varying mediump vec2 var_texcoord1; // var texcoord 1 usado com o sampler water_waves; calculo da animacao UV feito no vertex program

uniform lowp sampler2D tex0; // Slot de sampler 0 do material = plano de fundo de agua / definido em plane.model
uniform lowp sampler2D tex1; // Slot de sampler 1 do material = ondas da agua / definido em plane.model

void main()
{
    vec4 water_bg = texture2D(tex0, var_texcoord0.xy);
    vec4 water_waves = texture2D(tex1, var_texcoord1.xy);
    
    gl_FragColor = vec4(water_bg.rgb + water_waves.rgb ,1.0); // adiciona as ondas da textura ao bg usando adicao(+), alfa definido como 1.0 pois nao ha transparencia sendo usada0
}
```

Agora, no fragment program, temos uma configuração simples. Duas varying `vec2` de entrada que enviamos do vertex program, `var_textcoord0` e `var_texcoord1`, e então fornecemos uniforms para as texturas de sampler que definimos no modelo e no material, chamadas `tex0` e `tex1`. Depois, em `void main()`, criamos vector 4 para atribuir às nossas texturas usando `texture2d()`; as imagens estão no formato de canais RGBA (red, green, blue, alpha). Atribuímos o nome do sampler e, em seguida, as coordenadas de textura que queremos usar. Como você vê na imagem acima, "water_waves" tem `var_texcoord1` atribuído. Essa é a textura que estamos animando/rolando, e `var_texcoord0`, atribuído a `water_bg`, deixamos como está. Para a variável global reservada `gl_FragColor`, é aqui que as cores dos pixels são atribuídas com o mesmo formato `vec4(r,g,b,a)`. Queremos combinar as 2 texturas, então usamos adição para misturar os canais rgb de cada textura. Também não estamos usando o canal alfa das texturas, então atribuímos o valor float 1.0, que equivale a opacidade total.


## Script de animação do shader

```lua
-- animate_shader.script
local animate = 1.0
-- o float local sera usado para definir a constante animation_time no material scroll; apenas o valor x da constante e usado no shader 
-- portanto nao ha necessidade de criar um vector 4

function init(self)
	go.animate("/scroll#plane", "animation_time.x", go.PLAYBACK_LOOP_FORWARD, animate, go.EASING_LINEAR, 4.0)
end
```

Há mais de uma maneira de animar valores constantes: você pode calcular passos de delta time e atualizar a constante com esses valores no script de renderização ou em um script normal, se quiser. Neste caso, estamos animando apenas um shader, e se você quisesse um passo de tempo calculado em vários shaders, fazer isso em um `update()` talvez fosse mais adequado. Porém, usaremos `go.animate()` porque temos muita funcionalidade à disposição. Usando `go.animate()`, podemos animar apenas o valor x da nossa constante com "animation_time.x". Também temos duração, atraso e easing para ajustar, se quisermos. Também podemos definir o playback para loop ou para tocar uma vez e cancelar a animação se for necessário. Tudo isso é muito útil ao animar nossos shaders.

O float `local animate` 1.0 é o valor-alvo que estamos animando em "animation_time.x". Em shaders, na maior parte do tempo, trabalhamos com valores float normalizados de 0.0 a 1.0. Observe que os valores padrão da constante no material para nosso `animation_time` são (0,0,0,0); estamos animando o primeiro zero de 0.0 para 1.0. Isso significa que nossas coordenadas UV deslocadas animarão até a borda e então entrarão em loop de novo e de novo, que é exatamente o que queremos!


## Próximos passos

Como exercício, você pode tentar animar as coordenadas de textura de `water_bg` na direção oposta, como na demo de exemplo!

Espero que isso ajude. Se você fizer algo rolar, compartilhe!

/ MasterMind


