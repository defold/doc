`adb` komut satırı aracı, Android cihazlarıyla etkileşim kurmak için kullanılan, kullanımı kolay ve çok yönlü bir programdır. `adb` aracını Mac, Linux veya Windows için Android SDK Platform-Tools paketinin bir parçası olarak indirip kurabilirsiniz.

Android SDK Platform-Tools paketini şu adresten indirin: https://developer.android.com/studio/releases/platform-tools. *adb* aracını */platform-tools/* dizininde bulabilirsiniz. Alternatif olarak, platforma özgü paketler ilgili paket yöneticileri aracılığıyla kurulabilir.

Ubuntu Linux üzerinde:

```
$ sudo apt-get install android-tools-adb
```

Fedora 18/19 üzerinde:

```
$ sudo yum install android-tools
```

macOS üzerinde (Homebrew)

```
$ brew cask install android-platform-tools
```

Android cihazınızı USB aracılığıyla bilgisayarınıza bağlayıp aşağıdaki komutu çalıştırarak `adb` aracının çalıştığını doğrulayabilirsiniz:

```
$ adb devices
List of devices attached
31002535c90ef000    device
```

Cihazınız görünmüyorsa Android cihazında *USB debugging* seçeneğini etkinleştirdiğinizi doğrulayın. Cihazın *Settings* bölümünü açın ve *Developer options* (veya *Development*) seçeneğini bulun.

![USB hata ayıklamayı etkinleştirme](images/android/usb_debugging.png)
