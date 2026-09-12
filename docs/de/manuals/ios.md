---
title: Entwicklung mit Defold für die iOS-Plattform
brief: Dieses Handbuch erklärt, wie du in Defold Spiele und Apps für iOS-Geräte erstellst und ausführst.
---

# Entwicklung für iOS {#ios-development}

::: sidenote
Das Erstellen eines Bundles für iOS ist nur in der Mac-Version des Defold-Editors verfügbar.
:::

iOS verlangt, dass _jede_ App, die du erstellst und auf deinem Telefon oder Tablet ausführen möchtest, mit einem von Apple ausgestellten Zertifikat und Bereitstellungsprofil (provisioning profile) signiert werden _muss_. Dieses Handbuch erläutert die Schritte zur Erstellung eines Bundles deines Spiels für iOS. Während der Entwicklung ist es oft vorzuziehen, dein Spiel über die [Entwicklungs-App](/manuals/dev-app) auszuführen, da du damit Inhalte und Code per Hot Reload direkt auf dein Gerät laden kannst.

## Apples Verfahren zur Codesignierung {#apples-code-signing-process}

Die Sicherheit von iOS-Apps setzt sich aus mehreren Bestandteilen zusammen. Zugang zu den benötigten Werkzeugen erhältst du, indem du dich für das [iOS Developer Program von Apple](https://developer.apple.com/programs/) anmeldest. Rufe nach deiner Anmeldung das [Developer Member Center von Apple](https://developer.apple.com/membercenter/index.action) auf.

![Apple Member Center](images/ios/apple_member_center.png)

Der Bereich *Certificates, Identifiers & Profiles* enthält alle Werkzeuge, die du benötigst. Hier kannst du Folgendes erstellen, löschen und bearbeiten:

Certificates
: Von Apple ausgestellte kryptografische Zertifikate, die dich als Entwickler identifizieren. Du kannst Entwicklungs- oder Produktionszertifikate erstellen. Mit Entwicklungszertifikaten kannst du bestimmte Funktionen wie den Mechanismus für In-App-Käufe in einer Sandbox-Testumgebung testen. Produktionszertifikate werden verwendet, um die fertige App für das Hochladen in den App Store zu signieren. Du benötigst ein Zertifikat, um Apps zu signieren, bevor du sie zum Testen auf dein Gerät übertragen kannst.

Identifiers
: Kennungen für verschiedene Verwendungszwecke. Du kannst Kennungen mit Platzhaltern registrieren (z. B. `some.prefix.*`), die sich für mehrere Apps verwenden lassen. App-IDs können Informationen zu Anwendungsdiensten enthalten, etwa dazu, ob die App die Integration von Passbook, Game Center usw. aktiviert. Solche App-IDs können keine Kennungen mit Platzhaltern sein. Damit Anwendungsdienste funktionieren, muss die *Bundle-ID* deiner Anwendung mit der App-ID übereinstimmen.

Devices
: Jedes Entwicklungsgerät muss mit seiner UDID (Unique Device IDentifier, siehe unten) registriert werden.

Provisioning Profiles
: Bereitstellungsprofile verknüpfen Zertifikate mit App-IDs und einer Liste von Geräten. Sie legen fest, welche App von welchem Entwickler auf welchen Geräten vorhanden sein darf.

Zum Signieren deiner Spiele und Apps in Defold benötigst du ein gültiges Zertifikat und ein gültiges Bereitstellungsprofil.

::: sidenote
Einige der Aktionen auf der Startseite des Member Center kannst du auch in der Entwicklungsumgebung Xcode ausführen---sofern du sie installiert hast.
:::

Gerätekennung (UDID)
: Die UDID eines iOS-Geräts findest du, indem du das Gerät per WLAN oder Kabel mit einem Computer verbindest. Öffne Xcode und wähle <kbd>Window ▸ Devices and Simulators</kbd>. Wenn du dein Gerät auswählst, werden die Seriennummer und die Kennung angezeigt.

  ![Geräte in Xcode](images/ios/xcode_devices.png)

  Wenn du Xcode nicht installiert hast, kannst du die Kennung in iTunes finden. Klicke auf das Gerätesymbol und wähle dein Gerät aus.

  ![Geräte in iTunes](images/ios/itunes_devices.png)

  1. Suche auf der Seite *Summary* nach *Serial Number*.
  2. Klicke einmal auf *Serial Number*, damit das Feld zu *UDID* wechselt. Wenn du wiederholt klickst, werden verschiedene Informationen zum Gerät angezeigt. Klicke einfach weiter, bis *UDID* erscheint.
  3. Klicke mit der rechten Maustaste auf die lange UDID-Zeichenfolge und wähle <kbd>Copy</kbd>, um die Kennung in die Zwischenablage zu kopieren. So kannst du sie bei der Registrierung des Geräts im Developer Member Center von Apple bequem in das UDID-Feld einfügen.

## Mit einem kostenlosen Apple-Entwicklerkonto entwickeln {#developing-using-a-free-apple-developer-account}

Seit Xcode 7 kann jeder Xcode installieren und kostenlos direkt auf einem Gerät entwickeln. Du musst dich nicht für das iOS Developer Program anmelden. Stattdessen stellt Xcode automatisch ein Zertifikat für dich als Entwickler (1 Jahr gültig) und ein Bereitstellungsprofil für deine App (eine Woche gültig) auf deinem jeweiligen Gerät aus.

1. Verbinde dein Gerät.
2. Installiere Xcode.
3. Füge Xcode ein neues Konto hinzu und melde dich mit deiner Apple-ID an.
4. Erstelle ein neues Projekt. Die einfachste Vorlage `Single View App` eignet sich dafür.
5. Wähle dein `Team` (wird automatisch für dich erstellt) und gib der App eine Bundle-ID.

::: important
Notiere dir die Bundle-ID, da du dieselbe Bundle-ID in deinem Defold-Projekt verwenden musst.
:::

6. Stelle sicher, dass Xcode ein *Provisioning Profile* und ein *Signing Certificate* für die App erstellt hat.

   ![](images/ios/xcode_certificates.png)

7. Erstelle den Build der App auf deinem Gerät. Beim ersten Mal fordert Xcode dich auf, den Entwicklermodus zu aktivieren, und bereitet das Gerät mit Debugger-Unterstützung vor. Dies kann eine Weile dauern.
8. Wenn du geprüft hast, dass die App funktioniert, suche sie auf deinem Datenträger. Den Speicherort des Builds findest du im Build-Bericht im `Report Navigator`.

   ![](images/ios/app_location.png)

9. Suche die App, klicke mit der rechten Maustaste darauf und wähle <kbd>Show Package Contents</kbd>.

   ![](images/ios/app_contents.png)

10. Kopiere die Datei `embedded.mobileprovision` an einen Ort auf deinem Laufwerk, an dem du sie wiederfindest.

   ![](images/ios/free_provisioning.png)

Mit dieser Bereitstellungsdatei und deiner Identität für die Codesignierung kannst du eine Woche lang Apps in Defold signieren.

Wenn die Gültigkeit des Bereitstellungsprofils abläuft, musst du den Build der App erneut in Xcode erstellen und dir wie oben beschrieben eine neue temporäre Bereitstellungsdatei beschaffen.

## Ein iOS-Anwendungsbundle erstellen {#creating-an-ios-application-bundle}

Sobald du die Identität für die Codesignierung und das Bereitstellungsprofil hast, kannst du im Editor ein eigenständiges Anwendungsbundle für dein Spiel erstellen. Wähle dazu im Menü <kbd>Project ▸ Bundle... ▸ iOS Application...</kbd>.

![iOS-Bundle signieren](images/ios/sign_bundle.png)

Wähle deine Identität für die Codesignierung, suche deine mobile Bereitstellungsdatei und wähle die Variante (Debug oder Release). Du kannst optional das Kontrollkästchen `Sign application` deaktivieren, um die Signierung zu überspringen und später manuell zu signieren. Aktiviere `Simulator`, um ein `arm64_sim-ios`-Bundle für den iOS-Simulator anstelle eines Gerätebundles zu erstellen.

::: important
Simulator-Bundles laufen nur im iOS-Simulator auf Macs mit Apple Silicon. Sie verwenden weder eine Signierungsidentität noch ein Bereitstellungsprofil. Deshalb sind die Optionen zum Signieren, Installieren und Starten deaktiviert, wenn `Simulator` aktiviert ist. Installiere das Bundle wie unten beschrieben mit `xcrun simctl`.
:::

Klicke auf *Create Bundle*. Anschließend wirst du aufgefordert, den Speicherort auf deinem Computer anzugeben, an dem das Bundle erstellt werden soll.

![iOS-Anwendungsbundle im IPA-Format](images/ios/ipa_file.png){.left}

Das Symbol für die App, das Storyboard für den Startbildschirm und weitere Angaben legst du in der Projekteinstellungsdatei *game.project* im [Abschnitt iOS](/manuals/project-settings/#ios) fest.

### Benutzerdefinierte Info.plist und Erkennung lokaler Ziele {#custom-infoplist-and-local-target-discovery}

Die integrierte iOS-Datei `Info.plist` enthält den Bonjour-Dienst und die Beschreibung der Nutzung des lokalen Netzwerks, die für die automatische Zielerkennung im Editor bei Builds erforderlich sind, die keine Release-Builds sind. Eine benutzerdefinierte `Info.plist` ersetzt dieses integrierte Basismanifest. Wenn du für einen Debug-Build ein benutzerdefiniertes Manifest verwendest und Zielerkennung, Profiling, Hot Reload oder die Übertragung von Protokollen über das lokale Netzwerk benötigst, füge diese Einträge hinzu:

```xml
{{^variant_release}}
<key>NSBonjourServices</key>
<array>
    <string>_defold._tcp</string>
</array>
<key>NSLocalNetworkUsageDescription</key>
<string>Discover Defold targets on the local network.</string>
{{/variant_release}}
```

Die Mustache-Bedingung verhindert, dass die Einträge zur Erkennung in Release-Bundles enthalten sind. iOS zeigt den Text zur Beschreibung der Nutzung dem Benutzer an; du kannst ihn anpassen oder lokalisieren. Entferne die Bedingung nur, wenn die Release-Anwendung selbst denselben Bonjour-Dienst und dieselbe Funktionalität im lokalen Netzwerk verwendet.

:[Build Variants](../shared/build-variants.md)

## Ein Bundle auf einem verbundenen iPhone installieren und starten {#installing-and-launching-bundle-on-a-connected-iphone}

Du kannst das erstellte Bundle mit den Kontrollkästchen `Install on connected device` und `Launch installed app` im Bundle-Dialogfeld des Editors installieren und starten:

![iOS-Bundle installieren und starten](images/ios/install_and_launch.png)

Damit diese Funktion verfügbar ist, muss das Kommandozeilenwerkzeug [ios-deploy](https://github.com/ios-control/ios-deploy) installiert sein. Am einfachsten installierst du es mit Homebrew:
```
$ brew install ios-deploy
```

Wenn der Editor den Installationsort des Werkzeugs ios-deploy nicht erkennen kann, musst du ihn in den [Editoreinstellungen](/manuals/editor-preferences/#tools) angeben. 

### Ein Storyboard erstellen {#creating-a-storyboard}

Eine Storyboard-Datei erstellst du mit Xcode. Starte Xcode und erstelle ein neues Projekt. Wähle iOS und Single View App:

![Projekt erstellen](images/ios/xcode_create_project.png)

Klicke auf Next und fahre mit der Konfiguration deines Projekts fort. Gib einen Product Name ein:

![Projekteinstellungen](images/ios/xcode_storyboard_create_project_settings.png)

Klicke auf Create, um den Vorgang abzuschließen. Dein Projekt ist nun erstellt, und wir können mit der Erstellung des Storyboards fortfahren:

![Die Projektansicht](images/ios/xcode_storyboard_project_view.png)

Ziehe ein Bild in das Projekt und lege es dort ab, um es zu importieren. Wähle anschließend `Assets.xcassets` und lege das Bild in `Assets.xcassets` ab:

![Bild hinzufügen](images/ios/xcode_storyboard_add_image.png)

Öffne `LaunchScreen.storyboard` und klicke auf die Plus-Schaltfläche (<kbd>+</kbd>). Gib `imageview` in das Dialogfeld ein, um die ImageView-Komponente zu finden.

![Bildansicht hinzufügen](images/ios/xcode_storyboard_add_imageview.png)

Ziehe die Komponente Image View auf das Storyboard:

![Zum Storyboard hinzufügen](images/ios/xcode_storyboard_add_imageview_to_storyboard.png)

Wähle aus der Auswahlliste Image das Bild aus, das du zuvor zu `Assets.xcassets` hinzugefügt hast:

![](images/ios/xcode_storyboard_select_image.png)

Positioniere das Bild und nimm alle weiteren gewünschten Anpassungen vor. Füge beispielsweise ein Label oder ein anderes UI-Element hinzu. Wenn du fertig bist, setze das aktive Schema auf **Any iOS Device (arm64)** (oder **Generic iOS Device**) und wähle **Product ▸ Build**. Defold unterstützt iOS 15.0 und neuer auf 64-Bit-Geräten. Belasse daher das Bereitstellungsziel bei 15.0 oder neuer. Warte, bis der Build-Vorgang abgeschlossen ist.

Wenn du Bilder im Storyboard verwendest, werden sie nicht automatisch in deine `LaunchScreen.storyboardc` aufgenommen. Verwende das Feld `Bundle Resources` in *game.project*, um Ressourcen einzuschließen.
Erstelle beispielsweise den Ordner `LaunchScreen` im Defold-Projekt und darin den Ordner `ios` (der Ordner `ios` ist erforderlich, damit diese Dateien nur in iOS-Bundles enthalten sind). Lege deine Dateien dann in `LaunchScreen/ios/` ab. Füge diesen Pfad in `Bundle Resources` hinzu.

![](images/ios/bundle_res.png)

Im letzten Schritt kopierst du die kompilierte Datei `LaunchScreen.storyboardc` in dein Defold-Projekt. Öffne im Finder den folgenden Speicherort und kopiere die Datei `LaunchScreen.storyboardc` in dein Defold-Projekt:

    /Library/Developer/Xcode/DerivedData/YOUR-PRODUCT-NAME-cbqnwzfisotwygbybxohrhambkjy/Build/Intermediates.noindex/YOUR-PRODUCT-NAME.build/Debug-iphonesimulator/YOUR-PRODUCT-NAME.build/Base.lproj/LaunchScreen.storyboardc

::: sidenote
Der Forennutzer Sergey Lerg hat [ein Video-Tutorial zum Ablauf](https://www.youtube.com/watch?v=6jU8wGp3OwA&feature=emb_logo) zusammengestellt.
:::

Sobald du die Storyboard-Datei hast, kannst du in *game.project* darauf verweisen.


### Einen Asset-Katalog für Symbole erstellen {#creating-an-icon-asset-catalog}

Ein Asset-Katalog ist Apples bevorzugte Methode zur Verwaltung der Symbole deiner Anwendung. Tatsächlich ist dies die einzige Möglichkeit, das im App-Store-Eintrag verwendete Symbol bereitzustellen. Du erstellst einen Asset-Katalog genauso wie ein Storyboard mit Xcode. Starte Xcode und erstelle ein neues Projekt. Wähle iOS und Single View App:

![Projekt erstellen](images/ios/xcode_create_project.png)

Klicke auf Next und fahre mit der Konfiguration deines Projekts fort. Gib einen Product Name ein:

![Projekteinstellungen](images/ios/xcode_icons_create_project_settings.png)

Klicke auf Create, um den Vorgang abzuschließen. Dein Projekt ist nun erstellt, und wir können mit der Erstellung des Asset-Katalogs fortfahren:

![Die Projektansicht](images/ios/xcode_icons_project_view.png)

Ziehe Bilder in die leeren Felder für die verschiedenen unterstützten Symbolgrößen und lege sie dort ab:

![Symbole hinzufügen](images/ios/xcode_icons_add_icons.png)

::: sidenote
Füge keine Symbole für Notifications, Settings oder Spotlight hinzu.
:::

Wenn du fertig bist, setze das aktive Schema auf `Build -> Any iOS Device (arm64)` (oder `Generic iOS Device`) und wähle <kbd>Product</kbd> -> <kbd>Build</kbd>. Warte, bis der Build-Vorgang abgeschlossen ist.

::: sidenote
Stelle sicher, dass du den Build für `Any iOS Device (arm64)` oder `Generic iOS Device` erstellst. Andernfalls erhältst du beim Hochladen deines Builds den Fehler `ERROR ITMS-90704`.
:::

![Projekt erstellen](images/ios/xcode_icons_build.png)

Im letzten Schritt kopierst du die kompilierte Datei `Assets.car` in dein Defold-Projekt. Öffne im Finder den folgenden Speicherort und kopiere die Datei `Assets.car` in dein Defold-Projekt:

    /Library/Developer/Xcode/DerivedData/YOUR-PRODUCT-NAME-cbqnwzfisotwygbybxohrhambkjy/Build/Products/Debug-iphoneos/Icons.app/Assets.car

Sobald du die Asset-Katalogdatei hast, kannst du in *game.project* auf sie und die Symbole verweisen:

![Symbol und Asset-Katalog zu game.project hinzufügen](images/ios/defold_icons_game_project.png)

::: sidenote
Auf das App-Store-Symbol muss in *game.project* nicht verwiesen werden. Es wird beim Hochladen in iTunes Connect automatisch aus der Datei `Assets.car` extrahiert.
:::


## Ein iOS-Anwendungsbundle installieren {#installing-an-ios-application-bundle}

Der Editor schreibt eine Datei mit der Erweiterung *.ipa*, die ein iOS-Anwendungsbundle ist. Um die Datei auf deinem Gerät zu installieren, kannst du eines der folgenden Werkzeuge verwenden:

* Xcode über das Fenster `Devices and Simulators`
* das Kommandozeilenwerkzeug [`ios-deploy`](https://github.com/ios-control/ios-deploy)
* [`Apple Configurator 2`](https://apps.apple.com/us/app/apple-configurator-2/) aus dem macOS App Store
* iTunes

Du kannst auch das Kommandozeilenwerkzeug `xcrun simctl` verwenden, um mit den über Xcode verfügbaren iOS-Simulatoren zu arbeiten:

```
# show a list of available devices
xcrun simctl list

# boot an iPhone X simulator
xcrun simctl boot "iPhone X"

# install your.app to a booted simulator
xcrun simctl install booted your.app

# launch the simulator
open /Applications/Xcode.app/Contents/Developer/Applications/Simulator.app
```

:[Apple Privacy Manifest](../shared/apple-privacy-manifest.md)


## Angaben zur Einhaltung von Exportvorschriften {#export-compliance-information}

Wenn du dein Spiel beim App Store einreichst, wirst du aufgefordert, Angaben zur Einhaltung von Exportvorschriften im Hinblick auf die Verwendung von Verschlüsselung in deinem Spiel zu machen. [Apple erklärt, warum dies erforderlich ist](https://developer.apple.com/documentation/security/complying_with_encryption_export_regulations):

„Wenn du deine App bei TestFlight oder dem App Store einreichst, lädst du sie auf einen Server in den Vereinigten Staaten hoch. Wenn du deine App außerhalb der USA oder Kanadas vertreibst, unterliegt sie den US-Exportgesetzen, unabhängig davon, wo deine juristische Person ihren Sitz hat. Wenn deine App Verschlüsselung verwendet, darauf zugreift, sie enthält, implementiert oder integriert, gilt dies als Export von Verschlüsselungssoftware. Damit unterliegt deine App den US-Exportvorschriften sowie den Einfuhrvorschriften der Länder, in denen du deine App vertreibst.“

Die Defold-Game-Engine verwendet Verschlüsselung für die folgenden Zwecke:

* Aufrufe über sichere Kanäle (z. B. HTTPS und SSL)
* Urheberrechtlicher Schutz von Lua-Code (um eine Vervielfältigung zu verhindern)

Diese Verwendungen von Verschlüsselung in der Defold-Engine sind nach dem Recht der Vereinigten Staaten und der Europäischen Union von der Pflicht zur Vorlage von Dokumenten zur Einhaltung von Exportvorschriften ausgenommen. Die meisten Defold-Projekte bleiben davon ausgenommen. Durch das Hinzufügen anderer kryptografischer Verfahren kann sich dieser Status jedoch ändern. Es liegt in deiner Verantwortung, sicherzustellen, dass dein Projekt die Anforderungen dieser Gesetze und die Regeln des App Store erfüllt. Weitere Informationen findest du in Apples [Übersicht zur Einhaltung von Exportvorschriften](https://help.apple.com/app-store-connect/#/dev88f5c7bf9).

Wenn du davon ausgehst, dass dein Projekt ausgenommen ist, setze den Schlüssel [`ITSAppUsesNonExemptEncryption`](https://developer.apple.com/documentation/bundleresources/information-property-list/itsappusesnonexemptencryption) in der Datei `Info.plist` des Projekts auf `False`. Weitere Einzelheiten findest du unter [Anwendungsmanifeste](/manuals/extensions-manifest-merge-tool).

## FAQ
:[iOS FAQ](../shared/ios-faq.md)
