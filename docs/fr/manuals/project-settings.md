---
title: Paramètres d'un projet Defold
brief: Ce manuel décrit le fonctionnement des paramètres propres à chaque projet dans Defold.
---

# Paramètres du projet {#project-settings}

Le fichier *game.project* contient tous les paramètres qui s'appliquent à l'ensemble du projet. Il doit rester dans le dossier racine du projet et doit s'appeler *game.project*. La première chose que fait le moteur au démarrage, lorsqu'il lance votre jeu, est de rechercher ce fichier.

Chaque paramètre du fichier appartient à une catégorie. Lorsque vous ouvrez le fichier, Defold présente tous les paramètres regroupés par catégorie.

![Paramètres du projet](images/project-settings/settings.jpg)


## Format du fichier {#file-format}

Les paramètres de *game.project* sont généralement modifiés dans Defold, mais vous pouvez aussi modifier le fichier dans n'importe quel éditeur de texte standard. Le fichier respecte le format INI et se présente ainsi :

```ini
[category1]
setting1 = value
setting2 = value
[category2]
...
```

Voici un exemple concret :

```ini
[bootstrap]
main_collection = /main/main.collectionc
```

ce qui signifie que le paramètre *main_collection* appartient à la catégorie *bootstrap*. Chaque fois qu'une référence à un fichier est utilisée, comme dans l'exemple ci-dessus, le caractère 'c' doit être ajouté à la fin du chemin pour indiquer que vous faites référence à la version compilée du fichier. Notez également que le dossier contenant *game.project* constitue la racine du projet, ce qui explique le '/' initial dans le chemin du paramètre.


## Accès à l'exécution {#runtime-access}

