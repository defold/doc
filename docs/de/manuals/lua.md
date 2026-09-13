---
title: Lua-Programmierung in Defold
brief: Dieses Handbuch bietet eine kurze Einführung in die Grundlagen der Lua-Programmierung und erklärt, was du bei der Arbeit mit Lua in Defold beachten solltest.
---

# Lua in Defold

In die Defold-Engine ist die Sprache Lua für die Skriptprogrammierung eingebettet. Lua ist eine schlanke dynamische Sprache, die leistungsfähig, schnell und leicht einzubetten ist. Sie wird häufig als Skriptsprache für Videospiele eingesetzt. Lua-Programme werden in einer einfachen prozeduralen Syntax geschrieben. Die Sprache ist dynamisch typisiert und wird von einem Bytecode-Interpreter ausgeführt. Sie bietet eine automatische Speicherverwaltung mit inkrementeller automatischer Speicherbereinigung (Garbage Collection).

Dieses Handbuch bietet eine kurze Einführung in die Grundlagen der Lua-Programmierung und erklärt, was du bei der Arbeit mit Lua in Defold beachten solltest. Wenn du bereits Erfahrung mit Python, Perl, Ruby, JavaScript oder einer ähnlichen dynamischen Sprache hast, wirst du dich schnell zurechtfinden. Wenn du noch keine Programmiererfahrung hast, kannst du mit einem Lua-Buch für den Einstieg beginnen. Es gibt eine große Auswahl.

## Lua-Versionen {#lua-versions}

