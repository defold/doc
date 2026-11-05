---
title: Importation de modèles
brief: Ce manuel explique comment importer les modèles 3D utilisés par le composant Model.
---

# Importation de modèles 3D {#importing-3d-models}
Defold prend en charge les modèles, les squelettes et les animations au format glTF 2.0 (GL Transmission Format). Utilisez des fichiers *.gltf* ou *.glb* pour les modèles 3D. Le glTF est un format moderne conçu pour transférer et charger des données 3D dans les moteurs de jeu et les applications en temps réel.

Vous pouvez utiliser des outils tels que Maya, 3ds Max, SketchUp et Blender pour créer des modèles 3D ou les convertir au format glTF.

Blender est un logiciel puissant et populaire de modélisation, d'animation et de rendu 3D. Il fonctionne sous Windows, macOS et Linux et est disponible gratuitement sur [https://www.blender.org](https://www.blender.org).

![Modèle dans Blender](images/model/blender_gltf.png)

## Importation dans Defold {#importing-to-defold}
Pour importer un modèle, faites glisser le fichier *.gltf* ou *.glb* dans le volet *Assets* de l'éditeur Defold.

Le glTF peut être stocké de deux façons courantes :

* Un fichier *.glb* est un fichier binaire unique. Il contient les données du modèle et peut également contenir les images des textures intégrées. C'est pratique lorsque vous souhaitez déplacer ou stocker un modèle dans un seul fichier.
* Un fichier *.gltf* est un fichier JSON au format texte. Il référence généralement un fichier *.bin* distinct pour les données du maillage et des images de textures séparées, telles que des fichiers *.png* ou *.jpg*. Avec cette variante, ajoutez tous les fichiers référencés au projet et conservez leurs chemins relatifs.

Les images intégrées sont utilisables directement depuis un fichier glTF ou GLB, sans les extraire en ressources distinctes. Les fichiers d'images et de tampons externes doivent toujours être importés avec le modèle, en conservant leurs chemins relatifs.

::: sidenote
Defold conserve les positions et les transformations du fichier glTF importé et ne recentre pas automatiquement le modèle lors de l'importation. L'aperçu de l'éditeur et le moteur à l'exécution utilisent les transformations importées de façon cohérente : les maillages déformés par un squelette ou rattachés à un os conservent leurs transformations locales relatives au squelette, tandis que les maillages rigides conservent leur placement dans l'espace monde obtenu par aplatissement.

