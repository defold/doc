---
title: Написання ігрової логіки у скриптах
brief: Цей посібник описує, як додавати ігрову логіку за допомогою компонентів-скриптів.
---

# Скрипти {#scripts}

Компоненти-скрипти (script components) дають змогу створювати ігрову логіку за допомогою [мови програмування Lua](/manuals/lua).


## Типи скриптів {#script-types}

У Defold є три типи скриптів Lua, для кожного з яких доступні різні бібліотеки Defold.

Скрипти ігрових об’єктів
: Розширення _.script_. Ці скрипти додаються до ігрових об’єктів (game objects) так само, як будь-який інший [компонент (component)](/manuals/components), а Defold виконує код Lua в межах функцій життєвого циклу рушія. Скрипти ігрових об’єктів зазвичай використовують для керування ігровими об’єктами та логікою, що об’єднує гру в єдине ціле: завантаженням рівнів, правилами гри тощо. Скрипти ігрових об’єктів мають доступ до функцій [GO](/ref/go) та всіх функцій бібліотек Defold, крім функцій [GUI](/ref/gui) і [Render](/ref/render).


Скрипти GUI
: Розширення _.gui_script_. Виконуються компонентами GUI й зазвичай містять логіку, потрібну для відображення елементів GUI, як-от ігрові інформаційні панелі, меню тощо. Defold виконує код Lua в межах функцій життєвого циклу рушія. Скрипти GUI мають доступ до функцій [GUI](/ref/gui) та всіх функцій бібліотек Defold, крім функцій [GO](/ref/go) і [Render](/ref/render).


Скрипти рендерингу
: Розширення _.render_script_. Виконуються конвеєром рендерингу й містять логіку, потрібну для рендерингу всієї графіки застосунку чи гри в кожному кадрі. Скрипт рендерингу посідає особливе місце в життєвому циклі вашої гри. Докладніше про це можна дізнатися в [документації про життєвий цикл застосунку](/manuals/application-lifecycle). Скрипти рендерингу мають доступ до функцій [Render](/ref/render) та всіх функцій бібліотек Defold, крім функцій [GO](/ref/go) і [GUI](/ref/gui).


## Виконання скриптів, зворотні виклики та self {#script-execution-callbacks-and-self}

Defold виконує скрипти Lua в межах життєвого циклу рушія та надає доступ до нього через набір заздалегідь визначених функцій зворотного виклику. Коли ви додаєте компонент-скрипт до ігрового об’єкта, скрипт стає частиною життєвого циклу ігрового об’єкта та його компонентів. Код скрипту виконується в контексті Lua під час завантаження, після чого рушій виконує наведені нижче функції та передає як параметр посилання на поточний екземпляр (instance) компонента-скрипту. За допомогою цього посилання `self` ви можете зберігати стан в екземплярі компонента.

::: important
`self` — це об’єкт типу `userdata`, який поводиться як таблиця Lua, але його не можна перебрати за допомогою `pairs()` чи `ipairs()` або вивести за допомогою `pprint()`.
:::

#### `init(self)`
Викликається під час ініціалізації компонента.

```lua
function init(self)
  -- These variables are available through the lifetime of the component instance
  self.my_var = "something"
  self.age = 0
end
```

#### `final(self)`
Викликається під час видалення компонента. Це корисно для очищення, наприклад, якщо ви створили ігрові об’єкти, які потрібно видалити разом із компонентом.

```lua
function final(self)
  if self.my_var == "something" then
      -- do some cleanup
  end
end
```

#### `fixed_update(self, dt)`
Оновлення, незалежне від частоти кадрів. Параметр `dt` містить проміжок часу від попереднього оновлення. Ця функція викликається `0-N` разів залежно від тривалості кадру та фіксованої частоти оновлення. Вона викликається лише тоді, коли в *game.project* увімкнено `Physics`-->`Use Fixed Timestep`, а значення `Engine`-->`Fixed Update Frequency` більше за 0. Це корисно, коли потрібно змінювати фізичні об’єкти через рівні проміжки часу, щоб досягти стабільної фізичної симуляції.

```lua
function fixed_update(self, dt)
  msg.post("#co", "apply_force", {force = vmath.vector3(1, 0, 0), position = go.get_world_position()})
end
```

#### `update(self, dt)`
Викликається один раз за кадр після зворотного виклику `fixed_update` усіх скриптів (якщо ввімкнено Fixed Timestep). Параметр `dt` містить проміжок часу від попереднього кадру.

```lua
function update(self, dt)
  self.age = self.age + dt -- increase age with the timestep
end
```

#### `late_update(self, dt)`
Викликається один раз за кадр після зворотного виклику `update` усіх скриптів, але безпосередньо перед рендерингом. Параметр `dt` містить проміжок часу від попереднього кадру.

```lua
function late_update(self, dt)
  go.set_position("/camera", self.final_camera_position)
end
```

