---
title: Exécuter l'application de développement sur un appareil
brief: Ce manuel explique comment installer l'application de développement sur votre appareil pour y développer de manière itérative.
---

# L'application de développement mobile {#the-mobile-development-app}

L'application de développement vous permet d'y transférer du contenu par Wi-Fi. Vous réduisez ainsi considérablement la durée des itérations, car vous n'avez pas à créer un bundle et à l'installer chaque fois que vous souhaitez tester vos modifications. Installez l'application de développement sur votre ou vos appareils, lancez-la, puis sélectionnez l'appareil comme cible de build dans l'éditeur.

## Installer une application de développement {#installing-a-development-app}

Toute application iOS ou Android dont le bundle est créé en mode Debug peut servir d'application de développement. C'est d'ailleurs la solution recommandée, car l'application de développement disposera des paramètres de projet appropriés et utilisera les mêmes [extensions natives](/manuals/extensions/) que le projet sur lequel vous travaillez.

Il est possible de créer un bundle de votre projet avec la variante Debug sans aucun contenu. Utilisez cette option pour créer une version de votre application avec les extensions natives, adaptée au développement itératif décrit dans ce manuel.

![bundle sans contenu](images/dev-app/contentless-bundle.png)

### Installer sur iOS {#installing-on-ios}

Suivez les [instructions du manuel iOS](/manuals/ios/#creating-an-ios-application-bundle) pour créer un bundle pour iOS. Veillez à sélectionner la variante Debug !

### Installer sur Android {#installing-on-android}

Suivez les [instructions du manuel Android](https://defold.com/manuals/android/#creating-an-android-application-bundle) pour créer un bundle pour Android.

## Lancer votre jeu {#launching-your-game}

Pour lancer votre jeu sur votre appareil, l'application de développement et l'éditeur doivent pouvoir se connecter, sur le même réseau Wi-Fi ou par USB (voir ci-dessous).

1. Assurez-vous que l'éditeur est lancé et fonctionne.
2. Lancez l'application de développement sur l'appareil.
3. Sélectionnez votre appareil dans <kbd>Project ▸ Targets</kbd> dans l'éditeur.
4. Sélectionnez <kbd>Project ▸ Build</kbd> pour exécuter le jeu. Le démarrage peut prendre un certain temps, car le contenu du jeu est transféré vers l'appareil par le réseau.
5. Pendant que le jeu s'exécute, vous pouvez utiliser le [rechargement à chaud](/manuals/hot-reload/) comme d'habitude.

### Se connecter à un appareil iOS par USB sous Windows {#connecting-to-an-ios-device-using-usb-on-windows}

Pour vous connecter par USB sous Windows à une application de développement exécutée sur un appareil iOS, vous devez d'abord [installer iTunes](https://www.apple.com/lae/itunes/download/). Une fois iTunes installé, vous devez également [activer Personal Hotspot](https://support.apple.com/en-us/HT204023) sur votre appareil iOS depuis le menu Settings. Si une alerte « Trust This Computer? » s'affiche, touchez Trust. L'appareil devrait maintenant apparaître dans <kbd>Project ▸ Targets</kbd> lorsque l'application de développement est en cours d'exécution.

### Se connecter à un appareil iOS par USB sous Linux {#connecting-to-an-ios-device-using-usb-on-linux}

Sous Linux, vous devez activer Personal Hotspot sur votre appareil depuis le menu Settings lorsque vous le connectez par USB. Si une alerte « Trust This Computer? » s'affiche, touchez Trust. L'appareil devrait maintenant apparaître dans <kbd>Project ▸ Targets</kbd> lorsque l'application de développement est en cours d'exécution.

### Se connecter à un appareil iOS par USB sous macOS {#connecting-to-an-ios-device-using-usb-on-macos}

Sur les versions récentes d'iOS, l'appareil ouvre automatiquement une nouvelle interface Ethernet entre l'appareil et l'ordinateur lorsqu'il est connecté par USB sous macOS. L'appareil devrait apparaître dans <kbd>Project ▸ Targets</kbd> lorsque l'application de développement est en cours d'exécution.

Sur les anciennes versions d'iOS, vous devez activer Personal Hotspot sur votre appareil depuis le menu Settings lorsque vous le connectez par USB sous macOS. Si une alerte « Trust This Computer? » s'affiche, touchez Trust. L'appareil devrait maintenant apparaître dans <kbd>Project ▸ Targets</kbd> lorsque l'application de développement est en cours d'exécution.

### Se connecter à un appareil Android par USB sous macOS {#connecting-to-an-android-device-using-usb-on-macos}

Sous macOS, il est possible de se connecter par USB à une application de développement en cours d'exécution sur un appareil Android lorsque l'appareil est en USB Tethering Mode. Sous macOS, vous devez installer un pilote tiers tel que [HoRNDIS](https://joshuawise.com/horndis#available_versions). Une fois HoRNDIS installé, vous devez également l'autoriser à s'exécuter dans les paramètres Security & Privacy. Une fois USB Tethering activé, l'appareil apparaîtra dans <kbd>Project ▸ Targets</kbd> lorsque l'application de développement est en cours d'exécution.

### Se connecter à un appareil Android par USB sous Windows ou Linux {#connecting-to-an-android-device-using-usb-on-windows-or-linux}

Sous Windows et Linux, il est possible de se connecter par USB à une application de développement en cours d'exécution sur un appareil Android lorsque l'appareil est en USB Tethering Mode. Une fois USB Tethering activé, l'appareil apparaîtra dans <kbd>Project ▸ Targets</kbd> lorsque l'application de développement est en cours d'exécution.

## Dépannage {#troubleshooting}

Message « Unable to download application »
: Assurez-vous que l'UDID de votre appareil figure dans le profil de provisionnement mobile utilisé pour signer l'application.

Votre appareil n'apparaît pas dans le menu Targets
: Assurez-vous que votre appareil est connecté au même réseau Wi-Fi que votre ordinateur. Assurez-vous que l'application de développement est compilée en mode Debug.

Le jeu ne démarre pas et affiche un message indiquant que les versions ne correspondent pas
: Cela se produit lorsque vous avez mis à jour l'éditeur vers la dernière version. Vous devez compiler et installer une nouvelle version.
