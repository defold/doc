---
title: Передавання повідомлень у Defold
brief: Передавання повідомлень — це механізм у Defold, який забезпечує спілкування між слабко пов’язаними об’єктами. У цьому посібнику ми докладно розглянемо цей механізм.
---

# Передавання повідомлень

Передавання повідомлень — це механізм у Defold, який дає ігровим об’єктам змогу спілкуватися один з одним. Цей посібник передбачає, що ви знайомі з [адресацією](/manuals/addressing) у Defold та [базовими будівельними блоками](/manuals/building-blocks).

У Defold не використовується об’єктно-орієнтований підхід у тому сенсі, що ваш застосунок складається з ієрархій класів з успадкуванням та функціями-членами в об’єктах (як, наприклад, у Java, C++ або C#). Натомість Defold доповнює Lua простим і потужним об’єктно-орієнтованим дизайном: стан об’єкта зберігається всередині компонентів-скриптів і доступний через посилання `self`. Крім того, об’єкти можна повністю відокремити один від одного, використовуючи асинхронне передавання повідомлень як засіб комунікації.


## Приклади використання

Спочатку розгляньмо декілька прикладів використання. Уявіть, що ви створюєте гру з такою структурою:

1. Головна стартова колекція містить ігровий об’єкт з компонентом GUI (GUI складається з мінімапи та лічильника рахунку), а також колекцію з ідентифікатором "level".
2. Колекція "level" містить два ігрові об’єкти: персонажа гравця та ворога.

![Структура передавання повідомлень](images/message_passing/message_passing_structure.png)

::: sidenote
Вміст цього прикладу міститься у двох окремих файлах: один призначений для головної стартової колекції, а другий — для колекції "level". Однак імена файлів _не мають значення_ у Defold. Значення мають призначені ідентифікатори.
:::

Гра складається з декількох простих механік, які потребують комунікації між об’єктами:

![Передавання повідомлень](images/message_passing/message_passing.png)

① Герой б’є ворога
: У межах цієї механіки повідомлення `"punch"` надсилається від скрипту, що належить "hero", до скрипту, що належить "enemy". Віддамо перевагу відносній адресації, тому що обидва об’єкти перебувають на одному рівні ієрархії колекції:

  ```lua
  -- Send "punch" from the "hero" script to "enemy" script
  msg.post("enemy#controller", "punch")
  ```

  Усі удари в грі мають однакову силу, тому повідомлення не міститиме жодної додаткової інформації, крім своєї назви — "punch".

  У скрипті, що належить ворогу (enemy), створимо функцію, щоб отримати повідомлення:

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("punch") then
      self.health = self.health - 100
    end
  end
  ```

  У цьому випадку код перевіряє лише назву повідомлення (надіслану як хешований рядок у параметрі `message_id`). Дані повідомлення та відправник не мають значення: *будь-хто* може надіслати повідомлення "punch" і завдати шкоди бідолашному ворогу.

② Отримання балів героєм
: Щоразу, коли гравець долає ворога, його рахунок збільшується. Повідомлення `"update_score"` також надсилається від скрипту "hero" до компонента "gui", що належить ігровому об’єкту "interface".

  ```lua
  -- Enemy defeated. Increase score counter by 100.
  self.score = self.score + 100
  msg.post("/interface#gui", "update_score", { score = self.score })
  ```

  Написати відносну адресу в цьому випадку неможливо, тому що "interface" перебуває в корені ієрархії іменування, а "hero" — ні. Повідомлення надсилається компоненту GUI, до якого прикріплено скрипт, тому він може належно відреагувати. Повідомлення можна вільно надсилати між скриптами, скриптами GUI та скриптами рендерингу.

  Повідомлення `"update_score"` містить дані про рахунок. Дані передаються як таблиця Lua в параметрі `message`:

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("update_score") then
      -- set the score counter to new score
      local score_node = gui.get_node("score")
      gui.set_text(score_node, "SCORE: " .. message.score)
    end
  end
  ```

③ Позиція ворога на мінімапі
: Гравець бачить мінімапу на екрані, щоб знаходити ворогів і стежити за ними. Кожен ворог передає свою позицію, надсилаючи повідомлення `"update_minimap"` компоненту "gui" в ігровому об’єкті "interface":

  ```lua
  -- Send the current position to update the interface minimap
  local pos = go.get_position()
  msg.post("/interface#gui", "update_minimap", { position = pos })
  ```

  Код скрипту GUI має стежити за позицією кожного ворога. Якщо той самий ворог надсилає нову позицію, стару позицію слід оновити. Відправника повідомлення (параметр `sender`) можна використовувати як ключ у таблиці Lua з позиціями:

  ```lua
  function init(self)
    self.minimap_positions = {}
  end

  local function update_minimap(self)
    for url, pos in pairs(self.minimap_positions) do
      -- update position on map
      ...
    end
  end

  function on_message(self, message_id, message, sender)
    if message_id == hash("update_score") then
      -- set the score counter to new score
      local score_node = gui.get_node("score")
      gui.set_text(score_node, "SCORE: " .. message.score)
    elseif message_id == hash("update_minimap") then
      -- update the minimap with new positions
      self.minimap_positions[sender] = message.position
      update_minimap(self)
    end
  end
  ```

## Надсилання повідомлень

Як ми вже побачили, механіка надсилання повідомлень дуже проста. Вам достатньо викликати функцію `msg.post()`, яка додає ваше повідомлення до черги. Потім кожного кадру рушій обробляє чергу та доставляє кожне повідомлення за вказаною адресою. Деякі системні повідомлення (наприклад, `"enable"`, `"disable"`, `"set_parent"` тощо) обробляються кодом рушія. Сам рушій також створює деякі системні повідомлення для ваших об’єктів (наприклад, `"collision_response"` під час фізичних колізій). Для обробки користувацьких повідомлень у компонентах-скриптах рушій викликає спеціальну функцію Defold Lua `on_message()`.

Ви можете надсилати будь-які повідомлення будь-якому наявному об’єкту або компоненту, а код отримувача вирішує, чи відповідати на них. Якщо ви надіслали повідомлення, а скрипт отримувача проігнорував його, це нормально. За обробку повідомлень повністю відповідає отримувач.

Рушій перевіряє адресу повідомлення. Якщо ви намагаєтеся надіслати повідомлення невідомому отримувачу, Defold повідомить про помилку в консолі:

```lua
-- Try to post to a non existing object
msg.post("dont_exist#script", "hello")
```

```txt
ERROR:GAMEOBJECT: Instance '/dont_exists' could not be found when dispatching message 'hello' sent from main:/my_object#script
```

Повна сигнатура функції `msg.post()` така:

`msg.post(receiver, message_id, [message])`

receiver
: Ідентифікатор цільового компонента або ігрового об’єкта. Зауважте, що повідомлення, надіслане ігровому об’єкту, буде передано всім компонентам цього об’єкта.

message_id
: Рядок або хеш рядка з назвою повідомлення.

[message]
: Необов’язковий параметр — таблиця Lua, що містить дані повідомлення у вигляді пар ключ-значення. До таблиці повідомлення можна включати майже будь-які дані: числа, рядки, булеві значення, URL-адреси, хеші та вкладені таблиці. Функції передавати не можна.

  ```lua
  -- Send table data containing a nested table
  local inventory_table = { sword = true, shield = true, bow = true, arrows = 9 }
  local stats = { score = 100, stars = 2, health = 4, inventory = inventory_table }
  msg.post("other_object#script", "set_stats", stats)
  ```

::: sidenote
Наразі розмір таблиці параметра `message` суворо обмежено 2 кілобайтами. Простого способу визначити точний розмір таблиці немає, але можна викликати `collectgarbage("count")` до та після додавання таблиці, щоб відстежити використання пам’яті.
:::

### Скорочення

Defold надає два корисних скорочення для надсилання повідомлень без повного URL:

:[Скорочення](../shared/url-shorthands.md)


## Отримання повідомлень

Щоб отримувати повідомлення, цільовий компонент-скрипт повинен містити функцію `on_message()`. Вона отримує чотири аргументи:

`function on_message(self, message_id, message, sender)`

`self`
: Посилання на сам скрипт.

`message_id`
: Містить _хешовану_ назву повідомлення.

`message`
: Містить дані повідомлення у вигляді таблиці Lua. Якщо даних немає, таблиця буде порожньою.

`sender`
: Містить повний URL відправника.

```lua
function on_message(self, message_id, message, sender)
    print(message_id) --> hash: [my_message_name]

    pprint(message) --> {
                    -->   score = 100,
                    -->   value = "some string"
                    --> }

    print(sender) --> url: [main:/my_object#script]
end
```

## Спілкування між двома ігровими світами

Якщо ви використовуєте компонент проксі колекції для завантаження нового світу в середовище виконання, вам може знадобитися надсилати повідомлення між світами. Наприклад, ви завантажили нову колекцію через проксі, а її властивість *Name* дорівнює "level":

![Ім’я колекції](images/message_passing/collection_name.png)

Щойно колекцію буде завантажено, ініціалізовано та активовано, ви зможете надсилати повідомлення будь-яким компонентам та об’єктам у новому світі. Для цього треба вказати ім’я ігрового світу в полі "socket" адреси отримувача:

```lua
-- Send a message to the player in the new game world
msg.post("level:/player#controller", "wake_up")
```

Докладніший опис роботи проксі наведено в [посібнику з проксі колекцій](/manuals/collection-proxy).

## Ланцюги повідомлень

Коли надіслане повідомлення дістається адресата, викликається функція отримувача `on_message()`. Код, що реагує на повідомлення, часто створює нові повідомлення, які додаються до черги.

Коли рушій починає обробляти чергу повідомлень (dispatching messages), він проходить нею й викликає `on_message()` отримувача кожного повідомлення. Це триває, доки черга не спорожніє. Якщо під час такого проходу до черги додано нові повідомлення, рушій проходить нею знову. Однак кількість спроб спорожнити чергу суворо обмежена. Це, своєю чергою, обмежує довжину ланцюгів повідомлень, які можна повністю обробити за поточний кадр. Наступний скрипт дає змогу перевірити, скільки проходів обробки черги рушій виконує між викликами `update()`:

```lua
function init(self)
    -- We’re starting a long message chain during object init
    -- and keeps it running through a number of update() steps.
    print("INIT")
    msg.post("#", "msg")
    self.updates = 0
    self.count = 0
end

function update(self, dt)
    if self.updates < 5 then
        self.updates = self.updates + 1
        print("UPDATE " .. self.updates)
        print(self.count .. " dispatch passes before this update.")
        self.count = 0
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("msg") then
        self.count = self.count + 1
        msg.post("#", "msg")
    end
end
```

Виконання цього скрипту виведе приблизно таке:

```txt
DEBUG:SCRIPT: INIT
INFO:ENGINE: Defold Engine 1.2.36 (5b5af21)
DEBUG:SCRIPT: UPDATE 1
DEBUG:SCRIPT: 10 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 2
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 3
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 4
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 5
DEBUG:SCRIPT: 75 dispatch passes before this update.
```

Бачимо, що ця версія рушія Defold виконує 10 проходів між викликом `init()` і першим викликом `update()`. Потім рушій виконує 75 проходів під час кожного оновлення.
