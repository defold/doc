---
brief: Если вы новичок в Defold, это руководство поможет начать работу со скриптовой логикой и несколькими базовыми строительными блоками Defold, создав клон Snake с нуля.
layout: tutorial
title: Создание игры Snake в Defold
difficulty: Beginner
---

# Snake

В этом учебнике мы шаг за шагом создадим одну из самых классических игр, которые можно попробовать воссоздать. У этой игры существует множество вариаций; в нашей версии есть змейка, которая ест "еду" и растет только тогда, когда ее съедает. Кроме того, змейка ползает по игровому полю с препятствиями.

![thumbnail](images/snake/thumbnail.png)

### Чему вы научитесь?

В этом учебнике вы научитесь:
- создавать игру с нуля в Defold
- настраивать и обрабатывать ввод
- создавать tilemap и изменять их во время выполнения
- писать скрипты на Lua

### Примечание для начинающих

Этот учебник рассчитан на начинающих, но если вы совсем не знакомы с Defold и разработкой игр, мы рекомендуем сначала прочитать несколько вводных руководств, особенно о [структурных элементах Defold](/manuals/building-blocks/) и [глоссарий](/manuals/glossary/). Если Defold еще не установлен, загляните в [руководство по установке](/manuals/install/). Также стоит посмотреть [обзор редактора](manuals/editor/), чтобы быстрее освоиться в самом редакторе; в этом учебнике мы также приводим скриншоты для каждого шага.

## Создание проекта

Запустите Defold и:

1. Выберите *Create From* ▸ *Templates* слева.
2. Выберите *Empty Project*.
3. Введите название проекта в поле *Title*.
4. Выберите *Location* для проекта.
5. Нажмите *Create New Project*.

![start](images/snake/1.png)

<input type="checkbox"/> Готово!

## Настройки проекта

Начнем с настройки разрешения игры.

1. Когда редактор откроется, найдите файл `game.project` слева, в панели *Assets*. Дважды щелкните по нему, чтобы открыть.
2. Перейдите в раздел *Display* файла `game.project`.
3. Задайте размеры игры (`Width` и `Height`) равными 768⨉768 или другому числу, кратному 16.

![display](images/snake/2.png)

Это нужно потому, что игра будет рисоваться по сетке, где каждый сегмент имеет размер 16x16 пикселей, и тогда экран не будет обрезать частичные сегменты. Файл `game.project` содержит все важные настройки проекта — подробнее о них можно прочитать в [руководстве по настройкам проекта](/manuals/project-settings/).

<input type="checkbox"/> Готово!

## Создание новых папок в панели Assets

Для минималистичного клона Snake нужно совсем немного графики: один зеленый сегмент 16⨉16 для змейки, один белый блок для препятствий и один красный блок меньшего размера для еды.

Сначала создайте директорию для ассетов в редакторе Defold:

1. <kbd>Щелкните правой кнопкой</kbd> по папке `main`.
2. Выберите `New Folder`.
3. Появится окно с запросом имени — введите `assets` и нажмите `Create Folder`.

![new_folder](images/snake/3.png)

<input type="checkbox"/>`Готово!`

## Добавление графики в игру

Ниже находится единственный ассет, который вам понадобится:

![snake_sprites](images/snake/snake.png)

1. <kbd>Щелкните правой кнопкой</kbd> по изображению выше и сохраните его на локальный диск. Затем перетащите или скопируйте скачанное изображение в новую папку проекта, которую вы только что создали.

![new_folder](images/snake/4.png)

Подробнее об этом можно прочитать в руководстве по [импорту графики](/manuals/importing-graphics/).

<input type="checkbox"/>`Готово!`

## Добавление Tile Source

В Defold есть встроенный компонент [Tilemap](/manuals/tilemap/), который вы будете использовать для создания игрового поля из *тайлов*, выровненных по сетке. Tilemap позволяет задавать и читать отдельные тайлы, что идеально подходит для этой игры. Поскольку tilemap берет графику из [Tilesource](/manuals/tilesource/), сначала нужно создать его:

1. <kbd>Щелкните правой кнопкой</kbd> по папке `assets`.
2. Выберите `New` ▸ `Tile Source` в разделе "Resources".
3. Назовите новый файл "snake" (редактор сохранит его как `snake.tilesource`).

![new_tilesource](images/snake/5.png)

Tilesource откроется в отдельном редакторе Tilesource, и нужно будет указать для него изображение. Справа находится панель `Properties`:

4. Установите свойство `Image` на графический файл, который вы только что импортировали.
![tilesource](images/snake/6.png)

5. Свойства `Width` и `Height` должны остаться равными 16 (значение по умолчанию). Это разделит изображение 32⨉32 пикселя на 4 тайла с номерами 1–4.

![tilesource_properties](images/snake/7.png)

Обратите внимание, что свойство *Extrude Borders* установлено в 2 пикселя. Это нужно, чтобы избежать визуальных артефактов вокруг тайлов, у которых графика доходит до самого края.

Если вы измените файл, рядом с его именем на вкладке появится звездочка `*`. Выберите `File` ▸ `Save All` или используйте сочетание <kbd>Ctrl</kbd>+<kbd>S</kbd> (<kbd>⌘Cmd</kbd> + <kbd>S</kbd> на Mac), чтобы сохранить все файлы.

<input type="checkbox"/> Готово!

## Создание tilemap игрового поля

Теперь у вас есть tilesource, готовый к использованию, и можно создать компонент tilemap для игрового поля:

1. <kbd>Щелкните правой кнопкой</kbd> по папке `main` и выберите <kbd>New</kbd> ▸ <kbd>Tile Map</kbd> в разделе "Components". Назовите новый файл "grid" (редактор сохранит его как "grid.tilemap").
![add_tilemap](images/snake/8.png)

2. Файл откроется в редакторе Tilemap, который покажет, что ему нужен **Tile Source**. Установите свойство *Tile Source* на ранее созданный "snake.tilesource".
![set_tilesource](images/snake/9.png)

<input type="checkbox"/> Готово!

## Рисование тайлов в tilemap

Defold хранит только реально используемую область tilemap, поэтому нужно добавить достаточно тайлов, чтобы заполнить границы экрана.

1. Выберите слой `layer1` в панели `Outline` справа.
2. Выберите пункт меню `Edit` ▸ `Select Tile...` или нажмите <kbd>Space</kbd>, чтобы открыть палитру тайлов, затем щелкните по тайлу, которым хотите рисовать.
![tilemap](images/snake/10.png)

3. Нарисуйте рамку по краю экрана и несколько препятствий.
![tilemap_final](images/snake/11.png)

Вам понадобится tilemap размером 48x48 тайлов, потому что размер экрана равен 768, размер тайла — 16 пикселей, а 768/16 = 48.

Когда закончите, сохраните tilemap.

<input type="checkbox"/> Готово!

## Добавление tilemap в игру

Теперь нужно добавить tilemap в игру. Если вы знакомы со структурными элементами Defold, то знаете, что компоненты входят в игровые объекты, а игровые объекты могут быть описаны в коллекциях.

1. Откройте `main.collection`, дважды щелкнув по нему в панели `Assets`. В шаблоне Empty Project это bootstrap-коллекция, которая загружается при старте движка.

2. <kbd>Щелкните правой кнопкой</kbd> по корню в `Outline` и выберите `Add Game Object`. Так вы создадите новый игровой объект в коллекции, которая загружается при запуске игры.
![add_game_object](images/snake/12.png)

3. <kbd>Щелкните правой кнопкой</kbd> по новому игровому объекту и выберите `Add Component File`. Выберите файл "grid.tilemap", который вы только что создали.
![add_component](images/snake/13.png)

