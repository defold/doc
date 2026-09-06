---
title: Введення з геймпада в Defold
brief: Цей посібник пояснює, як працює введення з геймпада.
---

::: sidenote
Рекомендуємо ознайомитися із загальними принципами роботи введення в Defold, способами його отримання та порядком, у якому його отримують ваші файли скриптів. Докладніше про систему введення читайте в [оглядовому посібнику з введення](/manuals/input).
:::

# Геймпади {#gamepads}
Тригери геймпада дають змогу прив’язати стандартне введення з геймпада до функцій гри. Для введення з геймпада доступні прив’язки до таких елементів:

- Лівий і правий стіки (напрямок і натискання)
- Ліва та права групи цифрових кнопок. Права група зазвичай відповідає кнопкам «A», «B», «X» і «Y» на контролері Xbox та кнопкам «квадрат», «коло», «трикутник» і «хрестик» на контролері Playstation.
- Лівий і правий курки
- Ліва та права плечові кнопки
- Кнопки Start, Back і Guide

![](images/input/gamepad_bindings.png)

::: important
У наведених нижче прикладах використовуються дії, показані на зображенні вище. Як і для будь-якого іншого введення, ви можете довільно називати свої дії введення.
:::

## Цифрові кнопки {#digital-buttons}
Цифрові кнопки генерують події `pressed`, `released` і `repeated`. Приклад виявлення введення з цифрової кнопки (натискання або відпускання):

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

## Аналогові стіки {#analog-sticks}
Аналогові стіки безперервно генерують події введення, коли стік відхилено за межі мертвої зони, визначеної у файлі налаштувань геймпадів (див. нижче). Приклад виявлення введення з аналогового стіка:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") then
        -- left stick was moved down
        print(action.value) -- a value between 0.0 an -1.0
    end
end
```

Аналогові стіки також генерують події `pressed` і `released`, коли відхилення в основних напрямках перетинає певне порогове значення. Завдяки цьому аналоговий стік також легко використовувати для цифрового введення напрямку:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") and action.pressed then
        -- left stick was moved to its extreme down position
    end
end
```

## Кілька геймпадів {#multiple-gamepads}
Defold підтримує кілька геймпадів через операційну систему пристрою. У полі `gamepad` таблиці `action` для дії вказується номер геймпада, з якого надійшло введення:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_start") then
        if action.gamepad == 0 then
          -- gamepad 0 wants to join the game
        end
    end
end
```

## Підключення й відключення {#connect-and-disconnect}
Прив’язки введення з геймпада також містять дві окремі прив’язки з назвами `Connected` і `Disconnected`, які дають змогу виявляти підключення геймпада (навіть якщо він був підключений від початку) або його відключення.

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

## Необроблені дані геймпадів {#raw-gamepads}

Прив’язки введення з геймпада також містять окрему прив’язку з назвою `Raw`, яка надає нефільтроване (без застосування мертвої зони) введення з кнопок, осей і перемикачів напрямку (hat) будь-якого підключеного геймпада.

```lua
function on_input(self, action_id, action)
    if action_id == hash("raw") then
        pprint(action.gamepad_buttons)
        pprint(action.gamepad_axis)
        pprint(action.gamepad_hats)
    end
end
```

## Файл налаштувань геймпадів {#gamepads-settings-file}
Для налаштування введення з геймпада використовується окремий файл відповідностей для кожного типу фізичного геймпада. Відповідності для конкретних фізичних геймпадів задаються у файлі *gamepads*. Defold постачається із вбудованим файлом gamepads, що містить налаштування для поширених геймпадів:

![Налаштування геймпадів](images/input/gamepads.png)

Якщо вам потрібно створити новий файл налаштувань геймпадів, у нас є простий інструмент, який у цьому допоможе:

[Натисніть, щоб завантажити gdc.zip](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032).

Він містить виконувані файли для Windows, Linux і macOS. Запустіть його з командного рядка:

```sh
./gdc
```

Інструмент попросить вас натискати різні кнопки на підключеному контролері. Після цього він створить новий файл gamepads із правильними відповідностями для вашого контролера. Збережіть новий файл або об’єднайте його з наявним файлом gamepads, а потім оновіть налаштування в *game.project*:

![Налаштування геймпадів](images/input/gamepad_setting.png)

### Нерозпізнані геймпади {#unidentified-gamepads}

Якщо підключений геймпад не має визначених відповідностей, він генеруватиме лише дії `connected`, `disconnected` і `raw`. У такому разі вам потрібно вручну зіставити необроблені дані геймпада з діями у вашій грі.

Щоб перевірити, чи надійшла дія введення з невідомого геймпада, прочитайте значення `gamepad_unknown` у таблиці `action`:

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

## Геймпади в HTML5 {#gamepads-in-html5}
Геймпади підтримуються у збірках HTML5 і генерують ті самі події введення, що й на інших платформах. Підтримка геймпадів ґрунтується на [Gamepad API](https://www.w3.org/TR/gamepad/), який підтримується більшістю браузерів ([див. цю таблицю підтримки](https://caniuse.com/?search=gamepad)). Якщо браузер не підтримує Gamepad API, Defold без жодних повідомлень ігноруватиме всі тригери геймпадів у вашому проєкті. Щоб перевірити, чи підтримує браузер Gamepad API, перевірте наявність функції `getGamepads` в об’єкті `navigator`:

```lua
local function supports_gamepads()
    return not html5 or (html5.run('typeof navigator.getGamepads === "function"') == "true")
