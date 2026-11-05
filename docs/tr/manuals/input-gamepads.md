---
title: Defold'da oyun kumandası girdisi
brief: Bu kılavuz, oyun kumandası girdisinin nasıl çalıştığını açıklar.
---

::: sidenote
Defold'da girdinin genel olarak nasıl çalıştığını, girdinin nasıl alındığını ve betik dosyalarınızda hangi sırayla alındığını öğrenmeniz önerilir. Girdi sistemi hakkında daha fazla bilgi için [Girdiye genel bakış kılavuzuna](/manuals/input) bakın.
:::

# Oyun kumandaları {#gamepads}
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

## Dijital düğmeler {#digital-buttons}
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

## Analog çubuklar {#analog-sticks}
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

## Birden fazla oyun kumandası {#multiple-gamepads}
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

## Bağlanma ve bağlantının kesilmesi {#connect-and-disconnect}
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

## Ham oyun kumandası girdileri {#raw-gamepads}

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

Oyun kumandası eşlemeleri, bir kumandanın düğmelerini, eksenlerini ve yön anahtarlarını girdi eşlemelerinizin kullandığı standart denetimlere dönüştürür. Defold, *game.project* dosyasının *Input* bölümünde yapılandırılan iki eşleme kaynağını birleştirir:

| Ayar | Eşleme biçimi | Varsayılan |
| --- | --- | --- |
| [Gamepad Database](/manuals/project-settings/#gamepad-database) | Kumandanın GUID değeriyle eşleştirilen SDL biçimli metin veritabanı | `/builtins/input/gamecontrollerdb.txt` |
| [Gamepads](/manuals/project-settings/#gamepads) | Cihaz adları ve platformlar için eski `.gamepads` girdileri | `/builtins/input/default.gamepads` |

SDL veritabanı eşlemeleri ve otomatik platform eşlemeleri, [Gamepad Deadzone](/manuals/project-settings/#gamepad-deadzone) ayarını kullanır. Eski `.gamepads` girdileri kendi ölü bölgelerini tanımlar. Android'de, veritabanı girdisi olmayan bir kumanda [otomatik eşleme](#gamepads-on-android) de alabilir.

### Eski .gamepads eşlemeleri {#legacy-gamepads-mappings}

Bir `.gamepads` dosyası birden çok kumanda için eşlemeler içerebilir. Mevcut eski eşlemeler desteklenmeye devam eder. Defold, varsayılan dosyada yaygın kumandalar için eşlemeler içerir:

![Oyun kumandası ayarları](images/input/gamepads.png)

Bir masaüstü platformunda eski biçimli bir `.gamepads` eşlemesi oluşturmanız gerekiyorsa aşağıdaki araç yardımcı olabilir. Android için [Android'de oyun kumandaları](#gamepads-on-android) bölümüne bakın.

[gdc.zip dosyasını indirmek için tıklayın](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032).

Windows, Linux ve macOS için ikili dosyalar içerir. Komut satırından çalıştırın:

```sh
./gdc
```

Araç, bağlı oyun kumandanızdaki farklı düğmelere basmanızı ister. Ardından kumandanız için doğru eşlemeleri içeren yeni bir gamepads dosyası oluşturur. Yeni dosyayı kaydedin veya mevcut gamepads dosyanızla birleştirin, ardından *game.project* dosyasındaki ayarı güncelleyin:

![Oyun kumandası ayarları](images/input/gamepad_setting.png)

### Tanımlanamayan oyun kumandaları {#unidentified-gamepads}

Ne yapılandırılmış bir eşleme ne de otomatik platform eşlemesi kullanılabiliyorsa oyun kumandası yalnızca `Connected`, `Disconnected` ve `Raw` öğelerine bağlanan eylemleri üretir. Bir kumanda eşlemesi ekleyebilir veya ham girdisini oyununuzda işleyebilirsiniz.

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

### Standart oyun kumandası {#standard-gamepad}

Bağlı bir oyun kumandası tarayıcı tarafından standart oyun kumandası olarak tanımlanırsa, [oyun kumandası ayar dosyasındaki](/manuals/input-gamepads/#gamepads-settings-file) `Standard Gamepad` eşlemesini kullanır (`/builtins` içindeki `default.gamepads` dosyasında bir `Standard Gamepad` eşlemesi bulunur). Standart oyun kumandası, PlayStation veya Xbox oyun kumandasına benzer bir düğme düzeninde 16 düğme ve 2 analog çubuğa sahip kumanda olarak tanımlanır (daha fazla bilgi için [W3C tanımına ve düğme düzenine](https://w3c.github.io/gamepad/#dfn-standard-gamepad) bakın). Bağlı oyun kumandası standart oyun kumandası olarak tanımlanmazsa Defold, oyun kumandası ayar dosyasında donanımsal oyun kumandası türüne uyan bir eşleme arar.

## Windows'ta oyun kumandaları {#gamepads-on-windows}
Windows'ta şu anda yalnızca XBox 360 oyun kumandaları desteklenir. 360 oyun kumandanızı Windows bilgisayarınıza bağlamak için [doğru yapılandırıldığından emin olun](http://www.wikihow.com/Use-Your-Xbox-360-Controller-for-Windows).

## Android'de oyun kumandaları {#gamepads-on-android}

Oyun kumandaları Android derlemelerinde desteklenir ve diğer platformlarla aynı girdi eylemlerini üretir. Defold, yapılandırılmış [oyun kumandası eşlemelerini](#gamepads-settings-file) kullanır ve eşleşen girdisi olmayan bazı kumandaları otomatik olarak eşleyebilir.

Bir kumanda tanımlanamıyorsa veya denetimleri yanlışsa Android cihazında test edip eşlemesini ekleyin veya güncelleyin. Sorun giderme için [Tanımlanamayan oyun kumandaları](#unidentified-gamepads) ve [Ham oyun kumandası girdileri](#raw-gamepads) bölümlerine bakın.
