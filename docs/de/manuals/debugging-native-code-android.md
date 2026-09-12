---
title: Debugging unter Android
brief: Dieses Handbuch beschreibt, wie du einen Build mit Android Studio debuggst.
---

# Debugging unter Android {#debugging-on-android}

Hier beschreiben wir, wie du einen Build mit [Android Studio](https://developer.android.com/studio/) debuggst, der offiziellen IDE für Googles Betriebssystem Android.


## Android Studio

* Bereite das Bundle vor, indem du die Option `android.debuggable` in *game.project* setzt

	![android.debuggable](images/extensions/debugging/android/game_project_debuggable.png)

* Erstelle im Debug-Modus ein Bundle der App in einem Ordner deiner Wahl.

	![Android-Bundle erstellen](images/extensions/debugging/android/bundle_android.png)

* Starte [Android Studio](https://developer.android.com/studio/)

* Wähle `Profile or debug APK`

	![APK debuggen](images/extensions/debugging/android/android_profile_or_debug.png)

* Wähle das APK-Bundle, das du gerade erstellt hast

	![APK auswählen](images/extensions/debugging/android/android_select_apk.png)

* Wähle die Hauptdatei mit der Erweiterung `.so` und stelle sicher, dass sie Debug-Symbole enthält

	![SO-Datei auswählen](images/extensions/debugging/android/android_missing_symbols.png)

* Falls sie keine enthält, lade eine `.so`-Datei hoch, deren Debug-Symbole nicht entfernt wurden. (Die Größe beträgt etwa 20 MB)

* Mit Pfadzuordnungen kannst du die einzelnen Pfade, unter denen die ausführbare Datei in der Cloud erstellt wurde, einem tatsächlichen Ordner auf deinem lokalen Laufwerk zuordnen.

* Wähle die .so-Datei und füge dann eine Zuordnung zu deinem lokalen Laufwerk hinzu

	![Pfadzuordnung 1](images/extensions/debugging/android/path_mappings_android.png)

	![Pfadzuordnung 2](images/extensions/debugging/android/path_mappings_android2.png)

* Wenn du Zugriff auf den Quellcode der Engine hast, füge auch dafür eine Pfadzuordnung hinzu.

* Stelle sicher, dass du die Version auscheckst, die du gerade debuggst

	defold$ git checkout 1.2.148

* Klicke auf `Apply changes`

* Du solltest den zugeordneten Quellcode jetzt in deinem Projekt sehen

	![Quellcode](images/extensions/debugging/android/source_mappings_android.png)

* Füge einen Haltepunkt hinzu

	![Haltepunkt](images/extensions/debugging/android/breakpoint_android.png)

* Wähle `Run` -> `Debug "Appname"` und rufe den Code auf, in dem du die Ausführung anhalten möchtest

	![Haltepunkt](images/extensions/debugging/android/callstack_variables_android.png)

* Du kannst jetzt schrittweise durch den Aufrufstapel gehen und die Variablen untersuchen


## Hinweise {#notes}

### Auftragsordner für native Erweiterungen {#native-extension-job-folder}

Der Arbeitsablauf bei der Entwicklung nativer Erweiterungen (native extensions) ist derzeit etwas umständlich. Das liegt daran, dass der Name des Auftragsordners
bei jedem Build zufällig gewählt wird, wodurch die Pfadzuordnung bei jedem Build ungültig wird.

Für eine Debugging-Sitzung funktioniert dies jedoch problemlos.

Die Pfadzuordnungen werden in der `.iml`-Datei des Android-Studio-Projekts gespeichert.

Du kannst den Auftragsordner aus der ausführbaren Datei ermitteln

```sh
$ arm-linux-androideabi-readelf --string-dump=.debug_str build/armv7-android/libdmengine.so | grep /job
```

Der Auftragsordner hat einen Namen wie `job1298751322870374150`, jeweils mit einer zufälligen Zahl.

