---
title: Defold-Entwicklung für die macOS-Plattform
brief: Dieses Handbuch beschreibt, wie du Defold-Anwendungen für macOS erstellst und ausführst
---

# Entwicklung für macOS {#macos-development}

Die Entwicklung von Defold-Anwendungen für die macOS-Plattform ist unkompliziert und erfordert nur wenige besondere Überlegungen.

## Projekteinstellungen {#project-settings}

Die macOS-spezifische Konfiguration der Anwendung erfolgt im [Abschnitt macOS](/manuals/project-settings/#macos) der Einstellungsdatei *game.project*.

## Anwendungssymbol {#application-icon}

Das Anwendungssymbol für ein macOS-Spiel muss im Format .`icns` vorliegen. Du kannst eine `.icns`-Datei ganz einfach aus mehreren `.png`-Dateien erstellen, die als `.iconset` zusammengefasst sind. Befolge die [offizielle Anleitung zum Erstellen einer `.icns`-Datei](https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Optimizing/Optimizing.html). Hier ist eine kurze Zusammenfassung der erforderlichen Schritte:

* Erstelle einen Ordner für die Symbole, z. B. `game.iconset`
* Kopiere die Symboldateien in den erstellten Ordner:

    * `icon_16x16.png`
    * `icon_16x16@2x.png`
    * `icon_32x32.png`
    * `icon_32x32@2x.png`
    * `icon_128x128.png`
    * `icon_128x128@2x.png`
    * `icon_256x256.png`
    * `icon_256x256@2x.png`
    * `icon_512x512.png`
    * `icon_512x512@2x.png`

* Konvertiere den `.iconset`-Ordner in eine `.icns`-Datei. Verwende dazu das Kommandozeilenwerkzeug `iconutil`:

```
iconutil -c icns -o game.icns game.iconset
```

## Deine Anwendung veröffentlichen {#publishing-your-application}
Du kannst deine Anwendung im Mac App Store, über einen Store oder ein Portal eines Drittanbieters wie Steam oder itch.io oder selbst über eine Website veröffentlichen. Vor der Veröffentlichung musst du deine Anwendung für die Einreichung vorbereiten. Die folgenden Schritte sind unabhängig davon erforderlich, wie du die Anwendung verteilen möchtest:

1. Stelle sicher, dass alle dein Spiel ausführen können, indem du die Ausführungsberechtigungen hinzufügst (standardmäßig hat nur der Dateieigentümer Ausführungsberechtigungen):

```
$ chmod +x Game.app/Contents/MacOS/Game
```

2. Erstelle eine Berechtigungsdatei, die die von deinem Spiel benötigten Berechtigungen festlegt. Für die meisten Spiele reichen die folgenden Berechtigungen aus:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.allow-dyld-environment-variables</key>
    <true/>
  </dict>
</plist>
```

  * `com.apple.security.cs.allow-jit` - Gibt an, ob die Anwendung mit dem Flag MAP_JIT beschreibbaren und ausführbaren Speicher erstellen darf
  * `com.apple.security.cs.allow-unsigned-executable-memory` - Gibt an, ob die Anwendung beschreibbaren und ausführbaren Speicher ohne die Einschränkungen erstellen darf, die durch die Verwendung des Flags MAP_JIT auferlegt werden
  * `com.apple.security.cs.allow-dyld-environment-variables` - Gibt an, ob die Anwendung von Umgebungsvariablen des dynamischen Linkers beeinflusst werden darf, mit denen du Code in den Prozess deiner Anwendung einschleusen kannst

Einige Anwendungen benötigen möglicherweise zusätzliche Berechtigungen. Die Steamworks-Erweiterung benötigt diese zusätzliche Berechtigung:

```
<key>com.apple.security.cs.disable-library-validation</key>
<true/>
```

  * `com.apple.security.cs.disable-library-validation` - Gibt an, ob die Anwendung beliebige Plug-ins oder Frameworks laden darf, ohne dass eine Codesignierung erforderlich ist.

Alle Berechtigungen, die einer Anwendung erteilt werden können, sind in der offiziellen [Entwicklerdokumentation von Apple](https://developer.apple.com/documentation/bundleresources/entitlements) aufgeführt.

3. Signiere dein Spiel mit `codesign`:

```
$ codesign --force --sign "Developer ID Application: Company Name" --options runtime --deep --timestamp --entitlements entitlement.plist Game.app
```

## Außerhalb des Mac App Store veröffentlichen {#publishing-outside-the-mac-app-store}
Apple verlangt, dass sämtliche Software, die außerhalb des Mac App Store verteilt wird, von Apple notarisiert wird, damit sie unter macOS Catalina standardmäßig ausgeführt werden kann. In der [offiziellen Dokumentation](https://developer.apple.com/documentation/xcode/notarizing_macos_software_before_distribution/customizing_the_notarization_workflow) erfährst du, wie du die Notarisierung in eine skriptgesteuerte Build-Umgebung außerhalb von Xcode integrierst. Hier ist eine kurze Zusammenfassung der erforderlichen Schritte:

1. Befolge die obigen Schritte zum Hinzufügen von Berechtigungen und zum Signieren der Anwendung.

2. Verpacke dein Spiel als ZIP-Datei und lade es mit `altool` zur Notarisierung hoch.

```
$ xcrun altool --notarize-app
               --primary-bundle-id "com.acme.foobar"
               --username "AC_USERNAME"
               --password "@keychain:AC_PASSWORD"
               --asc-provider <ProviderShortname>
               --file Game.zip

altool[16765:378423] No errors uploading 'Game.zip'.
RequestUUID = 2EFE2717-52EF-43A5-96DC-0797E4CA1041
```

3. Prüfe den Status deiner Einreichung mithilfe der Anfrage-UUID, die vom Aufruf von `altool --notarize-app` zurückgegeben wurde:

```
$ xcrun altool --notarization-info 2EFE2717-52EF-43A5-96DC-0797E4CA1041
               -u "AC_USERNAME"
```

4. Warte, bis der Status `success` lautet, und füge dem Spiel das Notarisierungsticket hinzu:

```
$ xcrun stapler staple "Game.app"
```

5. Dein Spiel ist jetzt bereit zur Verteilung.

## Im Mac App Store veröffentlichen {#publishing-to-the-mac-app-store}
Der Ablauf zur Veröffentlichung im Mac App Store ist in der [Entwicklerdokumentation von Apple](https://developer.apple.com/macos/submit/) gut dokumentiert. Stelle sicher, dass du vor der Einreichung wie oben beschrieben Berechtigungen hinzufügst und die Anwendung mit `codesign` signierst.

Hinweis: Bei der Veröffentlichung im Mac App Store muss das Spiel nicht notarisiert werden.

:[Apple Privacy Manifest](../shared/apple-privacy-manifest.md)
