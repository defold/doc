---
title: Debugging unter iOS/macOS
brief: Dieses Handbuch beschreibt, wie du einen Build mit Xcode debuggst.
---

# Debugging unter iOS/macOS {#debugging-on-iosmacos}

Hier beschreiben wir, wie du einen Build mit [Xcode](https://developer.apple.com/xcode/), Apples bevorzugter IDE zur Entwicklung für macOS und iOS, debuggst.

## Xcode

* Erstelle mit bob und der Option `--with-symbols` ein Bundle der App ([weitere Informationen](/manuals/debugging-native-code/#symbolicate-a-callstack)):

```sh
$ cd myproject
$ wget http://d.defold.com/archive/<sha1>/bob/bob.jar
$ java -jar bob.jar --platform armv7-darwin build --with-symbols --variant debug --archive bundle -bo build/ios -mp <app>.mobileprovision --identity "iPhone Developer: Your Name (ID)"
```

* Installiere die App mit `Xcode`, `iTunes` oder [ios-deploy](https://github.com/ios-control/ios-deploy)

```sh
$ ios-deploy -b <AppName>.ipa
```

* Besorge dir den Ordner `.dSYM` (also die Debug-Symbole)

	* Wenn die App keine nativen Erweiterungen (native extensions) verwendet, kannst du die Datei `.dSYM` von [d.defold.com](http://d.defold.com) herunterladen

	* Wenn du eine native Erweiterung verwendest, wird der Ordner `.dSYM` beim Erstellen eines Builds mit [bob.jar](https://www.defold.com/manuals/bob/) erzeugt. Dafür ist nur ein Build erforderlich (keine Archivierung oder Bundle-Erstellung):

```sh
$ cd myproject
$ unzip .internal/cache/arm64-ios/build.zip
$ mv dmengine.dSYM <AppName>.dSYM
$ mv <AppName>.dSYM/Contents/Resources/DWARF/dmengine <AppName>.dSYM/Contents/Resources/DWARF/<AppName>
```

### Projekt erstellen {#create-project}

Um richtig debuggen zu können, benötigen wir ein Projekt, in dem der Quellcode zugeordnet ist.
Wir verwenden dieses Projekt nur zum Debuggen, nicht zum Erstellen von Builds.

* Erstelle ein neues Xcode-Projekt und wähle die Vorlage `Game`

	![Projektvorlage](images/extensions/debugging/ios/project_template.png)

* Wähle einen Namen (z. B. `debug`) und die Standardeinstellungen

* Wähle einen Ordner, in dem das Projekt gespeichert werden soll

* Füge deinen Code zur App hinzu

	![Dateien hinzufügen](images/extensions/debugging/ios/add_files.png)

* Stelle sicher, dass „Copy items if needed“ deaktiviert ist.

	![Quellcode hinzufügen](images/extensions/debugging/ios/add_source.png)

* So sieht das Endergebnis aus

	![Hinzugefügter Quellcode](images/extensions/debugging/ios/added_source.png)


* Deaktiviere den Schritt `Build`

	![Schema bearbeiten](images/extensions/debugging/ios/edit_scheme.png)

	![Build-Schritt deaktivieren](images/extensions/debugging/ios/disable_build.png)

* Stelle die Version von `Deployment target` so ein, dass sie nun höher als die iOS-Version deines Geräts ist

	![Bereitstellungsversion](images/extensions/debugging/ios/deployment_version.png)

* Wähle das Zielgerät

	![Gerät auswählen](images/extensions/debugging/ios/select_device.png)


### Den Debugger starten {#launch-the-debugger}

Du hast mehrere Möglichkeiten, eine App zu debuggen

1. Wähle entweder `Debug` -> `Attach to process...` und wähle dort die App aus

2. Oder wähle `Attach to process by PID or Process name`

	![Gerät auswählen](images/extensions/debugging/ios/attach_to_process_name.png)

3. Starte die App auf dem Gerät

4. Füge unter `Edit Scheme` den Ordner <AppName>.app als ausführbare Datei hinzu

### Debug-Symbole {#debug-symbols}

**Um lldb zu verwenden, muss die Ausführung angehalten sein**

* Füge den Pfad zu `.dSYM` in lldb hinzu

```
(lldb) add-dsym <PathTo.dSYM>
```

	![Debug-Symbole hinzufügen](images/extensions/debugging/ios/add_dsym.png)

* Prüfe, ob `lldb` die Symbole erfolgreich eingelesen hat

```
(lldb) image list <AppName>
```

### Pfadzuordnungen {#path-mappings}

* Füge den Quellcode der Engine hinzu (passe die Pfade an deine Bedürfnisse an)

```
(lldb) settings set target.source-map /Users/builder/ci/builds/engine-ios-64-master/build /Users/mathiaswesterdahl/work/defold
(lldb) settings append target.source-map /private/var/folders/m5/bcw7ykhd6vq9lwjzq1mkp8j00000gn/T/job4836347589046353012/upload/videoplayer/src /Users/mathiaswesterdahl/work/projects/extension-videoplayer-native/videoplayer/src
```

* Du kannst den Job-Ordner aus der ausführbaren Datei ermitteln. Der Job-Ordner heißt `job1298751322870374150`, wobei die Zahl jedes Mal zufällig gewählt wird.

```sh
$ dsymutil -dump-debug-map <executable> 2>&1 >/dev/null | grep /job

```

* Prüfe die Quellcodezuordnungen

```
(lldb) settings show target.source-map
```

Mit folgendem Befehl kannst du prüfen, aus welcher Quelldatei ein Symbol stammt

```
(lldb) image lookup -va <SymbolName>
```

### Haltepunkte {#breakpoints}

* Öffne eine Datei in der Projektansicht und setze einen Haltepunkt

	![Haltepunkt](images/extensions/debugging/ios/breakpoint.png)

## Hinweise {#notes}

### UUID der Binärdatei prüfen {#check-uuid-of-binary}

Damit der Debugger den Ordner `.dSYM` akzeptiert, muss dessen UUID mit der UUID der ausführbaren Datei übereinstimmen, die du debuggst. Du kannst die UUID wie folgt prüfen:

```sh
$ dwarfdump -u <PathToBinary>
```