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

Si le modèle doit utiliser une texture dans Defold, importez l'image de la texture en tant que ressource distincte. Même lorsque le fichier glTF/GLB source contient des images intégrées, les textures doivent être affectées au composant (component) Model au moyen des propriétés de texture du matériau du composant.

![Ressources du modèle importées](images/model/assets_gltf.png)

::: sidenote
À partir de Defold 1.13.0, Defold conserve les positions et les transformations du fichier glTF importé et ne recentre plus automatiquement le modèle lors de l'importation. L'aperçu de l'éditeur et le moteur à l'exécution utilisent les transformations importées de façon cohérente : les maillages déformés par un squelette ou rattachés à un os conservent leurs transformations locales relatives au squelette, tandis que les maillages rigides conservent leur placement dans l'espace monde obtenu par aplatissement.

Depuis Defold 1.13.2, un [composant Model](/manuals/model/#model-properties) peut sélectionner un seul maillage nommé dans la scène importée. Laisser le champ *Mesh* vide utilise toute la scène et préserve les transformations décrites ci-dessus. Sélectionner un maillage utilise sa géométrie locale sans les transformations des nœuds glTF ; placez-le donc à l'aide de la transformation du composant Model ou de l'objet de jeu.

Si un modèle créé avec une ancienne version de Defold change de position ou d'orientation après avoir été réimporté, corrigez la transformation dans Blender ou un autre outil de création et exportez à nouveau le fichier *.gltf* ou *.glb*.
:::

## Utilisation d'un modèle {#using-a-model}
Une fois le modèle importé, utilisez-le dans un [composant Model](/manuals/model) :

1. Créez un fichier Model depuis le volet *Assets* avec <kbd>New... ▸ Model</kbd>, ou ajoutez un composant Model directement à un objet de jeu (game object) avec <kbd>Add Component ▸ Model</kbd>.
2. Définissez la propriété *Scene* sur le fichier *.gltf* ou *.glb* importé. Laissez *Mesh* vide pour utiliser toute la scène, ou sélectionnez un maillage nommé pour utiliser uniquement sa géométrie locale.
3. Pour un modèle animé, définissez la propriété *Skeleton* sur le fichier *.gltf* ou *.glb* contenant le squelette. Il s'agit souvent du même fichier que celui utilisé pour *Scene* lorsque le maillage, le squelette et les animations sont exportés ensemble.
4. Créez un fichier *Animation Set* pour les animations et affectez-le à la propriété *Animations*. Définissez *Default Animation* si vous souhaitez qu'une animation démarre automatiquement.
5. Définissez la propriété *Material* sur un matériau adapté au modèle. Les fichiers intégrés *model.material*, *model_instanced.material*, *model_skinned.material* et *model_skinned_instanced.material* constituent des points de départ utiles. Les matériaux de déformation par squelette utilisent l'espace local des sommets pour que la déformation puisse s'exécuter sur le GPU ; les matériaux personnalisés pour les modèles déformés par squelette sur le GPU ou rendus par instanciation doivent également utiliser l'espace local des sommets. Consultez le [manuel des modèles](/manuals/model/#material) pour connaître les exigences concernant l'adaptateur graphique.
6. Définissez les propriétés de texture du matériau, telles que *Texture*, sur les fichiers d'image des textures importés. Si le matériau utilise plusieurs textures, affectez chaque texture au champ de texture du matériau correspondant.


## Exportation au format glTF {#exporting-to-gltf}
Le fichier *.gltf* ou *.glb* exporté contient tous les sommets, arêtes et faces qui constituent le modèle, ainsi que les _coordonnées UV_ (la partie de l'image de texture qui correspond à une partie donnée du maillage) si vous les avez définies, les os du squelette et les données d'animation.

* Vous trouverez une description détaillée des maillages polygonaux sur http://en.wikipedia.org/wiki/Polygon_mesh.

* Les coordonnées UV et le placage UV sont décrits sur http://en.wikipedia.org/wiki/UV_mapping.

Defold impose certaines limitations aux données d'animation exportées :

* Defold ne prend actuellement en charge que les animations précalculées. Les animations doivent contenir des matrices pour chaque os animé à chaque image clé, et non des clés distinctes pour la position, la rotation et l'échelle.

* Les animations sont également interpolées de façon linéaire. Si vous utilisez une interpolation par courbes plus avancée, les animations doivent être précalculées par l'exportateur.

### Exigences {#requirements}
Lorsque vous exportez un modèle, gardez à l'esprit que la prise en charge du glTF peut varier selon les outils et les moteurs. Utilisez glTF 2.0, assurez-vous que le modèle possède des coordonnées UV correctes s'il utilise des textures et importez les images des textures séparément lorsqu'elles doivent être affectées à un composant Model.

Bien que notre ambition soit de prendre entièrement en charge le format glTF, nous n'y sommes pas encore tout à fait.
Si une fonctionnalité manque, veuillez soumettre une demande pour celle-ci dans [notre dépôt](https://github.com/defold/defold/issues)

### Exportation d'une texture {#exporting-a-texture}
Si vous n'avez pas encore de texture pour votre modèle, vous pouvez utiliser Blender pour en générer une. Vous devriez le faire avant de supprimer les matériaux supplémentaires du modèle. Commencez par sélectionner le maillage et tous ses sommets :

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