Теперь в игровой коллекции есть tilemap. Он должен быть виден, если запустить игру из редактора.

1. Выберите `Project` ▸ `Build` или используйте сочетание <kbd>Ctrl</kbd> + <kbd>B</kbd> (<kbd>⌘Cmd</kbd> + <kbd>B</kbd> на Mac).

![run_game](images/snake/14.png)

<input type="checkbox"/> Готово!

## Добавление скрипта в игру

1. <kbd>Щелкните правой кнопкой</kbd> по папке `main` в браузере `Assets` и выберите `New` ▸ `Script` в разделе Scripts. Назовите новый файл скрипта "snake" (он будет сохранен как "snake.script"). В этом файле будет вся игровая логика.
![add_script](images/snake/15.png)

2. Вернитесь к *main.collection* и <kbd>щелкните правой кнопкой</kbd> по игровому объекту с tilemap. Выберите <kbd>Add&nbsp;Component&nbsp;File</kbd> и укажите файл "snake.script".

![main _ollection](images/snake/16.png)

Теперь tilemap и скрипт на месте.

<input type="checkbox"/> Готово!

## Игровой скрипт

Скрипт, который вы будете писать, будет управлять всей игрой. Мы будем добавлять возможности одну за другой.

### Простой алгоритм движения

Идея работы будет такой:

1. Скрипт хранит список позиций тайлов, которые в данный момент занимает змейка.
2. Если игрок нажимает клавишу направления, сохраняется направление, в котором должна двигаться змейка.
3. Через регулярный интервал змейка делает один шаг в текущем направлении.

### Инициализация

Откройте *snake.script* и найдите функцию `init()`. Эта функция вызывается движком при инициализации скрипта во время запуска игры. Замените код на следующий:

```lua
function init(self)
    self.segments = { -- <1>
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0} -- <2>
    self.speed = 7.0 -- <3>
    self.time = 0 -- <4>
end
```

В этом коде мы:

1. Сохраняем сегменты змейки как Lua-таблицу `self.segments`, содержащую список таблиц, каждая из которых хранит позицию X и Y одного сегмента.
2. Сохраняем текущее направление как таблицу `self.dir` с направлением по X и Y.
3. Сохраняем текущую скорость движения в `self.speed`, выраженную в тайлах в секунду.
4. Сохраняем значение таймера в `self.time`, которое будет использоваться для отслеживания скорости движения.

Код выше написан на языке Lua. В нем есть несколько важных моментов, но если вы пока не все понимаете, не переживайте. Продолжайте, экспериментируйте и дайте себе время — постепенно все станет понятнее. Сейчас достаточно запомнить, что в `init()` мы инициализировали переменные, которые будем использовать.

- Defold резервирует набор встроенных callback-*functions*, которые вызываются в течение жизненного цикла script component. Это *не* методы, а обычные функции.
- Runtime передает ссылку на текущий экземпляр script component через параметр `self`. Ссылка `self` используется для хранения данных экземпляра.
- Ссылку `self` можно использовать как Lua-таблицу для хранения данных. Просто используйте точечную нотацию, как с любой другой таблицей: `self.data = "value"`. Эта ссылка действительна на протяжении всего времени жизни скрипта, в данном случае — с запуска игры до выхода из нее.
- Литералы Lua-таблиц записываются в фигурных скобках `{}`.
- Записи таблицы могут быть парами ключ/значение (`{x = 10, y = 20}`), вложенными Lua-таблицами (`{ {a = 1}, {b = 2} }`) или данными других типов.

<input type="checkbox"/> Готово!

### Update

Функция `init()` вызывается ровно один раз, когда script component создается в работающей игре. Функция `update()`, напротив, вызывается **каждый кадр**, то есть по умолчанию 60 раз в секунду. Поэтому она идеально подходит для игровой логики в реальном времени.

