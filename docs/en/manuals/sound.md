---
title: Sound in Defold
brief: This manual explains how you bring sounds into your Defold project, play back and control them.
---

# Sound

Defold's sound implementation is simple but powerful. There are only two concepts that you need to be aware of:

Sound components
: These components contain an actual sound that should be played and is able to play back the sound.

Sound groups
: Each sound component can be designated to belong to a _group_. Groups offer an easy way to manage sounds that belong together in an intuitive way. For instance, a group "sound_fx" can be set up and any sound belonging to that group can be ducked by a simple function call.

## Creating a sound component

Sound components can only be instanced in-place in a game object. Create a new game object, right click on it and select *Add Component*. Select *Sound* and press *OK*.

![Select component](images/sound/sound_select_component.png)

The created component has a set of properties that should be set:

*Sound*
: Should be set to a sound file in your project. The file should be in _Wave_ or _Ogg Vorbis_ format (See http://en.wikipedia.org/wiki/WAV and http://en.wikipedia.org/wiki/Vorbis for details).

*Looping*
: If checked the sound will playback looping until explicitly stopped.

*Gain*
: You can set the gain for the sound directly on the component. This allows you to easily tweak the gain for a sound without going back to your sound program and perform a re-export. See below for details on how gain is calculated.

*Group*
: The name of the sound group the sound should belong to. If this property is left empty, the sound will be assigned to the built-in "master" group.

![Create component](images/sound/sound_create_component.png)

## Gain

![Gain](images/sound/sound_gain.png)

The sound system has 4 levels of gain:

- The gain set on the sound component.
- The gain set when starting the sound via a `play_sound` message or when changing the gain on the voice via a `set_gain` message.
- The gain set on the group via a [`sound.set_group_gain()`](/ref/sound#sound.set_group_gain) function call.
- The gain set on the "master" group. This can be altered by `sound.set_group_gain(hash("master"))`.

The output gain is the result of these 4 gains multiplied. The default gain is 1.0 everywhere (0 dB).

## Sound groups

Any sound component with a sound group name specified will be put in a sound group with that name. If you don't specify a group the sound will be assigned to the "master" group. You can also explicitly set the group on a sound component to "master" which has the same effect.

A few functions are available to get all available groups, get the string name, get and set gain, rms (see http://en.wikipedia.org/wiki/Root_mean_square) and peak gain. There is also a function that allows you to test if the target device's music player is running:

```lua
-- If sound playing on this iPhone/Android device, silence everything
if sound.is_music_playing() then
    for i, group_hash in ipairs(sound.get_groups()) do
        sound.set_group_gain(group_hash, 0)
    end
end
```

The groups are identified with a hash value. The string name can be retrieved with [`sound.get_group_name()`](/ref/sound#sound.get_group_name) which can be used to display group names in development tools, for instance a mixer to test group levels.

![Sound group mixer](images/sound/sound_mixer.png)

::: important
You should not write code that rely on the string value of a sound group since it is not available in release builds.
:::

All values are linear between 0 and 1.0 (0 dB). To convert to decibel, simply use the standard formula:

$$
db = 20 \times \log \left( gain \right)
$$

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

## Gating sounds

If your game plays the same sound on an event and that event is triggered often, you run the risk of playing the same sound two times or more almost at the same time. If that happens, the sounds will be _phase shifted_ which can result in some very noticeable artifacts. 

![Phase shift](images/sound/sound_phase_shift.png)

The easiest way to deal with this problem is to build a gate that filters sound messages and does not allow the same sound to be played more than once within a set interval:

```lua
-- Don't allow the same sound to be played within "gate_time" interval.
local gate_time = 0.3

function init(self)
    -- Store played sound timers in table and count down each frame until they have been 
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
            -- Redirect the "play_sound" message to the real target
            msg.post(message.soundcomponent, "play_sound", { gain = message.gain })
        else
            -- An attempt to play a sound was gated
            print("gated " .. message.soundcomponent)
        end
    end
end
```

To use the gate, simply send it a `play_gated_sound` message and specify the target sound component and sound gain. The gate will send a `play_sound` message to the target sound component if the gate is open:

```lua
msg.post("/sound_gate#script", "play_gated_sound", { soundcomponent = "/sounds#explosion1", gain = 1.0 })
```

::: important
It does not work to have the gate listen to `play_sound` messages since that name is reserved by the Defold engine. You will get unexpected behavior if you do use reserved message names.
:::

