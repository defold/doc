---
title: Модулі Lua у Defold
brief: Модулі Lua дають змогу структурувати проєкт і створювати бібліотечний код для повторного використання. Цей посібник пояснює, як це робити в Defold.
---

# Модулі Lua {#lua-modules}

Модулі Lua дають змогу структурувати проєкт і створювати бібліотечний код для повторного використання. Загалом варто уникати дублювання коду у своїх проєктах. Defold дає змогу використовувати механізм модулів Lua для підключення файлів скриптів до інших файлів скриптів. Завдяки цьому можна інкапсулювати функціональність (і дані) в окремому файлі скрипту для повторного використання у скриптах ігрових об’єктів (game objects) і скриптах GUI.

## Підключення файлів Lua {#requiring-lua-files}

Код Lua, збережений у файлах із розширенням `.lua` будь-де у структурі ігрового проєкту, можна завантажувати за допомогою `require` у файли скриптів і скриптів GUI. Щоб створити новий файл модуля Lua, клацніть правою кнопкою миші папку, у якій хочете його створити, на панелі *Assets*, а потім виберіть <kbd>New... ▸ Lua Module</kbd>. Надайте файлу унікальне ім’я та натисніть <kbd>Ok</kbd>:

![новий файл](images/modules/new_name.png)

Припустімо, до файлу `main/anim.lua` додано такий код:

```lua
function direction_animation(direction, char)
    local d = ""
    if direction.x > 0 then
        d = "right"
    elseif direction.x < 0 then
        d = "left"
    elseif direction.y > 0 then
        d = "up"
    elseif direction.y < 0 then
        d = "down"
    end
    return hash(char .. "-" .. d)
end
```

Тоді будь-який скрипт може завантажити цей файл за допомогою `require` і використовувати функцію:

```lua
require "main.anim"

function update(self, dt)
    -- update position, set direction etc
    ...

    -- set animation
    local anim = direction_animation(self.dir, "player")
    if anim ~= self.current_anim then
        sprite.play_flipbook("#sprite", anim)
        self.current_anim = anim
    end
end
```

Функція `require` завантажує вказаний модуль. Спочатку вона перевіряє таблицю `package.loaded`, щоб визначити, чи модуль уже завантажено. Якщо так, `require` повертає значення, збережене в `package.loaded[module_name]`. Інакше вона завантажує та виконує файл за допомогою завантажувача.

Синтаксис рядка з іменем файлу, переданого до `require`, має особливість. Lua замінює символи `.` у рядку з іменем файлу на роздільники шляху: `/` у macOS і Linux та `\\` у Windows.

Зауважте, що зазвичай не варто зберігати стан і визначати функції в глобальній області видимості, як ми зробили вище. Це створює ризик колізій імен, відкриває доступ до стану модуля або спричиняє залежності між частинами коду, що використовують модуль.

## Модулі {#modules}

Для інкапсуляції даних і функцій Lua використовує _модулі_. Модуль Lua — це звичайна таблиця Lua, що містить функції та дані. Таблицю оголошують локальною, щоб не засмічувати глобальну область видимості:

```lua
local M = {}

-- private
local message = "Hello world!"

function M.hello()
    print(message)
end

return M
```

Після цього модуль можна використовувати. Знову ж таки, бажано присвоїти його локальній змінній:

```lua
local m = require "mymodule"
m.hello() --> "Hello world!"
```

## Гаряче перезавантаження модулів {#hot-reloading-modules}

Розгляньмо простий модуль:

```lua
-- module.lua
local M = {} -- creates a new table in the local scope
M.value = 4711
return M
```

І код, що використовує цей модуль: 

```lua
local m = require "module"
print(m.value) --> "4711" (even if "module.lua" is changed and hot reloaded)
```

Якщо виконати гаряче перезавантаження файлу модуля, код виконається знову, але `m.value` не зміниться. Чому так відбувається?

