---
title: Урок зі створення Magic Link
brief: У цьому уроці ви створите завершену невелику гру-головоломку зі стартовим екраном, ігровими механіками та простим переходом між рівнями зі зростанням складності.
---

# Урок зі створення Magic Link {#magic-link-tutorial}

Ця гра — варіація класичних ігор на поєднання однакових елементів на кшталт _Bejeweled_ і _Candy Crush_. Гравець проводить пальцем і з’єднує блоки одного кольору, щоб прибрати їх, але мета гри — не прибирати довгі ряди одноколірних блоків, очищувати поле чи набирати очки, а з’єднати між собою особливі «магічні блоки», розкидані по полю.

Цей урок — покроковий посібник, у якому ми створюємо гру за готовим задумом. Насправді пошук вдалого ігрового задуму потребує багато часу й зусиль. Можна почати з основної ідеї, а потім знайти спосіб створити її прототип, щоб краще зрозуміти її потенціал. Навіть така проста гра, як «Magic Link», потребує чимало роботи над дизайном. Ця гра пройшла кілька ітерацій і експериментів, перш ніж набула остаточного (і все ще далеко не досконалого) вигляду та набору правил. Але в цьому уроці ми пропустимо цей процес і почнемо створення гри за остаточним задумом.

## Початок роботи {#getting-started}

Почніть зі створення нового проєкту та імпорту пакета ресурсів:

* Створіть [новий проєкт](/manuals/project-setup/#creating-a-new-project) із шаблону «Empty Project»
* Завантажте повний проєкт «Magic Link» [magic-link.zip](https://github.com/defold/defold-examples/releases/latest) як зразок. Він містить усі ресурси на випадок, якщо ви захочете створити проєкт із нуля.

## Правила гри {#game-rules}

![Схема правил гри](images/magic-link/linker_rules.png)

На початку кожного раунду поле випадково заповнюється кольоровими й магічними блоками. Кольорові блоки підпорядковуються таким правилам:

* Вони зникають, якщо гравець з’єднує їх із блоками того самого кольору, проводячи по них пальцем.
* Коли блоки зникають, під іншими блоками утворюються порожні місця. Кольорові блоки просто падають вертикально вниз у порожні місця, що з’явилися під ними.
* Нижній край екрана зупиняє подальше падіння всіх блоків.

Магічні блоки поводяться інакше, за такими правилами:

* Магічні блоки рухаються _вбік_, якщо з будь-якого боку з’являється порожнє місце.
* Якщо порожнє місце з’являється під ними, вони натомість падають, як звичайні кольорові блоки.

Гравець взаємодіє з грою за такими правилами:

* Гравець може проводити пальцем і з’єднувати кольорові блоки, що сусідять по горизонталі, вертикалі й діагоналі.
* З’єднані блоки зникають, щойно гравець припиняє дотик (піднімає палець).
* Магічні блоки не реагують на проведення пальцем, і їх не можна з’єднати вручну.
* Проте магічні блоки реагують на сусідство по горизонталі чи вертикалі. Тобто за таких умов вони з’єднуються автоматично.
* Рівень пройдено, якщо гравцеві вдається домогтися автоматичного з’єднання всіх магічних блоків на полі.

Рівень складності визначає кількість магічних блоків, які розміщуються на полі.

## Огляд {#overview}

Як і в будь-якому проєкті, потрібно скласти загальний план реалізації. Структурувати й побудувати гру можна багатьма способами. Технічно, за бажанням, ми могли б реалізувати всю гру в системі GUI. Однак найчастіше природно створювати гру за допомогою ігрових об’єктів (game objects) і спрайтів, а API GUI використовувати для екранного графічного інтерфейсу та інформаційних елементів поверх гри, тож підемо цим шляхом.

Оскільки ми очікуємо порівняно невелику кількість файлів, структура папок проєкту буде дуже простою:

![Структура папок](images/magic-link/linker_folders.png)

*main*
: У цій папці міститиметься вся ігрова логіка. Тут зберігатимуться всі скрипти, файли ігрових об’єктів, файли колекцій (collections), файли GUI тощо. За бажанням ви цілком можете розділити її на кілька папок або створити вкладені папки.

*images*
: У цій папці зберігатимуться всі зображення.

*fonts*
: Тут зберігаються шрифти, які використовуються для рендерингу тексту.

*input*
: У цій папці зберігаються прив’язки введення.

## Налаштування проєкту {#setting-up-the-project}

У файлі *game.project* здебільшого залишаються типові налаштування, але деякі з них потрібно визначити. Насамперед слід вибрати роздільну здатність гри. Її досить легко змінити пізніше, а для завершеної гри нам потрібно буде попрацювати над тим, щоб вона добре виглядала незалежно від роздільної здатності чи співвідношення сторін цільового пристрою.

Ми вибрали роздільну здатність 640x960 пікселів, яка є рідною для iPhone 4. Вона також вміщується на багатьох моніторах, тож тестувати гру на комп’ютері буде зручно. Якщо ви хочете працювати з іншою роздільною здатністю, потрібно буде лише відповідно скоригувати кілька значень.

![Налаштування проєкту](images/magic-link/linker_project_settings.png)

Також потрібно збільшити максимальну кількість спрайтів для рендерингу. За бажанням ви можете перейти до наступного розділу й повернутися сюди, коли консоль повідомить про досягнення обмеження кількості спрайтів.

![Схема розмірів гри](images/magic-link/linker_layout.png)

Можна розрахувати максимальну потрібну кількість спрайтів:

* Ігрове поле вміщуватиме 7x9 блоків. Уздовж країв поля потрібні відступи, а вгорі — місце для елементів GUI. Отже, розмір блоків становитиме приблизно 90x90 пікселів. Менші блоки були б надто дрібними для взаємодії на невеликому екрані телефона.
* Кожен блок — це один спрайт. Для встановлення кольору блока ми використовуватимемо однокадрові анімації.
* Деякі блоки будуть магічними, і для спецефектів кожного з них ми використовуватимемо 4 спрайти.
* Для графіки з’єднань потрібен один спрайт на елемент. У найгіршому випадку це ще 61 спрайт, якщо гравець якимось чином з’єднає все поле (за винятком 2 магічних блоків, які не можна з’єднати проведенням пальця).

Отже, припустімо, що маємо щонайбільше 30 магічних блоків. Поле містить 63 блоки (спрайти). З них кожен із 30 магічних блоків додає 4 спрайти для спецефектів. Це ще 120 спрайтів. Отже, разом із графікою з’єднань (у цьому випадку щонайбільше 33 спрайти) нам потрібно малювати принаймні 120 + 33 = 153 спрайти кожного кадру. Найближчий степінь двійки — 256.

Однак встановити максимум 256 недостатньо. Щоразу, коли ми очищуватимемо й заново заповнюватимемо поле, ми видалятимемо всі поточні ігрові об’єкти та створюватимемо нові. Обмеження кількості спрайтів має враховувати всі об’єкти, що існують протягом кадру. Це також стосується видалених об’єктів, оскільки вони прибираються наприкінці кадру. Отже, максимального значення 512 спрайтів буде достатньо.

![Максимальна кількість спрайтів](images/magic-link/linker_sprite_max_count.png)

## Додавання графічних ресурсів {#adding-the-graphics-assets}

Усі необхідні ресурси для гри підготовлено заздалегідь. Ми додаємо їх як зображення розміром 512x512 пікселів і даємо рушію зменшити їх до потрібного розміру.

::: sidenote
Увімкнення *hidpi* в налаштуваннях проєкту підвищує роздільну здатність заднього буфера. Великі зображення, намальовані зі зменшенням масштабу, виглядатимуть дуже чітко на екранах Retina.
:::

![Додавання зображень](images/magic-link/linker_add_images.png)

Окрім блоків, до набору входять зображення з’єднувача та спрайти ефектів. Також маємо два фонові зображення: одне для ігрового поля, інше — для головного меню. Додайте всі зображення до папки *images*, а потім створіть файл атласу *sprites.atlas*. Відкрийте файл атласу й додайте всі зображення.

![Додавання зображень до атласу](images/magic-link/linker_add_to_atlas.png)

Набір зображень GUI використовується для створення елементів інтерфейсу, як-от кнопок і спливних вікон. Їх додають до окремого атласу під назвою *gui.atlas*.

## Генерування поля {#generating-the-board}

Перший крок — створити логіку поля. Поле буде в окремій колекції, яка міститиме все, що видно на екрані під час гри. Наразі потрібні лише компонент-фабрика (factory component) «blockfactory» і скрипт. Згодом ми додамо фабрику для з’єднань, компоненти GUI головного меню, а насамкінець — механіку завантаження для початку гри з головного меню та спосіб виходу до меню.

1. Створіть *`board.collection`* у папці *`main`*. Обов’язково назвіть колекцію «board», щоб ми могли адресувати її пізніше. Якщо ви додаєте компонент фонового спрайта, встановіть його позицію Z у -1, інакше він не відображатиметься позаду всіх блоків, які ми створимо згодом.
2. Тимчасово встановіть *Main Collection* (у розділі *Bootstrap*) у *game.project* на `/main/board.collection`, щоб спростити тестування.

![Колекція поля](images/magic-link/linker_board_collection.png)

![Колекція поля як стартова](images/magic-link/linker_bootstrap_board.png)

Файл скрипту *board.script* міститиме всю логіку самого поля та блоків на ньому. Почніть зі створення функції побудови поля й тимчасово викличте її з `init()`. Також додамо дві функції, які поки що не використовуватимемо, але які стануть у пригоді пізніше:

`filter()`
: Ця функція дасть змогу фільтрувати списки елементів (блоків).

`build_blocklist()`
: Створює плоский список усіх блоків на полі, що дає змогу фільтрувати його.

Після побудови поля ми використовуватимемо два різні набори даних, що містять усі блоки: `self.blocks` і `self.board`:

```lua
-- board.script
go.property("timer", 0)     -- Use to time events
local blocksize = 80        -- Distance between block centers
local edge = 40             -- Left and right edge.
local bottom_edge = 50      -- Bottom edge.
local boardwidth = 7        -- Number of columns
local boardheight = 9       -- Number of rows
local centeroff = vmath.vector3(8, -8, 0) -- Center offset for connector gfx since there's shadow below in the block img
local dropamount = 3        -- The number of blocks dropped on a "drop"
local colors = { hash("orange"), hash("pink"), hash("blue"), hash("yellow"), hash("green") }

--
-- filter(function, table)
-- e.g: filter(is_even, {1,2,3,4}) -> {2,4}
--
local function filter(func, tbl)
    local new = {}
    for i, v in pairs(tbl) do
        if func(v) then
            new[i] = v
        end
    end
    return new
end

--
-- Build a list of blocks in 1 dimension for easy filtering
--
local function build_blocklist(self)
    self.blocks = {}
    for x, l in pairs(self.board) do
        for y, b in pairs(self.board[x]) do
            table.insert(self.blocks, { id = b.id, color = b.color, x = b.x, y = b.y })
        end
    end
end

--
-- INIT
--
function init(self)
    self.board = {}             -- Contains the board structure
    self.blocks = {}            -- List of all blocks. Used for easy filtering on selection.
    self.chain = {}             -- Current selection chain
    self.connectors = {}        -- Connector elements to mark the selection chain
    self.num_magic = 3          -- Number of magic blocks on the board
    self.drops = 1              -- Number of drops you have available
    self.magic_blocks = {}      -- Magic blocks that are lined up
    self.dragging = false       -- Drag touch input
    msg.post(".", "acquire_input_focus")
    msg.post("#", "start_level")
end

local function build_board(self)
    math.randomseed(os.time())
    local pos = vmath.vector3()
    local c
    local x = 0
    local y = 0
    for x = 0,boardwidth-1 do
        pos.x = edge + blocksize / 2 + blocksize * x
        self.board[x] = {}
        for y = 0,boardheight-1 do
            pos.y = bottom_edge + blocksize / 2 + blocksize * y
            -- Calc z
            pos.z = x * -0.1 + y * 0.01 -- <1>
            c = colors[math.random(#colors)]    -- Pick a random color
            local id = factory.create("#blockfactory", pos, null, { color = c })
            self.board[x][y] = { id = id, color = c,  x = x, y = y }
        end
    end

    -- Build 1d list that we can easily filter.
    build_blocklist(self)
end

function on_message(self, message_id, message, sender)
    if message_id == hash("start_level") then
        build_board(self)
    end
end
```
1. Зауважте, що графіка блоків перекривається, тому їх потрібно малювати в правильному порядку. Для цього встановлюємо координату z кожного блока. Її значення залишатиметься значно вищим за -1, де розташований фоновий спрайт.

Логіка поля створює ігрові об’єкти «`block`» через компонент-фабрику «`blockfactory`». Щоб це працювало, потрібно створити ігровий об’єкт блока. Блок містить скрипт і спрайт. Встановлюємо типову анімацію спрайта на будь-який із кольорових блоків у *`sprites.atlas`*, а потім додаємо код до *`block.script`*, щоб блок набував потрібного кольору під час створення:

![Ігровий об’єкт блока](images/magic-link/linker_block.png)

```lua
-- block.script
go.property("color", hash("none"))

function init(self)
    go.set_scale_xy(0.18)     -- render scaled down without changing Z

    if self.color ~= nil then
        sprite.play_flipbook("#sprite", self.color)
    else
        msg.post("#sprite", "disable")
    end
end
```

Встановіть властивість *Prototype* компонента-фабрики «blockfactory» на новий файл ігрового об’єкта *block.go*.

![Фабрика блоків](images/magic-link/linker_blockfactory.png)

Тепер ви можете запустити гру й побачити поле, заповнене блоками випадкових кольорів:

![Перший знімок екрана](images/magic-link/linker_first_screenshot.png)

## Взаємодія {#interactions}

Тепер, коли ми маємо поле, потрібно додати взаємодію з користувачем. Спочатку визначимо прив’язки введення у файлі *game.input_binding* у папці *input*. Переконайтеся, що налаштування *game.project* використовують ваш файл прив’язок введення.

![Прив’язки введення](images/magic-link/linker_input_bindings.png)

Нам потрібна лише одна прив’язка: призначаємо `MOUSE_BUTTON_LEFT` дії з назвою «touch». Ця гра не використовує мультитач, а для зручності Defold перетворює дотики одним пальцем на натискання лівої кнопки миші.

За обробку введення відповідає поле, тому потрібно додати відповідний код до *board.script*:

```lua
-- board.script
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.value == 1 then
        -- What block was touched or dragged over?
        local x = math.floor((action.x - edge) / blocksize)
        local y = math.floor((action.y - bottom_edge) / blocksize)

        if x < 0 or x >= boardwidth or y < 0 or y >= boardheight or self.board[x][y] == nil then
            -- outside board.
            return
        end

        if action.pressed then
            -- Player started touch
            msg.post(self.board[x][y].id, "make_orange")

            self.dragging = true
        elseif self.dragging then
            -- then drag
            msg.post(self.board[x][y].id, "make_green")
        end
    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false
    end
end
```

Повідомлення `make_orange` і `make_green` потрібні лише тимчасово, щоб візуально перевірити роботу коду. Для обробки цих повідомлень потрібно додати код до *block.script*:

```lua
-- block.script
function on_message(self, message_id, message, sender)
    if message_id == hash("make_orange") then
        sprite.play_flipbook("#sprite", hash("orange"))
    elseif message_id == hash("make_green") then
        sprite.play_flipbook("#sprite", hash("green"))
    end
end
```

Тепер блоки отримуватимуть спочатку одне повідомлення `make_orange`, а потім повідомлення `make_green`, доки ви торкаєтеся екрана (або утримуєте кнопку миші). Тож блоки, найімовірніше, лише на мить стануть помаранчевими (якщо взагалі встигнуть), перш ніж позеленіють. Зате ми знаємо, якого блока торкається гравець! Якщо хочете докладніше простежити обробку введення, вставте в код виклики `print()` або `pprint()`.

## Позначення з’єднань {#mark-links}

Тепер потрібні ресурси для маркера, який показуватиме, що гравець з’єднав блоки. Ідея проста: накласти зображення на кожен блок, щоб позначити його як з’єднаний.

Потрібно створити ігровий об’єкт «connector», що містить спрайт з’єднувача, а також компонент-фабрику «connector factory» в ігровому об’єкті «board»:

![Ігровий об’єкт з’єднувача](images/magic-link/linker_connector.png)

![Фабрика з’єднувачів](images/magic-link/linker_connector_factory.png)

Скрипт цього ігрового об’єкта мінімальний: він має лише змінити масштаб графіки, щоб вона відповідала решті гри, і правильно встановити порядок за Z.

```lua
-- connector.script
function init(self)
    go.set_scale_xy(0.18)           -- Scale in 2D without changing Z.
    go.set(".", "position.z", 1)    -- Put on top.
end
```

Функція `same_color_neighbors()` повертає список блоків того самого кольору, що сусідять із певним блоком (у позиції x, y). Ця функція використовує `filter()`, застосовуючи її до повного плоского списку блоків у `self.blocks`.

```lua
-- board.script
--
-- Returns a list of neighbor blocks of the same color as the
-- block on x, y
--
local function same_color_neighbors(self, x, y)
    local f = function (v)
        return (v.id ~= self.board[x][y].id) and
               (v.x == x or v.x == x - 1 or v.x == x + 1) and
               (v.y == y or v.y == y - 1 or v.y == y + 1) and
               (v.color == self.board[x][y].color)
    end
    return filter(f, self.blocks)
end
```

Допоміжна функція `in_blocklist()` перевіряє, чи є блок у списку блоків:

```lua
-- board.script
--
-- Does the block exist in the list of blocks?
--
local function in_blocklist(blocks, block)
    for i, b in pairs(blocks) do
        if b.id == block then
            return true
        end
    end
    return false
end
```

Під час обробки дотиків і проведення пальцем у `on_input()` ми використовуємо ці функції, щоб формувати з’єднання між блоками, яких торкнулися. Тут ми перевірятимемо й ігноруватимемо магічні блоки, хоча їх поки що немає:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    -- If trying to manipulate magic blocks, ignore.
    if self.board[x][y].color == hash("magic") then
        return
    end

    if action.pressed then
        -- List of neighbors of the same color as touched block
        self.neighbors = same_color_neighbors(self, x, y)
        self.chain = {}
        table.insert(self.chain, self.board[x][y])

        -- Mark block.
        p = go.get_position(self.board[x][y].id)
        local id = factory.create("#connectorfactory", p + centeroff)
        table.insert(self.connectors, id)

        self.dragging = true
    elseif self.dragging then
        -- then drag
        if in_blocklist(self.neighbors, self.board[x][y].id) and not in_blocklist(self.chain, self.board[x][y].id) then
            -- dragging over a same-colored neighbor
            table.insert(self.chain, self.board[x][y])
            self.neighbors = same_color_neighbors(self, x, y)

            -- Mark block.
            p = go.get_position(self.board[x][y].id)
            local id = factory.create("#connectorfactory", p + centeroff)
            table.insert(self.connectors, id)
        end
    end
```

І нарешті, після припинення дотику приберемо з екрана всі з’єднувачі.

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        -- Empty chain of connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
end
```

![З’єднувачі в грі](images/magic-link/linker_connector_screen.png)

## Видалення з’єднаних блоків {#remove-linked-blocks}

Тепер маємо логіку для з’єднання блоків одного кольору, тож видалити з’єднані блоки нескладно. Ми встановлюємо для клітинки поля значення `hash("removing")`, а не просто `nil`, тому що пізніше, під час реалізації логіки магічних блоків, потрібно буде забезпечити їхнє переміщення лише на місця щойно видалених блоків. Якщо тут встановити для клітинки поля `nil`, ми не зможемо відрізнити щойно видалені блоки від видалених раніше.

```lua
-- board.script
-- Remove the currently selected block-chain
--
local function remove_chain(self)
    -- Delete all chained blocks
    for i, c in ipairs(self.chain) do
        self.board[c.x][c.y] = hash("removing")
        go.delete(c.id)
    end
    self.chain = {}
end
```

Також потрібна функція, яка остаточно видалить (встановить у `nil`) клітинки поля, яким було призначено `hash("removing")`:

```lua
-- board.script
--
-- Set removed blocks to nil
--
local function nilremoved(self)
    for y = 0,boardheight - 1 do
        for x = 0,boardwidth - 1 do
            if self.board[x][y] == hash("removing") then
                self.board[x][y] = nil
            end
        end
    end
end
```

Створимо ще й функцію, яка зсуває решту блоків униз, коли блоки під ними видаляються (встановлюються в `nil`). Обходимо поле стовпцями зліва направо, а кожен стовпець — знизу вгору. Якщо трапляється порожня клітинка (`nil`), зсуваємо всі блоки над нею вниз.

```lua
-- board.script
--
-- Apply shift-down logic to all blocks.
--
local function slide_board(self)
    -- Slide all remaining blocks down into blank spots.
    -- Going column by column makes this easy.
    local dy = 0
    local pos = vmath.vector3()
    for x = 0,boardwidth - 1 do
        dy = 0
        for y = 0,boardheight - 1 do
            if self.board[x][y] ~= nil then
                if dy > 0 then
                    -- Move down dy steps
                    self.board[x][y - dy] = self.board[x][y]
                    self.board[x][y] = nil
                    -- Calc new position
                    self.board[x][y - dy].y = self.board[x][y - dy].y - dy
                    go.animate(self.board[x][y-dy].id, "position.y", go.PLAYBACK_ONCE_FORWARD, bottom_edge + blocksize / 2 + blocksize * (y - dy), go.EASING_OUTBOUNCE, 0.3)
                    -- Calc new z
                    go.set(self.board[x][y-dy].id, "position.z", x * -0.1 + (y-dy) * 0.01)
                end
            else
                dy = dy + 1
            end
        end
    end
    -- blocklist needs updating
    build_blocklist(self)
end
```

![Зсування блоків униз](images/magic-link/linker_blocks_slide.png)

Тепер можна просто додати виклики цих функцій у `on_input()`, коли дотик припинився й у `self.chain` є блоки.

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        if #self.chain > 1 then
            -- There is a chain of blocks. Remove it from board and slide the remaining blocks down.
            remove_chain(self)
            nilremoved(self)
            slide_board(self)
        end

        -- Empty chain of connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

## Логіка магічних блоків {#magic-block-logic}

Час додати магічні блоки. Насамперед додамо можливість перетворення звичайного блока на магічний. Тоді ми зможемо окремо пройтися по заповненому полю й перетворити потрібні блоки на магічні. Щоб трохи пожвавити їх, спочатку створимо анімований магічний ефект у вигляді ігрового об’єкта *`magic_fx.go`*, який зможемо створювати з магічного блока.

![Magic_fx.go](images/magic-link/linker_magic_fx.png)

Цей ігровий об’єкт містить два спрайти. Один — «магічний» колір (спрайт із зображенням *`magic-sphere_layer2.png`*), а інший — ефект світла (спрайт із зображенням *`magic-sphere_layer3.png`*). Після створення об’єкт починає обертатися залежно від значення властивості `direction`. Також налаштовуємо обробку двох повідомлень: `lights_on` і `lights_off`, які керують спрайтом світлового ефекту.

Створіть новий скрипт і додайте його як компонент-скрипт до *`magic_fx.go`*:

```lua
-- magic_fx.script
go.property("direction", hash("left"))

function init(self)
    msg.post("#", "lights_off")
    if self.direction == hash("left") then
        go.set(".", "euler.z", 0)
        go.animate(".", "euler.z", go.PLAYBACK_LOOP_FORWARD, 360,  go.EASING_LINEAR, 3 + math.random())
    else
        go.set(".", "euler.z", 0)
        go.animate(".", "euler.z", go.PLAYBACK_LOOP_FORWARD, -360,  go.EASING_LINEAR, 2 + math.random())
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("lights_on") then
        msg.post("#light", "enable")
    elseif message_id == hash("lights_off") then
        msg.post("#light", "disable")
    end
end
```

Тепер магічний блок створюватиме два ігрові об’єкти `magic_fx`, отримавши повідомлення `make_magic`. Вони обертатимуться в протилежних напрямках, створюючи гарну гру кольорів усередині блоків. Також додамо до *`block.go`* ще один спрайт із зображенням *`magic-sphere_layer4.png`*. Це зображення розміщується на вищій координаті Z, ніж створений ефект, і зображає оболонку, або «покриття», магічної сфери.

![Спрайт оболонки](images/magic-link/linker_cover.png)

Зауважте, що до ігрового об’єкта блока потрібно додати компонент *Factory* і вказати наш ігровий об’єкт *`magic_fx.go`* у властивості *Prototype*. Скрипт блока також має обробляти повідомлення `lights_on` і `lights_off` та передавати їх створеним об’єктам. Зауважте, що створені об’єкти потрібно видаляти разом із блоком. Це робить функція `final()` блока. Усе це відбувається у *`block.script`*.

```lua
-- block.script
function init(self)
    go.set_scale_xy(0.18) -- render scaled down without changing Z

    self.fx1 = nil
    self.fx2 = nil

    msg.post("#cover", "disable")

    if self.color ~= nil then
        sprite.play_flipbook("#sprite", self.color)
    else
        msg.post("#sprite", "disable")
    end
end

function final(self)
    if self.fx1 ~= nil then
        go.delete(self.fx1)
    end

    if self.fx2 ~= nil then
        go.delete(self.fx2)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("make_magic") then
        self.color = hash("magic")
        msg.post("#cover", "enable")
        msg.post("#sprite", "enable")
        sprite.play_flipbook("#sprite", hash("magic-sphere_layer1"))

        self.fx1 = factory.create("#fxfactory", p, nil, { direction = hash("left") })
        self.fx2 = factory.create("#fxfactory", p, nil, { direction = hash("right") })

        go.set_parent(self.fx1, go.get_id())
        go.set_parent(self.fx2, go.get_id())

        go.set(self.fx1, "position.z", 0.01)
        go.set(self.fx1, "scale.xy", 1)
        go.set(self.fx2, "position.z", 0.02)
        go.set(self.fx2, "scale.xy", 1)
    elseif message_id == hash("lights_on") or message_id == hash("lights_off") then
        msg.post(self.fx1, message_id)
        msg.post(self.fx2, message_id)
    end
end
```

Тепер ми можемо створювати магічні блоки й підсвічувати їх. Цим ефектом ми показуватимемо, що магічний блок розташований поруч з іншим магічним блоком.

![Магічний блок без підсвічування та з ним](images/magic-link/linker_magic_blocks.png)

Тепер потрібно змінити код заповнення поля блоками, щоб на ньому з’явилися й магічні блоки:

```lua
-- board.script
local function build_board(self)

    ...

    -- Distribute magic blocks.
    local rand_x = 0
    local rand_y
    for y = 0, boardheight - 1, boardheight / self.num_magic do
        local set = false
        while not set do
            rand_y = math.random(math.floor(y), math.min(boardheight - 1, math.floor(y + boardheight / self.num_magic)))
            rand_x = math.random(0, boardwidth - 1)
            if self.board[rand_x][rand_y].color ~= hash("magic") then
                msg.post(self.board[rand_x][rand_y].id, "make_magic")
                self.board[rand_x][rand_y].color = hash("magic")
                set = true
            end
        end
    end

    -- Build 1d list that we can easily filter.
    build_blocklist(self)
end
```

Основна механіка магічних блоків — здатність зсуватися вбік, коли поруч зникає інший блок. Усі деталі цієї механіки реалізуємо у функції `slide_magic_blocks()` у *board.script*. Алгоритм простий:

1. Для кожного рядка поля створіть список `M` магічних блоків.
2. Обходьте всі магічні блоки в списку `M`, доки список не перестане зменшуватися. На кожній ітерації:
    1. Якщо під магічним блоком є клітинка зі значенням `hash("removing")`, просто видаліть його зі списку `M`.
    2. Якщо збоку від магічного блока є порожнє місце, позначене `hash("removing")`, зсуньте його туди, встановіть для попередньої клітинки `hash("removing")`, а потім видаліть його зі списку `M`.

```lua
-- board.script
-- Apply the shifting logic to magic blocks. Only slide to positions
-- marked for removal with hash("removing")
--
local function slide_magic_blocks(self)
    -- Slide all magic blocks to the side that should slide first.
    -- This works best going row by row!
    local row_m
    for y = 0,boardheight - 1 do
        row_m = {}
        -- Build list of magic blocks on this row.
        for x = 0,boardwidth - 1 do
            if self.board[x][y] ~= nil and self.board[x][y] ~= hash("removing") and self.board[x][y].color == hash("magic") then
                table.insert(row_m, self.board[x][y])
            end
        end

        local mc = #row_m + 1
        -- Go through list, slide and remove if possible. Reiterate until the list does not shrink.
        while #row_m < mc do
            mc = #row_m
            for i, m in pairs(row_m) do
                local x = m.x
                if y > 0 and self.board[x][y-1] == hash("removing") then
                    -- Hole below, do nothing.
                    row_m[i] = nil
                elseif x > 0 and self.board[x-1][y] == hash("removing") then
                    -- Hole to the left! Slide magic block there
                    self.board[x-1][y] = self.board[x][y]
                    self.board[x-1][y].x = x - 1
                    go.animate(self.board[x][y].id, "position.x", go.PLAYBACK_ONCE_FORWARD, edge + blocksize / 2 + blocksize * (x - 1), go.EASING_OUTBOUNCE, 0.3)
                    -- Calc new z
                    go.set(self.board[x][y].id, "position.z", (x - 1) * -0.1 + y * 0.01)
                    self.board[x][y] = hash("removing") -- Will be nilled later
                    row_m[i] = nil
                elseif x < boardwidth - 1 and self.board[x + 1][y] == hash("removing") then
                    -- Hole to the right. Slide magic block there
                    self.board[x+1][y] = self.board[x][y]
                    self.board[x+1][y].x = x + 1
                    go.animate(self.board[x+1][y].id, "position.x", go.PLAYBACK_ONCE_FORWARD, edge + blocksize / 2 + blocksize * (x + 1), go.EASING_OUTBOUNCE, 0.3)
                    -- Calc new z
                    go.set(self.board[x+1][y].id, "position.z", (x + 1) * -0.1 + y * 0.01)
                    self.board[x][y] = hash("removing") -- Will be nilled later
                    row_m[i] = nil
                end
            end
        end
    end
end
```

Можна випробувати механіку, додавши виклик функції в `on_input()`:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        if #self.chain > 1 then
            -- There is a chain of blocks. Remove it from board
            remove_chain(self)
            slide_magic_blocks(self)
            nilremoved(self)
            -- Slide remaining blocks down.
            slide_board(self)
        end
        self.chain = {}
        -- Empty chain clears connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

Тепер зрозуміло, навіщо ми використовували проміжну «позначку» `hash("removing")` для клітинок під час видалення блоків. Без неї магічні блоки зсувалися б туди-сюди в будь-яке порожнє місце збоку. Можливо, це цікава механіка, але для цієї невеликої гри задумано іншу.

Тепер потрібна логіка, яка визначатиме, чи з’єднані магічні блоки (чи стоять вони ліворуч, праворуч, угорі або внизу один від одного). Також потрібно знати, чи з’єднані всі магічні блоки на полі. Алгоритм досить простий:

1. Створіть список `M` усіх магічних блоків на полі.
2. Для кожного блока в списку `M`:
    1. Якщо для блока не встановлено `region`, призначте йому номер області `R` (спочатку `1`).
    2. Позначте всіх непозначених сусідів блока тим самим номером області `R` і перейдіть до їхніх сусідів, сусідів їхніх сусідів тощо.
    3. Збільште номер області `R` на `1`.

![Позначення областей](images/magic-link/linker_regions.png)

Ось реалізація алгоритму:

```lua
-- board.script
--
-- Build list of all current magic blocks.
--
local function magic_blocks(self)
    local magic = {}
    for x = 0,boardwidth - 1 do
        for y = 0,boardheight - 1 do
            if self.board[x][y] ~= nil and self.board[x][y].color == hash("magic") then
                table.insert(magic, self.board[x][y])
            end
        end
    end
    return magic
end

--
-- Filter out adjacent magic blocks
--
local function adjacent_magic_blocks(blocks, block)
    return filter(function (e)
        return (block.x == e.x and math.abs(block.y - e.y) == 1) or
            (block.y == e.y and math.abs(block.x - e.x) == 1)
    end, blocks)
end

--
-- Spread region to neighbors
--
local function mark_neighbors(blocks, block, region)
    local neighbors = adjacent_magic_blocks(blocks, block)
    for i, m in pairs(neighbors) do
        if m.region == nil then
            m.region = region
            mark_neighbors(blocks, m, region)
        end
    end
end

--
-- Mark all magic block regions
--
local function mark_magic_regions(self)
    local m_blocks = magic_blocks(self)
    -- 1. Clear all region marks and count neighbors
    for i, m in pairs(m_blocks) do
        m.region = nil
        local n = 0
        for _ in pairs(adjacent_magic_blocks(m_blocks, m)) do n = n + 1 end
        m.neighbors = n
    end

    -- 2. Assign regions and spread them
    local region = 1
    for i, m in pairs(m_blocks) do
        if m.region == nil then
            m.region = region
            mark_neighbors(m_blocks, m, region)
            region = region + 1
        end
    end
    return m_blocks
end
```

Також створимо функції, які дадуть змогу підрахувати кількість областей серед магічних блоків. Якщо кількість областей дорівнює 1, ми знаємо, що всі магічні блоки з’єднані. Крім того, додамо функцію, яка вимикає підсвічування всіх магічних блоків, і функцію, яка вмикає світлові ефекти в магічних блоках із сусідніми магічними блоками:

```lua
-- board.script
--
-- Count the number of connected regions among the magic blocks.
--
local function count_magic_regions(blocks)
    local maxr = 0
    for i, m in pairs(blocks) do
        if m.region > maxr then
            maxr = m.region
        end
    end
    return maxr
end

--
-- Shut off lights on all listed magic blocks
--
local function shutdown_lined_up_magic(self)
    for i, m in ipairs(self.lined_up_magic) do
        msg.post(m.id, "lights_off")
    end
end

--
-- Set highlight for all magic blocks
--
local function highlight_magic(blocks)
    for i, m in pairs(blocks) do
        if m.neighbors > 0 then
            msg.post(m.id, "lights_on")
        else
            msg.post(m.id, "lights_off")
        end
    end
end
```

Тепер можна додати ці частини логіки до загального процесу. По-перше, оскільки поле генерується випадково, існує невелика ймовірність, що воно відразу опиниться у виграшному стані. Якщо так станеться, просто відкинемо це поле й побудуємо його заново:

```lua
-- board.script
--
-- Clear the board
--
local function clear_board(self)
    for y = 0,boardheight - 1 do
        for x = 0,boardwidth - 1 do
            if self.board[x][y] ~= nil then
                go.delete(self.board[x][y].id)
                self.board[x][y] = nil
            end
        end
    end
end

local function build_board(self)

    ...

    -- Build 1d list that we can easily filter.
    build_blocklist(self)

    local magic_blocks = mark_magic_regions(self)
    if count_magic_regions(magic_blocks) == 1 then
        -- "Win" from start. Make new board.
        clear_board(self)
        build_board(self)
    end
    highlight_magic(magic_blocks)
end
```

Решта логіки вміщується в `on_input()`. Коду для обробки повідомлення `level_completed` поки що немає, але на цьому етапі це нормально:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        if #self.chain > 1 then
            -- There is a chain of blocks. Remove it from board and refill board.
            remove_chain(self)
            slide_magic_blocks(self)
            nilremoved(self)
            -- Slide remaining blocks down.
            slide_board(self)

            local magic_blocks = mark_magic_regions(self)
            -- Highlight adjacent magic blocks.
            if count_magic_regions(magic_blocks) == 1 then
                -- Win!
                msg.post("#", "level_completed")
            end
            highlight_magic(magic_blocks)
        end
        self.chain = {}
        -- Empty chain clears connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

Тепер можна грати й досягати виграшного стану, хоча після з’єднання всіх магічних блоків поки що нічого не відбувається.

![Перша перемога](images/magic-link/linker_first_win.png)

## Скидання блоків {#drops}

Ідея «скидання» — додати просту механіку поступу в грі. Натискаючи кнопку *DROP*, гравець може виконати обмежену кількість скидань: кілька нових випадкових блоків просто падають згори на поле. На початку гравець має одне скидання, а за кожен пройдений рівень отримує ще одне. Код механіки скидання вміщується у двох функціях. Одна повертає список можливих місць приземлення блоків, а друга виконує саме скидання разом з анімацією та всім іншим.

```lua
-- board.script
--
-- Find spots for a drop.
--
local function dropspots(self)
    local spots = {}
    for x = 0, boardwidth - 1 do
        for y = 0, boardheight - 1 do
            if self.board[x][y] == nil then
                table.insert(spots, { x = x, y = y })
                break
            end
        end
    end
    -- If more than dropamount, randomly remove a slot until dropamount
    for c = 1, #spots - dropamount do
        table.remove(spots, math.random(#spots))
    end
    return spots
end

--
-- Perform the drop
--
local function drop(self, spots)
    for i, s in pairs(spots) do
        local pos = vmath.vector3()
        pos.x = edge + blocksize / 2 + blocksize * s.x
        pos.y = 1000
        c = colors[math.random(#colors)]    -- Pick a random color
        local id = factory.create("#blockfactory", pos, null, { color = c })
        go.animate(id, "position.y", go.PLAYBACK_ONCE_FORWARD, bottom_edge + blocksize / 2 + blocksize * s.y, go.EASING_OUTBOUNCE, 0.5)
        -- Calc new z
        go.set(id, "position.z", s.x * -0.1 + s.y * 0.01)

        self.board[s.x][s.y] = { id = id, color = c,  x = s.x, y = s.y }
    end

    -- Rebuild blocklist
    build_blocklist(self)
end
```

Щоб перевірити скидання, можна виконати наведений нижче код, наприклад, у `on_reload()` або прив’язати його до тимчасової дії введення:

```lua
s = dropspots(self)
if #s > 0 then
    -- Do the drop
    drop(self, s)
end
```

![Скидання блоків](images/magic-link/linker_drop.png)

## Головне меню {#the-main-menu}

Час зібрати все докупи. Насамперед створимо стартовий екран і відокремимо його від поля. Перший крок — створити *main_menu.gui* й додати до нього кнопку *Start* (текстовий вузол і вузол Box із текстурою), текстовий вузол заголовка та кілька декоративних блоків (вузли Box із текстурами). Скрипт *main_menu.gui_script*, який ми приєднуємо до GUI, анімує декоративні блоки в `init()`. Він також містить `on_input()`, що надсилає повідомлення `start_game` головному скрипту. Цей скрипт створимо трохи згодом.

![GUI головного меню](images/magic-link/linker_main_menu.png)

```lua
-- main_menu.gui_script
function init(self)
    msg.post(".", "acquire_input_focus")

    local bs = { "brick1", "brick2", "brick3", "brick4", "brick5", "brick6" }
    for i, b in ipairs(bs) do
        local n = gui.get_node(b)
        local rt = (math.random() * 3) + 1
        local a = math.random(-45, 45)
        gui.set_color(n, vmath.vector4(1, 1, 1, 0))

        gui.animate(n, "position.y", -100 - math.random(0, 50), gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
        gui.animate(n, "color.w", 1, gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
        gui.animate(n, "rotation.z", a, gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
    end

    gui.animate(gui.get_node("start"), "color.x", 1, gui.EASING_INOUTSINE, 1, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local start = gui.get_node("start")

        if gui.pick_node(start, action.x, action.y) then
            msg.post("/main#script", "start_game")
        end
    end
end
```

Оскільки невдовзі за запуск гри відповідатиме скрипт головного меню, видаліть тимчасовий виклик налаштування поля з `init()` у *board.script*:

```lua
-- board.script
--
-- INIT
--
function init(self)
    self.board = {}                -- Contains the board structure
    self.blocks = {}            -- List of all blocks. Used for easy filtering on selection.

    self.chain = {}                -- Current selection chain
    self.connectors = {}        -- Connector elements to mark the selection chain
    self.num_magic = 3            -- Number of magic blocks on the board

    self.drops = 1                -- Number of drops you have available

    self.magic_blocks = {}        -- Magic blocks that are lined up

    self.dragging = false        -- Drag touch input
end
```

Головний скрипт зберігатиме загальний стан гри й запускатиме її за запитом. Тут ми хочемо, щоб *main.collection* містила лише мінімальний набір ресурсів, потрібних для відображення під час запуску. Для цього *main.collection* міститиме ігровий об’єкт «main» із GUI головного меню, компонентом-скриптом і, найголовніше, компонентом *Collection Proxy*.

Проксі колекції (collection proxy) дає змогу динамічно завантажувати й вивантажувати колекції в запущеній грі. Він діє від імені вказаного файлу колекції, а ми завантажуємо, ініціалізуємо, вмикаємо, вимикаємо й вивантажуємо динамічну колекцію, надсилаючи повідомлення проксі. Повний опис використання наведено в [документації проксі колекції](/manuals/collection-proxy).

У нашому випадку встановлюємо властивість *Collection* компонента проксі колекції на *board.collection*, яка містить «рівень».

![Головна колекція](images/magic-link/linker_main_collection.png)

Тепер відкрийте *game.project* і змініть стартову *main_collection* на `/main/main.collectionc`.

![Головна колекція як стартова](images/magic-link/linker_bootstrap_main.png)

Тепер початок гри означає надсилання повідомлень проксі колекції для завантаження, ініціалізації та ввімкнення поля, а потім вимкнення головного меню, щоб приховати його. Повернення до головного меню виконує зворотні дії (за умови, що проксі завантажив колекцію).

```lua
-- main.script
function init(self)
    msg.post("#", "to_main_menu")
    self.state = "MAIN_MENU"
end

function on_message(self, message_id, message, sender)
    if message_id == hash("to_main_menu") then
        if self.state ~= "MAIN_MENU" then
            msg.post("#boardproxy", "unload")
        end
        msg.post("main:/main#menu", "enable") -- <1>
        self.state = "MAIN_MENU"
    elseif message_id == hash("start_game") then
        msg.post("#boardproxy", "load")
        msg.post("#menu", "disable")
    elseif message_id == hash("proxy_loaded") then
        -- Board collection has loaded...
        msg.post(sender, "init")
        msg.post("board:/board#script", "start_level", { difficulty = 1 }) -- <2>
        msg.post(sender, "enable")
        self.state = "GAME_RUNNING"
    end
end
```
1. Зауважте, що ми називаємо сокет «main», тому потрібно переконатися, що таку назву встановлено для *main.collection*. Виберіть кореневий вузол і перевірте, що властивість *Name* має значення «main».
2. Аналогічно ми надсилаємо повідомлення до завантаженої колекції через її сокет, назву якого задано властивістю *Name* у колекції.

## GUI під час гри {#the-in-game-gui}

Перш ніж додавати останню частину логіки до скрипту поля, потрібно додати до поля набір елементів GUI. Спочатку над полем додамо кнопки *RESTART* і *DROP*.

![GUI поля](images/magic-link/linker_board_gui.png)

Скрипт GUI поля надсилає повідомлення діалоговому елементу GUI перезапуску після натискання та самому скрипту поля після натискання *DROP*:

```lua
-- board.gui_script
function init(self)
    msg.post("#", "show")
    msg.post("/restart#gui", "hide")
    msg.post("/level_complete#gui", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
    elseif message_id == hash("set_drop_counter") then
        local n = gui.get_node("drop_counter")
        gui.set_text(n, message.drops .. " x")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local restart = gui.get_node("restart")
        local drop = gui.get_node("drop")

        if gui.pick_node(restart, action.x, action.y) then
            -- Show the restart dialog box.
            msg.post("/restart#gui", "show")
            msg.post("#", "hide")
        elseif gui.pick_node(drop, action.x, action.y) then
            msg.post("/board#script", "drop")
        end
    end
end
```

Діалогове вікно *RESTART* просте. Створимо його як *restart.gui* й приєднаємо простий скрипт: він нічого не робить, якщо гравець натискає *NO*, надсилає повідомлення `restart_level` скрипту поля після натискання *YES* і повідомлення `to_main_menu` головному скрипту після натискання *Quit to main menu*:

![GUI перезапуску](images/magic-link/linker_restart_gui.png)

```lua
-- restart.gui_script
function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
        msg.post(".", "release_input_focus")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
        msg.post(".", "acquire_input_focus")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local yes = gui.get_node("yes")
        local no = gui.get_node("no")
        local quit = gui.get_node("quit")

        if gui.pick_node(no, action.x, action.y) then
            msg.post("#", "hide")
            msg.post("/board#gui", "show")
        elseif gui.pick_node(yes, action.x, action.y) then
            msg.post("board:/board#script", "restart_level")
            msg.post("/board#gui", "show")
            msg.post("#", "hide")
        elseif gui.pick_node(quit, action.x, action.y) then
            msg.post("main:/main#script", "to_main_menu")
            msg.post("#", "hide")
        end
    end
    -- Consume all input until we're gone.
    return true
end
```

Також створимо просте діалогове вікно GUI завершення рівня у *level_complete.gui* із простим скриптом, який надсилає повідомлення `next_level` скрипту поля, коли гравець натискає *CONTINUE*:

![Діалогове вікно завершення рівня](images/magic-link/linker_level_complete_gui.png)

```lua
-- level_complete.gui_script
function init(self)
    msg.post("#", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
        msg.post(".", "release_input_focus")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
        msg.post(".", "acquire_input_focus")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local continue = gui.get_node("continue")

        if gui.pick_node(continue, action.x, action.y) then
            msg.post("board#script", "next_level")
            msg.post("#", "hide")
        end
    end
    -- Consume all input until we're gone.
    return true
end
```

Діалогове вікно для представлення поточного рівня має скрипт, який лише приховує та показує це вікно. Під час показу текст вікна встановлюється на повідомлення з поточним рівнем складності:

![GUI представлення рівня](images/magic-link/linker_present_level_gui.png)

```lua
-- present_level.gui_script
function init(self)
    msg.post("#", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        local n = gui.get_node("message")
        gui.set_text(n, "Level " .. message.level)
        msg.post("#", "enable")
    end
end
```

Також додамо діалогове вікно, яке з’являється, коли гравець намагається скинути блоки, але для них немає місця.

![GUI браку місця для скидання](images/magic-link/linker_no_drop_room_gui.png)

```lua
-- no_drop_room.gui_script
function init(self)
    msg.post("#", "hide")
    self.t = 0
end

function update(self, dt)
    if self.t < 0 then
        msg.post("#", "hide")
    else
        self.t = self.t - dt
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        self.t = 1
        msg.post("#", "enable")
    end
end
```

Насамкінець додамо ці компоненти GUI до *board.collection* і потрібний код до *board.script*:

![Остаточна колекція поля](images/magic-link/linker_board_collection_final.png)

У `on_message()` потрібен код для всіх повідомлень, які надсилаються до поля й від нього.

`start_level`
: Встановіть кількість магічних блоків відповідно до параметра складності, побудуйте поле й покажіть діалогове вікно GUI «present_level» на 2 секунди перед початком гри (приховуванням вікна й отриманням фокуса введення). Зауважте, що ми використовуємо `go.animate()` як таймер, анімуючи значення «timer», яке більше ніде не використовується.

`restart_level`
: Це відбувається, коли гравець натискає кнопку GUI *RESTART* і підтверджує дію. Очистьте й заново побудуйте поле та скиньте лічильник скидань.

`level_completed`
: Надсилається, щойно поле переходить у виграшний стан. Вимкніть введення, анімуйте магічні блоки й покажіть діалогове вікно GUI «level_complete». Вікно надішле у відповідь повідомлення `next_level`, коли гравець натисне в ньому кнопку *CONTINUE*.

`next_level`
: Після отримання цього повідомлення очистьте поле, збільште лічильник скидань і надішліть `start_level` із заданим наступним рівнем складності.

`drop`
: Перевірте, де можна скинути блоки. Якщо можливих місць немає, покажіть діалогове вікно GUI «no_drop_room»; інакше виконайте скидання (якщо в гравця ще залишилися скидання), зменште лічильник скидань та оновіть його відображення.

```lua
-- board.script
function on_message(self, message_id, message, sender)
    if message_id == hash("start_level") then
        self.num_magic = message.difficulty + 1
        build_board(self)

        msg.post("#gui", "set_drop_counter", { drops = self.drops } )

        msg.post("present_level#gui", "show", { level = message.difficulty } )
        -- Wait some...
        go.animate("#", "timer", go.PLAYBACK_ONCE_FORWARD, 1, go.EASING_LINEAR, 2, 0, function ()
            msg.post("present_level#gui", "hide")
            msg.post(".", "acquire_input_focus")
        end)
    elseif message_id == hash("restart_level") then
        clear_board(self)
        build_board(self)
        self.drops = 1
        msg.post("#gui", "set_drop_counter", { drops = self.drops } )
        msg.post(".", "acquire_input_focus")
    elseif message_id == hash("level_completed") then
        -- turn off input
        msg.post(".", "release_input_focus")

        -- Animate the magic!
        for i, m in ipairs(magic_blocks(self)) do
            go.set_scale_xy(0.17, m.id)
            go.animate(m.id, "scale.xy", go.PLAYBACK_LOOP_PINGPONG, 0.19, go.EASING_INSINE, 0.5, 0)
        end

        -- Show completion screen
        msg.post("level_complete#gui", "show")
    elseif message_id == hash("next_level") then
        clear_board(self)
        self.drops = self.drops + 1
        -- Difficulty level is number of magic blocks - 1
        msg.post("#", "start_level", { difficulty = self.num_magic })
    elseif message_id == hash("drop") then
        s = dropspots(self)
        if #s == 0 then
            -- Can't perform drop
            msg.post("no_drop_room#gui", "show")
        elseif self.drops > 0 then
            -- Do the drop
            drop(self, s)
            self.drops = self.drops - 1
            msg.post("#gui", "set_drop_counter", { drops = self.drops } )
        end
    end
end
```

Ось і все! Гру та цей урок завершено! Тепер насолоджуйтеся грою!

![Завершена гра](images/magic-link/linker_game_finished.png)

## Подальші кроки {#moving-on}

Ця невелика гра має цікаві властивості, і ми заохочуємо вас експериментувати з нею. Ось список вправ, які допоможуть вам краще познайомитися з Defold:

* Зробіть взаємодію зрозумілішою. Новому гравцеві може бути складно зрозуміти, як працює гра та з чим можна взаємодіяти. Приділіть час тому, щоб зробити гру зрозумілішою, не додаючи навчальних елементів.
* Додайте звуки. Наразі гра зовсім беззвучна, і приємний музичний супровід та звуки взаємодії покращили б її.
* Автоматично визначайте закінчення гри.
* Рекорди. Додайте функцію збереження найкращого результату між запусками.
* Заново реалізуйте гру, використовуючи лише API GUI.
* Наразі з кожним підвищенням рівня у грі додається один магічний блок. Це не може тривати безкінечно. Знайдіть вдале розв’язання цієї проблеми.
* Оптимізуйте гру та зменште максимальну кількість спрайтів, використовуючи їх повторно замість видалення й повторного створення.
* Реалізуйте рендеринг гри, незалежний від роздільної здатності, щоб вона однаково добре виглядала на екранах із різною роздільною здатністю та співвідношенням сторін.
