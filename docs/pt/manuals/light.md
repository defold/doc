---
title: Componente de luz no Defold
brief: Este manual explica como usar luzes ambiente, direcionais, de ponto e do tipo holofote e como acessar dados de luz em shaders.
---

# Componente de luz

O componente de luz representa uma fonte de luz em uma coleção. Atualmente, o Defold oferece suporte a quatro tipos de recurso de luz:

- Luz Ambiente (`.ambient_light`)
- Luz Direcional (`.directional_light`)
- Luz de Ponto (`.point_light`)
- Luz Holofote (`.spot_light`)

Os recursos de luz são adicionados a objetos de jogo como outros recursos de componente. Você pode criar componentes de luz diretamente em um objeto de jogo ou criar um recurso de luz no navegador *Conteúdo* e depois adicioná-lo como componente a um objeto de jogo na visualização *Estrutura*.

O Defold não aplica iluminação automaticamente a todos os materiais. As luzes são coletadas pelo engine e disponibilizadas aos shaders por meio do buffer de luz integrado. O shader do seu material decide como usar os dados de luz.

Os exemplos abaixo usam a mesma cena para mostrar como os diferentes tipos de luz afetam o resultado final:

![Cena sem luzes](images/light/no_light.png)

## Propriedades das luzes

Todas as cores de luz são valores RGB. O canal alfa não é usado pelos recursos de luz.

### Luz ambiente

As luzes ambiente adicionam uma luz constante à cena. Elas não são afetadas pela posição, rotação ou escala do objeto de jogo. Elas podem ser usadas, por exemplo, para uma iluminação geral de fundo ou para fazer os objetos parecerem não iluminados.

O componente de luz ambiente é representado no editor por um ícone com setas apontando para o centro. A cor do ícone é igual à da propriedade `color`.

![Luz ambiente com intensidade menor](images/light/ambient_light_less_intensity.png)

Propriedades:

`color`
: A cor RGB da luz ambiente.

`intensity`
: Multiplica a cor da luz ambiente.

![Luz ambiente com intensidade maior](images/light/ambient_light_full_intensity.png)

As luzes ambiente são acumuladas em uma única cor ambiente, `light_info.xyz`, no buffer de luz do shader. Elas não ocupam entradas no array `lights[]`. Vários componentes de luz ambiente na cena produzem apenas uma cor de saída, que é uma combinação de todos eles.

### Luz direcional

As luzes direcionais representam a luz que vem de uma direção, como a luz solar. Elas não usam a posição ou a escala do objeto de jogo, mas a direção da luz é derivada da rotação no mundo do objeto de jogo aplicada à direção frontal local `(0, 0, -1)`.

O componente de luz direcional é representado no editor por um ícone de sol colorido com uma seta 3D que indica sua direção.

![Luz direcional](images/light/directional_light.png)

Propriedades:

`color`
: A cor RGB da luz direcional.

`intensity`
: Multiplica a cor da luz direcional.


As luzes direcionais costumam ser combinadas com luz ambiente para evitar que as superfícies voltadas para o lado oposto à luz direcional fiquem completamente escuras.

![Luz direcional e ambiente](images/light/directional_and_ambient_light.png)

### Luz de ponto

As luzes de ponto emitem luz para fora a partir da posição do objeto de jogo no mundo. A posição da luz de ponto é obtida da posição do objeto de jogo no mundo.

O componente de luz de ponto é representado no editor por um ponto com raios emitidos ao redor. Sua cor representa a propriedade `color`, e um círculo representa o `range`.

![Luz de ponto](images/light/point_light.png)

Propriedades:

`color`
: A cor RGB da luz de ponto.

`intensity`
: Multiplica a cor da luz de ponto.

`range`
: O raio da luz em unidades do mundo.

O alcance efetivo é multiplicado pelo menor eixo absoluto da escala do objeto de jogo no mundo.

![Alcance da luz de ponto](images/light/point_light_range.png)

Alterar a cor da luz tinge a contribuição da luz de ponto, enquanto o alcance controla a distância que a luz alcança a partir da fonte.

![Alcance da luz de ponto com cor verde](images/light/point_ight_range_green_color.png)

### Luz holofote

As luzes do tipo holofote emitem luz em um cone a partir da posição do objeto de jogo no mundo. A direção é derivada da rotação no mundo do objeto de jogo aplicada a `(0, 0, -1)`.

O componente de luz holofote é representado no editor por um ícone de lâmpada colorido e linhas-guia que mostram os cones externo e interno.

![Luz holofote](images/light/spot_light.png)

Propriedades:

`color`
: A cor RGB da luz holofote.

`intensity`
: Multiplica a cor da luz holofote.

`range`
: O raio da luz em unidades do mundo.

`inner_cone_angle`
: O ângulo do cone interno em graus no editor. Os pixels dentro desse cone recebem toda a contribuição da luz holofote.