Vous pouvez lire les valeurs de *game.project* à l'exécution à l'aide de [`sys.get_config_string(key)`](/ref/sys/#sys.get_config_string), [`sys.get_config_number(key)`](/ref/sys/#sys.get_config_number), [`sys.get_config_int(key)`](/ref/sys/#sys.get_config_int) et [`sys.get_config_boolean(key)`](/ref/sys/#sys.get_config_boolean). Exemples :

```lua
local title = sys.get_config_string("project.title")
local gravity_y = sys.get_config_number("physics.gravity_y")
local fullscreen = sys.get_config_boolean("display.fullscreen", false)
```

::: sidenote
La clé combine le nom de la catégorie et celui du paramètre, séparés par un point, écrits en minuscules et avec les espaces remplacés par des traits de soulignement. Exemples : le champ « Title » de la catégorie « Project » devient `project.title`, et le champ « Gravity Y » de la catégorie « Physics » devient `physics.gravity_y`.
:::


## Sections et paramètres {#sections-and-settings}

Tous les paramètres disponibles sont présentés ci-dessous, classés par catégorie.

### Project {#project}

#### Title {#title}
Le titre de l'application.

#### Version {#version}
La version de l'application.

#### Publisher {#publisher}
Le nom de l'éditeur de l'application.

#### Developer {#developer}
Le nom du développeur.

#### Write Log File {#write-log-file}
Détermine quand le moteur écrit un fichier journal. Options :

- "Never" : ne pas écrire de fichier journal.
- "Debug" : écrire un fichier journal uniquement pour les builds Debug.
- "Always" : écrire un fichier journal pour les builds Debug et Release.

Si vous exécutez plusieurs instances depuis l'éditeur, le fichier s'appellera *instance_2_log.txt*, où `2` est l'indice de l'instance. Si vous exécutez une seule instance ou lancez l'application depuis un bundle, le fichier s'appellera *log.txt*. Le fichier journal sera placé à l'un des chemins suivants, essayés dans cet ordre :

1. Le chemin indiqué dans *project.log_dir* (paramètre masqué)
2. Le chemin des journaux système :
  * macOS/iOS : `NSDocumentDirectory`
  * Android : `Context.getExternalFilesDir()`
  * Autres : racine de l'application
3. Le chemin des données de prise en charge de l'application
  * macOS/iOS : `NSApplicationSupportDirectory`
  * Windows : `CSIDL_APPDATA` (par exemple `C:\Users\<username>\AppData\Roaming`)
  * Android : `Context.getFilesDir()`
  * Linux : variable d'environnement `HOME`

#### Minimum Log Level {#minimum-log-level}
Définissez le niveau minimal de journalisation. Seuls les messages de ce niveau ou d'un niveau supérieur seront affichés.

#### Compress Archive {#compress-archive}
Active la compression des archives lors de la création des bundles. Notez que cela s'applique actuellement à toutes les plateformes sauf Android, où l'apk contient déjà toutes les données sous forme compressée.

#### Dependencies {#dependencies}
Une liste d'URL correspondant aux *Library URL* du projet. Consultez le [manuel des bibliothèques](/manuals/libraries/) pour en savoir plus.

#### Custom Resources {#custom-resources}
`custom_resources`
:[Custom Resources](../shared/custom-resources.md)

Le chargement des ressources personnalisées est présenté plus en détail dans le [manuel d'accès aux fichiers](/manuals/file-access/#how-to-access-files-bundled-with-the-application).

Les chemins fournis par les extensions via `custom_resources.default` dans `ext.properties` sont combinés à ce paramètre. Consultez [Ressources personnalisées des extensions](/manuals/extensions/#custom-resources) pour un exemple.

#### Bundle Resources {#bundle-resources}
`bundle_resources`
:[Bundle Resources](../shared/bundle-resources.md)

Le chargement des ressources du bundle est présenté plus en détail dans le [manuel d'accès aux fichiers](/manuals/file-access/#how-to-access-files-bundled-with-the-application).

#### Bundle Exclude Resources {#bundle-exclude-resources}
`bundle_exclude_resources`
Une liste de ressources, séparées par des virgules, qui ne doivent pas être incluses dans le bundle. Elles sont donc retirées du résultat du rassemblement des ressources effectué à l'étape `bundle_resources`.

---

### Bootstrap {#bootstrap}

#### Main Collection {#main-collection}
Référence au fichier de collection à utiliser pour démarrer l'application, `/logic/main.collection` par défaut.

#### Render {#render}
Le fichier de configuration du rendu à utiliser, qui définit la chaîne de rendu, `/builtins/render/default.render` par défaut.

---

### Library {#library}

#### Include Dirs {#include-dirs}
Une liste de répertoires, séparés par des espaces, à partager depuis votre projet via le partage de bibliothèques. Consultez le [manuel des bibliothèques](/manuals/libraries/) pour en savoir plus.

---

### Script {#script}

#### Shared State {#shared-state}
Cochez cette option pour partager un même état Lua entre tous les types de scripts.

---

### Engine {#engine}

#### Run While Iconified {#run-while-iconified}
Autorise le moteur à continuer de fonctionner lorsque la fenêtre de l'application est réduite (plateformes de bureau uniquement).

#### Fixed Update Frequency {#fixed-update-frequency}
La fréquence de mise à jour de la fonction de cycle de vie `fixed_update(self, dt)`, en hertz.

#### Max Time Step {#max-time-step}
Si le pas de temps devient trop grand au cours d'une même image, il sera limité à cette valeur maximale, en secondes.

---

### Display {#display}

#### Width {#width}
La largeur de la fenêtre de l'application, en pixels.

#### Height {#height}
La hauteur de la fenêtre de l'application, en pixels.

#### High Dpi {#high-dpi}
Crée un tampon arrière à haute densité de pixels sur les écrans compatibles. En général, le jeu sera rendu à une résolution deux fois supérieure à celle définie par les paramètres *Width* et *Height*, qui restera la résolution logique utilisée dans les scripts et les propriétés.

#### Samples {#samples}
Le nombre d'échantillons à utiliser pour l'anticrénelage par suréchantillonnage. Ce paramètre définit l'indication de fenêtre `GLFW_FSAA_SAMPLES`. Une valeur de `0` signifie que l'anticrénelage est désactivé.

Ce paramètre contrôle la fenêtre. Les [cibles de rendu multi-échantillonnées](/manuals/render/#multisampled-render-targets) hors écran possèdent leur propre nombre d'échantillons.

#### Fullscreen {#fullscreen}
Cochez cette option si l'application doit démarrer en plein écran. Si elle est décochée, l'application s'exécute dans une fenêtre.

#### Update Frequency {#update-frequency}
La fréquence d'images souhaitée, en hertz. Définissez-la sur 0 pour une fréquence d'images variable. Une valeur supérieure à 0 produit une fréquence d'images fixe, plafonnée à l'exécution par la fréquence d'images réelle (vous ne pouvez donc pas mettre à jour la boucle de jeu deux fois au cours d'une image du moteur). Utilisez [`sys.set_update_frequency(hz)`](https://defold.com/ref/stable/sys/?q=set_update_frequency#sys.set_update_frequency:frequency) pour modifier cette valeur à l'exécution. Ce paramètre fonctionne également dans les builds sans interface graphique (headless).

#### Swap interval {#swap-interval}
Cette valeur entière détermine la façon dont l'application gère la synchronisation verticale. 0 désactive la synchronisation verticale, et la valeur par défaut est 1. Avec un adaptateur OpenGL, cette valeur définit le nombre d'images que la fenêtre doit [mettre à jour entre les échanges de tampons](https://www.khronos.org/opengl/wiki/Swap_Interval). Vulkan ne possède pas de notion intégrée d'intervalle d'échange ; la valeur détermine à la place si la synchronisation verticale doit être activée ou non.

#### Vsync {#vsync}
Paramètre de compatibilité avec les anciennes versions. Ce paramètre est obsolète ; utilisez **Swap Interval** pour les nouveaux projets. S'il est désactivé, il force l'intervalle d'échange effectif à `0`. S'il est activé, **Swap Interval** détermine la valeur effective.

#### Display Profiles {#display-profiles}
Définit le fichier de profils d'affichage à utiliser, `/builtins/render/default.display_profilesc` par défaut. Pour en savoir plus, consultez le [manuel des dispositions d'interface graphique](/manuals/gui-layouts/#creating-display-profiles).

#### Dynamic Orientation {#dynamic-orientation}
Cochez cette option si l'application doit basculer dynamiquement entre les modes portrait et paysage lorsque l'appareil pivote. Notez que l'application de développement ne respecte actuellement pas ce paramètre.

#### Display Device Info {#display-device-info}
Affiche les informations sur le GPU dans la console au démarrage.

---

### Render {#render}

#### Clear Color Red {#clear-color-red}
Canal rouge de la couleur d'effacement, utilisé par le script de rendu et lors de la création de la fenêtre.

#### Clear Color Green {#clear-color-green}
Canal vert de la couleur d'effacement, utilisé par le script de rendu et lors de la création de la fenêtre.

#### Clear Color Blue {#clear-color-blue}
Canal bleu de la couleur d'effacement, utilisé par le script de rendu et lors de la création de la fenêtre.

#### Clear Color Alpha {#clear-color-alpha}
Canal alpha de la couleur d'effacement, utilisé par le script de rendu et lors de la création de la fenêtre.

---

### Font {#font}

#### Runtime Generation {#runtime-generation}
Utilise la génération des polices à l'exécution.

---

### Physics {#physics}

#### Max Collision Object Count {#max-collision-object-count}
Le nombre maximal d'objets de collision.

#### Type {#type}
Le type de physique à utiliser, `2D` ou `3D`.

#### Gravity X {#gravity-x}
La gravité du monde selon l'axe x, en mètres par seconde.

#### Gravity Y {#gravity-y}
La gravité du monde selon l'axe y, en mètres par seconde.

#### Gravity Z {#gravity-z}
La gravité du monde selon l'axe z, en mètres par seconde.

#### Debug {#debug}
Cochez cette option pour visualiser la physique à des fins de débogage.

#### Debug Alpha {#debug-alpha}
La valeur de la composante alpha pour la visualisation de la physique, `0`--`1`.

#### World Count {#world-count}
Le nombre maximal de mondes physiques simultanés, `4` par défaut. Si vous chargez plus de quatre mondes simultanément au moyen de proxys de collection (collection proxy), vous devez augmenter cette valeur. Sachez que chaque monde physique alloue une quantité de mémoire non négligeable.

#### Scale {#scale}
Indique au moteur physique comment mettre les mondes physiques à l'échelle par rapport au monde de jeu (game world) pour assurer la précision numérique, `0.01`--`1.0`. Si la valeur est définie sur `0.02`, le moteur physique considère que 50 unités représentent 1 mètre ($1 / 0.02$).

#### Allow Dynamic Transforms {#allow-dynamic-transforms}
Cochez cette option pour que le moteur physique applique la transformation d'un objet de jeu (game object) à tous les composants (component) d'objet de collision qui lui sont rattachés. Cela permet de déplacer, redimensionner et faire pivoter les formes de collision, y compris les formes dynamiques.

#### Use Fixed Timestep {#use-fixed-timestep}
Cochez cette option pour que le moteur physique utilise des mises à jour fixes, indépendantes de la fréquence d'images. Utilisez ce paramètre avec la fonction de cycle de vie `fixed_update(self, dt)` et le paramètre de projet `engine.fixed_update_frequency` pour interagir avec le moteur physique à intervalles réguliers. Pour les nouveaux projets, la valeur recommandée est `true`.

#### Debug Scale {#debug-scale}
La taille de dessin des objets unitaires de la physique, tels que les trièdres et les normales.

#### Max Collisions {#max-collisions}
Le nombre de collisions qui seront signalées aux scripts.

#### Max Contacts {#max-contacts}
Le nombre de points de contact qui seront signalés aux scripts.

#### Contact Impulse Limit {#contact-impulse-limit}
Ignore les impulsions de contact dont la valeur est inférieure à ce paramètre.

#### Ray Cast Limit 2d {#ray-cast-limit-2d}
Le nombre maximal de requêtes de lancer de rayon 2D par image.

#### Ray Cast Limit 3d {#ray-cast-limit-3d}
Le nombre maximal de requêtes de lancer de rayon 3D par image.

#### Trigger Overlap Capacity {#trigger-overlap-capacity}
Le nombre maximal de déclencheurs physiques qui se chevauchent.

#### Velocity Threshold {#velocity-threshold}
La vitesse minimale à partir de laquelle les collisions sont élastiques.

#### Max Fixed Timesteps {#max-fixed-timesteps}
Le nombre maximal d'étapes de simulation avec un pas de temps fixe (3D uniquement).

---

### Graphics {#graphics}

#### Default Texture Min Filter {#default-texture-min-filter}
Définit le filtrage à utiliser pour la réduction.

#### Default Texture Mag Filter {#default-texture-mag-filter}
Définit le filtrage à utiliser pour l'agrandissement.

#### Max Draw Calls {#max-draw-calls}
Le nombre maximal d'appels de rendu.

#### Max Characters: {#max-characters}
Le nombre de caractères préalloués dans le tampon de rendu du texte, c'est-à-dire le nombre de caractères pouvant être affichés à chaque image.

#### Max Font Batches {#max-font-batches}
Le nombre maximal de lots de texte pouvant être affichés à chaque image.

#### Max Debug Vertices {#max-debug-vertices}
Le nombre maximal de sommets de débogage. Ils sont notamment utilisés pour le rendu des formes physiques.

#### Texture Profiles {#texture-profiles}
Le fichier de profils de texture à utiliser pour ce projet, `/builtins/graphics/default.texture_profiles` par défaut.

#### Verify Graphics Calls {#verify-graphics-calls}
Vérifie la valeur de retour après chaque appel graphique et signale les éventuelles erreurs dans le journal.

#### WebGL Version Hint {#webgl-version-hint}
`graphics.webgl_version_hint` sélectionne la version du contexte WebGL à demander pour HTML5. Les valeurs valides sont `1` (WebGL 1) et `2` (WebGL 2, valeur par défaut). Définissez-la sur `1` pour cibler ou tester WebGL 1, même dans un navigateur prenant en charge WebGL 2. Laissez [Exclude GLES 2.0](#exclude-gles-20) désactivé lorsque vous ciblez WebGL 1 afin d'inclure les shaders nécessaires.

#### OpenGL Version Hint {#opengl-version-hint}
Indication de la version du contexte OpenGL. Si une version précise est sélectionnée, elle sera utilisée comme version minimale requise (ne s'applique pas à OpenGL ES).

#### OpenGL Core Profile Hint {#opengl-core-profile-hint}
Définit l'indication de profil OpenGL 'core' lors de la création du contexte. Le profil core retire toutes les fonctionnalités obsolètes d'OpenGL, comme le rendu en mode immédiat. Ne s'applique pas à OpenGL ES.

#### Vulkan Version Major {#vulkan-version-major}
`graphics.vulkan_version_major` indique la version majeure souhaitée pour le contexte et l'API Vulkan. Cela s'applique uniquement lorsque le backend graphique Vulkan est sélectionné. La valeur par défaut est `1`.

#### Vulkan Version Minor {#vulkan-version-minor}
`graphics.vulkan_version_minor` indique la version mineure souhaitée pour le contexte et l'API Vulkan. Cela s'applique uniquement lorsque le backend graphique Vulkan est sélectionné. La valeur par défaut est `0`.

---

### Shader {#shader}

#### Exclude GLES 2.0 {#exclude-gles-20}
Ne compile pas les shaders pour les appareils utilisant OpenGLES 2.0 / WebGL 1.0.

#### GLSL ES Default Precision Float {#glsl-es-default-precision-float}
`shader.glsl_es_default_precision_float` définit le qualificateur de précision global par défaut des valeurs à virgule flottante dans les shaders GLSL ES issus de la compilation croisée. Les valeurs valides sont `mediump` et `highp` ; la valeur par défaut est `mediump`.

#### GLSL ES Default Precision Int {#glsl-es-default-precision-int}
`shader.glsl_es_default_precision_int` définit le qualificateur de précision global par défaut des valeurs entières dans les shaders GLSL ES issus de la compilation croisée. Les valeurs valides sont `mediump` et `highp` ; la valeur par défaut est `highp`.

---

### Input {#input}

#### Repeat Delay {#repeat-delay}
Le nombre de secondes à attendre avant qu'une entrée maintenue enfoncée commence à se répéter.

#### Repeat Interval {#repeat-interval}
Le nombre de secondes à attendre entre chaque répétition d'une entrée maintenue enfoncée.

#### Gamepads {#gamepads}
Référence au fichier de configuration des manettes, qui associe leurs signaux au système d'exploitation, `/builtins/input/default.gamepads` par défaut.

#### Game Binding {#game-binding}
Référence au fichier de configuration des entrées, qui associe les entrées matérielles à des actions, `/input/game.input_binding` par défaut.

#### Use Accelerometer {#use-accelerometer}
Cochez cette option pour que le moteur reçoive les événements d'entrée de l'accéléromètre à chaque image. La désactivation des entrées de l'accéléromètre peut améliorer les performances.

---

### Resource {#resource}

#### Http Cache {#http-cache}
Si cette option est cochée, un cache HTTP est activé pour accélérer le chargement des ressources par le réseau vers le moteur en cours d'exécution sur l'appareil.

#### Uri {#uri}
L'emplacement des données du build du projet, au format URI.

#### Max Resources {#max-resources}
Le nombre maximal de ressources pouvant être chargées simultanément.

---

### Network {#network}

#### Http Timeout {#http-timeout}
Le délai d'expiration HTTP, en secondes. Définissez-le sur `0` pour désactiver l'expiration.

#### Http Thread Count {#http-thread-count}
Le nombre de threads de travail du service HTTP.

#### Http Cache Enabled {#http-cache-enabled}
Cochez cette option pour activer le cache HTTP pour les requêtes réseau (avec `http.request()`). Le cache HTTP stocke la réponse associée à une requête et réutilise cette réponse pour les requêtes suivantes. Le cache HTTP prend en charge les en-têtes de réponse HTTP `ETag` et `Cache-Control: max-age`.

#### SSL Certificates {#ssl-certificates}
Le fichier contenant les certificats racines SSL à utiliser pour vérifier la chaîne de certificats lors des négociations SSL.

---

### Collection {#collection}

#### Max Instances {#max-instances}
Le nombre maximal d'instances d'objets de jeu dans une collection, `1024` par défaut. [(Voir les informations sur les optimisations du nombre maximal de composants)](#component-max-count-optimizations).

#### Max Input Stack Entries {#max-input-stack-entries}
Le nombre maximal d'objets de jeu dans la pile d'entrée.

---

### Sound {#sound}

#### Gain {#gain}
Le gain global (volume), `0`--`1`.

#### Use Linear Gain {#use-linear-gain}
Si cette option est activée, le gain est linéaire. Si elle est désactivée, une courbe exponentielle est utilisée.

#### Max Sound Data {#max-sound-data}
Le nombre maximal de ressources sonores, c'est-à-dire le nombre de fichiers audio distincts à l'exécution.

#### Max Sound Buffers {#max-sound-buffers}
(Actuellement inutilisé) Le nombre maximal de tampons audio simultanés.

#### Max Sound Sources {#max-sound-sources}
(Actuellement inutilisé) Le nombre maximal de sons lus simultanément.

#### Max Sound Instances {#max-sound-instances}
Le nombre maximal d'instances sonores simultanées, c'est-à-dire les sons effectivement lus en même temps.

#### Max Component Count {#max-component-count}
Le nombre maximal de composants sonores par collection.

#### Sample Frame Count {#sample-frame-count}
Le nombre d'échantillons utilisés pour chaque mise à jour audio. 0 signifie automatique (1024 pour 48 kHz, 768 pour 44.1 kHz).

#### Use Thread {#use-thread}
Si cette option est cochée, le système audio utilise des threads pour la lecture audio afin de réduire le risque de saccades lorsque le thread principal est fortement sollicité.

#### Stream Enabled {#stream-enabled}
Si cette option est cochée, le système audio charge les fichiers sources en continu.

#### Stream Cache Size {#stream-cache-size}
La taille maximale du cache de blocs audio contenant _tous_ les blocs. `2097152` octets par défaut.
Ce nombre devrait être supérieur au nombre de fichiers audio chargés multiplié par la taille d'un bloc du flux.
Sinon, vous risquez d'évincer de nouveaux blocs du cache à chaque image.

#### Stream Chunk Size {#stream-chunk-size}
La taille en octets de chaque bloc lu en continu.

#### Stream Preload Size {#stream-preload-size}
Détermine la taille en octets du bloc initial des fichiers audio lus depuis l'archive.

---

### Sprite {#sprite}

#### Max Count {#max-count}
Le nombre maximal de sprites par collection. [(Voir les informations sur les optimisations du nombre maximal de composants)](#component-max-count-optimizations).

#### Subpixels {#subpixels}
Cochez cette option pour autoriser les sprites à s'afficher sans être alignés sur les pixels.

---

### Tilemap {#tilemap}

#### Max Count {#max-count}
Le nombre maximal de tilemaps par collection. [(Voir les informations sur les optimisations du nombre maximal de composants)](#component-max-count-optimizations).

#### Max Tile Count {#max-tile-count}
Le nombre maximal de tuiles visibles simultanément par collection.

---

### Spine {#spine}

#### Max Count {#max-count}
Le nombre maximal de composants de modèle Spine. [(Voir les informations sur les optimisations du nombre maximal de composants)](#component-max-count-optimizations).

---

### Mesh {#mesh}

#### Max Count {#max-count}
Le nombre maximal de composants de maillage par collection. [(Voir les informations sur les optimisations du nombre maximal de composants)](#component-max-count-optimizations).

---

### Model {#model}

#### Max Count {#max-count}
Le nombre maximal de composants de modèle par collection. [(Voir les informations sur les optimisations du nombre maximal de composants)](#component-max-count-optimizations).

#### Split Meshes {#split-meshes}
Divise les maillages de plus de 65536 sommets en nouveaux maillages.

#### Max Bone Matrix Texture Width {#max-bone-matrix-texture-width}
La largeur maximale de la texture des matrices des os. Seule la taille nécessaire aux animations est utilisée, arrondie à la puissance de deux supérieure ou égale la plus proche.

#### Max Bone Matrix Texture Height {#max-bone-matrix-texture-height}
La hauteur maximale de la texture des matrices des os. Seule la taille nécessaire aux animations est utilisée, arrondie à la puissance de deux supérieure ou égale la plus proche.

---

### GUI {#gui}

#### Max Count {#max-count}
Le nombre maximal de composants d'interface graphique. [(Voir les informations sur les optimisations du nombre maximal de composants)](#component-max-count-optimizations).

#### Max Particle Count {#max-particle-count}
Le nombre maximal de particules simultanées dans l'interface graphique.

#### Max Animation Count {#max-animation-count}
Le nombre maximal d'animations actives dans l'interface graphique.

---

### Label {#label}

#### Max Count {#max-count}
Le nombre maximal de composants label. [(Voir les informations sur les optimisations du nombre maximal de composants)](#component-max-count-optimizations).

#### Subpixels {#subpixels}
Cochez cette option pour autoriser les composants label à s'afficher sans être alignés sur les pixels.

---

### Particle FX {#particle-fx}

#### Max Count {#max-count}
Le nombre maximal d'émetteurs simultanés. [(Voir les informations sur les optimisations du nombre maximal de composants)](#component-max-count-optimizations).

#### Max Particle Count {#max-particle-count}
Le nombre maximal de particules simultanées.

---

### Box2D {#box2d}

#### Velocity Iterations {#velocity-iterations}
Le nombre d'itérations de vitesse du solveur physique Box2D 2.2.

#### Position Iterations {#position-iterations}
Le nombre d'itérations de position du solveur physique Box2D 2.2.

#### Sub Step Count {#sub-step-count}
Le nombre de sous-étapes du solveur physique Box2D 3.x.

---

### Collection proxy {#collection-proxy}

#### Max Count {#max-count}
Le nombre maximal de proxys de collection. [(Voir les informations sur les optimisations du nombre maximal de composants)](#component-max-count-optimizations).

---

### Collection factory {#collection-factory}

#### Max Count {#max-count}
Le nombre maximal de composants collection factory. [(Voir les informations sur les optimisations du nombre maximal de composants)](#component-max-count-optimizations).

---

### Factory {#factory}

#### Max Count {#max-count}
Le nombre maximal de composants factory d'objets de jeu. [(Voir les informations sur les optimisations du nombre maximal de composants)](#component-max-count-optimizations).

---

### iOS {#ios}

#### App Icon 57x57--180x180 {#app-icon-57x57-180x180}
Fichier image (.png) à utiliser comme icône d'application aux dimensions de largeur et de hauteur données `W` &times; `H`.

#### Launch Screen {#launch-screen}
Fichier de storyboard (.storyboard). Pour savoir comment en créer un, consultez le [manuel iOS](/manuals/ios/#creating-a-storyboard).

#### Icons Asset {#icons-asset}
Le fichier de ressources d'icônes (.car) contenant les icônes de l'application.

#### Prerendered Icons {#prerendered-icons}
(iOS 6 et versions antérieures) Cochez cette option si vos icônes sont prérendues. Si elle est décochée, un effet brillant sera automatiquement ajouté aux icônes.

#### Bundle Identifier {#bundle-identifier}
L'identifiant du bundle permet à iOS de reconnaître les mises à jour de votre application. Il doit être enregistré auprès d'Apple et être propre à votre application. Vous ne pouvez pas utiliser le même identifiant pour les applications iOS et macOS. Il doit comporter au moins deux segments séparés par un point. Chaque segment doit commencer par une lettre et ne contenir que des caractères alphanumériques, le trait de soulignement ou le trait d'union (-) (voir [`CFBundleIdentifier`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430))

#### Bundle Name {#bundle-name}
Le nom court du bundle (15 caractères) (voir [`CFBundleName`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)).

#### Bundle Version {#bundle-version}
La version du bundle, sous la forme d'un nombre ou de x.y.z. (voir [`CFBundleVersion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430))

#### Info.plist {#infoplist}
S'il est indiqué, ce fichier *`Info.plist`* est utilisé à la place du manifeste de base iOS intégré lors de la création du bundle de votre application. Le manifeste intégré contient les entrées de réseau local et Bonjour nécessaires à la découverte des cibles par l'éditeur dans les builds autres que ceux de publication. Si vous fournissez un manifeste personnalisé et avez besoin de la découverte des cibles, du profilage, du rechargement à chaud ou de la diffusion des journaux sur un appareil, conservez ces entrées comme indiqué dans le [manuel iOS](/manuals/ios/#creating-an-ios-application-bundle).

#### Privacy Manifest {#privacy-manifest}
Le manifeste de confidentialité Apple de l'application. La valeur par défaut du champ est `/builtins/manifests/ios/PrivacyInfo.xcprivacy`.

#### Custom Entitlements {#custom-entitlements}
Si un profil d'approvisionnement est indiqué, les droits qu'il contient (`.entitlements`, `.xcent`, `.plist`) seront fusionnés avec ceux du profil d'approvisionnement fourni lors de la création du bundle de l'application.

#### Default Language {#default-language}
La langue utilisée si la langue préférée de l'utilisateur ne figure pas dans la liste `Localizations` de l'application (voir [`CFBundleDevelopmentRegion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)). Utilisez le code à deux lettres de la norme ISO 639-1 si la langue préférée y figure, ou le code à trois lettres de la norme ISO 639-2.

#### Localizations {#localizations}
Ce champ contient des chaînes séparées par des virgules qui indiquent le nom de la langue ou le code de langue ISO des localisations prises en charge (voir [`CFBundleLocalizations`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552)).

---

### Android {#android}

#### App Icon 36x36--192x192 {#app-icon-36x36-192x192}
Fichier image (.png) à utiliser comme icône d'application aux dimensions de largeur et de hauteur données `W` &times; `H`.

#### Push Icon Small--LargeXxxhdpi {#push-icon-small-largexxxhdpi}
Fichiers image (.png) à utiliser comme icônes personnalisées de notification push sur Android. Les icônes seront automatiquement utilisées pour les notifications push locales comme distantes. Si aucun fichier n'est défini, l'icône de l'application sera utilisée par défaut.

#### Push Field Title {#push-field-title}
Définit le champ JSON de la charge utile à utiliser comme titre de notification. Si ce paramètre reste vide, les notifications push utilisent par défaut le nom de l'application comme titre.

#### Push Field Text {#push-field-text}
Définit le champ JSON de la charge utile à utiliser comme texte de notification. Si ce paramètre reste vide, le texte du champ `alert` est utilisé, comme sur iOS.

#### Version Code {#version-code}
Une valeur entière indiquant la version de l'application. Augmentez cette valeur à chaque mise à jour ultérieure.

#### Minimum SDK Version {#minimum-sdk-version}
Le niveau d'API minimal requis pour que l'application s'exécute (`android:minSdkVersion`).

#### Target SDK Version {#target-sdk-version}
Le niveau d'API ciblé par l'application (`android:targetSdkVersion`).

#### Package {#package}
L'identifiant du paquet. Il doit comporter au moins deux segments séparés par un point. Chaque segment doit commencer par une lettre et ne contenir que des caractères alphanumériques ou le trait de soulignement.

#### GCM Sender Id {#gcm-sender-id}
L'identifiant d'expéditeur Google Cloud Messaging. Définissez-le sur la chaîne attribuée par Google pour activer les notifications push.

#### FCM Application Id {#fcm-application-id}
L'identifiant d'application Firebase Cloud Messaging.

#### Manifest {#manifest}
Si ce paramètre est défini, le fichier XML de manifeste Android indiqué est utilisé lors de la création du bundle. Un manifeste personnalisé remplace le manifeste de base intégré de Defold. Les fragments de manifeste des extensions natives y sont toujours fusionnés, mais les modifications ultérieures du manifeste de base intégré ne sont pas reprises automatiquement : comparez donc vos manifestes personnalisés au manifeste intégré actuel lors des mises à niveau. Pour les jeux, définissez `android:appCategory="game"` sur l'élément `<application>`. Pour les applications qui ne sont pas des jeux, définissez `android:appCategory` uniquement si l'une des [catégories d'applications](https://developer.android.com/guide/topics/manifest/application-element#appCategory) définies par Android décrit précisément l'application.

#### Iap Provider {#iap-provider}
Définit la boutique à utiliser. Les options valides sont `Amazon` et `GooglePlay`. Consultez [extension-iap](/extension-iap/) pour en savoir plus.

#### Input Method {#input-method}
Définit la méthode à utiliser pour obtenir les entrées clavier sur les appareils Android. Les options valides sont `KeyEvent` (ancienne méthode) et `HiddenInputField` (nouvelle méthode).

#### Immersive Mode {#immersive-mode}
Si cette option est activée, les barres de navigation et d'état sont masquées et votre application peut capturer tous les événements tactiles de l'écran.

#### Display Cutout {#display-cutout}
Étend l'affichage à la zone de découpe de l'écran.

#### Debuggable {#debuggable}
Détermine si l'application peut être déboguée à l'aide d'outils comme [GAPID](https://github.com/google/gapid) ou [Android Studio](https://developer.android.com/studio/profile/android-profiler). Cela définit l'indicateur `android:debuggable` dans le manifeste Android ([documentation officielle](https://developer.android.com/guide/topics/manifest/application-element#debug)).

<a id="proguard-config"></a>

#### R8 Keep Rules {#r8-keep-rules}
`android.r8_keep_rules` sélectionne un fichier `.keep` pour activer la suppression du code inutilisé, l'optimisation et l'obfuscation du code Java avec R8 dans les builds Android. Laissez ce paramètre vide pour utiliser D8 sans suppression du code inutilisé.

Sélectionnez `/builtins/manifests/android/dmengine.keep` pour utiliser directement les règles par défaut de Defold. Les extensions fournissent leurs propres [règles de conservation](/manuals/extensions/#r8-keep-rules-for-android), qui sont combinées à ce fichier.

Copiez le fichier intégré dans votre projet uniquement si vous devez ajouter des règles propres au projet. Préservez les règles intégrées dans la copie : sélectionner un fichier personnalisé remplace l'ensemble des règles du projet.

Consultez le [manuel Android](/manuals/android/#shrinking-java-code-with-r8) pour activer R8 et conserver sa table de correspondance d'obfuscation avec un bundle de publication.

#### Extract Native Libraries {#extract-native-libraries}
Définit si le programme d'installation du paquet extrait les bibliothèques natives de l'APK vers le système de fichiers. Si la valeur est `false`, vos bibliothèques natives sont stockées sans compression dans l'APK. Bien que votre APK puisse être plus volumineux, votre application se charge plus vite, car les bibliothèques sont chargées directement depuis l'APK à l'exécution. Cela définit l'indicateur `android:extractNativeLibs` dans le manifeste Android ([documentation officielle](https://developer.android.com/guide/topics/manifest/application-element#extractNativeLibs)).

---

### macOS {#macos}

#### App Icon {#app-icon}
Fichier d'icône de bundle (.icns) à utiliser comme icône d'application sur macOS.

#### Info.plist {#infoplist}
Si ce paramètre est défini, le fichier info.plist indiqué est utilisé lors de la création du bundle.

#### Privacy Manifest {#privacy-manifest}
Le manifeste de confidentialité Apple de l'application. La valeur par défaut du champ est `/builtins/manifests/osx/PrivacyInfo.xcprivacy`.

#### Bundle Identifier {#bundle-identifier}
L'identifiant du bundle permet à macOS de reconnaître les mises à jour de votre application. Il doit être enregistré auprès d'Apple et être propre à votre application. Vous ne pouvez pas utiliser le même identifiant pour les applications iOS et macOS. Il doit comporter au moins deux segments séparés par un point. Chaque segment doit commencer par une lettre et ne contenir que des caractères alphanumériques, le trait de soulignement ou le trait d'union (-).

#### Default Language {#default-language}
La langue utilisée si la langue préférée de l'utilisateur ne figure pas dans la liste `Localizations` de l'application (voir [`CFBundleDevelopmentRegion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)). Utilisez le code à deux lettres de la norme ISO 639-1 si la langue préférée y figure, ou le code à trois lettres de la norme ISO 639-2.

#### Localizations {#localizations}
Ce champ contient des chaînes séparées par des virgules qui indiquent le nom de la langue ou le code de langue ISO des localisations prises en charge (voir [`CFBundleLocalizations`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552)).

---

### Windows {#windows}

#### App Icon {#app-icon}
Fichier image (.ico) à utiliser comme icône d'application sur Windows. Pour savoir comment créer un fichier .ico, consultez le [manuel Windows](/manuals/windows).

---

### HTML5 {#html5}

Consultez le [manuel de la plateforme HTML5](/manuals/html5/) pour en savoir plus sur bon nombre de ces options.

#### Heap Size {#heap-size}
La taille du tas mémoire qu'Emscripten doit utiliser, en mégaoctets.

#### .html Shell {#html-shell}
Utilise le fichier de modèle HTML indiqué lors de la création du bundle. Par défaut, `/builtins/manifests/web/engine_template.html`.

#### Custom .css {#custom-css}
Utilise le fichier de thème CSS indiqué lors de la création du bundle. Par défaut, `/builtins/manifests/web/light_theme.css`.

#### Splash Image {#splash-image}
Si ce paramètre est défini, utilise l'image d'accueil indiquée au démarrage à la place du logo Defold lors de la création du bundle.

#### Archive Location Prefix {#archive-location-prefix}
Lors de la création d'un bundle HTML5, les données du jeu sont réparties dans un ou plusieurs fichiers d'archive. Lorsque le moteur démarre le jeu, ces fichiers d'archive sont chargés en mémoire. Utilisez ce paramètre pour définir l'emplacement des données.

#### Archive Location Suffix {#archive-location-suffix}
Le suffixe à ajouter aux fichiers d'archive. Utile, par exemple, pour forcer le chargement de contenu non mis en cache depuis un CDN (`?version2`, par exemple).

#### Engine Arguments {#engine-arguments}
La liste des arguments qui seront transmis au moteur.

#### Wasm Streaming {#wasm-streaming}
Active le chargement en continu du fichier wasm (plus rapide et moins gourmand en mémoire, mais nécessite le type MIME `application/wasm`).

#### Show Fullscreen Button {#show-fullscreen-button}
Active le bouton de plein écran dans le fichier `index.html`.

#### Show Made With Defold {#show-made-with-defold}
Active le lien Made With Defold dans le fichier `index.html`.

#### Show Console Banner {#show-console-banner}
Lorsqu'elle est activée, cette option affiche des informations sur le moteur et sa version dans la console du navigateur (avec `console.log()`) au démarrage du moteur.

#### Scale Mode {#scale-mode}
Définit la méthode à utiliser pour mettre le canevas du jeu à l'échelle.

#### Retry Count {#retry-count}
Le nombre de nouvelles tentatives après un échec de téléchargement au démarrage, y compris les erreurs réseau, les statuts HTTP d'échec et les écarts de taille du fichier JavaScript ou WebAssembly du moteur. La requête initiale est comptée séparément. La vérification des fichiers de l'archive possède sa propre limite de tentatives ; consultez [Vérification des téléchargements](/manuals/html5/#download-verification) et `Retry Time`.

#### Retry Time {#retry-time}
Le nombre de secondes à attendre entre les tentatives de téléchargement d'un fichier après un échec (voir `Retry Count`).

#### Verify Downloaded File Size {#verify-downloaded-file-size}
`html5.verify_downloaded_file_size` compare la taille des fichiers du moteur et de l'archive téléchargés à leur taille attendue. Activé par défaut (`true`). Définissez-le sur `false` uniquement si un serveur, proxy ou CDN réécrit volontairement les fichiers et modifie leur taille. Un échec de vérification déclenche de nouvelles tentatives de téléchargement avant l'échec du démarrage. Les limites de tentatives diffèrent entre les téléchargements du moteur et la vérification des fichiers de l'archive ; consultez [Vérification des téléchargements](/manuals/html5/#download-verification).

#### Transparent Graphics Context {#transparent-graphics-context}
Cochez cette option si vous souhaitez que le contexte graphique ait un arrière-plan transparent.

---

### IAP {#iap}

#### Auto Finish Transactions {#auto-finish-transactions}
Cochez cette option pour terminer automatiquement les transactions IAP. Si elle est décochée, vous devez appeler explicitement `iap.finish()` après une transaction réussie.

---

### Live update {#live-update}

#### Settings {#settings}
Le fichier de ressources des paramètres de mise à jour en direct à utiliser lors de la création du bundle.

---

### Native extension {#native-extension}

#### _App Manifest_ {#_app-manifest_}
Si ce paramètre est défini, utilise le manifeste d'application pour personnaliser le build du moteur. Cela vous permet de retirer les parties inutilisées du moteur afin de réduire la taille du binaire final. Découvrez comment exclure les fonctionnalités inutilisées [dans le manuel du manifeste d'application](/manuals/app-manifest).

---

### Profiler {#profiler}

Le paramètre **Profiler** de l'App Manifest détermine si le code de profilage est lié aux builds de débogage et de publication. Les paramètres ci-dessous déterminent le comportement à l'exécution du code de profilage présent dans le build sélectionné. Consultez le [manuel du profilage](/manuals/profiling/) pour en savoir plus.

#### Enabled {#enabled}
Active le profileur intégré au jeu.

#### Track Cpu {#track-cpu}
L'échantillonnage de l'utilisation du processeur est activé par défaut dans les builds de débogage. Activez ce paramètre lorsque l'échantillonnage du processeur est également nécessaire dans un build de publication qui inclut la prise en charge du profilage via l'App Manifest.

#### Sleep Between Server Updates {#sleep-between-server-updates}
Le nombre de millisecondes de pause entre les mises à jour du serveur.

#### Performance Timeline Enabled {#performance-timeline-enabled}
Active la chronologie des performances dans le navigateur (HTML5 uniquement).

#### Max Sample Count {#max-sample-count}
`profiler.max_sample_count` est le nombre maximal d'échantillons de profilage enregistrés par thread et par image. La valeur par défaut est `4096` et le minimum est `128`. N'augmentez cette valeur que si un profil valide dépasse la limite ; vérifiez d'abord que les appels de début et de fin de portée correspondent dans le code de profilage des extensions natives.

---

## Définir des valeurs de configuration au démarrage du moteur {#setting-config-values-on-engine-startup}

Au démarrage du moteur, vous pouvez fournir en ligne de commande des valeurs de configuration qui remplacent les paramètres de *game.project* :

```bash
# Specify a bootstrap collection
$ dmengine --config=bootstrap.main_collection=/my.collectionc

# Set two custom config values
$ dmengine --config=test.my_value=4711 --config=test2.my_value2=foobar
```

Les valeurs personnalisées peuvent---comme toute autre valeur de configuration---être lues avec la fonction correspondante décrite dans la section [Accès à l'exécution](#runtime-access) :

```lua
local my_value = sys.get_config_number("test.my_value")
local my_value2 = sys.get_config_string("test.my_value2")
local my_flag = sys.get_config_boolean("test.my_flag", false)
```


:[Component max count optimizations](../shared/component-max-count-optimizations.md)


## Paramètres de projet personnalisés {#custom-project-settings}

Vous pouvez définir des paramètres personnalisés pour le projet principal ou pour une [extension native](/manuals/extensions/). Les paramètres personnalisés du projet principal doivent être définis dans un fichier `game.properties` à la racine du projet. Les fichiers nommés `ext.properties` sont détectés partout dans le projet et dans les bibliothèques récupérées comme dépendances ; ils ne nécessitent pas de fichier `ext.manifest` voisin. Toutes les métadonnées d'extension détectées sont fusionnées, puis le fichier `game.properties` à la racine est appliqué et peut les remplacer.

Le fichier de paramètres utilise le même format INI que *game.project*, et les attributs des propriétés sont définis avec une notation pointée et un suffixe :

```
[my_category]
my_property.private = 1
...
```

Le fichier de métadonnées par défaut, qui est toujours appliqué, est disponible [ici](https://github.com/defold/defold/blob/dev/com.dynamo.cr/com.dynamo.cr.bob/src/com/dynamo/bob/meta.properties)

Les attributs suivants sont actuellement disponibles :

```
[my_extension]
// `type` - used for the value string parsing
my_property.type = string // one of the following values: bool, string, number, integer, string_array, resource

// `help` - displayed as a help tooltip in the editor
my_property.help = string

// `default` - value used as default if user didn't set value manually
my_property.default = string

// `private` - private value used during the bundle process but will be removed from the bundle itself
my_property.private = 1 // boolean value 1 or 0

// `label` - editor input label
my_property.label = My Awesome Property

// `minimum` and/or `maximum` - valid range for numeric properties, validated in the editor UI
my_property.minimum = 0
my_property.maximum = 255

// `options` - drop-down choices for the editor UI, comma-separated value[:label] pairs
my_property.options = android: Android, ios: iOS

// `resource` type only:
my_property.filter = jpg,png // allowed file extensions for resource selector dialog
my_property.preserve-extension = 1 // use original resource extension instead of a built one

// deprecation
my_property.deprecated = 1 // mark property as deprecated
my_property.severity-default = warning // if deprecated property is specified, but set to a default value
my_property.severity-override = error  // if deprecated property is specified and set to a non-default value

```
Vous pouvez également définir les attributs suivants pour une catégorie de paramètres :
```
[my_extension]
// `group` - game.project category group, e.g. Main, Platforms, Components, Runtime, Distribution
group = Runtime
// `title` - displayed category title
title = My Awesome Extension
// `help` - displayed category help
help = Settings for My Awesome Extension
```


Bob et l'éditeur analysent tous deux ces fichiers de métadonnées. L'éditeur les utilise pour créer les champs, les choix, les validations et les infobulles d'aide correspondants dans la vue de *game.project*.
