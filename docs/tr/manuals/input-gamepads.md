---
title: Defold'da oyun kumandası girdisi
brief: Bu kılavuz, oyun kumandası girdisinin nasıl çalıştığını açıklar.
---

::: sidenote
Defold'da girdinin genel olarak nasıl çalıştığını, girdinin nasıl alındığını ve betik dosyalarınızda hangi sırayla alındığını öğrenmeniz önerilir. Girdi sistemi hakkında daha fazla bilgi için [Girdiye genel bakış kılavuzuna](/manuals/input) bakın.
:::

# Oyun kumandaları
Oyun kumandası (gamepad) tetikleyicileri, standart oyun kumandası girdisini oyun işlevlerine bağlamanızı sağlar. Oyun kumandası girdisi şu öğeler için girdi eşlemeleri (input binding) sunar:

- Sol ve sağ çubuklar (yön ve tıklamalar)
- Sol ve sağ dijital düğme grupları (digital pads). Sağ düğme grubu genellikle Xbox oyun kumandasında "A", "B", "X" ve "Y" düğmelerine, Playstation oyun kumandasında ise "square", "circle", "triangle" ve "cross" düğmelerine karşılık gelir.
- Sol ve sağ tetikler
- Sol ve sağ omuz düğmeleri
- Start, Back ve Guide düğmeleri

![](images/input/gamepad_bindings.png)

::: important
Aşağıdaki örneklerde, yukarıdaki görüntüde gösterilen eylemler kullanılır. Tüm girdilerde olduğu gibi, girdi eylemlerinizi istediğiniz şekilde adlandırabilirsiniz.
:::

## Dijital düğmeler
Dijital düğmeler `pressed`, `released` ve `repeated` olayları üretir. Aşağıdaki örnek, bir dijital düğmenin girdisinin (basılma veya bırakılma) nasıl algılandığını gösterir:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lpad_left") then
        if action.pressed then
            -- start moving left
        elseif action.released then
            -- stop moving left
        end
    end
end
```

## Analog çubuklar
Analog çubuklar (analog stick), oyun kumandası ayar dosyasında tanımlanan ölü bölgenin (dead zone) dışına hareket ettirildiğinde sürekli girdi olayları üretir (aşağıya bakın). Aşağıdaki örnek, bir analog çubuğun girdisinin nasıl algılandığını gösterir:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") then
        -- left stick was moved down
        print(action.value) -- a value between 0.0 an -1.0
    end
end
```

Analog çubuklar, ana yönlerde belirli bir eşik değerinin ötesine hareket ettirildiğinde `pressed` ve `released` olayları da üretir. Böylece bir analog çubuğu dijital yön girdisi olarak da kullanmak kolaylaşır:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") and action.pressed then
        -- left stick was moved to its extreme down position
    end
end
```

## Birden fazla oyun kumandası
Defold, üzerinde çalıştığı işletim sistemi aracılığıyla birden fazla oyun kumandasını destekler. Eylemler, `action` tablosunun `gamepad` alanını girdinin geldiği oyun kumandasının numarasına ayarlar:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_start") then
        if action.gamepad == 0 then
          -- gamepad 0 wants to join the game
        end
    end
end
```

## Bağlanma ve bağlantının kesilmesi
Oyun kumandası girdi eşlemeleri, bir oyun kumandasının bağlandığını (başlangıçtan itibaren bağlı olanlar dahil) veya bağlantısının kesildiğini algılamak için `Connected` ve `Disconnected` adlı iki ayrı eşleme de sağlar.

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_connected") then
        if action.gamepad == 0 then
          -- gamepad 0 was connected
        end
    elseif action_id == hash("gamepad_disconnected") then
        if action.gamepad == 0 then
          -- gamepad 0 was disconnected
        end
    end
end
```

## Ham oyun kumandası girdileri

Oyun kumandası girdi eşlemeleri, bağlı herhangi bir oyun kumandasının filtrelenmemiş (ölü bölge uygulanmamış) düğme, eksen ve yön anahtarı (hat) girdisini sağlamak için `Raw` adlı ayrı bir eşleme de sunar.

```lua
function on_input(self, action_id, action)
    if action_id == hash("raw") then
        pprint(action.gamepad_buttons)
        pprint(action.gamepad_axis)
        pprint(action.gamepad_hats)
    end