По-перше, таблиця у `module.lua` створюється в локальній області видимості, а код, що використовує модуль, отримує _посилання_ на цю таблицю. Перезавантаження `module.lua` повторно виконує код модуля, але при цьому створюється нова таблиця в локальній області видимості, замість того щоб оновити таблицю, на яку посилається `m`.

По-друге, Lua кешує файли, завантажені за допомогою `require`. Коли файл підключається вперше, його додають до таблиці [`package.loaded`](/ref/package/#package.loaded), щоб наступні виклики `require` могли прочитати його швидше. Можна примусово перечитати файл із диска, встановивши для його запису значення `nil`: `package.loaded["my_module"] = nil`.

Для правильного гарячого перезавантаження модуля потрібно перезавантажити модуль, скинути кеш, а потім перезавантажити всі файли, що використовують цей модуль. Це далеко не оптимально.

Натомість можна розглянути обхідний спосіб для використання _під час розробки_: розмістіть таблицю модуля в глобальній області видимості та зробіть так, щоб `M` посилалася на глобальну таблицю, замість створення нової таблиці під час кожного виконання файлу. Тоді перезавантаження модуля змінюватиме вміст глобальної таблиці:

```lua
--- module.lua

-- Replace with local M = {} when done
uniquevariable12345 = uniquevariable12345 or {}
local M = uniquevariable12345

M.value = 4711
return M
```

## Модулі та стан {#modules-and-state}

Модулі зі станом зберігають внутрішній стан, спільний для всіх частин коду, що використовують модуль, і їх можна порівняти із синглтонами:

```lua
local M = {}

-- all users of the module will share this table
local state = {}

function M.do_something(foobar)
    table.insert(state, foobar)
end

return M
```

Модуль без стану, навпаки, не зберігає внутрішнього стану. Натомість він надає механізм винесення стану в окрему таблицю, локальну для коду, що використовує модуль. Ось кілька різних способів це реалізувати:

Використання таблиці стану
: Мабуть, найпростіший підхід — використати функцію-конструктор, яка повертає нову таблицю, що містить лише стан. Стан явно передається до модуля як перший параметр кожної функції, що працює з таблицею стану.

  ```lua
  local M = {}
  
  function M.alter_state(the_state, v)
      the_state.value = the_state.value + v
  end
  
  function M.get_state(the_state)
      return the_state.value
  end
  
  function M.new(v)
      local state = {
          value = v
      }
      return state
  end
  
  return M
  ```
  
  Використовуйте модуль так:
  
  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  m.alter_state(my_state, 1)
  print(m.get_state(my_state)) --> 43
  ```

Використання метатаблиць
: Інший підхід — використати функцію-конструктор, яка під час кожного виклику повертає нову таблицю зі станом і публічними функціями модуля:

  ```lua
  local M = {}
  
  function M:alter_state(v)
      -- self is added as first argument when using : notation
      self.value = self.value + v
  end
  
  function M:get_state()
      return self.value
  end
  
  function M.new(v)
      local state = {
          value = v
      }
      return setmetatable(state, { __index = M })
  end
  
  return M
  ```

  Використовуйте модуль так:

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state:alter_state(1) -- "my_state" is added as first argument when using : notation
  print(my_state:get_state()) --> 43
  ```

Використання замикань
:  Третій спосіб — повернути замикання, що містить увесь стан і функції. Тут не потрібно передавати екземпляр як аргумент (явно чи неявно за допомогою оператора двокрапки), як у випадку з метатаблицями. Цей спосіб також дещо швидший за використання метатаблиць, оскільки виклики функцій не мають проходити через метаметоди `__index`, але кожне замикання містить власну копію методів, тож споживання пам’яті вище.

  ```lua
  local M = {}
  
  function M.new(v)
      local state = {
          value = v
      }
  
      state.alter_state = function(v)
          state.value = state.value + v
      end
  
      state.get_state = function()
          return state.value
      end
  
      return state
  end
  
  return M
  ```

  Використовуйте модуль так:

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state.alter_state(1)
  print(my_state.get_state()) 
  ```
