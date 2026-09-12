---
title: Властивості компонентів-скриптів
brief: Цей посібник пояснює, як додавати власні властивості до компонентів-скриптів і звертатися до них із редактора та скриптів під час виконання.
---

# Властивості скриптів {#script-properties}

Властивості скриптів — простий і потужний спосіб визначати власні властивості для конкретного екземпляра (instance) ігрового об’єкта (game object) і надавати до них доступ. Властивості скриптів можна редагувати для окремих екземплярів безпосередньо в редакторі, а їхні значення — використовувати в коді для змінення поведінки ігрового об’єкта. Властивості скриптів дуже корисні в багатьох випадках:

* Коли ви хочете перевизначати значення для окремих екземплярів у редакторі й у такий спосіб розширити можливості повторного використання скрипту.
* Коли ви хочете створити ігровий об’єкт із початковими значеннями.
* Коли ви хочете анімувати значення властивості.
* Коли ви хочете отримати доступ до даних стану одного скрипту з іншого. (Зауважте: якщо ви часто звертаєтеся до властивостей між об’єктами, можливо, краще перенести дані до спільного сховища.)

Типові випадки використання — задавання здоров’я або швидкості конкретного ворога, керованого ШІ, кольору тонування предмета, який можна підібрати, атласу спрайта або повідомлення, яке об’єкт-кнопка має надсилати після натискання, та/або адреси його отримувача.

## Визначення властивості скрипту {#defining-a-script-property}

Властивості скриптів додають до компонента-скрипту (script component), визначаючи їх за допомогою спеціальної функції `go.property()`. Цю функцію потрібно використовувати на верхньому рівні — поза функціями життєвого циклу, як-от `init()` і `update()`. Надане значення за замовчуванням визначає тип властивості: `number`, `boolean`, `string`, `hash`, `msg.url`, `vmath.vector3`, `vmath.vector4`, `vmath.quaternion` і `resource` (див. нижче).

::: important
Зауважте, що відновлення початкового рядка за значенням хешу працює лише у збірці Debug, щоб полегшити налагодження. У збірці Release початкове рядкове значення відсутнє, тому використовувати `tostring()` для значення `hash`, щоб отримати з нього рядок, немає сенсу.
:::


```lua
-- can.script
-- Define script properties for health and an attack target
go.property("health", 100)
go.property("target", msg.url())

function init(self)
  -- store initial position of target.
  -- self.target is a url referencing another object.
  self.target_pos = go.get_position(self.target)
  ...
end

function on_message(self, message_id, message, sender)
  if message_id == hash("take_damage") then
    -- decrease the health property
    self.health = self.health - message.damage
    if self.health <= 0 then
      go.delete()
    end
  end
end
```

Після цього для будь-якого екземпляра компонента-скрипту, створеного з цього скрипту, можна задавати значення властивостей.

![Компонент із властивостями](images/script-properties/component.png)

 Виберіть компонент-скрипт у панелі *Outline* редактора, і властивості з’являться в панелі *Properties*, де їх можна редагувати:

![Властивості](images/script-properties/properties.png)

Кожна властивість, для якої перевизначено значення в конкретному екземплярі, позначається синім. Натисніть кнопку скидання біля назви властивості, щоб повернути типове значення (задане у скрипті).


::: important
Властивості скриптів розбираються під час збирання проєкту. Вирази значень не обчислюються. Це означає, що запис на кшталт `go.property("hp", 3+6)` не працюватиме, а `go.property("hp", 9)` — працюватиме.
:::

### Текстові властивості {#text-properties}

Починаючи з Defold 1.13.2, рядкове значення за замовчуванням визначає текстову властивість. Текстові властивості підтримують UTF-8 і символи нового рядка та редагуються в багаторядковому полі редактора:

```lua
go.property("greeting", "Hello!\nWelcome, José!")

function init(self)
    go.set("#label", "text", self.greeting)
end
```

Виберіть компонент-скрипт в ігровому об’єкті або колекції, щоб перевизначити його текстові властивості так само, як інші властивості скрипту. Символи NUL усередині значень за замовчуванням або перевизначень не допускаються.

