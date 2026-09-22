---
title: Recommandations pour le portage et la publication
brief: Ce manuel présente plusieurs points à prendre en compte lorsque vous portez un jeu sur une nouvelle plateforme ou que vous publiez votre jeu pour la première fois.
---

# Recommandations pour le portage et la publication {#porting-and-release-guidelines}

Cette page propose un guide pratique et une liste de points à vérifier lors de la publication d'un jeu ou de son portage sur une nouvelle plateforme.

Le portage d'un jeu Defold sur une nouvelle plateforme ou sa première publication est généralement un processus simple. En théorie, il suffit de s'assurer que les sections pertinentes sont configurées dans le fichier *game.project*, mais pour tirer le meilleur parti de chaque plateforme, il est recommandé d'adapter le jeu à ses spécificités.


## Entrées {#input}
Veillez à adapter le jeu aux méthodes d'entrée de la plateforme. Envisagez d'ajouter la prise en charge des [manettes](/manuals/input-gamepads) si la plateforme le permet ! Et assurez-vous que le jeu dispose d'un menu de pause : si une manette se déconnecte soudainement, le jeu devrait être mis en pause !

## Localisation {#localization}
Traduisez tous les textes du jeu. Pour une publication en Europe et dans les Amériques, envisagez de traduire au moins dans les langues EFIGS (anglais, français, italien, allemand et espagnol). Assurez-vous qu'il est facile de passer d'une langue à l'autre dans le jeu (via le menu de pause).

