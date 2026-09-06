---
title: Посібник із компонента-фабрики
brief: Цей посібник пояснює, як використовувати компоненти-фабрики для динамічного створення ігрових об’єктів під час виконання.
---

# Компоненти-фабрики {#factory-components}

Компоненти-фабрики (factory components) використовуються для динамічного створення ігрових об’єктів (game objects) із пулу об’єктів у запущеній грі.

Коли ви додаєте компонент-фабрику до ігрового об’єкта, у властивості *Prototype* ви вказуєте, який файл ігрового об’єкта фабрика має використовувати як прототип (в інших рушіях також відомий як «префаб» (prefab) або «шаблон» (blueprint)) для всіх нових ігрових об’єктів, які вона створює.

![Компонент-фабрика](images/factory/factory_collection.png)

![Компонент-фабрика](images/factory/factory_component.png)

Щоб створити ігровий об’єкт, викличте `factory.create()`:

```lua
-- factory.script
local p = go.get_position()
p.y = vmath.lerp(math.random(), min_y, max_y)
local component = "#star_factory"
factory.create(component, p)
```

![Створений ігровий об’єкт](images/factory/factory_spawned.png)

`factory.create()` приймає 5 параметрів:

`url`
: Ідентифікатор компонента-фабрики, який має створити новий ігровий об’єкт.

`[position]`
: (необов’язковий) Позиція нового ігрового об’єкта у світовому просторі. Має бути значенням типу `vector3`. Якщо ви не вкажете позицію, ігровий об’єкт буде створено в позиції ігрового об’єкта, який викликає `factory.create()`.

`[rotation]`
: (необов’язковий) Поворот нового ігрового об’єкта у світовому просторі. Має бути значенням типу `quat`.

`[properties]`
: (необов’язковий) Таблиця Lua зі значеннями властивостей скрипту, якими потрібно ініціалізувати ігровий об’єкт. Інформацію про властивості скрипту див. у [посібнику з властивостей скрипту](/manuals/script-properties).

`[scale]`
: (необов’язковий) Масштаб створеного ігрового об’єкта. Масштаб можна задати значенням типу `number` (більшим за 0), яке визначає рівномірне масштабування вздовж усіх осей. Також можна передати `vector3`, у якому кожен компонент визначає масштабування вздовж відповідної осі.

Наприклад:

```lua
-- factory.script
local p = go.get_position()
p.y = vmath.lerp(math.random(), min_y, max_y)
local component = "#star_factory"
-- Spawn with no rotation but double scale.
-- Set the score of the star to 10.
factory.create(component, p, nil, { score = 10 }, 2.0) -- <1>
```
1. Задає властивість `score` ігрового об’єкта зірки.

```lua
-- star.script
go.property("score", 1) -- <1>

local speed = -240

function update(self, dt)
    local p = go.get_position()
    p.x = p.x + speed * dt
    if p.x < -32 then
        go.delete()
    end
    go.set_position(p)
end

function on_message(self, message_id, message, sender)
    if message_id == hash("collision_response") then
        msg.post("main#gui", "add_score", {amount = self.score}) -- <2>
        go.delete()
    end
end
```
1. Властивість скрипту `score` визначено зі значенням за замовчуванням.
2. Звертайтеся до властивості скрипту `score` як до значення, збереженого в `self`.

![Створений ігровий об’єкт із властивістю та масштабуванням](images/factory/factory_spawned2.png)

::: sidenote
Наразі Defold не підтримує нерівномірне масштабування форм колізій. Якщо ви передасте значення нерівномірного масштабу, наприклад `vmath.vector3(1.0, 2.0, 1.0)`, спрайт буде масштабовано правильно, а форми колізій — ні.
:::


## Адресація об’єктів, створених фабрикою {#addressing-of-factory-created-objects}

Механізм адресації Defold дає змогу звертатися до кожного об’єкта й компонента в запущеній грі. У [посібнику з адресації](/manuals/addressing/) докладно описано, як працює ця система. Той самий механізм адресації можна використовувати для створених ігрових об’єктів та їхніх компонентів. Часто достатньо використати ідентифікатор створеного об’єкта, наприклад, для надсилання повідомлення:

