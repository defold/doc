---
title: Développement avec Defold pour la plateforme macOS
brief: Ce manuel décrit comment compiler et exécuter des applications Defold sous macOS
---

# Développement pour macOS {#macos-development}

Développer des applications Defold pour la plateforme macOS est un processus simple, avec très peu de points à prendre en compte.

## Paramètres du projet {#project-settings}

La configuration de l'application propre à macOS s'effectue dans la [section macOS](/manuals/project-settings/#macos) du fichier de paramètres *game.project*.

## Icône de l'application {#application-icon}

L'icône de l'application utilisée pour un jeu macOS doit être au format .`icns`. Vous pouvez facilement créer un fichier `.icns` à partir d'un ensemble de fichiers `.png` regroupés dans un `.iconset`. Suivez les [instructions officielles pour créer un fichier `.icns`](https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Optimizing/Optimizing.html). Voici un bref résumé des étapes à suivre :

* Créez un dossier pour les icônes, par exemple `game.iconset`
* Copiez les fichiers des icônes dans le dossier créé :

    * `icon_16x16.png`
    * `icon_16x16@2x.png`
    * `icon_32x32.png`
    * `icon_32x32@2x.png`
    * `icon_128x128.png`
    * `icon_128x128@2x.png`
    * `icon_256x256.png`
    * `icon_256x256@2x.png`
    * `icon_512x512.png`
    * `icon_512x512@2x.png`

* Convertissez le dossier `.iconset` en fichier `.icns` à l'aide de l'outil en ligne de commande `iconutil` :

```
iconutil -c icns -o game.icns game.iconset
```

## Publication de votre application {#publishing-your-application}
Vous pouvez publier votre application sur le Mac App Store, sur une boutique ou un portail tiers comme Steam ou itch.io, ou par vos propres moyens sur un site web. Avant de publier votre application, vous devez la préparer pour sa soumission. Les étapes suivantes sont obligatoires, quel que soit le mode de distribution envisagé pour l'application :

1. Assurez-vous que tout le monde peut exécuter votre jeu en ajoutant les droits d'exécution (par défaut, seul le propriétaire du fichier dispose de ces droits) :

```
$ chmod +x Game.app/Contents/MacOS/Game
```

2. Créez un fichier d'autorisations indiquant les autorisations requises par votre jeu. Pour la plupart des jeux, les autorisations suivantes suffisent :

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.allow-dyld-environment-variables</key>
    <true/>
  </dict>
</plist>
```

  * `com.apple.security.cs.allow-jit` - Indique si l'application peut créer de la mémoire accessible en écriture et exécutable à l'aide de l'indicateur MAP_JIT
  * `com.apple.security.cs.allow-unsigned-executable-memory` - Indique si l'application peut créer de la mémoire accessible en écriture et exécutable sans les restrictions imposées par l'utilisation de l'indicateur MAP_JIT
  * `com.apple.security.cs.allow-dyld-environment-variables` - Indique si l'application peut être affectée par les variables d'environnement de l'éditeur de liens dynamique, que vous pouvez utiliser pour injecter du code dans le processus de votre application

Certaines applications peuvent également nécessiter des autorisations supplémentaires. L'extension Steamworks a besoin de cette autorisation supplémentaire :

```
<key>com.apple.security.cs.disable-library-validation</key>
<true/>
```

  * `com.apple.security.cs.disable-library-validation` - Indique si l'application peut charger des modules complémentaires ou des frameworks quelconques, sans exiger de signature de code.

Toutes les autorisations pouvant être accordées à une application sont répertoriées dans la [documentation officielle Apple destinée aux développeurs](https://developer.apple.com/documentation/bundleresources/entitlements).

3. Signez votre jeu à l'aide de `codesign` :

```
$ codesign --force --sign "Developer ID Application: Company Name" --options runtime --deep --timestamp --entitlements entitlement.plist Game.app
```

## Publication en dehors du Mac App Store {#publishing-outside-the-mac-app-store}
Apple exige que tous les logiciels distribués en dehors du Mac App Store soient notariés par Apple pour pouvoir être exécutés par défaut sous macOS Catalina. Consultez la [documentation officielle](https://developer.apple.com/documentation/xcode/notarizing_macos_software_before_distribution/customizing_the_notarization_workflow) pour savoir comment ajouter la notarisation à un environnement de build piloté par des scripts en dehors de Xcode. Voici un bref résumé des étapes à suivre :

1. Suivez les étapes ci-dessus pour ajouter les autorisations et signer l'application.

2. Compressez votre jeu au format ZIP et envoyez-le pour notarisation à l'aide de `altool`.

```
$ xcrun altool --notarize-app
               --primary-bundle-id "com.acme.foobar"
               --username "AC_USERNAME"
               --password "@keychain:AC_PASSWORD"
               --asc-provider <ProviderShortname>
               --file Game.zip

altool[16765:378423] No errors uploading 'Game.zip'.
RequestUUID = 2EFE2717-52EF-43A5-96DC-0797E4CA1041
```

3. Vérifiez l'état de votre soumission à l'aide de l'UUID de requête renvoyé par l'appel à `altool --notarize-app` :

```
$ xcrun altool --notarization-info 2EFE2717-52EF-43A5-96DC-0797E4CA1041
               -u "AC_USERNAME"
```

4. Attendez que l'état devienne `success`, puis attachez le ticket de notarisation au jeu :

```
$ xcrun stapler staple "Game.app"
```

5. Votre jeu est maintenant prêt à être distribué.

## Publication sur le Mac App Store {#publishing-to-the-mac-app-store}
Le processus de publication sur le Mac App Store est bien décrit dans la [documentation Apple destinée aux développeurs](https://developer.apple.com/macos/submit/). Veillez à ajouter les autorisations et à signer l'application avec `codesign` comme décrit ci-dessus avant de la soumettre.

Remarque : le jeu n'a pas besoin d'être notarié pour être publié sur le Mac App Store.

:[Apple Privacy Manifest](../shared/apple-privacy-manifest.md)
