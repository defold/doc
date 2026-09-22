---
title: Звук у Defold
brief: Цей посібник пояснює, як додавати звуки до проєкту Defold, відтворювати їх і керувати ними.
---

# Звук {#sound}

Реалізація звуку в Defold проста, але потужна. Вам потрібно знати лише два поняття:

Звукові компоненти (sound components)
: Ці компоненти містять сам звук, який потрібно відтворити, і можуть його відтворювати.

Групи звуків (sound groups)
: Кожен звуковий компонент можна призначити до певної _групи_. Групи дають змогу легко й інтуїтивно керувати звуками, які пов’язані між собою. Наприклад, можна створити групу `sound_fx` і приглушувати будь-який звук із цієї групи простим викликом функції.

## Створення звукового компонента {#creating-a-sound-component}

Екземпляри звукових компонентів можна створювати лише на місці (in-place) в ігровому об’єкті (game object). Створіть новий ігровий об’єкт, клацніть його правою кнопкою миші, виберіть <kbd>Add Component ▸ Sound</kbd> і натисніть *OK*.

![Вибір компонента](images/sound/sound_add_component.jpg)

Створений компонент має набір властивостей, які потрібно налаштувати:

![Вибір компонента](images/sound/sound_properties.png)

*Sound*
: Укажіть звуковий файл у вашому проєкті. Файл має бути у форматі _Wave_, _Ogg Vorbis_ або _Ogg Opus_. Defold підтримує 8-бітні та 16-бітні файли PCM Wave. Відтворення Ogg Opus необов’язкове й потребує ввімкнення **Include Sound Decoder: Opus** у [маніфесті застосунку](/manuals/app-manifest/#sound); декодер Opus типово не включено.

*Looping*
: Якщо позначено, звук відтворюватиметься стільки разів, скільки вказано в _Loopcount_, або доки його явно не зупинять.

*Loopcount*
: Кількість повторів зацикленого звуку до зупинки (0 означає, що звук повторюватиметься, доки його явно не зупинять).

*Group*
: Назва групи звуків, до якої має належати звук. Якщо залишити цю властивість порожньою, звук буде призначено до вбудованої групи `master`.

*Gain*
: Коефіцієнт підсилення звуку можна задати безпосередньо в компоненті. Це дає змогу легко відрегулювати підсилення звуку, не повертаючись до програми для роботи зі звуком і не експортуючи його повторно. Докладніше про обчислення підсилення дивіться нижче.

*Pan*
: Панораму звуку можна задати безпосередньо в компоненті. Значення панорами має бути в межах від -1 (-45 градусів ліворуч) до 1 (45 градусів праворуч).

*Speed*
: Швидкість відтворення звуку можна задати безпосередньо в компоненті. Значення 1.0 відповідає звичайній швидкості, 0.5 — удвічі повільнішій, а 2.0 — удвічі швидшій.


## Відтворення звуку {#playing-the-sound}

Налаштувавши звуковий компонент, ви можете запустити відтворення його звуку викликом [`sound.play()`](/ref/sound/#sound.play:url-[play_properties]-[complete_function]):

```lua
sound.play("go#sound", {delay = 1, gain = 0.5, pan = -1.0, speed = 1.25})
```

::: sidenote
Звук продовжить відтворюватися, навіть якщо видалити ігровий об’єкт, якому належав звуковий компонент. Щоб зупинити звук, можна викликати [`sound.stop()`](/ref/sound/#sound.stop:url) (дивіться нижче).
:::
Кожне повідомлення, надіслане компоненту, запускає відтворення ще одного екземпляра звуку, доки не заповниться доступний звуковий буфер і рушій не почне виводити помилки в консоль. Радимо реалізувати механізм обмеження частоти відтворення та групування звуків.

## Зупинка звуку {#stopping-the-sound}

Щоб зупинити відтворення звуку, викличте [`sound.stop()`](/ref/sound/#sound.stop:url):

```lua
sound.stop("go#sound")
```

## Підсилення {#gain}

![Підсилення](images/sound/sound_gain.png)

Звукова система має 4 рівні підсилення:

- Підсилення, задане у звуковому компоненті.
- Підсилення, задане під час запуску звуку викликом `sound.play()` або під час зміни підсилення відтворюваного екземпляра викликом `sound.set_gain()`.
- Підсилення, задане для групи викликом функції [`sound.set_group_gain()`](/ref/sound#sound.set_group_gain).
- Підсилення, задане для групи `master`. Його можна змінити за допомогою `sound.set_group_gain(hash("master"), gain)`.

Якщо в [налаштуваннях звуку проєкту](/manuals/project-settings/#sound) увімкнено **Use Linear Gain** (типово ввімкнено), вихідний коефіцієнт підсилення дорівнює добутку цих чотирьох коефіцієнтів. Значення `1.0` відповідає одиничному коефіцієнту підсилення (0 дБ). Якщо лінійне підсилення вимкнено, Defold застосовує нелінійну криву під час мікшування, тому пряме множення чотирьох коефіцієнтів і наведене нижче перетворення в децибели не описують кінцевий вихідний рівень.

## Групи звуків {#sound-groups}

Будь-який звуковий компонент, для якого вказано назву групи звуків, потрапляє до групи з цією назвою. Якщо не вказати групу, звук буде призначено до групи `master`. Можна також явно задати для звукового компонента групу `master` — результат буде той самий.

Доступні функції для отримання всіх наявних груп, отримання їхніх назв у вигляді рядків, отримання й установлення підсилення, а також отримання середньоквадратичного значення (rms, дивіться http://en.wikipedia.org/wiki/Root_mean_square) і пікового підсилення. Також є функція, яка дає змогу перевірити, чи працює музичний програвач на цільовому пристрої:

```lua
-- If sound playing on this iPhone/Android device, silence everything
if sound.is_music_playing() then
    for i, group_hash in ipairs(sound.get_groups()) do
        sound.set_group_gain(group_hash, 0)
    end
end
```

Групи ідентифікуються хешованим значенням. Назву у вигляді рядка можна отримати за допомогою [`sound.get_group_name()`](/ref/sound#sound.get_group_name), щоб відображати назви груп в інструментах розробки, наприклад у мікшері для перевірки рівнів груп.

![Мікшер груп звуків](images/sound/sound_mixer.png)

::: important
Не пишіть код, який покладається на рядкові назви груп звуків, оскільки вони недоступні у збірках випуску.
:::

Якщо **Use Linear Gain** увімкнено, перетворюйте додатне значення коефіцієнта підсилення в децибели за стандартною формулою:

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

У Defold 1.10.2 виправлено давнє послаблення сигналу приблизно на 3 дБ у звуковому мікшері. Якщо мікс старішого проєкту компенсував це послаблення й після оновлення звучить голосніше, відрегулюйте глобальне налаштування **Sound ▸ Gain** або підсилення відповідних груп.

## Обмеження частоти відтворення звуків {#gating-sounds}

Якщо гра відтворює певний звук у відповідь на подію, яка часто спрацьовує, той самий звук може відтворитися двічі або більше майже одночасно. У такому разі звуки матимуть _зсув фази_, що може спричинити дуже помітні артефакти.

![Зсув фази](images/sound/sound_phase_shift.png)

Найпростіший спосіб розв’язати цю проблему — створити обмежувач, який фільтрує звукові повідомлення й не дає відтворювати той самий звук більше одного разу протягом заданого інтервалу:

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

Щоб скористатися обмежувачем, надішліть йому повідомлення `play_gated_sound`, указавши цільовий звуковий компонент і коефіцієнт підсилення звуку. Якщо обмежувач пропускає відтворення, він викличе `sound.play()` для цільового звукового компонента:

```lua
msg.post("/sound_gate#script", "play_gated_sound", { soundcomponent = "/sounds#explosion1", gain = 1.0 })
```

::: important
Обмежувач не може обробляти повідомлення `play_sound`, оскільки цю назву зарезервовано рушієм Defold. Використання зарезервованих назв повідомлень призведе до неочікуваної поведінки.
:::


## Керування під час виконання {#runtime-manipulation}
Керувати звуками під час виконання можна за допомогою низки властивостей (способи використання наведено в [документації API](/ref/sound/)). За допомогою `go.get()` і `go.set()` можна працювати з такими властивостями:

`gain`
: Коефіцієнт підсилення звукового компонента (`number`).

`pan`
: Панорама звукового компонента (`number`). Значення панорами має бути в межах від -1 (-45 градусів ліворуч) до 1 (45 градусів праворуч).

`speed`
: Швидкість відтворення звукового компонента (`number`). Значення 1.0 відповідає звичайній швидкості, 0.5 — удвічі повільнішій, а 2.0 — удвічі швидшій.

`sound`
: Шлях до ресурсу звуку (`hash`). Цей шлях можна використати, щоб змінити звук за допомогою `resource.set_sound(path, buffer)`. Приклад:

```lua
local boom = sys.load_resource("/sounds/boom.wav")
local path = go.get("#sound", "sound")
resource.set_sound(path, boom)
```


## Налаштування проєкту {#project-configuration}

Файл *game.project* містить кілька [налаштувань проєкту](/manuals/project-settings#sound), пов’язаних зі звуковими компонентами.

## Потокове відтворення звуку {#sound-streaming}

Також можна підтримувати [потокове відтворення звуків](/manuals/sound-streaming)
