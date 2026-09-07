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
La configurazione dell'input dei gamepad usa un file di mappatura distinto per ogni tipo di gamepad hardware. Le mappature per modelli hardware specifici vengono definite in un file *gamepads*. Defold include un file gamepads integrato con le impostazioni per i gamepad più comuni:

![Impostazioni dei gamepad](images/input/gamepads.png)

Se devi creare un nuovo file delle impostazioni dei gamepad, è disponibile un semplice strumento che può aiutarti:

[Fai clic per scaricare gdc.zip](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032).

Include eseguibili per Windows, Linux e macOS. Eseguilo dalla riga di comando:

```sh
./gdc
```

Lo strumento ti chiederà di premere diversi pulsanti sul controller connesso. Genererà quindi un nuovo file gamepads con le mappature corrette per il tuo controller. Salva il nuovo file oppure uniscilo al file gamepads esistente, quindi aggiorna l'impostazione in *game.project*:

![Impostazioni dei gamepad](images/input/gamepad_setting.png)

### Gamepad non identificati {#unidentified-gamepads}

Quando viene connesso un gamepad per cui non esiste una mappatura, questo genera soltanto le azioni `connected`, `disconnected` e `raw`. In questo caso devi associare manualmente i dati grezzi del gamepad alle azioni del gioco.

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

I gamepad sono supportati nelle build Android e generano gli stessi eventi di input delle altre piattaforme. Il supporto dei gamepad si basa sul [sistema di input Android per gli eventi dei tasti e di movimento](https://developer.android.com/training/game-controllers/controller-input). Gli eventi di input Android vengono convertiti in eventi dei gamepad di Defold usando lo stesso file *gamepad* descritto sopra.

Quando aggiungi altri binding dei gamepad su Android, puoi usare le seguenti tabelle di corrispondenza per convertire gli eventi di input Android nei valori del file *gamepad*:

| Da evento del tasto a indice del pulsante   | Indice |
|-----------------------------|-------|
| `AKEYCODE_BUTTON_A`           | 0     |
| `AKEYCODE_BUTTON_B`           | 1     |
| `AKEYCODE_BUTTON_C`           | 2     |
| `AKEYCODE_BUTTON_X`           | 3     |
| `AKEYCODE_BUTTON_L1`          | 4     |
| `AKEYCODE_BUTTON_R1`          | 5     |
| `AKEYCODE_BUTTON_Y`           | 6     |
| `AKEYCODE_BUTTON_Z`           | 7     |
| `AKEYCODE_BUTTON_L2`          | 8     |
| `AKEYCODE_BUTTON_R2`          | 9     |
| `AKEYCODE_DPAD_CENTER`        | 10    |
| `AKEYCODE_DPAD_DOWN`          | 11    |
| `AKEYCODE_DPAD_LEFT`          | 12    |
| `AKEYCODE_DPAD_RIGHT`         | 13    |
| `AKEYCODE_DPAD_UP`            | 14    |
| `AKEYCODE_BUTTON_START`       | 15    |
| `AKEYCODE_BUTTON_SELECT`      | 16    |
| `AKEYCODE_BUTTON_THUMBL`      | 17    |
| `AKEYCODE_BUTTON_THUMBR`      | 18    |
| `AKEYCODE_BUTTON_MODE`        | 19    |
| `AKEYCODE_BUTTON_1`           | 20    |
| `AKEYCODE_BUTTON_2`           | 21    |
| `AKEYCODE_BUTTON_3`           | 22    |
| `AKEYCODE_BUTTON_4`           | 23    |
| `AKEYCODE_BUTTON_5`           | 24    |
| `AKEYCODE_BUTTON_6`           | 25    |
| `AKEYCODE_BUTTON_7`           | 26    |
| `AKEYCODE_BUTTON_8`           | 27    |
| `AKEYCODE_BUTTON_9`           | 28    |
| `AKEYCODE_BUTTON_10`          | 29    |
| `AKEYCODE_BUTTON_11`          | 30    |
| `AKEYCODE_BUTTON_12`          | 31    |
| `AKEYCODE_BUTTON_13`          | 32    |
| `AKEYCODE_BUTTON_14`          | 33    |
| `AKEYCODE_BUTTON_15`          | 34    |
| `AKEYCODE_BUTTON_16`          | 35    |

([Definizioni di `KeyEvent` in Android](https://developer.android.com/ndk/reference/group/input#group___input_1gafccd240f973cf154952fb917c9209719))

| Da evento di movimento a indice dell'asse  | Indice |
|-----------------------------|-------|
| `AMOTION_EVENT_AXIS_X`        | 0     |
| `AMOTION_EVENT_AXIS_Y`        | 1     |
| `AMOTION_EVENT_AXIS_Z`        | 2     |
| `AMOTION_EVENT_AXIS_RZ`       | 3     |
| `AMOTION_EVENT_AXIS_LTRIGGER` | 4     |
| `AMOTION_EVENT_AXIS_RTRIGGER` | 5     |
| `AMOTION_EVENT_AXIS_HAT_X`    | 6     |
| `AMOTION_EVENT_AXIS_HAT_Y`    | 7     |

([Definizioni di `MotionEvent` in Android](https://developer.android.com/ndk/reference/group/input#group___input_1ga157d5577a5b2f5986037d0d09c7dc77d))

Usa questa tabella di corrispondenza insieme a un'app per testare i gamepad disponibile sul Google Play Store per individuare l'evento del tasto associato a ciascun pulsante del gamepad.
