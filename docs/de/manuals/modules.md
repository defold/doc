---
title: Lua-Module in Defold
brief: Mit Lua-Modulen kannst du dein Projekt strukturieren und wiederverwendbaren Bibliothekscode erstellen. Dieses Handbuch erklärt, wie das in Defold funktioniert.
---

# Lua-Module {#lua-modules}

Mit Lua-Modulen kannst du dein Projekt strukturieren und wiederverwendbaren Bibliothekscode erstellen. Im Allgemeinen ist es sinnvoll, Duplizierungen in deinen Projekten zu vermeiden. Defold ermöglicht es dir, mit der Modulfunktionalität von Lua Skriptdateien in andere Skriptdateien einzubinden. So kannst du Funktionalität (und Daten) in einer externen Skriptdatei kapseln und sie in Skriptdateien für Spielobjekte (game objects) und GUIs wiederverwenden.

## Lua-Dateien mit require laden {#requiring-lua-files}

Lua-Code, der in Dateien mit der Dateierweiterung `.lua` an beliebiger Stelle in der Struktur deines Spielprojekts gespeichert ist, kann mit `require` in Skript- und GUI-Skriptdateien geladen werden. Um eine neue Lua-Moduldatei zu erstellen, klicke in der Ansicht *Assets* mit der rechten Maustaste auf den Ordner, in dem du sie erstellen möchtest, und wähle dann <kbd>New... ▸ Lua Module</kbd>. Gib der Datei einen eindeutigen Namen und drücke <kbd>Ok</kbd>:

![Neue Datei](images/modules/new_name.png)

Angenommen, du fügst der Datei „`main/anim.lua`“ den folgenden Code hinzu:

```lua
function direction_animation(direction, char)
    local d = ""
    if direction.x > 0 then
        d = "right"
    elseif direction.x < 0 then
        d = "left"
    elseif direction.y > 0 then
        d = "up"
    elseif direction.y < 0 then
        d = "down"
    end
    return hash(char .. "-" .. d)
end
```

Dann kann jedes Skript diese Datei mit `require` laden und die Funktion verwenden:

```lua
require "main.anim"

function update(self, dt)
    -- update position, set direction etc
    ...

    -- set animation
    local anim = direction_animation(self.dir, "player")
    if anim ~= self.current_anim then
        sprite.play_flipbook("#sprite", anim)
        self.current_anim = anim
    end
end
```

Die Funktion `require` lädt das angegebene Modul. Zuerst prüft sie anhand der Tabelle `package.loaded`, ob das Modul bereits geladen ist. Falls ja, gibt `require` den unter `package.loaded[module_name]` gespeicherten Wert zurück. Andernfalls lädt sie die Datei über eine Ladefunktion und wertet sie aus.

Die Syntax der Dateinamenzeichenfolge, die du an `require` übergibst, hat eine Besonderheit. Lua ersetzt die Zeichen `.` in der Dateinamenzeichenfolge durch Pfadtrennzeichen: `/` unter macOS und Linux und `\\` unter Windows.

Beachte, dass es in der Regel keine gute Idee ist, wie oben den globalen Gültigkeitsbereich zum Speichern von Zustand und Definieren von Funktionen zu verwenden. Du riskierst Namenskonflikte, legst den Zustand des Moduls offen oder erzeugst eine Kopplung zwischen den Stellen, die das Modul verwenden.

## Module {#modules}

Um Daten und Funktionen zu kapseln, verwendet Lua _Module_. Ein Lua-Modul ist eine gewöhnliche Lua-Tabelle, die Funktionen und Daten enthält. Die Tabelle wird lokal deklariert, um den globalen Gültigkeitsbereich nicht mit zusätzlichen Namen zu belegen:

```lua
local M = {}

-- private
local message = "Hello world!"

function M.hello()
    print(message)
end

return M
```

Anschließend kannst du das Modul verwenden. Auch hier solltest du es vorzugsweise einer lokalen Variablen zuweisen:

```lua
local m = require "mymodule"
m.hello() --> "Hello world!"
```

## Module mit Hot Reload neu laden {#hot-reloading-modules}

Betrachte ein einfaches Modul:

```lua
-- module.lua
local M = {} -- creates a new table in the local scope
M.value = 4711
return M
```

Und Code, der dieses Modul verwendet: 

```lua
local m = require "module"
print(m.value) --> "4711" (even if "module.lua" is changed and hot reloaded)
```

Wenn du die Moduldatei mit Hot Reload neu lädst, wird der Code erneut ausgeführt, aber `m.value` bleibt unverändert. Woran liegt das?

