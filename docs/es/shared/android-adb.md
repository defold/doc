La herramienta de línea de comando `adb` es un programa fácil de usar y versátil que se utiliza para interactuar con dispositivos Android. Puedes descargar e instalar `adb` como parte de Android SDK Platform-Tools, para Mac, Linux o Windows.

Descarga Android SDK Platform-Tools desde: https://developer.android.com/studio/releases/platform-tools. Encontrarás la herramienta *adb* en */platform-tools/*. Como alternativa, se pueden instalar paquetes específicos de cada plataforma mediante los respectivos gestores de paquetes.

En Ubuntu Linux:

```
$ sudo apt-get install android-tools-adb
```

En Fedora 18/19:

```
$ sudo yum install android-tools
```

En macOS (Homebrew)

```
$ brew cask install android-platform-tools
```

Puedes verificar que `adb` funciona conectando tu dispositivo Android a tu computadora mediante USB y ejecutando el siguiente comando:

```
$ adb devices
List of devices attached
31002535c90ef000    device
```

Si tu dispositivo no aparece, verifica que hayas habilitado *USB debugging* en el dispositivo Android. Abre *Settings* del dispositivo y busca *Developer options* (o *Development*).

![Habilitar USB debugging](images/android/usb_debugging.png)