```lua
local function create_hunter(target_id)
    local id = factory.create("#hunterfactory")
    msg.post(id, "hunt", { target = target_id })
    return id
end
```

::: sidenote
Надсилання повідомлення самому ігровому об’єкту замість конкретного компонента фактично надсилає його всім компонентам. Зазвичай це не проблема, але варто пам’ятати про це, якщо об’єкт має багато компонентів.
:::

А що робити, якщо потрібно звернутися до конкретного компонента створеного ігрового об’єкта, наприклад, щоб вимкнути об’єкт колізії або змінити зображення спрайта? Для цього потрібно сформувати URL з ідентифікатора ігрового об’єкта та ідентифікатора компонента.

```lua
local function create_guard(unarmed)
    local id = factory.create("#guardfactory")
    if unarmed then
        local weapon_sprite_url = msg.url(nil, id, "weapon")
        msg.post(weapon_sprite_url, "disable")

        local body_sprite_url = msg.url(nil, id, "body")
        sprite.play_flipbook(body_sprite_url, hash("red_guard"))
    end
end
```


## Відстеження створених і батьківських об’єктів {#tracking-spawned-and-parent-objects}

Коли ви викликаєте `factory.create()`, у відповідь ви отримуєте ідентифікатор нового ігрового об’єкта, який можна зберегти для подальшого використання. Поширений варіант — створювати об’єкти й додавати їхні ідентифікатори до таблиці, щоб згодом видалити їх усі, наприклад, під час скидання розташування об’єктів рівня:

```lua
-- spawner.script
self.spawned_coins = {}

...

-- Spawn a coin and store it in the "coins" table.
local id = factory.create("#coinfactory", coin_position)
table.insert(self.spawned_coins, id)
```

А згодом:

```lua
-- spawner.script
-- Delete all spawned coins.
for _, coin_id in ipairs(self.spawned_coins) do
    go.delete(coin_id)
end

-- or alternatively
go.delete(self.spawned_coins)
```

Також часто потрібно, щоб створений об’єкт знав про ігровий об’єкт, який його створив. Наприклад, це може бути певний тип автономного об’єкта, який може існувати лише в одному екземплярі (instance) одночасно. Тоді створений об’єкт має сповістити об’єкт, який його створив, про своє видалення або деактивацію, щоб можна було створити наступний:

```lua
-- spawner.script
-- Spawn a drone and set its parent to the url of this script component
self.spawned_drone = factory.create("#dronefactory", drone_position, nil, { parent = msg.url() })

...

function on_message(self, message_id, message, sender)
    if message_id == hash("drone_dead") then
        self.spawned_drone = nil
    end
end
```

А логіка створеного об’єкта:

```lua
-- drone.script
go.property("parent", msg.url())

...

function final(self)
    -- I'm dead.
    msg.post(self.parent, "drone_dead")
end
```

## Динамічне завантаження ресурсів фабрики {#dynamic-loading-of-factory-resources}

Якщо встановити прапорець *Load Dynamically* у властивостях фабрики, рушій відкладе завантаження ресурсів, пов’язаних із фабрикою.

![Динамічне завантаження](images/factory/load_dynamically.png)

Якщо прапорець не встановлено, рушій завантажує ресурси прототипу під час завантаження компонента-фабрики, тому вони одразу готові до створення об’єктів.

Якщо прапорець встановлено, є два варіанти використання:

