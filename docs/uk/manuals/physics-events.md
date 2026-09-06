---
title: Події колізій у Defold
brief: Обробку подій колізій можна централізувати за допомогою `physics.set_event_listener()`, спрямувавши всі повідомлення про колізії та взаємодії до однієї вказаної функції.
---

# Обробка подій фізики в Defold {#defold-physics-event-handling}

Defold надає централізовану обробку подій фізики за допомогою функції `physics.set_event_listener()`. Ця функція дає змогу встановити власний слухач для обробки всіх подій фізичної взаємодії в одному місці, що спрощує код і підвищує ефективність.

## Встановлення слухача фізичного світу {#setting-the-physics-world-listener}

У Defold кожен проксі колекції (collection proxy) створює власний окремий фізичний світ. Тому, коли ви працюєте з кількома проксі колекцій, необхідно керувати окремими фізичними світами, пов’язаними з кожним із них. Щоб події фізики оброблялися правильно в кожному світі, потрібно встановити окремий слухач фізичного світу для світу кожного проксі колекції.

Це означає, що слухач подій фізики потрібно встановлювати в контексті колекції (collection), яку представляє проксі. Так ви пов’язуєте слухач безпосередньо з відповідним фізичним світом, що дає йому змогу правильно обробляти події фізики.

Ось приклад встановлення слухача фізичного світу в межах проксі колекції:

```lua
function init(self)
    -- Assuming this script is attached to a game object within the collection loaded by the proxy
    -- Set the physics world listener for the physics world of this collection proxy
    physics.set_event_listener(physics_world_listener)
end
```

За допомогою цього підходу ви забезпечуєте окремий слухач для кожного фізичного світу, створеного проксі колекції. Це необхідно для ефективної обробки подій фізики в проєктах, які використовують кілька проксі колекцій.

::: important
Якщо слухач встановлено, [повідомлення фізики](/manuals/physics-messages) більше не надсилатимуться для фізичного світу, у якому його встановлено.
:::

## Структура даних подій {#event-data-structure}

Слухач викликається з `self` і таблицею `events`. Таблиця `events` — це масив, що містить усі події фізики, зібрані для цього зворотного виклику. Кожен елемент — це таблиця події з полем `type`, що містить хешовану назву події, та додатковими полями, притаманними цьому типу події.

Таблиці подій містять такі дані:

1. **Подія точки контакту (`contact_point_event`):**
Ця подія повідомляє про точку контакту між двома об’єктами колізій. Вона корисна для детальної обробки колізій, наприклад для обчислення сили удару або власних реакцій на колізії.

   - `applied_impulse`: Імпульс, що виник унаслідок контакту.
   - `distance`: Глибина проникнення об’єктів один в одного.
   - `a` і `b`: Об’єкти, що представляють учасників колізії; кожен із них містить:
     - `position`: Позиція точки контакту у світовому просторі (vector3).
     - `instance_position`: Позиція екземпляра (instance) ігрового об’єкта (game object) у світовому просторі (vector3).
     - `id`: Ідентифікатор екземпляра (hash).
     - `group`: Група колізій (hash).
     - `relative_velocity`: Швидкість відносно іншого об’єкта (vector3).
     - `mass`: Маса в кілограмах (number).
     - `normal`: Нормаль контакту, спрямована від іншого об’єкта (vector3).

2. **Подія колізії (`collision_event`):**
Ця подія вказує, що між двома об’єктами сталася колізія. Вона загальніша за подію точки контакту й добре підходить для виявлення колізій, коли докладна інформація про точки контакту не потрібна.

   - `a` і `b`: Об’єкти, що представляють учасників колізії; кожен із них містить:
     - `position`: Позиція у світовому просторі (vector3).
     - `id`: Ідентифікатор екземпляра (hash).
     - `group`: Група колізій (hash).

3. **Подія тригера (`trigger_event`):**
Ця подія надсилається, коли об’єкт взаємодіє з об’єктом-тригером. Вона корисна для створення областей у грі, які спричиняють певні дії, коли об’єкт входить до них або виходить із них.

   - `enter`: Вказує, чи була взаємодія входом (true) або виходом (false).
   - `a` і `b`: Об’єкти, що беруть участь у події тригера; кожен із них містить:
     - `id`: Ідентифікатор екземпляра (hash).
     - `group`: Група колізій (hash).

4. **Відповідь на трасування променя (`ray_cast_response`):**
Ця подія надсилається у відповідь на трасування променя та надає інформацію про об’єкт, у який влучив промінь.

   - `group`: Група колізій об’єкта, у який влучив промінь (hash).
   - `request_id`: Ідентифікатор запиту на трасування променя (number).
   - `position`: Позиція влучання (vector3).
   - `fraction`: Частка довжини променя до точки влучання (number).
   - `normal`: Нормаль у позиції влучання (vector3).
   - `id`: Ідентифікатор екземпляра об’єкта, у який влучив промінь (hash).

5. **Промах під час трасування променя (`ray_cast_missed`):**
Ця подія надсилається, коли під час трасування промінь не влучає в жоден об’єкт.

   - `request_id`: Ідентифікатор запиту на трасування променя, який не влучив у жоден об’єкт (number).

## Приклад використання {#example-usage}

```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            -- Handle detailed contact point data
            pprint(event)
        elseif event.type == hash("collision_event") then
            -- Handle general collision data
            pprint(event)
        elseif event.type == hash("trigger_event") then
            -- Handle trigger interaction data
            pprint(event)
        elseif event.type == hash("ray_cast_response") then
            -- Handle raycast hit data
            pprint(event)
        elseif event.type == hash("ray_cast_missed") then
            -- Handle raycast miss data
            pprint(event)
        end
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```

## Обмеження {#limitations}

Слухач викликається синхронно в момент виникнення події. Це відбувається посеред кроку симуляції, тобто фізичний світ заблокований. Через це неможливо використовувати функції, які можуть вплинути на симуляцію фізичного світу, наприклад `physics.create_joint()`.

Ось невеликий приклад того, як обійти ці обмеження:
```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            local position_a = event.a.normal * SIZE
            local position_b =  event.b.normal * SIZE
            local url_a = msg.url(nil, event.a.id, "collisionobject")
            local url_b = msg.url(nil, event.b.id, "collisionobject")
            -- fill the message in the same way arguments should be passed to `physics.create_joint()`
            local message = {physics.JOINT_TYPE_FIXED, url_a, "joind_id", position_a, url_b, position_b, {max_length = SIZE}}
            -- send message to the object itself
            msg.post(".", "create_joint", message)
        end
    end
end

function on_message(self, message_id, message)
    if message_id == hash("create_joint") then
        -- unpack message with function arguments
        physics.create_joint(unpack(message))
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```
