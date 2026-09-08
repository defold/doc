Lo strumento a riga di comando `adb` è un programma versatile e facile da usare che permette di interagire con i dispositivi Android. Puoi scaricare e installare `adb` come parte di Android SDK Platform-Tools, per Mac, Linux o Windows.

Scarica Android SDK Platform-Tools da: https://developer.android.com/studio/releases/platform-tools. Trovi lo strumento *adb* in */platform-tools/*. In alternativa, puoi installare i pacchetti specifici per la tua piattaforma tramite i rispettivi gestori di pacchetti.

Su Ubuntu Linux:

```
$ sudo apt-get install android-tools-adb
```

Su Fedora 18/19:

```
$ sudo yum install android-tools
```

Su macOS (Homebrew)

```
$ brew cask install android-platform-tools
```

Puoi verificare che `adb` funzioni collegando il dispositivo Android al computer tramite USB ed eseguendo il seguente comando:

```
$ adb devices
List of devices attached
31002535c90ef000    device
```

Se il dispositivo non compare, verifica di aver abilitato *USB debugging* sul dispositivo Android. Apri *Settings* sul dispositivo e cerca *Developer options* (o *Development*).

![Abilitare il debug USB](images/android/usb_debugging.png)
