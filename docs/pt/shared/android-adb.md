A ferramenta de linha de comando `adb` é um programa fácil de usar e versátil usado para interagir com dispositivos Android. Você pode baixar e instalar o `adb` como parte do Android SDK Platform-Tools, para macOS, Linux ou Windows.

Baixe o Android SDK Platform-Tools em: https://developer.android.com/studio/releases/platform-tools. Você encontrará a ferramenta *adb* em */platform-tools/*. Como alternativa, pacotes específicos de plataforma podem ser instalados pelos respectivos gerenciadores de pacotes.

No Ubuntu Linux:

```
$ sudo apt-get install android-tools-adb
```

No Fedora 18/19:

```
$ sudo yum install android-tools
```

No macOS (Homebrew)

```
$ brew cask install android-platform-tools
```

Você pode verificar se o `adb` funciona conectando seu dispositivo Android ao computador via USB e executando o seguinte comando:

```
$ adb devices
List of devices attached
31002535c90ef000    device
```

Se o seu dispositivo não aparecer, verifique se você habilitou *USB debugging* no dispositivo Android. Abra *Settings* no dispositivo e procure por *Developer options* (ou *Development*).

![Habilitar depuração USB](images/android/usb_debugging.png)
