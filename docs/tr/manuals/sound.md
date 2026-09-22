---
title: Defold'da ses
brief: Bu kılavuz, sesleri Defold projenize nasıl ekleyeceğinizi, oynatacağınızı ve kontrol edeceğinizi açıklar.
---

# Ses

Defold'un ses sistemi basit ama güçlüdür. Bilmeniz gereken yalnızca iki kavram vardır:

Ses bileşenleri
: Bu bileşenler (sound component), oynatılacak asıl sesi içerir ve bu sesi oynatabilir.

Ses grupları
: Her ses bileşeni bir _gruba_ (sound group) ait olacak şekilde atanabilir. Gruplar, birbiriyle ilişkili sesleri anlaşılır bir şekilde yönetmenin kolay bir yolunu sunar. Örneğin, bir `sound_fx` grubu oluşturulabilir ve bu gruba ait herhangi bir ses, basit bir işlev çağrısıyla kısılabilir.

## Ses bileşeni oluşturma

Ses bileşenlerinin örnekleri yalnızca bir oyun nesnesi (game object) içinde yerinde oluşturulabilir. Yeni bir oyun nesnesi oluşturun, üzerine sağ tıklayıp <kbd>Add Component ▸ Sound</kbd> seçeneğini seçin ve *OK* düğmesine basın.

![Bileşen seçme](images/sound/sound_add_component.jpg)

Oluşturulan bileşenin ayarlanması gereken bir dizi özelliği vardır:

![Bileşen seçme](images/sound/sound_properties.png)