Идея обновления такая: через заданный интервал выполнить следующее:

1. Найти, где находится голова змейки, затем создать новую голову в соседней позиции со смещением по текущему направлению движения. Например, если змейка движется с X=1 и Y=0, а текущая голова находится в X=0 и Y=0, новая голова должна оказаться в X=1 и Y=0.
2. Сохранить позицию новой головы в списке сегментов, из которых состоит змейка.
3. Получить позицию хвоста из таблицы сегментов.
4. Очистить тайл хвоста в этой позиции.
5. Нарисовать все сегменты змейки (тайлы) в позициях из таблицы.

![algorithm](images/snake/17.png)

:::sidenote
Помните, что голова змейки находится в конце таблицы, а хвост — в начале.
:::

1. Найдите функцию `update()` в *snake.script* и замените код на следующий:

```lua
function update(self, dt)
    self.time = self.time + dt -- <1>
    if self.time >= 1.0 / self.speed then -- <2>
        local head = self.segments[#self.segments] -- <3>

        local newhead = {
            x = head.x + self.dir.x,
            y = head.y + self.dir.y
        } -- <4>

        table.insert(self.segments, newhead) -- <5>

        local tail = table.remove(self.segments, 1) -- <6>

        tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 0) -- <7>

        for i, s in ipairs(self.segments) do -- <8>
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2) -- <9>
        end

        self.time = 0 -- <10>
    end
end
```

В этом коде мы:

1. Продвигаем таймер на время в секундах, прошедшее с прошлого вызова `update()`, то есть на "delta time" или `dt`.
2. Проверяем, накопил ли таймер достаточно времени.
3. Получаем текущую позицию головы. `#` — оператор получения длины таблицы, если она используется как массив; в нашем случае это так, потому что все сегменты — значения таблицы без явно заданных ключей.
4. Создаем новый сегмент головы на основе текущей позиции головы и направления движения (`self.dir`).
5. Добавляем новую голову в конец таблицы сегментов.
6. Извлекаем хвост из начала таблицы сегментов.
7. Очищаем тайл в позиции удаленного хвоста. У нашей tilemap `#grid` только один слой с именем `layer1`.
8. Проходим по элементам таблицы сегментов. На каждой итерации `i` содержит позицию в таблице, начиная с 1, а `s` — текущий сегмент.
9. Устанавливаем тайл в позиции сегмента в значение 2, то есть тайл зеленого цвета змейки.
10. После завершения сбрасываем таймер в ноль.

Если сейчас запустить игру, вы увидите, как змейка длиной 4 сегмента ползет слева направо по игровому полю.

![run the game](images/snake/snake_run_1.png)

<input type="checkbox"/> Готово!

## Ввод игрока

Прежде чем добавить код для реакции на ввод игрока, нужно настроить input connections.

### Привязки ввода

1. Найдите в папке `input` файл `game.input_binding` и <kbd>дважды щелкните</kbd> по нему, чтобы открыть.
2. Добавьте набор привязок *Key Trigger* для движения вверх, вниз, влево и вправо. В колонке *Input* выберите клавиши клавиатуры, а в колонке *Action* введите имена действий.

![input](images/snake/18.png)

Файл input binding сопоставляет реальный пользовательский ввод (клавиши, движения мыши и т. д.) с *именами* действий, которые затем передаются скриптам, запросившим ввод.

<input type="checkbox"/> Готово!

### Получение фокуса ввода

Когда привязки готовы, откройте *snake.script* и добавьте следующую строку в начало функции `init()`:

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.speed = 7.0
    self.time = 0
end
```

Добавленная строка:
1. Отправляет сообщение текущему игровому объекту ("." — сокращение для текущего игрового объекта), чтобы он начал получать ввод от движка.

Затем найдите функцию `on_input` и введите следующий код:

```lua
function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then -- <1>
        self.dir.x = 0 -- <2>
        self.dir.y = 1
    elseif action_id == hash("down") and action.pressed then
        self.dir.x = 0
        self.dir.y = -1
    elseif action_id == hash("left") and action.pressed then
        self.dir.x = -1
        self.dir.y = 0
    elseif action_id == hash("right") and action.pressed then
        self.dir.x = 1
        self.dir.y = 0
    end
