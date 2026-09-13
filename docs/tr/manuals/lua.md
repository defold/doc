---
title: Defold'da Lua programlama
brief: Bu kılavuz, genel olarak Lua programlamanın temellerine ve Defold'da Lua ile çalışırken dikkat etmeniz gerekenlere kısa bir giriş sunar.
---

# Defold'da Lua

Defold motoru, betik (script) yazımı için gömülü Lua dilini kullanır. Lua güçlü, hızlı ve başka yazılımlara gömülmesi kolay, hafif bir dinamik dildir. Video oyunlarında betik dili olarak yaygın biçimde kullanılır. Lua programları basit bir yordamsal sözdizimiyle yazılır. Dil dinamik türlendirmelidir ve bir bayt kodu (bytecode) yorumlayıcısı tarafından çalıştırılır. Artımlı çöp toplama (incremental garbage collection) ile otomatik bellek yönetimi sunar.

Bu kılavuz, genel olarak Lua programlamanın temellerine ve Defold'da Lua ile çalışırken dikkat etmeniz gerekenlere kısa bir giriş sunar. Python, Perl, Ruby, JavaScript veya benzer bir dinamik dil konusunda biraz deneyiminiz varsa oldukça hızlı ilerleyebilirsiniz. Programlamaya yeni başlıyorsanız başlangıç düzeyine yönelik bir Lua kitabıyla başlamak isteyebilirsiniz. Aralarından seçim yapabileceğiniz pek çok kitap vardır.

## Lua sürümleri

Defold, Lua'nın oyunlarda ve performansın kritik olduğu diğer yazılımlarda kullanıma uygun, yüksek ölçüde optimize edilmiş bir sürümü olan [LuaJIT](https://luajit.org/) kullanır. Lua 5.1'den geçişte tam uyumluluk sağlar ve tüm standart Lua kütüphanesi işlevleriyle Lua/C API işlevlerinin tamamını destekler.

