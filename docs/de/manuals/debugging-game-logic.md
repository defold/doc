---
title: Debugging in Defold
brief: Dieses Handbuch erläutert die in Defold verfügbaren Debugging-Funktionen.
---

# Spiellogik debuggen {#debugging-game-logic}

Defold enthält einen integrierten Lua-Debugger mit Möglichkeiten zur Untersuchung des Spielzustands. Zusammen mit den integrierten [Profiling-Werkzeugen](/manuals/profiling) ist er ein leistungsfähiges Werkzeug, mit dem du die Ursache von Fehlern in deiner Spiellogik finden oder Leistungsprobleme analysieren kannst.

## Debugging mit Ausgaben und visuellen Hilfen {#print-and-visual-debugging}

Die einfachste Möglichkeit, dein Spiel in Defold zu debuggen, ist [Debugging mit Ausgaben](http://en.wikipedia.org/wiki/Debugging#Techniques). Verwende `print()`- oder [`pprint()`](/ref/builtins#pprint)-Anweisungen, um Variablen zu beobachten oder den Ausführungsablauf sichtbar zu machen. Wenn sich ein Spielobjekt (game object) ohne Skript ungewöhnlich verhält, kannst du ihm ein Skript hinzufügen, das ausschließlich der Fehlersuche dient. Jede der Ausgabefunktionen schreibt in die Ansicht *Console* im Editor und in das [Spielprotokoll](/manuals/debugging-game-and-system-logs).

Zusätzlich zu Ausgaben kann die Engine auch Debug-Text und gerade Linien auf dem Bildschirm zeichnen. Dazu sendest du Nachrichten an den Socket `@render`:

```lua
-- Draw value of "my_val" with debug text on the screen
msg.post("@render:", "draw_text", { text = "My value: " .. my_val, position = vmath.vector3(200, 200, 0) })

-- Draw colored text on the screen
local color_green = vmath.vector4(0, 1, 0, 1)
msg.post("@render:", "draw_debug_text", { text = "Custom color", position = vmath.vector3(200, 180, 0), color = color_green })

-- Draw debug line between player and enemy on the screen
local start_p = go.get_position("player")
local end_p = go.get_position("enemy")
local color_red = vmath.vector4(1, 0, 0, 1)
msg.post("@render:", "draw_line", { start_point = start_p, end_point = end_p, color = color_red })
```

Die Nachrichten für das visuelle Debugging fügen der Rendering-Pipeline Daten hinzu, die als Teil der regulären Rendering-Pipeline gezeichnet werden.

* `"draw_line"` fügt Daten hinzu, die mit der Funktion `render.draw_debug3d()` im Render-Skript gerendert werden.
* `"draw_text"` wird mit der Schriftressource `/builtins/fonts/debug/always_on_top.font` gerendert, die das Material `/builtins/fonts/debug/always_on_top_font.material` verwendet.
* `"draw_debug_text"` entspricht `"draw_text"`, wird aber in einer benutzerdefinierten Farbe gerendert.

Beachte, dass du diese Daten wahrscheinlich in jedem Frame aktualisieren möchtest. Daher bietet es sich an, die Nachrichten in der Funktion `update()` zu senden.

## Den Debugger starten {#running-the-debugger}

Der Lua-Debugger ist in nativen Debug- und Headless-Builds verfügbar. Verwende eine Engine derselben Defold-Version wie der Editor. Release- und Web-Builds unterstützen das Verbinden eines Debuggers nicht.

Wähle <kbd>Debug ▸ Start/Attach</kbd>, um den Debugger zu starten. Dadurch wird das Spiel mit verbundenem Debugger gestartet oder der Debugger mit einem bereits laufenden Spiel verbunden. Beim Start zum Debuggen richtet der Editor aktivierte Haltepunkte ein, bevor die Startskripte ausgeführt werden. Du kannst daher vor dem Start einen Haltepunkt in `init()` setzen.

Um den Debugger mit einem Gerät zu verbinden, wähle es unter <kbd>Project ▸ Targets</kbd> und anschließend <kbd>Debug ▸ Start/Attach</kbd> aus. Die Ausführung hält bei der nächsten Lua-Zeile an. Der Editor richtet die Debugger-Verbindung für unterstützte lokale und entfernte Ziele automatisch ein. Die Verbindungsanforderungen stehen unter [Entfernte Ziele](#remote-targets); außerdem kannst du einen [externen Debugger verbinden](#native-dap-connections).

![Übersicht](images/debugging/overview.png)

Sobald der Debugger verbunden ist, kannst du die Ausführung des Spiels über die Debugger-Schaltflächen in der Konsole oder über das Menü <kbd>Debug</kbd> steuern:

Break
: ![Pausieren](images/debugging/pause.svg){width=60px .left}
  Hält die Lua-Ausführung bei der nächsten Quellcodezeile an. Du kannst nun den Spielzustand untersuchen, das Spiel schrittweise ausführen oder bis zum nächsten Haltepunkt fortsetzen. Die aktuelle Ausführungsposition wird im Codeeditor markiert:

  ![Skript](images/debugging/script.png)

Continue
: ![Fortsetzen](images/debugging/play.svg){width=60px .left}
  Setze die Ausführung des Spiels fort. Der Spielcode läuft weiter, bis du entweder auf die Pause-Schaltfläche klickst oder die Ausführung einen von dir gesetzten Haltepunkt erreicht. Wenn die Ausführung an einem gesetzten Haltepunkt anhält, wird die Ausführungsstelle im Code-Editor über der Haltepunktmarkierung angezeigt:

  ![Unterbrechung](images/debugging/break.png)

Stop
: ![Beenden](images/debugging/stop.svg){width=60px .left}
  Beende den Debugger. Wenn du diese Schaltfläche drückst, wird der Debugger sofort beendet, vom Spiel getrennt und das laufende Spiel beendet.

Step Over
: ![Aufruf ohne Einsteigen ausführen](images/debugging/step_over.svg){width=60px .left}
  Führe das Programm einen Schritt weiter aus. Wenn dabei eine weitere Lua-Funktion aufgerufen wird, _steigt die Ausführung nicht in diese Funktion ein_, sondern läuft weiter und hält in der nächsten Zeile unterhalb des Funktionsaufrufs an. Wenn du in diesem Beispiel „step over“ drückst, führt der Debugger den Code aus und hält an der `end`-Anweisung unterhalb der Zeile mit dem Aufruf der Funktion `nextspawn()` an:

  ![Schritt](images/debugging/step.png)

::: sidenote
Die schrittweise Ausführung folgt den Lua-Quellcodezeilen. Ein Schritt kann dieselbe Zeile erneut erreichen, etwa bei einer wiederholten Schleife; er führt daher nicht immer zur nächsten Zeile der Datei.
:::

Step Into
: ![In einen Aufruf einsteigen](images/debugging/step_in.svg){width=60px .left}
  Führe das Programm einen Schritt weiter aus. Wenn dabei eine weitere Lua-Funktion aufgerufen wird, _steigt die Ausführung in diese Funktion ein_. Der Funktionsaufruf fügt dem Aufrufstapel einen Eintrag hinzu. Du kannst jeden Eintrag in der Liste des Aufrufstapels anklicken, um die Eintrittsstelle und den Inhalt aller Variablen in dieser Closure anzuzeigen. Hier wurde in die Funktion `nextspawn()` eingestiegen:

  ![In eine Funktion einsteigen](images/debugging/step_into.png)

Step Out
: ![Bis zum Rücksprung ausführen](images/debugging/step_out.svg){width=60px .left}
  Setze die Ausführung fort, bis die aktuelle Funktion zurückkehrt. Wenn du bei der Ausführung in eine Funktion eingestiegen bist, setzt die Schaltfläche „step out“ die Ausführung fort, bis die Funktion zurückkehrt.

Haltepunkte setzen und entfernen
: Du kannst beliebig viele Haltepunkte in deinem Lua-Code setzen. Wenn das Spiel mit verbundenem Debugger läuft, hält es die Ausführung am nächsten erreichten Haltepunkt an und wartet auf weitere Eingaben von dir.

  ![Haltepunkt hinzufügen](images/debugging/add_breakpoint.png)

  Um einen Haltepunkt zu setzen oder zu entfernen, klicke im Code-Editor in die Spalte direkt rechts neben den Zeilennummern. Du kannst auch <kbd>Edit ▸ Toggle Breakpoint</kbd> im Menü wählen.

Haltepunkte deaktivieren und aktivieren
: Haltepunkte können vorübergehend deaktiviert werden, ohne sie zu entfernen. Wenn sie deaktiviert sind, werden sie während der Ausführung ignoriert, können aber jederzeit wieder aktiviert werden. Klicke mit der rechten Maustaste auf den Haltepunkt am Rand des Code-Editors und schalte dann das Kontrollkästchen `Enabled` um. Deaktivierte Haltepunkte werden unausgefüllt dargestellt, um anzuzeigen, dass sie inaktiv sind.

  ![Haltepunkt deaktivieren](images/debugging/disable_breakpoint.png)

Bedingte Haltepunkte setzen
: Du kannst für deinen Haltepunkt eine Bedingung festlegen, die den Wert true ergeben muss, damit der Haltepunkt ausgelöst wird. Die Bedingung kann auf lokale Variablen zugreifen, die während der Codeausführung in dieser Zeile verfügbar sind.

  ![Haltepunkt bearbeiten](images/debugging/edit_breakpoint.png)

  Um die Bedingung des Haltepunkts zu bearbeiten, klicke im Code-Editor mit der rechten Maustaste in die Spalte direkt rechts neben den Zeilennummern oder wähle <kbd>Edit ▸ Edit Breakpoint</kbd> im Menü.

Lua-Ausdrücke auswerten
: Wähle bei angehaltenem Spiel einen Frame in *Call Stack*, gib unten in der Konsole einen Lua-Ausdruck oder eine Lua-Anweisung ein und drücke <kbd>Enter</kbd>. Die Auswertung verwendet die lokalen Variablen, Upvalues und globalen Variablen des ausgewählten Frames. Ergebnisse in Form von Tabellen enthalten auch deren verschachtelte Inhalte.

  ![Konsole](images/debugging/console.png)

  Du kannst Werte auch durch Zuweisungen ändern, beispielsweise mit `self.score = 100` in einem Frame, in dem `self` verfügbar ist. Ausgewerteter Code wirkt sich genauso auf den Spielzustand aus wie Code, den dein Spiel ausführt.

Variablen untersuchen
: Wähle einen Frame in *Call Stack*, um seine lokalen Variablen und Upvalues in der Ansicht *Variables* zu untersuchen. Klappe `_G` auf, um globale Variablen anzuzeigen, sowie Tabellen oder `self`, um deren Felder zu untersuchen. Beim schrittweisen Ausführen, Wechseln des Frames oder Aktualisieren nach einer Auswertung erhält der Editor aufgeklappte Pfade, Auswahl und Scrollposition und ruft dabei die aktuellen Werte ab.

Den Debugger trennen
: Wähle <kbd>Debug ▸ Detach Debugger</kbd>, um den Debugger vom Spiel zu trennen. Das Spiel wird sofort fortgesetzt. Mit <kbd>Debug ▸ Start/Attach</kbd> verbindest du den Debugger erneut, ohne das Spiel neu zu starten.

## Native DAP-Verbindungen {#native-dap-connections}

Die Engine stellt einen nativen Server für das Debug Adapter Protocol (DAP) über TCP bereit. Starte für einen externen DAP-Client den Listener in einer nativen Defold-Debug- oder Headless-Engine und verbinde den Client anschließend mit deren Adresse und Port. Bei <kbd>Debug ▸ Start/Attach</kbd> richtet der Editor den Listener automatisch ein.

Der aktuelle Editor kann sich nicht mit älteren Engines verbinden, die nur MobDebug unterstützen. Ein Aufruf von `require "builtins.scripts.mobdebug"` ist in aktuellen Versionen weder erforderlich noch verfügbar.

### Den Listener starten {#starting-the-listener}

Erstelle zunächst einen Build deines Projekts. Starte die native Debug-Engine aus dem Projektverzeichnis, das `build/default/game.projectc` enthält, mit diesen [Konfigurationsüberschreibungen beim Start](/manuals/project-settings/#setting-config-values-on-engine-startup):

```sh
dmengine --config=debugger.enabled=1 \
  --config=debugger.port=8172 --config=debugger.wait=1
```

Verbinde deinen DAP-Client mit `127.0.0.1:8172`. Die Engine wartet darauf, dass der Client die Haltepunkte konfiguriert, bevor sie die Startskripte ausführt.

| Einstellung | Standard | Zweck |
| --- | --- | --- |
| `debugger.enabled` | `0` | Setze den Wert auf `1`, um den Listener beim Start der Engine zu starten. |
| `debugger.address` | `127.0.0.1` | IPv4-Adresse, auf der gelauscht wird. Der Standardwert akzeptiert Verbindungen vom selben Computer. |
| `debugger.port` | `8172` | TCP-Port des Listeners. Verwende `0`, um einen verfügbaren Port auszuwählen. |
| `debugger.wait` | `0` | Setze den Wert auf `1`, um vor der Ausführung der Startskripte auf die Konfiguration des Debugger-Clients zu warten. |

Du kannst diese Werte auch im [Abschnitt Debugger von game.project](/manuals/project-settings/#debugger) eintragen. Für <kbd>Debug ▸ Start/Attach</kbd> konfiguriert der Editor den Listener automatisch; eine manuelle Konfiguration ist daher nur nötig, wenn du den Listener selbst startest.

Das Engine-Protokoll meldet die ausgewählte Adresse und den Port. Mit `debugger.wait=0` startet das Spiel sofort, und du kannst den Debugger später verbinden. Mit `debugger.wait=1` wartet es, bis der Client die Sitzung einschließlich der Haltepunkte konfiguriert hat. Bei lokalen Debug-Starts wählt der Editor automatisch einen verfügbaren Port.

Wird ein Client getrennt, wird die Ausführung fortgesetzt, und der Listener bleibt für eine neue Verbindung verfügbar. Auch das Trennen während des Wartens auf die Startkonfiguration gibt die Engine frei. Kann der Listener nicht starten, protokolliert die Engine den Fehler und setzt den Start fort; du kannst mit `debugger.start(0)` aus Lua einen neuen Versuch mit einem verfügbaren Port starten.

### Den Listener während der Ausführung aktivieren {#enabling-the-listener-while-running}

So aktivierst du den Listener aus einem Skript, ohne das Spiel neu zu starten:

```lua
if debugger then
    local port = debugger.start(0)
    print("DAP listener port:", port)
end
```

`debugger.start([port [, address]])` gibt den Listener-Port sofort zurück. Die Funktion wartet weder auf einen Client noch hält sie das Spiel an. Nicht angegebene Argumente verwenden `debugger.port` und `debugger.address`; mit `0` wird ein verfügbarer Port ausgewählt. Wiederholte Aufrufe geben den Port des bestehenden Listeners zurück und ändern dessen Adresse oder Port nicht. Das Modul `debugger` wird von nativen Debug- und Headless-Engines bereitgestellt.

Der Port muss eine Ganzzahl zwischen `0` und `65535` sein. Übergib als erstes Argument `nil`, um nur die Adresse zu überschreiben. Ungültige Argumente oder ein Fehler beim Binden des Listeners lösen einen Lua-Fehler aus.

### Entfernte Ziele {#remote-targets}

Binde den Listener für eine direkte Verbindung von einem anderen Computer an die IPv4-Schnittstelle des Geräts oder an `0.0.0.0` (alle IPv4-Schnittstellen). Verwende beispielsweise `debugger.start(8172, "0.0.0.0")` oder ergänze den obigen Startbefehl um `--config=debugger.address=0.0.0.0`. Verbinde den Client mit der tatsächlichen IP-Adresse des Geräts und erlaube TCP-Zugriff auf den Listener-Port. `0.0.0.0` ist eine Bindeadresse und nicht die Adresse, die im Client eingetragen wird.

Der Defold-Editor fordert diese entfernte Bindung automatisch an und verwendet für entfernte Ziele den Port `8172 + project.instance_index`. Einen dynamisch ausgewählten entfernten Port kann er nicht ermitteln. Falls du den entfernten Listener bereits auf localhost oder einem anderen Port gestartet hast, starte die Engine vor dem Verbinden über den Editor neu.

Der Debugger kann Lua auswerten und besitzt keine Authentifizierung. Aktiviere den Fernzugriff nur in einem vertrauenswürdigen Entwicklungsnetzwerk.

### Externe Clients {#external-clients}

Verwende einen Client, der sich direkt über TCP mit einem DAP-Server verbinden kann. Konfiguriere seine Quellcodezuordnung für den Ordner mit `game.project` (das DAP-Attach-Argument `localRoot`). Starte zuerst den Listener der Engine und verbinde anschließend den Client.

#### VS Code

Installiere die [Erweiterung Lua Debug](https://marketplace.visualstudio.com/items?itemName=actboy168.lua-debug) (`actboy168.lua-debug`), öffne den Ordner mit `game.project` in VS Code und ergänze `.vscode/launch.json` um diese Konfiguration:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to Defold Lua",
      "type": "lua",
      "request": "attach",
      "address": "127.0.0.1:8172",
      "debugServer": 8172,
      "localRoot": "${workspaceFolder}",
      "stopOnEntry": false
    }
  ]
}
```

Wenn VS Code eine Datei vom Typ `.script`, `.gui_script` oder `.render_script` als einfachen Text öffnet, wähle in der Sprachanzeige der Statusleiste **Lua** aus, bevor du Haltepunkte setzt.

Setze einen Haltepunkt, beispielsweise in der Funktion `init()` eines Skripts. Starte die Engine mit dem [obigen Startbefehl](#starting-the-listener) und wähle anschließend **Attach to Defold Lua** in der Ansicht **Run and Debug** von VS Code. Mit `debugger.wait=1` führt die Engine Startskripte aus, nachdem der Client die Haltepunkte eingerichtet hat. Setze `stopOnEntry` auf `true`, wenn du nach dem Verbinden zusätzlich bei der nächsten Lua-Zeile anhalten möchtest.

Die [Einstellung `debugServer`](https://code.visualstudio.com/api/extension-guides/debugger-extension#development-setup-for-mock-debug) von VS Code verbindet sich direkt mit dem lokalen TCP-Listener der Engine. Das Feld `address` wird von der Attach-Konfiguration der Lua-Debug-Erweiterung benötigt. Ändere beide Felder, wenn du den Listener-Port änderst. `localRoot` muss auf den Projektordner zeigen, damit der Client die Lua-Quellcodenamen der Engine deinen Dateien zuordnen kann.

Leite bei einer entfernten Engine deren DAP-Port an localhost weiter und trage den weitergeleiteten Port in beide Felder ein, oder verwende einen DAP-Client, der sich direkt mit dem entfernten Host verbindet.

## Registerkarte Breakpoints {#breakpoints-tab}

  ![Registerkarte Breakpoints](images/debugging/breakpoints_tab.png)

  Wenn du mit mehreren Haltepunkten in verschiedenen Skripten arbeitest, bietet die Registerkarte Breakpoints eine zentrale Ansicht, in der du alle deine Haltepunkte an einem Ort verwalten kannst.

##### Einzelne Haltepunkte steuern {#individual-breakpoint-controls}

  Für die Arbeit mit einzelnen Haltepunkten:
  - Klicke auf das rote Papierkorbsymbol, um einen Haltepunkt zu entfernen
  - Doppelklicke auf die Zeile (außerhalb des Bedingungsbereichs), um in der Code View zu dieser Zeile zu springen
  - Doppelklicke auf die Bedingungszelle oder klicke auf das Stiftsymbol, um bedingte Haltepunkte zu bearbeiten
  - Klicke auf die Schaltfläche X zum Löschen, während du den Mauszeiger über eine Bedingungszelle hältst, um die Bedingung zu entfernen

##### Mehrere Haltepunkte gleichzeitig bearbeiten {#batch-operations}

  Wähle mehrere Haltepunkte mit Ctrl/Cmd+click oder Shift+click aus und klicke dann mit der rechten Maustaste, um Aktionen auf mehrere Haltepunkte anzuwenden. Du kannst die Bedingungen mehrerer Haltepunkte gleichzeitig bearbeiten, ihren Aktivierungszustand umschalten oder sie vollständig entfernen.

  Mit den Schaltflächen der Werkzeugleiste kannst du alle Haltepunkte auf einmal aktivieren, deaktivieren oder umschalten. Das ist nützlich, wenn du dein Spiel ohne Unterbrechungen ausführen möchtest, aber die Positionen der Haltepunkte beibehalten willst. Du kannst auch alle entfernen, wenn du deine Debugging-Sitzung beendet hast.

## Lua-Debug-Bibliothek {#lua-debug-library}

Lua enthält eine Debug-Bibliothek, die in manchen Situationen nützlich ist, insbesondere wenn du das Innenleben deiner Lua-Umgebung untersuchen musst. Weitere Informationen findest du im [Kapitel zur Debug-Bibliothek im Lua-Handbuch](http://www.lua.org/pil/contents.html#23).

## Checkliste zur Fehlersuche {#debugging-checklist}

Wenn ein Fehler auftritt oder sich dein Spiel nicht wie erwartet verhält, hilft dir diese Checkliste zur Fehlersuche:

1. Prüfe die Konsolenausgabe und stelle sicher, dass keine Laufzeitfehler auftreten.

2. Füge deinem Code `print`-Anweisungen hinzu, um zu prüfen, ob der Code tatsächlich ausgeführt wird.

3. Wenn er nicht ausgeführt wird, prüfe, ob du im Editor die für seine Ausführung erforderlichen Einstellungen vorgenommen hast. Ist das Skript dem richtigen Spielobjekt hinzugefügt? Hat dein Skript den Eingabefokus erhalten? Sind die Eingabeauslöser korrekt? Ist der Shader-Code dem Material hinzugefügt? Und so weiter.

4. Wenn dein Code von den Werten von Variablen abhängt (beispielsweise in einer if-Anweisung), gib diese Werte entweder mit `print` dort aus, wo sie verwendet oder geprüft werden, oder untersuche sie mit dem Debugger.

Manchmal kann die Fehlersuche schwierig und zeitaufwendig sein. Dann musst du deinen Code Stück für Stück durchgehen, alles prüfen, den fehlerhaften Code eingrenzen und Fehlerquellen ausschließen. Das gelingt am besten mit einer Methode namens „Teile und herrsche“:

1. Ermittle, welche Hälfte (oder welcher kleinere Teil) des Codes den Fehler enthalten muss.
2. Ermittle erneut, welche Hälfte dieser Hälfte den Fehler enthalten muss.
3. Grenze den Code, der den Fehler verursachen muss, weiter ein, bis du ihn findest.

Viel Erfolg bei der Fehlersuche!

## Physikprobleme debuggen {#debugging-problems-with-physics}

Wenn du Probleme mit der Physik hast und Kollisionen nicht wie erwartet funktionieren, empfiehlt es sich, das Physik-Debugging zu aktivieren. Aktiviere das Kontrollkästchen *Debug* im Abschnitt *Physics* der Datei *game.project*:

![Einstellung für Physik-Debugging](images/debugging/physics_debug_setting.png)

Wenn dieses Kontrollkästchen aktiviert ist, zeichnet Defold alle Kollisionsformen und Kontaktpunkte von Kollisionen:

![Visualisierung für Physik-Debugging](images/debugging/physics_debug_visualisation.png)