end
```

Эти ветки `if...elseif...` делают следующее:
1. Если получено действие "up", как задано в input bindings, и в таблице `action` поле `pressed` равно `true` (игрок нажал клавишу), то:
2. Устанавливают направление движения.

Снова запустите игру и проверьте, что змейкой можно управлять.

<input type="checkbox"/> Готово!

### Улучшение обработки ввода

Теперь обратите внимание: если нажать две клавиши одновременно, это приведет к двум вызовам `on_input()`, по одному на каждое нажатие. В приведенном выше коде на направление змейки повлияет только последний вызов, потому что последующие вызовы `on_input()` перезаписывают значения в `self.dir`.

Также заметьте, что если змейка движется влево и вы нажмете <kbd>right</kbd>, она повернет в себя. *На первый взгляд* очевидное исправление — добавить дополнительные условия в ветки `if` функции `on_input()`:

```lua
if action_id == hash("up") and self.dir.y ~= -1 and action.pressed then
    ...
elseif action_id == hash("down") and self.dir.y ~= 1 and action.pressed then
    ...
```

Однако если змейка движется влево, а игрок *быстро* нажимает сначала <kbd>up</kbd>, а затем <kbd>right</kbd> до следующего шага змейки, сработает только нажатие <kbd>right</kbd>, и змейка все равно повернет в себя. С условиями в `if`, показанными выше, ввод будет проигнорирован. *Плохо!*

Правильное решение — хранить ввод в очереди и извлекать элементы из этой очереди по мере движения змейки:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.speed = 7.0
    self.time = 0

    self.dirqueue = {} -- <1>
end
```

На этот раз мы:
1. Добавили переменную `self.dirqueue`, инициализированную пустой таблицей.

В функцию `update()` добавьте:

```lua
function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed then
        local newdir = table.remove(self.dirqueue, 1) -- <1>
        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y -- <2>
            if not opposite then
                self.dir = newdir -- <3>
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tail = table.remove(self.segments, 1)
        tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 0)

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)
        end

        self.time = 0
    end
end
```

1. Извлекаем первый элемент из очереди направлений.
2. Если элемент есть (`newdir` не null), проверяем, направлен ли он противоположно `self.dir`.
3. Устанавливаем новое направление только если оно не противоположно текущему.

И измените `on_input`, чтобы сохранять текущий ввод в очередь:

```lua
function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = 1}) -- <1>
    elseif action_id == hash("down") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = -1})
    elseif action_id == hash("left") and action.pressed then
        table.insert(self.dirqueue, {x = -1, y = 0})
    elseif action_id == hash("right") and action.pressed then
        table.insert(self.dirqueue, {x = 1, y = 0})
    end
end
```

1. Добавляем направление ввода в очередь направлений вместо прямой записи в `self.dir`.

Запустите игру и проверьте, что она работает как ожидается.

<input type="checkbox"/> Готово!

## Еда и столкновения с препятствиями

Змейке нужна еда на карте, чтобы она могла становиться длиннее и быстрее. Добавим ее!

### Размещение еды

Над функцией `init()` добавьте новую функцию:

```lua
local function put_food(self) -- <1>
    self.food = {x = math.random(2, 47), y = math.random(2, 47)} -- <2>
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3) -- <3>
end
```

В этой функции мы:
1. Объявляем новую функцию `put_food()`, которая размещает еду на карте.
2. Сохраняем случайные X и Y в переменной `self.food`.
3. Устанавливаем тайл в позиции X и Y в значение 3, то есть тайл с графикой еды.

