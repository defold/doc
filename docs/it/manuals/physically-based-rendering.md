---
title: Rendering basato sulla fisica in Defold
brief: Questo manuale spiega come usare i materiali PBR integrati e personalizzare lo shading fisicamente basato in Defold.
---

# Rendering basato sulla fisica (PBR) {#physically-based-rendering-pbr}

Il rendering fisicamente basato (Physically Based Rendering, PBR) è un approccio allo shading che modella l'interazione della luce con le superfici usando principi fisici. Le proprietà del materiale, come colore di base, fattore metallico e rugosità, descrivono la superficie indipendentemente dall'illuminazione della scena.

I materiali glTF integrati forniscono l'illuminazione PBR. Defold espone inoltre agli shader personalizzati le proprietà dei materiali glTF 2.0 importati e i dati delle estensioni Khronos supportate.

## Materiali PBR integrati {#built-in-pbr-materials}

Assegna un file glTF o GLB alla proprietà *Scene* di un [componente Model](/manuals/model). Quando l'editor propone di compilare materiali e texture, scegli <kbd>Auto Fill</kbd> per applicare le associazioni di materiali generate dalla scena, sostituendo quelle eventualmente esistenti. Questi materiali usano gli shader glTF integrati e possono referenziare direttamente le immagini incorporate. Scegli <kbd>Keep Current</kbd> per conservare le tue associazioni e assegnare manualmente materiali e texture. Consulta il [flusso di importazione dei modelli](/manuals/importing-models/#using-a-model) per esplorare le risorse incorporate e selezionare singole mesh.

I seguenti materiali sono disponibili in `/builtins/materials/`. Scegli la variante adatta al modello e all'eventuale uso di istanze:

| Tipo di modello | Materiale |
|---|---|
| Statico, senza istanze | `gltf.material` |
| Statico, con istanze | `gltf_instanced.material` |
| Con skinning (animato), senza istanze | `gltf_skinned.material` |
| Con skinning (animato), con istanze | `gltf_skinned_instanced.material` |

