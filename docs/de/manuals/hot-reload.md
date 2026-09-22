---
title: Hot Reload
brief: Dieses Handbuch erklärt die Hot-Reload-Funktion in Defold.
---

# Ressourcen per Hot Reload neu laden {#hot-reloading-resources}

Defold ermöglicht es dir, Ressourcen (resources) per Hot Reload neu zu laden. Bei der Entwicklung eines Spiels beschleunigt diese Funktion bestimmte Aufgaben enorm. Du kannst damit Code und Inhalte eines Spiels ändern, während es läuft. Häufige Anwendungsfälle sind:

- Gameplay-Parameter in Lua-Skripten anpassen.
- Grafische Elemente (wie Partikeleffekte oder GUI-Elemente) bearbeiten und anpassen und die Ergebnisse im passenden Kontext betrachten.
- Shader-Code bearbeiten und anpassen und die Ergebnisse im passenden Kontext betrachten.
- Das Testen des Spiels erleichtern, indem du Level neu startest, Zustände festlegst und ähnliche Aktionen ausführst---ohne das Spiel anzuhalten.

## Hot Reload verwenden {#how-to-hot-reload}

Starte dein Spiel über den Editor (<kbd>Project ▸ Build</kbd>).

Um anschließend eine aktualisierte Ressource neu zu laden, wähle einfach den Menüpunkt <kbd>File ▸ Hot Reload</kbd> oder drücke die entsprechende Tastenkombination:

![Ressourcen neu laden](images/hot-reload/menu.png)

## Hot Reload auf Geräten {#hot-reloading-on-device}

Hot Reload funktioniert sowohl auf Geräten als auch auf Desktop-Computern. Um es auf einem Gerät zu verwenden, starte einen Debug-Build deines Spiels oder die [Entwicklungs-App](/manuals/dev-app) auf deinem Mobilgerät und wähle es anschließend im Editor als Ziel aus:

![Zielgerät](images/hot-reload/target.png)

Wenn du nun einen Build erstellst und startest, überträgt der Editor alle Assets an die laufende App auf dem Gerät und startet das Spiel. Ab diesem Zeitpunkt wird jede Datei, die du per Hot Reload neu lädst, auf dem Gerät aktualisiert.

Wenn du beispielsweise einer GUI, die in einem laufenden Spiel auf deinem Smartphone angezeigt wird, ein paar Schaltflächen hinzufügen möchtest, öffne einfach die GUI-Datei:

![GUI neu laden](images/hot-reload/gui.png)

Füge die neuen Schaltflächen hinzu, speichere die GUI-Datei und lade sie per Hot Reload neu. Die neuen Schaltflächen sind jetzt auf dem Bildschirm des Smartphones zu sehen:

![Neu geladene GUI](images/hot-reload/gui-reloaded.png)

Wenn du eine Datei per Hot Reload neu lädst, gibt die Engine jede neu geladene Ressourcendatei in der Konsole aus.

## Skripte neu laden {#reloading-scripts}

Jede neu geladene Lua-Skriptdatei wird in der laufenden Lua-Umgebung erneut ausgeführt.

```lua
local my_value = 10

function update(self, dt)
    print(my_value)
end
```

Wenn du `my_value` auf 11 änderst und die Datei per Hot Reload neu lädst, wirkt sich das sofort aus:

```text
...
DEBUG:SCRIPT: 10
DEBUG:SCRIPT: 10
DEBUG:SCRIPT: 10
INFO:RESOURCE: /main/hunter.scriptc was successfully reloaded.
DEBUG:SCRIPT: 11
DEBUG:SCRIPT: 11
DEBUG:SCRIPT: 11
...
```

Beachte, dass Hot Reload die Ausführung der Lebenszyklusfunktionen nicht verändert. Beispielsweise wird `init()` bei einem Hot Reload nicht aufgerufen. Wenn du die Lebenszyklusfunktionen neu definierst, werden jedoch die neuen Versionen verwendet.

## Lua-Module neu laden {#reloading-lua-modules}

Solange du Variablen in einer Moduldatei zum globalen Gültigkeitsbereich hinzufügst, werden diese globalen Variablen beim erneuten Laden der Datei geändert:

```lua
--- my_module.lua
my_module = {}
my_module.val = 10
```

```lua
-- user.script
require "my_module"

function update(self, dt)
    print(my_module.val) -- hot reload "my_module.lua" and the new value will print
end
```

Ein gängiges Muster für Lua-Module besteht darin, eine lokale Tabelle zu erstellen, sie mit Werten zu füllen und anschließend zurückzugeben:

```lua
--- my_module.lua
local M = {} -- a new table object is created here
M.val = 10
return M
```

```lua
-- user.script
local mm = require "my_module"

function update(self, dt)
    print(mm.val) -- will print 10 even if you change and hot reload "my_module.lua"
end
```

Das Ändern und erneute Laden von `my_module.lua` verändert das Verhalten von `user.script` _nicht_. Im [Handbuch zu Modulen](/manuals/modules) erfährst du mehr darüber, warum das so ist und wie du diese Falle vermeidest.

## Die Funktion on_reload() {#the-on_reload-function}

Jede Skriptkomponente (script component) kann eine Funktion `on_reload()` definieren. Wenn sie vorhanden ist, wird sie jedes Mal aufgerufen, wenn das Skript neu geladen wird. Das ist nützlich, um Daten zu untersuchen oder zu ändern, Nachrichten zu senden und ähnliche Aufgaben auszuführen:

```lua
function on_reload(self)
    print(self.velocity)

    msg.post("/level#controller", "setup")
end
```

## Shader-Code neu laden {#reloading-shader-code}

Beim erneuten Laden von Vertex- und Fragment-Shadern kompiliert der Grafiktreiber den GLSL-Code neu und überträgt ihn an die GPU. Wenn der Shader-Code einen Absturz verursacht, stürzt auch die Engine ab. Das kann leicht passieren, da GLSL-Code auf einer sehr niedrigen Abstraktionsebene arbeitet.