Erstens wird die Tabelle in `module.lua` im lokalen Gültigkeitsbereich erstellt, und eine _Referenz_ auf diese Tabelle wird an den aufrufenden Code zurückgegeben. Beim erneuten Laden von `module.lua` wird der Modulcode erneut ausgewertet. Dabei entsteht jedoch eine neue Tabelle im lokalen Gültigkeitsbereich, anstatt die Tabelle zu aktualisieren, auf die `m` verweist.

Zweitens speichert Lua Dateien, die mit `require` geladen werden, im Cache. Beim ersten Laden einer Datei wird sie in der Tabelle [`package.loaded`](/ref/package/#package.loaded) abgelegt, damit sie bei nachfolgenden Aufrufen von `require` schneller gelesen werden kann. Du kannst das erneute Einlesen einer Datei vom Datenträger erzwingen, indem du den Eintrag der Datei auf `nil` setzt: `package.loaded["my_module"] = nil`.

Damit Hot Reload bei einem Modul korrekt funktioniert, musst du das Modul neu laden, den Cache zurücksetzen und dann alle Dateien neu laden, die das Modul verwenden. Das ist alles andere als optimal.

Stattdessen kannst du _während der Entwicklung_ eine Behelfslösung verwenden: Lege die Modultabelle im globalen Gültigkeitsbereich ab und lasse `M` auf die globale Tabelle verweisen, anstatt bei jeder Auswertung der Datei eine neue Tabelle zu erstellen. Das erneute Laden des Moduls ändert dann den Inhalt der globalen Tabelle:

```lua
--- module.lua

-- Replace with local M = {} when done
uniquevariable12345 = uniquevariable12345 or {}
local M = uniquevariable12345

M.value = 4711
return M
```

## Module und Zustand {#modules-and-state}

Zustandsbehaftete Module speichern einen internen Zustand, den sich alle Stellen teilen, die das Modul verwenden. Sie lassen sich mit Singletons vergleichen:

```lua
local M = {}

-- all users of the module will share this table
local state = {}

function M.do_something(foobar)
    table.insert(state, foobar)
end

return M
```

Ein zustandsloses Modul speichert dagegen keinen internen Zustand. Stattdessen bietet es einen Mechanismus, um den Zustand in eine separate Tabelle auszulagern, die beim aufrufenden Code lokal ist. Dafür gibt es verschiedene Umsetzungsmöglichkeiten:

Eine Zustandstabelle verwenden
: Der vielleicht einfachste Ansatz ist eine Konstruktorfunktion, die eine neue Tabelle zurückgibt, die nur den Zustand enthält. Der Zustand wird dem Modul explizit als erster Parameter jeder Funktion übergeben, die die Zustandstabelle verändert.

  ```lua
  local M = {}
  
  function M.alter_state(the_state, v)
      the_state.value = the_state.value + v
  end
  
  function M.get_state(the_state)
      return the_state.value
  end
  
  function M.new(v)
      local state = {
          value = v
      }
      return state
  end
  
  return M
  ```
  
  Verwende das Modul so:
  
  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  m.alter_state(my_state, 1)
  print(m.get_state(my_state)) --> 43
  ```

Metatabellen verwenden
: Ein weiterer Ansatz ist eine Konstruktorfunktion, die bei jedem Aufruf eine neue Tabelle mit dem Zustand und den öffentlichen Funktionen des Moduls zurückgibt:

  ```lua
  local M = {}
  
  function M:alter_state(v)
      -- self is added as first argument when using : notation
      self.value = self.value + v
  end
  
  function M:get_state()
      return self.value
  end
  
  function M.new(v)
      local state = {
          value = v
      }
      return setmetatable(state, { __index = M })
  end
  
  return M
  ```

  Verwende das Modul so:

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state:alter_state(1) -- "my_state" is added as first argument when using : notation
  print(my_state:get_state()) --> 43
  ```

Closures verwenden
:  Eine dritte Möglichkeit besteht darin, eine Closure zurückzugeben, die den gesamten Zustand und alle Funktionen enthält. Du musst die Instanz nicht wie bei Metatabellen als Argument übergeben (weder explizit noch implizit mit dem Doppelpunktoperator). Diese Methode ist außerdem etwas schneller als die Verwendung von Metatabellen, da Funktionsaufrufe nicht über die Metamethoden `__index` laufen müssen. Allerdings enthält jede Closure eine eigene Kopie der Methoden, weshalb der Speicherverbrauch höher ist.

  ```lua
  local M = {}
  
  function M.new(v)
      local state = {
          value = v
      }
  
      state.alter_state = function(v)
          state.value = state.value + v
      end
  
      state.get_state = function()
          return state.value
      end
  
      return state
  end
  
  return M
  ```

  Verwende das Modul so:

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state.alter_state(1)
  print(my_state.get_state()) 
  ```
