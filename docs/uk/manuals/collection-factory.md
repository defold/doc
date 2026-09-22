---
title: Посібник з фабрик колекцій
brief: Цей посібник пояснює, як використовувати компоненти фабрик колекцій для створення ієрархій ігрових об’єктів.
---

# Фабрики колекцій {#collection-factories}

Компонент (component) фабрики колекцій (collection factory) використовується для створення в запущеній грі груп та ієрархій ігрових об’єктів (game objects), збережених у файлах колекцій (collections).

Колекції надають потужний механізм створення шаблонів для повторного використання, або «префабів» (prefabs), у Defold. Огляд колекцій наведено в [документації про будівельні блоки](/manuals/building-blocks#collections). Колекції можна розміщувати в редакторі або динамічно додавати до гри.

За допомогою компонента фабрики колекцій можна створити в ігровому світі об’єкти з файлу колекції. Це аналогічно створенню всіх ігрових об’єктів усередині колекції за допомогою фабрики з подальшою побудовою батьківсько-дочірньої ієрархії між ними. Типовий випадок використання — створення ворогів, що складаються з кількох ігрових об’єктів (наприклад, ворог + зброя).

## Створення колекції {#spawning-a-collection}

Припустімо, нам потрібні ігровий об’єкт персонажа й окремий ігровий об’єкт щита, дочірній до персонажа. Побудуємо ієрархію ігрових об’єктів у файлі колекції та збережемо його як `bean.collection`.

::: sidenote
Компонент *проксі колекції* (collection proxy) використовується для створення нового ігрового світу, включно з окремим фізичним світом, на основі колекції. Доступ до нового світу здійснюється через новий сокет. Усі ресурси колекції завантажуються через проксі, коли ви надсилаєте йому повідомлення для початку завантаження. Завдяки цьому проксі дуже корисні, наприклад, для зміни рівнів у грі. Однак створення нових ігрових світів потребує досить значних додаткових витрат ресурсів, тому не використовуйте їх для динамічного завантаження дрібних елементів. Докладніше див. у [документації про проксі колекції](/manuals/collection-proxy).
:::

![Колекція для створення](images/collection_factory/collection.png)

Далі додамо *Collection factory* до ігрового об’єкта, який відповідатиме за створення, і задамо `bean.collection` у властивості *Prototype* цього компонента:

![Фабрика колекцій](images/collection_factory/factory.png)

Тепер для створення `bean` і щита достатньо викликати функцію `collectionfactory.create()`:

```lua
local bean_ids = collectionfactory.create("#bean_factory")
```

Функція приймає 5 параметрів:

`url`
: Ідентифікатор компонента фабрики колекцій, який має створити новий набір ігрових об’єктів.

`[position]`
: (необов’язковий) Позиція створених ігрових об’єктів у світовому просторі. Має бути значенням типу `vector3`. Якщо позицію не вказано, об’єкти створюються в позиції компонента фабрики колекцій.

`[rotation]`
: (необов’язковий) Поворот нових ігрових об’єктів у світовому просторі. Має бути значенням типу `quat`.

`[properties]`
: (необов’язковий) Таблиця Lua з парами `id`-`table`, що використовуються для ініціалізації створених ігрових об’єктів. Нижче описано, як побудувати цю таблицю.

`[scale]`
: (необов’язковий) Масштаб створених ігрових об’єктів. Масштаб можна виразити значенням типу `number` (більшим за 0), яке задає рівномірне масштабування вздовж усіх осей. Також можна передати `vector3`, де кожна складова задає масштабування вздовж відповідної осі.

`collectionfactory.create()` повертає ідентифікатори створених ігрових об’єктів у вигляді таблиці. Ключі таблиці зіставляють хеш локального для колекції ідентифікатора кожного об’єкта з його ідентифікатором у середовищі виконання:

::: sidenote
Батьківсько-дочірній зв’язок між `bean` і `shield` *не* відображається в повернутій таблиці. Цей зв’язок існує лише в графі сцени під час виконання, тобто визначає, як об’єкти трансформуються разом. Зміна батьківського об’єкта ніколи не змінює ідентифікатор об’єкта.
:::

```lua
local bean_ids = collectionfactory.create("#bean_factory")
go.set_scale_xy(0.5, bean_ids[hash("/bean")])
pprint(bean_ids)
-- DEBUG:SCRIPT:
-- {
--   hash: [/shield] = hash: [/collection0/shield], -- <1>
--   hash: [/bean] = hash: [/collection0/bean],
-- }
```
1. До ідентифікатора додається префікс `/collection[N]/`, де `[N]` — лічильник, щоб однозначно ідентифікувати кожен екземпляр (instance):

## Властивості {#properties}

Під час створення колекції можна передати параметри властивостей кожному ігровому об’єкту, побудувавши таблицю, у якій ключами є ідентифікатори об’єктів, а значеннями — таблиці з властивостями скрипту, які потрібно встановити.

```lua
local props = {}
props[hash("/bean")] = { shield = false }
local ids = collectionfactory.create("#bean_factory", nil, nil, props)
```

Припустімо, що ігровий об’єкт `bean` у `bean.collection` визначає властивість `shield`. [Посібник із властивостей скриптів](/manuals/script-properties) містить інформацію про властивості скриптів.

```lua
-- bean/controller.script
go.property("shield", true)

function init(self)
    if not self.shield then
        go.delete("shield")
    end     
end
```

## Динамічне завантаження ресурсів фабрики {#dynamic-loading-of-factory-resources}

Якщо встановити прапорець *Load Dynamically* у властивостях фабрики колекцій, рушій відкладе завантаження пов’язаних із фабрикою ресурсів.

![Динамічне завантаження](images/collection_factory/load_dynamically.png)

Якщо прапорець знято, рушій завантажує ресурси прототипу під час завантаження компонента фабрики колекцій, тож вони одразу готові до створення об’єктів.

Якщо прапорець встановлено, є два варіанти використання:

Синхронне завантаження
: Викличте [`collectionfactory.create()`](/ref/collectionfactory/#collectionfactory.create:url-[position]-[rotation]-[properties]-[scale]), коли потрібно створити об’єкти. Це синхронно завантажить ресурси, що може спричинити короткочасну затримку, а потім створить нові екземпляри.

  ```lua
  function init(self)
      -- No factory resources are loaded when the collection factory’s
      -- parent collection is loaded. Calling create without
      -- having called load will create the resources synchronously.
      self.go_ids = collectionfactory.create("#collectionfactory")
  end

  function final(self)  
      -- Delete game objects. Will decref resources.
      -- In this case resources are deleted since the collection
      -- factory component holds no reference.
      go.delete(self.go_ids)

      -- Calling unload will do nothing since factory holds
      -- no references
      collectionfactory.unload("#factory")
  end
  ```

Асинхронне завантаження
: Викличте [`collectionfactory.load()`](/ref/collectionfactory/#collectionfactory.load:[url]-[complete_function]), щоб явно завантажити ресурси асинхронно. Коли ресурси будуть готові до створення об’єктів, буде виконано зворотний виклик.

  ```lua
  function load_complete(self, url, result)
      -- Loading is complete, resources are ready to spawn
      self.go_ids = collectionfactory.create(url)
  end

  function init(self)
      -- No factory resources are loaded when the collection factory’s
      -- parent collection is loaded. Calling load will load the resources.
      collectionfactory.load("#factory", load_complete)
  end

  function final(self)
      -- Delete game object. Will decref resources.
      -- In this case resources aren’t deleted since the collection factory
      -- component still holds a reference.
      go.delete(self.go_ids)

      -- Calling unload will decref resources held by the factory component,
      -- resulting in resources being destroyed.
      collectionfactory.unload("#factory")
  end
  ```


## Динамічний прототип {#dynamic-prototype}

Можна змінювати, який *Prototype* створює фабрика колекцій, якщо встановити прапорець *Dynamic Prototype* у властивостях фабрики колекцій.

![Динамічний прототип](images/collection_factory/dynamic_prototype.png)

Коли прапорець *Dynamic Prototype* встановлено, компонент фабрики колекцій може змінювати прототип за допомогою функції `collectionfactory.set_prototype()`. Приклад:

```lua
collectionfactory.unload("#factory") -- unload the previous resources
collectionfactory.set_prototype("#factory", "/main/levels/level1.collectionc")
local ids = collectionfactory.create("#factory")
```

::: important
Коли параметр *Dynamic Prototype* увімкнено, кількість компонентів колекції не можна оптимізувати, і колекція, якій належить фабрика, використовуватиме типові значення кількості компонентів із файлу *game.project*.
:::