end

if supports_gamepads() then
    print("Platform supports gamepads")
end
```

Якщо ваша гра працює всередині `iframe`, також переконайтеся, що для цього `iframe` додано дозвіл `gamepad`:

```html
<iframe allow="gamepad"></iframe>
```

### Стандартний геймпад {#standard-gamepad}

Якщо браузер розпізнає підключений геймпад як стандартний, для нього використовуватимуться відповідності `Standard Gamepad` із [файлу налаштувань геймпадів](/manuals/input-gamepads/#gamepads-settings-file) (відповідності `Standard Gamepad` включено до файлу `default.gamepads` у `/builtins`). Стандартний геймпад визначається як пристрій із 16 кнопками та 2 аналоговими стіками, розташування кнопок якого подібне до контролера PlayStation або Xbox (докладніше див. [визначення та розташування кнопок у W3C](https://w3c.github.io/gamepad/#dfn-standard-gamepad)). Якщо підключений геймпад не розпізнано як стандартний, Defold шукатиме у файлі налаштувань геймпадів відповідності для типу цього фізичного геймпада.

## Геймпади у Windows {#gamepads-on-windows}
У Windows наразі підтримуються лише контролери XBox 360. Щоб підключити контролер 360 до комп’ютера з Windows, [переконайтеся, що його правильно налаштовано](http://www.wikihow.com/Use-Your-Xbox-360-Controller-for-Windows).

## Геймпади в Android {#gamepads-on-android}

Геймпади підтримуються у збірках Android і генерують ті самі події введення, що й на інших платформах. Підтримка геймпадів ґрунтується на [системі введення Android для подій клавіш і руху](https://developer.android.com/training/game-controllers/controller-input). Події введення Android перетворюються на події геймпадів Defold за допомогою того самого файлу *gamepad*, що описаний вище.

Додаючи додаткові прив’язки геймпадів в Android, ви можете використовувати наведені нижче таблиці відповідностей, щоб перетворювати події введення Android на значення файлу *gamepad*:

| Відповідність події клавіші індексу кнопки | Індекс |
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

([Визначення `KeyEvent` в Android](https://developer.android.com/ndk/reference/group/input#group___input_1gafccd240f973cf154952fb917c9209719))

| Відповідність події руху індексу осі | Індекс |
|-----------------------------|-------|
| `AMOTION_EVENT_AXIS_X`        | 0     |
| `AMOTION_EVENT_AXIS_Y`        | 1     |
| `AMOTION_EVENT_AXIS_Z`        | 2     |
| `AMOTION_EVENT_AXIS_RZ`       | 3     |
| `AMOTION_EVENT_AXIS_LTRIGGER` | 4     |
| `AMOTION_EVENT_AXIS_RTRIGGER` | 5     |
| `AMOTION_EVENT_AXIS_HAT_X`    | 6     |
| `AMOTION_EVENT_AXIS_HAT_Y`    | 7     |

([Визначення `MotionEvent` в Android](https://developer.android.com/ndk/reference/group/input#group___input_1ga157d5577a5b2f5986037d0d09c7dc77d))

Використовуйте цю таблицю відповідностей разом із застосунком для тестування геймпадів із Google Play Store, щоб визначити, якій події клавіші відповідає кожна кнопка вашого геймпада.
