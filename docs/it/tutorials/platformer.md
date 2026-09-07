---
title: Tutorial Defold per un platformer
brief: In questo articolo esamini l'implementazione di un semplice platformer 2D basato su tile in Defold. Le meccaniche che impari sono il movimento a sinistra e a destra, il salto e la caduta.
---

# Platformer

In questo articolo esaminiamo l'implementazione di un semplice platformer 2D basato su tile in Defold. Le meccaniche che impareremo sono il movimento a sinistra e a destra, il salto e la caduta.

Ci sono molti modi diversi per creare un platformer. Rodrigo Monteiro ha scritto un'analisi approfondita su questo e altri argomenti, disponibile [qui](http://higherorderfun.com/blog/2012/05/20/the-guide-to-implementing-2d-platformers/).

Ti consigliamo vivamente di leggerla se sei alle prime armi con i platformer, perché contiene molte informazioni preziose. Approfondiremo alcuni dei metodi descritti e la loro implementazione in Defold. Dovrebbe comunque essere facile adattare tutto ad altre piattaforme e ad altri linguaggi (in Defold usiamo Lua).

Diamo per scontato che tu abbia qualche nozione di matematica vettoriale (algebra lineare). In caso contrario, ti consigliamo di studiarla, perché è estremamente utile per lo sviluppo di giochi. David Rosen di Wolfire ha scritto un'ottima serie di articoli sull'argomento, disponibile [qui](http://blog.wolfire.com/2009/07/linear-algebra-for-game-developers-part-1/).

Se usi già Defold, puoi creare un nuovo progetto basato sul modello _Platformer_ e sperimentare mentre leggi questo articolo.

::: sidenote
Alcuni lettori hanno fatto notare che il metodo proposto non è realizzabile con l'implementazione predefinita di Box2D. Abbiamo apportato alcune modifiche a Box2D per renderlo possibile:

Le collisioni tra oggetti cinematici e statici vengono ignorate. Modifica i controlli in `b2Body::ShouldCollide` e `b2ContactManager::Collide`.

Inoltre, la distanza di contatto (chiamata separazione in Box2D) non viene fornita alla funzione di callback.
Aggiungi un membro per la distanza a `b2ManifoldPoint` e assicurati che venga aggiornato nelle funzioni `b2Collide*`.
:::

## Rilevamento delle collisioni {#collision-detection}

Il rilevamento delle collisioni serve a impedire al personaggio di attraversare la geometria del livello.
Esistono diversi modi per gestirlo, a seconda del gioco e delle sue esigenze specifiche.
Uno dei modi più semplici, quando possibile, è affidarlo a un motore fisico.
In Defold usiamo il motore fisico [Box2D](http://box2d.org/) per i giochi 2D.
L'implementazione predefinita di Box2D non offre tutte le funzionalità necessarie; consulta la parte finale di questo articolo per scoprire come l'abbiamo modificata.

Un motore fisico memorizza gli stati degli oggetti fisici insieme alle loro forme per simularne il comportamento fisico. Segnala anche le collisioni durante la simulazione, così il gioco può reagire quando si verificano. Nella maggior parte dei motori fisici esistono tre tipi di oggetti: _statici_, _dinamici_ e _cinematici_ (questi nomi possono essere diversi in altri motori fisici). Esistono anche altri tipi di oggetti, ma per ora ignoriamoli.

- Un oggetto *statico* non si muove mai (ad esempio la geometria del livello).
- Un oggetto *dinamico* è influenzato da forze e momenti torcenti, che vengono trasformati in velocità durante la simulazione.
- Un oggetto *cinematico* è controllato dalla logica dell'applicazione, ma continua a influenzare gli altri oggetti dinamici.

In un gioco come questo cerchiamo un comportamento che ricordi la fisica del mondo reale, ma è molto più importante avere controlli reattivi e meccaniche equilibrate. Un salto piacevole da eseguire non deve necessariamente essere fisicamente accurato o soggetto alla gravità del mondo reale. [Questa](http://hypertextbook.com/facts/2007/mariogravity.shtml) analisi mostra comunque che la gravità nei giochi di Mario si avvicina sempre di più a 9.8 m/s<sup>2</sup> a ogni versione. :-)

È importante avere il pieno controllo di ciò che accade, così da poter progettare e regolare le meccaniche per ottenere l'esperienza desiderata. Per questo scegliamo di rappresentare il personaggio del giocatore con un oggetto cinematico. Possiamo quindi spostarlo come vogliamo, senza dover gestire le forze fisiche. Questo significa che dovremo risolvere da soli la separazione tra il personaggio e la geometria del livello (ne parleremo più avanti), ma è uno svantaggio che siamo disposti ad accettare. Nel mondo fisico rappresenteremo il personaggio con una forma rettangolare.

## Movimento {#movement}

Ora che abbiamo deciso di rappresentare il personaggio con un oggetto cinematico, possiamo spostarlo liberamente impostandone la posizione. Iniziamo dal movimento a sinistra e a destra.

Il movimento si baserà sull'accelerazione, per dare al personaggio una sensazione di peso. Come per un normale veicolo, l'accelerazione determina quanto rapidamente il personaggio può raggiungere la velocità massima e cambiare direzione. L'accelerazione agisce durante l'intervallo di tempo del fotogramma---solitamente fornito nel parametro `dt` (delta-`t`)---e il suo contributo viene poi aggiunto alla velocità. Analogamente, la velocità agisce durante il fotogramma e lo spostamento risultante viene aggiunto alla posizione. In matematica, questa operazione si chiama [integrazione nel tempo](http://en.wikipedia.org/wiki/Integral).

![Integrazione approssimata della velocità](images/platformer/integration.png)

Le due linee verticali indicano l'inizio e la fine del fotogramma. La loro altezza corrisponde alla velocità del personaggio in questi due istanti. Chiamiamo queste velocità `v0` e `v1`. `v1` si ottiene applicando l'accelerazione (la pendenza della curva) per l'intervallo di tempo `dt`:

![Equazione della velocità](images/platformer/equationofvelocity.png)

L'area arancione rappresenta lo spostamento che dobbiamo applicare al personaggio durante il fotogramma corrente. Dal punto di vista geometrico, possiamo approssimare l'area così:

![Equazione dello spostamento](images/platformer/equationoftranslation.png)

Ecco come integriamo l'accelerazione e la velocità per spostare il personaggio nel ciclo di aggiornamento:

1. Determina la velocità desiderata in base all'input
2. Calcola la differenza tra la velocità attuale e quella desiderata
3. Imposta l'accelerazione in modo che agisca nella direzione della differenza
4. Calcola la variazione di velocità in questo fotogramma (`dv` è l'abbreviazione di delta-velocità), come sopra:

    ```lua
    local dv = acceleration * dt
    ```

5. Controlla se `dv` supera la differenza di velocità desiderata e, in tal caso, limitalo a quel valore
6. Salva la velocità attuale per usarla in seguito (`self.velocity`, che in questo momento è la velocità usata nel fotogramma precedente):

    ```lua
    local v0 = self.velocity
    ```

7. Calcola la nuova velocità aggiungendo la variazione di velocità:

    ```lua
    self.velocity = self.velocity + dv
    ```

8. Calcola lo spostamento lungo x in questo fotogramma integrando la velocità, come sopra:

    ```lua
    local dx = (v0 + self.velocity) * dt * 0.5
    ```

9. Applicalo al personaggio

Se non sai bene come gestire l'input in Defold, trovi una guida sull'argomento [qui](/manuals/input).

A questo punto possiamo muovere il personaggio a sinistra e a destra con controlli fluidi che trasmettono una sensazione di peso. Ora aggiungiamo la gravità!

Anche la gravità è un'accelerazione, ma agisce sul personaggio lungo l'asse y. Questo significa che verrà applicata allo stesso modo dell'accelerazione di movimento descritta sopra. Basta riscrivere i calcoli precedenti usando vettori e includere la gravità nella componente y dell'accelerazione al passaggio 3), e tutto funzionerà. Impossibile non amare la matematica vettoriale! :-)

## Risposta alle collisioni {#collision-response}

Ora il personaggio può muoversi e cadere, quindi è il momento di esaminare le risposte alle collisioni.
Ovviamente deve poter atterrare e muoversi lungo la geometria del livello. Useremo i punti di contatto forniti dal motore fisico per assicurarci che non si sovrapponga mai ad alcun oggetto.

Un punto di contatto contiene una _normale_ del contatto (diretta verso l'esterno dell'oggetto con cui entriamo in collisione, anche se in altri motori potrebbe essere diverso) e una _distanza_, che misura quanto siamo penetrati nell'altro oggetto. È tutto ciò che ci serve per separare il personaggio dalla geometria del livello.
Dato che usiamo un rettangolo, potremmo ricevere più punti di contatto durante un fotogramma. Succede, ad esempio, quando due angoli del rettangolo intersecano il terreno orizzontale oppure quando il personaggio si sposta verso un angolo.

![Normali di contatto che agiscono sul personaggio](images/platformer/collision.png)

Per evitare di applicare più volte la stessa correzione, accumuliamo le correzioni in un vettore e ci assicuriamo così di non compensare eccessivamente. Una compensazione eccessiva ci porterebbe troppo lontano dall'oggetto con cui siamo entrati in collisione. Nell'immagine sopra puoi vedere due punti di contatto, rappresentati dalle due frecce (normali). La distanza di penetrazione è uguale per entrambi i contatti: se la usassimo senza verifiche ogni volta, finiremmo per spostare il personaggio del doppio del necessario.

::: sidenote
È importante reimpostare il vettore delle correzioni accumulate al vettore nullo a ogni fotogramma.
Inserisci qualcosa di simile alla fine della funzione `update()`:
`self.corrections = vmath.vector3()`
:::

Supponendo che esista una funzione di callback chiamata per ogni punto di contatto, ecco come eseguire la separazione al suo interno:

```lua
local proj = vmath.dot(self.correction, normal) -- <1>
local comp = (distance - proj) * normal -- <2>
self.correction = self.correction + comp -- <3>
go.set_position(go.get_position() + comp) -- <4>
```

1. Proietta il vettore di correzione sulla normale di contatto (per il primo punto di contatto, il vettore di correzione è il vettore nullo)
2. Calcola la compensazione necessaria per questo punto di contatto
3. Aggiungila al vettore di correzione
4. Applica la compensazione al personaggio

Dobbiamo anche annullare la parte della velocità del personaggio diretta verso il punto di contatto:

```lua
proj = vmath.dot(self.velocity, message.normal) -- <1>
if proj < 0 then
    self.velocity = self.velocity - proj * message.normal -- <2>
end
```
1. Proietta la velocità sulla normale
2. Se la proiezione è negativa, significa che una parte della velocità è diretta verso il punto di contatto; in tal caso, rimuovi quella componente

## Salto {#jumping}

Ora che possiamo correre sulla geometria del livello e cadere, è il momento di saltare! I salti nei platformer si possono realizzare in molti modi diversi. In questo gioco puntiamo a qualcosa di simile a Super Mario Bros e Super Meat Boy. Durante il salto, il personaggio viene spinto verso l'alto da un impulso, che in pratica corrisponde a una velocità fissa.

La gravità continuerà a tirare il personaggio verso il basso, producendo una bella traiettoria ad arco. Mentre il personaggio è in aria, il giocatore può ancora controllarlo. Se il giocatore rilascia il pulsante del salto prima di raggiungere il punto più alto della traiettoria, la velocità verso l'alto viene ridotta per interrompere il salto in anticipo.

1. Quando viene premuto il comando di input, esegui:

    ```lua
    -- jump_takeoff_speed is a constant defined elsewhere
    self.velocity.y = jump_takeoff_speed
    ```

    Questo va eseguito soltanto quando il comando di input viene _premuto_, non a ogni fotogramma in cui viene _tenuto premuto_.

2. Quando viene rilasciato il comando di input, esegui:

    ```lua
    -- cut the jump short if we are still going up
    if self.velocity.y > 0 then
        -- scale down the upwards speed
        self.velocity.y = self.velocity.y * 0.5
    end
    ```

ExciteMike ha realizzato degli ottimi grafici delle traiettorie dei salti in [Super Mario Bros 3](http://meyermike.com/wp/?p=175) e [Super Meat Boy](http://meyermike.com/wp/?p=160), che meritano uno sguardo.

## Geometria del livello {#level-geometry}

La geometria del livello è costituita dalle forme di collisione dell'ambiente con cui il personaggio (ed eventualmente altri elementi) entra in collisione. In Defold esistono due modi per creare questa geometria.

Il primo consiste nel creare forme di collisione separate sopra i livelli che costruisci. Questo metodo è molto flessibile e permette di posizionare con precisione gli elementi grafici. È particolarmente utile se vuoi pendenze dolci.
Il gioco [Braid](http://braid-game.com/) usava questo metodo per costruire i livelli, ed è anche il metodo usato per il livello di esempio di questo tutorial. Ecco come appare nell'editor Defold:

![L'editor Defold con la geometria del livello e il personaggio posizionati nel mondo](images/platformer/editor.png)

Un'altra possibilità è costruire i livelli con tile e lasciare che l'editor generi automaticamente le forme fisiche a partire dalla grafica dei tile. In questo modo, la geometria del livello viene aggiornata automaticamente quando modifichi i livelli, il che può essere estremamente utile.

Se i tile posizionati sono allineati, le loro forme fisiche vengono automaticamente unite in un'unica forma.
Questo elimina gli spazi che possono far fermare o sobbalzare il personaggio mentre scorre su più tile orizzontali. Il risultato si ottiene sostituendo i poligoni dei tile con forme di bordo in Box2D durante il caricamento.

![Più poligoni basati su tile uniti in un'unica forma](images/platformer/stitching.png)

Sopra trovi un esempio in cui abbiamo creato cinque tile adiacenti a partire da una porzione della grafica del platformer. Nell'immagine puoi vedere come i tile posizionati (in alto) corrispondano a un'unica forma ottenuta unendoli (il contorno grigio in basso).

Per maggiori informazioni, consulta le nostre guide sulla [fisica](/manuals/physics) e sui [tile](/manuals/2dgraphics).

## Considerazioni finali {#final-words}

Se vuoi saperne di più sulle meccaniche dei platformer, trovi una quantità impressionante di informazioni sulla fisica di [Sonic](http://info.sonicretro.org/Sonic_Physics_Guide).

Se provi il nostro progetto modello su un dispositivo iOS o con un mouse, il salto può risultare davvero scomodo.
È soltanto il nostro modesto tentativo di realizzare un platformer con input a tocco singolo. :-)

Non abbiamo parlato di come abbiamo gestito le animazioni in questo gioco. Puoi fartene un'idea esaminando il file *player.script* qui sotto: cerca la funzione `update_animations()`.

Speriamo che queste informazioni ti siano state utili!
Crea un gran bel platformer, così potremo giocarci tutti! <3

## Codice {#code}

Ecco il contenuto di *player.script*:

```lua
-- player.script

-- these are the tweaks for the mechanics, feel free to change them for a different feeling
-- the acceleration to move right/left
local move_acceleration = 3500
-- acceleration factor to use when air-borne
local air_acceleration_factor = 0.8
-- max speed right/left
local max_speed = 450
-- gravity pulling the player down in pixel units
local gravity = -1000
-- take-off speed when jumping in pixel units
local jump_takeoff_speed = 550
-- time within a double tap must occur to be considered a jump (only used for mouse/touch controls)
local touch_jump_timeout = 0.2

-- prehashing ids improves performance
local msg_contact_point_response = hash("contact_point_response")
local msg_animation_done = hash("animation_done")
local group_obstacle = hash("obstacle")
local input_left = hash("left")
local input_right = hash("right")
local input_jump = hash("jump")
local input_touch = hash("touch")
local anim_run = hash("run")
local anim_idle = hash("idle")
local anim_jump = hash("jump")
local anim_fall = hash("fall")

function init(self)
    -- this lets us handle input in this script
    msg.post(".", "acquire_input_focus")

    -- initial player velocity
    self.velocity = vmath.vector3(0, 0, 0)
    -- support variable to keep track of collisions and separation
    self.correction = vmath.vector3()
    -- if the player stands on ground or not
    self.ground_contact = false
    -- movement input in the range [-1,1]
    self.move_input = 0
    -- the currently playing animation
    self.anim = nil
    -- timer that controls the jump-window when using mouse/touch
    self.touch_jump_timer = 0
end

local function play_animation(self, anim)
    -- only play animations which are not already playing
    if self.anim ~= anim then
        -- tell the sprite to play the animation
        sprite.play_flipbook("#sprite", anim)
        -- remember which animation is playing
        self.anim = anim
    end
end

local function update_animations(self)
    -- make sure the player character faces the right way
    sprite.set_hflip("#sprite", self.move_input < 0)
    -- make sure the right animation is playing
    if self.ground_contact then
        if self.velocity.x == 0 then
            play_animation(self, anim_idle)
        else
            play_animation(self, anim_run)
        end
    else
        if self.velocity.y > 0 then
            play_animation(self, anim_jump)
        else
            play_animation(self, anim_fall)
        end
    end
end

function update(self, dt)
    -- determine the target speed based on input
    local target_speed = self.move_input * max_speed
    -- calculate the difference between our current speed and the target speed
    local speed_diff = target_speed - self.velocity.x
    -- the complete acceleration to integrate over this frame
    local acceleration = vmath.vector3(0, gravity, 0)
    if speed_diff ~= 0 then
        -- set the acceleration to work in the direction of the difference
        if speed_diff < 0 then
            acceleration.x = -move_acceleration
        else
            acceleration.x = move_acceleration
        end
        -- decrease the acceleration when air-borne to give a slower feel
        if not self.ground_contact then
            acceleration.x = air_acceleration_factor * acceleration.x
        end
    end
    -- calculate the velocity change this frame (dv is short for delta-velocity)
    local dv = acceleration * dt
    -- check if dv exceeds the intended speed difference, clamp it in that case
    if math.abs(dv.x) > math.abs(speed_diff) then
        dv.x = speed_diff
    end
    -- save the current velocity for later use
    -- (self.velocity, which right now is the velocity used the previous frame)
    local v0 = self.velocity
    -- calculate the new velocity by adding the velocity change
    self.velocity = self.velocity + dv
    -- calculate the translation this frame by integrating the velocity
    local dp = (v0 + self.velocity) * dt * 0.5
    -- apply it to the player character
    go.set_position(go.get_position() + dp)

    -- update the jump timer
    if self.touch_jump_timer > 0 then
        self.touch_jump_timer = self.touch_jump_timer - dt
    end

    update_animations(self)

    -- reset volatile state
    self.correction = vmath.vector3()
    self.move_input = 0
    self.ground_contact = false

end

local function handle_obstacle_contact(self, normal, distance)
    -- project the correction vector onto the contact normal
    -- (the correction vector is the 0-vector for the first contact point)
    local proj = vmath.dot(self.correction, normal)
    -- calculate the compensation we need to make for this contact point
    local comp = (distance - proj) * normal
    -- add it to the correction vector
    self.correction = self.correction + comp
    -- apply the compensation to the player character
    go.set_position(go.get_position() + comp)
    -- check if the normal points enough up to consider the player standing on the ground
    -- (0.7 is roughly equal to 45 degrees deviation from pure vertical direction)
    if normal.y > 0.7 then
        self.ground_contact = true
    end
    -- project the velocity onto the normal
    proj = vmath.dot(self.velocity, normal)
    -- if the projection is negative, it means that some of the velocity points towards the contact point
    if proj < 0 then
        -- remove that component in that case
        self.velocity = self.velocity - proj * normal
    end
end

function on_message(self, message_id, message, sender)
    -- check if we received a contact point message
    if message_id == msg_contact_point_response then
        -- check that the object is something we consider an obstacle
        if message.group == group_obstacle then
            handle_obstacle_contact(self, message.normal, message.distance)
        end
    end
end

local function jump(self)
    -- only allow jump from ground
    -- (extend this with a counter to do things like double-jumps)
    if self.ground_contact then
        -- set take-off speed
        self.velocity.y = jump_takeoff_speed
        -- play animation
        play_animation(self, anim_jump)
    end
end

local function abort_jump(self)
    -- cut the jump short if we are still going up
    if self.velocity.y > 0 then
        -- scale down the upwards speed
        self.velocity.y = self.velocity.y * 0.5
    end
end

function on_input(self, action_id, action)
    if action_id == input_left then
        self.move_input = -action.value
    elseif action_id == input_right then
        self.move_input = action.value
    elseif action_id == input_jump then
        if action.pressed then
            jump(self)
        elseif action.released then
            abort_jump(self)
        end
    elseif action_id == input_touch then
        -- move towards the touch-point
        local diff = action.x - go.get_position().x
        -- only give input when far away (more than 10 pixels)
        if math.abs(diff) > 10 then
            -- slow down when less than 100 pixels away
            self.move_input = diff / 100
            -- clamp input to [-1,1]
            self.move_input = math.min(1, math.max(-1, self.move_input))
        end
        if action.released then
            -- start timing the last release to see if we are about to jump
            self.touch_jump_timer = touch_jump_timeout
        elseif action.pressed then
            -- jump on double tap
            if self.touch_jump_timer > 0 then
                jump(self)
            end
        end
    end
end
```
