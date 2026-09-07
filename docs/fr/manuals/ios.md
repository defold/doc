---
title: Développement avec Defold pour la plateforme iOS
brief: Ce manuel explique comment créer et exécuter des jeux et des applications sur des appareils iOS avec Defold.
---

# Développement pour iOS {#ios-development}

::: sidenote
La création d'un bundle de jeu pour iOS est disponible uniquement dans la version Mac de l'éditeur Defold.
:::

Sous iOS, _toute_ application que vous créez et souhaitez exécuter sur votre téléphone ou votre tablette _doit_ être signée avec un certificat délivré par Apple et un profil d'approvisionnement. Ce manuel explique les étapes de la création d'un bundle de votre jeu pour iOS. Pendant le développement, il est souvent préférable d'exécuter votre jeu au moyen de l'[application de développement](/manuals/dev-app), car elle vous permet de recharger à chaud le contenu et le code directement sur votre appareil.

## Processus de signature de code d'Apple {#apples-code-signing-process}

La sécurité des applications iOS repose sur plusieurs composants. Vous pouvez accéder aux outils nécessaires en vous inscrivant au [programme iOS Developer Program d'Apple](https://developer.apple.com/programs/). Une fois inscrit, rendez-vous dans l'[espace Developer Member Center d'Apple](https://developer.apple.com/membercenter/index.action).

![Espace membre Apple](images/ios/apple_member_center.png)

La section *Certificates, Identifiers & Profiles* contient tous les outils dont vous avez besoin. Vous pouvez y créer, supprimer et modifier les éléments suivants :

Certificates
: Certificats cryptographiques délivrés par Apple qui vous identifient en tant que développeur. Vous pouvez créer des certificats de développement ou de production. Les certificats de développement vous permettent de tester certaines fonctionnalités, comme le mécanisme d'achats intégrés, dans un environnement de test isolé. Les certificats de production servent à signer l'application finale destinée à être envoyée sur l'App Store. Vous avez besoin d'un certificat pour signer les applications avant de pouvoir les installer sur votre appareil afin de les tester.

Identifiers
: Identifiants destinés à différents usages. Il est possible d'enregistrer des identifiants génériques (par exemple `some.prefix.*`) utilisables avec plusieurs applications. Les App ID peuvent contenir des informations sur les services d'application, par exemple si l'application active l'intégration de Passbook, le Game Center, etc. Ces App ID ne peuvent pas être des identifiants génériques. Pour que les services d'application fonctionnent, l'*identifiant de bundle* de votre application doit correspondre à l'identifiant App ID.

Devices
: Chaque appareil de développement doit être enregistré avec son UDID (identifiant unique d'appareil, voir ci-dessous).

Provisioning Profiles
: Les profils d'approvisionnement associent des certificats à des App ID et à une liste d'appareils. Ils indiquent quelle application de quel développeur est autorisée sur quels appareils.

Pour signer vos jeux et applications dans Defold, vous avez besoin d'un certificat valide et d'un profil d'approvisionnement valide.

::: sidenote
Certaines opérations disponibles sur la page d'accueil du Member Center peuvent également être effectuées depuis l'environnement de développement Xcode, si vous l'avez installé.
:::

Identifiant de l'appareil (UDID)
: Vous pouvez trouver l'UDID d'un appareil iOS en le connectant à un ordinateur par Wi-Fi ou par câble. Ouvrez Xcode et sélectionnez <kbd>Window ▸ Devices and Simulators</kbd>. Le numéro de série et l'identifiant s'affichent lorsque vous sélectionnez votre appareil.

  ![Appareils dans Xcode](images/ios/xcode_devices.png)

  Si Xcode n'est pas installé, vous pouvez trouver l'identifiant dans iTunes. Cliquez sur l'icône des appareils et sélectionnez le vôtre.

  ![Appareils dans iTunes](images/ios/itunes_devices.png)

  1. Sur la page *Summary*, repérez le champ *Serial Number*.
  2. Cliquez une fois sur *Serial Number* pour que le champ affiche *UDID*. Si vous cliquez plusieurs fois, différentes informations sur l'appareil s'affichent. Continuez simplement à cliquer jusqu'à ce que *UDID* apparaisse.
  3. Faites un clic droit sur la longue chaîne UDID et sélectionnez <kbd>Copy</kbd> pour copier l'identifiant dans le presse-papiers. Vous pourrez ainsi facilement le coller dans le champ UDID lors de l'enregistrement de l'appareil dans le Developer Member Center d'Apple.

## Développement avec un compte développeur Apple gratuit {#developing-using-a-free-apple-developer-account}

Depuis Xcode 7, tout le monde peut installer Xcode et développer gratuitement sur un appareil. Vous n'avez pas besoin de vous inscrire à l'iOS Developer Program. Xcode vous délivrera automatiquement un certificat de développeur (valable un an) et un profil d'approvisionnement pour votre application (valable une semaine) sur votre appareil spécifique.

1. Connectez votre appareil.
2. Installez Xcode.
3. Ajoutez un nouveau compte dans Xcode et connectez-vous avec votre identifiant Apple.
4. Créez un nouveau projet. Le modèle le plus simple, `Single View App`, convient parfaitement.
5. Sélectionnez votre `Team` (créée automatiquement pour vous) et attribuez un identifiant de bundle à l'application.

::: important
Notez l'identifiant de bundle, car vous devez utiliser le même dans votre projet Defold.
:::

6. Vérifiez que Xcode a créé un *Provisioning Profile* et un *Signing Certificate* pour l'application.

   ![](images/ios/xcode_certificates.png)

7. Compilez l'application sur votre appareil. La première fois, Xcode vous demandera d'activer le mode développeur et préparera l'appareil pour permettre le débogage. Cela peut prendre un certain temps.
8. Une fois que vous avez vérifié que l'application fonctionne, retrouvez-la sur votre disque. Vous pouvez voir l'emplacement du build dans le rapport de build, dans le `Report Navigator`.

   ![](images/ios/app_location.png)

9. Repérez l'application, faites un clic droit dessus et sélectionnez <kbd>Show Package Contents</kbd>.

   ![](images/ios/app_contents.png)

10. Copiez le fichier `embedded.mobileprovision` à un endroit de votre disque où vous pourrez le retrouver.

   ![](images/ios/free_provisioning.png)

Ce fichier d'approvisionnement peut être utilisé avec votre identité de signature de code pour signer des applications dans Defold pendant une semaine.

Lorsque le profil d'approvisionnement expire, vous devez compiler de nouveau l'application dans Xcode et obtenir un nouveau fichier d'approvisionnement temporaire comme décrit ci-dessus.

## Création d'un bundle d'application iOS {#creating-an-ios-application-bundle}

Une fois que vous disposez de l'identité de signature de code et du profil d'approvisionnement, vous pouvez créer depuis l'éditeur un bundle d'application autonome pour votre jeu. Sélectionnez simplement <kbd>Project ▸ Bundle... ▸ iOS Application...</kbd> dans le menu.

![Signature d'un bundle iOS](images/ios/sign_bundle.png)

Sélectionnez votre identité de signature de code, parcourez vos fichiers pour choisir votre fichier d'approvisionnement mobile et sélectionnez la variante (Debug ou Release). Vous pouvez décocher la case `Sign application` pour ignorer la signature et signer manuellement à une étape ultérieure. Cochez `Simulator` pour créer un bundle `arm64_sim-ios` destiné au simulateur iOS, à la place d'un bundle pour appareil.

::: important
Les bundles pour simulateur s'exécutent uniquement dans le simulateur iOS sur les Mac avec puce Apple Silicon. Ils n'utilisent ni identité de signature ni profil d'approvisionnement ; les options de signature, d'installation et de lancement sont donc désactivées lorsque `Simulator` est coché. Installez le bundle avec `xcrun simctl` comme décrit ci-dessous.
:::

Cliquez sur *Create Bundle*. Vous serez alors invité à préciser l'emplacement de votre ordinateur où le bundle sera créé.

![Bundle d'application iOS au format ipa](images/ios/ipa_file.png){.left}

Vous définissez l'icône de l'application, le storyboard de l'écran de lancement, etc. dans la [section iOS](/manuals/project-settings/#ios) du fichier de paramètres du projet *game.project*.

### Info.plist personnalisé et découverte de cibles locales {#custom-infoplist-and-local-target-discovery}

Le fichier `Info.plist` iOS intégré contient le service Bonjour et la description de l'utilisation du réseau local nécessaires à la découverte automatique des cibles par l'éditeur dans les builds autres que ceux de publication. Un fichier `Info.plist` personnalisé remplace ce manifeste de base intégré. Si vous utilisez un manifeste personnalisé pour un build de débogage et avez besoin de la découverte de cibles, du profilage, du rechargement à chaud ou de la diffusion des journaux sur le réseau local, ajoutez ces entrées :

```xml
{{^variant_release}}
<key>NSBonjourServices</key>
<array>
    <string>_defold._tcp</string>
</array>
<key>NSLocalNetworkUsageDescription</key>
<string>Discover Defold targets on the local network.</string>
{{/variant_release}}
```

La condition Mustache exclut les entrées de découverte des bundles de publication. La chaîne décrivant l'utilisation est affichée à l'utilisateur par iOS et peut être adaptée ou localisée. Ne supprimez la condition que si l'application de publication utilise elle-même le même service Bonjour et la même fonctionnalité de réseau local.

:[Build Variants](../shared/build-variants.md)

## Installation et lancement du bundle sur un iPhone connecté {#installing-and-launching-bundle-on-a-connected-iphone}

Vous pouvez installer et lancer le bundle généré à l'aide des cases à cocher `Install on connected device` et `Launch installed app` de l'éditeur, dans la boîte de dialogue Bundle :

![Installation et lancement d'un bundle iOS](images/ios/install_and_launch.png)

L'outil en ligne de commande [ios-deploy](https://github.com/ios-control/ios-deploy) doit être installé pour que cette fonctionnalité fonctionne. Le moyen le plus simple de l'installer est d'utiliser Homebrew :
```
$ brew install ios-deploy
```

Si l'éditeur ne parvient pas à détecter l'emplacement d'installation de l'outil ios-deploy, vous devrez le préciser dans les [préférences](/manuals/editor-preferences/#tools). 

### Création d'un storyboard {#creating-a-storyboard}

Vous créez un fichier de storyboard à l'aide de Xcode. Lancez Xcode et créez un nouveau projet. Sélectionnez iOS et Single View App :

![Création d'un projet](images/ios/xcode_create_project.png)

Cliquez sur Next et configurez votre projet. Renseignez le champ Product Name :

![Paramètres du projet](images/ios/xcode_storyboard_create_project_settings.png)

Cliquez sur Create pour terminer. Votre projet est maintenant créé et nous pouvons passer à la création du storyboard :

![Vue du projet](images/ios/xcode_storyboard_project_view.png)

Glissez-déposez une image pour l'importer dans le projet. Sélectionnez ensuite `Assets.xcassets` et déposez l'image dans `Assets.xcassets` :

![Ajout d'une image](images/ios/xcode_storyboard_add_image.png)

Ouvrez `LaunchScreen.storyboard` et cliquez sur le bouton plus (<kbd>+</kbd>). Saisissez `imageview` dans la boîte de dialogue pour trouver le composant ImageView.

![Ajout d'une vue d'image](images/ios/xcode_storyboard_add_imageview.png)

Faites glisser le composant Image View sur le storyboard :

![Ajout au storyboard](images/ios/xcode_storyboard_add_imageview_to_storyboard.png)

Sélectionnez l'image que vous avez précédemment ajoutée à `Assets.xcassets` dans la liste déroulante Image :

![](images/ios/xcode_storyboard_select_image.png)

Positionnez l'image et effectuez les autres ajustements nécessaires, en ajoutant éventuellement un Label ou un autre élément d'interface. Une fois terminé, définissez le schéma actif sur **Any iOS Device (arm64)** (ou **Generic iOS Device**) et sélectionnez **Product ▸ Build**. Defold prend en charge iOS 15.0 et les versions ultérieures sur les appareils 64 bits ; conservez donc une cible de déploiement égale ou supérieure à 15.0. Attendez la fin de la compilation.

Si vous utilisez des images dans le storyboard, elles ne seront pas automatiquement incluses dans votre fichier `LaunchScreen.storyboardc`. Utilisez le champ `Bundle Resources` de *game.project* pour inclure les ressources.
Par exemple, créez un dossier `LaunchScreen` dans le projet Defold et un dossier `ios` à l'intérieur (le dossier `ios` est nécessaire pour inclure ces fichiers uniquement dans les bundles iOS), puis placez vos fichiers dans `LaunchScreen/ios/`. Ajoutez ce chemin dans `Bundle Resources`.

![](images/ios/bundle_res.png)

La dernière étape consiste à copier le fichier compilé `LaunchScreen.storyboardc` dans votre projet Defold. Ouvrez le Finder à l'emplacement suivant et copiez le fichier `LaunchScreen.storyboardc` dans votre projet Defold :

    /Library/Developer/Xcode/DerivedData/YOUR-PRODUCT-NAME-cbqnwzfisotwygbybxohrhambkjy/Build/Intermediates.noindex/YOUR-PRODUCT-NAME.build/Debug-iphonesimulator/YOUR-PRODUCT-NAME.build/Base.lproj/LaunchScreen.storyboardc

::: sidenote
Sergey Lerg, utilisateur du forum, a réalisé [un tutoriel vidéo montrant la procédure](https://www.youtube.com/watch?v=6jU8wGp3OwA&feature=emb_logo).
:::

Une fois le fichier de storyboard obtenu, vous pouvez le référencer dans *game.project*.


### Création d'un catalogue de ressources d'icônes {#creating-an-icon-asset-catalog}

L'utilisation d'un catalogue de ressources est la méthode privilégiée par Apple pour gérer les icônes de votre application. C'est d'ailleurs le seul moyen de fournir l'icône utilisée sur la fiche de l'App Store. Vous créez un catalogue de ressources de la même manière qu'un storyboard, à l'aide de Xcode. Lancez Xcode et créez un nouveau projet. Sélectionnez iOS et Single View App :

![Création d'un projet](images/ios/xcode_create_project.png)

Cliquez sur Next et configurez votre projet. Renseignez le champ Product Name :

![Paramètres du projet](images/ios/xcode_icons_create_project_settings.png)

Cliquez sur Create pour terminer. Votre projet est maintenant créé et nous pouvons passer à la création du catalogue de ressources :

![Vue du projet](images/ios/xcode_icons_project_view.png)

Glissez-déposez des images dans les cases vides correspondant aux différentes tailles d'icônes prises en charge :

![Ajout d'icônes](images/ios/xcode_icons_add_icons.png)

::: sidenote
N'ajoutez aucune icône pour Notifications, Settings ou Spotlight.
:::

Une fois terminé, définissez le schéma actif sur `Build -> Any iOS Device (arm64)` (ou `Generic iOS Device`) et sélectionnez <kbd>Product</kbd> -> <kbd>Build</kbd>. Attendez la fin de la compilation.

::: sidenote
Veillez à compiler pour `Any iOS Device (arm64)` ou `Generic iOS Device`, sinon vous obtiendrez l'erreur `ERROR ITMS-90704` lors de l'envoi de votre build.
:::

![Compilation du projet](images/ios/xcode_icons_build.png)

La dernière étape consiste à copier le fichier compilé `Assets.car` dans votre projet Defold. Ouvrez le Finder à l'emplacement suivant et copiez le fichier `Assets.car` dans votre projet Defold :

    /Library/Developer/Xcode/DerivedData/YOUR-PRODUCT-NAME-cbqnwzfisotwygbybxohrhambkjy/Build/Products/Debug-iphoneos/Icons.app/Assets.car

Une fois le fichier de catalogue de ressources obtenu, vous pouvez le référencer, ainsi que les icônes, dans *game.project* :

![Ajout de l'icône et du catalogue de ressources dans game.project](images/ios/defold_icons_game_project.png)

::: sidenote
L'icône de l'App Store n'a pas besoin d'être référencée dans *game.project*. Elle est automatiquement extraite du fichier `Assets.car` lors de l'envoi à iTunes Connect.
:::


## Installation d'un bundle d'application iOS {#installing-an-ios-application-bundle}

L'éditeur crée un fichier *.ipa*, qui est un bundle d'application iOS. Pour installer ce fichier sur votre appareil, vous pouvez utiliser l'un des outils suivants :

* Xcode, via la fenêtre `Devices and Simulators`
* L'outil en ligne de commande [`ios-deploy`](https://github.com/ios-control/ios-deploy)
* [`Apple Configurator 2`](https://apps.apple.com/us/app/apple-configurator-2/), disponible dans l'App Store de macOS
* iTunes

Vous pouvez également utiliser l'outil en ligne de commande `xcrun simctl` pour travailler avec les simulateurs iOS disponibles via Xcode :

```
# show a list of available devices
xcrun simctl list

# boot an iPhone X simulator
xcrun simctl boot "iPhone X"

# install your.app to a booted simulator
xcrun simctl install booted your.app

# launch the simulator
open /Applications/Xcode.app/Contents/Developer/Applications/Simulator.app
```

:[Apple Privacy Manifest](../shared/apple-privacy-manifest.md)


## Informations de conformité à l'exportation {#export-compliance-information}

Lorsque vous soumettez votre jeu à l'App Store, il vous sera demandé de fournir des informations de conformité à l'exportation concernant l'utilisation du chiffrement dans votre jeu. [Apple explique pourquoi ces informations sont requises](https://developer.apple.com/documentation/security/complying_with_encryption_export_regulations) :

« Lorsque vous soumettez votre application à TestFlight ou à l'App Store, vous l'envoyez sur un serveur situé aux États-Unis. Si vous distribuez votre application en dehors des États-Unis ou du Canada, elle est soumise aux lois américaines sur l'exportation, quel que soit le pays où votre entité juridique est établie. Si votre application utilise du chiffrement, y accède, en contient, en implémente ou en intègre, cela est considéré comme une exportation de logiciel de chiffrement. Votre application est donc soumise aux exigences américaines de conformité à l'exportation, ainsi qu'aux exigences de conformité à l'importation des pays où vous la distribuez. »

Le moteur de jeu Defold utilise le chiffrement aux fins suivantes :

* Effectuer des appels sur des canaux sécurisés (c'est-à-dire HTTPS et SSL)
* Protéger les droits d'auteur sur le code Lua (pour empêcher sa duplication)

Ces usages du chiffrement dans le moteur Defold sont exemptés des exigences documentaires de conformité à l'exportation en vertu des lois des États-Unis et de l'Union européenne. La plupart des projets Defold resteront exemptés, mais l'ajout d'autres méthodes cryptographiques peut modifier ce statut. Il vous incombe de vérifier que votre projet satisfait aux exigences de ces lois et aux règles de l'App Store. Consultez la [présentation de la conformité à l'exportation](https://help.apple.com/app-store-connect/#/dev88f5c7bf9) d'Apple pour plus d'informations.

Si vous estimez que votre projet bénéficie d'une exemption, définissez la clé [`ITSAppUsesNonExemptEncryption`](https://developer.apple.com/documentation/bundleresources/information-property-list/itsappusesnonexemptencryption) sur `False` dans le fichier `Info.plist` du projet. Consultez les [manifestes d'application](/manuals/extensions-manifest-merge-tool) pour plus de détails.

## Foire aux questions {#faq}
:[iOS FAQ](../shared/ios-faq.md)
