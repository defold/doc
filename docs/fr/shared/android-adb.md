L'outil en ligne de commande `adb` est un programme polyvalent et facile à utiliser qui permet d'interagir avec les appareils Android. Vous pouvez télécharger et installer `adb` avec les Android SDK Platform-Tools, pour Mac, Linux ou Windows.

Téléchargez les Android SDK Platform-Tools à l'adresse suivante : https://developer.android.com/studio/releases/platform-tools. Vous trouverez l'outil *adb* dans */platform-tools/*. Vous pouvez également installer des paquets propres à chaque plateforme à l'aide de leurs gestionnaires de paquets respectifs.

Sur Ubuntu Linux :

```
$ sudo apt-get install android-tools-adb
```

Sur Fedora 18/19 :

```
$ sudo yum install android-tools
```

Sur macOS (Homebrew)

```
$ brew cask install android-platform-tools
```

Vous pouvez vérifier que `adb` fonctionne en connectant votre appareil Android à votre ordinateur par USB et en exécutant la commande suivante :

```
$ adb devices
List of devices attached
31002535c90ef000    device
```

Si votre appareil n'apparaît pas, vérifiez que vous avez activé *USB debugging* sur l'appareil Android. Ouvrez les *Settings* de l'appareil et recherchez *Developer options* (ou *Development*).

![Activer le débogage USB](images/android/usb_debugging.png)
