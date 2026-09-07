---
title: Suoni in Defold
brief: Questo manuale spiega come aggiungere suoni al tuo progetto Defold, riprodurli e controllarli.
---

# Suoni {#sound}

L'implementazione audio di Defold è semplice ma potente. Devi conoscere soltanto due concetti:

Componenti audio
: Questi componenti contengono un suono da riprodurre e ne gestiscono la riproduzione.

Gruppi di suoni
: Ogni componente audio può essere assegnato a un _gruppo_. I gruppi permettono di gestire in modo semplice e intuitivo i suoni correlati. Per esempio, puoi creare un gruppo `sound_fx` e attenuare qualsiasi suono che ne fa parte con una semplice chiamata a funzione.

## Creare un componente audio {#creating-a-sound-component}

I componenti audio possono essere istanziati soltanto direttamente all'interno di un oggetto di gioco. Crea un nuovo oggetto di gioco, fai clic con il pulsante destro del mouse su di esso, seleziona <kbd>Add Component ▸ Sound</kbd> e premi *OK*.

![Selezionare un componente](images/sound/sound_add_component.jpg)

Il componente creato ha una serie di proprietà da impostare:

![Selezionare un componente](images/sound/sound_properties.png)

*Sound*
: Deve indicare un file audio del progetto. Il file deve essere in formato _Wave_, _Ogg Vorbis_ o _Ogg Opus_. Defold supporta i file Wave PCM a 8 e 16 bit. La riproduzione Ogg Opus è facoltativa e richiede **Include Sound Decoder: Opus** nel [manifest dell'applicazione](/manuals/app-manifest/#sound); il decoder Opus non è incluso per impostazione predefinita.

*Looping*
: Se selezionata, il suono viene riprodotto per il numero di volte specificato in _Loopcount_ oppure finché non viene interrotto esplicitamente.

*Loopcount*
: Il numero di volte in cui un suono in ciclo viene riprodotto prima di fermarsi (0 indica che il suono deve ripetersi finché non viene interrotto esplicitamente).

*Group*
: Il nome del gruppo di suoni a cui il suono deve appartenere. Se questa proprietà viene lasciata vuota, il suono viene assegnato al gruppo integrato `master`.

*Gain*
: Puoi impostare il guadagno del suono direttamente sul componente. Questo permette di regolarlo facilmente senza tornare al programma audio ed esportare di nuovo il file. Più avanti trovi i dettagli su come viene calcolato il guadagno.

*Pan*
: Puoi impostare il valore del panorama stereo del suono direttamente sul componente. Il valore deve essere compreso tra -1 (-45 gradi a sinistra) e 1 (45 gradi a destra).

*Speed*
: Puoi impostare la velocità del suono direttamente sul componente. Un valore di 1.0 corrisponde alla velocità normale, 0.5 alla metà della velocità e 2.0 al doppio.


## Riprodurre il suono {#playing-the-sound}

Una volta configurato correttamente un componente audio, puoi avviare la riproduzione del suo suono chiamando [`sound.play()`](/ref/sound/#sound.play:url-[play_properties]-[complete_function]):

```lua
sound.play("go#sound", {delay = 1, gain = 0.5, pan = -1.0, speed = 1.25})
```

::: sidenote
Un suono continua a essere riprodotto anche se l'oggetto di gioco a cui apparteneva il componente audio viene eliminato. Puoi chiamare [`sound.stop()`](/ref/sound/#sound.stop:url) per interrompere il suono (vedi sotto).
:::
Ogni messaggio inviato a un componente avvia un'altra istanza del suono, finché il buffer audio disponibile non si riempie e il motore non stampa errori nella console. È consigliabile implementare un meccanismo di limitazione delle ripetizioni e di raggruppamento dei suoni.

## Interrompere il suono {#stopping-the-sound}

Per interrompere la riproduzione di un suono, puoi chiamare [`sound.stop()`](/ref/sound/#sound.stop:url):

```lua
sound.stop("go#sound")
```

## Guadagno {#gain}

![Guadagno](images/sound/sound_gain.png)

Il sistema audio ha 4 livelli di guadagno:

- Il guadagno impostato sul componente audio.
- Il guadagno impostato all'avvio del suono tramite una chiamata a `sound.play()` oppure quando si modifica il guadagno della voce tramite una chiamata a `sound.set_gain()`.
- Il guadagno impostato sul gruppo tramite una chiamata alla funzione [`sound.set_group_gain()`](/ref/sound#sound.set_group_gain).
- Il guadagno impostato sul gruppo `master`. Puoi modificarlo con `sound.set_group_gain(hash("master"), gain)`.

Quando **Use Linear Gain** è abilitata nelle [impostazioni audio del progetto](/manuals/project-settings/#sound) (l'impostazione predefinita), il guadagno in uscita è il prodotto di questi quattro guadagni. Un guadagno di `1.0` è un guadagno unitario (0 dB). Quando il guadagno lineare è disabilitato, Defold applica una curva non lineare durante il missaggio, quindi la moltiplicazione diretta dei quattro guadagni e la conversione in decibel riportata sotto non descrivono il livello risultante in uscita.

## Gruppi di suoni {#sound-groups}

Ogni componente audio per cui è specificato il nome di un gruppo viene inserito in un gruppo di suoni con quel nome. Se non specifichi un gruppo, il suono viene assegnato al gruppo `master`. Puoi anche impostare esplicitamente il gruppo di un componente audio su `master` per ottenere lo stesso effetto.

Sono disponibili alcune funzioni per ottenere tutti i gruppi disponibili, recuperarne il nome come stringa, leggere e impostare il guadagno e ottenere il valore RMS (vedi http://en.wikipedia.org/wiki/Root_mean_square) e il guadagno di picco. Esiste anche una funzione che permette di verificare se il lettore musicale del dispositivo di destinazione è in esecuzione:

```lua
-- If sound playing on this iPhone/Android device, silence everything
if sound.is_music_playing() then
    for i, group_hash in ipairs(sound.get_groups()) do
        sound.set_group_gain(group_hash, 0)
    end
end
```

I gruppi sono identificati da un valore hash. Il nome come stringa può essere recuperato con [`sound.get_group_name()`](/ref/sound#sound.get_group_name) e usato per mostrare i nomi dei gruppi negli strumenti di sviluppo, per esempio in un mixer per provare i livelli dei gruppi.

![Mixer dei gruppi di suoni](images/sound/sound_mixer.png)

::: important
Non scrivere codice che dipenda dal nome di un gruppo di suoni come stringa, perché queste stringhe non sono disponibili nelle build di release.
:::

Con **Use Linear Gain** abilitata, puoi convertire un valore di guadagno positivo in decibel con la formula standard:

```math
db = 20 \times \log \left( gain \right)
```

```lua
for i, group_hash in ipairs(sound.get_groups()) do
    -- The name string is only available in debug. Returns "unknown_*" in release.
    local name = sound.get_group_name(group_hash)
    local gain = sound.get_group_gain(group_hash)

    -- Convert to decibel.
    local db = 20 * math.log10(gain)

    -- Get RMS (gain Root Mean Square). Left and right channel separately.
    local left_rms, right_rms = sound.get_rms(group_hash, 2048 / 65536.0)
    left_rmsdb = 20 * math.log10(left_rms)
    right_rmsdb = 20 * math.log10(right_rms)

    -- Get gain peak. Left and right separately.
    left_peak, right_peak = sound.get_peak(group_hash, 2048 * 10 / 65536.0)
    left_peakdb = 20 * math.log10(left_peak)
    right_peakdb = 20 * math.log10(right_peak)
end

-- Set the master gain to +6 dB (math.pow(10, 6/20)).
sound.set_group_gain("master", 1.995)
```

Defold 1.10.2 ha corretto un'attenuazione di circa 3 dB presente da tempo nel mixer audio. Se il mix di un progetto precedente compensava tale attenuazione e il volume risulta più alto dopo l'aggiornamento, regola nuovamente l'impostazione globale **Sound ▸ Gain** o i guadagni dei gruppi interessati.

## Limitare le ripetizioni dei suoni {#gating-sounds}

Se il gioco riproduce lo stesso suono al verificarsi di un evento e quell'evento si attiva spesso, rischi di riprodurre lo stesso suono due o più volte quasi contemporaneamente. In questo caso i suoni saranno _sfasati_, il che può produrre artefatti molto evidenti.

![Sfasamento](images/sound/sound_phase_shift.png)

Il modo più semplice per risolvere questo problema è creare un filtro temporale che filtri i messaggi audio e impedisca di riprodurre lo stesso suono più di una volta entro un intervallo prestabilito:

```lua
-- Don't allow the same sound to be played within "gate_time" interval.
local gate_time = 0.3

function init(self)
    -- Store played sound timers in a table and count down each frame until they have been
    -- in the table for "gate_time" seconds. Then remove them.
    self.sounds = {}
end

function update(self, dt)
    -- Count down the stored timers
    for k,_ in pairs(self.sounds) do
        self.sounds[k] = self.sounds[k] - dt
        if self.sounds[k] < 0 then
            self.sounds[k] = nil
        end
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("play_gated_sound") then
        -- Only play sounds that are not currently in the gating table.
        if self.sounds[message.soundcomponent] == nil then
            -- Store sound timer in table
            self.sounds[message.soundcomponent] = gate_time
            -- Play the sound
            sound.play(message.soundcomponent, { gain = message.gain })
        else
            -- An attempt to play a sound was gated
            print("gated " .. message.soundcomponent)
        end
    end
end
```

Per usare il filtro, basta inviargli un messaggio `play_gated_sound` e specificare il componente audio di destinazione e il guadagno del suono. Il filtro chiamerà `sound.play()` con il componente audio di destinazione se la riproduzione è consentita:

```lua
msg.post("/sound_gate#script", "play_gated_sound", { soundcomponent = "/sounds#explosion1", gain = 1.0 })
```

::: important
Il filtro non può intercettare messaggi `play_sound`, perché questo nome è riservato dal motore Defold. L'uso di nomi di messaggi riservati causa comportamenti imprevisti.
:::


## Modifiche a runtime {#runtime-manipulation}
Puoi modificare i suoni durante l'esecuzione tramite diverse proprietà (consulta la [documentazione API per l'utilizzo](/ref/sound/)). Le seguenti proprietà possono essere modificate usando `go.get()` e `go.set()`:

`gain`
: Il guadagno del componente audio (`number`).

`pan`
: Il panorama stereo del componente audio (`number`). Il valore deve essere compreso tra -1 (-45 gradi a sinistra) e 1 (45 gradi a destra).

`speed`
: La velocità del componente audio (`number`). Un valore di 1.0 corrisponde alla velocità normale, 0.5 alla metà della velocità e 2.0 al doppio.

`sound`
: Il percorso della risorsa del suono (`hash`). Puoi usare il percorso della risorsa per cambiare il suono con `resource.set_sound(path, buffer)`. Esempio:

```lua
local boom = sys.load_resource("/sounds/boom.wav")
local path = go.get("#sound", "sound")
resource.set_sound(path, boom)
```


## Configurazione del progetto {#project-configuration}

Il file *game.project* contiene alcune [impostazioni del progetto](/manuals/project-settings#sound) relative ai componenti audio.

## Streaming audio {#sound-streaming}

È anche possibile supportare la [riproduzione di suoni in streaming](/manuals/sound-streaming)
