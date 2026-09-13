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

Um den Debugger zu starten, wähle <kbd>Debug ▸ Start/Attach</kbd>. Dadurch wird entweder das Spiel mit verbundenem Debugger gestartet oder der Debugger mit einem bereits laufenden Spiel verbunden.

![Übersicht](images/debugging/overview.png)

Sobald der Debugger verbunden ist, kannst du die Ausführung des Spiels über die Debugger-Schaltflächen in der Konsole oder über das Menü <kbd>Debug</kbd> steuern:

Break
: ![Pausieren](images/debugging/pause.svg){width=60px .left}
  Unterbrich die Ausführung des Spiels sofort. Das Spiel hält an der aktuellen Stelle an. Du kannst nun den Spielzustand untersuchen, das Spiel schrittweise ausführen oder es bis zum nächsten Haltepunkt weiterlaufen lassen. Die aktuelle Ausführungsstelle wird im Code-Editor markiert:

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
Eine Zeile Lua-Code entspricht nicht einem einzelnen Ausdruck. Beim schrittweisen Ausführen im Debugger wird jeweils ein Ausdruck weitergegangen. Das bedeutet, dass du derzeit die Schaltfläche für einen Schritt möglicherweise mehr als einmal drücken musst, um zur nächsten Zeile zu gelangen.
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
: Wenn der Debugger verbunden ist und das Spiel an einem Haltepunkt angehalten wurde, steht eine Lua-Laufzeitumgebung mit dem aktuellen Kontext zur Verfügung. Gib unten in der Konsole Lua-Ausdrücke ein und drücke <kbd>Enter</kbd>, um sie auszuwerten:

  ![Konsole](images/debugging/console.png)

  Derzeit ist es nicht möglich, Variablen über diese Auswertung zu ändern.

Den Debugger trennen
: Wähle <kbd>Debug ▸ Detach Debugger</kbd>, um den Debugger vom Spiel zu trennen. Das Spiel läuft sofort weiter.

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