Tutti e quattro usano lo spazio locale dei vertici e lo stesso fragment shader `gltf.fp`. Le varianti con skinning lo eseguono sulla GPU. Consulta i [requisiti dei materiali dei modelli](/manuals/model/#material) per lo skinning GPU e le istanze.

Per le associazioni manuali delle texture, i materiali integrati usano questi nomi di sampler:

| Texture | Sampler | Dati usati |
|---|---|---|
| Colore di base | `PbrMetallicRoughness_baseColorTexture` | Colore RGB e alpha |
| Metallic/roughness | `PbrMetallicRoughness_metallicRoughnessTexture` | Rugosità in G, fattore metallico in B |
| Normale | `PbrMaterial_normalTexture` | Normale nello spazio tangente in RGB |
| Occlusione | `PbrMaterial_occlusionTexture` | Occlusione in R |
| Emissiva | `PbrMaterial_emissiveTexture` | Colore RGB |

Configura una [camera](/manuals/camera/#using-the-camera) e aggiungi [componenti luce](/manuals/light) per illuminare il modello. Lo shader usa luci direzionali, puntiformi e spot per l'illuminazione diretta, più luci ambientali per un semplice contributo ambientale. I materiali hanno il tag `model`, disegnato dallo script di rendering predefinito. Uno script di rendering personalizzato deve disegnare un predicato corrispondente.

### Comportamento degli shader integrati {#built-in-shader-behavior}

Gli shader integrati implementano lo shading metallic/roughness, il colore di base e dei vertici, il normal mapping quando sono disponibili dati delle tangenti, l'occlusione e l'emissione, compresa l'intensità emissiva. Le texture di colore di base ed emissive vengono decodificate da sRGB per l'illuminazione e il colore finale viene riconvertito in sRGB. Le mappe metallic/roughness, delle normali e dell'occlusione contengono dati lineari.

Lo shader rispetta i materiali non illuminati e l'alpha mascherato e regola le normali per le superfici a doppia faccia. Lo stato di rendering rimane comunque determinante:

- Per i materiali a doppia faccia, disabilita il face culling nel passaggio di rendering pertinente affinché le facce posteriori raggiungano lo shader.
- Per l'alpha con fusione, lo shader produce alpha non premoltiplicato. Abilita la fusione con `graphics.BLEND_FACTOR_SRC_ALPHA` e `graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA` e gestisci nello script di rendering l'ordine di disegno degli oggetti trasparenti e le scritture della profondità. Il passaggio predefinito dei modelli non abilita automaticamente la fusione.

Il contributo ambientale integrato è un'approssimazione, senza illuminazione tramite mappe ambientali né ombre. Effetti come clearcoat, trasmissione, sheen, iridescenza e il flusso specular/glossiness richiedono uno shading personalizzato; importarli come parametri non abilita questi effetti in `gltf.fp`.

## Panoramica delle proprietà dei materiali {#material-properties-overview}

Le seguenti proprietà vengono lette dai file sorgente glTF 2.0 assegnati a un componente Model. Questo elenco descrive i dati dei materiali disponibili; l'illuminazione integrata usa il sottoinsieme descritto sopra. Non tutte le proprietà sono standard. Alcune vengono fornite tramite estensioni glTF facoltative, che possono essere incluse o meno dallo strumento usato per esportare il file glTF. L'estensione pertinente è indicata tra parentesi dopo il nome della proprietà.

Metallicità e rugosità
: Descrive l'interazione della luce con il materiale. Il modello PBR predefinito.

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
: Richiede il rendering di entrambi i lati della superficie. Il passaggio di rendering deve consentire alle facce posteriori di raggiungere lo shader.

Senza illuminazione
: Se il valore è vero, il materiale salta i calcoli dell'illuminazione.

## Integrazione negli shader {#shader-integration}

Le sezioni seguenti riguardano gli shader personalizzati. Copia nel progetto la risorsa `.material` integrata appropriata e `gltf.fp`, quindi imposta *Fragment Program* del materiale copiato sul tuo shader. Mantieni il vertex program glTF corrispondente, i nomi dei sampler e lo spazio locale dei vertici, a meno che tu non sostituisca anche queste interfacce.

Le funzioni di supporto integrate separano il campionamento delle texture dalla preparazione delle superfici, dai calcoli BRDF e dall'illuminazione. `gltf_sampling.glsl` legge il blocco uniform grezzo `PbrMaterial` e produce un valore `PBRMaterial` contenente gli ingressi del materiale risolti e lineari. `gltf_lighting.glsl` fornisce l'illuminazione diretta e ambientale e ne combina i contributi. L'uso delle maiuscole distingue il blocco uniform grezzo dalla struttura del materiale campionato.

### Shader di esempio {#example-shader}

Questo fragment shader aumenta la rugosità minima mantenendo l'illuminazione integrata. Funziona con i vertex program usati da tutte e quattro le varianti dei materiali glTF:

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

Modifica gli ingressi del materiale campionato prima di chiamare `pbr_create_material_info()`. Se cambi la posizione o le normali di una superficie nello spazio della vista, chiama `pbr_finalize_surface(surface, var_view)` per aggiornarne i campi derivati nello spazio del mondo. Per una BRDF personalizzata o i contributi delle singole luci, usa o sostituisci `pbr_evaluate_brdf()` e `pbr_evaluate_light()` delle funzioni di supporto integrate.

Puoi sostituire `lighting.indirect` con la tua illuminazione ambientale o globale. I suoi contributi diffuso e speculare sono luce uscente lineare, quindi non applicare una seconda volta la BRDF del materiale. Applica la visibilità delle ombre al contributo appropriato della luce diretta; gli argomenti di visibilità di `pbr_compose_lighting()` influiscono soltanto sull'illuminazione indiretta. Per una pipeline HDR, scrivi colori lineari nella destinazione intermedia ed esegui la conversione sRGB nel passaggio finale.

### Dati grezzi dei materiali {#raw-material-data}

Per uno shader completamente personalizzato, dichiara un blocco uniform chiamato `PbrMaterial` con i nomi e i tipi di membro riconosciuti. Defold riempie i campi corrispondenti dal materiale glTF sorgente. Le dichiarazioni seguenti descrivono le strutture delle funzionalità disponibili; includi soltanto quelle necessarie al tuo shader. Dichiarare una struttura fornisce i dati, ma lo shader deve implementarne il campionamento e il comportamento di illuminazione.

Non dichiarare di nuovo il blocco uniform o `PbrMetallicRoughness` quando includi `gltf_sampling.glsl`, che li dichiara già. Le dichiarazioni seguenti sono un'alternativa per gli shader che gestiscono autonomamente gli ingressi dei materiali.

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

Le proprietà comuni e le strutture delle funzionalità sono membri del blocco uniform. I componenti impacchettati sono:

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

Ometti dal blocco i membri delle funzionalità inutilizzate. Se mancano il blocco o i campi riconosciuti di una funzionalità, i dati corrispondenti non vengono forniti. I flag di presenza delle texture descrivono i riferimenti alle texture del materiale sorgente; un materiale personalizzato richiede comunque dichiarazioni di sampler e associazioni di texture corrispondenti per le mappe che campiona.

### Costanti {#constants}

I campi delle funzionalità usano nomi come `pbrMetallicRoughness.baseColorFactor`; i campi comuni usano nomi come `pbrEmissiveFactorAndStrength`. Il motore popola queste costanti a partire dal materiale importato o da un materiale predefinito quando il modello non contiene dati di materiale. Impostare valori predefiniti nella risorsa `.material` non sostituisce quelli importati.

Per personalizzare lo shading integrato, modifica il `PBRMaterial` campionato prima di ricavarne i valori BRDF, come nell'esempio precedente. Per ulteriori controlli a runtime, dichiara le tue costanti shader e usa l'[API delle costanti dei materiali dei modelli](/manuals/model/#material-constants).

## Passi successivi {#next-steps}

Usa i materiali integrati per il flusso standard glTF metallic/roughness. Estendi le funzioni di supporto degli shader o fornisci un materiale personalizzato quando ti servono una BRDF diversa, illuminazione ambientale, ombre o effetti aggiuntivi dei materiali glTF.

Consulta anche:

* [Manuale delle luci](/manuals/light)
* [Manuale dei materiali](/manuals/material)
* [Manuale degli shader](/manuals/shader)
* [Manuale del rendering](/manuals/render)
* [Specifica glTF 2.0](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
