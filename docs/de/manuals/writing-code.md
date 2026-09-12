---
title: Code schreiben
brief: Dieses Handbuch gibt einen kurzen Überblick über die Arbeit mit Code in Defold.
---

# Code schreiben {#writing-code}

Defold ermöglicht dir zwar, viele Spielinhalte mit visuellen Werkzeugen wie den Editoren für Kachelkarten (tile maps) und Partikeleffekte zu erstellen, deine Spiellogik schreibst du jedoch weiterhin in einem Code-Editor. Die Spiellogik wird in der [Programmiersprache Lua](https://www.lua.org/) geschrieben, während Erweiterungen der Engine selbst in den nativen Programmiersprachen der Zielplattform geschrieben werden.

## Lua-Code schreiben {#writing-lua-code}

Defold verwendet Lua 5.1 und LuaJIT (je nach Zielplattform). Beim Schreiben deiner Spiellogik musst du die Sprachspezifikation dieser jeweiligen Lua-Versionen einhalten. Weitere Einzelheiten zur Arbeit mit Lua in Defold findest du in unserem [Handbuch zu Lua in Defold](/manuals/lua).

## Andere Sprachen verwenden, die nach Lua transpilieren {#using-other-languages-that-transpile-to-lua}

Defold unterstützt Transpiler, die Lua-Code erzeugen. Wenn eine Transpiler-Erweiterung installiert ist, kannst du alternative Sprachen wie [Teal](https://github.com/defold/extension-teal) verwenden, um statisch geprüften Lua-Code zu schreiben. Diese Vorschaufunktion hat Einschränkungen: Die derzeitige Transpiler-Unterstützung stellt keine Informationen über Module und Funktionen bereit, die in der Lua-Laufzeitumgebung von Defold definiert sind. Wenn du Defold-APIs wie `go.animate` verwenden möchtest, musst du die externen Definitionen dafür daher selbst schreiben.

## Nativen Code schreiben {#writing-native-code}

Defold ermöglicht dir, die Game-Engine mit nativem Code zu erweitern, um auf plattformspezifische Funktionen zuzugreifen, die die Engine selbst nicht bereitstellt. Du kannst nativen Code auch verwenden, wenn die Leistung von Lua nicht ausreicht (ressourcenintensive Berechnungen, Bildverarbeitung usw.). Weitere Informationen findest du in unseren [Handbüchern zu nativen Erweiterungen (native extensions)](/manuals/extensions/).

## Den integrierten Code-Editor verwenden {#using-the-built-in-code-editor}

Defold verfügt über einen integrierten Code-Editor, mit dem du Lua-Dateien (.lua), Defold-Skriptdateien (.script, .gui_script und .render_script) sowie alle anderen Dateien öffnen und bearbeiten kannst, deren Dateierweiterung der Editor nicht von Haus aus verarbeitet. Außerdem bietet der Editor Syntaxhervorhebung für Lua- und Skriptdateien.

![](/images/editor/code-editor.png)

### Codevervollständigung {#code-completion}

Der integrierte Code-Editor zeigt beim Schreiben von Code Vorschläge zur Vervollständigung von Funktionen an:

![](/images/editor/codecompletion.png)

Wenn du <kbd>CTRL</kbd> + <kbd>Space</kbd> drückst, werden zusätzliche Informationen zu Funktionen, Argumenten und Rückgabewerten angezeigt:

![](/images/editor/apireference.png)

Der mitgelieferte Lua-Sprachserver enthält Typannotationen für die Defold-APIs. Die Vervollständigung, Informationen beim Überfahren mit dem Mauszeiger und die Diagnosefunktionen berücksichtigen Defold-Typen wie Hashwerte, URLs, Vektoren und Quaternionen sowie Funktionsargumente und Rückgabewerte. Der Editor stellt Annotationen für Spielskripte und für die `editor.*`-APIs bereit, die in `.editor_script`-Dateien verwendet werden. Wenn du den Code-Editor von Defold verwendest, benötigst du für die integrierten APIs keine separate Annotationsbibliothek.

APIs von Erweiterungen Dritter benötigen möglicherweise eigene Annotationen.

### Code formatieren {#formatting-code}

Wähle <kbd>Edit ▸ Format Document/Selection</kbd> oder drücke <kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>F</kbd>, um den Formatierer des Sprachservers auszuführen. Wenn eine Auswahl vorhanden ist, formatiert der Editor die ausgewählten Zeilen; andernfalls formatiert er das Dokument. Dafür ist ein Sprachserver erforderlich, der den jeweiligen Formatierungsvorgang unterstützt.

Um geänderte geöffnete Dateien beim Speichern zu formatieren, aktiviere **Format on save** unter <kbd>Preferences ▸ Code</kbd>. Diese Einstellung ist standardmäßig deaktiviert und erfordert einen Sprachserver, der die Formatierung von Dokumenten unterstützt. Siehe [Einstellungen für Code](/manuals/editor-preferences/#code).

### Zu einem Symbol springen {#jump-to-symbol}

Der integrierte Code-Editor kann eine durchsuchbare Liste der Symbole in der aktuellen Codedatei anzeigen, beispielsweise Funktionen, Objekte und Variablen. Wähle <kbd>View ▸ Jump to Symbol…</kbd> oder drücke unter Windows und Linux <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>O</kbd> beziehungsweise unter macOS <kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd> + <kbd>O</kbd>.

Beginne zu tippen, um die Symbole mit einer unscharfen Suche zu durchsuchen. Verwende die Pfeiltasten, um durch die Ergebnisse zu navigieren und ihre Positionen im Editor in der Vorschau zu sehen. Drücke anschließend <kbd>Enter</kbd>, um zum ausgewählten Symbol zu springen. Drücke <kbd>Esc</kbd>, um das Dialogfeld zu schließen und zur vorherigen Cursor- und Scrollposition zurückzukehren.

![](/images/editor/jump-to-symbol.png)

### Statische Codeprüfung konfigurieren {#linting-configuration}

Der integrierte Code-Editor führt mit [Luacheck](https://luacheck.readthedocs.io/en/stable/index.html) und dem [Lua-Sprachserver](https://luals.github.io/wiki/diagnostics/) eine statische Codeprüfung durch. Um Luacheck zu konfigurieren, erstelle eine Datei namens `.luacheckrc` im Stammverzeichnis des Projekts. Eine Liste der verfügbaren Optionen findest du auf der [Seite zur Konfiguration von Luacheck](https://luacheck.readthedocs.io/en/stable/config.html). Defold verwendet die folgenden Standardeinstellungen für die Luacheck-Konfiguration:

```lua
unused_args = false      -- don't warn on unused arguments (common for .script files)
max_line_length = false  -- don't warn on long lines
ignore = {
    "611",               -- line contains only whitespace
    "612",               -- line contains trailing whitespace
    "614"                -- trailing whitespace in a comment
},
```

## Einen externen Code-Editor verwenden {#using-an-external-code-editor}

Der Code-Editor in Defold bietet die grundlegenden Funktionen, die du zum Schreiben von Code benötigst. Für anspruchsvollere Anwendungsfälle oder wenn du als erfahrener Nutzer einen bevorzugten Code-Editor hast, kannst du Defold Dateien in einem externen Editor öffnen lassen. Im [Fenster Preferences auf der Registerkarte Code](/manuals/editor-preferences/#code) kannst du einen externen Editor festlegen, der zum Bearbeiten von Code verwendet werden soll.

### Visual Studio Code - Defold Kit

Defold Kit ist ein Plugin für Visual Studio Code mit den folgenden Funktionen:

* Installation empfohlener Erweiterungen
* Syntaxhervorhebung, automatische Vervollständigung und statische Codeprüfung für Lua
* Anwendung relevanter Einstellungen auf den Arbeitsbereich
* Lua-Annotationen für die Defold-API
* Lua-Annotationen für Abhängigkeiten
* Builds erstellen und starten
* Debuggen mit Haltepunkten
* Bundles für alle Plattformen erstellen
* Bereitstellung auf verbundenen Mobilgeräten

Weitere Informationen und die Möglichkeit, Defold Kit zu installieren, findest du im [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=astronachos.defold).


## Dokumentationssoftware {#documentation-software}

Von der Community erstellte API-Referenzpakete sind für [Dash und Zeal](https://forum.defold.com/t/defold-docset-for-dash/2417) verfügbar.
