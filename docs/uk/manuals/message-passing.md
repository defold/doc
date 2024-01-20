---
title: Передавання повідомлень в Defold
brief: Передавання повідомлень - це маханізм в Defold, який дозволяє спілкування між слабко повʼязаними обʼєктами. В цьому посібнику ми розглянемо цей механізм більш детально.
---

# Передавання повідомлень

Передавання повідомлень - це механізм в Defold, який дозволяє ігровим обʼєктам спілкуватися одне з одним. В цьому посібнику передбачається що ви знайомі з [адресацією](/manuals/addressing) в Defold та [базовими будівельними блоками](/manuals/building-blocks).

У Defold не використовується обʼєктно-орієнтований підхід у тому сенсі, що ваш додаток складається з ієрархій класів із успадкуванням та функціями-членами в ваших обʼєктах (як, наприклад, в Java, C++ або C#). Натомість Defold додає простий та потужний обʼєктно-орієнтований дизайн до Lua: стан обʼєкта зберігається внутрішньо в скриптах, доступний через посилання `self`. Крім того, обʼєкти можна відокремити одне від одного за допомогою відправлення асинхронних повідомлень в якості засоба комунікації між собою.


## Приклади використання

Перш за все, давайте подивимося на декілька прикладів використання. Уявіть, що ви будуєте гру, яка складається з:

1. Головної стартової колекції, що містить ігровий обʼєкт з GUI компонентом (GUI складається з мінімапи та лічильника рахунку). А також колекції з ідентифікатором "level".
2. Колекція "level" містить два ігрових обʼєкта: один персонаж героя гравця та один ворог.

![Структура відправлення повідомлень](images/message_passing/message_passing_structure.png)

::: sidenote
Зміст цього прикладу знаходиться в двох окремих файлах. Один файл для головної стартової колекції, а другий - для колекції "level". Однак, імена файлів _не мають значення_ в Defold. Значення мають задані ідентифікатори.
:::

Гра складається з декількох простих механік, які потребують комунікацію між обʼєктами:

![Відправлення повідомлень](images/message_passing/message_passing.png)

① Герой бʼє ворога
: В межах цієї механіки, повідомлення `"punch"` відправляється від скрипта, що належить "hero", до скрипта, що належить "enemy". Віддамо перевагу відносній адресації, тому що обидва обʼєкти знаходяться в одному місці в ієрархії колекції:

  ```lua
  -- Send "punch" from the "hero" script to "enemy" script
  msg.post("enemy#controller", "punch")
  ```

  Всі удари в грі однієї сили, тому повідомлення не буде містити ніякої додаткової інформації окрім свого імені - "punch".

  В скрипті, що належить ворогу (enemy), створимо функцію, щоб отримати повідомлення:

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("punch") then
      self.health = self.health - 100
    end
  end
  ```

  В цьому випадку код дивиться лише на імʼя повідомлення (відправлене як хешований рядок в параметрі `message_id`). Код не піклується про дані повідомлення або відправника --- *будь-хто* може відправити повідомлення "punch" і нанести шкоду бідолашному ворогу.

② Отримання балів героєм
: Кожен раз, коли гравець долає ворога, рахунок гравця збільшується. Повідомлення `"update_score"` також відправляється від скрипта "hero" до компонента "gui", що належить ігровому обʼєкту "interface".

  ```lua
  -- Enemy defeated. Increase score counter by 100.
  self.score = self.score + 100
  msg.post("/interface#gui", "update_score", { score = self.score })
  ```

  Написати відносну адресу в цьому випадку неможливо, тому що "interface" знаходиться в корні ієрархії іменування, а "hero" - ні. Повідомлення відправляється GUI компоненту, до якого прикріплено скрипт, тому він може відреагувати на повідомлення відповідним чином. Повідомлення можна вільно відправляти між сриптами, GUI скриптами та рендер скриптами.

  Повідомлення `"update_score"` містить дані про рахунок. Дані передаються як Lua таблиця в параметрі `message`:

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
: Гравець бачить мінімапу на екрані щоб знаходити та стежити за ворогами. Кожен ворог відповідає за трансляцію своєї позиції шляхом відправлення повідомлення `"update_minimap"` компоненту "gui" в ігровому обʼєкті "interface":

  ```lua
  -- Send the current position to update the interface minimap
  local pos = go.get_position()
  msg.post("/interface#gui", "update_minimap", { position = pos })
  ```

  Код GUI скрипту має стежити за позицією кожного ворога та, якщо один і той же ворог відправляє нову позицію, стара позиція має оновитись. Відправник повідомлення (параметр `sender`) може використовуватися як ключ для Lua таблиці з позиціями:

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

## Відправлення повідомлень

Як ми вже побачили, механіка відправлення повідомлень дуже проста. Вам достатньо викликати функцію `msg.post()`, яка відправляє ваше повідомлення в чергу повідомлень. Потім, кожен кадр, рушій обробляє чергу та доставляє кожне повідомлення по зазначеній адресі. Деякі системні повідомлення (наприклад, `"enable"`, `"disable"`, `"set_parent"` та ін.) обробляються кодом рушія. Сам рушій також створює деякі системні повідомлення для ваших обʼєктів (наприклад, `"collision_response"` під час фізичних колізій). Для обробки користувацьких повідомлень в компонентах-скриптах, рушій просто викликає спеціальну Defold Lua функцію `on_message()`.

Ви можете відправляти будь-які повідомлення будь-якому існуючому обʼєкту або компоненту, і код отримувача вирішує чи відповідати на це повідомлення. Якщо ви відправили повідомленя, а скрипт отримувача проігнорував його, це нормально. Відповідальність за обробку повідомлень повністю лежить на стороні отримувача.

Рушій перевірить адресу повідомлення. Якщо ви намагаєтесь відправити повідомлення невідомому отримувачу, Defold повідомить помилкою в консолі:

```lua
-- Try to post to a non existing object
msg.post("dont_exist#script", "hello")
```

```txt
ERROR:GAMEOBJECT: Instance '/dont_exists' could not be found when dispatching message 'hello' sent from main:/my_object#script
```

Повна сігнатура функції `msg.post()` така:

`msg.post(receiver, message_id, [message])`

receiver
: Ідетифікатор цільового компонента або ігровго обʼєкта. Відмітьте, що повідомлення, відправлене ігровому обʼєкту, буде трансльоване всім компонентам цього обʼєкта.

message_id
: Рядок, або хеш рядка, з імʼям повідомлення.

[message]
: Необовʼязковий параметр, Lua таблиця, що містить дані повідомлення у вигляді пар ключ-значення. Майже будь-які дані можна включати в таблицю повідомлення. Ви можете передавати числа, рядки, булеві значення, URL-и, хеші і вкладені таблиці. Ви не можете передавати функції.

  ```lua
  -- Send table data containing a nested table
  local inventory_table = { sword = true, shield = true, bow = true, arrows = 9 }
  local stats = { score = 100, stars = 2, health = 4, inventory = inventory_table }
  msg.post("other_object#script", "set_stats", stats)
  ```

::: sidenote
Наразі параметр `message` суворо обмежений розміром у 2 кілобайти. Тривіального методу вимірювання розміру таблиці не існує, але ви можете скористатися `collectgarbage("count")` до та після додавання таблиці щоб відстежувати вживання памʼяті.
:::

### Скорочення

Defold використовує два корисних скорочення, які можна використовувати для відправлення повідомлень без повного URL:

:[Shorthands](../shared/url-shorthands.md)


## Отримання повідомлень

Отримання повідомлень полягає в забезпеченні цільового скрипта функцією `on_message()`. Вона отримує чотири аргументи:

`function on_message(self, message_id, message, sender)`

`self`
: Посилання на сам скрипт.

`message_id`
: Містить _хешовану_ назву повідомлення.

`message`
: Містить дані повідомлення у вигляді Lua таблиці. Якщо даних немає, то таблиця буде пустою.

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

Якщо ви використовуєте компонент проксі колекції для завантаження нового нового світу в середовище виконання, вам може знадобитися відправляти повідомлення між світами. Наприклад, ви завантажили нову колекцію через проксі, а її властивість *Name* дорівнює "level":

![Імʼя колекції](images/message_passing/collection_name.png)

Як тільки колекцію було завантажено, ініціалізовано та активовано, ви можете відправляти повідомлення будь-яким компонентам та обʼєктам в новому світі. Для цього треба вказати імʼя ігрового світу в полі "socket" адреси отримувача:

```lua
-- Send a message to the player in the new game world
msg.post("level:/player#controller", "wake_up")
```

Більш детальний опис того, як працюють проксі, можна подвитись в документації [проксі колекцій](/manuals/collection-proxy).

## Ланцюги повідомлень

Коли відправлене повідомлення дістається своєї мети, буде викликана функція отримувача `on_message()`. Часто буває так, що реагуючий код також створює нові повідомлення, які додаються до черги повідомлень.

Коли рушій починає відправляти (dispatching) повідомлення, він проходиться по черзі повідомлень і викликає `on_message()` отримувача кожного повідомлення. Це продовжується поки черга повідомлень не спорожніє. Якщо після цього до черги були додані нові повідомлення, то рушій знов пройдеться по черзі. Але кількість спроб спутошити чергу повідомлень суворо обмежена. Що в свою чергу обмежує довжину ланцюгів повідомлень, які ми очікуємо встигнути повіністю обробити за поточний кадр. Наступний скрипт дозволяє протестувати скільки циклів відправки рушій виконує між кожним викликом `update()`:

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

Виконання цього скрипту видасть щось таке:

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

Можемо побачити що ця версія рушія Defold виконує 10 проходів між викликом `init()` і першим викликом `update()`. Потім рушій виконує 75 проходів під час кожного оновлення.
