---
title: Renderização fisicamente baseada no Defold
brief: Este manual explica como usar materiais PBR integrados e personalizar o sombreamento fisicamente baseado no Defold.
---

# Physically Based Rendering (PBR)

A renderização fisicamente baseada (PBR, Physically Based Rendering) é uma abordagem de sombreamento que modela como a luz interage com superfícies usando princípios físicos. Propriedades de material como cor base, fator metálico e rugosidade descrevem a superfície independentemente da iluminação da cena.

Os materiais glTF integrados fornecem iluminação PBR. O Defold também expõe propriedades de materiais glTF 2.0 importados e dados de extensões Khronos compatíveis a shaders personalizados.

## Materiais PBR integrados {#built-in-pbr-materials}

Atribua um arquivo glTF ou GLB à propriedade *Scene* de um [componente Model](/manuals/model). Quando o editor oferecer o preenchimento de materiais e texturas, escolha <kbd>Auto Fill</kbd> para aplicar os vínculos de materiais gerados da cena, substituindo os existentes, se houver. Esses materiais usam os shaders glTF integrados e podem referenciar imagens incorporadas diretamente. Escolha <kbd>Keep Current</kbd> para preservar seus vínculos e atribuir materiais e texturas manualmente. Consulte o [fluxo de importação de modelos](/manuals/importing-models/#using-a-model) para explorar recursos incorporados e selecionar malhas individuais.

Os seguintes materiais estão disponíveis em `/builtins/materials/`. Escolha a variante que corresponda ao seu modelo e ao uso ou não de instanciamento:

| Tipo de modelo | Material |
|---|---|
| Estático, sem instâncias | `gltf.material` |
| Estático, com instâncias | `gltf_instanced.material` |
| Com skinning (animado), sem instâncias | `gltf_skinned.material` |
| Com skinning (animado), com instâncias | `gltf_skinned_instanced.material` |

Todos os quatro usam espaço de vértices local e o mesmo fragment shader `gltf.fp`. As variantes com skinning o executam na GPU. Consulte os [requisitos de materiais de modelos](/manuals/model/#material) para skinning na GPU e instanciamento.

Para vínculos manuais de texturas, os materiais integrados usam estes nomes de sampler:

| Textura | Sampler | Dados usados |
|---|---|---|
| Cor base | `PbrMetallicRoughness_baseColorTexture` | Cor RGB e alfa |
| Metalicidade/rugosidade | `PbrMetallicRoughness_metallicRoughnessTexture` | Rugosidade em G, metalicidade em B |
| Normal | `PbrMaterial_normalTexture` | Normal no espaço tangente em RGB |
| Oclusão | `PbrMaterial_occlusionTexture` | Oclusão em R |
| Emissiva | `PbrMaterial_emissiveTexture` | Cor RGB |

Configure uma [câmera](/manuals/camera/#using-the-camera) e adicione [componentes de luz](/manuals/light) para iluminar o modelo. O shader usa luzes direcionais, pontuais e spot para iluminação direta, além de luzes ambientes para uma contribuição ambiente simples. Os materiais têm a tag `model`, que é desenhada pelo script de renderização padrão. Um script personalizado deve desenhar um predicado correspondente.

### Comportamento dos shaders integrados {#built-in-shader-behavior}

Os shaders integrados implementam sombreamento por metalicidade/rugosidade, cor base e cor dos vértices, mapeamento de normais quando há dados de tangentes, oclusão e emissão, incluindo intensidade emissiva. Texturas de cor base e emissivas são decodificadas de sRGB para a iluminação, e a cor final é convertida de volta para sRGB. Mapas de metalicidade/rugosidade, normais e oclusão contêm dados lineares.

O shader respeita materiais sem iluminação e alfa mascarado, e ajusta as normais de superfícies de dupla face. O estado de renderização ainda importa:

- Para materiais de dupla face, desabilite o descarte de faces na passagem de renderização correspondente para que as faces traseiras cheguem ao shader.
- Para alfa com mesclagem, o shader produz alfa não pré-multiplicado. Habilite a mesclagem com `graphics.BLEND_FACTOR_SRC_ALPHA` e `graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA` e controle a ordem de desenho dos objetos transparentes e a escrita de profundidade no script de renderização. A passagem padrão de modelos não habilita a mesclagem automaticamente.

A contribuição ambiente integrada é uma aproximação, sem iluminação por mapas de ambiente nem sombras. Efeitos como clearcoat, transmissão, sheen, iridescência e o fluxo de especularidade/brilho exigem sombreamento personalizado; importar seus parâmetros não habilita esses efeitos em `gltf.fp`.

## Visão geral das propriedades de material

As propriedades abaixo são lidas de arquivos-fonte glTF 2.0 atribuídos a um componente Model. Esta lista descreve os dados de material disponíveis; a iluminação integrada usa o subconjunto descrito acima. Nem todas as propriedades são padrão. Algumas são fornecidas por extensões glTF opcionais, que podem ou não ser incluídas pela ferramenta usada para exportar o arquivo glTF. A extensão relevante é indicada entre parênteses após o nome da propriedade abaixo.

Metallic roughness
: Descreve como a luz interage com o material. O modelo PBR padrão.

Specular glossiness (KHR_materials_pbrSpecularGlossiness)
: Uma alternativa a metallic roughness. Usada com frequência em assets mais antigos.

Clearcoat (KHR_materials_clearcoat)
: Adiciona uma camada transparente de revestimento com sua própria rugosidade e normal map.

Ior (KHR_materials_ior)
: Adiciona um índice de refração.

Specular (KHR_materials_specular)
: Adiciona intensidade especular dedicada e canal de cor.

Iridescence (KHR_materials_iridescence)
: Simula interferência de filme fino para materiais como bolhas de sabão ou pérolas.

Sheen (KHR_materials_sheen)
: Modela reflexos de microssuperfície semelhantes a tecido.

Transmission (KHR_materials_transmission)
: Modela transmissão de luz para materiais transparentes ou semelhantes a vidro.

Volume (KHR_materials_volume)
: Suporta efeitos volumétricos como espessura e atenuação.

Emissive strength (KHR_materials_emissive_strength)
: Controla o brilho emissivo independentemente da cor base.

Normal map
: Normal map para detalhes de superfície.

Occlusion map
: Mapa de oclusão ambiente.

Emissive map
: Textura autoemissiva para superfícies brilhantes.

Emissive factor
: Multiplicador RGB para intensidade emissiva

Alpha cutoff
: Limiar para transparência mascarada.

Alpha mode
: Modos de transparência Opaque, Masked ou Blended.

Double sided
: Solicita a renderização dos dois lados da superfície. A passagem de renderização deve permitir que as faces traseiras cheguem ao shader.

Unlit
: Se verdadeiro, o material ignora cálculos de iluminação.

## Integração com shaders

As seções abaixo abordam shaders personalizados. Copie o recurso `.material` integrado adequado e `gltf.fp` para seu projeto e aponte o *Fragment Program* do material copiado para seu shader. Mantenha o programa de vértices glTF correspondente, os nomes dos samplers e o espaço de vértices local, a menos que também esteja substituindo essas interfaces.

As funções auxiliares integradas separam a amostragem de texturas da preparação da superfície, dos cálculos de BRDF e da iluminação. `gltf_sampling.glsl` lê o bloco de uniformes bruto `PbrMaterial` e produz um valor `PBRMaterial` com as entradas de material resolvidas e lineares. `gltf_lighting.glsl` fornece iluminação direta e ambiente e combina suas contribuições. A capitalização distingue o bloco de uniformes bruto da estrutura do material amostrado.

### Exemplo de shader {#example-shader}

Este fragment shader aumenta a rugosidade mínima mantendo a iluminação integrada. Ele funciona com os programas de vértices usados pelas quatro variantes de material glTF:

```glsl
#version 140

#include "/builtins/materials/gltf_sampling.glsl"
#include "/builtins/materials/gltf_lighting.glsl"

out vec4 out_fragColor;

void main()
{
    PBRMaterial inputs = pbr_sample_material(var_texcoord0, var_color);
    inputs.roughness = max(inputs.roughness, 0.35);

    // Sample textures, including the normal map, before discarding fragments.
    PBRSurface surface = pbr_sample_surface(inputs, var_texcoord0);
    if ((!inputs.doubleSided && !gl_FrontFacing) || pbr_should_discard_alpha(inputs))
    {
        discard;
    }

    // Derive BRDF values after editing the material inputs.
    MaterialInfo material = pbr_create_material_info(inputs);
    PBRLighting lighting = pbr_create_lighting();
    if (!inputs.unlit)
    {
        lighting.direct = pbr_evaluate_direct_lighting(material, surface, var_view);
        lighting.indirect = pbr_evaluate_ambient_lighting(material, ambient_light());
    }

    vec3 color = pbr_compose_lighting(inputs, lighting, inputs.occlusion, inputs.occlusion);
    out_fragColor = vec4(pbr_linear_to_srgb(color), pbr_get_alpha(inputs));
}
```

Edite as entradas do material amostrado antes de chamar `pbr_create_material_info()`. Se alterar a posição ou as normais de uma superfície no espaço de visualização, chame `pbr_finalize_surface(surface, var_view)` para atualizar seus campos derivados no espaço global. Para uma BRDF personalizada ou contribuições de luz individuais, use ou substitua `pbr_evaluate_brdf()` e `pbr_evaluate_light()` das funções auxiliares integradas.

Você pode substituir `lighting.indirect` por sua própria iluminação de ambiente ou iluminação global. Suas contribuições difusas e especulares são luz de saída linear, portanto não aplique a BRDF do material uma segunda vez. Aplique a visibilidade das sombras à contribuição apropriada de luz direta; os argumentos de visibilidade de `pbr_compose_lighting()` afetam apenas a iluminação indireta. Para um pipeline HDR, escreva cor linear no alvo intermediário e faça a conversão para sRGB na passagem final.

### Dados brutos do material {#raw-material-data}

Para um shader totalmente personalizado, declare um bloco de uniformes chamado `PbrMaterial` com os nomes e tipos de membros reconhecidos. O Defold preenche os campos correspondentes a partir do material glTF de origem. As declarações abaixo descrevem as estruturas de recursos disponíveis; inclua apenas as necessárias para seu shader. Declarar uma estrutura fornece dados, mas o shader deve implementar seu comportamento de amostragem e iluminação.

Não declare novamente o bloco de uniformes nem `PbrMetallicRoughness` ao incluir `gltf_sampling.glsl`, que já os declara. As declarações abaixo são uma alternativa para shaders que gerenciam suas próprias entradas de material.

```glsl
struct PbrMetallicRoughness
{
    vec4 baseColorFactor;
    // R: metallic (Default=1.0), G: roughness (Default=1.0)
    vec4 metallicAndRoughnessFactor;
    // R: use baseColorTexture, G: use metallicRoughnessTexture
    vec4 metallicRoughnessTextures;
};

struct PbrSpecularGlossiness
{
    vec4 diffuseFactor;
    // RGB: specular (Default=1.0), A: glossiness (Default=1.0)
    vec4 specularAndSpecularGlossinessFactor;
    // R: use diffuseTexture, G: use specularGlossinessTexture
    vec4 specularGlossinessTextures;
};

struct PbrClearCoat
{
    // R: clearCoat (Default=0.0), G: clearCoatRoughness (Default=0.0)
    vec4 clearCoatAndClearCoatRoughnessFactor;
    // R: use clearCoatTexture, G: use clearCoatRoughnessTexture, B: use clearCoatNormalTexture
    vec4 clearCoatTextures;
};

struct PbrTransmission
{
    // R: transmission (Default=0.0)
    vec4 transmissionFactor;
    // R: use transmissionTexture
    vec4 transmissionTextures;
};

struct PbrIor
{
    // R: ior (Default=0.0)
    vec4 ior;
};

struct PbrSpecular
{
    // RGB: specularColor, A: specularFactor (Default=1.0);
    vec4 specularColorAndSpecularFactor;
    // R: use specularTexture, G: use specularColorTexture
    vec4 specularTextures;
};

struct PbrVolume
{
    // R: thicknessFactor (Default=0.0), GBA: attenuationColor
    vec4 thicknessFactorAndAttenuationColor;
    // R: attenuationDistance (Default=-1.0)
    vec4 attenuationDistance;
    // R: use thicknessTexture
    vec4 volumeTextures;
};

struct PbrSheen
{
    // RGB: sheenColor, A: sheenRoughnessFactor (Default=0.0)
    vec4 sheenColorAndRoughnessFactor;
    // R: use sheenColorTexture, G: use sheenRoughnessTexture
    vec4 sheenTextures;
};

struct PbrEmissiveStrength
{
    // R: emissiveStrength (Default=1.0)
    vec4 emissiveStrength;
};

struct PbrIridescence
{
    // R: iridescenceFactor (Default=0.0), G: iridescenceIor (Default=1.3), B: iridescenceThicknessMin (Default=100.0), A: iridescenceThicknessMax (Default=400.0)
    vec4 iridescenceFactorAndIorAndThicknessMinMax;
    // R: use iridescenceTexture, G: use iridescenceThicknessTexture
    vec4 iridescenceTextures;
};
```

As propriedades comuns e as estruturas de recursos são membros do bloco de uniformes. Os componentes empacotados são:

```glsl
uniform PbrMaterial
{
    // X: alpha cutoff, Y: double-sided, Z: unlit,
    // W: alpha mode (0 = opaque, 1 = mask, 2 = blend)
    vec4 pbrAlphaCutoffAndDoubleSidedAndIsUnlit;
    // X: has normal texture, Y: has occlusion texture, Z: has emissive texture
    vec4 pbrCommonTextures;
    // RGB: emissive factor, W: emissive strength
    vec4 pbrEmissiveFactorAndStrength;
    // X: normal scale, Y: occlusion strength
    vec4 pbrNormalScaleAndOcclusionStrength;

    PbrMetallicRoughness pbrMetallicRoughness;
    PbrSpecularGlossiness pbrSpecularGlossiness;
    PbrClearCoat pbrClearCoat;
    PbrTransmission pbrTransmission;
    PbrIor pbrIor;
    PbrSpecular pbrSpecular;
    PbrVolume pbrVolume;
    PbrSheen pbrSheen;
    PbrEmissiveStrength pbrEmissiveStrength;
    PbrIridescence pbrIridescence;
};
```

Omita membros de recursos não utilizados do bloco. Se o bloco ou os campos reconhecidos de um recurso estiverem ausentes, os dados correspondentes não serão fornecidos. As flags de presença de textura descrevem as referências a texturas do material de origem; um material personalizado ainda precisa de declarações de samplers e vínculos de texturas correspondentes para os mapas que amostra.

### Constantes

Campos de recursos usam nomes como `pbrMetallicRoughness.baseColorFactor`; campos comuns usam nomes como `pbrEmissiveFactorAndStrength`. A engine preenche essas constantes a partir do material importado ou de um material padrão quando o modelo não tem dados de material. Definir valores padrão no recurso `.material` não substitui os valores importados.

Para personalizar o sombreamento integrado, edite o `PBRMaterial` amostrado antes de derivar seus valores de BRDF, como no exemplo acima. Para controles adicionais em tempo de execução, declare suas próprias constantes de shader e use a [API de constantes de material de modelos](/manuals/model/#material-constants).

## Próximos passos

Use os materiais integrados para o fluxo padrão de metalicidade/rugosidade do glTF. Estenda as funções auxiliares de shader ou forneça seu próprio material quando precisar de uma BRDF diferente, iluminação de ambiente, sombras ou efeitos adicionais de materiais glTF.

Veja também:

* [Manual de luzes](/manuals/light)
* [Manual de materiais](/manuals/material)
* [Manual de Shaders](/manuals/shader)
* [Manual de Renderização](/manuals/render)
* [Especificação glTF 2.0](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)

