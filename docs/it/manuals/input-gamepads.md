---
title: Input dei gamepad in Defold
brief: Questo manuale spiega come funziona l'input dei gamepad.
---

::: sidenote
Ti consigliamo di familiarizzare con il funzionamento generale dell'input in Defold, con le modalità di ricezione dell'input e con l'ordine in cui viene ricevuto nei file script. Per saperne di più sul sistema di input, consulta il [manuale di panoramica dell'input](/manuals/input).
:::

# Gamepad {#gamepads}
I trigger di input dei gamepad consentono di associare l'input standard dei gamepad alle funzioni del gioco. L'input dei gamepad offre binding per:

- Stick sinistro e destro (direzione e pressione)
- Pad digitali sinistro e destro. Il pad destro corrisponde solitamente ai pulsanti "A", "B", "X" e "Y" sul controller Xbox e ai pulsanti "quadrato", "cerchio", "triangolo" e "croce" sul controller PlayStation.
- Grilletti sinistro e destro
- Pulsanti dorsali sinistro e destro
- Pulsanti Start, Back e Guide

![](images/input/gamepad_bindings.png)

::: important
Gli esempi seguenti usano le azioni mostrate nell'immagine qui sopra. Come per tutti gli input, puoi assegnare alle azioni di input i nomi che preferisci.
:::

## Pulsanti digitali {#digital-buttons}
I pulsanti digitali generano eventi `pressed`, `released` e `repeated`. Questo esempio mostra come rilevare l'input di un pulsante digitale (premuto o rilasciato):

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lpad_left") then
        if action.pressed then
            -- start moving left
        elseif action.released then
            -- stop moving left
        end
    end
end
```

## Stick analogici {#analog-sticks}
Gli stick analogici generano eventi di input continui quando lo stick viene spostato al di fuori della zona morta definita nel file delle impostazioni dei gamepad (vedi sotto). Questo esempio mostra come rilevare l'input di uno stick analogico:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") then
        -- left stick was moved down
        print(action.value) -- a value between 0.0 an -1.0
    end
end
```

Gli stick analogici generano anche eventi `pressed` e `released` quando vengono spostati nelle direzioni cardinali oltre un determinato valore di soglia. Questo permette di usare facilmente uno stick analogico anche come input direzionale digitale:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") and action.pressed then
        -- left stick was moved to its extreme down position
    end
end
```

## Più gamepad {#multiple-gamepads}
Defold supporta più gamepad attraverso il sistema operativo host. Le azioni impostano il campo `gamepad` della tabella `action` sul numero del gamepad da cui proviene l'input:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_start") then
        if action.gamepad == 0 then
          -- gamepad 0 wants to join the game
        end
    end
end
```

