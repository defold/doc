---
title: Програмування мовою Lua у Defold
brief: Цей посібник стисло ознайомлює з основами програмування мовою Lua загалом і з тим, що слід враховувати під час роботи з Lua у Defold.
---

# Lua у Defold {#lua-in-defold}

У рушій Defold вбудовано мову Lua для написання скриптів. Lua — легка динамічна мова, потужна, швидка й проста для вбудовування. Її широко використовують як мову скриптів у відеоіграх. Програми Lua пишуть із простим процедурним синтаксисом. Мова має динамічну типізацію, а програми виконує інтерпретатор байткоду. Вона підтримує автоматичне керування пам’яттю з інкрементальним збиранням сміття.

Цей посібник стисло ознайомлює з основами програмування мовою Lua загалом і з тим, що слід враховувати під час роботи з Lua у Defold. Якщо ви вже маєте певний досвід роботи з Python, Perl, Ruby, Javascript або подібною динамічною мовою, то зможете досить швидко розпочати роботу. Якщо ви лише починаєте програмувати, варто спершу прочитати книжку з Lua для початківців. Таких книжок чимало.

## Версії Lua {#lua-versions}

Defold використовує [LuaJIT](https://luajit.org/) — високооптимізовану версію Lua, придатну для ігор та іншого програмного забезпечення, для якого критична продуктивність. Вона зберігає повну сумісність із Lua 5.1 та підтримує всі функції стандартних бібліотек Lua і повний набір функцій API Lua/C.

LuaJIT також додає кілька [розширень мови](https://luajit.org/extensions.html) і деякі можливості Lua 5.2 та 5.3.

Ми прагнемо забезпечити однакову роботу Defold на всіх платформах, але наразі між платформами є кілька невеликих відмінностей у версії мови Lua:
* iOS не дозволяє JIT-компіляцію.
* Nintendo Switch не дозволяє JIT-компіляцію.
* HTML5 використовує Lua 5.1.4 замість LuaJIT.

::: important
Щоб гарантувати роботу гри на всіх підтримуваних платформах, наполегливо рекомендуємо використовувати ЛИШЕ можливості мови Lua 5.1.
:::

### Стандартні бібліотеки й розширення {#standard-libraries-and-extensions}
Defold містить усі [стандартні бібліотеки Lua 5.1](http://www.lua.org/manual/5.1/manual.html#5), а також бібліотеки для роботи із сокетами та бітових операцій:

  - base (`assert()`, `error()`, `print()`, `ipairs()`, `require()` тощо)
  - coroutine
  - package
  - string
  - table
  - math
  - io
  - os
  - debug
  - socket (з [LuaSocket](https://github.com/diegonehab/luasocket))
  - bitop (з [BitOp](http://bitop.luajit.org/api.html))

Усі бібліотеки описано в [довіднику API](/ref/go).

## Книжки та ресурси з Lua {#lua-books-and-resources}

### Онлайн-ресурси {#online-resources}
* [Програмування мовою Lua (перше видання)](http://www.lua.org/pil/contents.html) Пізніші видання доступні в друкованому вигляді.
* [Довідник Lua 5.1](http://www.lua.org/manual/5.1/)
* [Вивчіть Lua за 15 хвилин](http://tylerneylon.com/a/learn-lua/)
* [Awesome Lua — розділ уроків](https://github.com/LewisJEllis/awesome-lua#tutorials)

### Книжки {#books}
* [Програмування мовою Lua](https://www.amazon.com/gp/product/8590379868/ref=dbs_a_def_rwt_hsch_vapi_taft_p1_i0) — «Програмування мовою Lua» — офіційна книжка про цю мову, яка дає міцну основу кожному програмісту, що хоче використовувати Lua. Її автор — Роберто Єрузалімскі, головний архітектор мови.
* [Перлини програмування мовою Lua](https://www.amazon.com/Programming-Gems-Luiz-Henrique-Figueiredo/dp/8590379841) — Ця збірка статей узагальнює частину наявних знань і практичного досвіду якісного програмування мовою Lua.
* [Довідник Lua 5.1](https://www.amazon.com/gp/product/8590379833/ref=dbs_a_def_rwt_hsch_vapi_taft_p1_i4) — Також доступний онлайн (див. вище)
* [Початки програмування мовою Lua](https://www.amazon.com/Beginning-Lua-Programming-Kurt-Jung/dp/0470069171)

### Відео {#videos}
* [Вивчіть Lua за одне відео](https://www.youtube.com/watch?v=iMacxZQMPXs)

## Синтаксис {#syntax}

Програми мають простий, зрозумілий синтаксис. Інструкції записують по одній на рядок, і позначати кінець інструкції не потрібно. За бажанням можна розділяти інструкції крапкою з комою `;`. Блоки коду обмежуються ключовими словами й завершуються ключовим словом `end`. Коментарі можна записувати як окремий блок або до кінця рядка:

```lua
--[[
Here is a block of comments that can run
over several lines in the source file.
--]]

a = 10
b = 20 ; c = 30 -- two statements on one line

if my_variable == 3 then
    call_some_function(true) -- Here is a line comment
else
    call_another_function(false)
end
```

## Змінні й типи даних {#variables-and-data-types}

Lua має динамічну типізацію: змінні не мають типів, а значення мають. 
На відміну від статично типізованих мов, ви можете довільно присвоювати будь-яке значення будь-якій змінній. 

У Lua є вісім основних типів:

`nil`
: Цей тип має лише значення `nil`. Зазвичай воно позначає відсутність корисного значення, наприклад у змінних, яким ще нічого не присвоєно.

  ```lua
  print(my_var) -- will print 'nil' since 'my_var' is not yet assigned a value
  ```

boolean
: Має значення `true` або `false`. Умови зі значенням `false` або `nil` вважаються хибними. Будь-яке інше значення робить умову істинною.

  ```lua
  flag = true
  if flag then
      print("flag is true")
  else
      print("flag is false")
  end

  if my_var then
      print("my_var is not nil nor false!")
  end

  if not my_var then
      print("my_var is either nil or false!")
  end
  ```

number
: Внутрішньо числа подано як 64-бітові _цілі числа_ або 64-бітові числа _з рухомою комою_. Lua автоматично перетворює їх між цими поданнями за потреби, тому зазвичай вам не потрібно про це турбуватися.

  ```lua
  print(10) --> prints '10'
  print(10.0) --> '10'
  print(10.000000000001) --> '10.000000000001'

  a = 5 -- integer
  b = 7/3 -- float
  print(a - b) --> '2.6666666666667'
  ```

string
: Рядки — незмінні послідовності байтів, які можуть містити будь-яке 8-бітове значення, зокрема вбудовані нулі (`\0`). Lua не робить жодних припущень щодо вмісту рядка, тож у рядках можна зберігати будь-які дані. Рядкові літерали записують в одинарних або подвійних лапках. Lua перетворює числа на рядки й навпаки під час виконання. Рядки можна з’єднувати оператором `..`.

  Рядки можуть містити такі керівні послідовності у стилі C:

  | Послідовність | Символ |
  | -------- | --------- |
  | `\a`     | звуковий сигнал       |
  | `\b`     | повернення на один символ |
  | `\f`     | переведення сторінки  |
  | `\n`     | новий рядок    |
  | `\r`     | повернення каретки |
  | `\t`     | горизонтальна табуляція |
  | `\v`     | вертикальна табуляція   |
  | `\\`     | зворотна скісна риска      |
  | `\"`     | подвійні лапки   |
  | `\'`     | одинарні лапки   |
  | `\[`     | ліва квадратна дужка    |
  | `\]`     | права квадратна дужка   |
  | `\ddd`   | символ, заданий числовим значенням, де `ddd` — послідовність щонайбільше з трьох _десяткових_ цифр |

  ```lua
  my_string = "hello"
  another_string = 'world'
  print(my_string .. another_string) --> "helloworld"

  print("10.2" + 1) --> 11.2
  print(my_string + 1) -- error, can't convert "hello"
  print(my_string .. 1) --> "hello1"

  print("one\nstring") --> one
                       --> string

  print("\097bc") --> "abc"

  multi_line_string = [[
  Here is a chunk of text that runs over several lines. This is all
  put into the string and is sometimes very handy.
  ]]
  ```

function
: Функції в Lua є значеннями першого класу: їх можна передавати як параметри іншим функціям і повертати як значення. Змінні, яким присвоєно функцію, містять посилання на неї. Можна присвоювати змінним анонімні функції, але для зручності Lua надає синтаксичний цукор (`function name(param1, param2) ... end`).

  ```lua
  -- Assign 'my_plus' to function
  my_plus = function(p, q)
      return p + q
  end

  print(my_plus(4, 5)) --> 9

  -- Convenient syntax to assign function to variable 'my_mult'
  function my_mult(p, q)
      return p * q
  end

  print(my_mult(4, 5)) --> 20

  -- Takes a function as parameter 'func'
  function operate(func, p, q)
      return func(p, q) -- Calls the provided function with parameters 'p' and 'q'
  end

  print(operate(my_plus, 4, 5)) --> 9
  print(operate(my_mult, 4, 5)) --> 20

  -- Create an adder function and return it
  function create_adder(n)
      return function(a)
          return a + n
      end
  end

  adder = create_adder(2)
  print(adder(3)) --> 5
  print(adder(10)) --> 12
  ```

table
: Таблиці — єдиний тип Lua для структурування даних. Це _об’єкти_ асоціативних масивів, які використовують для подання списків, масивів, послідовностей, таблиць символів, множин, записів, графів, дерев тощо. Таблиці завжди анонімні, а змінні, яким ви присвоюєте таблицю, містять не саму таблицю, а посилання на неї. Під час ініціалізації таблиці як послідовності перший індекс — `1`, а не `0`.

  ```lua
  -- Initialize a table as a sequence
  weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday"}
  print(weekdays[1]) --> "Sunday"
  print(weekdays[5]) --> "Thursday"

  -- Initialize a table as a record with sequence values
  moons = { Earth = { "Moon" },
            Uranus = { "Puck", "Miranda", "Ariel", "Umbriel", "Titania", "Oberon" } }
  print(moons.Uranus[3]) --> "Ariel"

  -- Build a table from an empty constructor {}
  a = 1
  t = {}
  t[1] = "first"
  t[a + 1] = "second"
  t.x = 1 -- same as t["x"] = 1

  -- Iterate over the table key, value pairs
  for key, value in pairs(t) do
      print(key, value)
  end
  --> 1   first
  --> 2   second
  --> x   1

  u = t -- u now refers to the same table as t
  u[1] = "changed"

  for key, value in pairs(t) do -- still iterating over t!
      print(key, value)
  end
  --> 1   changed
  --> 2   second
  --> x   1
  ```

userdata
: Тип `userdata` дає змогу зберігати довільні дані C у змінних Lua. Defold використовує об’єкти Lua типу `userdata` для зберігання хешованих значень (hash), об’єктів URL (url), математичних об’єктів (vector3, vector4, matrix4, quaternion), ігрових об’єктів (game object), вузлів GUI (node), предикатів рендерингу (predicate), цільових буферів рендерингу (render_target) і буферів констант рендерингу (constant_buffer)

thread
: Потоки представляють незалежні потоки виконання й використовуються для реалізації співпрограм. Докладніше див. нижче.

## Оператори {#operators}

Арифметичні оператори
: Математичні оператори `+`, `-`, `*`, `/`, унарний `-` (зміна знака) і піднесення до степеня `^`.

  ```lua
  a = -1
  print(a * 2 + 3 / 4^5) --> -1.9970703125
  ```

  Lua автоматично перетворює числа на рядки й навпаки під час виконання. Будь-яка числова операція над рядком намагається перетворити його на число:

  ```lua
  print("10" + 1) --> 11
  ```

Оператори відношення й порівняння
: `<` (менше), `>` (більше), `<=` (менше або дорівнює), `>=` (більше або дорівнює), `==` (дорівнює), `~=` (не дорівнює). Ці оператори завжди повертають `true` або `false`. Значення різних типів вважаються різними. Якщо типи однакові, порівнюються їхні значення. Lua порівнює таблиці, `userdata` та функції за посиланням. Два такі значення вважаються рівними, лише якщо вони посилаються на той самий об’єкт.

  ```lua
  a = 5
  b = 6

  if a <= b then
      print("a is less than or equal to b")
  end

  print("A" < "a") --> true
  print("aa" < "ab") --> true
  print(10 == "10") --> false
  print(tostring(10) == "10") --> true
  ```

Логічні оператори
: `and`, `or` та `not`. `and` повертає перший аргумент, якщо він дорівнює `false`, інакше повертає другий аргумент. `or` повертає перший аргумент, якщо він не дорівнює `false`, інакше повертає другий аргумент.

  ```lua
  print(true or false) --> true
  print(true and false) --> false
  print(not false) --> true

  if a == 5 and b == 6 then
      print("a is 5 and b is 6")
  end
  ```

Конкатенація
: Рядки можна з’єднувати оператором `..`. Під час конкатенації числа перетворюються на рядки.

  ```lua
  print("donkey" .. "kong") --> "donkeykong"
  print(1 .. 2) --> "12"
  ```

Довжина
: Унарний оператор довжини `#`. Довжина рядка — це кількість байтів у ньому. Довжина таблиці — це довжина її послідовності, кількість індексів, пронумерованих від `1` і далі, значення яких не дорівнює `nil`. Примітка: якщо в послідовності є «прогалини» зі значенням `nil`, довжиною може бути будь-який індекс, що передує значенню `nil`.

  ```lua
  s = "donkey"
  print(#s) --> 6

  t = { "a", "b", "c", "d" }
  print(#t) --> 4

  u = { a = 1, b = 2, c = 3 }
  print(#u) --> 0

  v = { "a", "b", nil }
  print(#v) --> 2
  ```

## Керування потоком виконання {#flow-control}

Lua надає звичний набір конструкцій керування потоком виконання.

if---then---else
: Перевіряє умову й виконує частину `then`, якщо умова істинна, або необов’язкову частину `else`, якщо умова хибна. Замість вкладених інструкцій `if` можна використовувати `elseif`. Це замінює інструкцію switch, якої в Lua немає.

  ```lua
  a = 5
  b = 4

  if a < b then
      print("a is smaller than b")
  end

  if a == '1' then
      print("a is 1")
  elseif a == '2' then
      print("a is 2")
  elseif a == '3' then
      print("a is 3")
  else
      print("I have no idea what a is...")
  end
  ```

while
: Перевіряє умову й виконує блок, доки вона істинна.

  ```lua
  weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday"}

  -- Print each weekday
  i = 1
  while weekdays[i] do
      print(weekdays[i])
      i = i + 1
  end
  ```

repeat---until
: Повторює блок, доки умова не стане істинною. Умова перевіряється після тіла циклу, тому воно виконається щонайменше один раз.

  ```lua
  weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday"}

  -- Print each weekday
  i = 0
  repeat
      i = i + 1
      print(weekdays[i])
  until weekdays[i] == "Saturday"
  ```

for
: У Lua є два різновиди циклу `for`: числовий і узагальнений. Числовий `for` приймає 2 або 3 числові значення, а узагальнений `for` перебирає всі значення, які повертає функція-_ітератор_.

  ```lua
  -- Print the numbers 1 to 10
  for i = 1, 10 do
      print(i)
  end

  -- Print the numbers 1 to 10 and increment with 2 each time
  for i = 1, 10, 2 do
      print(i)
  end

  -- Print the numbers 10 to 1
  for i=10, 1, -1 do
      print(i)
  end

  t = { "a", "b", "c", "d" }
  -- Iterate over the sequence and print the values
  for i, v in ipairs(t) do
      print(v)
  end
  ```

break і return
: Використовуйте інструкцію `break`, щоб вийти з внутрішнього блоку циклу `for`, `while` або `repeat`. Використовуйте `return`, щоб повернути значення з функції або завершити її виконання й повернути керування коду, що її викликав. `break` або `return` можуть бути лише останньою інструкцією блоку.

  ```lua
  a = 1
  while true do
      a = a + 1
      if a >= 100 then
          break
      end
  end

  function my_add(a, b)
      return a + b
  end

  print(my_add(10, 12)) --> 22
  ```

## Локальні й глобальні змінні та лексична область видимості {#locals-globals-and-lexical-scoping}

Усі змінні, які ви оголошуєте, за замовчуванням глобальні, тобто доступні в усіх частинах контексту середовища виконання Lua. Ви можете явно оголосити змінні як `local`, тоді змінна існуватиме лише в поточній області видимості.

Кожен файл вихідного коду Lua визначає окрему область видимості. Оголошення `local` на найвищому рівні файлу означає, що змінна локальна для цього файлу скрипту Lua. Кожна функція створює ще одну вкладену область видимості, а кожен блок керівної конструкції — додаткові області видимості. Ви можете явно створити область видимості за допомогою ключових слів `do` та `end`. Lua використовує лексичну область видимості: кожна область має повний доступ до _локальних_ змінних зовнішньої області видимості. Зауважте, що локальні змінні потрібно оголосити до їх використання.

```lua
function my_func(a, b)
    -- 'a' and 'b' are local to this function and available through its scope

    do
        local x = 1
    end

    print(x) --> nil. 'x' is not available outside the do-end scope
    print(foo) --> nil. 'foo' is declared after 'my_func'
    print(foo_global) --> "value 2"
end

local foo = "value 1"
foo_global = "value 2"

print(foo) --> "value 1". 'foo' is available in the topmost scope after declaration.
```

Зауважте: якщо ви оголошуєте функції як `local` у файлі скрипту (що зазвичай варто робити), потрібно стежити за порядком коду. Для функцій, що взаємно викликають одна одну, можна використовувати попередні оголошення.

```lua
local func2 -- Forward declare 'func2'

local function func1(a)
    print("func1")
    func2(a)
end

function func2(a) -- or func2 = function(a)
    print("func2")
    if a < 10 then
        func1(a + 1)
    end
end

function init(self)
    func1(1)
end
```

Якщо написати функцію всередині іншої функції, вона також матиме повний доступ до локальних змінних зовнішньої функції. Це дуже потужна конструкція.

```lua
function create_counter(x)
    -- 'x' is a local variable in 'create_counter'
    return function()
        x = x + 1
        return x
    end
end

count1 = create_counter(10)
count2 = create_counter(20)
print(count1()) --> 11
print(count2()) --> 21
print(count1()) --> 12
```

## Затінення змінних {#variable-shadowing}

Локальні змінні, оголошені в блоці, затінюють змінні з такими самими іменами із зовнішнього блоку.

```lua
my_global = "global"
print(my_global) -->"global"

local v = "local"
print(v) --> "local"

local function test(v)
    print(v)
end

function init(self)
    v = "apple"
    print(v) --> "apple"
    test("banana") --> "banana"
end
```

## Співпрограми {#coroutines}

Функції виконуються від початку до кінця, і призупинити їх посеред виконання неможливо. Співпрограми дають таку можливість, що в деяких випадках дуже зручно. Припустімо, ми хочемо створити певну покадрову анімацію, у якій ігровий об’єкт переміщується з позиції `0` за віссю y у точно задані позиції за цією віссю протягом кадрів від 1 до 5. Це можна реалізувати за допомогою лічильника у функції `update()` (див. нижче) і списку позицій. Однак співпрограма дає дуже зрозумілу реалізацію, яку легко розширювати та з якою зручно працювати. Увесь стан міститься в самій співпрограмі.

Коли співпрограма призупиняється, вона повертає керування коду, що її викликав, але запам’ятовує точку виконання, щоб згодом продовжити з неї.

```lua
-- This is our coroutine
local function sequence(self)
    coroutine.yield(120)
    coroutine.yield(320)
    coroutine.yield(510)
    coroutine.yield(240)
    return 440 -- return the final value
end

function init(self)
    self.co = coroutine.create(sequence) -- Create the coroutine. 'self.co' is a thread object
    go.set_position(vmath.vector3(100, 0, 0)) -- Set initial position
end

function update(self, dt)
    local status, y_pos = coroutine.resume(self.co, self) -- Continue execution of coroutine.
    if status then
        -- If the coroutine is still not terminated/dead, use its yielded return value as a new position
        go.set_position(vmath.vector3(100, y_pos, 0))
    end
end
```


## Контексти Lua у Defold {#lua-contexts-in-defold}

Усі змінні, які ви оголошуєте, за замовчуванням глобальні, тобто доступні в усіх частинах контексту середовища виконання Lua. У Defold цим контекстом керує налаштування *shared_state* у файлі *game.project*. Якщо цей параметр увімкнено, усі скрипти, скрипти GUI та скрипт рендерингу виконуються в одному контексті Lua, а глобальні змінні видимі всюди. Якщо параметр вимкнено, рушій виконує скрипти, скрипти GUI та скрипт рендерингу в окремих контекстах.

![Контексти](images/lua/lua_contexts.png)

У Defold можна використовувати той самий файл скрипту в кількох окремих компонентах (component) ігрових об’єктів. Усі локально оголошені змінні є спільними для компонентів, які виконують той самий файл скрипту.

```lua
-- 'my_global_value' will be available from all scripts, gui_scripts, render script and modules (Lua files)
my_global_value = "global scope"

-- this value will be shared through all component instances that use this particular script file
local script_value = "script scope"

function init(self, dt)
    -- This value will be available on this script component instance
    self.foo = "self scope"

    -- this value will be available inside init() and after it's declaration
    local local_foo = "local scope"
    print(local_foo)
end

function update(self, dt)
    print(self.foo)
    print(my_global_value)
    print(script_value)
    print(local_foo) -- will print nil, since local_foo is only visible in init()
end
```

## Міркування щодо продуктивності {#performance-considerations}

У високопродуктивній грі, розрахованій на плавну роботу з частотою 60 FPS, навіть невеликі помилки, пов’язані з продуктивністю, можуть суттєво вплинути на враження від гри. Варто враховувати як деякі прості загальні речі, так і ті, що на перший погляд не здаються проблемними.

Почнімо з простого. Зазвичай варто писати зрозумілий код без зайвих циклів. Іноді справді потрібно перебирати списки елементів, але будьте обережні, якщо список досить великий. Цей приклад виконується трохи довше ніж 1 мілісекунду на доволі непоганому ноутбуці. Це може бути суттєво, якщо на кожен кадр відведено лише 16 мілісекунд (за 60 FPS), а частину цього часу вже витрачають рушій, скрипт рендерингу, симуляція фізики тощо.

```lua
local t = socket.gettime()
local table = {}
for i=1,2000 do
    table[i] = vmath.vector3(i, i, i)
end
print((socket.gettime() - t) * 1000)

-- DEBUG:SCRIPT: 0.40388
```

Використовуйте значення, яке повертає `socket.gettime()` (секунди від початку системної епохи), щоб вимірювати швидкодію підозрілих ділянок коду.

## Пам’ять і збирання сміття {#memory-and-garbage-collection}

За замовчуванням збирання сміття в Lua автоматично працює у фоні й вивільняє пам’ять, виділену середовищем виконання Lua. Збирання великої кількості сміття може забирати багато часу, тому варто зменшувати кількість об’єктів, які потребуватимуть збирання:

* Локальні змінні самі по собі не створюють додаткових витрат і не генерують сміття. (Наприклад, `local v = 42`)
* Кожен _новий унікальний_ рядок створює новий об’єкт. Запис `local s = "some_string"` створить новий об’єкт і присвоїть посилання на нього змінній `s`. Сама локальна змінна `s` не генеруватиме сміття, але об’єкт рядка — генеруватиме. Багаторазове використання того самого рядка не збільшує витрати пам’яті.
* Кожне виконання конструктора таблиці (`{ ... }`) створює нову таблицю.
* Виконання _інструкції визначення функції_ створює об’єкт замикання. (Тобто виконання інструкції `function () ... end`, а не виклик визначеної функції)
* Функції зі змінною кількістю аргументів (`function(v, ...) end`) створюють таблицю для трикрапки щоразу, коли функцію _викликають_ (у Lua до версії 5.2 або якщо не використовується LuaJIT).
* `dofile()` і `dostring()`
* Об’єкти userdata

У багатьох випадках можна уникнути створення нових об’єктів і натомість повторно використовувати вже наявні. Наприклад, наприкінці кожного `update()` часто можна побачити таке:

```lua
-- Reset velocity
self.velocity = vmath.vector3()
```

Легко забути, що кожен виклик `vmath.vector3()` створює новий об’єкт. З’ясуймо, скільки пам’яті використовує один `vector3`:

```lua
print(collectgarbage("count") * 1024)       -- 88634
local v = vmath.vector3()
print(collectgarbage("count") * 1024)       -- 88704. 70 bytes in total has been allocated
```

Між викликами `collectgarbage()` додалося 70 байтів, але це включає виділення пам’яті не лише для об’єкта `vector3`. Кожне виведення результату `collectgarbage()` формує рядок, який сам по собі додає 22 байти сміття:

```lua
print(collectgarbage("count") * 1024)       -- 88611
print(collectgarbage("count") * 1024)       -- 88633. 22 bytes allocated
```

Отже, `vector3` займає 70-22=48 байтів. Це небагато, але якщо створювати _один_ такий об’єкт кожного кадру в грі з частотою 60 FPS, це вже 2,8 КБ сміття за секунду. Якщо 360 компонентів-скриптів створюють по одному `vector3` кожного кадру, утворюється 1 МБ сміття за секунду. Ці обсяги можуть зростати дуже швидко. Коли середовище виконання Lua збирає сміття, це може забирати багато цінних мілісекунд — особливо на мобільних платформах.

Один зі способів уникнути виділення пам’яті — створити `vector3`, а потім працювати з тим самим об’єктом. Наприклад, щоб обнулити `vector3`, можна використати таку конструкцію:

```lua
-- Instead of doing self.velocity = vmath.vector3() which creates a new object
-- we zero an existing velocity vector object's components
self.velocity.x = 0
self.velocity.y = 0
self.velocity.z = 0
```

Стандартна схема збирання сміття може бути неоптимальною для деяких застосунків, чутливих до затримок. Якщо ви помічаєте ривки у грі чи застосунку, варто налаштувати збирання сміття в Lua за допомогою функції [`collectgarbage()`](/ref/base/#collectgarbage). Наприклад, можна запускати збирач ненадовго кожного кадру з малим значенням `step`. Щоб оцінити, скільки пам’яті споживає ваша гра чи застосунок, можна вивести поточний обсяг сміття в байтах:

```lua
print(collectgarbage("count") * 1024)
```

## Рекомендовані практики {#best-practices}

Під час проєктування реалізації часто постає питання, як структурувати код спільної поведінки. Можливі кілька підходів.

Поведінка в модулі
: Інкапсуляція поведінки в модулі дає змогу легко ділитися кодом між компонентами-скриптами різних ігрових об’єктів (і скриптами GUI). Функції модуля зазвичай найкраще писати в суто функціональному стилі. Трапляються випадки, коли збереження стану або побічні ефекти необхідні (чи роблять архітектуру зрозумілішою). Якщо вам потрібно зберігати внутрішній стан у модулі, пам’ятайте, що компоненти використовують спільні контексти Lua. Докладніше див. у [документації з модулів](/manuals/modules).

  ![Модуль](images/lua/lua_module.png)

  Крім того, хоча код модуля може безпосередньо змінювати внутрішній стан ігрового об’єкта (якщо передати `self` функції модуля), ми наполегливо не рекомендуємо цього робити, оскільки це створює дуже тісну зв’язаність.

Допоміжний ігровий об’єкт з інкапсульованою поведінкою
: Як і в модулі Lua, код скрипту можна розмістити в ігровому об’єкті з компонентом-скриптом. Різниця в тому, що з кодом в ігровому об’єкті можна взаємодіяти виключно через передавання повідомлень.

  ![Допоміжний об’єкт](images/lua/lua_helper.png)

Групування ігрового об’єкта з допоміжним об’єктом поведінки всередині колекції
: За такого підходу можна створити ігровий об’єкт поведінки, який автоматично впливає на інший цільовий ігровий об’єкт: за заздалегідь визначеним іменем (користувач має відповідно перейменувати цільовий ігровий об’єкт) або через URL у `go.property()`, що вказує на цільовий ігровий об’єкт.

  ![Колекція](images/lua/lua_collection.png)

  Перевага такої організації в тому, що ви можете додати ігровий об’єкт поведінки до колекції (collection), яка містить цільовий об’єкт. Додатковий код узагалі не потрібен.

  Коли потрібно керувати великою кількістю ігрових об’єктів, цей підхід менш придатний, оскільки об’єкт поведінки дублюється для кожного екземпляра (instance), а кожен об’єкт споживає пам’ять.
