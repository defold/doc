---
title: Audio in Defold
brief: Dieses Handbuch erklärt, wie du Töne in dein Defold-Projekt einbindest, wiedergibst und steuerst.
---

# Audio {#sound}

Defolds Audioimplementierung ist einfach, aber leistungsfähig. Du musst nur zwei Konzepte kennen:

Audiokomponenten (sound components)
: Diese Komponenten enthalten einen konkreten Ton, der abgespielt werden soll, und können ihn wiedergeben.

Audiogruppen (sound groups)
: Jede Audiokomponente kann einer _Gruppe_ zugeordnet werden. Gruppen bieten eine einfache und intuitive Möglichkeit, zusammengehörende Töne zu verwalten. Du kannst beispielsweise eine Gruppe `sound_fx` einrichten und jeden Ton, der zu dieser Gruppe gehört, mit einem einfachen Funktionsaufruf in der Lautstärke absenken.

## Eine Audiokomponente erstellen {#creating-a-sound-component}

Audiokomponenten können nur direkt in einem Spielobjekt (game object) instanziiert werden. Erstelle ein neues Spielobjekt, klicke mit der rechten Maustaste darauf, wähle <kbd>Add Component ▸ Sound</kbd> und drücke *OK*.

![Komponente auswählen](images/sound/sound_add_component.jpg)

Die erstellte Komponente hat einige Eigenschaften, die du festlegen solltest:

![Komponente auswählen](images/sound/sound_properties.png)

