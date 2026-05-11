---
title: Programação Lua no Defold
brief: Este manual dará uma introdução rápida aos conceitos básicos de programação Lua em geral e ao que você precisa considerar ao trabalhar com Lua no Defold.
---

# Lua no Defold

A engine Defold incorpora a linguagem Lua para scripting. Lua é uma linguagem dinâmica leve, poderosa, rápida e fácil de incorporar. Ela é amplamente usada como linguagem de scripting para videogames. Programas Lua são escritos em uma sintaxe procedural simples. A linguagem é tipada dinamicamente e executada por um interpretador de bytecode. Ela conta com gerenciamento automático de memória por coleta de lixo incremental.

Este manual dará uma introdução rápida aos conceitos básicos de programação Lua em geral e ao que você precisa considerar ao trabalhar com Lua no Defold. Se você tem alguma experiência com Python, Perl, Ruby, Javascript ou uma linguagem dinâmica semelhante, começará rapidamente. Se você é iniciante em programação, talvez queira começar com um livro de Lua voltado para iniciantes. Há muitos para escolher.

## Versões de Lua

O Defold usa [LuaJIT](https://luajit.org/), uma versão altamente otimizada de Lua adequada para uso em jogos e outros softwares críticos para desempenho. Ela é totalmente compatível para cima com Lua 5.1 e oferece suporte a todas as funções da biblioteca padrão de Lua e ao conjunto completo de funções da API Lua/C.

LuaJIT também adiciona várias [extensões de linguagem](https://luajit.org/extensions.html) e alguns recursos de Lua 5.2 e 5.3.

Nosso objetivo é manter o Defold igual em todas as plataformas, mas atualmente temos algumas pequenas discrepâncias na versão da linguagem Lua entre plataformas:
* iOS não permite compilação JIT.
* Nintendo Switch não permite compilação JIT.
* HTML5 usa Lua 5.1.4 em vez de LuaJIT.

::: important
Para garantir que seu jogo funcione em todas as plataformas compatíveis, recomendamos fortemente que você use APENAS recursos de linguagem de Lua 5.1.
:::

### Bibliotecas padrão e extensões
O Defold inclui todas as [bibliotecas padrão de Lua 5.1](http://www.lua.org/manual/5.1/manual.html#5), além de uma biblioteca de socket e uma de operações de bit:

  - base (`assert()`, `error()`, `print()`, `ipairs()`, `require()` etc.)
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

Todas as bibliotecas estão documentadas na [documentação de referência da API](/ref/go).

## Livros e recursos de Lua

### Recursos online
* [Programming in Lua (first edition)](http://www.lua.org/pil/contents.html) Edições posteriores estão disponíveis impressas.
* [Manual de referência de Lua 5.1](http://www.lua.org/manual/5.1/)
* [Learn Lua in 15 Minutes](http://tylerneylon.com/a/learn-lua/)
* [Awesome Lua - seção de tutoriais](https://github.com/LewisJEllis/awesome-lua#tutorials)

### Livros
* [Programming in Lua](https://www.amazon.com/gp/product/8590379868/ref=dbs_a_def_rwt_hsch_vapi_taft_p1_i0) - Programming in Lua é o livro oficial sobre a linguagem, fornecendo uma base sólida para qualquer programador que queira usar Lua. Escrito por Roberto Ierusalimschy, o arquiteto-chefe da linguagem.
* [Lua programming gems](https://www.amazon.com/Programming-Gems-Luiz-Henrique-Figueiredo/dp/8590379841) - Esta coleção de artigos registra parte da sabedoria e prática existentes sobre como programar bem em Lua.
* [Lua 5.1 reference manual](https://www.amazon.com/gp/product/8590379833/ref=dbs_a_def_rwt_hsch_vapi_taft_p1_i4) - Também disponível online (veja acima)
* [Beginning Lua Programming](https://www.amazon.com/Beginning-Lua-Programming-Kurt-Jung/dp/0470069171)

### Vídeos
* [Learn Lua in one video](https://www.youtube.com/watch?v=iMacxZQMPXs)

## Sintaxe

Programas têm uma sintaxe simples e fácil de ler. Instruções são escritas uma por linha e não há necessidade de marcar o fim de uma instrução. Você pode opcionalmente usar ponto e vírgula `;` para separar instruções. Blocos de código são delimitados por palavras-chave, terminando com a palavra-chave `end`. Comentários podem ser escritos em bloco ou até o fim da linha:

```lua
--[[
Aqui há um bloco de comentários que pode ocupar
várias linhas no arquivo-fonte.
--]]

a = 10
b = 20 ; c = 30 -- duas instruções em uma linha

if my_variable == 3 then
    call_some_function(true) -- Aqui há um comentário de linha
else
    call_another_function(false)
end
```

## Variáveis e tipos de dados

Lua é tipada dinamicamente, o que significa que variáveis não têm tipos, mas valores têm. 
Ao contrário de linguagens com tipagem estática, você pode atribuir qualquer valor a qualquer variável como quiser. 

Há oito tipos básicos em Lua:

`nil`
: Este tipo tem apenas o valor `nil`. Ele geralmente representa a ausência de um valor útil, por exemplo variáveis não atribuídas.

  ```lua
  print(my_var) -- imprimirá 'nil', já que 'my_var' ainda não recebeu um valor
  ```

boolean
: Tem o valor `true` ou `false`. Condições que são `false` ou `nil` são consideradas falsas. Qualquer outro valor a torna verdadeira.

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
: Números são representados internamente como _inteiros_ de 64 bits ou números de _ponto flutuante_ de 64 bits. Lua converte automaticamente entre essas representações conforme necessário, então em geral você não precisa se preocupar com isso.

  ```lua
  print(10) --> prints '10'
  print(10.0) --> '10'
  print(10.000000000001) --> '10.000000000001'

  a = 5 -- inteiro
  b = 7/3 -- float
  print(a - b) --> '2.6666666666667'
  ```

string
: Strings são sequências imutáveis de bytes que podem conter qualquer valor de 8 bits, incluindo zeros incorporados (`\0`). Lua não faz suposições sobre o conteúdo de uma string, então você pode armazenar nelas qualquer dado que quiser. Literais de string são escritos entre aspas simples ou duplas. Lua converte entre números e strings em tempo de execução. Strings podem ser concatenadas com o operador `..`.

  Strings podem conter as seguintes sequências de escape no estilo C:

  | Sequência | Caractere |
  | -------- | --------- |
  | `\a`     | bell       |
  | `\b`     | back space |
  | `\f`     | form feed  |
  | `\n`     | nova linha |
  | `\r`     | carriage return |
  | `\t`     | tabulação horizontal |
  | `\v`     | tabulação vertical |
  | `\\`     | barra invertida |
  | `\"`     | aspas duplas |
  | `\'`     | aspas simples |
  | `\[`     | colchete esquerdo |
  | `\]`     | colchete direito |
  | `\ddd`   | caractere indicado por seu valor numérico, em que `ddd` é uma sequência de até três dígitos _decimais_ |

  ```lua
  my_string = "hello"
  another_string = 'world'
  print(my_string .. another_string) --> "helloworld"

  print("10.2" + 1) --> 11.2
  print(my_string + 1) -- erro, não é possível converter "hello"
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
: Funções são valores de primeira classe em Lua, o que significa que você pode passá-las como parâmetros para funções e retorná-las como valores. Variáveis atribuídas a uma função contêm uma referência à função. Você pode atribuir variáveis a funções anônimas, mas Lua fornece açúcar sintático (`function name(param1, param2) ... end`) por conveniência.

  ```lua
  -- Atribui 'my_plus' a uma função
  my_plus = function(p, q)
      return p + q
  end

  print(my_plus(4, 5)) --> 9

  -- Sintaxe conveniente para atribuir função à variável 'my_mult'
  function my_mult(p, q)
      return p * q
  end

  print(my_mult(4, 5)) --> 20

  -- Recebe uma função como parâmetro 'func'
  function operate(func, p, q)
      return func(p, q) -- Chama a função fornecida com os parâmetros 'p' e 'q'
  end

  print(operate(my_plus, 4, 5)) --> 9
  print(operate(my_mult, 4, 5)) --> 20

  -- Cria uma função somadora e a retorna
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
: Tabelas são o único tipo de estruturação de dados em Lua. Elas são _objetos_ de array associativo usados para representar listas, arrays, sequências, tabelas de símbolos, conjuntos, registros, grafos, árvores etc. Tabelas são sempre anônimas, e variáveis às quais você atribui uma tabela não contêm a tabela em si, mas uma referência a ela. Ao inicializar uma tabela como sequência, o primeiro índice é `1`, não `0`.

  ```lua
  -- Inicializa uma tabela como sequência
  weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday"}
  print(weekdays[1]) --> "Sunday"
  print(weekdays[5]) --> "Thursday"

  -- Inicializa uma tabela como registro com valores de sequência
  moons = { Earth = { "Moon" },
            Uranus = { "Puck", "Miranda", "Ariel", "Umbriel", "Titania", "Oberon" } }
  print(moons.Uranus[3]) --> "Ariel"

  -- Constrói uma tabela a partir de um construtor vazio {}
  a = 1
  t = {}
  t[1] = "first"
  t[a + 1] = "second"
  t.x = 1 -- igual a t["x"] = 1

  -- Itera sobre os pares chave, valor da tabela
  for key, value in pairs(t) do
      print(key, value)
  end
  --> 1   first
  --> 2   second
  --> x   1

  u = t -- u agora referencia a mesma tabela que t
  u[1] = "changed"

  for key, value in pairs(t) do -- ainda iterando sobre t!
      print(key, value)
  end
  --> 1   changed
  --> 2   second
  --> x   1
  ```

userdata
: Userdata é fornecido para permitir que dados C arbitrários sejam armazenados em variáveis Lua. O Defold usa objetos userdata de Lua para armazenar valores Hash (hash), objetos URL (url), objetos matemáticos (vector3, vector4, matrix4, quaternion), objetos de jogo, nodes GUI (node), predicados de Render (predicate), alvos de Render (render_target) e buffers de constantes de Render (constant_buffer)

thread
: Threads representam threads independentes de execução e são usadas para implementar corrotinas. Veja abaixo para detalhes.

## Operadores

Operadores aritméticos
: Operadores matemáticos `+`, `-`, `*`, `/`, o `-` unário (negação) e exponencial `^`.

  ```lua
  a = -1
  print(a * 2 + 3 / 4^5) --> -1.9970703125
  ```

  Lua fornece conversões automáticas entre números e strings em tempo de execução. Qualquer operação numérica aplicada a uma string tenta converter a string para um número:

  ```lua
  print("10" + 1) --> 11
  ```

Operadores relacionais/de comparação
: `<` (menor que), `>` (maior que), `<=` (menor ou igual), `>=` (maior ou igual), `==` (igual), `~=` (diferente). Esses operadores sempre retornam `true` ou `false`. Valores de tipos diferentes são considerados diferentes. Se os tipos forem os mesmos, eles são comparados de acordo com seu valor. Lua compara tabelas, userdata e funções por referência. Dois valores assim são considerados iguais apenas se referenciam o mesmo objeto.

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
: `and`, `or` e `not`. `and` retorna seu primeiro argumento se ele for `false`; caso contrário, retorna seu segundo argumento. `or` retorna seu primeiro argumento se ele não for `false`; caso contrário, retorna seu segundo argumento.

  ```lua
  print(true or false) --> true
  print(true and false) --> false
  print(not false) --> true

  if a == 5 and b == 6 then
      print("a is 5 and b is 6")
  end
  ```

Concatenação
: Strings podem ser concatenadas com o operador `..`. Números são convertidos para strings quando concatenados.

  ```lua
  print("donkey" .. "kong") --> "donkeykong"
  print(1 .. 2) --> "12"
  ```

Comprimento
: O operador unário de comprimento `#`. O comprimento de uma string é seu número de bytes. O comprimento de uma tabela é o comprimento da sequência, o número de índices numerados a partir de `1` e para cima em que o valor não é `nil`. Observação: se a sequência tiver "buracos" com valor `nil`, o comprimento pode ser qualquer índice anterior a um valor `nil`.

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

## Controle de fluxo

Lua fornece o conjunto usual de construções de controle de fluxo.

if---then---else
: Testa uma condição, executa a parte `then` se a condição for verdadeira; caso contrário, executa a parte `else` (opcional). Em vez de aninhar instruções `if`, você pode usar `elseif`. Isso substitui uma instrução switch, que Lua não tem.

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
: Testa uma condição e executa o bloco enquanto ela for verdadeira.

  ```lua
  weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday"}

  -- Imprime cada dia da semana
  i = 1
  while weekdays[i] do
      print(weekdays[i])
      i = i + 1
  end
  ```

repeat---until
: Repete o bloco até que uma condição seja verdadeira. A condição é testada depois do corpo, então ele será executado pelo menos uma vez.

  ```lua
  weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday"}

  -- Imprime cada dia da semana
  i = 0
  repeat
      i = i + 1
      print(weekdays[i])
  until weekdays[i] == "Saturday"
  ```

for
: Lua tem dois tipos de loop `for`: numérico e genérico. O `for` numérico recebe 2 ou 3 valores numéricos, enquanto o `for` genérico itera sobre todos os valores retornados por uma função _iterator_.

  ```lua
  -- Imprime os números de 1 a 10
  for i = 1, 10 do
      print(i)
  end

  -- Imprime os números de 1 a 10 e incrementa em 2 a cada vez
  for i = 1, 10, 2 do
      print(i)
  end

  -- Imprime os números de 10 a 1
  for i=10, 1, -1 do
      print(i)
  end

  t = { "a", "b", "c", "d" }
  -- Itera sobre a sequência e imprime os valores
  for i, v in ipairs(t) do
      print(v)
  end
  ```

break e return
: Use a instrução `break` para sair de um bloco interno de um loop `for`, `while` ou `repeat`. Use `return` para retornar um valor de uma função ou para finalizar a execução de uma função e retornar ao chamador. `break` ou `return` podem aparecer apenas como a última instrução de um bloco.

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

## Locais, globais e escopo léxico

Todas as variáveis que você declara são globais por padrão, o que significa que elas ficam disponíveis por todas as partes do contexto de runtime Lua. Você pode declarar variáveis explicitamente como `local`, o que significa que a variável existirá apenas dentro do escopo atual.

Cada arquivo-fonte Lua define um escopo separado. Declarações locais no nível mais alto de um arquivo significam que a variável é local ao arquivo de script Lua. Cada função cria outro escopo aninhado, e cada bloco de estrutura de controle cria escopos adicionais. Você pode criar explicitamente um escopo com as palavras-chave `do` e `end`. Lua tem escopo léxico, o que significa que um escopo tem acesso total às variáveis _local_ do escopo envolvente. Observe que as variáveis locais devem ser declaradas antes do uso.

```lua
function my_func(a, b)
    -- 'a' e 'b' são locais a esta função e disponíveis em seu escopo

    do
        local x = 1
    end

    print(x) --> nil. 'x' não está disponível fora do escopo do-end
    print(foo) --> nil. 'foo' é declarado depois de 'my_func'
    print(foo_global) --> "value 2"
end

local foo = "value 1"
foo_global = "value 2"

print(foo) --> "value 1". 'foo' está disponível no escopo mais alto após a declaração.
```

Observe que, se você declarar funções `local` em um arquivo de script (o que geralmente é uma boa ideia), precisa prestar atenção à ordem do código. Você pode usar declarações antecipadas se tiver funções que chamam umas às outras mutuamente.

```lua
local func2 -- Declara antecipadamente 'func2'

local function func1(a)
    print("func1")
    func2(a)
end

function func2(a) -- ou func2 = function(a)
    print("func2")
    if a < 10 then
        func1(a + 1)
    end
end

function init(self)
    func1(1)
end
```

Se você escrever uma função dentro de outra função, ela também terá acesso total às variáveis locais da função envolvente. Esta é uma construção muito poderosa.

```lua
function create_counter(x)
    -- 'x' é uma variável local em 'create_counter'
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

## Sombreamento de variáveis

Variáveis locais declaradas em um bloco sombrearão variáveis de um bloco externo com o mesmo nome.

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

## Corrotinas

Funções executam do início ao fim e não há como pará-las no meio. Corrotinas permitem fazer isso, o que pode ser muito conveniente em alguns casos. Suponha que queremos criar uma animação frame a frame muito específica em que movemos um objeto de jogo da posição y `0` para algumas posições y específicas do frame 1 ao frame 5. Poderíamos resolver isso com um contador na função `update()` (veja abaixo) e uma lista de posições. No entanto, com uma corrotina, obtemos uma implementação muito limpa, fácil de estender e de trabalhar. Todo o estado fica contido dentro da própria corrotina.

Quando uma corrotina cede, ela retorna o controle ao chamador, mas lembra seu ponto de execução para poder continuar dali mais tarde.

```lua
-- Esta é a nossa corrotina
local function sequence(self)
    coroutine.yield(120)
    coroutine.yield(320)
    coroutine.yield(510)
    coroutine.yield(240)
    return 440 -- retorna o valor final
end

function init(self)
    self.co = coroutine.create(sequence) -- Cria a corrotina. 'self.co' é um objeto thread
    go.set_position(vmath.vector3(100, 0, 0)) -- Define a posição inicial
end

function update(self, dt)
    local status, y_pos = coroutine.resume(self.co, self) -- Continua a execução da corrotina.
    if status then
        -- Se a corrotina ainda não terminou/morreu, usa seu valor retornado por yield como nova posição
        go.set_position(vmath.vector3(100, y_pos, 0))
    end
end
```


## Contextos Lua no Defold

Todas as variáveis que você declara são globais por padrão, o que significa que elas ficam disponíveis por todas as partes do contexto de runtime Lua. O Defold tem uma configuração *shared_state* em *game.project* que controla esse contexto. Se a opção estiver definida, todos os scripts, scripts de GUI e o script de renderização serão avaliados no mesmo contexto Lua, e variáveis globais ficarão visíveis em todos os lugares. Se a opção não estiver definida, a engine executará scripts, scripts de GUI e o script de renderização em contextos separados.

![Contexts](images/lua/lua_contexts.png)

O Defold permite usar o mesmo arquivo de script em vários componentes de objeto de jogo separados. Quaisquer variáveis declaradas localmente são compartilhadas entre componentes que executam o mesmo arquivo de script.

```lua
-- 'my_global_value' estará disponível a partir de todos os scripts, gui_scripts, render script e módulos (arquivos Lua)
my_global_value = "global scope"

-- este valor será compartilhado por todas as instâncias de componente que usam este arquivo de script específico
local script_value = "script scope"

function init(self, dt)
    -- Este valor estará disponível nesta instância de componente de script
    self.foo = "self scope"

    -- este valor estará disponível dentro de init() e após sua declaração
    local local_foo = "local scope"
    print(local_foo)
end

function update(self, dt)
    print(self.foo)
    print(my_global_value)
    print(script_value)
    print(local_foo) -- imprimirá nil, pois local_foo só é visível em init()
end
```

## Considerações de desempenho

Em um jogo de alto desempenho destinado a rodar a 60 FPS estáveis, pequenos erros de desempenho podem ter um grande impacto na experiência. Há algumas coisas gerais simples a considerar e algumas coisas que talvez não pareçam problemáticas.

Começando pelas coisas simples. Em geral, é uma boa ideia escrever código direto que não contenha loops desnecessários. Às vezes você precisa iterar sobre listas de coisas, mas tenha cuidado se a lista de coisas for suficientemente grande. Este exemplo roda em pouco mais de 1 milissegundo em um laptop bastante decente, o que pode fazer toda a diferença se cada frame tiver apenas 16 milissegundos (a 60 FPS) e a engine, o script de renderização, a simulação de física e assim por diante consumirem uma parte disso.

```lua
local t = socket.gettime()
local table = {}
for i=1,2000 do
    table[i] = vmath.vector3(i, i, i)
end
print((socket.gettime() - t) * 1000)

-- DEBUG:SCRIPT: 0.40388
```

Use o valor retornado por `socket.gettime()` (segundos desde a época do sistema) para fazer benchmark de código suspeito.

## Memória e coleta de lixo

A coleta de lixo de Lua roda automaticamente em segundo plano por padrão e recupera memória alocada pelo runtime Lua. Coletar muito lixo pode ser uma tarefa demorada, então é bom manter baixo o número de objetos que precisam ser coletados:

* Variáveis locais em si são gratuitas e não gerarão lixo. (ou seja, `local v = 42`)
* Cada string _nova e única_ cria um novo objeto. Escrever `local s = "some_string"` criará um novo objeto e atribuirá `s` a ele. O `s` local em si não gerará lixo, mas o objeto string sim. Usar a mesma string várias vezes não adiciona custo extra de memória.
* Cada vez que um construtor de tabela é executado (`{ ... }`), uma nova tabela é criada.
* Executar uma _instrução de função_ cria um objeto closure. (ou seja, executar a instrução `function () ... end`, não chamar uma função definida)
* Funções vararg (`function(v, ...) end`) criam uma tabela para as reticências cada vez que a função é _chamada_ (em Lua antes da versão 5.2, ou se não estiver usando LuaJIT).
* `dofile()` e `dostring()`
* Objetos userdata

Há muitos casos em que você pode evitar criar novos objetos e, em vez disso, reutilizar os que já tem. Por exemplo, o seguinte é comum ao final de cada `update()`:

```lua
-- Redefine a velocidade
self.velocity = vmath.vector3()
```

É fácil esquecer que cada chamada a `vmath.vector3()` cria um novo objeto. Vamos descobrir quanta memória um `vector3` usa:

```lua
print(collectgarbage("count") * 1024)       -- 88634
local v = vmath.vector3()
print(collectgarbage("count") * 1024)       -- 88704. 70 bytes no total foram alocados
```

70 bytes foram adicionados entre as chamadas a `collectgarbage()`, mas isso inclui alocações para mais do que o objeto `vector3`. Cada impressão do resultado de `collectgarbage()` cria uma string que por si só adiciona 22 bytes de lixo:

```lua
print(collectgarbage("count") * 1024)       -- 88611
print(collectgarbage("count") * 1024)       -- 88633. 22 bytes alocados
```

Então um `vector3` pesa 70-22=48 bytes. Isso não é muito, mas se você criar _um_ a cada frame em um jogo de 60 FPS, de repente são 2,8 kB de lixo por segundo. Com 360 componentes de script, cada um criando um `vector3` a cada frame, estamos olhando para 1 MB de lixo gerado por segundo. Os números podem crescer muito rapidamente. Quando o runtime Lua coleta lixo, ele pode consumir muitos milissegundos preciosos, especialmente em plataformas mobile.

Uma forma de evitar alocações é criar um `vector3` e continuar trabalhando com o mesmo objeto. Por exemplo, para redefinir um `vector3`, podemos usar a seguinte construção:

```lua
-- Em vez de fazer self.velocity = vmath.vector3(), que cria um novo objeto,
-- zeramos os componentes de um objeto vetor de velocidade existente
self.velocity.x = 0
self.velocity.y = 0
self.velocity.z = 0
```

O esquema padrão de coleta de lixo pode não ser ideal para algumas aplicações críticas em tempo. Se você notar um stutter no seu jogo ou app, talvez queira ajustar como Lua coleta lixo por meio da função Lua [`collectgarbage()`](/ref/base/#collectgarbage). Você pode, por exemplo, executar o coletor por um curto período a cada frame com um valor baixo de `step`. Para ter uma ideia de quanta memória seu jogo ou app está consumindo, você pode imprimir a quantidade atual de bytes de lixo com:

```lua
print(collectgarbage("count") * 1024)
```

## Boas práticas

Uma consideração comum de design de implementação é como estruturar código para comportamentos compartilhados. Várias abordagens são possíveis.

Comportamentos em um módulo
: Encapsular um comportamento em um módulo permite compartilhar código facilmente entre componentes de script de diferentes objetos de jogo (e scripts de GUI). Ao escrever funções de módulo, em geral é melhor escrever código estritamente funcional. Há casos em que estado armazenado ou efeitos colaterais são uma necessidade (ou levam a um design mais limpo). Se você precisa armazenar estado interno no módulo, esteja ciente de que componentes compartilham contextos Lua. Veja a [documentação de Módulos](/manuals/modules) para detalhes.

  ![Module](images/lua/lua_module.png)

  Além disso, mesmo que seja possível fazer o código de módulo modificar diretamente os internos de um objeto de jogo (passando `self` para uma função de módulo), desencorajamos fortemente isso, pois você criará um acoplamento muito forte.

Um objeto de jogo auxiliar com comportamento encapsulado
: Assim como você pode conter código de script em um módulo Lua, pode contê-lo em um objeto de jogo com um componente de script. A diferença é que, se você o contém em um objeto de jogo, pode se comunicar com ele estritamente por passagem de mensagens.

  ![Helper](images/lua/lua_helper.png)

Agrupando objeto de jogo com objeto de comportamento auxiliar dentro de uma coleção
: Neste design, você pode criar um objeto de jogo de comportamento que atua automaticamente sobre outro objeto de jogo alvo, seja por um nome predefinido (o usuário precisa renomear o objeto alvo para corresponder) ou por meio de uma URL `go.property()` que aponta para o objeto de jogo alvo.

  ![Collection](images/lua/lua_collection.png)

  O benefício dessa configuração é que você pode soltar um objeto de jogo de comportamento em uma coleção contendo o objeto alvo. Nenhum código adicional é necessário.

  Em situações em que você precisa gerenciar grandes quantidades de objetos de jogo, esse design não é preferível, pois o objeto de comportamento é duplicado para cada instância e cada objeto terá custo de memória.