## Connessione e disconnessione {#connect-and-disconnect}
I binding di input dei gamepad comprendono anche due binding distinti chiamati `Connected` e `Disconnected`, che rilevano quando un gamepad viene connesso (compresi quelli connessi fin dall'avvio) o disconnesso.

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_connected") then
        if action.gamepad == 0 then
          -- gamepad 0 was connected
        end
    elseif action_id == hash("gamepad_disconnected") then
        if action.gamepad == 0 then
          -- gamepad 0 was disconnected
        end
    end
end
```

## Input grezzo dei gamepad {#raw-gamepads}

I binding di input dei gamepad comprendono anche un binding distinto chiamato `Raw`, che fornisce l'input non filtrato (senza applicare la zona morta) di pulsanti, assi e hat di qualsiasi gamepad connesso.

```lua
function on_input(self, action_id, action)
    if action_id == hash("raw") then
        pprint(action.gamepad_buttons)
        pprint(action.gamepad_axis)
        pprint(action.gamepad_hats)
    end
end
```

## File delle impostazioni dei gamepad {#gamepads-settings-file}

Le mappature dei gamepad traducono pulsanti, assi e hat di un controller nei controlli standard usati dalle associazioni di input. Defold combina due sorgenti di mappature configurate nella sezione *Input* di *game.project*:

| Impostazione | Formato della mappatura | Valore predefinito |
| --- | --- | --- |
| [Gamepad Database](/manuals/project-settings/#gamepad-database) | Database testuale in formato SDL, abbinato tramite il GUID del controller | `/builtins/input/gamecontrollerdb.txt` |
| [Gamepads](/manuals/project-settings/#gamepads) | Voci `.gamepads` precedenti per nomi di dispositivi e piattaforme | `/builtins/input/default.gamepads` |

Le mappature del database SDL e quelle automatiche della piattaforma usano [Gamepad Deadzone](/manuals/project-settings/#gamepad-deadzone). Le voci `.gamepads` precedenti definiscono le proprie zone morte. Su Android, un controller senza una voce nel database può anche ricevere una [mappatura automatica](#gamepads-on-android).

### Mappature .gamepads precedenti {#legacy-gamepads-mappings}

Un file `.gamepads` può contenere mappature per più controller. Le mappature precedenti esistenti restano supportate. Defold include le mappature dei controller comuni nel file predefinito:

![Impostazioni dei gamepad](images/input/gamepads.png)

Se devi creare una mappatura `.gamepads` precedente su una piattaforma desktop, lo strumento seguente può aiutarti. Per Android, consulta [Gamepad su Android](#gamepads-on-android).

[Fai clic per scaricare gdc.zip](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032).

Include eseguibili per Windows, Linux e macOS. Eseguilo dalla riga di comando:

```sh
./gdc
```

Lo strumento ti chiederà di premere diversi pulsanti sul controller connesso. Genererà quindi un nuovo file gamepads con le mappature corrette per il tuo controller. Salva il nuovo file oppure uniscilo al file gamepads esistente, quindi aggiorna l'impostazione in *game.project*:

![Impostazioni dei gamepad](images/input/gamepad_setting.png)

### Gamepad non identificati {#unidentified-gamepads}

Quando non è disponibile né una mappatura configurata né una mappatura automatica della piattaforma, il gamepad genera soltanto le azioni associate a `Connected`, `Disconnected` e `Raw`. Puoi aggiungere una mappatura del controller oppure gestirne l'input grezzo nel gioco.

Puoi verificare se un'azione di input di un gamepad proviene da un gamepad sconosciuto leggendo il valore `gamepad_unknown` in `action`:

```lua
function on_input(self, action_id, action)
    if action_id == hash("connected") then
        if action.gamepad_unknown then
            print("The connected gamepad is unidentified and will only generate raw input")
        else
            print("The connected gamepad is known and will generate input actions for buttons and sticks")
        end
    end
end
```

## Gamepad in HTML5 {#gamepads-in-html5}
I gamepad sono supportati nelle build HTML5 e generano gli stessi eventi di input delle altre piattaforme. Il supporto dei gamepad si basa sulla [Gamepad API](https://www.w3.org/TR/gamepad/), supportata dalla maggior parte dei browser ([consulta questa tabella di compatibilità](https://caniuse.com/?search=gamepad)). Se il browser non supporta la Gamepad API, Defold ignora tutti i trigger di input dei gamepad nel progetto senza segnalarlo. Puoi verificare se il browser supporta la Gamepad API controllando se la funzione `getGamepads` esiste nell'oggetto `navigator`:

```lua
local function supports_gamepads()
    return not html5 or (html5.run('typeof navigator.getGamepads === "function"') == "true")
end

if supports_gamepads() then
    print("Platform supports gamepads")
end
```

Se il gioco viene eseguito all'interno di un `iframe`, devi anche assicurarti che all'`iframe` sia stata aggiunta l'autorizzazione `gamepad`:

```html
<iframe allow="gamepad"></iframe>
```

### Gamepad standard {#standard-gamepad}

Se il browser identifica un gamepad connesso come gamepad standard, viene usata la mappatura per `Standard Gamepad` nel [file delle impostazioni dei gamepad](/manuals/input-gamepads/#gamepads-settings-file) (una mappatura `Standard Gamepad` è inclusa nel file `default.gamepads` in `/builtins`). Un gamepad standard è definito come un dispositivo con 16 pulsanti e 2 stick analogici, con una disposizione dei pulsanti simile a quella di un controller PlayStation o Xbox (per ulteriori informazioni, consulta la [definizione e la disposizione dei pulsanti del W3C](https://w3c.github.io/gamepad/#dfn-standard-gamepad)). Se il gamepad connesso non viene identificato come gamepad standard, Defold cerca nel file delle impostazioni dei gamepad una mappatura corrispondente al tipo di gamepad hardware.

## Gamepad su Windows {#gamepads-on-windows}
Su Windows, al momento sono supportati solo i controller Xbox 360. Per collegare il controller 360 al computer Windows, [assicurati che sia configurato correttamente](http://www.wikihow.com/Use-Your-Xbox-360-Controller-for-Windows).

## Gamepad su Android {#gamepads-on-android}

I gamepad sono supportati nelle build Android e generano le stesse azioni di input delle altre piattaforme. Defold usa le [mappature dei gamepad](#gamepads-settings-file) configurate e può mappare automaticamente alcuni controller privi di una voce corrispondente.

Se un controller non viene identificato o i suoi controlli sono errati, provalo sul dispositivo Android e aggiungi o aggiorna la sua mappatura. Per la risoluzione dei problemi, consulta [Gamepad non identificati](#unidentified-gamepads) e [Gamepad grezzi](#raw-gamepads).
