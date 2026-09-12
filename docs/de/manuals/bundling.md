---
title: Ein Anwendungs-Bundle erstellen
brief: Dieses Handbuch beschreibt, wie du ein Anwendungs-Bundle erstellst.
---

# Ein Anwendungs-Bundle erstellen {#bundling-an-application}

Während du deine Anwendung entwickelst, solltest du dir angewöhnen, das Spiel so oft wie möglich auf den Zielplattformen zu testen. So erkennst du Leistungsprobleme früh im Entwicklungsprozess, wenn sie sich noch wesentlich leichter beheben lassen. Es wird außerdem empfohlen, auf allen Zielplattformen zu testen, um Unterschiede etwa bei Shadern zu finden. Bei der Entwicklung für Mobilgeräte kannst du die [Entwicklungs-App für Mobilgeräte](/manuals/dev-app/) verwenden, um Inhalte an die App zu übertragen, statt jedes Mal ein vollständiges Bundle erstellen und die App deinstallieren und erneut installieren zu müssen.

Du kannst direkt im Defold-Editor ein Anwendungs-Bundle für alle von Defold unterstützten Plattformen erstellen, ohne externe Werkzeuge zu benötigen. Mit unseren Kommandozeilenwerkzeugen kannst du Bundles auch über die Kommandozeile erstellen. Für die Erstellung eines Anwendungs-Bundles ist eine Netzwerkverbindung erforderlich, wenn dein Projekt eine oder mehrere [native Erweiterungen (native extensions)](/manuals/extensions) enthält.

## Ein Bundle im Editor erstellen {#bundling-from-within-the-editor}

Du erstellst ein Anwendungs-Bundle über die Option Bundle im Menü Project:

![](images/bundling/bundle_menu.png)

Wenn du eine der Menüoptionen auswählst, öffnet sich das Dialogfeld Bundle für die jeweilige Plattform.

### Build-Berichte {#build-reports}

Beim Erstellen eines Bundles für dein Spiel kannst du einen Build-Bericht erstellen lassen. Damit verschaffst du dir einen guten Überblick über die Größe aller Assets, die in deinem Spiel-Bundle enthalten sind. Aktiviere dazu beim Erstellen des Bundles einfach das Kontrollkästchen *Generate build report*.

![Build-Bericht](images/profiling/build_report.png)

Weitere Informationen zu Build-Berichten findest du im [Handbuch zum Profiling](/manuals/profiling/#build-reports).

### Android

Das Erstellen eines Android-Anwendungs-Bundles (.apk-Datei) wird im [Android-Handbuch](/manuals/android/#creating-an-android-application-bundle) beschrieben.

### iOS

Das Erstellen eines iOS-Anwendungs-Bundles (.ipa-Datei) wird im [iOS-Handbuch](/manuals/ios/#creating-an-ios-application-bundle) beschrieben.

### macOS

Das Erstellen eines macOS-Anwendungs-Bundles (.app-Datei) wird im [macOS-Handbuch](/manuals/macos) beschrieben.

### Linux

Das Erstellen eines Linux-Anwendungs-Bundles erfordert keine besondere Einrichtung und keine optionale plattformspezifische Konfiguration in der Datei *game.project* für die [Projekteinstellungen](/manuals/project-settings/).

### Windows

Das Erstellen eines Windows-Anwendungs-Bundles (.exe-Datei) wird im [Windows-Handbuch](/manuals/windows) beschrieben.

### HTML5

Das Erstellen eines HTML5-Anwendungs-Bundles sowie optionale Einrichtungsschritte werden im [HTML5-Handbuch](/manuals/html5/#creating-html5-bundle) beschrieben.

#### Facebook Instant Games

Du kannst eine spezielle Version eines HTML5-Anwendungs-Bundles für Facebook Instant Games erstellen. Dieser Vorgang wird im [Handbuch zu Facebook Instant Games](/manuals/instant-games/) beschrieben.

## Ein Bundle über die Kommandozeile erstellen {#bundling-from-the-command-line}

Der Editor verwendet unser Kommandozeilenwerkzeug [Bob](/manuals/bob/), um das Anwendungs-Bundle zu erstellen.

Bei der täglichen Entwicklung deiner Anwendung erstellst du Builds und Bundles wahrscheinlich im Defold-Editor. Unter anderen Umständen möchtest du Anwendungs-Bundles möglicherweise automatisch erzeugen, etwa Builds für alle Zielplattformen in einem Durchlauf bei der Veröffentlichung einer neuen Version oder nächtliche Builds der neuesten Spielversion, vielleicht in einer CI-Umgebung. Mit dem [Kommandozeilenwerkzeug Bob](/manuals/bob/) kannst du Builds und Bundles einer Anwendung außerhalb des üblichen Arbeitsablaufs im Editor erstellen.

## Der Aufbau eines Bundles {#the-bundle-layout}

Der logische Aufbau eines Bundles sieht folgendermaßen aus:

![](images/bundling/bundle_schematic_01.png)

Ein Bundle wird in einem Ordner ausgegeben. Je nach Plattform kann dieser Ordner außerdem als ZIP-Archiv in einer `.apk` oder `.ipa` gespeichert werden.
Der Inhalt des Ordners hängt von der Plattform ab.

Neben den ausführbaren Dateien stellt unser Vorgang zur Bundle-Erstellung auch die für die Plattform erforderlichen Assets zusammen (z. B. die .xml-Ressourcendateien für Android).

Mit der Einstellung [bundle_resources](https://defold.com/manuals/project-settings/#bundle-resources) kannst du Assets festlegen, die unverändert in das Bundle aufgenommen werden sollen.
Das kannst du für jede Plattform einzeln steuern.

Die Spiel-Assets befinden sich in der Datei `game.arcd` und werden einzeln mit LZ4 komprimiert.
Mit der Einstellung [custom_resources](https://defold.com/manuals/project-settings/#custom-resources) kannst du Assets festlegen, die (komprimiert) in die Datei `game.arcd` aufgenommen werden sollen.
Auf diese Assets kannst du mit der Funktion [`sys.load_resource()`](https://defold.com/ref/sys/#sys.load_resource) zugreifen.

## Release- und Debug-Bundles {#release-vs-debug}

Beim Erstellen eines Anwendungs-Bundles kannst du zwischen einem Debug- und einem Release-Bundle wählen. Die Unterschiede zwischen den beiden Bundles sind gering, du solltest sie jedoch beachten:

* Release-Builds enthalten standardmäßig keinen [Profiler](/manuals/profiling). Setze **Profiler** auf **Always** im [Anwendungsmanifest](/manuals/app-manifest/#profiler), um die Profiler-Unterstützung sowohl in Debug- als auch in Release-Builds einzuschließen.
* Release-Builds enthalten keine [Bildschirmaufnahmefunktion](/ref/stable/sys/#start_record)
* Release-Builds zeigen weder die Ausgabe von Aufrufen von `print()` noch die Ausgabe nativer Erweiterungen an
* Bei Release-Builds ist der Wert `is_debug` in `sys.get_engine_info()` auf `false` gesetzt
* Release-Builds führen beim Aufruf von `tostring()` keine Rückwärtssuche für `hash`-Werte durch. In der Praxis bedeutet das, dass `tostring()` für einen Wert vom Typ `url` oder `hash` dessen numerische Darstellung statt der ursprünglichen Zeichenfolge zurückgibt (`'hash: [/camera_001]'` gegenüber `'hash: [11844936738040519888 (unknown)]'`)
* Release-Builds können im Editor nicht als Ziel für [Hot Reload](/manuals/hot-reload) und ähnliche Funktionen ausgewählt werden