Інші скрипти можуть читати й записувати текстову властивість через URL компонента-скрипту. Наприклад, помістіть наведений вище скрипт і напис в ігровий об’єкт із назвою `speaker` у колекції, з ідентифікаторами компонентів `script` і `label`. Оновіть їх із `init()` іншого скрипту:

```lua
function init(self)
    local greeting = go.get("/speaker#script", "greeting")
    go.set("/speaker#script", "greeting", greeting .. "\nEnjoy the game!")
    go.set("/speaker#label", "text", go.get("/speaker#script", "greeting"))
end
```

Зміна властивості скрипту не оновлює напис автоматично; останній рядок явно копіює нове значення до властивості `text` напису.

## Доступ до властивостей скриптів {#accessing-script-properties}

Кожна визначена властивість скрипту доступна як поле в `self` — посиланні на екземпляр скрипту:

```lua
-- my_script.script
go.property("my_property", 1)

function update(self, dt)
  -- Read and write the property
  if self.my_property == 1 then
      self.my_property = 3
  end
end
```

Визначені користувачем властивості скриптів також можна читати за допомогою `go.get()` і записувати за допомогою `go.set()`. Числові властивості, зокрема вектори й кватерніони, можна анімувати за допомогою `go.animate()`. Текстові властивості можна читати й записувати, але не можна анімувати:

```lua
-- another.script

-- increase "my_property" in "myobject#script" by 1
local val = go.get("myobject#my_script", "my_property")
go.set("myobject#my_script", "my_property", val + 1)

-- animate "my_property" in "myobject#my_script"
go.animate("myobject#my_script", "my_property", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_LINEAR, 2.0)
```

## Об’єкти, створені фабрикою {#factory-created-objects}

Якщо ви використовуєте фабрику (factory) для створення ігрового об’єкта, властивості скрипту можна задати під час його створення:

```lua
local props = { health = 50, target = msg.url("player") }
local id = factory.create("#can_factory", nil, nil, props)

-- Accessing factory-created script properties
local url = msg.url(nil, id, "can")
local can_health = go.get(url, "health")
```

Коли ви створюєте ієрархію ігрових об’єктів через `collectionfactory.create()`, потрібно зіставити ідентифікатори об’єктів із таблицями властивостей. Ці пари об’єднують у таблицю й передають функції `create()`:

```lua
local props = {}
props[hash("/can1")] = { health = 150 }
props[hash("/can2")] = { health = 250, target = msg.url("player") }
props[hash("/can3")] = { health = 200 }

local ids = collectionfactory.create("#cangang_factory", nil, nil, props)
```

Значення властивостей, передані через `factory.create()` і `collectionfactory.create()`, перевизначають будь-які значення, задані у файлі прототипу, а також типові значення у скрипті.

Якщо кілька компонентів-скриптів, приєднаних до ігрового об’єкта, визначають ту саму властивість, кожен компонент буде ініціалізовано значенням, переданим у `factory.create()` або `collectionfactory.create()`.


## Властивості ресурсів {#resource-properties}

Властивості ресурсів визначають так само, як властивості скриптів для базових типів даних:

```lua
go.property("my_atlas", resource.atlas("/atlas.atlas"))
go.property("my_font", resource.font("/font.font"))
go.property("my_material", resource.material("/material.material"))
go.property("my_texture", resource.texture("/texture.png"))
go.property("my_tile_source", resource.tile_source("/tilesource.tilesource"))
```

Коли властивість ресурсу визначено, вона з’являється в панелі *Properties*, як і будь-яка інша властивість скрипту, але як поле вибору файлу або ресурсу:

![Властивості ресурсів](images/script-properties/resource-properties.png)

Ви отримуєте доступ до властивостей ресурсів через `go.get()` або посилання на екземпляр скрипту `self`, а використовуєте їх за допомогою `go.set()`:

```lua
function init(self)
  go.set("#sprite", "image", self.my_atlas)
  go.set("#label", "font", self.my_font)
  go.set("#sprite", "material", self.my_material)
  go.set("#model", "texture0", self.my_texture)
  go.set("#tilemap", "tile_source", self.my_tile_source)
end
```