::: important
iOS uniquement : veillez à renseigner [Localizations](/manuals/project-settings/#localizations) dans `game.project`, car `sys.get_info()` ne renverra jamais une langue qui ne figure pas dans cette liste.
:::

Traduisez le texte de la page de la boutique, car cela aura un effet positif sur les ventes ! Certaines plateformes exigent que le texte de la page de la boutique soit traduit dans la langue de chaque pays où le jeu est disponible.

## Éléments pour la boutique {#store-materials}

### Icône de l'application {#app-icon}
Assurez-vous que votre jeu se démarque de la concurrence. L'icône est souvent votre premier point de contact avec les joueurs potentiels. Elle doit être facile à repérer sur une page remplie d'icônes de jeux.

### Bannières et images de la boutique {#store-banners-and-images}
Veillez à utiliser des visuels percutants et attrayants pour votre jeu. Il vaut probablement la peine de dépenser un peu d'argent pour travailler avec un artiste afin de créer des visuels qui attirent les joueurs.


## Sauvegardes de parties {#save-games}

### Sauvegardes de parties sur ordinateur, sur mobile et sur le Web {#save-games-on-desktop-mobile-and-web}
Les sauvegardes de parties et les autres états sauvegardés peuvent être enregistrés à l'aide de la fonction `sys.save(filename, data)` de l'API Defold et chargés avec `sys.load(filename)`. Vous pouvez utiliser `sys.get_save_file(application_id, name)` pour obtenir le chemin d'un emplacement propre au système d'exploitation où les fichiers peuvent être enregistrés, généralement dans le dossier personnel de l'utilisateur connecté.

### Sauvegardes de parties sur console {#save-games-on-console}
L'utilisation de `sys.get_save_file()` et de `sys.save()` fonctionne bien sur la plupart des plateformes, mais une approche différente est recommandée sur console. Les plateformes de console associent généralement un utilisateur à chaque manette connectée ; les sauvegardes de parties, les succès et les autres fonctionnalités devraient donc être associés à leur utilisateur respectif.

Les événements d'entrée des manettes contiendront un identifiant d'utilisateur qui peut servir à associer les actions d'une manette à un utilisateur sur la console.

Les plateformes de console et leurs extensions natives exposeront des fonctions d'API propres à la plateforme pour enregistrer et charger les données associées à un utilisateur donné. Utilisez ces API pour l'enregistrement et le chargement sur console.

Les API des plateformes de console pour les opérations sur les fichiers sont généralement asynchrones. Lorsque vous développez un jeu multiplateforme destiné aux consoles, il est recommandé de concevoir votre jeu de sorte que toutes les opérations sur les fichiers soient asynchrones, quelle que soit la plateforme. Exemple :

```lua
local function save_game(data, user_id, cb)
	if console then
		local filename = "savegame"
		consoleapi.save(user_id, filename, data, cb)
	else
		local filename = sys.get_save_file("mygame", "savegame" .. user_id)
		local success = sys.save(filename, data)
		cb(success)
	end
end
```


## Artefacts de build {#build-artifacts}

Veillez à [générer les symboles de débogage](/manuals/debugging-native-code/#symbolicate-a-callstack) pour chaque version publiée afin de pouvoir déboguer les plantages. Conservez-les avec le bundle de l'application.

## Optimisations de l'application {#application-optimizations}

Consultez le [manuel d'optimisation](/manuals/optimization) pour savoir comment optimiser les performances, la taille, l'utilisation de la mémoire et la consommation de batterie de votre application.



## Performances {#performance}
Testez toujours sur le matériel cible ! Vérifiez les performances du jeu et optimisez-le si nécessaire. Utilisez le [profileur](/manuals/profiling) pour trouver les goulots d'étranglement dans le code.


## Résolution de l'écran et fréquence de rafraîchissement {#screen-resolution-and-refresh-rate}
Pour les plateformes dont l'orientation et la résolution d'écran sont fixes : vérifiez que le jeu fonctionne avec la résolution et le rapport largeur/hauteur de l'écran de la plateforme cible. Pour les plateformes dont la résolution et le rapport largeur/hauteur de l'écran sont variables : vérifiez que le jeu fonctionne avec différentes résolutions et différents rapports largeur/hauteur. Prenez en compte le type de [projection de vue](/manuals/render/#default-view-projection) utilisé dans le script de rendu et la caméra.

Pour les plateformes mobiles, verrouillez l'orientation de l'écran dans *game.project* ou assurez-vous que le jeu fonctionne aussi bien en mode paysage qu'en mode portrait.

* **Tailles d'affichage** - Tout s'affiche-t-il correctement sur un écran plus grand ou plus petit que la largeur et la hauteur par défaut définies dans *game.project* ?
  * La projection utilisée dans le script de rendu et les agencements utilisés dans l'interface graphique joueront un rôle ici.
* **Rapports largeur/hauteur** - Tout s'affiche-t-il correctement sur un écran dont le rapport largeur/hauteur diffère de celui obtenu à partir de la largeur et de la hauteur par défaut définies dans *game.project* ?
  * La projection utilisée dans le script de rendu et les agencements utilisés dans l'interface graphique joueront un rôle ici.
* **Fréquence de rafraîchissement** - Le jeu fonctionne-t-il bien sur un écran dont la fréquence de rafraîchissement est supérieure à 60 Hz ?
  * La synchronisation verticale et l'intervalle d'échange dans la section Display de *game.project* 


## Téléphones mobiles et caméras à encoche ou à poinçon {#mobile-phones-and-notch-and-hole-punch-cameras}
L'utilisation d'une petite découpe dans l'écran pour accueillir la caméra frontale et les capteurs (également appelée encoche ou poinçon) est de plus en plus courante. Lorsque vous portez un jeu sur mobile, veillez à ce que les informations essentielles restent dans la zone sûre de la plateforme.

Defold intègre la prise en charge de la zone sûre sur Android et iOS. Définissez `gui.safe_area_mode` dans *game.project* pour contrôler quelles marges de la zone sûre, sur des bords opposés, influencent l'ajustement de l'interface graphique. `none` est la valeur par défaut et ignore ces marges ; `long` applique les marges gauche/droite en mode paysage et haut/bas en mode portrait ; `short` applique la paire opposée ; et `both` applique les marges des quatre bords. Un script d'interface graphique peut remplacer, pour sa scène, le mode défini à l'échelle du projet à l'aide de [`gui.set_safe_area_mode()`](/ref/gui/#gui.set_safe_area_mode). Pour une logique d'interface graphique ou de rendu personnalisée, [`window.get_safe_area()`](/ref/window/#window.get_safe_area) renvoie le rectangle de la zone sûre et les marges de chaque bord. Les plateformes sans marges de zone sûre intégrées renvoient la fenêtre entière et des marges nulles.

L'[extension Safe Area](/extension-safearea) reste une solution possible pour les anciens projets ou les flux de travail qui nécessitent un comportement allant au-delà des API intégrées ; elle n'est pas nécessaire pour la gestion standard de la zone sûre sur Android et iOS.


## Recommandations propres aux plateformes {#platform-specific-guidelines}

### Android {#android}
Veillez à conserver votre [magasin de clés](/manuals/android/#creating-a-keystore) dans un endroit sûr afin de pouvoir mettre à jour votre jeu.


### Consoles {#consoles}
Conservez le bundle complet de chaque version. Vous aurez besoin de ces fichiers si vous souhaitez appliquer un correctif au jeu.


### Nintendo Switch {#nintendo-switch}
Intégrez le code propre à la plateforme : pour Nintendo Switch, une extension distincte fournit des fonctions utilitaires pour la sélection de l'utilisateur, etc.

Defold pour Nintendo Switch utilise Vulkan comme moteur de rendu graphique : veillez à tester le jeu avec le [moteur de rendu graphique Vulkan](https://github.com/defold/extension-vulkan).


### PlayStation®4 {#playstation4}
Intégrez le code propre à la plateforme : pour PlayStation®4, une extension distincte fournit des fonctions utilitaires pour la sélection de l'utilisateur, etc.


### HTML5 {#html5}
Les jeux Web sur téléphone mobile gagnent en popularité : essayez de faire en sorte que le jeu fonctionne bien aussi dans un navigateur mobile ! Gardez également à l'esprit que les jeux Web sont censés se charger rapidement ! Veillez à optimiser la taille du jeu. Pensez aussi à l'expérience de chargement dans son ensemble pour ne pas perdre de joueurs inutilement.

En 2018, les navigateurs ont introduit une politique de lecture automatique des sons qui empêche les jeux et les autres contenus Web de jouer des sons tant qu'aucun événement d'interaction utilisateur (toucher, bouton, manette, etc.) n'a eu lieu. Il est important d'en tenir compte lors du portage en HTML5 et de ne commencer à jouer les sons et la musique qu'à la première interaction de l'utilisateur. Les tentatives de lecture de sons avant toute interaction utilisateur seront consignées comme des erreurs dans la console de développement du navigateur, mais n'auront aucun effet sur le jeu.

Veillez également à mettre en pause tous les sons en cours de lecture si le jeu affiche des publicités.
