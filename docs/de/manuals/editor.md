---
title: Überblick über den Editor
brief: Dieses Handbuch gibt einen Überblick über das Aussehen und die Funktionsweise des Defold-Editors und erklärt, wie du darin navigierst.
---

# Überblick über den Editor {#editor-overview}

Mit dem Editor kannst du alle Dateien und Ordner in deinem Spielprojekt effizient durchsuchen und bearbeiten. Beim Bearbeiten einer Datei öffnet sich ein geeigneter Editor, und alle relevanten Informationen zur Datei werden in eigenen Ansichten angezeigt.

## Den Editor starten {#starting-the-editor}

Wenn du den Defold-Editor startest, erscheint ein Bildschirm zum Auswählen und Erstellen von Projekten. Wähle per Klick aus, was du tun möchtest:

MY PROJECTS
: Hier findest du deine zuletzt geöffneten Projekte, damit du schnell auf sie zugreifen kannst. Dies ist die Standardansicht des Startbildschirms.

  Wenn du noch keine Projekte geöffnet hast (oder alle entfernt hast), werden zwei Schaltflächen angezeigt. Du kannst auf `Open From Disk…` klicken, um ein Projekt mit dem Dateibrowser des Betriebssystems zu suchen und zu öffnen, oder auf die Schaltfläche `Create New Project` klicken, um zur Registerkarte `TEMPLATES` zu wechseln.

  ![Meine Projekte](images/editor/start_no_projects.png)


  Wenn du bereits Projekte geöffnet hast, erscheint eine Liste deiner Projekte, wie in der folgenden Abbildung:

  ![Meine Projekte](images/editor/start_my_projects.png)

TEMPLATES
: Enthält leere oder nahezu leere Basisprojekte für den schnellen Einstieg in ein neues Defold-Projekt für bestimmte Plattformen oder mit bestimmten Erweiterungen.


TUTORIALS
: Enthält Projekte mit angeleiteten Tutorials zum Lernen, Ausprobieren und Verändern, wenn du einem Tutorial folgen möchtest.


SAMPLES
: Enthält Projekte, die bestimmte Anwendungsfälle veranschaulichen.

  ![Neues Projekt](images/editor/start_templates.png)

Wenn du ein neues Projekt erstellst, wird es auf deinem lokalen Laufwerk gespeichert. Alle Änderungen, die du vornimmst, werden lokal gespeichert.