`outer_cone_angle`
: O ângulo do cone externo em graus no editor. A luz perde intensidade entre os cones interno e externo.

O alcance efetivo é multiplicado pelo menor eixo absoluto da escala do objeto de jogo no mundo. Os ângulos dos cones são editados em graus e convertidos em radianos no recurso de luz compilado.

![Gizmos de luz holofote](images/light/spot_light_gizmos.png)

## Validação

O pipeline de build valida e normaliza os dados do recurso de luz:

- `color` deve conter exatamente três números.
- `intensity` é limitado a `0` ou mais.
- `range` é limitado a `0` ou mais para luzes de ponto e do tipo holofote.
- Os ângulos dos cones da luz holofote são limitados a `0..180` graus.
- `inner_cone_angle` é limitado para nunca exceder `outer_cone_angle`.

## Limite do projeto

O número máximo de componentes de luz é controlado pela configuração de projeto `light.max_count`. O valor padrão é `64`.

As luzes ambiente não consomem entradas no array `lights[]` do shader, mas ainda são componentes de luz e contam para `light.max_count`. As luzes direcionais, de ponto e do tipo holofote consomem entradas em `lights[]` enquanto estão ativas.

Se o número de componentes de luz exceder `light.max_count`, o engine relatará um erro de buffer de componentes cheio.

## Buffer de luz em shaders

Um shader pode acessar as luzes ativas declarando um bloco uniform chamado `LightBuffer` com o layout integrado. O engine detecta esse bloco e vincula os dados de luz automaticamente para materiais e programas compute que o utilizam.

![Shader do buffer de luz](images/light/light-buffer-shader.png)

```glsl
#version 140

#define MAX_LIGHT_COUNT 32

struct Light
{
    vec4 position;        // xyz: posição no mundo, w: não usado
    vec4 color;           // rgb: cor, a: não usado
    vec4 direction_range; // xyz: direção normalizada no mundo, w: alcance
    vec4 params;          // x: tipo, y: intensidade, z: cone interno, w: cone externo
};

uniform LightBuffer
{
    // xyz: cor ambiente acumulada, w: contagem de luzes não ambiente ativas
    vec4 light_info;
    Light lights[MAX_LIGHT_COUNT];
};
```

O tipo de luz é armazenado em `lights[i].params.x`:

| Tipo | Valor |
|------|-------|
| Direcional | `0` |
| De ponto | `1` |
| Holofote | `2` |

O shader pode declarar um array `lights[]` menor que `light.max_count`, mas não maior. Sempre limite os loops de luz ao tamanho declarado do array:

```glsl
vec3 apply_lights(vec3 normal)
{
    vec3 result = light_info.xyz;
    int active_light_count = int(light_info.w);

    for (int i = 0; i < MAX_LIGHT_COUNT; ++i)
    {
        if (i >= active_light_count)
        {
            break;
        }

        int type = int(lights[i].params.x);
        vec3 light_color = lights[i].color.rgb * lights[i].params.y;

        if (type == 0) // Direcional
        {
            vec3 light_dir = normalize(-lights[i].direction_range.xyz);
            result += light_color * max(dot(normal, light_dir), 0.0);
        }
        else if (type == 1) // De ponto
        {
            result += light_color;
        }
        else if (type == 2) // Holofote
        {
            result += light_color;
        }
    }

    return result;
}
```

O exemplo acima mostra o padrão de acesso ao buffer. Um shader real para uma luz de ponto ou do tipo holofote também deve calcular o vetor entre o ponto sombreado e `lights[i].position.xyz`, aplicar a atenuação pela distância usando `lights[i].direction_range.w` e, para luzes do tipo holofote, usar `lights[i].params.z` e `lights[i].params.w` como ângulos dos cones em radianos.

## Função auxiliar de iluminação integrada

O Defold inclui uma função auxiliar de shader em `/builtins/materials/lighting.glsl`. Defina `MAX_LIGHT_COUNT`, forneça os varyings esperados pela função auxiliar e inclua-a a partir do seu fragment shader:

```glsl
#version 140

#define MAX_LIGHT_COUNT 32

in vec3 var_normal;
in vec4 var_position;
in mat4 var_view;

out vec4 color_out;

#include "/builtins/materials/lighting.glsl"

void main()
{
    vec3 normal = normalize(var_normal);
    vec3 ambient = ambient_light();
    vec3 diffuse = diffuse_lambert(normal, var_position.xyz);
    color_out = vec4(ambient + diffuse, 1.0);
}
```

A função auxiliar define as constantes `LIGHT_DIRECTIONAL`, `LIGHT_POINT` e `LIGHT_SPOT`, expõe `ambient_light()` e fornece funções de difusão de Lambert para as luzes no buffer.

## Veja também

- [Manual de shaders](/manuals/shader)
- [Manual de materiais](/manuals/material)
- [Manual de renderização](/manuals/render)