Un [composant Model](/manuals/model/#model-properties) peut sélectionner un seul maillage nommé dans la scène importée. Laisser le champ *Mesh* vide utilise toute la scène et préserve les transformations décrites ci-dessus. Sélectionner un maillage utilise sa géométrie locale sans les transformations des nœuds glTF ; placez-le donc à l'aide de la transformation du composant Model ou de l'objet de jeu.

Si un modèle créé avec une ancienne version de Defold change de position ou d'orientation après avoir été réimporté, corrigez la transformation dans Blender ou un autre outil de création et exportez à nouveau le fichier *.gltf* ou *.glb*.
:::

### Géométrie compressée {#compressed-geometry}

Les sources *.gltf* et *.glb* peuvent contenir de la géométrie compressée avec Draco ou Meshopt. Les extensions de compression glTF prises en charge sont :

| Compression | Extension glTF |
| --- | --- |
| Draco | `KHR_draco_mesh_compression` |
| Meshopt | `EXT_meshopt_compression` et `KHR_meshopt_compression` |

Exportez ou optimisez votre ressource glTF 2.0 avec l'une de ces extensions, puis importez-la comme un modèle non compressé. Incluez tous les tampons et textures externes en conservant leurs chemins relatifs. Affectez le fichier importé à la propriété *Scene* d'un composant Model comme d'habitude.

Defold décode la géométrie compressée lors de l'importation et du build. Le modèle résultant utilise la représentation géométrique habituelle de Defold à l'exécution. Cette prise en charge n'active pas la compression Draco ou Meshopt dans le moteur en cours d'exécution, et un fichier source plus petit ne garantit pas un bundle de jeu plus petit.

### Parcourir la scène importée {#browsing-the-imported-scene}

Développez un fichier *.gltf* ou *.glb* dans le panneau *Assets* pour parcourir ses maillages, matériaux générés et images intégrées. Ouvrir la scène affiche un aperçu avec ses matériaux et textures définis. Vous pouvez aussi ouvrir un maillage individuel pour en voir l'aperçu.

Les ressources exposées à l'intérieur du fichier sont en lecture seule. Pour créer une ressource Model modifiable à partir d'un maillage, copiez le maillage et collez-le dans un dossier du projet. Le fichier *.model* résultant référence toujours le fichier glTF ou GLB importé. Pour modifier la géométrie source ou les images intégrées, modifiez la ressource dans votre outil de création et exportez-la à nouveau.

Les scripts de l'éditeur peuvent énumérer ces ressources avec `editor.resource_children(path)`. Consultez [Parcourir les ressources du projet](/manuals/editor-scripts/#traversing-project-resources) pour un exemple qui visite récursivement les ressources des dossiers et fichiers glTF/GLB.

### Textures KTX2 {#ktx2-textures}

Les textures de modèles peuvent utiliser des sources *.ktx2*, sous forme de fichiers externes ou d'images intégrées à un fichier *.gltf* ou *.glb*. Importez les fichiers externes avec le modèle. Les images KTX2 intégrées apparaissent sous la scène dans le panneau *Assets* et peuvent être affectées directement aux champs de texture des matériaux ou via <kbd>Auto Fill</kbd>.

Les [profils de texture](/manuals/texture-profiles/#ktx2-source-textures) déterminent s'il faut conserver le format source KTX2 ou le convertir vers les formats de sortie configurés. **Keep KTX2 Format** conserve le format d'encodage source lorsque la compression de textures est activée, mais le traitement de l'image peut tout de même nécessiter un réencodage. Vérifiez la prise en charge du format sur les appareils ciblés et tenez compte d'une éventuelle perte de qualité supplémentaire lors de la recompression d'une texture déjà compressée. Consultez [Formats d'entrée et aperçus KTX2](/manuals/importing-graphics/#ktx2-textures).


## Utilisation d'un modèle {#using-a-model}
Une fois le modèle importé, utilisez-le dans un [composant Model](/manuals/model) :

1. Créez un fichier Model depuis le volet *Assets* avec <kbd>New... ▸ Model</kbd>, ou ajoutez un composant Model directement à un objet de jeu (game object) avec <kbd>Add Component ▸ Model</kbd>.
2. Définissez la propriété *Scene* sur le fichier *.gltf* ou *.glb* importé.
3. Lorsque la boîte de dialogue *Auto Fill Model Fields?* apparaît, choisissez <kbd>Auto Fill</kbd> pour affecter les matériaux générés et les textures référencées de la scène. Cela remplace les liaisons de matériaux et de textures existantes. Choisissez <kbd>Keep Current</kbd> pour conserver vos liaisons ; la nouvelle sélection de scène est tout de même appliquée.
4. Laissez *Mesh* vide pour utiliser toute la scène, ou sélectionnez un maillage nommé pour n'utiliser que sa géométrie locale. Modifier la sélection de maillage peut afficher la même boîte de dialogue : sélectionner un maillage propose ses matériaux, tandis que vider la sélection propose tous les matériaux de la scène. <kbd>Keep Current</kbd> conserve les liaisons tout en appliquant la nouvelle sélection de maillage.
5. Pour un modèle animé, définissez la propriété *Skeleton* sur le fichier *.gltf* ou *.glb* contenant le squelette. Il s'agit souvent du même fichier que celui utilisé pour *Scene* lorsque le maillage, le squelette et les animations sont exportés ensemble.
6. Créez un fichier *Animation Set* pour les animations et affectez-le à la propriété *Animations*. Définissez *Default Animation* si vous souhaitez qu'une animation démarre automatiquement.

L'éditeur propose de renseigner les liaisons lorsque la source glTF ou GLB sélectionnée expose des matériaux. Il résout aussi bien les images intégrées que les références d'images externes. Les matériaux générés utilisent les shaders glTF intégrés ; consultez le [manuel PBR](/manuals/physically-based-rendering/#built-in-pbr-materials) pour l'éclairage et les effets de matériaux pris en charge.

### Affecter manuellement les matériaux et les textures {#assigning-materials-and-textures-manually}

Si vous choisissez <kbd>Keep Current</kbd>, ou si vous avez besoin d'un ombrage personnalisé, définissez chaque propriété *Material* sur un matériau adapté. Les matériaux `gltf` intégrés fournissent un ombrage PBR ; les matériaux `model` intégrés et vos propres matériaux restent également disponibles. Consultez le [manuel des modèles](/manuals/model/#material) pour les variantes statiques, avec skinning et avec instanciation, ainsi que leurs exigences.

Affectez chaque texture au champ de texture du matériau correspondant. Vous pouvez utiliser une image intégrée exposée sous le fichier glTF ou GLB dans le panneau *Assets*, ou une image distincte du projet. Pour les matériaux comportant plusieurs samplers, associez chaque texture au sampler prévu ; le [manuel PBR répertorie les noms des samplers glTF intégrés](/manuals/physically-based-rendering/#built-in-pbr-materials).


## Exportation au format glTF {#exporting-to-gltf}
Le fichier *.gltf* ou *.glb* exporté contient tous les sommets, arêtes et faces qui constituent le modèle, ainsi que les _coordonnées UV_ (la partie de l'image de texture qui correspond à une partie donnée du maillage) si vous les avez définies, les os du squelette et les données d'animation.

* Vous trouverez une description détaillée des maillages polygonaux sur http://en.wikipedia.org/wiki/Polygon_mesh.

* Les coordonnées UV et le placage UV sont décrits sur http://en.wikipedia.org/wiki/UV_mapping.

Defold impose certaines limitations aux données d'animation exportées :

* Defold ne prend actuellement en charge que les animations précalculées. Les animations doivent contenir des matrices pour chaque os animé à chaque image clé, et non des clés distinctes pour la position, la rotation et l'échelle.

* Les animations sont également interpolées de façon linéaire. Si vous utilisez une interpolation par courbes plus avancée, les animations doivent être précalculées par l'exportateur.

### Exigences {#requirements}
Lorsque vous exportez un modèle, gardez à l'esprit que la prise en charge du glTF peut varier selon les outils et les moteurs. Utilisez glTF 2.0 et assurez-vous que le modèle possède des coordonnées UV correctes s'il utilise des textures. Les images peuvent être intégrées au fichier glTF ou GLB, ou stockées dans des fichiers distincts référencés par la scène. Incluez tous les fichiers d'images et de tampons externes lors de l'importation du modèle dans Defold.

Bien que notre ambition soit de prendre entièrement en charge le format glTF, nous n'y sommes pas encore tout à fait.
Si une fonctionnalité manque, veuillez soumettre une demande pour celle-ci dans [notre dépôt](https://github.com/defold/defold/issues)

### Exportation d'une texture {#exporting-a-texture}
Si vous souhaitez créer manuellement une image de texture, vous pouvez exporter le dépliage UV de Blender pour l'utiliser comme modèle. Commencez par sélectionner le maillage et tous ses sommets :

![Tout sélectionner](images/model/blender_select_all_vertices.png)

Une fois tous les sommets sélectionnés, dépliez le maillage pour obtenir le dépliage UV :

![Déplier le maillage](images/model/blender_unwrap_mesh.png)

Vous pouvez ensuite exporter le dépliage UV vers une image utilisable comme texture :

![Exporter le dépliage UV](images/model/blender_export_uv_layout.png)

![Résultat de l'exportation du dépliage UV](images/model/blender_export_uv_layout_result.png)

### Exportation avec Blender {#exporting-using-blender}
Exportez votre modèle depuis Blender avec <kbd>File ▸ Export ▸ glTF 2.0 (.glb/.gltf)</kbd>.

![Exportation avec Blender](images/model/export_gltf.png)

Sélectionnez le ou les objets avant l'exportation et activez *Selected Objects* si vous souhaitez exporter uniquement la sélection.

Choisissez l'une des options de *Format* :

* *glTF Binary (.glb)* crée un seul fichier. Utilisez cette option lorsque vous souhaitez pouvoir déplacer ou stocker facilement le modèle en tant que ressource unique.
* *glTF Separate (.gltf + .bin + textures)* crée des fichiers distincts pour la description du modèle, les données binaires et les textures. Utilisez cette option lorsque vous souhaitez modifier les images des textures ou les affecter séparément dans Defold.

Si le modèle contient des animations, activez l'exportation des animations et assurez-vous qu'elles sont précalculées. Si le modèle utilise des textures, assurez-vous que le maillage possède un dépliage UV et que les images des textures sont exportées dans un format que Defold peut importer, tel que PNG ou JPEG.

![Exportation avec Blender](images/model/export_settings.png)
