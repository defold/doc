---
title: Manifeste d'application
brief: Ce manuel décrit comment utiliser le manifeste d'application pour exclure des fonctionnalités du moteur.
---

# Manifeste d'application {#app-manifest}

Le manifeste d'application contrôle les fonctionnalités et les backends liés au moteur. Il est recommandé d'exclure les fonctionnalités inutilisées, car cela réduit la taille du fichier binaire final de votre jeu. Le manifeste d'application contient également des options de build, telles que les versions minimales de navigateurs prises en charge pour HTML5 et les paramètres de mémoire WebAssembly.

![](images/app_manifest/create-app-manifest.png)

![](images/app_manifest/app-manifest.png)

# Appliquer le manifeste {#applying-the-manifest}

Dans `game.project`, affectez le manifeste à `Native Extensions` -> `App Manifest`.

## Physique 2D {#physics-2d}

Sélectionnez l'implémentation de Box2D à inclure :

* **Box2D Version 3** - Inclut Box2D 3. Cette option doit être activée explicitement et peut produire des résultats de simulation différents de ceux de l'ancienne implémentation ; les projets existants peuvent donc nécessiter un réajustement de leurs paramètres de physique.
* **Box2D (Legacy Defold version)** - Inclut l'ancienne implémentation de Box2D de Defold. Il s'agit du choix par défaut.
* **None** - Exclut la physique 2D.

