---
title: Programación Lua en Defold
brief: Este manual ofrece una introducción rápida a los fundamentos de la programación Lua en general y a lo que debes considerar al trabajar con Lua en Defold.
---

# Lua en Defold

El motor Defold lleva integrado el lenguaje Lua para scripting. Lua es un lenguaje dinámico ligero que es potente, rápido y fácil de integrar. Se usa ampliamente como lenguaje de scripting para videojuegos. Los programas Lua se escriben con una sintaxis procedimental simple. El lenguaje tiene tipado dinámico y se ejecuta mediante un intérprete de bytecode. Incluye gestión automática de memoria con recolección de basura incremental.

Este manual ofrece una introducción rápida a los fundamentos de la programación Lua en general y a lo que debes considerar al trabajar con Lua en Defold. Si tienes algo de experiencia con Python, Perl, Ruby, JavaScript o un lenguaje dinámico similar, podrás avanzar bastante rápido. Si eres nuevo en la programación, tal vez quieras empezar con un libro de Lua orientado a principiantes. Hay muchos para elegir.

## Versiones de Lua

Defold usa [LuaJIT](https://luajit.org/), una versión altamente optimizada de Lua adecuada para juegos y otro software donde el rendimiento es crítico. Es totalmente compatible hacia arriba con Lua 5.1 y soporta todas las funciones de la biblioteca estándar de Lua y el conjunto completo de funciones de la API Lua/C.

LuaJIT también agrega varias [extensiones del lenguaje](https://luajit.org/extensions.html) y algunas funcionalidades de Lua 5.2 y 5.3.

Nuestro objetivo es mantener Defold igual en todas las plataformas, pero actualmente tenemos algunas discrepancias menores en la versión del lenguaje Lua entre plataformas:
* iOS no permite compilación JIT.
* Nintendo Switch no permite compilación JIT.
* HTML5 usa Lua 5.1.4 en lugar de LuaJIT.

::: important
Para garantizar que tu juego funcione en todas las plataformas compatibles, recomendamos firmemente que uses SOLO funcionalidades del lenguaje de Lua 5.1.
:::

### Bibliotecas estándar y extensiones
Defold incluye todas las [bibliotecas estándar de Lua 5.1](http://www.lua.org/manual/5.1/manual.html#5), así como una biblioteca de socket y una de operaciones de bits:

  - base (`assert()`, `error()`, `print()`, `ipairs()`, `require()`, etc.)
  - coroutine
  - package
  - string
  - table
  - math
  - io
  - os
  - debug
  - socket (de [LuaSocket](https://github.com/diegonehab/luasocket))
  - bitop (de [BitOp](http://bitop.luajit.org/api.html))

Todas las bibliotecas están documentadas en la [documentación de referencia de la API](/ref/go).

## Libros y recursos de Lua

### Recursos en línea
* [Programming in Lua (first edition)](http://www.lua.org/pil/contents.html) Las ediciones posteriores están disponibles en formato impreso.
* [Lua 5.1 reference manual](http://www.lua.org/manual/5.1/)
* [Learn Lua in 15 Minutes](http://tylerneylon.com/a/learn-lua/)
* [Awesome Lua - tutorial section](https://github.com/LewisJEllis/awesome-lua#tutorials)

### Libros
* [Programming in Lua](https://www.amazon.com/gp/product/8590379868/ref=dbs_a_def_rwt_hsch_vapi_taft_p1_i0) - Programming in Lua es el libro oficial sobre el lenguaje, y proporciona una base sólida a cualquier programador que quiera usar Lua. Escrito por Roberto Ierusalimschy, el arquitecto principal del lenguaje.
* [Lua programming gems](https://www.amazon.com/Programming-Gems-Luiz-Henrique-Figueiredo/dp/8590379841) - Esta colección de artículos recoge parte del conocimiento y la práctica existentes sobre cómo programar bien en Lua.
* [Lua 5.1 reference manual](https://www.amazon.com/gp/product/8590379833/ref=dbs_a_def_rwt_hsch_vapi_taft_p1_i4) - También disponible en línea (ver arriba).
* [Beginning Lua Programming](https://www.amazon.com/Beginning-Lua-Programming-Kurt-Jung/dp/0470069171)

### Videos
* [Learn Lua in one video](https://www.youtube.com/watch?v=iMacxZQMPXs)

## Sintaxis

Los programas tienen una sintaxis simple y fácil de leer. Las sentencias se escriben una por línea y no es necesario marcar el final de una sentencia. Opcionalmente puedes usar punto y coma `;` para separar sentencias. Los bloques de código están delimitados por palabras clave y terminan con la palabra clave `end`. Los comentarios pueden escribirse como bloque o hasta el final de la línea:

```lua
--[[
Aquí hay un bloque de comentarios que puede ocupar
varias líneas en el archivo fuente.
--]]

a = 10
b = 20 ; c = 30 -- dos sentencias en una línea

if my_variable == 3 then
    call_some_function(true) -- Este es un comentario de línea
else
    call_another_function(false)
end
```

## Variables y tipos de datos

Lua tiene tipado dinámico, lo que significa que las variables no tienen tipos, pero los valores sí.
A diferencia de los lenguajes con tipado estático, puedes asignar cualquier valor a cualquier variable como quieras.

Hay ocho tipos básicos en Lua:

`nil`
: Este tipo solo tiene el valor `nil`. Normalmente representa la ausencia de un valor útil, por ejemplo variables sin asignar.

  ```lua
  print(my_var) -- imprimirá 'nil' porque 'my_var' todavía no tiene un valor asignado
  ```

boolean
: Tiene el valor `true` o `false`. Las condiciones que son `false` o `nil` se consideran falsas. Cualquier otro valor se considera verdadero.

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
: Los números se representan internamente como _enteros_ de 64 bits o números de _punto flotante_ de 64 bits. Lua convierte automáticamente entre estas representaciones según sea necesario, así que por lo general no tienes que preocuparte por ello.

  ```lua
  print(10) --> imprime '10'
  print(10.0) --> '10'
  print(10.000000000001) --> '10.000000000001'

  a = 5 -- entero
  b = 7/3 -- float
  print(a - b) --> '2.6666666666667'
  ```

string
: Los strings son secuencias inmutables de bytes que pueden contener cualquier valor de 8 bits, incluidos ceros incrustados (`\0`). Lua no asume nada sobre el contenido de un string, así que puedes guardar en ellos cualquier dato que quieras. Los literales de string se escriben con comillas simples o dobles. Lua convierte entre números y strings en tiempo de ejecución. Los strings se pueden concatenar con el operador `..`.

  Los strings pueden contener las siguientes secuencias de escape de estilo C:

  | Secuencia | Carácter |
  | --------- | -------- |
  | `\a`     | campana  |
  | `\b`     | retroceso |
  | `\f`     | avance de página |
  | `\n`     | nueva línea |
  | `\r`     | retorno de carro |
  | `\t`     | tabulación horizontal |
  | `\v`     | tabulación vertical |
  | `\\`     | barra invertida |
  | `\"`     | comilla doble |
  | `\'`     | comilla simple |
  | `\[`     | corchete izquierdo |
  | `\]`     | corchete derecho |
  | `\ddd`   | carácter indicado por su valor numérico, donde `ddd` es una secuencia de hasta tres dígitos _decimales_ |

  ```lua
  my_string = "hello"
  another_string = 'world'
  print(my_string .. another_string) --> "helloworld"

  print("10.2" + 1) --> 11.2
  print(my_string + 1) -- error, no puede convertir "hello"
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
: Las funciones son valores de primera clase en Lua, lo que significa que puedes pasarlas como parámetros a funciones y devolverlas como valores. Las variables asignadas a una función contienen una referencia a la función. Puedes asignar variables a funciones anónimas, pero Lua proporciona azúcar sintáctico (`function name(param1, param2) ... end`) por comodidad.

  ```lua
  -- Asigna 'my_plus' a una función
  my_plus = function(p, q)
      return p + q
  end

  print(my_plus(4, 5)) --> 9

  -- Sintaxis conveniente para asignar una función a la variable 'my_mult'
  function my_mult(p, q)
      return p * q
  end

  print(my_mult(4, 5)) --> 20

  -- Toma una función como parámetro 'func'
  function operate(func, p, q)
      return func(p, q) -- Llama a la función proporcionada con los parámetros 'p' y 'q'
  end

  print(operate(my_plus, 4, 5)) --> 9
  print(operate(my_mult, 4, 5)) --> 20

  -- Crea una función sumadora y la devuelve
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
: Las tablas son el único tipo para estructurar datos en Lua. Son _objetos_ de array asociativo que se usan para representar listas, arrays, secuencias, tablas de símbolos, conjuntos, registros, grafos, árboles, etc. Las tablas siempre son anónimas y las variables a las que asignas una tabla no contienen la tabla en sí, sino una referencia a ella. Al inicializar una tabla como secuencia, el primer índice es `1`, no `0`.

  ```lua
  -- Inicializa una tabla como secuencia
  weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday"}
  print(weekdays[1]) --> "Sunday"
  print(weekdays[5]) --> "Thursday"

  -- Inicializa una tabla como registro con valores de secuencia
  moons = { Earth = { "Moon" },
            Uranus = { "Puck", "Miranda", "Ariel", "Umbriel", "Titania", "Oberon" } }
  print(moons.Uranus[3]) --> "Ariel"

  -- Construye una tabla desde un constructor vacío {}
  a = 1
  t = {}
  t[1] = "first"
  t[a + 1] = "second"
  t.x = 1 -- igual que t["x"] = 1

  -- Itera sobre los pares clave-valor de la tabla
  for key, value in pairs(t) do
      print(key, value)
  end
  --> 1   first
  --> 2   second
  --> x   1

  u = t -- ahora u se refiere a la misma tabla que t
  u[1] = "changed"

  for key, value in pairs(t) do -- sigue iterando sobre t
      print(key, value)
  end
  --> 1   changed
  --> 2   second
  --> x   1
  ```

`userdata`
: Userdata se proporciona para permitir almacenar datos arbitrarios de C en variables Lua. Defold usa objetos `userdata` de Lua para almacenar valores Hash (hash), objetos URL (url), objetos Math (vector3, vector4, matrix4, quaternion), objetos de juego, nodos GUI (node), predicados de Render (predicate), targets de Render (render_target) y buffers de constantes de Render (constant_buffer).

thread
: Los threads representan hilos de ejecución independientes y se usan para implementar corrutinas. Consulta los detalles más abajo.

## Operadores

Operadores aritméticos
: Operadores matemáticos `+`, `-`, `*`, `/`, el `-` unario (negación) y el exponencial `^`.

  ```lua
  a = -1
  print(a * 2 + 3 / 4^5) --> -1.9970703125
  ```

  Lua proporciona conversiones automáticas entre números y strings en tiempo de ejecución. Cualquier operación numérica aplicada a un string intenta convertir el string en un número:

  ```lua
  print("10" + 1) --> 11
  ```

Operadores relacionales/de comparación
: `<` (menor que), `>` (mayor que), `<=` (menor o igual), `>=` (mayor o igual), `==` (igual), `~=` (distinto). Estos operadores siempre devuelven `true` o `false`. Los valores de tipos distintos se consideran distintos. Si los tipos son iguales, se comparan según su valor. Lua compara tablas, `userdata` y funciones por referencia. Dos valores de ese tipo solo se consideran iguales si se refieren al mismo objeto.

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

Operadores lógicos
: `and`, `or` y `not`. `and` devuelve su primer argumento si es `false`; de lo contrario devuelve su segundo argumento. `or` devuelve su primer argumento si no es `false`; de lo contrario devuelve su segundo argumento.

  ```lua
  print(true or false) --> true
  print(true and false) --> false
  print(not false) --> true

  if a == 5 and b == 6 then
      print("a is 5 and b is 6")
  end
  ```

Concatenación
: Los strings se pueden concatenar con el operador `..`. Los números se convierten en strings al concatenarlos.

  ```lua
  print("donkey" .. "kong") --> "donkeykong"
  print(1 .. 2) --> "12"
  ```

Longitud
: El operador unario de longitud `#`. La longitud de un string es su número de bytes. La longitud de una tabla es la longitud de su secuencia: el número de índices numerados desde `1` en adelante cuyo valor no es `nil`. Nota: Si la secuencia tiene "huecos" con valores `nil`, la longitud puede ser cualquier índice anterior a un valor `nil`.

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

## Control de flujo

Lua proporciona el conjunto habitual de construcciones de control de flujo.

if---then---else
: Prueba una condición; ejecuta la parte `then` si la condición es verdadera; de lo contrario ejecuta la parte `else` (opcional). En lugar de anidar sentencias `if`, puedes usar `elseif`. Esto reemplaza a una sentencia switch, que Lua no tiene.

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
: Prueba una condición y ejecuta el bloque mientras sea verdadera.

  ```lua
  weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday"}

  -- Imprime cada día de la semana
  i = 1
  while weekdays[i] do
      print(weekdays[i])
      i = i + 1
  end
  ```

repeat---until
: Repite el bloque hasta que una condición sea verdadera. La condición se prueba después del cuerpo, así que se ejecutará al menos una vez.

  ```lua
  weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday"}

  -- Imprime cada día de la semana
  i = 0
  repeat
      i = i + 1
      print(weekdays[i])
  until weekdays[i] == "Saturday"
  ```

for
: Lua tiene dos tipos de bucle `for`: numérico y genérico. El `for` numérico toma 2 o 3 valores numéricos, mientras que el `for` genérico itera sobre todos los valores devueltos por una función _iteradora_.

  ```lua
  -- Imprime los números del 1 al 10
  for i = 1, 10 do
      print(i)
  end

  -- Imprime los números del 1 al 10 e incrementa en 2 cada vez
  for i = 1, 10, 2 do
      print(i)
  end

  -- Imprime los números del 10 al 1
  for i=10, 1, -1 do
      print(i)
  end

  t = { "a", "b", "c", "d" }
  -- Itera sobre la secuencia e imprime los valores
  for i, v in ipairs(t) do
      print(v)
  end
  ```

break y return
: Usa la sentencia `break` para salir de un bloque interno de un bucle `for`, `while` o `repeat`. Usa `return` para devolver un valor desde una función o para finalizar la ejecución de una función y volver al llamador. `break` o `return` solo pueden aparecer como la última sentencia de un bloque.

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

## Locales, globales y ámbito léxico

Todas las variables que declaras son globales por defecto, lo que significa que están disponibles en todas las partes del contexto de runtime de Lua. Puedes declarar variables explícitamente como `local`, lo que significa que la variable solo existirá dentro del ámbito actual.

Cada archivo fuente Lua define un ámbito separado. Las declaraciones locales en el nivel superior de un archivo hacen que la variable sea `local` al archivo script Lua. Cada función crea otro ámbito anidado y cada bloque de estructura de control crea ámbitos adicionales. Puedes crear un ámbito explícitamente con las palabras clave `do` y `end`. Lua tiene ámbito léxico, lo que significa que un ámbito tiene acceso completo a variables _locales_ del ámbito que lo contiene. Ten en cuenta que las variables locales deben declararse antes de usarlas.

```lua
function my_func(a, b)
    -- 'a' y 'b' son locales a esta función y están disponibles en su ámbito

    do
        local x = 1
    end

    print(x) --> nil. 'x' no está disponible fuera del ámbito do-end
    print(foo) --> nil. 'foo' se declara después de 'my_func'
    print(foo_global) --> "value 2"
end

local foo = "value 1"
foo_global = "value 2"

print(foo) --> "value 1". 'foo' está disponible en el ámbito superior después de la declaración.
```

Ten en cuenta que si declaras funciones `local` en un archivo script (lo que generalmente es una buena idea), debes prestar atención al orden del código. Puedes usar declaraciones adelantadas si tienes funciones que se llaman mutuamente.

```lua
local func2 -- Declaración adelantada de 'func2'

local function func1(a)
    print("func1")
    func2(a)
end

function func2(a) -- o func2 = function(a)
    print("func2")
    if a < 10 then
        func1(a + 1)
    end
end

function init(self)
    func1(1)
end
```

Si escribes una función dentro de otra función, también tiene acceso completo a las variables locales de la función que la contiene. Esta es una construcción muy potente.

```lua
function create_counter(x)
    -- 'x' es una variable local en 'create_counter'
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

## Ocultamiento de variables

Las variables locales declaradas en un bloque ocultarán variables de un bloque envolvente que tengan el mismo nombre.

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

## Corrutinas

Las funciones se ejecutan desde el principio hasta el final y no hay forma de detenerlas a la mitad. Las corrutinas te permiten hacerlo, lo que puede ser muy conveniente en algunos casos. Supongamos que queremos crear una animación muy específica fotograma por fotograma donde movemos un objeto de juego desde la posición y `0` hasta algunas posiciones y muy específicas desde el fotograma 1 hasta el fotograma 5. Podríamos resolverlo con un contador en la función `update()` (ver abajo) y una lista de posiciones. Sin embargo, con una corrutina obtenemos una implementación muy limpia, fácil de extender y de trabajar. Todo el estado queda contenido dentro de la propia corrutina.

Cuando una corrutina hace yield, devuelve el control al llamador pero recuerda su punto de ejecución para poder continuar desde ahí más tarde.

```lua
-- Esta es nuestra corrutina
local function sequence(self)
    coroutine.yield(120)
    coroutine.yield(320)
    coroutine.yield(510)
    coroutine.yield(240)
    return 440 -- devuelve el valor final
end

function init(self)
    self.co = coroutine.create(sequence) -- Crea la corrutina. 'self.co' es un objeto thread
    go.set_position(vmath.vector3(100, 0, 0)) -- Define la posición inicial
end

function update(self, dt)
    local status, y_pos = coroutine.resume(self.co, self) -- Continúa la ejecución de la corrutina.
    if status then
        -- Si la corrutina todavía no está terminada/muerta, usa su valor devuelto por yield como nueva posición
        go.set_position(vmath.vector3(100, y_pos, 0))
    end
end
```


## Contextos de Lua en Defold

Todas las variables que declaras son globales por defecto, lo que significa que están disponibles en todas las partes del contexto de runtime de Lua. Defold tiene una configuración *shared_state* en *game.project* que controla este contexto. Si la opción está activada, todos los scripts, scripts GUI y el render script se evalúan en el mismo contexto Lua y las variables globales son visibles en todas partes. Si la opción no está activada, el motor ejecuta scripts, scripts GUI y el render script en contextos separados.

![Contextos](images/lua/lua_contexts.png)

Defold te permite usar el mismo archivo script en varios componentes de objeto de juego separados. Cualquier variable declarada localmente se comparte entre los componentes que ejecutan el mismo archivo script.

```lua
-- 'my_global_value' estará disponible desde todos los scripts, gui_scripts, render script y módulos (archivos Lua)
my_global_value = "global scope"

-- este valor se compartirá entre todas las instancias de componente que usen este archivo script concreto
local script_value = "script scope"

function init(self, dt)
    -- Este valor estará disponible en esta instancia de componente script
    self.foo = "self scope"

    -- este valor estará disponible dentro de init() y después de su declaración
    local local_foo = "local scope"
    print(local_foo)
end

function update(self, dt)
    print(self.foo)
    print(my_global_value)
    print(script_value)
    print(local_foo) -- imprimirá nil, porque local_foo solo es visible en init()
end
```

## Consideraciones de rendimiento

En un juego de alto rendimiento pensado para ejecutarse a 60 FPS fluidos, los pequeños errores de rendimiento pueden tener un gran impacto en la experiencia. Hay algunas cosas generales simples que considerar, y algunas cosas que pueden no parecer problemáticas.

Empezando por lo simple: generalmente es buena idea escribir código directo que no contenga bucles innecesarios. A veces sí necesitas iterar sobre listas de cosas, pero ten cuidado si la lista es lo suficientemente grande. Este ejemplo se ejecuta en poco más de 1 milisegundo en una laptop bastante decente, lo que puede marcar toda la diferencia si cada fotograma solo dura 16 milisegundos (a 60 FPS) y el motor, el render script, la simulación de física, etc., consumen parte de ese tiempo.

```lua
local t = socket.gettime()
local table = {}
for i=1,2000 do
    table[i] = vmath.vector3(i, i, i)
end
print((socket.gettime() - t) * 1000)

-- DEBUG:SCRIPT: 0.40388
```

Usa el valor devuelto por `socket.gettime()` (segundos desde la época del sistema) para medir código sospechoso.

## Memoria y recolección de basura

La recolección de basura de Lua se ejecuta automáticamente en segundo plano de forma predeterminada y recupera memoria que el runtime de Lua ha asignado. Recolectar mucha basura puede llevar tiempo, así que conviene reducir la cantidad de objetos que necesitan ser recolectados:

* Las variables locales en sí mismas son gratis y no generarán basura. (es decir, `local v = 42`)
* Cada string _nuevo y único_ crea un objeto nuevo. Escribir `local s = "some_string"` creará un objeto nuevo y asignará `s` a él. La variable local `s` en sí no generará basura, pero el objeto string sí. Usar el mismo string varias veces no agrega coste de memoria adicional.
* Cada vez que se ejecuta un constructor de tabla (`{ ... }`), se crea una tabla nueva.
* Ejecutar una _sentencia de función_ crea un objeto closure. (es decir, ejecutar la sentencia `function () ... end`, no llamar a una función definida)
* Las funciones variádicas (`function(v, ...) end`) crean una tabla para los puntos suspensivos cada vez que se _llama_ a la función (en Lua anterior a la versión 5.2, o si no se usa LuaJIT).
* `dofile()` y `dostring()`
* Objetos `userdata`

Hay muchos casos en los que puedes evitar crear objetos nuevos y reutilizar los que ya tienes. Por ejemplo, lo siguiente es común al final de cada `update()`:

```lua
-- Restablecer velocidad
self.velocity = vmath.vector3()
```

Es fácil olvidar que cada llamada a `vmath.vector3()` crea un objeto nuevo. Averigüemos cuánta memoria usa un `vector3`:

```lua
print(collectgarbage("count") * 1024)       -- 88634
local v = vmath.vector3()
print(collectgarbage("count") * 1024)       -- 88704. Se han asignado 70 bytes en total
```

Se han agregado 70 bytes entre las llamadas a `collectgarbage()`, pero esto incluye asignaciones para algo más que el objeto `vector3`. Cada impresión del resultado de `collectgarbage()` construye un string que por sí mismo agrega 22 bytes de basura:

```lua
print(collectgarbage("count") * 1024)       -- 88611
print(collectgarbage("count") * 1024)       -- 88633. 22 bytes asignados
```

Así que un `vector3` ocupa 70-22=48 bytes. No es mucho, pero si creas _uno_ en cada fotograma en un juego a 60 FPS, de pronto son 2.8 kB de basura por segundo. Con 360 componentes script que crean un `vector3` cada uno en cada fotograma, hablamos de 1 MB de basura generada por segundo. Los números pueden crecer muy rápido. Cuando el runtime de Lua recolecta basura, puede consumir muchos milisegundos valiosos---especialmente en plataformas móviles.

Una forma de evitar asignaciones es crear un `vector3` y seguir trabajando con el mismo objeto. Por ejemplo, para restablecer un `vector3` podemos usar la siguiente construcción:

```lua
-- En lugar de hacer self.velocity = vmath.vector3(), lo que crea un objeto nuevo,
-- ponemos a cero los componentes de un objeto vector de velocidad existente
self.velocity.x = 0
self.velocity.y = 0
self.velocity.z = 0
```

El esquema predeterminado de recolección de basura puede no ser óptimo para algunas aplicaciones con restricciones estrictas de tiempo. Si ves tirones en tu juego o app, tal vez quieras ajustar cómo Lua recolecta basura mediante la función Lua [`collectgarbage()`](/ref/base/#collectgarbage). Por ejemplo, puedes ejecutar el recolector durante un tiempo corto en cada fotograma con un valor bajo de `step`. Para hacerte una idea de cuánta memoria consume tu juego o app, puedes imprimir la cantidad actual de bytes de basura con:

```lua
print(collectgarbage("count") * 1024)
```

## Buenas prácticas

Una consideración de diseño de implementación común es cómo estructurar el código para comportamientos compartidos. Son posibles varios enfoques.

Comportamientos en un módulo
: Encapsular un comportamiento en un módulo te permite compartir código fácilmente entre componentes script de distintos objetos de juego (y scripts GUI). Al escribir funciones de módulo, generalmente es mejor escribir código estrictamente funcional. Hay casos en los que el estado almacenado o los efectos secundarios son necesarios (o llevan a un diseño más limpio). Si tienes que almacenar el estado interno en el módulo, ten en cuenta que los componentes comparten contextos Lua. Consulta la [documentación de módulos](/manuals/modules) para más detalles.

  ![Módulo](images/lua/lua_module.png)

  Además, aunque sea posible que el código de un módulo modifique directamente los internos de un objeto de juego (pasando `self` a una función del módulo), lo desaconsejamos firmemente porque crearás un acoplamiento muy fuerte.

Un objeto de juego auxiliar con comportamiento encapsulado
: Igual que puedes contener código script en un módulo Lua, puedes contenerlo en un objeto de juego con un componente script. La diferencia es que si lo contienes en un objeto de juego, puedes comunicarte con él estrictamente mediante paso de mensajes.

  ![Auxiliar](images/lua/lua_helper.png)

Objeto de juego agrupador con objeto de comportamiento auxiliar dentro de una colección
: En este diseño, puedes crear un objeto de juego de comportamiento que actúe automáticamente sobre otro objeto de juego objetivo, ya sea por un nombre predefinido (el usuario debe renombrar el objeto de juego objetivo para que coincida) o mediante una URL `go.property()` que apunte al objeto de juego objetivo.

  ![Colección](images/lua/lua_collection.png)

  El beneficio de esta configuración es que puedes colocar un objeto de juego de comportamiento dentro de una colección que contenga el objeto objetivo. No se necesita código adicional.

  En situaciones donde necesitas gestionar grandes cantidades de objetos de juego, este diseño no es preferible porque el objeto de comportamiento se duplica por cada instancia y cada objeto costará memoria.
