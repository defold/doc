---
title: Eventi di collisione in Defold
brief: La gestione degli eventi di collisione può essere centralizzata usando `physics.set_event_listener()` per indirizzare tutti i messaggi di collisione e interazione a un'unica funzione specificata.
---

# Gestione degli eventi fisici in Defold {#defold-physics-event-handling}

Defold offre una gestione centralizzata degli eventi fisici tramite la funzione `physics.set_event_listener()`. Questa funzione consente di impostare una funzione di ascolto personalizzata per gestire tutti gli eventi di interazione fisica in un unico punto, semplificando il codice e migliorandone l'efficienza.

## Impostazione della funzione di ascolto del mondo fisico {#setting-the-physics-world-listener}

In Defold, ogni proxy di collezione (collection proxy) crea un proprio mondo fisico separato. Pertanto, quando lavori con più proxy di collezione, è essenziale gestire i mondi fisici distinti associati a ciascuno. Per assicurarti che gli eventi fisici siano gestiti correttamente in ogni mondo, devi impostare una funzione di ascolto specifica per il mondo fisico di ciascun proxy di collezione.

Questo significa che la funzione di ascolto degli eventi fisici deve essere impostata nel contesto della collezione rappresentata dal proxy. In questo modo, associ la funzione di ascolto direttamente al mondo fisico pertinente, consentendole di elaborare correttamente gli eventi fisici.

Ecco un esempio di come impostare una funzione di ascolto del mondo fisico all'interno di un proxy di collezione:

```lua
function init(self)
    -- Assuming this script is attached to a game object within the collection loaded by the proxy
    -- Set the physics world listener for the physics world of this collection proxy
    physics.set_event_listener(physics_world_listener)
end
```

Applicando questo metodo, ti assicuri che ogni mondo fisico generato da un proxy di collezione abbia una funzione di ascolto dedicata. Questo è fondamentale per gestire efficacemente gli eventi fisici nei progetti che utilizzano più proxy di collezione.

::: important
Se imposti una funzione di ascolto, i [messaggi fisici](/manuals/physics-messages) non verranno più inviati per il mondo fisico in cui è impostata.
:::

## Struttura dei dati degli eventi {#event-data-structure}

La funzione di ascolto viene chiamata con `self` e una tabella `events`. La tabella `events` è un array contenente tutti gli eventi fisici raccolti per la callback. Ogni elemento è una tabella evento con un campo `type` contenente l'hash del nome dell'evento e ulteriori campi specifici per quel tipo di evento.

Le tabelle degli eventi contengono i seguenti dati:

1. **Evento di punto di contatto (`contact_point_event`):**
Questo evento segnala un punto di contatto tra due oggetti di collisione. È utile per una gestione dettagliata delle collisioni, ad esempio per calcolare le forze d'impatto o le risposte personalizzate alle collisioni.

   - `applied_impulse`: L'impulso risultante dal contatto.
   - `distance`: La distanza di penetrazione tra gli oggetti.
   - `a` e `b`: Oggetti che rappresentano le entità in collisione, ciascuno contenente:
     - `position`: Posizione del punto di contatto nello spazio globale (vector3).
     - `instance_position`: Posizione dell'istanza dell'oggetto di gioco nello spazio globale (vector3).
     - `id`: ID dell'istanza (hash).
     - `group`: Gruppo di collisione (hash).
     - `relative_velocity`: Velocità relativa all'altro oggetto (vector3).
     - `mass`: Massa in chilogrammi (number).
     - `normal`: Normale di contatto, diretta dall'altro oggetto verso questo (vector3).

2. **Evento di collisione (`collision_event`):**
Questo evento indica che si è verificata una collisione tra due oggetti. È un evento più generale rispetto a quello del punto di contatto, ideale per rilevare collisioni senza avere bisogno di informazioni dettagliate sui punti di contatto.

   - `a` e `b`: Oggetti che rappresentano le entità in collisione, ciascuno contenente:
     - `position`: Posizione nello spazio globale (vector3).
     - `id`: ID dell'istanza (hash).
     - `group`: Gruppo di collisione (hash).

3. **Evento trigger (`trigger_event`):** 
Questo evento viene inviato quando un oggetto interagisce con un oggetto trigger. È utile per creare aree nel gioco che attivano un'azione quando un oggetto entra o esce.

   - `enter`: Indica se l'interazione è stata un ingresso (true) o un'uscita (false).
   - `a` e `b`: Oggetti coinvolti nell'evento trigger, ciascuno contenente:
     - `id`: ID dell'istanza (hash).
     - `group`: Gruppo di collisione (hash).

4. **Risposta al lancio di un raggio (`ray_cast_response`):**
Questo evento viene inviato in risposta al lancio di un raggio (raycast), fornendo informazioni sull'oggetto colpito dal raggio.

   - `group`: Gruppo di collisione dell'oggetto colpito (hash).
   - `request_id`: Identificatore della richiesta di raycast (number).
   - `position`: Posizione dell'impatto (vector3).
   - `fraction`: La frazione della lunghezza del raggio alla quale si è verificato l'impatto (number).
   - `normal`: Normale nella posizione dell'impatto (vector3).
   - `id`: ID dell'istanza dell'oggetto colpito (hash).

5. **Raggio senza impatto (`ray_cast_missed`):**
Questo evento viene inviato quando un raycast non colpisce alcun oggetto.

   - `request_id`: Identificatore della richiesta di raycast che non ha colpito alcun oggetto (number).

## Esempio d'uso {#example-usage}

```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            -- Handle detailed contact point data
            pprint(event)
        elseif event.type == hash("collision_event") then
            -- Handle general collision data
            pprint(event)
        elseif event.type == hash("trigger_event") then
            -- Handle trigger interaction data
            pprint(event)
        elseif event.type == hash("ray_cast_response") then
            -- Handle raycast hit data
            pprint(event)
        elseif event.type == hash("ray_cast_missed") then
            -- Handle raycast miss data
            pprint(event)
        end
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```

## Limitazioni {#limitations}

La funzione di ascolto viene chiamata in modo sincrono nel momento in cui si verifica l'evento. Questo avviene nel corso di un passo temporale, il che significa che il mondo fisico è bloccato. Di conseguenza, non è possibile usare funzioni che possono influire sulle simulazioni del mondo fisico, ad esempio `physics.create_joint()`.

Ecco un breve esempio di come aggirare queste limitazioni:
```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            local position_a = event.a.normal * SIZE
            local position_b =  event.b.normal * SIZE
            local url_a = msg.url(nil, event.a.id, "collisionobject")
            local url_b = msg.url(nil, event.b.id, "collisionobject")
            -- fill the message in the same way arguments should be passed to `physics.create_joint()`
            local message = {physics.JOINT_TYPE_FIXED, url_a, "joind_id", position_a, url_b, position_b, {max_length = SIZE}}
            -- send message to the object itself
            msg.post(".", "create_joint", message)
        end
    end
end

function on_message(self, message_id, message)
    if message_id == hash("create_joint") then
        -- unpack message with function arguments
        physics.create_joint(unpack(message))
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```
