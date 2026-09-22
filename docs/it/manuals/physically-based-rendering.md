---
title: Rendering basato sulla fisica in Defold
brief: Questo manuale spiega le basi per accedere ai dati dei materiali per il rendering basato sulla fisica in Defold.
---

# Rendering basato sulla fisica (PBR) {#physically-based-rendering-pbr}

Il rendering basato sulla fisica (Physically Based Rendering, PBR) è un metodo di ombreggiatura che modella l'interazione della luce con le superfici usando principi fisici del mondo reale. Produce un'illuminazione coerente e realistica in ambienti diversi e permette agli asset di avere un aspetto corretto in un'ampia gamma di condizioni di illuminazione.

L'implementazione PBR di Defold segue la specifica dei materiali glTF 2.0 e le relative estensioni Khronos. Quando importi asset glTF in Defold, le proprietà dei materiali vengono analizzate automaticamente e memorizzate come dati strutturati, accessibili dagli shader durante l'esecuzione.

I materiali PBR possono includere effetti come riflessi metallici, rugosità superficiale, trasmissione, rivestimento trasparente, diffusione subsuperficiale, iridescenza e altro ancora.

::: sidenote
Attualmente Defold espone i dati dei materiali PBR agli shader, ma non fornisce un modello di illuminazione PBR integrato. Puoi usare questi dati nei tuoi shader di illuminazione e riflessione per ottenere un rendering basato sulla fisica. Un modello di illuminazione PBR predefinito verrà aggiunto a Defold in una fase successiva.
:::

::: sidenote
Attualmente le texture incorporate nei file glTF non vengono assegnate automaticamente in Defold. Agli shader vengono esposti solo i parametri dei materiali. Puoi comunque assegnare manualmente le texture ai componenti modello e campionarle nel tuo shader.
:::

## Panoramica delle proprietà dei materiali {#material-properties-overview}

Le proprietà dei materiali vengono lette dai file sorgente glTF 2.0 assegnati a un componente modello. Non tutte le proprietà sono standard. Alcune sono fornite tramite estensioni glTF facoltative, che lo strumento usato per esportare il file glTF potrebbe includere oppure no. L'estensione pertinente è indicata tra parentesi dopo il nome della proprietà riportato di seguito.

Metallicità e rugosità
: Descrive come la luce interagisce con il materiale. È il modello PBR predefinito.

Specularità e lucentezza (KHR_materials_pbrSpecularGlossiness)
: Un'alternativa al modello metallicità e rugosità. Spesso usata negli asset meno recenti.

Rivestimento trasparente (KHR_materials_clearcoat)
: Aggiunge uno strato di rivestimento trasparente con rugosità e mappa delle normali proprie.

Indice di rifrazione (KHR_materials_ior)
: Aggiunge un indice di rifrazione.

Specularità (KHR_materials_specular)
: Aggiunge un canale dedicato all'intensità e al colore speculari.

Iridescenza (KHR_materials_iridescence)
: Simula l'interferenza di film sottili per materiali come bolle di sapone o perle.

Riflessi del tessuto (KHR_materials_sheen)
: Modella le riflessioni della microsuperficie tipiche dei tessuti.

Trasmissione (KHR_materials_transmission)
: Modella la trasmissione della luce per materiali trasparenti o simili al vetro.

Volume (KHR_materials_volume)
: Supporta effetti volumetrici come spessore e attenuazione.

Intensità di emissione (KHR_materials_emissive_strength)
: Controlla la luminosità emessa indipendentemente dal colore di base.

Mappa delle normali
: Mappa delle normali per i dettagli della superficie.

Mappa di occlusione
: Mappa di occlusione ambientale.

Mappa di emissione
: Texture autoemissiva per superfici luminose.

Fattore di emissione
: Moltiplicatore RGB per l'intensità di emissione

Soglia alfa
: Soglia per la trasparenza mascherata.

Modalità alfa
: Modalità di trasparenza opaca, mascherata o con fusione.

A due lati
: Se il valore è vero, vengono disegnati entrambi i lati della superficie.

Senza illuminazione
: Se il valore è vero, il materiale salta i calcoli dell'illuminazione.

::: sidenote
Alcune di queste proprietà forniscono indicazioni su come il materiale dovrebbe essere disegnato. I dati delle proprietà (soglia alfa, modalità alfa, a due lati e senza illuminazione) sono disponibili negli shader, ma non influenzano il modo in cui il materiale viene disegnato in Defold.
:::

## Integrazione negli shader {#shader-integration}

I dati dei materiali PBR vengono esposti agli shader in base ai tipi e a una convenzione di denominazione. Il sistema dei materiali PBR fornisce agli shader tutti i parametri dei materiali analizzati tramite un blocco uniform strutturato chiamato `PbrMaterial`. Ogni estensione glTF supportata corrisponde a una struttura in questo blocco, che può essere compilata in modo condizionale usando flag `#define`.

```glsl
uniform PbrMaterial
{
	// Material properties
};
```

Le varie funzionalità del materiale sono specificate nello shader tramite strutture fisse. I dati sono stati raggruppati il più possibile in valori `vec4`, perché questo è il formato con cui vengono impostate internamente le costanti in Defold. I casi in cui i dati sono stati raggruppati sono indicati nei commenti degli esempi di shader per ciascuna funzionalità riportati di seguito:

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
	// R: thicknessFactor (Default=0.0), RGB: attenuationColor
	vec4 thicknessFactorAndAttenuationColor;
	// R: attentuationDistance (Default=-1.0)
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

