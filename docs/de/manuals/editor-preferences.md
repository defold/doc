---
title: Editoreinstellungen
brief: Du kannst die Einstellungen des Editors im Fenster Preferences ändern.
---

# Editoreinstellungen {#editor-preferences}

Du kannst die Einstellungen des Editors im Fenster Preferences ändern. Du öffnest das Einstellungsfenster über das Menü <kbd>File -> Preferences</kbd>.

## General

![](images/editor/preferences_general.png)

Load External Changes on App Focus
: Aktiviert die Suche nach externen Änderungen, wenn der Editor den Fokus erhält.

Open Bundle Target Folder
: Aktiviert das Öffnen des Bundle-Zielordners nach Abschluss der Bundle-Erstellung.

Enable Texture Compression
: Aktiviert die [Texturkomprimierung](/manuals/texture-profiles) für alle Builds, die im Editor erstellt werden.

Escape Quits Game
: Beendet einen laufenden Build deines Spiels mit der Taste <kbd>Esc</kbd>.

Track Active Tab in Asset Browser
: Die Datei, die in der ausgewählten Registerkarte des Bereichs *Editor* bearbeitet wird, wird im Asset Browser (auch als Bereich *Asset* bekannt) ausgewählt.

Lint Code on Build
: Aktiviert die [statische Codeprüfung](/manuals/writing-code/#linting-configuration) beim Erstellen eines Builds des Projekts. Diese Option ist standardmäßig aktiviert, kann aber deaktiviert werden, wenn die statische Codeprüfung in einem großen Projekt zu viel Zeit beansprucht.

Engine Arguments
: Argumente, die an die ausführbare Datei dmengine übergeben werden, wenn der Editor einen Build erstellt und startet.
 Verwende ein Argument pro Zeile. Zum Beispiel:
 ```
--config=bootstrap.main_collection=/my dir/1.collectionc
--verbose
--graphics-adapter=vulkan
```


## Code

![](images/editor/preferences_code.png)

Custom Editor
: Absoluter Pfad zu einem externen Editor. Unter macOS sollte dies der Pfad zur ausführbaren Datei innerhalb der .app sein (z. B. `/Applications/Atom.app/Contents/MacOS/Atom`).

Open File
: Das Muster, mit dem der benutzerdefinierte Editor angibt, welche Datei geöffnet werden soll. Das Muster `{file}` wird durch den Namen der zu öffnenden Datei ersetzt.

Open File at Line
: Das Muster, mit dem der benutzerdefinierte Editor angibt, welche Datei an welcher Zeilennummer geöffnet werden soll. Das Muster `{file}` wird durch den Namen der zu öffnenden Datei ersetzt und `{line}` durch die Zeilennummer.

Code editor font
: Name einer auf dem System installierten Schriftart, die im Code-Editor verwendet werden soll.

Zoom on Scroll
: Legt fest, ob sich die Schriftgröße beim Scrollen im Code-Editor ändert, während die Taste Cmd/Ctrl gedrückt gehalten wird.

Auto-insert closing parens
: Fügt beim Bearbeiten von Code automatisch passende schließende Zeichen ein. Diese Option ist standardmäßig aktiviert.

Format on save
: Führt beim Speichern die Formatierung des Sprachservers für geänderte, geöffnete Codedateien aus. Standardmäßig deaktiviert. Der Sprachserver muss die Formatierung unterstützen; wie du ein Dokument oder eine Auswahl manuell formatierst, erfährst du unter [Code formatieren](/manuals/writing-code/#formatting-code).


### Skriptdateien in Visual Studio Code öffnen {#open-script-files-in-visual-studio-code}

![](images/editor/preferences_vscode.png)

Um Skriptdateien aus dem Defold-Editor direkt in Visual Studio Code zu öffnen, musst du die folgenden Einstellungen vornehmen und dabei den Pfad zur ausführbaren Datei angeben:

- MacOS: `/Applications/Visual Studio Code.app/Contents/MacOS/Electron`
- Linux: `/usr/bin/code`
- Windows: `C:\Program Files\Microsoft VS Code\Code.exe`

 Lege diese Parameter fest, um bestimmte Dateien und Zeilen zu öffnen:

- Open File: `. {file}`
- Open File at Line: `. -g {file}:{line}`

Das Zeichen `.` ist hier erforderlich, um den gesamten Arbeitsbereich zu öffnen und nicht nur eine einzelne Datei.


## Extensions

![](images/editor/preferences_extensions.png)

Build Server
: URL des Build-Servers, der beim Erstellen eines Builds eines Projekts mit [nativen Erweiterungen (native extensions)](/manuals/extensions) verwendet wird. Du kannst der URL einen Benutzernamen und ein Zugriffstoken hinzufügen, um dich beim Zugriff auf den Build-Server zu authentifizieren. Verwende die folgende Schreibweise, um den Benutzernamen und das Zugriffstoken anzugeben: `username:token@build.defold.com`. Ein authentifizierter Zugriff ist für Nintendo Switch-Builds erforderlich sowie dann, wenn du eine eigene Build-Server-Instanz mit aktivierter Authentifizierung betreibst (weitere Informationen findest du in der [Dokumentation des Build-Servers](https://github.com/defold/extender/blob/dev/README_SECURITY.md)). Benutzername und Passwort können auch über die Systemumgebungsvariablen `DM_EXTENDER_USERNAME` und `DM_EXTENDER_PASSWORD` festgelegt werden.

Build Server Username
: Benutzername für die Authentifizierung.

Build Server Password
: Passwort für die Authentifizierung; wird verschlüsselt in der Einstellungsdatei gespeichert.

Build Server Headers
: Zusätzliche Header für den Build-Server beim Erstellen nativer Erweiterungen. Sie sind wichtig für die Verwendung des Dienstes CloudFlare oder ähnlicher Dienste mit extender.

## Tools

![](images/editor/preferences_tools.png)

ADB path
: Pfad zum auf diesem System installierten Befehlszeilenwerkzeug [ADB](https://developer.android.com/tools/adb). Wenn ADB auf deinem System installiert ist, verwendet der Defold-Editor es, um als Bundle erstellte Android-APKs auf einem angeschlossenen Android-Gerät zu installieren und auszuführen. Standardmäßig prüft der Editor, ob ADB an bekannten Speicherorten installiert ist. Du musst den Pfad daher nur angeben, wenn du ADB an einem benutzerdefinierten Speicherort installiert hast.

ios-deploy path
: Pfad zu den auf diesem System installierten Befehlszeilenwerkzeugen [ios-deploy](https://github.com/ios-control/ios-deploy) (nur für macOS relevant). Ähnlich wie beim ADB-Pfad verwendet der Defold-Editor dieses Werkzeug, um als Bundle erstellte iOS-Anwendungen auf einem angeschlossenen iPhone zu installieren und auszuführen. Standardmäßig prüft der Editor, ob ios-deploy an bekannten Speicherorten installiert ist. Du musst den Pfad daher nur angeben, wenn du eine benutzerdefinierte Installation von ios-deploy verwendest.

## Keymap

![](images/editor/preferences_keymap.png)

Du kannst die Tastenkombinationen und die Maussteuerung des Editors auf der Registerkarte Keymap konfigurieren. Um einen Befehl zu ändern, doppelklicke darauf, drücke <kbd>Enter</kbd> oder <kbd>Space</kbd> oder verwende das Kontextmenü der Zeile.

Tastenkombinationen werden in der Spalte *Shortcuts* angezeigt. Maussteuerungen erscheinen in derselben Liste mit einer Kennzeichnung:

- <kbd>MB</kbd> steht für eine Maustastenbelegung, optional in Kombination mit <kbd>Shift</kbd>, <kbd>Ctrl</kbd>/<kbd>Control</kbd> oder <kbd>Alt</kbd>.
- <kbd>MM</kbd> steht für eine Modifikatortaste, die bei einer Mausaktion verwendet wird.

Einige Maussteuerungen verwenden die Standardbelegungen von Scene 2D Camera mit, sodass eine Zeile bereits eine Belegung anzeigen kann, bevor du sie anpasst. Diese Belegungen werden üblicherweise in einer dunkleren Farbe dargestellt. Wenn du für diese Zeile eine eigene Belegung festlegst, verwendet Defold stattdessen deine Belegung. Verwende *Reset to Defaults*, um deine Änderung zu entfernen und zum integrierten oder geerbten Verhalten zurückzukehren.

Warnungen werden orange angezeigt. Bewege den Mauszeiger über eine Warnung, um Details zu sehen. Warnungen bedeuten üblicherweise:
- Die Tastenkombination kann Text eingeben und Textfelder beeinträchtigen.
- Dieselbe Tastenkombination oder Mausbelegung wird bereits von einem anderen Befehl verwendet.
