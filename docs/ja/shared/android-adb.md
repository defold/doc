`adb` コマンドラインツールは、Android デバイスとやり取りするための、使いやすく多用途なプログラムです。Mac、Linux、Windows 向けの Android SDK Platform-Tools の一部として、`adb` をダウンロードしてインストールできます。

Android SDK Platform-Tools を https://developer.android.com/studio/releases/platform-tools からダウンロードします。*adb* ツールは */platform-tools/* にあります。また、各プラットフォーム向けのパッケージを、それぞれのパッケージマネージャーからインストールすることもできます。

Ubuntu Linux の場合:

```
$ sudo apt-get install android-tools-adb
```

Fedora 18/19 の場合:

```
$ sudo yum install android-tools
```

macOS（Homebrew）の場合

```
$ brew cask install android-platform-tools
```

Android デバイスを USB でコンピューターに接続し、次のコマンドを実行すると、`adb` が動作することを確認できます。

```
$ adb devices
List of devices attached
31002535c90ef000    device
```

デバイスが表示されない場合は、Android デバイスで *USB debugging* が有効になっていることを確認します。デバイスの *Settings* を開き、*Developer options*（または *Development*）を探します。

![USB デバッグを有効にする](images/android/usb_debugging.png)