Defold verwendet [LuaJIT](https://luajit.org/), eine stark optimierte Version von Lua, die sich für Spiele und andere Software mit hohen Leistungsanforderungen eignet. LuaJIT ist vollständig aufwärtskompatibel mit Lua 5.1 und unterstützt alle Funktionen der Lua-Standardbibliotheken sowie sämtliche Funktionen der Lua/C-API.

LuaJIT bietet außerdem mehrere [Spracherweiterungen](https://luajit.org/extensions.html) und einige Funktionen aus Lua 5.2 und 5.3.

Das Defold-Team strebt an, Defold auf allen Plattformen einheitlich zu halten. Derzeit gibt es jedoch einige kleinere Unterschiede zwischen den Plattformen bei der verwendeten Lua-Sprachversion:
* iOS erlaubt keine JIT-Kompilierung.
* Nintendo Switch erlaubt keine JIT-Kompilierung.
* HTML5 verwendet Lua 5.1.4 anstelle von LuaJIT.

::: important
Damit dein Spiel auf allen unterstützten Plattformen funktioniert, empfehlen wir dringend, NUR Sprachfunktionen aus Lua 5.1 zu verwenden.
:::

### Standardbibliotheken und Erweiterungen {#standard-libraries-and-extensions}
Defold enthält alle [Lua-5.1-Standardbibliotheken](http://www.lua.org/manual/5.1/manual.html#5) sowie eine Socket-Bibliothek und eine Bibliothek für Bitoperationen:

  - base (`assert()`, `error()`, `print()`, `ipairs()`, `require()` usw.)
  - coroutine
  - package
  - string
  - table
  - math
  - io
  - os
  - debug
  - socket (aus [LuaSocket](https://github.com/diegonehab/luasocket))
  - bitop (aus [BitOp](http://bitop.luajit.org/api.html))

Alle Bibliotheken sind in der [API-Referenzdokumentation](/ref/go) dokumentiert.

## Bücher und Ressourcen zu Lua {#lua-books-and-resources}

### Online-Ressourcen {#online-resources}
* [Programming in Lua (erste Ausgabe)](http://www.lua.org/pil/contents.html) Spätere Ausgaben sind in gedruckter Form erhältlich.
* [Lua-5.1-Referenzhandbuch](http://www.lua.org/manual/5.1/)
* [Lua in 15 Minuten lernen](http://tylerneylon.com/a/learn-lua/)
* [Awesome Lua – Abschnitt mit Tutorials](https://github.com/LewisJEllis/awesome-lua#tutorials)

### Bücher {#books}
* [Programming in Lua](https://www.amazon.com/gp/product/8590379868/ref=dbs_a_def_rwt_hsch_vapi_taft_p1_i0) - Programming in Lua ist das offizielle Buch zur Sprache und bietet allen, die mit Lua programmieren möchten, eine solide Grundlage. Geschrieben wurde es von Roberto Ierusalimschy, dem Hauptarchitekten der Sprache.
* [Lua programming gems](https://www.amazon.com/Programming-Gems-Luiz-Henrique-Figueiredo/dp/8590379841) - Diese Artikelsammlung hält einen Teil des vorhandenen Wissens und bewährter Verfahren für gutes Programmieren in Lua fest.
* [Lua-5.1-Referenzhandbuch](https://www.amazon.com/gp/product/8590379833/ref=dbs_a_def_rwt_hsch_vapi_taft_p1_i4) - Auch online verfügbar (siehe oben)
* [Beginning Lua Programming](https://www.amazon.com/Beginning-Lua-Programming-Kurt-Jung/dp/0470069171)

### Videos
* [Lua in einem Video lernen](https://www.youtube.com/watch?v=iMacxZQMPXs)

## Syntax

Programme haben eine einfache, gut lesbare Syntax. Anweisungen werden jeweils in eine eigene Zeile geschrieben, und ihr Ende muss nicht gekennzeichnet werden. Optional kannst du Semikolons `;` verwenden, um Anweisungen zu trennen. Codeblöcke werden durch Schlüsselwörter begrenzt und enden mit dem Schlüsselwort `end`. Kommentare können als Block oder bis zum Ende einer Zeile geschrieben werden:

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

## Variablen und Datentypen {#variables-and-data-types}

Lua ist dynamisch typisiert. Das bedeutet, dass Variablen keinen Typ haben, Werte hingegen schon. 
Anders als in statisch typisierten Sprachen kannst du jeder Variablen einen beliebigen Wert zuweisen. 

Lua hat acht grundlegende Typen:

`nil`
: Dieser Typ hat nur den Wert `nil`. Er steht gewöhnlich für das Fehlen eines sinnvollen Werts, beispielsweise bei Variablen, denen noch kein Wert zugewiesen wurde.

  ```lua
  print(my_var) -- will print 'nil' since 'my_var' is not yet assigned a value
  ```

boolean
: Hat entweder den Wert `true` oder `false`. Bedingungen mit dem Wert `false` oder `nil` werden als falsch ausgewertet. Jeder andere Wert wird als wahr ausgewertet.

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
: Zahlen werden intern entweder als _Ganzzahlen_ mit 64 Bit oder als _Gleitkommazahlen_ mit 64 Bit dargestellt. Lua wandelt diese Darstellungen bei Bedarf automatisch ineinander um, sodass du dich in der Regel nicht darum kümmern musst.

  ```lua
  print(10) --> prints '10'
  print(10.0) --> '10'
  print(10.000000000001) --> '10.000000000001'

  a = 5 -- integer
  b = 7/3 -- float
  print(a - b) --> '2.6666666666667'
  ```

string
: Zeichenfolgen sind unveränderliche Folgen von Bytes, die jeden beliebigen 8-Bit-Wert enthalten können, einschließlich eingebetteter Nullbytes (`\0`). Lua trifft keine Annahmen über den Inhalt einer Zeichenfolge, sodass du beliebige Daten darin speichern kannst. Zeichenfolgenliterale werden in einfache oder doppelte Anführungszeichen eingeschlossen. Lua wandelt Zahlen und Zeichenfolgen zur Laufzeit ineinander um. Zeichenfolgen lassen sich mit dem Operator `..` verketten.

  Zeichenfolgen können die folgenden Escape-Sequenzen im Stil von C enthalten:

  | Sequenz | Zeichen |
  | -------- | --------- |
  | `\a`     | Signalton       |
  | `\b`     | Rückschritt |
  | `\f`     | Seitenvorschub  |
  | `\n`     | Zeilenumbruch    |
  | `\r`     | Wagenrücklauf |
  | `\t`     | horizontaler Tabulator |
  | `\v`     | vertikaler Tabulator   |
  | `\\`     | umgekehrter Schrägstrich      |
  | `\"`     | doppeltes Anführungszeichen   |
  | `\'`     | einfaches Anführungszeichen   |
  | `\[`     | öffnende eckige Klammer    |
  | `\]`     | schließende eckige Klammer   |
  | `\ddd`   | durch seinen Zahlenwert angegebenes Zeichen, wobei `ddd` eine Folge aus bis zu drei _Dezimalziffern_ ist |

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
: Funktionen sind in Lua vollwertige Werte. Das bedeutet, dass du sie als Parameter an Funktionen übergeben und als Werte zurückgeben kannst. Variablen, denen eine Funktion zugewiesen ist, enthalten eine Referenz auf diese Funktion. Du kannst Variablen anonyme Funktionen zuweisen, aber Lua bietet zur Vereinfachung syntaktischen Zucker (`function name(param1, param2) ... end`).

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
: Tabellen sind der einzige Typ in Lua zur Strukturierung von Daten. Es sind _Objekte_ in Form assoziativer Arrays, mit denen Listen, Arrays, Sequenzen, Symboltabellen, Mengen, Datensätze, Graphen, Bäume usw. dargestellt werden. Tabellen sind immer anonym. Variablen, denen du eine Tabelle zuweist, enthalten nicht die Tabelle selbst, sondern eine Referenz darauf. Wenn du eine Tabelle als Sequenz initialisierst, ist der erste Index `1`, nicht `0`.

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
: `userdata` ermöglicht es, beliebige C-Daten in Lua-Variablen zu speichern. Defold verwendet Lua-Objekte vom Typ `userdata`, um Hash-Werte (hash), URL-Objekte (url), mathematische Objekte (vector3, vector4, matrix4, quaternion), Spielobjekte (game objects), GUI-Knoten (node), Render-Prädikate (predicate), Renderziele (render_target) und Render-Konstantenpuffer (constant_buffer) zu speichern

thread
: Threads stellen unabhängige Ausführungsstränge dar und werden zur Implementierung von Koroutinen verwendet. Einzelheiten findest du weiter unten.

## Operatoren {#operators}

Arithmetische Operatoren
: Die mathematischen Operatoren `+`, `-`, `*`, `/`, das unäre `-` (Negation) und der Potenzoperator `^`.

  ```lua
  a = -1
  print(a * 2 + 3 / 4^5) --> -1.9970703125
  ```

  Lua wandelt Zahlen und Zeichenfolgen zur Laufzeit automatisch ineinander um. Bei jeder numerischen Operation auf einer Zeichenfolge wird versucht, die Zeichenfolge in eine Zahl umzuwandeln:

  ```lua
  print("10" + 1) --> 11
  ```

Relations- und Vergleichsoperatoren
: `<` (kleiner als), `>` (größer als), `<=` (kleiner oder gleich), `>=` (größer oder gleich), `==` (gleich), `~=` (ungleich). Diese Operatoren geben immer `true` oder `false` zurück. Werte unterschiedlicher Typen gelten als verschieden. Bei gleichem Typ werden sie anhand ihres Werts verglichen. Lua vergleicht Tabellen, `userdata` und Funktionen anhand ihrer Referenz. Zwei solche Werte gelten nur dann als gleich, wenn sie auf dasselbe Objekt verweisen.

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

Logische Operatoren
: `and`, `or` und `not`. `and` gibt sein erstes Argument zurück, wenn es `false` ist, andernfalls sein zweites Argument. `or` gibt sein erstes Argument zurück, wenn es nicht `false` ist, andernfalls sein zweites Argument.

  ```lua
  print(true or false) --> true
  print(true and false) --> false
  print(not false) --> true

  if a == 5 and b == 6 then
      print("a is 5 and b is 6")
  end
  ```

Verkettung
: Zeichenfolgen lassen sich mit dem Operator `..` verketten. Zahlen werden bei der Verkettung in Zeichenfolgen umgewandelt.

  ```lua
  print("donkey" .. "kong") --> "donkeykong"
  print(1 .. 2) --> "12"
  ```

Länge
: Der unäre Längenoperator `#`. Die Länge einer Zeichenfolge ist ihre Anzahl an Bytes. Die Länge einer Tabelle ist ihre Sequenzlänge, also die Anzahl der ab `1` aufwärts nummerierten Indizes, deren Wert nicht `nil` ist. Hinweis: Wenn die Sequenz „Lücken“ mit dem Wert `nil` enthält, kann die Länge jeder Index sein, der einem Wert `nil` vorausgeht.

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

## Ablaufsteuerung {#flow-control}

Lua bietet die üblichen Konstrukte zur Ablaufsteuerung.

if---then---else
: Prüft eine Bedingung und führt den Teil `then` aus, wenn die Bedingung wahr ist, andernfalls den (optionalen) Teil `else`. Statt `if`-Anweisungen zu verschachteln, kannst du `elseif` verwenden. Dies ersetzt eine switch-Anweisung, die Lua nicht hat.

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
: Prüft eine Bedingung und führt den Block aus, solange sie wahr ist.

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
: Wiederholt den Block, bis eine Bedingung wahr ist. Die Bedingung wird nach dem Block geprüft, sodass dieser mindestens einmal ausgeführt wird.

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
: Lua hat zwei Arten von `for`-Schleifen: numerische und generische. Die numerische `for`-Schleife nimmt 2 oder 3 Zahlenwerte entgegen, während die generische `for`-Schleife über alle Werte iteriert, die eine _Iteratorfunktion_ zurückgibt.

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

break und return
: Verwende die Anweisung `break`, um aus einem inneren Block einer `for`-, `while`- oder `repeat`-Schleife auszubrechen. Verwende `return`, um einen Wert aus einer Funktion zurückzugeben oder die Ausführung einer Funktion zu beenden und zum Aufrufer zurückzukehren. `break` oder `return` darf nur als letzte Anweisung eines Blocks stehen.

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

## Lokale und globale Variablen sowie lexikalische Gültigkeitsbereiche {#locals-globals-and-lexical-scoping}

Alle Variablen, die du deklarierst, sind standardmäßig global. Das bedeutet, dass sie in allen Teilen des Lua-Laufzeitkontexts verfügbar sind. Du kannst Variablen ausdrücklich als `local` deklarieren. Dann existiert die Variable nur innerhalb des aktuellen Gültigkeitsbereichs.

Jede Lua-Quelldatei definiert einen eigenen Gültigkeitsbereich. Deklarationen mit `local` auf der obersten Ebene einer Datei bedeuten, dass die Variable lokal zur Lua-Skriptdatei ist. Jede Funktion erzeugt einen weiteren verschachtelten Gültigkeitsbereich, und jeder Block einer Kontrollstruktur erzeugt zusätzliche Gültigkeitsbereiche. Mit den Schlüsselwörtern `do` und `end` kannst du ausdrücklich einen Gültigkeitsbereich erstellen. Lua hat lexikalische Gültigkeitsbereiche. Das bedeutet, dass ein Gültigkeitsbereich vollen Zugriff auf _lokale_ Variablen des umgebenden Gültigkeitsbereichs hat. Beachte, dass lokale Variablen vor ihrer Verwendung deklariert werden müssen.

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

Wenn du Funktionen in einer Skriptdatei als `local` deklarierst, was in der Regel sinnvoll ist, musst du auf die Reihenfolge des Codes achten. Wenn sich Funktionen gegenseitig aufrufen, kannst du Vorwärtsdeklarationen verwenden.

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

Wenn du eine Funktion innerhalb einer anderen Funktion schreibst, hat auch sie vollen Zugriff auf die lokalen Variablen der umgebenden Funktion. Dies ist ein sehr leistungsfähiges Konstrukt.

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

## Überschattung von Variablen {#variable-shadowing}

Lokale Variablen, die in einem Block deklariert werden, überschatten gleichnamige Variablen aus einem umgebenden Block.

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

## Koroutinen {#coroutines}

Funktionen werden vom Anfang bis zum Ende ausgeführt und können nicht mittendrin angehalten werden. Koroutinen ermöglichen genau das, was in manchen Fällen sehr praktisch sein kann. Angenommen, wir möchten eine ganz bestimmte Animation Bild für Bild erstellen, bei der wir ein Spielobjekt von der y-Position `0` aus in den Frames 1 bis 5 zu bestimmten y-Positionen bewegen. Wir könnten dies mit einem Zähler in der Funktion `update()` (siehe unten) und einer Liste der Positionen lösen. Mit einer Koroutine erhalten wir jedoch eine sehr übersichtliche Implementierung, die sich leicht erweitern und bearbeiten lässt. Der gesamte Zustand ist in der Koroutine selbst enthalten.

Wenn eine Koroutine pausiert, gibt sie die Steuerung an den Aufrufer zurück, merkt sich aber ihre Ausführungsposition, sodass sie später dort fortfahren kann.

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


## Lua-Kontexte in Defold {#lua-contexts-in-defold}

Alle Variablen, die du deklarierst, sind standardmäßig global. Das bedeutet, dass sie in allen Teilen des Lua-Laufzeitkontexts verfügbar sind. Defold hat in *game.project* die Einstellung *shared_state*, die diesen Kontext steuert. Wenn die Option aktiviert ist, werden alle Skripte, GUI-Skripte und das Render-Skript im selben Lua-Kontext ausgewertet, und globale Variablen sind überall sichtbar. Wenn die Option deaktiviert ist, führt die Engine Skripte, GUI-Skripte und das Render-Skript in getrennten Kontexten aus.

![Kontexte](images/lua/lua_contexts.png)

In Defold kannst du dieselbe Skriptdatei in mehreren separaten Komponenten (components) von Spielobjekten verwenden. Alle lokal deklarierten Variablen werden von den Komponenten gemeinsam genutzt, die dieselbe Skriptdatei ausführen.

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

## Überlegungen zur Leistung {#performance-considerations}

In einem leistungsintensiven Spiel, das mit flüssigen 60 FPS laufen soll, können kleine Fehler bei der Leistung große Auswirkungen auf das Spielerlebnis haben. Es gibt einige einfache allgemeine Punkte zu beachten und einige Dinge, die zunächst unproblematisch erscheinen können.

Beginnen wir mit den einfachen Dingen. Im Allgemeinen ist es sinnvoll, übersichtlichen Code ohne unnötige Schleifen zu schreiben. Manchmal musst du über Listen von Elementen iterieren, aber sei vorsichtig, wenn die Liste entsprechend groß ist. Dieses Beispiel benötigt auf einem recht leistungsfähigen Laptop etwas mehr als 1 Millisekunde. Das kann entscheidend sein, wenn jeder Frame nur 16 Millisekunden dauert (bei 60 FPS) und die Engine, das Render-Skript, die Physiksimulation usw. bereits einen Teil davon beanspruchen.

```lua
local t = socket.gettime()
local table = {}
for i=1,2000 do
    table[i] = vmath.vector3(i, i, i)
end
print((socket.gettime() - t) * 1000)

-- DEBUG:SCRIPT: 0.40388
```

Verwende den von `socket.gettime()` zurückgegebenen Wert (Sekunden seit der Systemepoche), um die Ausführungszeit von verdächtigem Code zu messen.

## Speicher und automatische Speicherbereinigung {#memory-and-garbage-collection}

Die automatische Speicherbereinigung von Lua läuft standardmäßig im Hintergrund und gibt Speicher frei, den die Lua-Laufzeitumgebung zugewiesen hat. Die Bereinigung großer Mengen nicht mehr benötigter Daten kann viel Zeit beanspruchen. Daher ist es sinnvoll, die Anzahl der Objekte, die bereinigt werden müssen, gering zu halten:

* Lokale Variablen selbst verursachen keine Kosten und erzeugen keine zu bereinigenden Daten. (z. B. `local v = 42`)
* Jede _neue, eindeutige_ Zeichenfolge erzeugt ein neues Objekt. Mit `local s = "some_string"` wird ein neues Objekt erstellt und `s` darauf gesetzt. Die lokale Variable `s` selbst erzeugt keine zu bereinigenden Daten, das Zeichenfolgenobjekt jedoch schon. Die mehrfache Verwendung derselben Zeichenfolge verursacht keinen zusätzlichen Speicherbedarf.
* Jedes Mal, wenn ein Tabellenkonstruktor (`{ ... }`) ausgeführt wird, entsteht eine neue Tabelle.
* Die Ausführung einer _Funktionsanweisung_ erzeugt ein Closure-Objekt. (Gemeint ist die Ausführung der Anweisung `function () ... end`, nicht der Aufruf einer definierten Funktion.)
* Funktionen mit variabler Argumentzahl (`function(v, ...) end`) erzeugen bei jedem _Aufruf_ eine Tabelle für die Auslassungspunkte (in Lua vor Version 5.2 oder wenn LuaJIT nicht verwendet wird).
* `dofile()` und `dostring()`
* Userdata-Objekte

In vielen Fällen kannst du das Erstellen neuer Objekte vermeiden und stattdessen bereits vorhandene wiederverwenden. Beispielsweise steht häufig Folgendes am Ende jedes Aufrufs von `update()`:

```lua
-- Reset velocity
self.velocity = vmath.vector3()
```

Es wird leicht vergessen, dass jeder Aufruf von `vmath.vector3()` ein neues Objekt erzeugt. Sehen wir uns an, wie viel Speicher ein `vector3` benötigt:

```lua
print(collectgarbage("count") * 1024)       -- 88634
local v = vmath.vector3()
print(collectgarbage("count") * 1024)       -- 88704. 70 bytes in total has been allocated
```

Zwischen den Aufrufen von `collectgarbage()` sind 70 Byte hinzugekommen. Darin sind jedoch auch Speicherzuweisungen enthalten, die über das Objekt `vector3` hinausgehen. Jede Ausgabe des Ergebnisses von `collectgarbage()` erzeugt eine Zeichenfolge, die selbst 22 Byte an zu bereinigenden Daten hinzufügt:

```lua
print(collectgarbage("count") * 1024)       -- 88611
print(collectgarbage("count") * 1024)       -- 88633. 22 bytes allocated
```

Ein `vector3` benötigt also 70-22=48 Byte. Das ist nicht viel, aber wenn du in einem Spiel mit 60 FPS in jedem Frame _eines_ erstellst, entstehen plötzlich 2,8 kB an zu bereinigenden Daten pro Sekunde. Bei 360 Skriptkomponenten, die in jedem Frame jeweils ein `vector3` erstellen, entsteht 1 MB an zu bereinigenden Daten pro Sekunde. Die Zahlen können sich sehr schnell summieren. Wenn die Lua-Laufzeitumgebung den Speicher bereinigt, kann das viele kostbare Millisekunden beanspruchen---besonders auf mobilen Plattformen.

Eine Möglichkeit, Speicherzuweisungen zu vermeiden, besteht darin, ein `vector3` zu erstellen und dann mit demselben Objekt weiterzuarbeiten. Um beispielsweise ein `vector3` zurückzusetzen, können wir folgendes Konstrukt verwenden:

```lua
-- Instead of doing self.velocity = vmath.vector3() which creates a new object
-- we zero an existing velocity vector object's components
self.velocity.x = 0
self.velocity.y = 0
self.velocity.z = 0
```

Das standardmäßige Verfahren zur automatischen Speicherbereinigung ist für manche zeitkritischen Anwendungen möglicherweise nicht optimal. Wenn dein Spiel oder deine App ruckelt, kannst du das Verhalten der Speicherbereinigung in Lua über die Lua-Funktion [`collectgarbage()`](/ref/base/#collectgarbage) anpassen. Beispielsweise kannst du die Speicherbereinigung in jedem Frame mit einem niedrigen Wert für `step` kurz ausführen lassen. Um eine Vorstellung davon zu bekommen, wie viel Speicher dein Spiel oder deine App benötigt, kannst du die aktuelle Menge an zu bereinigenden Bytes so ausgeben:

```lua
print(collectgarbage("count") * 1024)
```

## Bewährte Verfahren {#best-practices}

Eine häufige Überlegung beim Entwurf einer Implementierung ist, wie Code für gemeinsam genutzte Verhaltensweisen strukturiert werden sollte. Dafür gibt es mehrere Ansätze.

Verhaltensweisen in einem Modul
: Wenn du eine Verhaltensweise in einem Modul kapselst, kannst du Code leicht zwischen den Skriptkomponenten verschiedener Spielobjekte (und GUI-Skripten) gemeinsam nutzen. Beim Schreiben von Modulfunktionen ist es in der Regel am besten, streng funktionalen Code zu schreiben. Es gibt Fälle, in denen ein gespeicherter Zustand oder Seiteneffekte erforderlich sind oder zu einem übersichtlicheren Entwurf führen. Wenn du den internen Zustand im Modul speichern musst, beachte, dass Komponenten Lua-Kontexte gemeinsam nutzen. Einzelheiten findest du in der [Dokumentation zu Modulen](/manuals/modules).

  ![Modul](images/lua/lua_module.png)

  Auch wenn Modulcode das Innere eines Spielobjekts direkt ändern kann, indem du `self` an eine Modulfunktion übergibst, raten wir dringend davon ab, da dadurch eine sehr enge Kopplung entsteht.

Ein Hilfsspielobjekt mit gekapseltem Verhalten
: So wie du Skriptcode in einem Lua-Modul kapseln kannst, kannst du ihn auch in einem Spielobjekt mit einer Skriptkomponente kapseln. Der Unterschied besteht darin, dass du bei der Kapselung in einem Spielobjekt ausschließlich über Nachrichten mit ihm kommunizieren kannst.

  ![Hilfsspielobjekt](images/lua/lua_helper.png)

Spielobjekt und Hilfsobjekt für das Verhalten in einer Sammlung gruppieren
: Bei diesem Entwurf kannst du ein Spielobjekt für eine Verhaltensweise erstellen, das automatisch auf ein anderes Zielspielobjekt einwirkt. Dies geschieht entweder über einen vordefinierten Namen, an den der Name des Zielspielobjekts angepasst werden muss, oder über eine URL in `go.property()`, die auf das Zielspielobjekt verweist.

  ![Sammlung](images/lua/lua_collection.png)

  Der Vorteil dieses Aufbaus ist, dass du ein Spielobjekt mit einer Verhaltensweise in einer Sammlung (collection) ablegen kannst, die das Zielobjekt enthält. Es ist kein zusätzlicher Code erforderlich.

  In Situationen, in denen du große Mengen von Spielobjekten verwalten musst, ist dieser Entwurf nicht vorzuziehen. Das Verhaltensobjekt wird für jede Instanz dupliziert, und jedes Objekt benötigt Speicher.
