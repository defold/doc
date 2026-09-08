---
title: Création d'un bundle d'application
brief: Ce manuel explique comment créer un bundle d'application.
---

# Création d'un bundle d'application {#bundling-an-application}

Pendant le développement de votre application, vous devriez prendre l'habitude de tester le jeu sur les plateformes cibles aussi souvent que possible. Cela vous permet de détecter les problèmes de performances dès le début du développement, lorsqu'ils sont beaucoup plus faciles à corriger. Il est également recommandé de tester le jeu sur toutes les plateformes cibles pour repérer les différences de comportement, par exemple au niveau des shaders. Lors du développement pour mobile, vous pouvez utiliser l'[application de développement mobile](/manuals/dev-app/) pour transférer du contenu vers l'application, au lieu de devoir effectuer un cycle complet de création de bundle, de désinstallation et d'installation.

Vous pouvez créer un bundle d'application pour toutes les plateformes prises en charge par Defold directement dans l'éditeur Defold, sans avoir besoin d'outils externes. Vous pouvez également créer des bundles en ligne de commande à l'aide de nos outils en ligne de commande. La création de bundles d'application nécessite une connexion réseau si votre projet contient une ou plusieurs [extensions natives](/manuals/extensions).

## Création de bundles dans l'éditeur {#bundling-from-within-the-editor}

Pour créer un bundle d'application, utilisez l'option Bundle du menu Project :

![](images/bundling/bundle_menu.png)

Sélectionnez l'une des options du menu pour ouvrir la boîte de dialogue Bundle correspondant à la plateforme choisie.

### Rapports de build {#build-reports}

Lors de la création d'un bundle de votre jeu, une option vous permet de créer un rapport de build. Celui-ci est très utile pour connaître la taille de toutes les ressources qui composent le bundle de votre jeu. Il vous suffit de cocher la case *Generate build report* lors de la création du bundle du jeu.

![rapport de build](images/profiling/build_report.png)

Pour en savoir plus sur les rapports de build, consultez le [manuel de profilage](/manuals/profiling/#build-reports).

### Android {#android}

La création d'un bundle d'application Android (fichier .apk) est décrite dans le [manuel Android](/manuals/android/#creating-an-android-application-bundle).

### iOS {#ios}

La création d'un bundle d'application iOS (fichier .ipa) est décrite dans le [manuel iOS](/manuals/ios/#creating-an-ios-application-bundle).

### macOS {#macos}

La création d'un bundle d'application macOS (fichier .app) est décrite dans le [manuel macOS](/manuals/macos).

### Linux {#linux}

La création d'un bundle d'application Linux ne nécessite aucune préparation particulière ni aucune configuration facultative propre à la plateforme dans *game.project*, le [fichier des paramètres du projet](/manuals/project-settings/).

### Windows {#windows}

La création d'un bundle d'application Windows (fichier .exe) est décrite dans le [manuel Windows](/manuals/windows).

### HTML5 {#html5}

La création d'un bundle d'application HTML5 ainsi que sa configuration facultative sont décrites dans le [manuel HTML5](/manuals/html5/#creating-html5-bundle).

#### Facebook Instant Games {#facebook-instant-games}

Vous pouvez créer une version spéciale d'un bundle d'application HTML5 destinée spécifiquement à Facebook Instant Games. Ce processus est décrit dans le [manuel Facebook Instant Games](/manuals/instant-games/).

## Création de bundles en ligne de commande {#bundling-from-the-command-line}

L'éditeur utilise notre outil en ligne de commande [Bob](/manuals/bob/) pour créer le bundle de l'application.

Au cours du développement quotidien de votre application, vous compilez probablement le projet et créez ses bundles depuis l'éditeur Defold. Dans d'autres circonstances, vous souhaiterez peut-être générer automatiquement des bundles d'application, par exemple en lançant des builds par lots pour toutes les cibles lors de la publication d'une nouvelle version ou en créant des builds nocturnes de la dernière version du jeu, éventuellement dans un environnement d'intégration continue. Vous pouvez compiler une application et créer ses bundles en dehors du flux de travail habituel de l'éditeur à l'aide de l'[outil en ligne de commande Bob](/manuals/bob/).

## Structure du bundle {#the-bundle-layout}

La structure logique d'un bundle se présente ainsi :

![](images/bundling/bundle_schematic_01.png)

Un bundle est généré dans un dossier. Selon la plateforme, ce dossier peut également être archivé au format zip dans un fichier `.apk` ou `.ipa`.
Le contenu du dossier dépend de la plateforme.

En plus des fichiers exécutables, notre processus de création de bundles rassemble également les ressources nécessaires pour la plateforme (par exemple, les fichiers de ressources .xml pour Android).

Le paramètre [bundle_resources](https://defold.com/manuals/project-settings/#bundle-resources) vous permet de configurer les ressources à placer telles quelles dans le bundle.
Vous pouvez définir cela pour chaque plateforme.

Les ressources du jeu se trouvent dans le fichier `game.arcd` et sont compressées individuellement avec la compression LZ4.
Le paramètre [custom_resources](https://defold.com/manuals/project-settings/#custom-resources) vous permet de configurer les ressources à placer (avec compression) dans le fichier `game.arcd`.
Vous pouvez accéder à ces ressources à l'aide de la fonction [`sys.load_resource()`](https://defold.com/ref/sys/#sys.load_resource).

## Différences entre Release et Debug {#release-vs-debug}

Lors de la création d'un bundle d'application, vous pouvez choisir entre un bundle Debug et un bundle Release. Les différences entre ces deux bundles sont minimes, mais il est important de les garder à l'esprit :

* Les builds Release n'incluent pas le [profileur](/manuals/profiling) par défaut. Définissez **Profiler** sur **Always** dans le [manifeste de l'application](/manuals/app-manifest/#profiler) pour inclure la prise en charge du profileur dans les builds Debug et Release.
* Les builds Release n'incluent pas l'[enregistreur d'écran](/ref/stable/sys/#start_record)
* Les builds Release n'affichent ni la sortie des appels à `print()` ni celle des extensions natives
* Dans les builds Release, la valeur `is_debug` de `sys.get_engine_info()` est définie sur `false`
* Les builds Release ne recherchent pas les chaînes d'origine des valeurs `hash` lors des appels à `tostring()`. En pratique, cela signifie qu'un appel à `tostring()` pour une valeur de type `url` ou `hash` renvoie sa représentation numérique et non la chaîne d'origine (`'hash: [/camera_001]'` contre `'hash: [11844936738040519888 (unknown)]'`)
* Les builds Release ne peuvent pas être ciblés depuis l'éditeur pour le [rechargement à chaud](/manuals/hot-reload) et les fonctionnalités similaires


