---
title: Messaggi di collisione in Defold
brief: Quando due oggetti entrano in collisione, il motore chiama la callback degli eventi o invia messaggi.
---

# Messaggi di collisione {#collision-messages}

Quando due oggetti entrano in collisione, il motore invia un evento alla callback degli eventi o messaggi a entrambi gli oggetti.

## Filtraggio degli eventi {#event-filtering}

Puoi controllare i tipi di eventi generati tramite le opzioni di ciascun oggetto:

* "Generate Collision Events"
* "Generate Contact Events"
* "Generate Trigger Events"

Per impostazione predefinita, sono tutte impostate su `true`.
Quando due oggetti di collisione interagiscono, il motore controlla queste caselle per determinare se inviare un messaggio all'utente.

Ad esempio, considerando le caselle "Generate Contact Events":

Quando usi `physics.set_event_listener()`:

| Componente A | Componente B | Invio messaggio |
|-------------|-------------|--------------|
| ✅︎          | ✅︎          | Sì          |
| ❌          | ✅︎          | Sì          |
| ✅︎          | ❌          | Sì          |
| ❌          | ❌          | No           |

Quando usi il gestore di messaggi predefinito:

| Componente A | Componente B | Invio messaggi   |
|-------------|-------------|-------------------|
| ✅︎          | ✅︎          | Sì (A,B) + (B,A) |
| ❌          | ✅︎          | Sì (B,A)         |
| ✅︎          | ❌          | Sì (A,B)         |
| ❌          | ❌          | No                |

## Risposta alla collisione {#collision-response}

Il messaggio `"collision_response"` viene inviato quando uno degli oggetti in collisione è di tipo "dynamic", "kinematic" o "static". Contiene i seguenti campi:

`other_id`
: l'ID dell'istanza con cui l'oggetto di collisione è entrato in collisione (`hash`)

`other_position`
: la posizione globale dell'istanza con cui l'oggetto di collisione è entrato in collisione (`vector3`)

`other_group`
: il gruppo di collisione dell'altro oggetto di collisione (`hash`)

`own_group`
: il gruppo di collisione dell'oggetto di collisione (`hash`)

Il messaggio `collision_response` è adatto a gestire solo le collisioni per cui non servono dettagli sull'effettiva intersezione degli oggetti, ad esempio se vuoi rilevare se un proiettile colpisce un nemico. Per ogni coppia di oggetti in collisione viene inviato un solo messaggio di questo tipo per fotogramma.

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("collision_response") then
        -- take action
        print("I collided with", message.other_id)
    end
end
```

## Risposta del punto di contatto {#contact-point-response}

Il messaggio `"contact_point_response"` viene inviato quando uno degli oggetti in collisione è di tipo "dynamic" o "kinematic" e l'altro è di tipo "dynamic", "kinematic" o "static". Contiene i seguenti campi:

`position`
: la posizione globale del punto di contatto (`vector3`).

`normal`
: la normale del punto di contatto nello spazio globale, diretta dall'altro oggetto verso l'oggetto corrente (`vector3`).

`relative_velocity`
: la velocità relativa dell'oggetto di collisione osservata dall'altro oggetto (`vector3`).

`distance`
: la distanza di penetrazione tra gli oggetti -- non negativa (`number`).

`applied_impulse`
: l'impulso risultante dal contatto (`number`).

`life_time`
: (*attualmente non utilizzato!*) la durata del contatto (`number`).

`mass`
: la massa dell'oggetto di collisione corrente in kg (`number`).

`other_mass`
: la massa dell'altro oggetto di collisione in kg (`number`).

`other_id`
: l'ID dell'istanza con cui l'oggetto di collisione è in contatto (`hash`).

`other_position`
: la posizione globale dell'altro oggetto di collisione (`vector3`).

`other_group`
: il gruppo di collisione dell'altro oggetto di collisione (`hash`).

`own_group`
: il gruppo di collisione dell'oggetto di collisione (`hash`).

In un gioco o un'applicazione in cui devi separare perfettamente gli oggetti, il messaggio `"contact_point_response"` fornisce tutte le informazioni necessarie. Tuttavia, tieni presente che, per ogni coppia di oggetti in collisione, puoi ricevere diversi messaggi `"contact_point_response"` per fotogramma, a seconda della natura della collisione. Consulta [Risoluzione delle collisioni per ulteriori informazioni](/manuals/physics-resolving-collisions).

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("contact_point_response") then
        -- take action
        if message.other_mass > 10 then
            print("I collided with something weighing more than 10 kilos!")
        end
    end
end
```

## Risposta del trigger {#trigger-response}

Il messaggio `"trigger_response"`  viene inviato quando uno degli oggetti in collisione è di tipo "trigger". Il messaggio viene inviato una volta quando viene rilevata la collisione e poi una seconda volta quando gli oggetti non sono più in collisione. Contiene i seguenti campi:

`other_id`
: l'ID dell'istanza con cui l'oggetto di collisione è entrato in collisione (`hash`).

`enter`
: `true` se l'interazione è stata un ingresso nel trigger, `false` se è stata un'uscita. (`boolean`).

`other_group`
: il gruppo di collisione dell'altro oggetto di collisione (`hash`).

`own_group`
: il gruppo di collisione dell'oggetto di collisione (`hash`).

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("trigger_response") then
        if message.enter then
            -- take action for entry
            print("I am now inside", message.other_id)
        else
            -- take action for exit
            print("I am now outside", message.other_id)
        end
    end
end
```