Les paramètres du solveur Box2D dépendent de la version. Consultez les [paramètres de projet Box2D](/manuals/project-settings/#box2d) pour en savoir plus.

## Physique 3D {#physics-3d}

Inclut l'implémentation de physique 3D Bullet. Elle est incluse par défaut ; désactivez ce paramètre pour exclure la physique 3D.

## Squelette + modèle {#rig-model}

Contrôlez les fonctionnalités des squelettes et des modèles, ou sélectionnez None pour exclure complètement les modèles et les squelettes. (Consultez la documentation de [`Model`](https://defold.com/manuals/model/#model-component)).


## Exclure l'enregistrement {#exclude-record}

Exclut la capacité d'enregistrement vidéo du moteur (consultez la documentation du message [`start_record`](https://defold.com/ref/stable/sys/#start_record)).


## Profileur {#profiler}

Contrôlez quand les fonctionnalités du profileur sont liées au moteur :

* **Debug Only** - Inclut le profileur uniquement dans les builds de débogage. Il s'agit du choix par défaut.
* **None** - Exclut les fonctionnalités du profileur de toutes les variantes de build.
* **Always** - Inclut le profileur dans les builds de débogage et de publication.

Le paramètre du manifeste d'application contrôle si le code du profileur est lié à un build. Les paramètres de la section `profiler` de *game.project* contrôlent le comportement du profileur à l'exécution. Découvrez comment utiliser les outils disponibles dans le [manuel de profilage](/manuals/profiling/).


## Son {#sound}

Les paramètres du son déterminent le système audio et les décodeurs liés au moteur.

### Exclure le son {#exclude-sound}

Exclut toutes les capacités de lecture audio du moteur.

### Exclure le décodeur audio : WAV {#exclude-sound-decoder-wav}

Exclut la prise en charge des ressources audio WAV.

### Exclure le décodeur audio : OGG {#exclude-sound-decoder-ogg}

Exclut la prise en charge des ressources audio Ogg Vorbis.

### Inclure le décodeur audio : Opus {#include-sound-decoder-opus}

Inclut la prise en charge des ressources audio Ogg Opus. Le décodeur Opus est exclu par défaut ; cette option doit donc être activée avant de pouvoir lire les ressources `.opus`. Consultez le [manuel du son](/manuals/sound/) pour connaître les formats pris en charge.


## Exclure les entrées {#exclude-input}

Exclut toute la gestion des entrées du moteur.


## Exclure Live Update {#exclude-live-update}

Exclut la [fonctionnalité Live Update](/manuals/live-update) du moteur.


## Exclure Image {#exclude-image}

Exclut le module de script `image` ([documentation](https://defold.com/ref/stable/image/)) du moteur.


## Exclure Types {#exclude-types}

Exclut le module de script `types` ([documentation](https://defold.com/ref/stable/types/)) du moteur.


## Exclure le transcodeur Basis {#exclude-basis-transcoder}

Exclut la [bibliothèque de compression de textures](/manuals/texture-profiles) Basis Universal du moteur.


## Utiliser la bibliothèque Android Support {#use-android-support-lib}

Utilise la bibliothèque obsolète Android Support Library à la place d'Android X. [En savoir plus](https://defold.com/manuals/android/#using-androidx).


## Graphismes {#graphics}

Sélectionnez les backends graphiques à inclure pour chaque plateforme. Un choix combiné inclut les deux backends, ce qui permet de basculer vers l'autre lorsque le backend préféré n'est pas disponible.

| Champ | Plateformes | Choix | Par défaut |
|---|---|---|---|
| **Graphics** | Windows et Linux | OpenGL, Vulkan, OpenGL & Vulkan | OpenGL |
| **Graphics (macOS)** | macOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | Vulkan |
| **Graphics (iOS)** | iOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | OpenGL |
| **Graphics (Android)** | Android | OpenGL+Vulkan, OpenGL, Vulkan | OpenGL+Vulkan |
| **Graphics (HTML5)** | HTML5 | WebGL, WebGPU, WebGL & WebGPU | WebGL |

Sur Linux ARM64, le choix **OpenGL** utilise le backend OpenGL ES. Le choix combiné par défaut sur Android privilégie Vulkan lorsqu'il est disponible et utilise OpenGL ES en solution de repli.

## Utiliser le système complet de mise en page du texte {#use-full-text-layout-system}

Si cette option est activée (`true`), elle permet de générer à l'exécution des polices de type SDF lorsque le projet utilise des polices True Type (`.ttf`). Consultez le [manuel des polices](https://defold.com/manuals/font/#enabling-runtime-fonts) pour en savoir plus.


## Versions minimales des navigateurs {#minimum-browser-versions}

Les champs YAML **`minSafariVersion`**, **`minFirefoxVersion`** et **`minChromeVersion`** définissent les versions minimales des navigateurs ciblés par Emscripten. Les valeurs par défaut actuelles et les versions minimales prises en charge diffèrent entre les cibles sans threads et avec threads :

| Cible | Safari | Firefox | Chrome |
|---|---:|---:|---:|
| `wasm-web` | `101000` | `40` | `45` |
| `wasm_pthread-web` | `150000` | `79` | `75` |

Définissez les valeurs de remplacement dans le contexte de la cible concernée. La cible avec threads a également des [exigences d'hébergement](/manuals/html5/#creating-html5-bundle) supplémentaires. Consultez la référence des paramètres Emscripten pour [`MIN_SAFARI_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-safari-version), [`MIN_FIREFOX_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-firefox-version) et [`MIN_CHROME_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-chrome-version).

## Mémoire initiale (HTML5) {#initial-memory-html5}
Nom du champ YAML : **`initialMemory`**
Valeur par défaut : **33554432**

La quantité initiale de mémoire allouée à l'application web, en octets. La valeur doit être un multiple de la taille d'une page WebAssembly (64 KiB). Consultez le paramètre [`INITIAL_MEMORY`](https://emscripten.org/docs/tools_reference/settings_reference.html#initial-memory) d'Emscripten.

Cette option fournit la valeur par défaut à la compilation. La valeur [`html5.heap_size`](/manuals/html5/#heap-size) de *game.project* la remplace à l'exécution.

## Taille de la pile (HTML5) {#stack-size-html5}
Nom du champ YAML : **`stackSize`**
Valeur par défaut : **5242880**

La taille de la pile de l'application, en octets. Consultez le paramètre [`STACK_SIZE`](https://emscripten.org/docs/tools_reference/settings_reference.html#stack-size) d'Emscripten.
