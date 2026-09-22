---
title: Développer avec Defold pour la plateforme Android
brief: Ce manuel décrit comment créer des builds d'applications Defold et les exécuter sur des appareils Android
---

# Développement pour Android {#android-development}

Les appareils Android vous permettent d'y exécuter librement vos propres applications. Il est très facile de créer un build de votre jeu et de le copier sur un appareil Android. Ce manuel explique les étapes nécessaires à la création d'un bundle de votre jeu pour Android. Pendant le développement, il est souvent préférable d'exécuter votre jeu avec l'[application de développement](/manuals/dev-app), car elle vous permet de recharger à chaud le contenu et le code directement sur votre appareil.

## Processus de signature pour Android et Google Play {#android-and-google-play-signing-process}

Android exige que tous les APK soient signés numériquement avec un certificat avant leur installation ou leur mise à jour sur un appareil. Si vous utilisez des Android App Bundles, vous devez uniquement signer votre bundle d'application avant de l'importer dans la Play Console, puis [Play App Signing](https://developer.android.com/studio/publish/app-signing#app-signing-google-play) s'occupe du reste. Vous pouvez aussi signer manuellement votre application pour l'importer sur Google Play ou d'autres boutiques d'applications, ou pour la distribuer en dehors de toute boutique.

Lorsque vous créez un bundle d'application Android depuis l'éditeur Defold ou l'[outil en ligne de commande](/manuals/bob), vous pouvez fournir un magasin de clés (keystore), contenant votre certificat et votre clé, ainsi que son mot de passe, qui serviront à signer votre application. Si vous ne le faites pas, Defold génère un magasin de clés de débogage et l'utilise pour signer le bundle d'application.

::: important
Vous ne devez **jamais** importer votre application sur Google Play si elle a été signée avec un magasin de clés de débogage. Utilisez toujours un magasin de clés dédié que vous avez créé vous-même.
:::

## Création d'un magasin de clés {#creating-a-keystore}

::: sidenote
Defold utilise un magasin de clés pour le processus de signature Android. [Vous trouverez plus d'informations dans ce message du forum](https://forum.defold.com/t/upcoming-change-to-the-android-build-pipeline/66084).
:::

Vous pouvez créer un magasin de clés [avec Android Studio](https://developer.android.com/studio/publish/app-signing#generate-key) ou depuis un terminal ou une invite de commandes :

```bash
keytool -genkey -v -noprompt -dname "CN=John Smith, OU=Area 51, O=US Air Force, L=Unknown, ST=Nevada, C=US" -keystore mykeystore.keystore -storepass 5Up3r_53cR3t -alias myAlias -keyalg RSA -validity 9125
```

Cette commande crée un fichier de magasin de clés nommé `mykeystore.keystore`, contenant une clé et un certificat. L'accès à la clé et au certificat est protégé par le mot de passe `5Up3r_53cR3t`. La clé et le certificat sont valables pendant 25 ans (9125 jours). La clé et le certificat générés sont identifiés par l'alias `myAlias`.

::: important
Veillez à conserver le magasin de clés et son mot de passe en lieu sûr. Si vous signez et importez vous-même vos applications sur Google Play et que vous perdez le magasin de clés ou son mot de passe, vous ne pourrez plus mettre à jour l'application sur Google Play. Vous pouvez éviter cette situation en utilisant Google Play App Signing et en laissant Google signer vos applications pour vous.
:::


## Création d'un bundle d'application Android {#creating-an-android-application-bundle}

L'éditeur vous permet de créer facilement un bundle d'application autonome pour votre jeu. Avant de créer le bundle, vous pouvez préciser les icônes à utiliser pour l'application, définir le code de version, etc. dans le [fichier de paramètres du projet](/manuals/project-settings/#android) *game.project*.

Pour créer un bundle, sélectionnez <kbd>Project ▸ Bundle... ▸ Android Application...</kbd> dans le menu.

Si vous souhaitez que l'éditeur crée automatiquement des certificats de débogage aléatoires, laissez les champs *Keystore* et *Keystore password* vides :

![Signature d'un bundle Android](images/android/sign_bundle.png)

Si vous souhaitez signer votre bundle avec un magasin de clés particulier, renseignez les champs *Keystore* et *Keystore password*. Le fichier *Keystore* doit avoir l'extension `.keystore`, tandis que le mot de passe doit être enregistré dans un fichier texte portant l'extension `.txt`. Vous pouvez aussi renseigner le champ *Key password* si la clé du magasin de clés utilise un mot de passe différent de celui du magasin lui-même :

![Signature d'un bundle Android](images/android/sign_bundle2.png)

Defold permet de créer des fichiers APK et AAB. Sélectionnez APK ou AAB dans la liste déroulante *Bundle Format*.

Cliquez sur <kbd>Create Bundle</kbd> lorsque vous avez configuré les paramètres du bundle d'application. Vous devrez ensuite préciser à quel emplacement de votre ordinateur le bundle sera créé.

![Fichier de paquet d'application Android](images/android/apk_file.png)

:[Build Variants](../shared/build-variants.md)

### Installation d'un bundle d'application Android {#installing-an-android-application-bundle}

#### Installation d'un APK {#installing-an-apk}

Vous pouvez copier un fichier *`.apk`* sur votre appareil avec l'outil `adb`, ou sur Google Play via la [console développeur Google Play](https://play.google.com/apps/publish/).

:[Android ADB](../shared/android-adb.md)

```
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
  pkg: /data/local/tmp/my_app.apk
Success
```

#### Installation d'un APK avec l'éditeur {#installing-an-apk-using-editor}

Vous pouvez installer et lancer un fichier *`.apk`* à l'aide des cases à cocher « Install on connected device » et « Launch installed app » de l'éditeur, dans la boîte de dialogue Bundle :

![Installation et lancement d'un APK](images/android/install_and_launch.png)

Pour que cette fonctionnalité fonctionne, *ADB* doit être installé et *USB debugging* doit être activé sur l'appareil connecté. Si l'éditeur ne parvient pas à détecter l'emplacement d'installation de l'outil en ligne de commande ADB, vous devez le préciser dans les [Preferences](/manuals/editor-preferences/#tools).

#### Installation d'un AAB {#installing-an-aab}

Vous pouvez importer un fichier *.aab* sur Google Play via la [console développeur Google Play](https://play.google.com/apps/publish/). Vous pouvez aussi générer un fichier *`.apk`* à partir d'un fichier *.aab* pour l'installer localement avec [Android bundletool](https://developer.android.com/studio/command-line/bundletool).

## Réduction du code Java avec R8 {#shrinking-java-code-with-r8}

R8 réduit la taille du code Java en supprimant le code inutilisé, en l'optimisant et en l'obfusquant.

### Activation de R8 {#enabling-r8}

Sélectionnez `/builtins/manifests/android/dmengine.keep` dans **Android ▸ R8 Keep Rules** dans *game.project*. Vous utilisez ainsi directement les règles par défaut de Defold :

```ini
[android]
r8_keep_rules = /builtins/manifests/android/dmengine.keep
```

Assurez-vous que chaque extension contenant du code Java fournit un fichier `.keep` pour les classes dont elle a besoin à l'exécution. Les règles des extensions sont combinées aux règles du projet sélectionnées lors du build. Testez un build de publication sur un appareil après avoir activé R8.

Si vous laissez **R8 Keep Rules** vide, D8 est utilisé sans suppression du code inutilisé. L'activation de R8 fait appel au service de build des extensions natives, même pour un projet sans extensions natives.

### Ajout de règles à une extension {#adding-rules-to-an-extension}

Les règles de conservation d'une extension doivent se trouver dans son répertoire `manifests/android`, à côté de `build.gradle`. Consultez les [règles de conservation R8 pour les extensions Android](/manuals/extensions/#r8-keep-rules-for-android) pour savoir comment ajouter un fichier et préserver les classes Java de l'extension.

### Conservation de la table de correspondance d'obfuscation {#keeping-the-obfuscation-mapping}

Activez **Generate debug symbols** dans la boîte de dialogue de création de bundles Android, ou passez `--with-symbols` à Bob, pour conserver le fichier `mapping.txt` de R8 lorsque le build en produit un. Par exemple, depuis le répertoire du projet :

```sh
java -jar bob.jar --platform arm64-android --variant release \
  --archive --with-symbols --bundle-output build/android \
  resolve build bundle
```

La table de correspondance est enregistrée sous `<binary-name>.apk.symbols/mapping.txt`, à côté de l'APK ou de l'AAB généré. Par exemple, avec le titre de projet `My Game`, la commande ci-dessus produit `build/android/MyGame/MyGame.apk.symbols/mapping.txt`.

Conservez ce fichier avec la version de publication exacte dont il provient. Il permet de retrouver les noms Java d'origine à partir des noms obfusqués pour interpréter les traces de pile ; une table issue d'un autre build peut donner des résultats incorrects.

## Autorisations {#permissions}

Le moteur Defold nécessite plusieurs autorisations pour que toutes ses fonctionnalités puissent fonctionner. Les autorisations sont définies dans le fichier `AndroidManifest.xml`, indiqué dans le [fichier de paramètres du projet](/manuals/project-settings/#android) *game.project*. Vous trouverez plus d'informations sur les autorisations Android dans [la documentation officielle](https://developer.android.com/guide/topics/permissions/overview). Les autorisations suivantes sont demandées dans le manifeste par défaut :

### android.permission.INTERNET et android.permission.ACCESS_NETWORK_STATE (niveau de protection : normal) {#androidpermissioninternet-and-androidpermissionaccess_network_state-protection-level-normal}
Permettent aux applications d'ouvrir des *sockets réseau* et d'accéder aux informations sur les réseaux. Ces autorisations sont nécessaires pour accéder à Internet. ([Documentation officielle Android](https://developer.android.com/reference/android/Manifest.permission#INTERNET)) et ([Documentation officielle Android](https://developer.android.com/reference/android/Manifest.permission#ACCESS_NETWORK_STATE)).

### android.permission.WAKE_LOCK (niveau de protection : normal) {#androidpermissionwake_lock-protection-level-normal}
Permet d'utiliser les WakeLocks de PowerManager pour empêcher la mise en veille du processeur ou la réduction de la luminosité de l'écran. Cette autorisation est nécessaire pour empêcher temporairement l'appareil de se mettre en veille pendant la réception d'une notification push. ([Documentation officielle Android](https://developer.android.com/reference/android/Manifest.permission#WAKE_LOCK))


## Utilisation d'AndroidX {#using-androidx}
AndroidX est une amélioration majeure de la bibliothèque Android Support Library d'origine, qui n'est plus maintenue. Les paquets AndroidX remplacent entièrement la Support Library en offrant les mêmes fonctionnalités et de nouvelles bibliothèques. La plupart des extensions Android de l'[Asset Portal](/assets) prennent en charge AndroidX. Si vous ne souhaitez pas utiliser AndroidX, vous pouvez le désactiver explicitement au profit de l'ancienne Android Support Library en cochant `Use Android Support Lib` dans le [manifeste de l'application](https://defold.com/manuals/app-manifest/).

![](images/android/enable_supportlibrary.png)

## Questions fréquentes {#faq}
:[Android FAQ](../shared/android-faq.md)
