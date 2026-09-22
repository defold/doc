---
title: Risoluzione delle collisioni cinematiche in Defold
brief: Questo manuale spiega come risolvere le collisioni fisiche degli oggetti cinematici.
---

# Risoluzione delle collisioni cinematiche {#resolving-kinematic-collisions}

Quando usi oggetti di collisione cinematici, devi risolvere le collisioni autonomamente e spostare gli oggetti di conseguenza. Un'implementazione elementare per separare due oggetti in collisione è la seguente:

```lua
function on_message(self, message_id, message, sender)
  -- Handle collision
  if message_id == hash("contact_point_response") then
    local newpos = go.get_position() + message.normal * message.distance
    go.set_position(newpos)
  end
end
```

Questo codice separa il tuo oggetto cinematico dagli altri oggetti fisici in cui penetra, ma spesso lo spostamento è eccessivo e in molti casi vedrai delle oscillazioni. Per capire meglio il problema, considera il seguente caso in cui il personaggio del giocatore è entrato in collisione con due oggetti, *A* e *B*:

![Collisione fisica](images/physics/collision_multi.png)

Nel fotogramma in cui si verifica la collisione, il motore fisico invia più messaggi `"contact_point_response"`, uno per l'oggetto *A* e uno per l'oggetto *B*. Se sposti il personaggio in risposta a ciascuna penetrazione, come nel codice elementare riportato sopra, la separazione risultante sarà:

- Sposta il personaggio fuori dall'oggetto *A* in base alla sua distanza di penetrazione (la freccia nera)
- Sposta il personaggio fuori dall'oggetto *B* in base alla sua distanza di penetrazione (la freccia nera)

L'ordine di queste operazioni è arbitrario, ma il risultato è lo stesso in entrambi i casi: una separazione totale pari alla *somma dei singoli vettori di penetrazione*:

![Separazione fisica elementare](images/physics/separation_naive.png)

Per separare correttamente il personaggio dagli oggetti *A* e *B*, devi gestire la distanza di penetrazione di ciascun punto di contatto e verificare se le separazioni precedenti hanno già prodotto, in tutto o in parte, la separazione necessaria.

Supponi che il primo messaggio di contatto provenga dall'oggetto *A* e che tu sposti il personaggio verso l'esterno usando il vettore di penetrazione di *A*:

![Separazione fisica, passo 1](images/physics/separation_step1.png)

A questo punto il personaggio è già stato parzialmente separato da *B*. La compensazione finale necessaria per ottenere la separazione completa dall'oggetto *B* è indicata dalla freccia nera qui sopra. Puoi calcolare la lunghezza del vettore di compensazione proiettando il vettore di penetrazione di *A* sul vettore di penetrazione di *B*:

![Proiezione](images/physics/projection.png)

```
l = vmath.project(A, B) * vmath.length(B)
```

Il vettore di compensazione si ottiene riducendo di *l* la lunghezza di *B*. Per eseguire questo calcolo con un numero qualsiasi di penetrazioni, puoi accumulare la correzione necessaria in un vettore. Parti da un vettore di correzione di lunghezza zero e, per ciascun punto di contatto:

1. Proietta la correzione attuale sul vettore di penetrazione del contatto.
2. Calcola la compensazione rimanente dal vettore di penetrazione (secondo la formula riportata sopra).
3. Sposta l'oggetto secondo il vettore di compensazione.
4. Aggiungi la compensazione alla correzione accumulata.

Ecco un'implementazione completa:

```lua
function init(self)
  -- correction vector
  self.correction = vmath.vector3()
end

function update(self, dt)
  -- reset correction
  self.correction = vmath.vector3()
end

function on_message(self, message_id, message, sender)
  -- Handle collision
  if message_id == hash("contact_point_response") then
    -- Get the info needed to move out of collision. We might
    -- get several contact points back and have to calculate
    -- how to move out of all of them by accumulating a
    -- correction vector for this frame:
    if message.distance > 0 then
      -- First, project the accumulated correction onto
      -- the penetration vector
      local proj = vmath.project(self.correction, message.normal * message.distance)
      if proj < 1 then
        -- Only care for projections that does not overshoot.
        local comp = (message.distance - message.distance * proj) * message.normal
        -- Apply compensation
        go.set_position(go.get_position() + comp)
        -- Accumulate correction done
        self.correction = self.correction + comp
      end
    end
  end
end
```