#### on_message(self, message_id, message, sender)
Коли компоненту-скрипту надсилають повідомлення через [`msg.post()`](/ref/msg#msg.post), рушій викликає цю функцію компонента-отримувача. Дізнайтеся [більше про передавання повідомлень](/manuals/message-passing).

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("increase_score") then
        self.total_score = self.total_score + message.score
    end
end
```

#### `on_input(self, action_id, action)`
Якщо цей компонент отримав фокус введення (див. [`acquire_input_focus`](/ref/go/#acquire_input_focus)), рушій викликає цю функцію, коли реєструється введення. Дізнайтеся [більше про обробку введення](/manuals/input).

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        print("Touch", action.x, action.y)
    end
end
```

#### `on_reload(self)`
Ця функція викликається, коли скрипт перезавантажується за допомогою функції гарячого перезавантаження редактора (<kbd>Edit ▸ Reload Resource</kbd>). Це дуже корисно для налагодження, тестування й підлаштування. Дізнайтеся [більше про гаряче перезавантаження](/manuals/hot-reload).

```lua
function on_reload(self)
  print(self.age) -- print the age of this game object
end
```


## Реактивна логіка {#reactive-logic}

Ігровий об’єкт із компонентом-скриптом реалізує певну логіку. Часто ця логіка залежить від якогось зовнішнього чинника. ШІ ворога може реагувати на перебування гравця в певному радіусі від нього; двері можуть розблокуватися й відчинитися внаслідок взаємодії з гравцем тощо.

Функція `update()` дає змогу реалізувати складну поведінку у вигляді автомата станів, який виконується щокадру — іноді такий підхід цілком доречний. Проте кожен виклик `update()` потребує ресурсів. Якщо ця функція вам не потрібна, видаліть її та спробуйте натомість побудувати логіку _реактивно_. Пасивно чекати на повідомлення, яке спричинить реакцію, потребує менше ресурсів, ніж активно перевіряти ігровий світ у пошуках даних для реагування. Крім того, реактивний підхід до розв’язання задачі проєктування часто робить і структуру, і реалізацію зрозумілішими та стабільнішими.

Розгляньмо конкретний приклад. Припустімо, ви хочете, щоб компонент-скрипт надіслав повідомлення через 2 секунди після ініціалізації. Потім він має дочекатися певного повідомлення-відповіді й через 5 секунд після його отримання надіслати ще одне повідомлення. Нереактивний код для цього виглядав би приблизно так:

```lua
function init(self)
    -- Counter to keep track of time.
    self.counter = 0
    -- We need this to keep track of our state.
    self.state = "first"
end

function update(self, dt)
    self.counter = self.counter + dt
    if self.counter >= 2.0 and self.state == "first" then
        -- send message after 2 seconds
        msg.post("some_object", "some_message")
        self.state = "waiting"
    end
    if self.counter >= 5.0 and self.state == "second" then
        -- send message 5 seconds after we received "response"
        msg.post("another_object", "another_message")
        -- Nil the state so we don’t reach this state block again.
        self.state = nil
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("response") then
        -- “first” state done. enter next
        self.state = "second"
        -- zero the counter
        self.counter = 0
    end
end
```

Навіть у цьому доволі простому випадку логіка виходить досить заплутаною. Її можна поліпшити за допомогою співпрограм у модулі (див. нижче), але спробуймо натомість зробити її реактивною та використати вбудований механізм таймерів.

```lua
local function send_first()
	msg.post("some_object", "some_message")
end

function init(self)
	-- Wait 2s then call send_first()
	timer.delay(2, false, send_first)
end

local function send_second()
	msg.post("another_object", "another_message")
end

function on_message(self, message_id, message, sender)
	if message_id == hash("response") then
		-- Wait 5s then call send_second()
		timer.delay(5, false, send_second)
	end
end
```

Такий код зрозуміліший, і за ним легше стежити. Ми позбуваємося внутрішніх змінних стану, за якими часто складно стежити в логіці та які можуть призводити до непомітних помилок. Також ми повністю прибираємо функцію `update()`. Це звільняє рушій від необхідності викликати наш скрипт 60 разів на секунду, навіть коли той просто очікує.


## Попередня обробка {#preprocessing}

За допомогою препроцесора Lua та спеціальної розмітки можна умовно включати код залежно від варіанта збірки. Приклад:

```lua
-- Use one of the following keywords: RELEASE, DEBUG or HEADLESS
--#IF DEBUG
local lives_num = 999
--#ELSE 
local lives_num = 3
--#ENDIF
```

Препроцесор доступний як розширення збирання. Дізнайтеся більше про його встановлення та використання на [сторінці розширення на GitHub](https://github.com/defold/extension-lua-preprocessor).


## Підтримка в редакторі {#editor-support}

Редактор Defold підтримує редагування скриптів Lua з підсвічуванням синтаксису й автодоповненням. Щоб доповнити назву функції Defold, натисніть *Ctrl+Space*: з’явиться список функцій, що відповідають уже введеному тексту.

![Автодоповнення](images/script/completion.png)