*Sound*
: Sollte auf eine Audiodatei in deinem Projekt gesetzt werden. Die Datei sollte im Format _Wave_, _Ogg Vorbis_ oder _Ogg Opus_ vorliegen. Defold unterstützt Wave-Dateien mit 8-Bit- und 16-Bit-PCM. Die Wiedergabe von Ogg Opus ist optional und erfordert **Include Sound Decoder: Opus** im [App-Manifest](/manuals/app-manifest/#sound); der Opus-Decoder ist standardmäßig nicht enthalten.

*Looping*
: Wenn diese Option aktiviert ist, wird der Ton so oft wiedergegeben, wie in _Loopcount_ angegeben, oder bis er ausdrücklich gestoppt wird.

*Loopcount*
: Die Anzahl der Wiedergaben eines wiederholt abgespielten Tons, bevor er stoppt (0 bedeutet, dass der Ton wiederholt werden soll, bis er ausdrücklich gestoppt wird).

*Group*
: Der Name der Audiogruppe, zu der der Ton gehören soll. Wenn diese Eigenschaft leer bleibt, wird der Ton der integrierten Gruppe `master` zugewiesen.

*Gain*
: Du kannst den Verstärkungsfaktor (gain) für den Ton direkt an der Komponente festlegen. So kannst du den Verstärkungsfaktor eines Tons einfach anpassen, ohne zu deinem Audioprogramm zurückzukehren und die Datei erneut zu exportieren. Weiter unten findest du Einzelheiten zur Berechnung des Verstärkungsfaktors.

*Pan*
: Du kannst das Stereopanorama (pan) für den Ton direkt an der Komponente festlegen. Der Wert muss zwischen -1 (-45 Grad links) und 1 (45 Grad rechts) liegen.

*Speed*
: Du kannst die Wiedergabegeschwindigkeit für den Ton direkt an der Komponente festlegen. Ein Wert von 1.0 entspricht der normalen Geschwindigkeit, 0.5 der halben und 2.0 der doppelten Geschwindigkeit.


## Den Ton wiedergeben {#playing-the-sound}

Wenn du eine Audiokomponente richtig eingerichtet hast, kannst du ihren Ton durch einen Aufruf von [`sound.play()`](/ref/sound/#sound.play:url-[play_properties]-[complete_function]) wiedergeben:

```lua
sound.play("go#sound", {delay = 1, gain = 0.5, pan = -1.0, speed = 1.25})
```

::: sidenote
Ein Ton wird auch dann weiter abgespielt, wenn das Spielobjekt, zu dem die Audiokomponente gehörte, gelöscht wird. Du kannst [`sound.stop()`](/ref/sound/#sound.stop:url) aufrufen, um den Ton zu stoppen (siehe unten).
:::
Jede an eine Komponente gesendete Nachricht bewirkt, dass sie eine weitere Instanz des Tons wiedergibt, bis der verfügbare Audiopuffer voll ist und die Engine Fehler in der Konsole ausgibt. Es empfiehlt sich, einen Mechanismus zur Begrenzung der Wiedergabe und zur Gruppierung von Tönen zu implementieren.

## Den Ton stoppen {#stopping-the-sound}

Wenn du die Wiedergabe eines Tons stoppen möchtest, kannst du [`sound.stop()`](/ref/sound/#sound.stop:url) aufrufen:

```lua
sound.stop("go#sound")
```

## Verstärkungsfaktor {#gain}

![Verstärkungsfaktor](images/sound/sound_gain.png)

Das Audiosystem hat 4 Ebenen für Verstärkungsfaktoren:

- Den an der Audiokomponente festgelegten Verstärkungsfaktor.
- Den Verstärkungsfaktor, der beim Starten des Tons durch einen Aufruf von `sound.play()` oder beim Ändern des Verstärkungsfaktors der Wiedergabeinstanz durch einen Aufruf von `sound.set_gain()` festgelegt wird.
- Den Verstärkungsfaktor, der durch einen Aufruf der Funktion [`sound.set_group_gain()`](/ref/sound#sound.set_group_gain) für die Gruppe festgelegt wird.
- Den für die Gruppe `master` festgelegten Verstärkungsfaktor. Du kannst ihn mit `sound.set_group_gain(hash("master"), gain)` ändern.

Wenn **Use Linear Gain** in den [Audio-Projekteinstellungen](/manuals/project-settings/#sound) aktiviert ist (die Standardeinstellung), ergibt sich der Verstärkungsfaktor der Ausgabe aus der Multiplikation dieser vier Verstärkungsfaktoren. Ein Verstärkungsfaktor von `1.0` bedeutet eine unveränderte Verstärkung (0 dB). Wenn die lineare Verstärkung deaktiviert ist, wendet Defold beim Mischen eine nichtlineare Kurve an. Daher beschreiben die direkte Multiplikation der vier Faktoren und die unten gezeigte Umrechnung in Dezibel den resultierenden Ausgangspegel nicht.

## Audiogruppen {#sound-groups}

Jede Audiokomponente, für die der Name einer Audiogruppe angegeben ist, wird einer Audiogruppe mit diesem Namen zugeordnet. Wenn du keine Gruppe angibst, wird der Ton der Gruppe `master` zugewiesen. Du kannst die Gruppe einer Audiokomponente auch ausdrücklich auf `master` setzen, was dieselbe Wirkung hat.

Es stehen einige Funktionen zur Verfügung, um alle verfügbaren Gruppen und ihre Namen als Zeichenfolge abzurufen sowie Verstärkungsfaktoren abzurufen und festzulegen. Außerdem kannst du den Effektivwert (RMS, siehe http://en.wikipedia.org/wiki/Root_mean_square) und den Spitzenwert des Verstärkungsfaktors abrufen. Es gibt auch eine Funktion, mit der du prüfen kannst, ob der Musikplayer des Zielgeräts läuft:

```lua
-- If sound playing on this iPhone/Android device, silence everything
if sound.is_music_playing() then
    for i, group_hash in ipairs(sound.get_groups()) do
        sound.set_group_gain(group_hash, 0)
    end
end
```

Die Gruppen werden durch einen Hashwert identifiziert. Den Namen als Zeichenfolge kannst du mit [`sound.get_group_name()`](/ref/sound#sound.get_group_name) abrufen. Damit kannst du Gruppennamen in Entwicklungswerkzeugen anzeigen, zum Beispiel in einem Mischpult zum Testen der Gruppenpegel.

![Mischpult für Audiogruppen](images/sound/sound_mixer.png)

::: important
Du solltest keinen Code schreiben, der sich auf den Namen einer Audiogruppe als Zeichenfolge verlässt, da diese Zeichenfolgen in Release-Builds nicht verfügbar sind.
:::

Wenn **Use Linear Gain** aktiviert ist, kannst du einen positiven Verstärkungsfaktor mit der Standardformel in Dezibel umrechnen:

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

Defold 1.10.2 hat eine seit Langem bestehende Dämpfung von ungefähr 3 dB im Audiomischer korrigiert. Wenn die Abmischung eines älteren Projekts diese Dämpfung ausgeglichen hat und nach dem Upgrade lauter klingt, passe die globale Einstellung **Sound ▸ Gain** oder die Verstärkungsfaktoren der betroffenen Gruppen erneut an.

## Die Wiedergabe von Tönen begrenzen {#gating-sounds}

Wenn dein Spiel bei einem Ereignis denselben Ton abspielt und dieses Ereignis häufig ausgelöst wird, besteht die Gefahr, dass derselbe Ton zwei- oder mehrmals fast gleichzeitig wiedergegeben wird. In diesem Fall sind die Töne _phasenverschoben_, was zu sehr auffälligen Artefakten führen kann.

![Phasenverschiebung](images/sound/sound_phase_shift.png)

Am einfachsten lässt sich dieses Problem mit einem Sperrmechanismus (Gate) lösen, der Audionachrichten filtert und verhindert, dass derselbe Ton innerhalb eines festgelegten Zeitintervalls mehr als einmal wiedergegeben wird:

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

Um den Sperrmechanismus zu verwenden, sende ihm einfach eine Nachricht `play_gated_sound` und gib die Ziel-Audiokomponente und den Verstärkungsfaktor des Tons an. Wenn die Sperre offen ist, ruft der Sperrmechanismus `sound.play()` mit der Ziel-Audiokomponente auf:

```lua
msg.post("/sound_gate#script", "play_gated_sound", { soundcomponent = "/sounds#explosion1", gain = 1.0 })
```

::: important
Es funktioniert nicht, den Sperrmechanismus auf Nachrichten `play_sound` reagieren zu lassen, da dieser Name von der Defold-Engine reserviert ist. Wenn du reservierte Nachrichtennamen verwendest, tritt unerwartetes Verhalten auf.
:::


## Änderungen zur Laufzeit {#runtime-manipulation}
Du kannst Töne zur Laufzeit über verschiedene Eigenschaften verändern (Informationen zur Verwendung findest du in der [API-Dokumentation](/ref/sound/)). Die folgenden Eigenschaften lassen sich mit `go.get()` und `go.set()` verändern:

`gain`
: Der Verstärkungsfaktor der Audiokomponente (`number`).

`pan`
: Das Stereopanorama der Audiokomponente (`number`). Der Wert muss zwischen -1 (-45 Grad links) und 1 (45 Grad rechts) liegen.

`speed`
: Die Wiedergabegeschwindigkeit der Audiokomponente (`number`). Ein Wert von 1.0 entspricht der normalen Geschwindigkeit, 0.5 der halben und 2.0 der doppelten Geschwindigkeit.

`sound`
: Der Ressourcenpfad zum Ton (`hash`). Du kannst den Ressourcenpfad verwenden, um den Ton mit `resource.set_sound(path, buffer)` zu ändern. Beispiel:

```lua
local boom = sys.load_resource("/sounds/boom.wav")
local path = go.get("#sound", "sound")
resource.set_sound(path, boom)
```


## Projektkonfiguration {#project-configuration}

Die Datei *game.project* enthält einige [Projekteinstellungen](/manuals/project-settings#sound) für Audiokomponenten.

## Audiostreaming {#sound-streaming}

Du kannst auch [Töne streamen](/manuals/sound-streaming)