Синхронне завантаження
: Викличте [`factory.create()`](/ref/factory/#factory.create), коли потрібно створити об’єкти. Ресурси буде завантажено синхронно, що може спричинити коротку затримку, а потім буде створено нові екземпляри.

  ```lua
  function init(self)
      -- No factory resources are loaded when the factory’s parent
      -- collection is loaded. Calling create without having called
      -- load will create the resources synchronously.
      self.go_id = factory.create("#factory")
  end

  function final(self)  
      -- Delete game objects. Will decref resources.
      -- In this case resources are deleted since the factory component
      -- holds no reference.
      go.delete(self.go_id)

      -- Calling unload will do nothing since factory holds no references
      factory.unload("#factory")
  end
  ```

Асинхронне завантаження
: Викличте [`factory.load()`](/ref/factory/#factory.load), щоб явно завантажити ресурси асинхронно. Коли ресурси будуть готові до створення об’єктів, буде виконано зворотний виклик.

  ```lua
  function load_complete(self, url, result)
      -- Loading is complete, resources are ready to spawn
      self.go_id = factory.create(url)
  end

  function init(self)
      -- No factory resources are loaded when the factory’s parent
      -- collection is loaded. Calling load will load the resources.
      factory.load("#factory", load_complete)
  end

  function final(self)
      -- Delete game object. Will decref resources.
      -- In this case resources aren’t deleted since the factory component
      -- still holds a reference.
      go.delete(self.go_id)

      -- Calling unload will decref resources held by the factory component,
      -- resulting in resources being destroyed.
      factory.unload("#factory")
  end
  ```

## Динамічний прототип {#dynamic-prototype}

Можна змінювати, який *Prototype* створює фабрика, установивши прапорець *Dynamic Prototype* у властивостях фабрики.

![Динамічний прототип](images/factory/dynamic_prototype.png)

Коли параметр *Dynamic Prototype* увімкнено, компонент-фабрика може змінювати прототип за допомогою функції `factory.set_prototype()`. Приклад:

```lua
factory.unload("#factory") -- unload the previous resources
factory.set_prototype("#factory", "/main/levels/enemyA.goc")
local enemy_id = factory.create("#factory")
```

::: important
Коли параметр *Dynamic Prototype* увімкнено, кількість компонентів колекції (collection) неможливо оптимізувати, і колекція, якій належить фабрика, використовуватиме значення кількості компонентів за замовчуванням із файлу *game.project*.
:::


## Обмеження кількості екземплярів {#instance-limits}

Налаштування проєкту *Max Instances* у розділі *Collection* задає верхню межу кількості ігрових об’єктів у кожній колекції (світі). Під час збирання Defold може виділити місце для меншої кількості об’єктів, якщо встановить, що це безпечно. До цього ліміту враховуються всі ігрові об’єкти, які одночасно існують у світі, незалежно від того, чи їх розміщено в редакторі, чи створено під час виконання.

![Максимальна кількість екземплярів](images/factory/factory_max_instances.png)

Фактичний обсяг виділеного місця залежить від аналізу під час збирання:

* Якщо під час збирання можна визначити фіксовану кількість ігрових об’єктів (зазвичай коли колекція не має фабрики або фабрики колекцій), ліміт дорівнює кількості, визначеній під час компіляції, але не перевищує *Max Instances*.
* Колекція, яка містить фабрику або фабрику колекцій, використовує *Max Instances* як ліміт кількості ігрових об’єктів. Для прототипу зі статичним посиланням під час збирання визначаються типи компонентів, які фабрика може створювати. Для цих типів використовуються відповідні максимальні значення кількості з налаштувань проєкту, а для типів компонентів, яких це не стосується, і далі можуть використовуватися точні кількості.
* Увімкнення *Dynamic Prototype* вимикає аналіз кількості компонентів для колекції, якій належить фабрика, тому вона використовує *Max Instances* і налаштовані максимальні значення кількості для кожного типу компонента.

Плануючи значення *Max Instances*, орієнтуйтеся на найбільшу кількість ігрових об’єктів, які можуть одночасно існувати в динамічному світі. Як обчислюються інші обмеження кількості компонентів, див. у розділі [Оптимізація максимальної кількості компонентів](/manuals/project-settings/#component-max-count-optimizations).

## Пул ігрових об’єктів {#pooling-of-game-objects}

Може здаватися, що зберігати створені ігрові об’єкти в пулі та використовувати їх повторно — добра ідея. Однак рушій уже використовує пул об’єктів усередині, тому додаткові накладні витрати лише сповільнять роботу. Видаляти ігрові об’єкти й створювати нові — швидше та простіше.