end
```

## Oyun kumandası ayar dosyası {#gamepads-settings-file}
Oyun kumandası girdi yapılandırması, her donanımsal oyun kumandası türü için ayrı bir eşleme dosyası kullanır. Belirli donanımsal oyun kumandalarının eşlemeleri bir *gamepads* dosyasında ayarlanır. Defold, yaygın oyun kumandalarının ayarlarını içeren yerleşik bir gamepads dosyasıyla gelir:

![Oyun kumandası ayarları](images/input/gamepads.png)

Yeni bir oyun kumandası ayar dosyası oluşturmanız gerekiyorsa, bunun için basit bir aracımız var:

[gdc.zip dosyasını indirmek için tıklayın](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032).

Windows, Linux ve macOS için ikili dosyalar içerir. Komut satırından çalıştırın:

```sh
./gdc
```

Araç, bağlı oyun kumandanızdaki farklı düğmelere basmanızı ister. Ardından kumandanız için doğru eşlemeleri içeren yeni bir gamepads dosyası oluşturur. Yeni dosyayı kaydedin veya mevcut gamepads dosyanızla birleştirin, ardından *game.project* dosyasındaki ayarı güncelleyin:

![Oyun kumandası ayarları](images/input/gamepad_setting.png)

### Tanımlanamayan oyun kumandaları

Bir oyun kumandası bağlandığında bu kumanda için bir eşleme yoksa, kumanda yalnızca `connected`, `disconnected` ve `raw` eylemlerini üretir. Bu durumda ham oyun kumandası verilerini oyununuzdaki eylemlerle elle eşleştirmeniz gerekir.

`action` içindeki `gamepad_unknown` değerini okuyarak bir oyun kumandası girdi eyleminin bilinmeyen bir oyun kumandasından gelip gelmediğini kontrol edebilirsiniz:

```lua
function on_input(self, action_id, action)
    if action_id == hash("connected") then
        if action.gamepad_unknown then
            print("The connected gamepad is unidentified and will only generate raw input")
        else
            print("The connected gamepad is known and will generate input actions for buttons and sticks")
        end
    end
end
``` 

## HTML5'te oyun kumandaları {#gamepads-in-html5}
Oyun kumandaları HTML5 derlemelerinde desteklenir ve diğer platformlarla aynı girdi olaylarını üretir. Oyun kumandası desteği, çoğu tarayıcı tarafından desteklenen [Gamepad API](https://www.w3.org/TR/gamepad/) üzerine kuruludur ([bu destek tablosuna bakın](https://caniuse.com/?search=gamepad)). Tarayıcı Gamepad API desteği sunmuyorsa Defold, projenizdeki tüm oyun kumandası tetikleyicilerini herhangi bir bildirim vermeden yok sayar. `navigator` nesnesinde `getGamepads` işlevinin bulunup bulunmadığını kontrol ederek tarayıcının Gamepad API desteği sunup sunmadığını öğrenebilirsiniz:

```lua
local function supports_gamepads()
    return not html5 or (html5.run('typeof navigator.getGamepads === "function"') == "true")
end

if supports_gamepads() then
    print("Platform supports gamepads")
