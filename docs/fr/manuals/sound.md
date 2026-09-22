---
title: Le son dans Defold
brief: Ce manuel explique comment ajouter des sons à votre projet Defold, les lire et les contrôler.
---

# Le son {#sound}

Le système audio de Defold est simple mais puissant. Vous n'avez besoin de connaître que deux concepts :

Composants audio
: Chaque composant (component) contient le son à jouer et peut en assurer la lecture.

Groupes de sons
: Chaque composant audio peut être affecté à un _groupe_. Les groupes permettent de gérer facilement et intuitivement les sons qui vont ensemble. Par exemple, vous pouvez créer un groupe `sound_fx` et atténuer les sons de ce groupe par un simple appel de fonction.

## Création d'un composant audio {#creating-a-sound-component}

Les composants audio ne peuvent être instanciés que directement dans un objet de jeu (game object). Créez un nouvel objet de jeu, faites un clic droit dessus, sélectionnez <kbd>Add Component ▸ Sound</kbd> et appuyez sur *OK*.

![Sélection du composant](images/sound/sound_add_component.jpg)

Le composant créé possède un ensemble de propriétés à configurer :

![Sélection du composant](images/sound/sound_properties.png)

*Sound*
: Doit désigner un fichier audio de votre projet. Le fichier doit être au format _Wave_, _Ogg Vorbis_ ou _Ogg Opus_. Defold prend en charge les fichiers Wave PCM 8 bits et 16 bits. La lecture Ogg Opus est facultative et nécessite **Include Sound Decoder: Opus** dans le [manifeste de l'application](/manuals/app-manifest/#sound) ; le décodeur Opus n'est pas inclus par défaut.

*Looping*
: Si cette option est cochée, le son sera lu _Loopcount_ fois ou jusqu'à son arrêt explicite.

*Loopcount*
: Le nombre de fois qu'un son en boucle sera lu avant de s'arrêter (0 signifie que le son doit être lu en boucle jusqu'à son arrêt explicite).

*Group*
: Le nom du groupe de sons auquel le son doit appartenir. Si cette propriété est laissée vide, le son sera affecté au groupe intégré `master`.

*Gain*
: Vous pouvez définir le gain du son directement sur le composant. Cela vous permet d'ajuster facilement le gain d'un son sans revenir à votre logiciel audio pour l'exporter à nouveau. Voir ci-dessous pour les détails du calcul du gain.

*Pan*
: Vous pouvez définir la valeur du panoramique du son directement sur le composant. Le panoramique doit être une valeur comprise entre -1 (-45 degrés à gauche) et 1 (45 degrés à droite).

*Speed*
: Vous pouvez définir la vitesse du son directement sur le composant. Une valeur de 1.0 correspond à la vitesse normale, 0.5 à la moitié de la vitesse et 2.0 au double de la vitesse.


## Lecture du son {#playing-the-sound}

Une fois votre composant audio correctement configuré, vous pouvez déclencher la lecture du son en appelant [`sound.play()`](/ref/sound/#sound.play:url-[play_properties]-[complete_function]) :

```lua
sound.play("go#sound", {delay = 1, gain = 0.5, pan = -1.0, speed = 1.25})
```

::: sidenote
Un son continue d'être lu même si l'objet de jeu auquel appartenait le composant audio est supprimé. Vous pouvez appeler [`sound.stop()`](/ref/sound/#sound.stop:url) pour arrêter le son (voir ci-dessous).
:::
Chaque message envoyé à un composant lui fait jouer une instance supplémentaire du son, jusqu'à ce que le tampon audio disponible soit plein et que le moteur affiche des erreurs dans la console. Il est conseillé de mettre en place un mécanisme de filtrage des déclenchements et de regroupement des sons.

## Arrêt du son {#stopping-the-sound}

Si vous souhaitez arrêter la lecture d'un son, vous pouvez appeler [`sound.stop()`](/ref/sound/#sound.stop:url) :

```lua
sound.stop("go#sound")
```

## Gain {#gain}

![Gain](images/sound/sound_gain.png)

Le système audio possède quatre niveaux de gain :

- Le gain défini sur le composant audio.
- Le gain défini au démarrage du son par un appel à `sound.play()` ou lors de la modification du gain de la voix par un appel à `sound.set_gain()`.
- Le gain défini sur le groupe par un appel à la fonction [`sound.set_group_gain()`](/ref/sound#sound.set_group_gain).
- Le gain défini sur le groupe `master`. Vous pouvez le modifier avec `sound.set_group_gain(hash("master"), gain)`.

Lorsque **Use Linear Gain** est activé dans les [paramètres audio du projet](/manuals/project-settings/#sound) (par défaut), le gain de sortie est le produit de ces quatre gains. Un gain de `1.0` est un gain unitaire (0 dB). Lorsque le gain linéaire est désactivé, Defold applique une courbe non linéaire lors du mixage ; la multiplication directe des quatre gains et la conversion en décibels ci-dessous ne décrivent donc pas le niveau de sortie obtenu.

## Groupes de sons {#sound-groups}

Tout composant audio pour lequel un nom de groupe de sons est spécifié sera placé dans un groupe de sons portant ce nom. Si vous ne spécifiez pas de groupe, le son sera affecté au groupe `master`. Vous pouvez aussi définir explicitement le groupe d'un composant audio sur `master`, ce qui a le même effet.

Plusieurs fonctions permettent de récupérer tous les groupes disponibles, d'obtenir leur nom sous forme de chaîne de caractères, d'obtenir et de définir le gain, et de connaître la valeur efficace (RMS, voir http://en.wikipedia.org/wiki/Root_mean_square) et le gain de crête. Une autre fonction vous permet de vérifier si le lecteur de musique de l'appareil cible est en cours d'exécution :

```lua
-- If sound playing on this iPhone/Android device, silence everything
if sound.is_music_playing() then
    for i, group_hash in ipairs(sound.get_groups()) do
        sound.set_group_gain(group_hash, 0)
    end
end
```

Les groupes sont identifiés par une valeur hachée. Vous pouvez récupérer le nom sous forme de chaîne de caractères avec [`sound.get_group_name()`](/ref/sound#sound.get_group_name) pour afficher les noms de groupes dans des outils de développement, par exemple une table de mixage permettant de tester les niveaux des groupes.

![Table de mixage des groupes de sons](images/sound/sound_mixer.png)

::: important
Vous ne devez pas écrire de code qui dépend du nom d'un groupe de sons sous forme de chaîne de caractères, car ces chaînes ne sont pas disponibles dans les builds de publication.
:::

Lorsque **Use Linear Gain** est activé, convertissez une valeur de gain positive en décibels à l'aide de la formule standard :

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

Defold 1.10.2 a corrigé une atténuation d'environ 3 dB présente depuis longtemps dans le mixeur audio. Si le mixage d'un ancien projet compensait cette atténuation et que le son est plus fort après la mise à jour, réajustez le paramètre global **Sound ▸ Gain** ou les gains des groupes concernés.

## Filtrage des déclenchements sonores {#gating-sounds}

Si votre jeu joue le même son en réponse à un événement et que cet événement se déclenche souvent, vous risquez de jouer le même son deux fois ou plus presque au même moment. Dans ce cas, les sons seront _déphasés_, ce qui peut entraîner des artefacts très perceptibles.

![Déphasage](images/sound/sound_phase_shift.png)

La manière la plus simple de résoudre ce problème consiste à créer un filtre qui traite les messages sonores et empêche de jouer un même son plus d'une fois dans un intervalle donné :

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

Pour utiliser le filtre, envoyez-lui simplement un message `play_gated_sound` en précisant le composant audio cible et le gain du son. Si le filtre autorise la lecture, il appelle `sound.play()` avec le composant audio cible :

```lua
msg.post("/sound_gate#script", "play_gated_sound", { soundcomponent = "/sounds#explosion1", gain = 1.0 })
```

::: important
Le filtre ne peut pas écouter les messages `play_sound`, car ce nom est réservé par le moteur Defold. Vous obtiendrez un comportement inattendu si vous utilisez des noms de messages réservés.
:::


## Manipulation à l'exécution {#runtime-manipulation}
Vous pouvez manipuler les sons à l'exécution à l'aide de différentes propriétés (consultez la [documentation de l'API pour leur utilisation](/ref/sound/)). Les propriétés suivantes peuvent être manipulées avec `go.get()` et `go.set()` :

`gain`
: Le gain du composant audio (`number`).

`pan`
: Le panoramique du composant audio (`number`). Le panoramique doit être une valeur comprise entre -1 (-45 degrés à gauche) et 1 (45 degrés à droite).

`speed`
: La vitesse du composant audio (`number`). Une valeur de 1.0 correspond à la vitesse normale, 0.5 à la moitié de la vitesse et 2.0 au double de la vitesse.

`sound`
: Le chemin de la ressource du son (`hash`). Vous pouvez utiliser ce chemin pour modifier le son avec `resource.set_sound(path, buffer)`. Exemple :

```lua
local boom = sys.load_resource("/sounds/boom.wav")
local path = go.get("#sound", "sound")
resource.set_sound(path, boom)
```


## Configuration du projet {#project-configuration}

Le fichier *game.project* comporte quelques [paramètres du projet](/manuals/project-settings#sound) relatifs aux composants audio.

## Lecture des sons en streaming {#sound-streaming}

Il est également possible de prendre en charge la [lecture des sons en streaming](/manuals/sound-streaming)