Le proprietà comuni vengono impostate direttamente nell'uniform del materiale (anche qui, nota il raggruppamento dei dati in `vec4`).

```glsl
// Common textures
uniform sampler2D PbrMaterial_normalTexture;
uniform sampler2D PbrMaterial_occlusionTexture;
uniform sampler2D PbrMaterial_emissiveTexture;

uniform PbrMaterial
{
	// Common properties:

	// R: alphaCutoff (Default=0.5), G: doubleSided (Default=false), B: unlit (Default=false)
	vec4 pbrAlphaCutoffAndDoubleSidedAndIsUnlit;
	// R: use normalTexture, G: use occlusionTexture, B: use emissiveTexture
	vec4 pbrCommonTextures;

	// Other properties...
};
```

### Shader di esempio {#example-shader}

Ecco uno shader di esempio che contiene tutte le funzionalità e una proposta di schema di denominazione per i binding delle texture (anche questi devono essere gestiti manualmente). Puoi disattivare le funzionalità semplicemente usando direttive `#define` attorno a ciascun membro di `PbrMaterial`, come mostrato nell'esempio seguente:

```glsl
// Feature flags, comment or remove these to slim down the shader.
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

// Common
uniform sampler2D PbrMaterial_normalTexture;
uniform sampler2D PbrMaterial_occlusionTexture;
uniform sampler2D PbrMaterial_emissiveTexture;

// PbrMetallicRoughness
uniform sampler2D PbrMetallicRoughness_baseColorTexture;
uniform sampler2D PbrMetallicRoughness_metallicRoughnessTexture;

struct PbrMetallicRoughness
{
    vec4 baseColorFactor;
    // R: metallic (Default=1.0), G: roughness (Default=1.0)
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
	// RGB: specular (Default=1.0), A: glossiness (Default=1.0)
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
	// R: clearCoat (Default=0.0), G: clearCoatRoughness (Default=0.0)
	vec4 clearCoatAndClearCoatRoughnessFactor;
	// R: use clearCoatTexture, G: use clearCoatRoughnessTexture, B: use clearCoatNormalTexture
	vec4 clearCoatTextures;
};

// PbrTransmission
uniform sampler2D PbrTransmission_transmissionTexture;

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

// PbrSpecular
uniform sampler2D PbrSpecular_specularTexture;
uniform sampler2D PbrSpecular_specularColorTexture;

struct PbrSpecular
{
	// RGB: specularColor, A: specularFactor (Default=1.0);
	vec4 specularColorAndSpecularFactor;
	// R: use specularTexture, G: use specularColorTexture
	vec4 specularTextures;
};

// PbrVolume
uniform sampler2D PbrVolume_thicknessTexture;

struct PbrVolume
{
	// R: thicknessFactor (Default=0.0), RGB: attenuationColor
	vec4 thicknessFactorAndAttenuationColor;
	// R: attentuationDistance (Default=-1.0)
	vec4 attenuationDistance;
	// R: use thicknessTexture
	vec4 volumeTextures;
};

// PbrSheen
uniform sampler2D PbrSheen_sheenColorTexture;
uniform sampler2D PbrSheen_sheenRoughnessTexture;

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

// PbrIridescence
uniform sampler2D PbrEmissive_iridescenceTexture;
uniform sampler2D PbrEmissive_iridescenceThicknessTexture;

struct PbrIridescence
{
	// R: iridescenceFactor (Default=0.0), G: iridescenceIor (Default=1.3), B: iridescenceThicknessMin (Default=100.0), A: iridescenceThicknessMax (Default=400.0)
	vec4 iridescenceFactorAndIorAndThicknessMinMax;
	// R: use iridescenceTexture, G: use iridescenceThicknessTexture
	vec4 iridescenceTextures;
};

uniform PbrMaterial
{
	// Common properties
	// R: alphaCutoff (Default=0.5), G: doubleSided (Default=false), B: unlit (Default=false)
	vec4 pbrAlphaCutoffAndDoubleSidedAndIsUnlit;
	// R: use normalTexture, G: use occlusionTexture, B: use emissiveTexture
	vec4 pbrCommonTextures;

	// Features
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
Se determinati campi non vengono trovati nella struttura del materiale, i dati delle relative funzionalità non vengono impostati. Per esempio, se nella struttura del materiale non è presente `pbrClearCoat`, non verranno impostati dati per il rivestimento trasparente. Se il blocco uniform non viene trovato, non verrà impostato alcun dato durante il rendering.
:::

### Costanti {#constants}

Ogni proprietà del materiale corrisponde a una costante di rendering interna di Defold. Puoi sovrascrivere i valori predefiniti definendo le costanti direttamente nella risorsa materiale, seguendo il modello di denominazione `pbrFeature.structMember`. Questi valori verranno applicati automaticamente se i dati corrispondenti non sono presenti nel materiale glTF.

![Costanti del materiale](images/physically-based-rendering/material-constants.png)

## Passi successivi {#next-steps}

Per usare i dati del materiale per un'illuminazione basata sulla fisica, implementa una BRDF nel tuo fragment shader usando i parametri forniti nel blocco `PbrMaterial`.
Consulta anche:

* [Manuale degli shader](/manuals/shader)
* [Manuale del rendering](/manuals/render)
* [Specifica glTF 2.0](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