Затем вызовите ее в конце функции `init()`:
```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    math.randomseed(socket.gettime()) -- <1>
    put_food(self) -- <2>
end
```

1. Перед использованием `math.random()` задаем seed генератора случайных чисел, иначе будет генерироваться одна и та же последовательность случайных значений. Этот seed нужно задать только один раз.
2. Вызываем функцию `put_food()` при старте игры, чтобы игрок начинал с одним кусочком еды на карте.

<input type="checkbox"/> Готово!

### Поедание еды

Теперь определение столкновения змейки с чем-либо сводится к проверке того, что находится в tilemap там, куда движется змейка, и реакции на это.

Добавьте переменную, которая отслеживает, жива ли змейка:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    self.alive = true -- <1>

    math.randomseed(socket.gettime())
    put_food(self)
end
```

1. Флаг, который показывает, жива ли змейка.

Затем добавьте логику проверки столкновений со стеной/препятствием и едой:

```lua
function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed and self.alive then -- <1>
        local newdir = table.remove(self.dirqueue, 1)

        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y
            if not opposite then
                self.dir = newdir
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tile = tilemap.get_tile("#grid", "layer1", newhead.x, newhead.y) -- <2>

        if tile == 2 or tile == 4 then
            self.alive = false -- <3>
        elseif tile == 3 then
            self.speed = self.speed + 1 -- <4>
            put_food(self)
        else
            local tail = table.remove(self.segments, 1) -- <5>
            tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 1)
        end

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)            
        end

        self.time = 0
    end
end
```

1. Продвигаем змейку только если она жива.
2. Перед рисованием в tilemap считываем, что находится в позиции, куда должна прийти новая голова змейки.
3. Если тайл — препятствие или другая часть змейки, игра окончена.
4. Если тайл — еда, увеличиваем скорость и размещаем новую еду.
5. Обратите внимание: хвост удаляется только если столкновения не было. Это значит, что при поедании еды змейка вырастет на один сегмент, потому что в этот ход хвост не удаляется.

Теперь попробуйте игру и убедитесь, что она работает хорошо!

На этом учебник заканчивается, но продолжайте экспериментировать с игрой и попробуйте выполнить упражнения ниже.

<input type="checkbox"/> Готово!

## Полный скрипт

Вот полный код скрипта для справки:

```lua
local function put_food(self)
    self.food = {x = math.random(2, 47), y = math.random(2, 47)}
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3)        
end

function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    self.alive = true

    math.randomseed(socket.gettime())
    put_food(self)
end

function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed and self.alive then
        local newdir = table.remove(self.dirqueue, 1)

        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y
            if not opposite then
                self.dir = newdir
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tile = tilemap.get_tile("#grid", "layer1", newhead.x, newhead.y)

        if tile == 2 or tile == 4 then
            self.alive = false
        elseif tile == 3 then
            self.speed = self.speed + 1
            put_food(self)
        else
            local tail = table.remove(self.segments, 1)
            tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 1)
        end

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)            
        end

        self.time = 0
    end
end

function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = 1})
    elseif action_id == hash("down") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = -1})
    elseif action_id == hash("left") and action.pressed then
        table.insert(self.dirqueue, {x = -1, y = 0})
    elseif action_id == hash("right") and action.pressed then
        table.insert(self.dirqueue, {x = 1, y = 0})
    end
end
```

## Упражнения

Полезно попробовать реализовать следующие улучшения:

1. Добавьте обработку клавиши для перезапуска игры после проигрыша.
2. Добавьте систему очков и счетчик очков, используя простой label component или полноценный gui.
3. Функция `put_food()` не учитывает позицию змейки и препятствия. Исправьте ее так, чтобы еда появлялась только на свободных местах.
4. Когда игра окончена, показывайте сообщение "Game Over" и дайте игроку попробовать еще раз.
5. Дополнительное задание: добавьте змейку для второго игрока.