LuaJIT ayrıca çeşitli [dil uzantıları](https://luajit.org/extensions.html) ile bazı Lua 5.2 ve 5.3 özellikleri ekler.

Defold'un tüm platformlarda aynı şekilde çalışmasını hedefliyoruz, ancak şu anda platformlar arasında Lua dili sürümü açısından birkaç küçük farklılık bulunuyor:
* iOS, JIT kod derlemesine izin vermez.
* Nintendo Switch, JIT kod derlemesine izin vermez.
* HTML5, LuaJIT yerine Lua 5.1.4 kullanır.

::: important
Oyununuzun desteklenen tüm platformlarda çalışmasını garantilemek için YALNIZCA Lua 5.1 dil özelliklerini kullanmanızı önemle öneririz.
:::

### Standart kütüphaneler ve uzantılar
Defold, [Lua 5.1 standart kütüphanelerinin](http://www.lua.org/manual/5.1/manual.html#5) tamamının yanı sıra bir soket ve bir bit işlemleri kütüphanesi içerir:

  - base (`assert()`, `error()`, `print()`, `ipairs()`, `require()` vb.)
  - coroutine
  - package
  - string
  - table
  - math
  - io
  - os
  - debug
  - socket ([LuaSocket](https://github.com/diegonehab/luasocket) kaynaklı)
  - bitop ([BitOp](http://bitop.luajit.org/api.html) kaynaklı)

Tüm kütüphaneler [API başvuru belgelerinde](/ref/go) açıklanmıştır.

## Lua kitapları ve kaynakları

### Çevrimiçi kaynaklar
* [Lua ile programlama (ilk baskı)](http://www.lua.org/pil/contents.html) Sonraki baskılar basılı olarak bulunabilir.
* [Lua 5.1 başvuru kılavuzu](http://www.lua.org/manual/5.1/)
* [15 dakikada Lua öğrenin](http://tylerneylon.com/a/learn-lua/)
* [Awesome Lua - öğreticiler bölümü](https://github.com/LewisJEllis/awesome-lua#tutorials)

### Kitaplar
* [Lua ile programlama](https://www.amazon.com/gp/product/8590379868/ref=dbs_a_def_rwt_hsch_vapi_taft_p1_i0) - Programming in Lua, dilin resmî kitabıdır ve Lua kullanmak isteyen her programcıya sağlam bir temel sunar. Dilin baş mimarı Roberto Ierusalimschy tarafından yazılmıştır.
* [Lua programlamanın incileri](https://www.amazon.com/Programming-Gems-Luiz-Henrique-Figueiredo/dp/8590379841) - Bu makale derlemesi, Lua'da iyi programlama konusunda birikmiş bilgi ve uygulamaların bir bölümünü bir araya getirir.
* [Lua 5.1 başvuru kılavuzu](https://www.amazon.com/gp/product/8590379833/ref=dbs_a_def_rwt_hsch_vapi_taft_p1_i4) - Çevrimiçi olarak da bulunabilir (yukarıya bakın)
* [Lua programlamaya başlangıç](https://www.amazon.com/Beginning-Lua-Programming-Kurt-Jung/dp/0470069171)

### Videolar
* [Tek videoda Lua öğrenin](https://www.youtube.com/watch?v=iMacxZQMPXs)

## Sözdizimi

Programların basit, okunması kolay bir sözdizimi vardır. Her deyim ayrı bir satıra yazılır ve deyimin sonunu işaretlemek gerekmez. İsterseniz deyimleri ayırmak için noktalı virgül `;` kullanabilirsiniz. Kod bloklarının sınırları anahtar sözcüklerle belirlenir ve bloklar `end` anahtar sözcüğüyle biter. Yorumlar bir blok halinde veya satır sonuna kadar yazılabilir:

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

## Değişkenler ve veri türleri

Lua dinamik türlendirmelidir; yani değişkenlerin türü yoktur, ancak değerlerin vardır. 
Statik türlendirmeli dillerden farklı olarak, istediğiniz herhangi bir değeri herhangi bir değişkene atayabilirsiniz. 

Lua'da sekiz temel tür vardır:

`nil`
: Bu türün yalnızca `nil` değeri vardır. Genellikle yararlı bir değerin bulunmadığını ifade eder; örneğin değer atanmamış değişkenlerde kullanılır.

  ```lua
  print(my_var) -- will print 'nil' since 'my_var' is not yet assigned a value
  ```

boolean
: `true` veya `false` değerini alır. `false` veya `nil` olan koşullar yanlış olarak değerlendirilir. Diğer tüm değerler doğru olarak değerlendirilir.

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
: Sayılar dahili olarak 64 bit _tam sayılar_ veya 64 bit _kayan noktalı_ sayılar biçiminde temsil edilir. Lua gerektiğinde bu gösterimler arasında otomatik dönüşüm yapar, dolayısıyla genellikle bununla ilgilenmeniz gerekmez.

  ```lua
  print(10) --> prints '10'
  print(10.0) --> '10'
  print(10.000000000001) --> '10.000000000001'

  a = 5 -- integer
  b = 7/3 -- float
  print(a - b) --> '2.6666666666667'
  ```

string
: Dizeler, gömülü sıfırlar (`\0`) dahil herhangi bir 8 bitlik değeri içerebilen, değişmez bayt dizileridir. Lua bir dizenin içeriği hakkında varsayımda bulunmaz; bu nedenle dizelerde istediğiniz veriyi saklayabilirsiniz. Dize sabitleri tek veya çift tırnak içinde yazılır. Lua, çalışma sırasında sayılarla dizeler arasında dönüşüm yapar. Dizeler `..` işleciyle birleştirilebilir.

  Dizeler, aşağıdaki C tarzı kaçış dizilerini içerebilir:

  | Dizi | Karakter |
  | -------- | --------- |
  | `\a`     | zil       |
  | `\b`     | geri silme |
  | `\f`     | sayfa ilerletme  |
  | `\n`     | yeni satır    |
  | `\r`     | satır başı |
  | `\t`     | yatay sekme |
  | `\v`     | dikey sekme   |
  | `\\`     | ters eğik çizgi      |
  | `\"`     | çift tırnak   |
  | `\'`     | tek tırnak   |
  | `\[`     | sol köşeli ayraç    |
  | `\]`     | sağ köşeli ayraç   |
  | `\ddd`   | sayısal değeriyle belirtilen karakter; burada `ddd`, en fazla üç _ondalık_ rakamdan oluşan bir dizidir |

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
: Lua'da işlevler birinci sınıf değerlerdir (first-class values); yani onları işlevlere parametre olarak aktarabilir ve değer olarak döndürebilirsiniz. Bir işlevin atandığı değişkenler, o işleve bir başvuru içerir. Değişkenlere anonim işlevler atayabilirsiniz, ancak Lua kolaylık sağlamak için bir sözdizimi kısayolu (`function name(param1, param2) ... end`) sunar.

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
: Tablolar, Lua'daki tek veri yapılandırma türüdür. Listeleri, dizileri, sıralı dizileri (sequence), simge tablolarını, kümeleri, kayıtları, grafları, ağaçları vb. temsil etmek için kullanılan ilişkisel dizi _nesneleridir_. Tablolar her zaman anonimdir ve bir tabloyu atadığınız değişkenler tablonun kendisini değil, ona bir başvuruyu içerir. Bir tabloyu sıralı dizi olarak başlatırken ilk indeks `0` değil, `1` olur.

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
: `userdata`, herhangi bir C verisinin Lua değişkenlerinde saklanabilmesini sağlar. Defold, karma değerlerini (hash), URL nesnelerini (url), matematik nesnelerini (vector3, vector4, matrix4, quaternion), oyun nesnelerini (game object), GUI düğümlerini (node), işleme yüklemlerini (predicate), işleme hedeflerini (render_target) ve işleme sabiti arabelleklerini (constant_buffer) saklamak için Lua `userdata` nesnelerini kullanır

thread
: İş parçacıkları (thread), birbirinden bağımsız yürütme akışlarını temsil eder ve eş yordamları (coroutine) uygulamak için kullanılır. Ayrıntılar için aşağıya bakın.

## İşleçler

Aritmetik işleçler
: Matematiksel işleçler `+`, `-`, `*`, `/`, tekli `-` (işaret değiştirme) ve üs alma işleci `^`.

  ```lua
  a = -1
  print(a * 2 + 3 / 4^5) --> -1.9970703125
  ```

  Lua, çalışma sırasında sayılarla dizeler arasında otomatik dönüşüm sağlar. Bir dizeye uygulanan her sayısal işlem, dizeyi sayıya dönüştürmeyi dener:

  ```lua
  print("10" + 1) --> 11
  ```

İlişkisel/karşılaştırma işleçleri
: `<` (küçüktür), `>` (büyüktür), `<=` (küçüktür veya eşittir), `>=` (büyüktür veya eşittir), `==` (eşittir), `~=` (eşit değildir). Bu işleçler her zaman `true` veya `false` döndürür. Farklı türlerdeki değerler farklı kabul edilir. Türler aynıysa değerlerine göre karşılaştırılırlar. Lua; tabloları, `userdata` değerlerini ve işlevleri başvurularına göre karşılaştırır. Bu türden iki değer, yalnızca aynı nesneye başvuruyorlarsa eşit kabul edilir.

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

Mantıksal işleçler
: `and`, `or` ve `not`. `and`, ilk bağımsız değişkeni `false` ise onu, aksi halde ikinci bağımsız değişkeni döndürür. `or`, ilk bağımsız değişkeni `false` değilse onu, aksi halde ikinci bağımsız değişkeni döndürür.

  ```lua
  print(true or false) --> true
  print(true and false) --> false
  print(not false) --> true

  if a == 5 and b == 6 then
      print("a is 5 and b is 6")
  end
  ```

Birleştirme
: Dizeler `..` işleciyle birleştirilebilir. Sayılar birleştirme sırasında dizeye dönüştürülür.

  ```lua
  print("donkey" .. "kong") --> "donkeykong"
  print(1 .. 2) --> "12"
  ```

Uzunluk
: Tekli uzunluk işleci `#`. Bir dizenin uzunluğu, içerdiği bayt sayısıdır. Bir tablonun uzunluğu, sıralı dizisinin uzunluğudur; yani `1`'den başlayarak yukarı doğru numaralandırılmış ve değeri `nil` olmayan indekslerin sayısıdır. Not: Sıralı dizide `nil` değerli "boşluklar" varsa uzunluk, bir `nil` değerinden önce gelen herhangi bir indeks olabilir.

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

## Akış denetimi

Lua, yaygın akış denetimi yapılarını sunar.

if---then---else
: Bir koşulu sınar; koşul doğruysa `then` bölümünü, aksi halde isteğe bağlı `else` bölümünü yürütür. `if` deyimlerini iç içe yazmak yerine `elseif` kullanabilirsiniz. Bu, Lua'da bulunmayan switch deyiminin yerini alır.

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
: Bir koşulu sınar ve koşul doğru olduğu sürece bloğu yürütür.

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
: Bir koşul doğru olana kadar bloğu tekrarlar. Koşul gövdeden sonra sınandığı için blok en az bir kez yürütülür.

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
: Lua'da iki tür `for` döngüsü vardır: sayısal ve genel. Sayısal `for`, 2 veya 3 sayısal değer alırken genel `for`, bir _yineleyici_ (iterator) işlevinin döndürdüğü tüm değerleri dolaşır.

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

break ve return
: Bir `for`, `while` veya `repeat` döngüsünün iç bloğundan çıkmak için `break` deyimini kullanın. Bir işlevden değer döndürmek ya da işlevin yürütülmesini bitirip çağırana dönmek için `return` kullanın. `break` veya `return`, yalnızca bir bloğun son deyimi olarak yer alabilir.

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

## Yerel değişkenler, genel değişkenler ve sözcüksel kapsam

Bildirdiğiniz tüm değişkenler varsayılan olarak geneldir (global); yani Lua çalışma zamanı bağlamının her yerinden kullanılabilirler. Değişkenleri açıkça `local` olarak bildirebilirsiniz; bu durumda değişken yalnızca geçerli kapsam içinde var olur.

Her Lua kaynak dosyası ayrı bir kapsam tanımlar. Bir dosyanın en üst düzeyindeki `local` bildirimleri, değişkenin o Lua betik dosyasına yerel olduğu anlamına gelir. Her işlev yeni bir iç kapsam oluşturur ve her denetim yapısı bloğu ek kapsamlar oluşturur. `do` ve `end` anahtar sözcükleriyle açıkça bir kapsam oluşturabilirsiniz. Lua sözcüksel kapsam (lexical scoping) kullanır; yani bir kapsam, kendisini çevreleyen kapsamdaki _yerel_ değişkenlere tam erişim sağlar. Yerel değişkenlerin kullanılmadan önce bildirilmesi gerektiğine dikkat edin.

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

Bir betik dosyasında işlevleri `local` olarak bildirirseniz (ki bu genellikle iyi bir fikirdir) kodun sıralamasına dikkat etmeniz gerekir. Birbirini çağıran işlevleriniz varsa ileri bildirimler kullanabilirsiniz.

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

Başka bir işlevin içinde bir işlev yazarsanız bu işlev de kendisini çevreleyen işlevin yerel değişkenlerine tam erişim sağlar. Bu çok güçlü bir yapıdır.

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

## Değişken gölgeleme

Bir blokta bildirilen yerel değişkenler, çevreleyen bloktaki aynı adlı değişkenleri gölgeler.

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

## Eş yordamlar

İşlevler baştan sona yürütülür ve onları yarıda durdurmanın bir yolu yoktur. Eş yordamlar bunu yapmanıza olanak tanır ve bu bazı durumlarda çok kullanışlı olabilir. Bir oyun nesnesini 1. kareden 5. kareye kadar, y konumu `0`'dan belirli y konumlarına taşıdığımız, kare kare ilerleyen çok özel bir animasyon oluşturmak istediğimizi varsayalım. Bunu `update()` işlevinde (aşağıya bakın) bir sayaç ve konum listesiyle çözebiliriz. Ancak eş yordam kullanarak genişletmesi ve üzerinde çalışması kolay, çok temiz bir uygulama elde ederiz. Durumun tamamı eş yordamın kendi içinde tutulur.

Bir eş yordam yürütmeye ara verdiğinde denetimi çağırana geri verir, ancak yürütmenin hangi noktasında olduğunu hatırlar; böylece daha sonra o noktadan devam edebilir.

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


## Defold'da Lua bağlamları

Bildirdiğiniz tüm değişkenler varsayılan olarak geneldir; yani Lua çalışma zamanı bağlamının her yerinden kullanılabilirler. Defold'un *game.project* dosyasında bu bağlamı denetleyen bir *shared_state* ayarı vardır. Seçenek etkinse tüm betikler, GUI betikleri ve işleme betiği (render script) aynı Lua bağlamında değerlendirilir ve genel değişkenler her yerden görünür. Seçenek etkin değilse motor; betikleri, GUI betiklerini ve işleme betiğini ayrı bağlamlarda yürütür.

![Bağlamlar](images/lua/lua_contexts.png)

Defold, aynı betik dosyasını birkaç ayrı oyun nesnesi bileşeninde (component) kullanmanıza izin verir. Yerel olarak bildirilen tüm değişkenler, aynı betik dosyasını çalıştıran bileşenler arasında paylaşılır.

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

## Performansla ilgili dikkat edilecek noktalar

Akıcı bir şekilde 60 FPS hızında çalışması hedeflenen yüksek performanslı bir oyunda, küçük performans hataları deneyimi büyük ölçüde etkileyebilir. Dikkat edilmesi gereken bazı basit genel noktalar ve ilk bakışta sorunlu görünmeyebilecek bazı durumlar vardır.

Basit noktalardan başlayalım. Gereksiz döngüler içermeyen, doğrudan anlaşılır kod yazmak genellikle iyi bir fikirdir. Bazen öğe listelerini dolaşmanız gerekir, ancak liste yeterince büyükse dikkatli olun. Bu örnek, oldukça iyi bir dizüstü bilgisayarda 1 milisaniyeden biraz daha uzun sürede çalışır. Her karenin yalnızca 16 milisaniye sürdüğü (60 FPS hızında) ve motorun, işleme betiğinin, fizik benzetiminin vb. bu sürenin bir kısmını kullandığı düşünüldüğünde, bu süre belirleyici olabilir.

```lua
local t = socket.gettime()
local table = {}
for i=1,2000 do
    table[i] = vmath.vector3(i, i, i)
end
print((socket.gettime() - t) * 1000)

-- DEBUG:SCRIPT: 0.40388
```

Şüphelendiğiniz kodun performansını ölçmek için `socket.gettime()` işlevinin döndürdüğü değeri (sistemin zaman başlangıcından beri geçen saniye sayısı) kullanın.

## Bellek ve çöp toplama

Lua'nın çöp toplama işlemi varsayılan olarak arka planda otomatik çalışır ve Lua çalışma zamanı ortamının ayırdığı belleği geri kazanır. Çok miktarda çöp toplamak zaman alabileceğinden, çöp toplama gerektiren nesnelerin sayısını düşük tutmak yararlıdır:

* Yerel değişkenler kendi başlarına maliyetsizdir ve çöp oluşturmaz. (ör. `local v = 42`)
* Her _yeni ve benzersiz_ dize yeni bir nesne oluşturur. `local s = "some_string"` yazmak yeni bir nesne oluşturur ve bu nesneyi `s` değişkenine atar. Yerel `s` değişkeninin kendisi çöp oluşturmaz, ancak dize nesnesi çöp oluşturur. Aynı dizeyi birden fazla kez kullanmanın ek bellek maliyeti yoktur.
* Bir tablo oluşturucusu her yürütüldüğünde (`{ ... }`) yeni bir tablo oluşturulur.
* Bir _işlev deyiminin_ yürütülmesi bir kapanış (closure) nesnesi oluşturur. (yani tanımlı bir işlevi çağırmak değil, `function () ... end` deyimini yürütmek)
* Değişken sayıda bağımsız değişken alan işlevler (vararg) (`function(v, ...) end`), işlev her _çağrıldığında_ üç nokta için bir tablo oluşturur (Lua'nın 5.2 öncesi sürümlerinde veya LuaJIT kullanılmıyorsa).
* `dofile()` ve `dostring()`
* Userdata nesneleri

Yeni nesneler oluşturmak yerine elinizdekileri yeniden kullanabileceğiniz pek çok durum vardır. Örneğin, her `update()` işlevinin sonunda aşağıdaki kullanım yaygındır:

```lua
-- Reset velocity
self.velocity = vmath.vector3()
```

Her `vmath.vector3()` çağrısının yeni bir nesne oluşturduğunu unutmak kolaydır. Bir `vector3` nesnesinin ne kadar bellek kullandığını bulalım:

```lua
print(collectgarbage("count") * 1024)       -- 88634
local v = vmath.vector3()
print(collectgarbage("count") * 1024)       -- 88704. 70 bytes in total has been allocated
```

`collectgarbage()` çağrıları arasında 70 bayt eklenmiştir, ancak buna `vector3` nesnesi dışındaki bellek ayırmaları da dahildir. `collectgarbage()` sonucunun her yazdırılışında, kendi başına 22 bayt çöp ekleyen bir dize oluşturulur:

```lua
print(collectgarbage("count") * 1024)       -- 88611
print(collectgarbage("count") * 1024)       -- 88633. 22 bytes allocated
```

Yani bir `vector3` nesnesi 70-22=48 bayt yer kaplar. Bu fazla değildir, ancak 60 FPS hızındaki bir oyunda her karede _bir tane_ oluşturursanız bir anda saniyede 2,8 kB çöp ortaya çıkar. Her biri her karede bir `vector3` oluşturan 360 betik bileşeniyle, saniyede 1 MB çöp üretilir. Miktarlar çok hızlı birikebilir. Lua çalışma zamanı ortamı çöp toplarken, özellikle mobil platformlarda, değerli milisaniyelerinizin çoğunu tüketebilir.

Bellek ayırmalarından kaçınmanın bir yolu, bir `vector3` oluşturup aynı nesneyle çalışmaya devam etmektir. Örneğin, bir `vector3` nesnesini sıfırlamak için aşağıdaki yapıyı kullanabiliriz:

```lua
-- Instead of doing self.velocity = vmath.vector3() which creates a new object
-- we zero an existing velocity vector object's components
self.velocity.x = 0
self.velocity.y = 0
self.velocity.z = 0
```

Varsayılan çöp toplama düzeni, zamanlamanın kritik olduğu bazı uygulamalar için en uygun seçenek olmayabilir. Oyununuzda veya uygulamanızda takılmalar görüyorsanız [`collectgarbage()`](/ref/base/#collectgarbage) Lua işleviyle Lua'nın çöp toplama biçimini ayarlamak isteyebilirsiniz. Örneğin, düşük bir `step` değeriyle toplayıcıyı her karede kısa bir süre çalıştırabilirsiniz. Oyununuzun veya uygulamanızın ne kadar bellek tükettiği hakkında fikir edinmek için geçerli çöp miktarını bayt cinsinden şöyle yazdırabilirsiniz:

```lua
print(collectgarbage("count") * 1024)
```

## İyi uygulamalar

Yaygın bir uygulama tasarımı konusu, ortak davranışlar için kodun nasıl yapılandırılacağıdır. Birkaç yaklaşım mümkündür.

Modül içindeki davranışlar
: Bir davranışı bir modül içinde kapsüllemek, farklı oyun nesnelerinin betik bileşenleri (ve GUI betikleri) arasında kodu kolayca paylaşmanızı sağlar. Modül işlevleri yazarken genellikle tamamen işlevsel programlamaya dayalı kod yazmak en iyisidir. Durum saklamanın veya yan etkilerin gerekli olduğu (ya da daha temiz bir tasarım sağladığı) durumlar vardır. Dahili durumu modülde saklamanız gerekiyorsa bileşenlerin Lua bağlamlarını paylaştığını unutmayın. Ayrıntılar için [Modüller belgelerine](/manuals/modules) bakın.

  ![Modül](images/lua/lua_module.png)

  Ayrıca modül kodunun bir oyun nesnesinin iç yapısını doğrudan değiştirmesi mümkün olsa da (bir modül işlevine `self` aktararak), çok sıkı bir bağımlılık oluşturacağınız için bunu yapmaktan kesinlikle kaçınmanızı öneririz.

Davranışı kapsülleyen yardımcı bir oyun nesnesi
: Betik kodunu bir Lua modülünde barındırabildiğiniz gibi, betik bileşeni olan bir oyun nesnesinde de barındırabilirsiniz. Aradaki fark, kodu bir oyun nesnesinde barındırdığınızda onunla yalnızca ileti aktarımı (message passing) yoluyla iletişim kurabilmenizdir.

  ![Yardımcı](images/lua/lua_helper.png)

Oyun nesnesini yardımcı davranış nesnesiyle bir koleksiyon içinde gruplama
: Bu tasarımda, başka bir hedef oyun nesnesi üzerinde otomatik olarak işlem yapan bir davranış oyun nesnesi oluşturabilirsiniz. Bunun için önceden tanımlanmış bir ad (kullanıcının hedef oyun nesnesinin adını buna uyacak şekilde değiştirmesi gerekir) veya hedef oyun nesnesini gösteren bir `go.property()` URL değeri kullanılabilir.

  ![Koleksiyon](images/lua/lua_collection.png)

  Bu düzenin yararı, hedef nesneyi içeren bir koleksiyona (collection) bir davranış oyun nesnesi bırakabilmenizdir. Hiçbir ek kod gerekmez.

  Çok sayıda oyun nesnesini yönetmeniz gereken durumlarda bu tasarım tercih edilmez; çünkü davranış nesnesi her örnek (instance) için çoğaltılır ve her nesnenin bellek maliyeti vardır.
