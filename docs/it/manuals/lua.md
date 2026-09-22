---
title: Programmazione Lua in Defold
brief: Questo manuale offre una breve introduzione alle basi della programmazione Lua in generale e agli aspetti da considerare quando usi Lua in Defold.
---

# Lua in Defold

Il motore Defold integra il linguaggio Lua per la scrittura di script. Lua è un linguaggio dinamico leggero, potente, veloce e facile da integrare. È ampiamente utilizzato come linguaggio di scripting per videogiochi. I programmi Lua si scrivono con una semplice sintassi procedurale. Il linguaggio è tipizzato dinamicamente e viene eseguito da un interprete di bytecode. Offre una gestione automatica della memoria con garbage collection incrementale.

Questo manuale offre una breve introduzione alle basi della programmazione Lua in generale e agli aspetti da considerare quando usi Lua in Defold. Se hai già esperienza con Python, Perl, Ruby, JavaScript o un linguaggio dinamico simile, potrai iniziare piuttosto rapidamente. Se invece ti avvicini alla programmazione per la prima volta, puoi cominciare con un libro su Lua rivolto ai principianti. Ce ne sono molti tra cui scegliere.

## Versioni di Lua {#lua-versions}

Defold usa [LuaJIT](https://luajit.org/), una versione di Lua altamente ottimizzata, adatta ai giochi e ad altri software in cui le prestazioni sono fondamentali. È pienamente compatibile con Lua 5.1 e supporta tutte le funzioni delle librerie standard di Lua e l'intero insieme di funzioni dell'API Lua/C.

LuaJIT aggiunge inoltre diverse [estensioni del linguaggio](https://luajit.org/extensions.html) e alcune funzionalità di Lua 5.2 e 5.3.

Puntiamo a mantenere Defold uniforme su tutte le piattaforme, ma attualmente esistono alcune piccole differenze nella versione del linguaggio Lua tra una piattaforma e l'altra:
* iOS non consente la compilazione JIT.
* Nintendo Switch non consente la compilazione JIT.
* HTML5 usa Lua 5.1.4 al posto di LuaJIT.

::: important
Per garantire che il tuo gioco funzioni su tutte le piattaforme supportate, ti consigliamo vivamente di usare SOLO le funzionalità del linguaggio disponibili in Lua 5.1.
:::

### Librerie standard ed estensioni {#standard-libraries-and-extensions}
Defold include tutte le [librerie standard di Lua 5.1](http://www.lua.org/manual/5.1/manual.html#5), oltre a una libreria per i socket e una per le operazioni sui bit:

  - base (`assert()`, `error()`, `print()`, `ipairs()`, `require()` ecc.)
  - coroutine
  - package
  - string
  - table
  - math
  - io
  - os
  - debug
  - socket (da [LuaSocket](https://github.com/diegonehab/luasocket))
  - bitop (da [BitOp](http://bitop.luajit.org/api.html))

Tutte le librerie sono descritte nella [documentazione di riferimento delle API](/ref/go).

## Libri e risorse su Lua {#lua-books-and-resources}

### Risorse online {#online-resources}
* [Programming in Lua (prima edizione)](http://www.lua.org/pil/contents.html) Le edizioni successive sono disponibili in formato cartaceo.
* [Manuale di riferimento di Lua 5.1](http://www.lua.org/manual/5.1/)
* [Impara Lua in 15 minuti](http://tylerneylon.com/a/learn-lua/)
* [Awesome Lua - sezione tutorial](https://github.com/LewisJEllis/awesome-lua#tutorials)

### Libri {#books}
* [Programming in Lua](https://www.amazon.com/gp/product/8590379868/ref=dbs_a_def_rwt_hsch_vapi_taft_p1_i0) - Programming in Lua è il libro ufficiale sul linguaggio e offre solide basi a ogni programmatore che desideri usare Lua. È scritto da Roberto Ierusalimschy, il principale progettista del linguaggio.
* [Lua programming gems](https://www.amazon.com/Programming-Gems-Luiz-Henrique-Figueiredo/dp/8590379841) - Questa raccolta di articoli riunisce parte delle conoscenze e delle pratiche consolidate per programmare bene in Lua.
* [Manuale di riferimento di Lua 5.1](https://www.amazon.com/gp/product/8590379833/ref=dbs_a_def_rwt_hsch_vapi_taft_p1_i4) - Disponibile anche online (vedi sopra)
* [Beginning Lua Programming](https://www.amazon.com/Beginning-Lua-Programming-Kurt-Jung/dp/0470069171)

### Video {#videos}
* [Impara Lua in un solo video](https://www.youtube.com/watch?v=iMacxZQMPXs)

## Sintassi {#syntax}

I programmi hanno una sintassi semplice e facile da leggere. Le istruzioni si scrivono una per riga, senza doverne segnalare la fine. Facoltativamente, puoi usare il punto e virgola `;` per separarle. I blocchi di codice sono delimitati da parole chiave e terminano con la parola chiave `end`. I commenti possono occupare un blocco oppure estendersi fino alla fine della riga:

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

## Variabili e tipi di dati {#variables-and-data-types}

Lua è tipizzato dinamicamente: i tipi appartengono ai valori, non alle variabili. 
A differenza dei linguaggi tipizzati staticamente, puoi assegnare liberamente qualsiasi valore a qualsiasi variabile. 

In Lua esistono otto tipi di base:

`nil`
: Questo tipo ha un solo valore, `nil`. Di solito rappresenta l'assenza di un valore utile, per esempio nel caso delle variabili a cui non è stato assegnato alcun valore.

  ```lua
  print(my_var) -- will print 'nil' since 'my_var' is not yet assigned a value
  ```

boolean
: Può avere il valore `true` oppure `false`. Le condizioni che valgono `false` o `nil` sono considerate false. Qualsiasi altro valore le rende vere.

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
: I numeri sono rappresentati internamente come numeri _interi_ a 64 bit oppure numeri _in virgola mobile_ a 64 bit. Lua converte automaticamente tra queste rappresentazioni quando necessario, quindi in genere non devi preoccupartene.

  ```lua
  print(10) --> prints '10'
  print(10.0) --> '10'
  print(10.000000000001) --> '10.000000000001'

  a = 5 -- integer
  b = 7/3 -- float
  print(a - b) --> '2.6666666666667'
  ```

string
: Le stringhe sono sequenze immutabili di byte che possono contenere qualsiasi valore a 8 bit, compresi gli zeri incorporati (`\0`). Lua non fa alcuna ipotesi sul contenuto di una stringa, quindi puoi usarla per memorizzare qualsiasi dato. Le stringhe letterali si scrivono tra apici singoli o doppi. Lua converte tra numeri e stringhe durante l'esecuzione. Le stringhe possono essere concatenate con l'operatore `..`.

  Le stringhe possono contenere le seguenti sequenze di escape in stile C:

  | Sequenza | Carattere |
  | -------- | --------- |
  | `\a`     | segnale acustico |
  | `\b`     | ritorno di un carattere |
  | `\f`     | avanzamento pagina |
  | `\n`     | nuova riga |
  | `\r`     | ritorno carrello |
  | `\t`     | tabulazione orizzontale |
  | `\v`     | tabulazione verticale |
  | `\\`     | barra inversa |
  | `\"`     | apice doppio |
  | `\'`     | apice singolo |
  | `\[`     | parentesi quadra aperta |
  | `\]`     | parentesi quadra chiusa |
  | `\ddd`   | carattere indicato dal suo valore numerico, dove `ddd` è una sequenza di un massimo di tre cifre _decimali_ |

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
: In Lua le funzioni sono valori di prima classe: puoi passarle come parametri ad altre funzioni e restituirle come valori. Le variabili a cui assegni una funzione contengono un riferimento alla funzione. Puoi assegnare funzioni anonime alle variabili, ma Lua offre una sintassi semplificata (`function name(param1, param2) ... end`) per comodità.

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
: Le tabelle sono l'unico tipo di Lua per strutturare i dati. Sono _oggetti_ di tipo array associativo, usati per rappresentare elenchi, array, sequenze, tabelle di simboli, insiemi, record, grafi, alberi e così via. Le tabelle sono sempre anonime e le variabili a cui assegni una tabella non contengono la tabella stessa, ma un riferimento a essa. Quando inizializzi una tabella come sequenza, il primo indice è `1`, non `0`.

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
: `userdata` consente di memorizzare dati C arbitrari nelle variabili Lua. Defold usa gli oggetti Lua `userdata` per memorizzare valori hash (hash), oggetti URL (url), oggetti matematici (vector3, vector4, matrix4, quaternion), oggetti di gioco, nodi GUI (node), predicati di rendering (predicate), destinazioni di rendering (render_target) e buffer di costanti di rendering (constant_buffer)

thread
: I thread rappresentano flussi di esecuzione indipendenti e sono usati per implementare le coroutine. Vedi sotto per i dettagli.

## Operatori {#operators}

Operatori aritmetici
: Gli operatori matematici `+`, `-`, `*`, `/`, l'operatore unario `-` (negazione) e l'operatore di elevamento a potenza `^`.

  ```lua
  a = -1
  print(a * 2 + 3 / 4^5) --> -1.9970703125
  ```

  Lua converte automaticamente tra numeri e stringhe durante l'esecuzione. Qualsiasi operazione numerica applicata a una stringa tenta di convertirla in un numero:

  ```lua
  print("10" + 1) --> 11
  ```

Operatori relazionali e di confronto
: `<` (minore di), `>` (maggiore di), `<=` (minore o uguale), `>=` (maggiore o uguale), `==` (uguale), `~=` (diverso). Questi operatori restituiscono sempre `true` o `false`. Valori di tipi diversi sono considerati diversi. Se i tipi coincidono, vengono confrontati in base al valore. Lua confronta tabelle, `userdata` e funzioni per riferimento. Due valori di questi tipi sono considerati uguali solo se fanno riferimento allo stesso oggetto.

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

Operatori logici
: `and`, `or` e `not`. `and` restituisce il primo argomento se è `false`, altrimenti restituisce il secondo argomento. `or` restituisce il primo argomento se non è `false`, altrimenti restituisce il secondo argomento.

  ```lua
  print(true or false) --> true
  print(true and false) --> false
  print(not false) --> true

  if a == 5 and b == 6 then
      print("a is 5 and b is 6")
  end
  ```

Concatenazione
: Le stringhe possono essere concatenate con l'operatore `..`. I numeri vengono convertiti in stringhe quando vengono concatenati.

  ```lua
  print("donkey" .. "kong") --> "donkeykong"
  print(1 .. 2) --> "12"
  ```

Lunghezza
: L'operatore unario di lunghezza `#`. La lunghezza di una stringa è il suo numero di byte. La lunghezza di una tabella è la lunghezza della sua sequenza, ossia il numero di indici numerati a partire da `1` e in ordine crescente il cui valore non è `nil`. Nota: se la sequenza contiene dei "buchi" con valore `nil`, la lunghezza può corrispondere a qualsiasi indice che precede un valore `nil`.

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

## Controllo del flusso {#flow-control}

Lua offre il consueto insieme di costrutti per il controllo del flusso.

if---then---else
: Verifica una condizione ed esegue la parte `then` se la condizione è vera, altrimenti esegue la parte `else` (facoltativa). Invece di annidare istruzioni `if`, puoi usare `elseif`. Questo sostituisce l'istruzione switch, che Lua non prevede.

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
: Verifica una condizione ed esegue il blocco finché è vera.

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
: Ripete il blocco finché una condizione diventa vera. La condizione viene verificata dopo il corpo del ciclo, che quindi viene eseguito almeno una volta.

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
: Lua ha due tipi di ciclo `for`: numerico e generico. Il `for` numerico accetta 2 o 3 valori numerici, mentre il `for` generico scorre tutti i valori restituiti da una funzione _iteratore_.

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

break e return
: Usa l'istruzione `break` per uscire dal blocco interno di un ciclo `for`, `while` o `repeat`. Usa `return` per restituire un valore da una funzione oppure per terminare l'esecuzione di una funzione e tornare al chiamante. `break` e `return` possono comparire solo come ultima istruzione di un blocco.

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

## Variabili locali, globali e ambito lessicale {#locals-globals-and-lexical-scoping}

Tutte le variabili che dichiari sono globali per impostazione predefinita: sono disponibili in ogni parte del contesto di runtime Lua. Puoi dichiarare esplicitamente le variabili come `local`, in modo che esistano solo nell'ambito corrente.

Ogni file sorgente Lua definisce un ambito distinto. Le dichiarazioni `local` al livello più esterno di un file rendono la variabile locale al file di script Lua. Ogni funzione crea un ulteriore ambito annidato e ogni blocco di una struttura di controllo crea altri ambiti. Puoi creare esplicitamente un ambito con le parole chiave `do` ed `end`. Lua usa un ambito lessicale: un ambito ha pieno accesso alle variabili _locali_ dell'ambito che lo racchiude. Tieni presente che le variabili locali devono essere dichiarate prima di essere usate.

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

Se dichiari funzioni `local` in un file di script (una buona pratica in generale), devi fare attenzione all'ordine del codice. Puoi usare dichiarazioni anticipate se hai funzioni che si chiamano a vicenda.

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

Se scrivi una funzione all'interno di un'altra funzione, anche questa ha pieno accesso alle variabili locali della funzione che la racchiude. È un costrutto molto potente.

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

## Oscuramento delle variabili {#variable-shadowing}

Le variabili locali dichiarate in un blocco oscurano le variabili con lo stesso nome dichiarate in un blocco che lo racchiude.

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

## Coroutine {#coroutines}

Le funzioni vengono eseguite dall'inizio alla fine e non è possibile interromperle a metà. Le coroutine lo consentono, e in alcuni casi questo può essere molto utile. Supponiamo di voler creare un'animazione molto precisa, fotogramma per fotogramma, in cui spostiamo un oggetto di gioco dalla posizione y `0` a determinate posizioni y dal fotogramma 1 al fotogramma 5. Potremmo risolvere il problema con un contatore nella funzione `update()` (vedi sotto) e un elenco di posizioni. Con una coroutine, però, otteniamo un'implementazione molto chiara, facile da estendere e usare. Tutto lo stato è contenuto nella coroutine stessa.

Quando una coroutine si sospende, restituisce il controllo al chiamante, ma ricorda il punto di esecuzione per poter riprendere da lì in seguito.

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


## Contesti Lua in Defold {#lua-contexts-in-defold}

Tutte le variabili che dichiari sono globali per impostazione predefinita: sono disponibili in ogni parte del contesto di runtime Lua. Defold ha un'impostazione *shared_state* in *game.project* che controlla questo contesto. Se l'opzione è attiva, tutti gli script, gli script GUI e lo script di rendering vengono valutati nello stesso contesto Lua e le variabili globali sono visibili ovunque. Se l'opzione non è attiva, il motore esegue gli script, gli script GUI e lo script di rendering in contesti separati.

![Contesti](images/lua/lua_contexts.png)

Defold consente di usare lo stesso file di script in diversi componenti di oggetti di gioco. Le variabili dichiarate localmente sono condivise tra i componenti che eseguono lo stesso file di script.

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

## Considerazioni sulle prestazioni {#performance-considerations}

In un gioco ad alte prestazioni progettato per girare fluidamente a 60 FPS, piccoli errori che incidono sulle prestazioni possono avere un grande impatto sull'esperienza. Ci sono alcuni semplici aspetti generali da considerare e altri che a prima vista potrebbero non sembrare problematici.

Cominciamo dagli aspetti più semplici. In generale è bene scrivere codice lineare che non contenga cicli inutili. A volte è necessario scorrere elenchi di elementi, ma fai attenzione se l'elenco è piuttosto grande. Questo esempio viene eseguito in poco più di 1 millisecondo su un portatile di buon livello: può fare la differenza quando ogni fotogramma dura solo 16 millisecondi (a 60 FPS) e il motore, lo script di rendering, la simulazione fisica e così via ne consumano già una parte.

```lua
local t = socket.gettime()
local table = {}
for i=1,2000 do
    table[i] = vmath.vector3(i, i, i)
end
print((socket.gettime() - t) * 1000)

-- DEBUG:SCRIPT: 0.40388
```

Usa il valore restituito da `socket.gettime()` (i secondi trascorsi dall'epoca di riferimento del sistema) per misurare le prestazioni del codice sospetto.

## Memoria e garbage collection {#memory-and-garbage-collection}

Per impostazione predefinita, la garbage collection di Lua viene eseguita automaticamente in background e recupera la memoria allocata dal runtime Lua. Recuperare una grande quantità di memoria inutilizzata può richiedere molto tempo, quindi è bene limitare il numero di oggetti che devono essere raccolti:

* Le variabili locali, di per sé, non hanno costi e non generano memoria da recuperare con la garbage collection. (Per esempio `local v = 42`)
* Ogni stringa _nuova e distinta_ crea un nuovo oggetto. Scrivere `local s = "some_string"` crea un nuovo oggetto e lo assegna a `s`. La variabile locale `s`, di per sé, non genera memoria da recuperare con la garbage collection, mentre l'oggetto stringa sì. Usare più volte la stessa stringa non comporta ulteriori costi di memoria.
* Ogni volta che viene eseguito un costruttore di tabella (`{ ... }`), viene creata una nuova tabella.
* L'esecuzione di un'_istruzione function_ crea un oggetto closure. (Si intende l'esecuzione dell'istruzione `function () ... end`, non la chiamata a una funzione definita)
* Le funzioni con un numero variabile di argomenti (`function(v, ...) end`) creano una tabella per i puntini di sospensione ogni volta che la funzione viene _chiamata_ (nelle versioni di Lua precedenti alla 5.2 o se non si usa LuaJIT).
* `dofile()` e `dostring()`
* Oggetti userdata

In molti casi puoi evitare di creare nuovi oggetti e riutilizzare quelli che hai già. Per esempio, questa istruzione è comune alla fine di ogni `update()`:

```lua
-- Reset velocity
self.velocity = vmath.vector3()
```

È facile dimenticare che ogni chiamata a `vmath.vector3()` crea un nuovo oggetto. Vediamo quanta memoria usa un `vector3`:

```lua
print(collectgarbage("count") * 1024)       -- 88634
local v = vmath.vector3()
print(collectgarbage("count") * 1024)       -- 88704. 70 bytes in total has been allocated
```

Tra le chiamate a `collectgarbage()` sono stati aggiunti 70 byte, ma questo include anche allocazioni oltre a quella dell'oggetto `vector3`. Ogni stampa del risultato di `collectgarbage()` costruisce una stringa che, da sola, aggiunge 22 byte di memoria da recuperare:

```lua
print(collectgarbage("count") * 1024)       -- 88611
print(collectgarbage("count") * 1024)       -- 88633. 22 bytes allocated
```

Un `vector3` occupa quindi 70-22=48 byte. Non è molto, ma se ne crei _uno_ a ogni fotogramma in un gioco a 60 FPS, diventano 2,8 kB di memoria da recuperare al secondo. Con 360 componenti script che creano ciascuno un `vector3` a ogni fotogramma, si arriva a 1 MB di memoria da recuperare generata ogni secondo. Le quantità possono crescere molto rapidamente. Quando il runtime Lua esegue la garbage collection, può consumare molti millisecondi preziosi---soprattutto sulle piattaforme mobili.

Un modo per evitare allocazioni è creare un `vector3` e continuare a lavorare con lo stesso oggetto. Per esempio, per azzerare un `vector3` possiamo usare il seguente costrutto:

```lua
-- Instead of doing self.velocity = vmath.vector3() which creates a new object
-- we zero an existing velocity vector object's components
self.velocity.x = 0
self.velocity.y = 0
self.velocity.z = 0
```

La modalità predefinita di garbage collection potrebbe non essere ottimale per alcune applicazioni con vincoli temporali stringenti. Se noti degli scatti nel gioco o nell'applicazione, puoi regolare il modo in cui Lua esegue la garbage collection tramite la funzione Lua [`collectgarbage()`](/ref/base/#collectgarbage). Puoi, per esempio, eseguire il raccoglitore per un breve intervallo a ogni fotogramma con un valore basso di `step`. Per farti un'idea di quanta memoria consumi il gioco o l'applicazione, puoi stampare la quantità corrente di byte gestiti dalla garbage collection con:

```lua
print(collectgarbage("count") * 1024)
```

## Buone pratiche {#best-practices}

Un aspetto comune da considerare nella progettazione di un'implementazione è come strutturare il codice per i comportamenti condivisi. Sono possibili diversi approcci.

Comportamenti in un modulo
: Incapsulare un comportamento in un modulo consente di condividere facilmente il codice tra i componenti script di diversi oggetti di gioco (e gli script GUI). Quando scrivi le funzioni di un modulo, in genere è meglio usare codice strettamente funzionale. In alcuni casi, memorizzare lo stato o produrre effetti collaterali è necessario (oppure porta a una progettazione più chiara). Se devi memorizzare lo stato interno nel modulo, ricorda che i componenti condividono i contesti Lua. Consulta la [documentazione sui moduli](/manuals/modules) per i dettagli.

  ![Modulo](images/lua/lua_module.png)

  Inoltre, anche se il codice di un modulo può modificare direttamente lo stato interno di un oggetto di gioco (passando `self` a una funzione del modulo), ti sconsigliamo vivamente di farlo perché creeresti un accoppiamento molto stretto.

Un oggetto di gioco ausiliario con comportamento incapsulato
: Proprio come puoi racchiudere il codice di uno script in un modulo Lua, puoi racchiuderlo in un oggetto di gioco con un componente script. La differenza è che, racchiudendolo in un oggetto di gioco, puoi comunicare con esso esclusivamente tramite lo scambio di messaggi.

  ![Oggetto ausiliario](images/lua/lua_helper.png)

Raggruppare un oggetto di gioco e un oggetto ausiliario che ne gestisce il comportamento in una collezione
: Con questa progettazione puoi creare un oggetto di gioco che definisce un comportamento e agisce automaticamente su un altro oggetto di gioco di destinazione, identificato da un nome predefinito (l'utente deve rinominare l'oggetto di destinazione in modo che corrisponda) oppure da un URL `go.property()` che punta all'oggetto di gioco di destinazione.

  ![Collezione](images/lua/lua_collection.png)

  Il vantaggio di questa configurazione è che puoi inserire un oggetto di gioco che definisce un comportamento in una collezione contenente l'oggetto di destinazione. Non serve codice aggiuntivo.

  Nelle situazioni in cui devi gestire grandi quantità di oggetti di gioco, questa progettazione non è consigliabile: l'oggetto che definisce il comportamento viene duplicato per ogni istanza e ogni oggetto occupa memoria.
