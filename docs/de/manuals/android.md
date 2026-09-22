---
title: Defold-Entwicklung für die Android-Plattform
brief: Dieses Handbuch beschreibt, wie du Defold-Anwendungen für Android-Geräte erstellst und darauf ausführst
---

# Android-Entwicklung {#android-development}

Auf Android-Geräten kannst du deine eigenen Apps frei ausführen. Es ist sehr einfach, eine Version deines Spiels zu erstellen und auf ein Android-Gerät zu kopieren. Dieses Handbuch erklärt die Schritte zur Bundle-Erstellung deines Spiels für Android. Während der Entwicklung wird häufig die Ausführung deines Spiels über die [Entwicklungs-App (development app)](/manuals/dev-app) bevorzugt, da du damit Inhalte und Code per Hot Reload direkt auf deinem Gerät aktualisieren kannst.

## Signieren für Android und Google Play {#android-and-google-play-signing-process}

Android verlangt, dass alle APKs mit einem Zertifikat digital signiert werden, bevor sie auf einem Gerät installiert oder aktualisiert werden. Wenn du Android App Bundles verwendest, musst du nur dein App Bundle signieren, bevor du es in die Play Console hochlädst. [Play App Signing](https://developer.android.com/studio/publish/app-signing#app-signing-google-play) übernimmt den Rest. Du kannst deine App aber auch manuell signieren, um sie bei Google Play oder anderen App-Stores hochzuladen oder außerhalb eines Stores zu verteilen.

Wenn du ein Android-Anwendungs-Bundle mit dem Defold-Editor oder dem [Befehlszeilenwerkzeug](/manuals/bob) erstellst, kannst du einen Schlüsselspeicher (keystore) mit deinem Zertifikat und Schlüssel sowie das Passwort des Schlüsselspeichers angeben. Diese werden zum Signieren deiner Anwendung verwendet. Wenn du diese Angaben weglässt, erzeugt Defold einen Debug-Schlüsselspeicher und verwendet ihn zum Signieren des Anwendungs-Bundles.

::: important
Du solltest deine Anwendung **niemals** bei Google Play hochladen, wenn sie mit einem Debug-Schlüsselspeicher signiert wurde. Verwende immer einen eigenen Schlüsselspeicher, den du selbst erstellt hast.
:::

## Einen Schlüsselspeicher erstellen {#creating-a-keystore}

::: sidenote
Defold verwendet einen Schlüsselspeicher für den Signierungsprozess unter Android. [Weitere Informationen findest du in diesem Forumsbeitrag](https://forum.defold.com/t/upcoming-change-to-the-android-build-pipeline/66084).
:::

Du kannst einen Schlüsselspeicher [mit Android Studio](https://developer.android.com/studio/publish/app-signing#generate-key) oder über ein Terminal bzw. die Eingabeaufforderung erstellen:

```bash
keytool -genkey -v -noprompt -dname "CN=John Smith, OU=Area 51, O=US Air Force, L=Unknown, ST=Nevada, C=US" -keystore mykeystore.keystore -storepass 5Up3r_53cR3t -alias myAlias -keyalg RSA -validity 9125
```

Dadurch wird eine Schlüsselspeicherdatei namens `mykeystore.keystore` erstellt, die einen Schlüssel und ein Zertifikat enthält. Der Zugriff auf Schlüssel und Zertifikat wird durch das Passwort `5Up3r_53cR3t` geschützt. Schlüssel und Zertifikat sind 25 Jahre (9125 Tage) gültig. Der erzeugte Schlüssel und das Zertifikat werden durch den Alias `myAlias` identifiziert.

::: important
Bewahre den Schlüsselspeicher und das zugehörige Passwort an einem sicheren Ort auf. Wenn du deine Anwendungen selbst signierst und bei Google Play hochlädst und der Schlüsselspeicher oder sein Passwort verloren geht, kannst du die Anwendung bei Google Play nicht mehr aktualisieren. Du kannst dies vermeiden, indem du Google Play App Signing verwendest und Google deine Anwendungen für dich signieren lässt.
:::


## Ein Android-Anwendungs-Bundle erstellen {#creating-an-android-application-bundle}

Mit dem Editor kannst du einfach ein eigenständiges Anwendungs-Bundle für dein Spiel erstellen. Vor der Bundle-Erstellung kannst du in der [Projekteinstellungsdatei](/manuals/project-settings/#android) *game.project* festlegen, welche Symbole für die App verwendet werden sollen, den Versionscode einstellen usw.

Wähle zum Erstellen eines Bundles im Menü <kbd>Project ▸ Bundle... ▸ Android Application...</kbd>.

Wenn der Editor automatisch zufällige Debug-Zertifikate erstellen soll, lasse die Felder *Keystore* und *Keystore password* leer:

![Android-Bundle signieren](images/android/sign_bundle.png)

Wenn du dein Bundle mit einem bestimmten Schlüsselspeicher signieren möchtest, gib *Keystore* und *Keystore password* an. Für *Keystore* wird die Dateierweiterung `.keystore` erwartet, während das Passwort in einer Textdatei mit der Erweiterung `.txt` gespeichert sein muss. Du kannst außerdem ein *Key password* angeben, wenn der Schlüssel im Schlüsselspeicher ein anderes Passwort als der Schlüsselspeicher selbst verwendet:

![Android-Bundle signieren](images/android/sign_bundle2.png)

Defold unterstützt die Erstellung von APK- und AAB-Dateien. Wähle APK oder AAB aus der Auswahlliste *Bundle Format*.

Klicke auf <kbd>Create Bundle</kbd>, sobald du die Einstellungen für das Anwendungs-Bundle konfiguriert hast. Anschließend wirst du aufgefordert, den Speicherort auf deinem Computer anzugeben, an dem das Bundle erstellt werden soll.

![Android-Anwendungspaketdatei](images/android/apk_file.png)

:[Build Variants](../shared/build-variants.md)

### Ein Android-Anwendungs-Bundle installieren {#installing-an-android-application-bundle}

#### Eine APK installieren {#installing-an-apk}

Eine *`.apk`*-Datei kann mit dem Werkzeug `adb` auf dein Gerät oder über die [Google Play-Entwicklerkonsole](https://play.google.com/apps/publish/) zu Google Play kopiert werden.

:[Android ADB](../shared/android-adb.md)

```
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
  pkg: /data/local/tmp/my_app.apk
Success
```

#### Eine APK mit dem Editor installieren {#installing-an-apk-using-editor}

Du kannst eine *`.apk`*-Datei mit den Kontrollkästchen „Install on connected device“ und „Launch installed app“ im Bundle-Dialogfeld des Editors installieren und starten:

![APK installieren und starten](images/android/install_and_launch.png)

Für diese Funktion muss *ADB* installiert und *USB debugging* auf dem verbundenen Gerät aktiviert sein. Wenn der Editor den Installationsort des ADB-Befehlszeilenwerkzeugs nicht erkennen kann, musst du ihn in [Preferences](/manuals/editor-preferences/#tools) angeben.

#### Eine AAB installieren {#installing-an-aab}

Eine *.aab*-Datei kann über die [Google Play-Entwicklerkonsole](https://play.google.com/apps/publish/) zu Google Play hochgeladen werden. Mit dem [Android bundletool](https://developer.android.com/studio/command-line/bundletool) kannst du außerdem aus einer *.aab*-Datei eine *`.apk`*-Datei erzeugen, um sie lokal zu installieren.

## Java-Code mit R8 verkleinern {#shrinking-java-code-with-r8}

R8 reduziert die Größe von Java-Code durch Verkleinerung, Optimierung und Verschleierung.

### R8 aktivieren {#enabling-r8}

Wähle `/builtins/manifests/android/dmengine.keep` unter **Android ▸ R8 Keep Rules** in *game.project* aus. Dadurch werden die Standardregeln von Defold direkt verwendet:

```ini
[android]
r8_keep_rules = /builtins/manifests/android/dmengine.keep
```

Stelle sicher, dass jede Erweiterung mit Java-Code eine `.keep`-Datei für die Klassen bereitstellt, die sie zur Laufzeit benötigt. Die Regeln der Erweiterungen werden beim Build mit den ausgewählten Projektregeln kombiniert. Teste nach dem Aktivieren von R8 einen Release-Build auf einem Gerät.

Wenn du **R8 Keep Rules** leer lässt, wird D8 ohne Verkleinerung verwendet. Beim Aktivieren von R8 wird der Build-Dienst für native Erweiterungen verwendet, auch für ein Projekt ohne native Erweiterungen.

### Regeln zu einer Erweiterung hinzufügen {#adding-rules-to-an-extension}

Die Keep-Regeln einer Erweiterung gehören in ihr Verzeichnis `manifests/android`, neben `build.gradle`. Unter [R8-Keep-Regeln für Android-Erweiterungen](/manuals/extensions/#r8-keep-rules-for-android) erfährst du, wie du eine Datei hinzufügst und die Java-Klassen der Erweiterung erhältst.

### Die Zuordnung verschleierter Namen aufbewahren {#keeping-the-obfuscation-mapping}

Aktiviere **Generate debug symbols** im Android-Bundle-Dialogfeld oder übergib `--with-symbols` an Bob, um die Datei `mapping.txt` von R8 aufzubewahren, wenn der Build eine erzeugt. Beispielsweise aus dem Projektverzeichnis:

```sh
java -jar bob.jar --platform arm64-android --variant release \
  --archive --with-symbols --bundle-output build/android \
  resolve build bundle
```

Die Zuordnung wird als `<binary-name>.apk.symbols/mapping.txt` neben der erzeugten APK oder AAB gespeichert. Bei dem Projekttitel `My Game` erzeugt der obige Befehl beispielsweise `build/android/MyGame/MyGame.apk.symbols/mapping.txt`.

Bewahre die Zuordnungsdatei zusammen mit genau der Release-Version auf, aus der sie stammt. Sie ordnet verschleierten Java-Namen wieder ihre ursprünglichen Namen zu, um Stacktraces auswerten zu können. Eine Zuordnung aus einem anderen Build kann falsche Ergebnisse liefern.

## Berechtigungen {#permissions}

Die Defold-Engine benötigt verschiedene Berechtigungen, damit alle Engine-Funktionen arbeiten können. Die Berechtigungen werden in der Datei `AndroidManifest.xml` definiert, die in der [Projekteinstellungsdatei](/manuals/project-settings/#android) *game.project* angegeben ist. Weitere Informationen zu Android-Berechtigungen findest du in der [offiziellen Dokumentation](https://developer.android.com/guide/topics/permissions/overview). Im Standardmanifest werden die folgenden Berechtigungen angefordert:

### android.permission.INTERNET und android.permission.ACCESS_NETWORK_STATE (Schutzstufe: normal) {#androidpermissioninternet-and-androidpermissionaccess_network_state-protection-level-normal}
Erlaubt Anwendungen, *Netzwerk-Sockets* zu öffnen und auf Informationen über Netzwerke zuzugreifen. Diese Berechtigungen werden für den Internetzugriff benötigt. ([Offizielle Android-Dokumentation](https://developer.android.com/reference/android/Manifest.permission#INTERNET)) und ([Offizielle Android-Dokumentation](https://developer.android.com/reference/android/Manifest.permission#ACCESS_NETWORK_STATE)).

### android.permission.WAKE_LOCK (Schutzstufe: normal) {#androidpermissionwake_lock-protection-level-normal}
Erlaubt die Verwendung von PowerManager-WakeLocks, um zu verhindern, dass der Prozessor in den Ruhezustand wechselt oder der Bildschirm gedimmt wird. Diese Berechtigung wird benötigt, um das Gerät beim Empfang einer Push-Benachrichtigung vorübergehend am Wechsel in den Ruhezustand zu hindern. ([Offizielle Android-Dokumentation](https://developer.android.com/reference/android/Manifest.permission#WAKE_LOCK))


## AndroidX verwenden {#using-androidx}
AndroidX ist eine wesentliche Verbesserung gegenüber der ursprünglichen Android Support Library, die nicht mehr gepflegt wird. AndroidX-Pakete ersetzen die Support Library vollständig, indem sie denselben Funktionsumfang und neue Bibliotheken bereitstellen. Die meisten Android-Erweiterungen im [Asset Portal](/assets) unterstützen AndroidX. Wenn du AndroidX nicht verwenden möchtest, kannst du es ausdrücklich zugunsten der alten Android Support Library deaktivieren, indem du `Use Android Support Lib` im [Anwendungsmanifest](https://defold.com/manuals/app-manifest/) aktivierst.

![](images/android/enable_supportlibrary.png)

## FAQ
:[Android FAQ](../shared/android-faq.md)