end
```

Oyununuz bir `iframe` içinde çalışıyorsa, `iframe` öğesine `gamepad` izninin de eklendiğinden emin olmanız gerekir:

```html
<iframe allow="gamepad"></iframe>
```

### Standart oyun kumandası

Bağlı bir oyun kumandası tarayıcı tarafından standart oyun kumandası olarak tanımlanırsa, [oyun kumandası ayar dosyasındaki](/manuals/input-gamepads/#gamepads-settings-file) `Standard Gamepad` eşlemesini kullanır (`/builtins` içindeki `default.gamepads` dosyasında bir `Standard Gamepad` eşlemesi bulunur). Standart oyun kumandası, PlayStation veya Xbox oyun kumandasına benzer bir düğme düzeninde 16 düğme ve 2 analog çubuğa sahip kumanda olarak tanımlanır (daha fazla bilgi için [W3C tanımına ve düğme düzenine](https://w3c.github.io/gamepad/#dfn-standard-gamepad) bakın). Bağlı oyun kumandası standart oyun kumandası olarak tanımlanmazsa Defold, oyun kumandası ayar dosyasında donanımsal oyun kumandası türüne uyan bir eşleme arar.

## Windows'ta oyun kumandaları
Windows'ta şu anda yalnızca XBox 360 oyun kumandaları desteklenir. 360 oyun kumandanızı Windows bilgisayarınıza bağlamak için [doğru yapılandırıldığından emin olun](http://www.wikihow.com/Use-Your-Xbox-360-Controller-for-Windows).

## Android'de oyun kumandaları

Oyun kumandaları Android derlemelerinde desteklenir ve diğer platformlarla aynı girdi olaylarını üretir. Oyun kumandası desteği, [tuş ve hareket olayları için Android girdi sistemine](https://developer.android.com/training/game-controllers/controller-input) dayanır. Android girdi olayları, yukarıda açıklanan aynı *gamepad* dosyası kullanılarak Defold oyun kumandası olaylarına dönüştürülür.

Android'de ek oyun kumandası eşlemeleri oluştururken Android girdi olaylarını *gamepad* dosyası değerlerine dönüştürmek için aşağıdaki başvuru tablolarını kullanabilirsiniz:

| Tuş olayından düğme indeksine   | İndeks |
|-----------------------------|-------|
| `AKEYCODE_BUTTON_A`           | 0     |
| `AKEYCODE_BUTTON_B`           | 1     |
| `AKEYCODE_BUTTON_C`           | 2     |
| `AKEYCODE_BUTTON_X`           | 3     |
| `AKEYCODE_BUTTON_L1`          | 4     |
| `AKEYCODE_BUTTON_R1`          | 5     |
| `AKEYCODE_BUTTON_Y`           | 6     |
| `AKEYCODE_BUTTON_Z`           | 7     |
| `AKEYCODE_BUTTON_L2`          | 8     |
| `AKEYCODE_BUTTON_R2`          | 9     |
| `AKEYCODE_DPAD_CENTER`        | 10    |
| `AKEYCODE_DPAD_DOWN`          | 11    |
| `AKEYCODE_DPAD_LEFT`          | 12    |
| `AKEYCODE_DPAD_RIGHT`         | 13    |
| `AKEYCODE_DPAD_UP`            | 14    |
| `AKEYCODE_BUTTON_START`       | 15    |
| `AKEYCODE_BUTTON_SELECT`      | 16    |
| `AKEYCODE_BUTTON_THUMBL`      | 17    |
| `AKEYCODE_BUTTON_THUMBR`      | 18    |
| `AKEYCODE_BUTTON_MODE`        | 19    |
| `AKEYCODE_BUTTON_1`           | 20    |
| `AKEYCODE_BUTTON_2`           | 21    |
| `AKEYCODE_BUTTON_3`           | 22    |
| `AKEYCODE_BUTTON_4`           | 23    |
| `AKEYCODE_BUTTON_5`           | 24    |
| `AKEYCODE_BUTTON_6`           | 25    |
| `AKEYCODE_BUTTON_7`           | 26    |
| `AKEYCODE_BUTTON_8`           | 27    |
| `AKEYCODE_BUTTON_9`           | 28    |
| `AKEYCODE_BUTTON_10`          | 29    |
| `AKEYCODE_BUTTON_11`          | 30    |
| `AKEYCODE_BUTTON_12`          | 31    |
| `AKEYCODE_BUTTON_13`          | 32    |
| `AKEYCODE_BUTTON_14`          | 33    |
| `AKEYCODE_BUTTON_15`          | 34    |
| `AKEYCODE_BUTTON_16`          | 35    |

([Android `KeyEvent` tanımları](https://developer.android.com/ndk/reference/group/input#group___input_1gafccd240f973cf154952fb917c9209719))

| Hareket olayından eksen indeksine  | İndeks |
|-----------------------------|-------|
| `AMOTION_EVENT_AXIS_X`        | 0     |
| `AMOTION_EVENT_AXIS_Y`        | 1     |
| `AMOTION_EVENT_AXIS_Z`        | 2     |
| `AMOTION_EVENT_AXIS_RZ`       | 3     |
| `AMOTION_EVENT_AXIS_LTRIGGER` | 4     |
| `AMOTION_EVENT_AXIS_RTRIGGER` | 5     |
| `AMOTION_EVENT_AXIS_HAT_X`    | 6     |
| `AMOTION_EVENT_AXIS_HAT_Y`    | 7     |

([Android `MotionEvent` tanımları](https://developer.android.com/ndk/reference/group/input#group___input_1ga157d5577a5b2f5986037d0d09c7dc77d))

Oyun kumandanızdaki her düğmenin hangi tuş olayına eşlendiğini belirlemek için bu başvuru tablosunu Google Play Store'dan edineceğiniz bir oyun kumandası test uygulamasıyla birlikte kullanın.
