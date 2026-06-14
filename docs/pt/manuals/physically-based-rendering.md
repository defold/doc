---
title: Renderização fisicamente baseada no Defold
brief: Este manual explica os fundamentos de como acessar dados de material para renderização fisicamente baseada no Defold.
---

# Physically Based Rendering (PBR)

Physically Based Rendering (PBR), ou renderização fisicamente baseada, é uma abordagem de sombreamento que modela como a luz interage com superfícies usando princípios físicos do mundo real. Ela produz iluminação consistente e realista em diferentes ambientes e permite que assets pareçam corretos sob uma ampla variedade de condições de iluminação.

A implementação de PBR do Defold segue a especificação de material glTF 2.0 e extensões Khronos associadas. Quando você importa assets glTF para o Defold, as propriedades de material são analisadas automaticamente e armazenadas como dados estruturados de material que podem ser acessados em shaders em tempo de execução.

Materiais PBR podem incluir efeitos como reflexos metálicos, rugosidade de superfície, transmissão, clearcoat, espalhamento subsuperficial, iridescência e outros.

::: sidenote
Atualmente, o Defold expõe dados de material PBR para shaders, mas não fornece um modelo de iluminação PBR integrado. Você pode usar esses dados nos seus próprios shaders de iluminação e reflexão para obter renderização fisicamente baseada. Um modelo padrão de iluminação PBR será adicionado ao Defold em uma etapa posterior.
:::

::: sidenote
Texturas embutidas de arquivos glTF atualmente não são atribuídas automaticamente no Defold. Apenas parâmetros de material são expostos aos shaders. Você ainda pode atribuir texturas manualmente a componentes de modelo e amostrá-las no seu shader.
:::

## Visão geral das propriedades de material

As propriedades de material são analisadas a partir dos arquivos-fonte glTF 2.0 atribuídos a um componente de modelo. Nem todas as propriedades são padrão. Algumas são fornecidas por extensões glTF opcionais que podem ou não ser incluídas pela ferramenta usada para exportar o arquivo glTF. A extensão relevante é indicada entre parênteses após o nome da propriedade abaixo.

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
: Se verdadeiro, ambos os lados da superfície são renderizados.

Unlit
: Se verdadeiro, o material ignora cálculos de iluminação.

::: sidenote
Algumas dessas propriedades fornecem indicações sobre como o material deve ser renderizado. Os dados das propriedades (alpha cutoff, alpha mode, double sided e unlit) estão disponíveis nos shaders, mas não afetam como o material é renderizado no Defold.
:::

## Integração com shaders

Os dados de material PBR são expostos aos shaders com base nos tipos e na convenção de nomes. O sistema de material PBR fornece todos os parâmetros de material analisados aos shaders por meio de um bloco uniforme estruturado chamado `PbrMaterial`. Cada extensão glTF suportada corresponde a uma struct dentro desse bloco, que pode ser compilada condicionalmente usando flags `#define`.

```glsl
uniform PbrMaterial
{
	// Propriedades do material
};
```

Os vários recursos do material são especificados como structs fixas no shader. Os dados foram compactados tanto quanto possível em `vec4`'s, pois é assim que constantes são definidas internamente no Defold. Nos casos em que os dados foram compactados, isso é indicado como comentários nos trechos de shader de cada recurso abaixo:

```glsl
struct PbrMetallicRoughness
{
    vec4 baseColorFactor;
    // R: metallic (Padrão=1.0), G: roughness (Padrão=1.0)
    vec4 metallicAndRoughnessFactor;
    // R: use baseColorTexture, G: use metallicRoughnessTexture
    vec4 metallicRoughnessTextures;
};

struct PbrSpecularGlossiness
{
	vec4 diffuseFactor;
	// RGB: specular (Padrão=1.0), A: glossiness (Padrão=1.0)
	vec4 specularAndSpecularGlossinessFactor;
	// R: use diffuseTexture, G: use specularGlossinessTexture
	vec4 specularGlossinessTextures;
};

struct PbrClearCoat
{
	// R: clearCoat (Padrão=0.0), G: clearCoatRoughness (Padrão=0.0)
	vec4 clearCoatAndClearCoatRoughnessFactor;
	// R: use clearCoatTexture, G: use clearCoatRoughnessTexture, B: use clearCoatNormalTexture
	vec4 clearCoatTextures;
};

struct PbrTransmission
{
	// R: transmission (Padrão=0.0)
	vec4 transmissionFactor;
	// R: use transmissionTexture
	vec4 transmissionTextures;
};

struct PbrIor
{
	// R: ior (Padrão=0.0)
	vec4 ior;
};

struct PbrSpecular
{
	// RGB: specularColor, A: specularFactor (Padrão=1.0);
	vec4 specularColorAndSpecularFactor;
	// R: use specularTexture, G: use specularColorTexture
	vec4 specularTextures;
};

struct PbrVolume
{
	// R: thicknessFactor (Padrão=0.0), RGB: attenuationColor
	vec4 thicknessFactorAndAttenuationColor;
	// R: attentuationDistance (Padrão=-1.0)
	vec4 attenuationDistance;
	// R: use thicknessTexture
	vec4 volumeTextures;
};

struct PbrSheen
{
	// RGB: sheenColor, A: sheenRoughnessFactor (Padrão=0.0)
	vec4 sheenColorAndRoughnessFactor;
	// R: use sheenColorTexture, G: use sheenRoughnessTexture
	vec4 sheenTextures;
};

struct PbrEmissiveStrength
{
	// R: emissiveStrength (Padrão=1.0)
	vec4 emissiveStrength;
};

struct PbrIridescence
{
	// R: iridescenceFactor (Padrão=0.0), G: iridescenceIor (Padrão=1.3), B: iridescenceThicknessMin (Padrão=100.0), A: iridescenceThicknessMax (Padrão=400.0)
	vec4 iridescenceFactorAndIorAndThicknessMinMax;
	// R: use iridescenceTexture, G: use iridescenceThicknessTexture
	vec4 iridescenceTextures;
};
```