*Sound*
: Projenizdeki bir ses dosyasına ayarlamanız önerilir. Dosyanın _Wave_, _Ogg Vorbis_ veya _Ogg Opus_ biçiminde olması önerilir. Defold, 8 bit ve 16 bit PCM Wave dosyalarını destekler. Ogg Opus oynatma isteğe bağlıdır ve [App Manifest](/manuals/app-manifest/#sound) içinde **Include Sound Decoder: Opus** seçeneğini gerektirir; Opus kod çözücüsü varsayılan olarak dahil edilmez.

*Looping*
: İşaretlendiğinde ses, _Loopcount_ kez veya açıkça durdurulana kadar oynatılır.

*Loopcount*
: Döngüde oynatılan bir sesin durmadan önce kaç kez oynatılacağıdır (0, sesin açıkça durdurulana kadar döngüde oynatılacağı anlamına gelir).

*Group*
: Sesin ait olacağı ses grubunun adıdır. Bu özellik boş bırakılırsa ses, yerleşik `master` grubuna atanır.

*Gain*
: Sesin kazancını (gain) doğrudan bileşen üzerinde ayarlayabilirsiniz. Böylece ses programınıza dönüp yeniden dışa aktarmadan sesin kazancını kolayca düzenleyebilirsiniz. Kazancın nasıl hesaplandığına ilişkin ayrıntılar için aşağıya bakın.

*Pan*
: Sesin stereo konumu (pan) değerini doğrudan bileşen üzerinde ayarlayabilirsiniz. Stereo konumunun -1 (sola -45 derece) ile 1 (sağa 45 derece) arasında bir değer olması gerekir.

*Speed*
: Sesin hız değerini doğrudan bileşen üzerinde ayarlayabilirsiniz. 1.0 değeri normal hız, 0.5 yarı hız, 2.0 ise iki kat hızdır.


## Sesi oynatma

Bir ses bileşenini doğru şekilde ayarladığınızda, [`sound.play()`](/ref/sound/#sound.play:url-[play_properties]-[complete_function]) işlevini çağırarak sesini oynatmasını sağlayabilirsiniz:

```lua
sound.play("go#sound", {delay = 1, gain = 0.5, pan = -1.0, speed = 1.25})
```

::: sidenote
Ses bileşeninin ait olduğu oyun nesnesi silinse bile ses oynatılmaya devam eder. Sesi durdurmak için [`sound.stop()`](/ref/sound/#sound.stop:url) işlevini çağırabilirsiniz (aşağıya bakın).
:::
Bileşene gönderilen her ileti, kullanılabilir ses arabelleği dolana ve motor konsola hatalar yazdırana kadar sesin başka bir örneğini oynatmasına neden olur. Ses oynatma aralığını sınırlayan (gating) ve sesleri gruplayan bir mekanizma uygulamanız önerilir.

## Sesi durdurma

Bir sesin oynatılmasını durdurmak istiyorsanız [`sound.stop()`](/ref/sound/#sound.stop:url) işlevini çağırabilirsiniz:

```lua
sound.stop("go#sound")
```

## Kazanç

![Kazanç](images/sound/sound_gain.png)

Ses sisteminde 4 kazanç düzeyi vardır:

- Ses bileşeninde ayarlanan kazanç.
- Sesi `sound.play()` çağrısıyla başlatırken veya oynatılan ses örneğinin (voice) kazancını `sound.set_gain()` çağrısıyla değiştirirken ayarlanan kazanç.
- Grupta bir [`sound.set_group_gain()`](/ref/sound#sound.set_group_gain) işlev çağrısıyla ayarlanan kazanç.
- `master` grubunda ayarlanan kazanç. Bu değer, `sound.set_group_gain(hash("master"), gain)` ile değiştirilebilir.

[Sound proje ayarlarında](/manuals/project-settings/#sound) **Use Linear Gain** etkin olduğunda (varsayılan durum), çıkış kazancı bu dört kazancın çarpımının sonucudur. `1.0` kazancı, birim kazançtır (0 dB). Doğrusal kazanç devre dışı bırakıldığında Defold, sesleri karıştırırken doğrusal olmayan bir eğri uygular; bu nedenle aşağıdaki dört değerin doğrudan çarpımı ve desibele dönüştürülmesi, oluşan çıkış seviyesini açıklamaz.

## Ses grupları

Ses grubu adı belirtilen her ses bileşeni, o ada sahip bir ses grubuna yerleştirilir. Bir grup belirtmezseniz ses, `master` grubuna atanır. Ses bileşeninin grubunu açıkça `master` olarak da ayarlayabilirsiniz; bunun etkisi aynıdır.

Kullanılabilir tüm grupları ve dize biçimindeki adlarını almak, kazancı almak ve ayarlamak, RMS (bkz. http://en.wikipedia.org/wiki/Root_mean_square) ve tepe kazanç değerlerini almak için birkaç işlev vardır. Hedef cihazın müzik çalarının çalışıp çalışmadığını sınamanızı sağlayan bir işlev de vardır:

```lua
-- If sound playing on this iPhone/Android device, silence everything
if sound.is_music_playing() then
    for i, group_hash in ipairs(sound.get_groups()) do
        sound.set_group_gain(group_hash, 0)
    end
end
```

Gruplar bir karma (hash) değeriyle tanımlanır. Dize biçimindeki ad, [`sound.get_group_name()`](/ref/sound#sound.get_group_name) ile alınabilir. Bu işlev, örneğin grup seviyelerini sınamak için kullanılan bir mikser gibi geliştirme araçlarında grup adlarını göstermek için kullanılabilir.

![Ses grubu mikseri](images/sound/sound_mixer.png)

::: important
Yayıma yönelik derlemelerde bulunmadığından, bir ses grubunun dize değerine dayanan kod yazmanız önerilmez.
:::

**Use Linear Gain** etkinken, pozitif bir kazanç değerini standart formülle desibele dönüştürün:

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

Defold 1.10.2, ses mikserinde uzun süredir var olan yaklaşık 3 dB'lik zayıflamayı düzeltti. Eski bir projenin ses karışımı bu zayıflamayı telafi edecek şekilde ayarlanmışsa ve yükseltme sonrasında daha yüksek ses veriyorsa, genel **Sound ▸ Gain** ayarını veya etkilenen grup kazançlarını yeniden ayarlayın.

## Ses oynatma aralığını sınırlama

Oyununuz bir olay gerçekleştiğinde aynı sesi oynatıyorsa ve bu olay sık tetikleniyorsa, aynı sesi neredeyse aynı anda iki veya daha fazla kez oynatma riski vardır. Bu durumda sesler arasında _faz kayması_ (phase shift) oluşur ve bu da oldukça belirgin ses kusurlarına yol açabilir.

![Faz kayması](images/sound/sound_phase_shift.png)

Bu sorunu çözmenin en kolay yolu, ses iletilerini filtreleyen ve belirlenen bir zaman aralığında aynı sesin birden fazla kez oynatılmasına izin vermeyen bir geçit (gate) oluşturmaktır:

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

Geçidi kullanmak için ona bir `play_gated_sound` iletisi gönderip hedef ses bileşenini ve ses kazancını belirtmeniz yeterlidir. Geçit açıksa hedef ses bileşeniyle `sound.play()` işlevini çağırır:

```lua
msg.post("/sound_gate#script", "play_gated_sound", { soundcomponent = "/sounds#explosion1", gain = 1.0 })
```

::: important
Geçidin `play_sound` iletilerini dinlemesi işe yaramaz; bu ad Defold motoru tarafından ayrılmıştır. Ayrılmış ileti adlarını kullanırsanız beklenmedik davranışlarla karşılaşırsınız.
:::


## Çalışma sırasında değiştirme
Sesleri çalışma sırasında çeşitli özellikler aracılığıyla değiştirebilirsiniz (kullanım için [API belgelerine](/ref/sound/) bakın). Aşağıdaki özellikler `go.get()` ve `go.set()` kullanılarak değiştirilebilir:

`gain`
: Ses bileşeninin kazancıdır (`number`).

`pan`
: Ses bileşeninin stereo konumudur (`number`). Stereo konumunun -1 (sola -45 derece) ile 1 (sağa 45 derece) arasında bir değer olması gerekir.

`speed`
: Ses bileşeninin hızıdır (`number`). 1.0 değeri normal hız, 0.5 yarı hız, 2.0 ise iki kat hızdır.

`sound`
: Sesin kaynak yoludur (`hash`). Kaynak yolunu kullanarak sesi `resource.set_sound(path, buffer)` ile değiştirebilirsiniz. Örnek:

```lua
local boom = sys.load_resource("/sounds/boom.wav")
local path = go.get("#sound", "sound")
resource.set_sound(path, boom)
```


## Proje yapılandırması

*game.project* dosyasında ses bileşenleriyle ilgili birkaç [proje ayarı](/manuals/project-settings#sound) bulunur.

## Akış yoluyla ses oynatma

[Akış yoluyla ses oynatma](/manuals/sound-streaming) desteği sağlamak da mümkündür
