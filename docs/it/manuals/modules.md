---
title: Moduli Lua in Defold
brief: I moduli Lua consentono di organizzare il progetto e creare codice di libreria riutilizzabile. Questo manuale spiega come farlo in Defold.
---

# Moduli Lua {#lua-modules}

I moduli Lua consentono di organizzare il progetto e creare codice di libreria riutilizzabile. In generale è buona norma evitare duplicazioni nei progetti. Defold consente di usare i moduli di Lua per includere file di script in altri file di script. In questo modo puoi incapsulare funzionalità (e dati) in un file di script esterno e riutilizzarle negli script degli oggetti di gioco (game object) e negli script GUI.

## Caricamento di file Lua con require {#requiring-lua-files}

Il codice Lua salvato in file con estensione `.lua` all'interno del progetto di gioco può essere caricato con `require` nei file di script e di script GUI. Per creare un nuovo file di modulo Lua, fai clic con il pulsante destro del mouse sulla cartella in cui vuoi crearlo nella vista *Assets*, quindi seleziona <kbd>New... ▸ Lua Module</kbd>. Assegna al file un nome univoco e premi <kbd>Ok</kbd>:

![Nuovo file](images/modules/new_name.png)

Supponiamo di aggiungere il codice seguente al file "`main/anim.lua`":

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

Qualsiasi script può quindi caricare questo file con `require` e usare la funzione:

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

La funzione `require` carica il modulo specificato. Per prima cosa consulta la tabella `package.loaded` per determinare se il modulo è già caricato. In tal caso, `require` restituisce il valore memorizzato in `package.loaded[module_name]`. Altrimenti, carica ed esegue il file tramite una funzione di caricamento.

La sintassi della stringa che indica il nome del file passato a `require` è un po' particolare. Lua sostituisce i caratteri `.` nella stringa del nome del file con i separatori di percorso: `/` su macOS e Linux e `\\` su Windows.

Tieni presente che in genere è sconsigliato usare l'ambito globale per memorizzare lo stato e definire funzioni, come abbiamo fatto sopra. Rischi conflitti tra nomi, di esporre lo stato del modulo o di introdurre dipendenze tra le parti di codice che lo usano.

## Moduli {#modules}

Per incapsulare dati e funzioni, Lua usa i _moduli_. Un modulo Lua è una normale tabella Lua che contiene funzioni e dati. La tabella viene dichiarata locale per non introdurre nomi nell'ambito globale:

```lua
local M = {}

-- private
local message = "Hello world!"

function M.hello()
    print(message)
end

return M
```

Il modulo può quindi essere usato. Anche in questo caso è preferibile assegnarlo a una variabile locale:

```lua
local m = require "mymodule"
m.hello() --> "Hello world!"
```

## Hot reload dei moduli {#hot-reloading-modules}

Considera un modulo semplice:

```lua
-- module.lua
local M = {} -- creates a new table in the local scope
M.value = 4711
return M
```

E del codice che usa il modulo: 

```lua
local m = require "module"
print(m.value) --> "4711" (even if "module.lua" is changed and hot reloaded)
```

Se esegui un hot reload del file del modulo, il codice viene eseguito di nuovo, ma `m.value` non cambia. Perché?

Innanzitutto, la tabella in `module.lua` viene creata nell'ambito locale e al codice che usa il modulo viene restituito un _riferimento_ a quella tabella. Il ricaricamento di `module.lua` esegue di nuovo il codice del modulo, ma crea una nuova tabella nell'ambito locale anziché aggiornare la tabella a cui fa riferimento `m`.

Inoltre, Lua memorizza nella cache i file caricati con `require`. La prima volta che un file viene caricato, viene inserito nella tabella [`package.loaded`](/ref/package/#package.loaded), così da poterlo leggere più velocemente nelle chiamate successive a `require`. Puoi forzare la rilettura di un file dal disco impostando a `nil` la voce corrispondente al file: `package.loaded["my_module"] = nil`.

Per eseguire correttamente un hot reload di un modulo, devi ricaricare il modulo, azzerare la cache e poi ricaricare tutti i file che usano il modulo. Una soluzione tutt'altro che ottimale.

Puoi invece valutare una soluzione alternativa da usare _durante lo sviluppo_: inserisci la tabella del modulo nell'ambito globale e fai in modo che `M` faccia riferimento alla tabella globale, invece di creare una nuova tabella ogni volta che il file viene eseguito. Il ricaricamento del modulo modifica così il contenuto della tabella globale:

```lua
--- module.lua

-- Replace with local M = {} when done
uniquevariable12345 = uniquevariable12345 or {}
local M = uniquevariable12345

M.value = 4711
return M
```

## Moduli e stato {#modules-and-state}

I moduli con stato mantengono uno stato interno condiviso da tutte le parti di codice che usano il modulo e sono paragonabili ai singleton:

```lua
local M = {}

-- all users of the module will share this table
local state = {}

function M.do_something(foobar)
    table.insert(state, foobar)
end

return M
```

Un modulo senza stato, invece, non mantiene alcuno stato interno. Fornisce piuttosto un meccanismo per spostare lo stato in una tabella separata, locale al codice che usa il modulo. Ecco alcuni modi per realizzarlo:

Uso di una tabella di stato
: Il metodo più semplice è probabilmente usare una funzione costruttore che restituisce una nuova tabella contenente solo lo stato. Lo stato viene passato esplicitamente al modulo come primo parametro di ogni funzione che modifica la tabella di stato.

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
  
  Usa il modulo in questo modo:
  
  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  m.alter_state(my_state, 1)
  print(m.get_state(my_state)) --> 43
  ```

Uso delle metatabelle
: Un altro metodo consiste nell'usare una funzione costruttore che, a ogni chiamata, restituisce una nuova tabella con lo stato e le funzioni pubbliche del modulo:

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

  Usa il modulo in questo modo:

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state:alter_state(1) -- "my_state" is added as first argument when using : notation
  print(my_state:get_state()) --> 43
  ```

Uso delle chiusure
:  Un terzo modo consiste nel restituire una chiusura contenente tutto lo stato e tutte le funzioni. Non è necessario passare l'istanza come argomento (né esplicitamente né implicitamente usando l'operatore due punti), come avviene con le metatabelle. Questo metodo è anche leggermente più veloce delle metatabelle, perché le chiamate alle funzioni non devono passare attraverso i metametodi `__index`; tuttavia, ogni chiusura contiene una propria copia dei metodi, quindi il consumo di memoria è maggiore.

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

  Usa il modulo in questo modo:

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state.alter_state(1)
  print(my_state.get_state()) 
  ```