Mehr über die verschiedenen Möglichkeiten erfährst du im [Handbuch zur Projekteinrichtung](https://www.defold.com/manuals/project-setup/).

## Sprache des Editors {#editor-language}

Unten links auf dem Startbildschirm findest du eine Sprachauswahl. Wähle eine der derzeit verfügbaren Übersetzungen aus. Diese Einstellung findest du auch im Editor unter `File ▸ Preferences ▸ General ▸ Editor Language`.

![Sprachen](images/editor/languages.png)

## Die Bereiche des Editors {#the-editor-views}

Der Defold-Editor ist in mehrere Bereiche oder Ansichten unterteilt, die jeweils bestimmte Informationen anzeigen.

![Editor 2](images/editor/editor_overview.png)

### 1. Bereich Assets {#1-assets-pane}
Listet alle Dateien und Ordner deines Projekts in einer Baumstruktur auf, die der Struktur auf deinem Laufwerk entspricht. Navigiere durch Klicken und Scrollen in der Liste. Alle dateibezogenen Vorgänge lassen sich in dieser Ansicht ausführen:

   - Mit einem <kbd>Klick mit der linken Maustaste</kbd> wählst du eine Datei oder einen Ordner aus. Wenn du dabei <kbd>⇧ Shift</kbd> gedrückt hältst, kannst du die Auswahl erweitern. Wenn du <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> gedrückt hältst, kannst du angeklickte Elemente auswählen oder aus der Auswahl entfernen.
   - Mit einem <kbd>Doppelklick</kbd> auf eine Datei öffnest du sie in einem Editor für den jeweiligen Dateityp.
   - Durch <kbd>Ziehen und Ablegen</kbd> kannst du Dateien von anderen Orten auf deinem Laufwerk zum Projekt hinzufügen oder Dateien und Ordner an andere Stellen im Projekt verschieben.
   - Mit einem <kbd>Klick mit der rechten Maustaste</kbd> öffnest du ein _Kontextmenü_, in dem du neue Dateien oder Ordner erstellen, sie umbenennen oder löschen, Dateiabhängigkeiten nachverfolgen und weitere Aktionen ausführen kannst.

Dateien und Ordner, die du über den Bereich *Assets* löschst, werden in den Papierkorb des Betriebssystems verschoben, sofern die Plattform dies unterstützt. Wenn das Verschieben in den Papierkorb nicht unterstützt wird oder fehlschlägt, löscht der Editor sie dauerhaft.

### 2. Bereich Scene Editor {#the-scene-editor}

Ein Doppelklick auf eine Datei für eine Sammlung (collection), ein Spielobjekt (game object) oder eine visuelle Komponente (component) öffnet den *Scene Editor*, den visuellen Editor zum Erstellen und Bearbeiten von Szenen. Skriptdateien und andere nicht visuelle Ressourcen werden in ihren jeweils eigenen Editoren geöffnet.

![Scene Editor](images/editor/2d_scene.png)

Zu den zentralen Funktionen des Szeneneditors gehören:

- [Navigation in 2D- und 3D-Szenen](/manuals/scene-editing/#2d-and-3d-scene-orientation) mit orthografischen und perspektivischen Kameramodi
- [Transformationswerkzeuge](/manuals/scene-editing/#manipulating-objects) zum Verschieben, Drehen und Skalieren von Objekten
- [Freier Kameramodus (Free Camera Mode)](/manuals/scene-editing/#free-camera-mode) für die 3D-Navigation aus der Ich-Perspektive
- [Rastereinstellungen](/manuals/scene-editing/#grid-settings) mit konfigurierbarer Größe, Ebene und Darstellung
- [Sichtbarkeitsfilter](/manuals/scene-editing/#visibility-filters) zum Ein- und Ausblenden von Komponententypen und Hilfslinien

Mehr dazu erfährst du im [Handbuch zum Szeneneditor](/manuals/scene-editing/).

### 3. Bereich Outline {#3-outline-pane}

Diese Ansicht zeigt den Inhalt der aktuell bearbeiteten Datei in einer hierarchischen Baumstruktur. Outline spiegelt die Editoransicht wider und ermöglicht dir, Aktionen an deinen Elementen auszuführen:

   - Mit einem <kbd>Klick mit der linken Maustaste</kbd> wählst du ein Element aus. Wenn du dabei <kbd>⇧ Shift</kbd> gedrückt hältst, kannst du die Auswahl erweitern. Wenn du <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> gedrückt hältst, kannst du angeklickte Elemente auswählen oder aus der Auswahl entfernen.
   - Durch <kbd>Ziehen und Ablegen</kbd> verschiebst du Elemente. Lege ein Spielobjekt auf einem anderen Spielobjekt in einer Sammlung ab, um eine Eltern-Kind-Beziehung herzustellen.
   - Mit einem <kbd>Klick mit der rechten Maustaste</kbd> öffnest du ein _Kontextmenü_, in dem du Elemente hinzufügen, ausgewählte Elemente löschen und weitere Aktionen ausführen kannst.

Du kannst die Sichtbarkeit von Spielobjekten und visuellen Komponenten umschalten, indem du auf das kleine Augensymbol `👁` rechts neben einem Element in der Liste klickst.

![Outline](images/editor/outline.png)

### 4. Bereich Properties {#4-properties-pane}

Diese Ansicht zeigt die Eigenschaften des aktuell ausgewählten Elements an, beispielsweise Id, URL, Position, Rotation, Scale und/oder andere komponentenspezifische Eigenschaften sowie benutzerdefinierte Eigenschaften für Skripte.

Du kannst auch den Auf-Ab-Pfeil `↕` <kbd>ziehen</kbd> und die Maus bewegen, um den Wert der jeweiligen numerischen Eigenschaft zu ändern.

![Properties](images/editor/properties.png)

### 5. Bereich Tools {#5-tools-pane}

Diese Ansicht enthält mehrere Registerkarten.

Registerkarte *Console*: zeigt alle Fehler-, Warn- und Informationsausgaben der Engine sowie die Ausgaben an, die du während der Ausführung deines Spiels gezielt erzeugst,

*Build Errors*: zeigt Fehler aus dem Build-Vorgang an,

*Search Results*: zeigt die Ergebnisse der Suche (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd> + <kbd>F</kbd>) im gesamten Projekt an, wenn du auf `Keep Results` klickst

*Curve Editor*: wird beim Bearbeiten von Kurven im [Partikeleditor](/manuals/particlefx/) verwendet.

Der Bereich Tools dient außerdem zur Bedienung des integrierten Debuggers. Mehr dazu erfährst du im [Handbuch zur Fehlersuche](/manuals/debugging/).

### 6. Bereich Changed Files {#6-changed-files-pane}

Wenn dein Projekt Git verwendet, listet diese Ansicht Dateien auf, die gegenüber dem aktuellen Commit (`HEAD`) lokal geändert, hinzugefügt, umbenannt oder gelöscht wurden. Verwende einen externen Git-Client oder die Kommandozeile, um das Projekt mit einem entfernten Repository zu synchronisieren. Mehr dazu erfährst du im [Handbuch zur Versionsverwaltung](/manuals/version-control/). Einige dateibezogene Vorgänge lassen sich in dieser Ansicht ausführen:

   - Mit einem <kbd>Klick mit der linken Maustaste</kbd> wählst du eine Datei aus. Wenn du dabei <kbd>⇧ Shift</kbd> gedrückt hältst, kannst du die Auswahl erweitern. Wenn du <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> gedrückt hältst, kannst du angeklickte Elemente auswählen oder aus der Auswahl entfernen. Wenn eine einzelne geänderte Datei ausgewählt ist, kannst du auf `Diff` klicken, um die Unterschiede anzuzeigen. Mit `Revert` kannst du die Änderungen in allen ausgewählten Dateien rückgängig machen.
   - Mit einem <kbd>Doppelklick mit der linken Maustaste</kbd> auf eine Datei öffnest du eine Ansicht der Datei. Der Editor öffnet die Datei in einem geeigneten Editor, genau wie in der Ansicht Assets.
   - Mit einem <kbd>Klick mit der rechten Maustaste</kbd> auf eine Datei öffnest du ein Popup-Menü, in dem du eine Ansicht der Unterschiede öffnen, alle Änderungen an der Datei rückgängig machen, die Datei im Dateisystem finden und weitere Aktionen ausführen kannst.

### Menüleiste {#menu-bar}

Oben in der Editoransicht oder auf dem Mac in der Systemleiste findest du die Menüleiste mit 6 Menüs: `File`, `Edit`, `View`, `Project`, `Debug`, `Help`. Ihre Funktionen werden in den Handbüchern erläutert.

### Statusleiste {#status-bar}

In der unteren Leiste des Editors findest du einen schmalen Bereich, in dem der Status angezeigt wird, zum Beispiel:
- Wenn ein neues Update verfügbar ist, erscheint die anklickbare Schaltfläche `Update Available`. Lies dazu weiter unten in diesem Handbuch den Abschnitt zum Aktualisieren des Editors.
- Beim Erstellen eines Builds oder Bundles wird dort der Fortschritt angezeigt.

## Größe und Sichtbarkeit der Bereiche {#panes-size-and-visibility}

Du kannst die Größe der Bereiche im Editor anpassen, indem du die Trennlinien zwischen den 6 oben beschriebenen Bereichen <kbd>ziehst</kbd>.

Du kannst die Sichtbarkeit der Bereiche im Editor über die Optionen im Menü `View` oder die angegebenen Tastenkombinationen umschalten:
- `Toggle Assets Pane` (<kbd>F6</kbd>) schaltet die Sichtbarkeit der Bereiche Assets und Changed Files um
- `Toggle Changed Files` schaltet nur die Sichtbarkeit des Bereichs Changed Files um
- `Toggle Tools Pane` (<kbd>F7</kbd>) schaltet die Sichtbarkeit des Bereichs Tools um
- `Toggle Properties Pane` (<kbd>F8</kbd>) schaltet die Sichtbarkeit der Bereiche Outline und Properties um

![Sichtbarkeit der Bereiche](images/editor/editor_panes.png)

Im Menü `View` kannst du auch andere Einstellungen für die Sichtbarkeit umschalten oder ändern, etwa Grid, Guides oder Camera. Du kannst die Ansicht an die Auswahl anpassen (`Frame Selection` oder die Taste <kbd>F</kbd>) und zwischen der standardmäßigen 2D- und 3D-Ansicht wechseln (`Realign Camera` oder die Taste <kbd>.</kbd>). Viele dieser Funktionen sind auch über die Werkzeugleiste oder Tastenkombinationen zugänglich.

## Registerkarten {#tabs}

Wenn du mehrere Dateien geöffnet hast, erscheint oben in der Editoransicht eine eigene Registerkarte für jede Datei. Registerkarten innerhalb eines Bereichs lassen sich verschieben: Durch <kbd>Ziehen und Ablegen</kbd> kannst du ihre Positionen innerhalb der Registerkartenleiste vertauschen. Außerdem kannst du:

- mit einem <kbd>Klick mit der rechten Maustaste</kbd> auf eine Registerkarte ein _Kontextmenü_ öffnen,
- auf `Close` (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>W</kbd>) klicken, um eine einzelne Registerkarte zu schließen,
- auf `Close Others` klicken, um alle Registerkarten außer der ausgewählten zu schließen,
- auf `Close All` (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd>+<kbd>W</kbd>) klicken, um alle Registerkarten im aktiven Bereich zu schließen,
- `➝| Open As` auswählen, um einen anderen Editor als den Standardeditor oder das zugeordnete externe Werkzeug zu verwenden, das unter `File ▸ Preferences ▸ Code ▸ Custom Editor` festgelegt ist. Mehr dazu erfährst du im [Handbuch zu den Editoreinstellungen](/manuals/editor-preferences).

![Registerkarten](images/editor/tabs_custom.png)

## Nebeneinander bearbeiten {#side-by-side-editing}

Du kannst 2 Editoransichten nebeneinander öffnen.

- Öffne mit einem <kbd>Klick mit der rechten Maustaste</kbd> das Menü der Registerkarte des Editors, den du verschieben möchtest, und wähle `Move to Other Tab Pane` aus.

![2 Bereiche](images/editor/2-panes.png)

Du kannst im Registerkartenmenü auch `Swap with Other Tab Pane` verwenden, um die jeweilige Registerkarte zwischen den Bereichen zu verschieben, oder die Bereiche mit `Join Tab Panes` zu einem einzigen Bereich zusammenführen.

## Neue Projektdateien erstellen {#creating-new-project-files}

Um neue Ressourcendateien zu erstellen, wähle entweder `File ▸ New…` und dann den Dateityp im Menü aus oder verwende das Kontextmenü:

Öffne mit einem <kbd>Klick mit der rechten Maustaste</kbd> das Kontextmenü am Zielort im Browser `Assets` und wähle dann `New… ▸ [file type]`:

![Datei erstellen](images/editor/create_file.png)

Gib unter *Name* einen passenden Namen für die neue Datei ein und ändere bei Bedarf *Location*. Der vollständige Dateiname einschließlich der Dateierweiterung wird im Dialogfeld unter *Preview* angezeigt:

![Dateinamen festlegen](images/editor/create_file_name.png)

## Vorlagen {#templates}

Du kannst für jedes Projekt eigene Vorlagen festlegen. Erstelle dazu einen neuen Ordner namens `templates` im Stammverzeichnis des Projekts und füge neue Dateien namens `default.*` mit den gewünschten Erweiterungen hinzu, beispielsweise `/templates/default.gui` oder `/templates/default.script`. Wenn in diesen Dateien das Token `{{NAME}}` verwendet wird, wird es außerdem durch den im Fenster zur Dateierstellung angegebenen Dateinamen ersetzt.

Wenn für einen Dateityp eine Vorlage verfügbar ist, wird jede neu erstellte Datei dieses Typs mit dem Inhalt der entsprechenden Datei aus `templates` initialisiert.


![Vorlagen](images/editor/templates.png)

## Dateien in dein Projekt importieren {#importing-files-to-your-project}

Um Asset-Dateien (Bilder, Audiodateien, Modelle usw.) zu deinem Projekt hinzuzufügen, ziehe sie einfach an die richtige Stelle im Browser *Assets* und lege sie dort ab. Dadurch werden _Kopien_ der Dateien am ausgewählten Ort in der Dateistruktur des Projekts erstellt. Mehr dazu erfährst du in unserem [Handbuch zum Importieren von Assets](/manuals/importing-assets/).

![Dateien importieren](images/editor/import.png)

## Den Editor aktualisieren {#updating-the-editor}

Der Editor sucht automatisch nach Updates, wenn eine Internetverbindung besteht. Wenn ein Update gefunden wird, erscheint der blaue anklickbare Link `Update Available` unten links auf dem Bildschirm zur Projektauswahl oder unten rechts im Editorfenster.

![Update über die Projektauswahl](images/editor/update_start.png)
![Update über den Editor](images/editor/update_available.png)

Klicke auf den Link `Update Available`, um das Update herunterzuladen und zu installieren. Ein Bestätigungsfenster mit Informationen erscheint. Klicke auf `Download Update`, um fortzufahren.

![Popup zum Aktualisieren des Editors](images/editor/update.png)

Den Downloadfortschritt siehst du in der unteren Statusleiste:

![Downloadfortschritt](images/editor/download_status.png)

Nach dem Herunterladen des Updates ändert sich der blaue Link zu `Restart to Update`. Klicke darauf, um den Editor neu zu starten und die aktualisierte Version zu öffnen.

![Zum Aktualisieren neu starten](images/editor/restart_to_update.png)

## Editoreinstellungen {#preferences}

Du kannst die Einstellungen des Editors im Fenster `Preferences` ändern. Klicke zum Öffnen auf `File ▸ Preferences…` oder verwende die Tastenkombination <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>,</kbd>

Weitere Einzelheiten findest du im [Handbuch zu den Editoreinstellungen](/manuals/editor-preferences)

![Editoreinstellungen](images/editor/preferences.png)

## Editorprotokolle {#editor-logs}
Wenn ein Problem mit dem Editor auftritt und du es melden musst (`Help  ▸ Report Issue`), ist es sinnvoll, Protokolldateien des Editors beizufügen. Klicke auf `Help ▸ Show Logs`, um den Speicherort der Protokolle im Dateibrowser deines Betriebssystems zu öffnen.

Mehr dazu erfährst du im [Handbuch zur Hilfesuche](/manuals/getting-help/#getting-help).

![Protokolle anzeigen](images/editor/show_logs.png)

Die Protokolldateien des Editors findest du hier:

  * Windows: `C:\Users\ **Your Username** \AppData\Local\Defold`
  * macOS: `/Users/ **Your Username** /Library/Application Support/` oder `~/Library/Application Support/Defold`
  * Linux: `$XDG_STATE_HOME/Defold` oder `~/.local/state/Defold`

Du kannst auch während der Ausführung des Editors auf seine Protokolle zugreifen, wenn du ihn über ein Terminal oder eine Eingabeaufforderung startest. Verwende zum Starten des Editors den Befehl:

```shell
# Linux:
$ ./path/to/Defold/Defold

# macOS:
$ > ./path/to/Defold.app/Contents/MacOS/Defold
```

## Editorserver {#editor-server}

Wenn der Editor ein Projekt öffnet, startet er einen Webserver auf einem zufälligen Port. Über den Server können andere Anwendungen mit dem Editor interagieren. Der Port wird in die Datei `.internal/editor.port` geschrieben.

Der Server stellt unter `http://localhost:$(cat .internal/editor.port)/openapi.json` eine OpenAPI-Spezifikation bereit. Dies ist ein nützlicher minimaler Ausgangspunkt für Arbeitsabläufe mit Agenten.

Außerdem unterstützt die ausführbare Datei des Editors die Kommandozeilenoption `--port` (oder `-p`), mit der sich der Port beim Start angeben lässt, zum Beispiel:
```shell
# Windows
.\path\to\Defold\Defold.exe --port 8181

# Linux:
./path/to/Defold/Defold --port 8181

# macOS:
./path/to/Defold/Defold.app/Contents/MacOS/Defold --port 8181
```

## Metadaten zur Editorinstallation {#editor-installation-metadata}

Beim Start schreibt der Editor Informationen über das Startprogramm und die Installationspfade an einen festgelegten Speicherort. IDE-Integrationen von Drittanbietern und andere Werkzeuge können damit installierte Defold-Editoren finden:

| Betriebssystem | Speicherort |
|---------|----------|
| macOS   | `~/Library/Application Support/Defold/installations.json` |
| Linux   | `${XDG_STATE_HOME:-~/.local/state}/Defold/installations.json` |
| Windows | `%LOCALAPPDATA%\Defold\installations.json` |

Die Datei enthält ein JSON-Array mit einem Objekt pro bekannter Installation:

```json
[
  {
    "launcherPath": "/Applications/Defold.app/Contents/MacOS/Defold",
    "installPath": "/Applications/Defold.app",
    "lastLaunchedAt": "2026-07-06T12:34:56.789Z"
  }
]
```

## Gestaltung des Editors {#editor-styling}

Du kannst das Aussehen des Editors durch eigene Stile anpassen. Mehr dazu erfährst du im [Handbuch zur Gestaltung des Editors](/manuals/editor-styling).

## FAQ
:[Editor FAQ](../shared/editor-faq.md)