As propriedades comuns são definidas no próprio uniform do material (e, mais uma vez, observe a compactação de dados em `vec4`).

```glsl
// Texturas comuns
uniform sampler2D PbrMaterial_normalTexture;
uniform sampler2D PbrMaterial_occlusionTexture;
uniform sampler2D PbrMaterial_emissiveTexture;

uniform PbrMaterial
{
	// Propriedades comuns:

	// R: alphaCutoff (Padrão=0.5), G: doubleSided (Padrão=false), B: unlit (Padrão=false)
	vec4 pbrAlphaCutoffAndDoubleSidedAndIsUnlit;
	// R: use normalTexture, G: use occlusionTexture, B: use emissiveTexture
	vec4 pbrCommonTextures;

	// Outras propriedades...
};
```

### Shader de exemplo

Aqui está um shader de exemplo que contém todos os recursos e um esquema de nomes proposto para bindings de textura (novamente, isso deve ser tratado manualmente). Observe que você pode desativar recursos simplesmente usando `#define`s ao redor de cada membro do próprio `PbrMaterial`, como mostrado no exemplo abaixo:

```glsl
// Flags de recursos; comente ou remova para reduzir o shader.
#define PBR_METALLIC_ROUGHNESS
#define PBR_SPECULAR_GLOSSINESS
#define PBR_CLEARCOAT
#define PBR_TRANSMISSION
#define PBR_IOR
#define PBR_SPECULAR
#define PBR_VOLUME
#define PBR_SHEEN
#define PBR_EMISSIVE_STRENGTH
#define PBR_IRIDESCENCE

// Comum
uniform sampler2D PbrMaterial_normalTexture;
uniform sampler2D PbrMaterial_occlusionTexture;
uniform sampler2D PbrMaterial_emissiveTexture;

// PbrMetallicRoughness
uniform sampler2D PbrMetallicRoughness_baseColorTexture;
uniform sampler2D PbrMetallicRoughness_metallicRoughnessTexture;

struct PbrMetallicRoughness
{
    vec4 baseColorFactor;
    // R: metallic (Padrão=1.0), G: roughness (Padrão=1.0)
    vec4 metallicAndRoughnessFactor;
    // R: use baseColorTexture, G: use metallicRoughnessTexture
    vec4 metallicRoughnessTextures;
};

// PbrSpecularGlossiness
uniform sampler2D PbrSpecularGlossiness_diffuseTexture;
uniform sampler2D PbrSpecularGlossiness_specularGlossinessTexture;

struct PbrSpecularGlossiness
{
	vec4 diffuseFactor;
	// RGB: specular (Padrão=1.0), A: glossiness (Padrão=1.0)
	vec4 specularAndSpecularGlossinessFactor;
	// R: use diffuseTexture, G: use specularGlossinessTexture
	vec4 specularGlossinessTextures;
};

// PbrClearCoat
uniform sampler2D PbrClearCoat_clearcoatTexture;
uniform sampler2D PbrClearCoat_clearcoatRoughnessTexture;
uniform sampler2D PbrClearCoat_clearcoatNormalTexture;

struct PbrClearCoat
{
	// R: clearCoat (Padrão=0.0), G: clearCoatRoughness (Padrão=0.0)
	vec4 clearCoatAndClearCoatRoughnessFactor;
	// R: use clearCoatTexture, G: use clearCoatRoughnessTexture, B: use clearCoatNormalTexture
	vec4 clearCoatTextures;
};

// PbrTransmission
uniform sampler2D PbrTransmission_transmissionTexture;

struct PbrTransmission
{
	// R: transmission (Padrão=0.0)
	vec4 transmissionFactor;
	// R: use transmissionTexture
	vec4 transmissionTextures;
};

struct PbrIor
{
	// R: ior (Padrão=0.0)
	vec4 ior;
};

// PbrSpecular
uniform sampler2D PbrSpecular_specularTexture;
uniform sampler2D PbrSpecular_specularColorTexture;

struct PbrSpecular
{
	// RGB: specularColor, A: specularFactor (Padrão=1.0);
	vec4 specularColorAndSpecularFactor;
	// R: use specularTexture, G: use specularColorTexture
	vec4 specularTextures;
};

// PbrVolume
uniform sampler2D PbrVolume_thicknessTexture;

struct PbrVolume
{
	// R: thicknessFactor (Padrão=0.0), RGB: attenuationColor
	vec4 thicknessFactorAndAttenuationColor;
	// R: attentuationDistance (Padrão=-1.0)
	vec4 attenuationDistance;
	// R: use thicknessTexture
	vec4 volumeTextures;
};

// PbrSheen
uniform sampler2D PbrSheen_sheenColorTexture;
uniform sampler2D PbrSheen_sheenRoughnessTexture;

struct PbrSheen
{
	// RGB: sheenColor, A: sheenRoughnessFactor (Padrão=0.0)
	vec4 sheenColorAndRoughnessFactor;
	// R: use sheenColorTexture, G: use sheenRoughnessTexture
	vec4 sheenTextures;
};

struct PbrEmissiveStrength
{
	// R: emissiveStrength (Padrão=1.0)
	vec4 emissiveStrength;
};

// PbrIridescence
uniform sampler2D PbrEmissive_iridescenceTexture;
uniform sampler2D PbrEmissive_iridescenceThicknessTexture;

struct PbrIridescence
{
	// R: iridescenceFactor (Padrão=0.0), G: iridescenceIor (Padrão=1.3), B: iridescenceThicknessMin (Padrão=100.0), A: iridescenceThicknessMax (Padrão=400.0)
	vec4 iridescenceFactorAndIorAndThicknessMinMax;
	// R: use iridescenceTexture, G: use iridescenceThicknessTexture
	vec4 iridescenceTextures;
};

uniform PbrMaterial
{
	// Propriedades comuns
	// R: alphaCutoff (Padrão=0.5), G: doubleSided (Padrão=false), B: unlit (Padrão=false)
	vec4 pbrAlphaCutoffAndDoubleSidedAndIsUnlit;
	// R: use normalTexture, G: use occlusionTexture, B: use emissiveTexture
	vec4 pbrCommonTextures;

	// Recursos
#ifdef PBR_METALLIC_ROUGHNESS
	PbrMetallicRoughness  pbrMetallicRoughness;
#endif
#ifdef PBR_SPECULAR_GLOSSINESS
	PbrSpecularGlossiness pbrSpecularGlossiness;
#endif
#ifdef PBR_CLEARCOAT
	PbrClearCoat pbrClearCoat;
#endif
#ifdef PBR_TRANSMISSION
	PbrTransmission pbrTransmission;
#endif
#ifdef PBR_IOR
	PbrIor pbrIor;
#endif
#ifdef PBR_SPECULAR
	PbrSpecular pbrSpecular;
#endif
#ifdef PBR_VOLUME
	PbrVolume pbrVolume;
#endif
#ifdef PBR_SHEEN
	PbrSheen pbrSheen;
#endif
#ifdef PBR_EMISSIVE_STRENGTH
	PbrEmissiveStrength pbrEmissiveStrength;
#endif
#ifdef PBR_IRIDESCENCE
	PbrIridescence pbrIridescence;
#endif
};
```

::: sidenote
Se pontos de dados específicos na struct de material não forem encontrados, os dados desses recursos não serão definidos. Por exemplo, se não houver `pbrClearCoat` na struct de material, nenhum dado de clear coat será definido. Se o bloco uniform não for encontrado, nenhum dado será definido durante a renderização.
:::

### Constantes

Cada propriedade de material corresponde a uma constante interna de renderização no Defold. Você pode sobrescrever valores padrão definindo constantes no próprio recurso de material, seguindo o padrão de nomenclatura `pbrFeature.structMember`. Esses valores serão aplicados automaticamente se os dados correspondentes estiverem ausentes no material glTF.

![Material constants](images/physically-based-rendering/material-constants.png)

## Próximos passos

Para usar os dados de material em iluminação fisicamente baseada, implemente uma BRDF no seu fragment shader usando os parâmetros fornecidos no bloco `PbrMaterial`.
Veja também:

* [Manual de Shaders](/manuals/shader)
* [Manual de Renderização](/manuals/render)
* [Especificação glTF 2.0](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)

