# Lua in Defold
디폴드 엔진은 스크립팅을 위한 Lua 언어가 내장되어 있습니다. Lua는 강력하고, 빠르며 가볍고 쉽게 임베드 되는 동적언어입니다. 이것은 비디오 게임 스크립팅 언어로 널리 사용되고 있습니다. Lua 프로그램은 간단한 절차적인 방식으로 실행됩니다. 이 언어는 동적으로 타이핑되며 바이트코드 인터프리터에 의해 실행됩니다. 증가하는 가비지 컬렉션을 관리하기 위한 자동 메모리 관리 기능도 있습니다. 

이 매뉴얼은 Defold에서 Lua로 작업할 때 무엇이 필요한지 고려하며 Lua 프로그래밍의 기본을 빠르게 소개할 것입니다.  만약 당신이 파이썬, 펄, 루비, 자바스크립트 같은 다른 동적 언어에 경험이 있다면, 당신은 좀 더 빨리 이해할 수도 있습니다.  당신이 만약 프로그래밍을 완전히 처음 시작한다면 초심자를 위한 Lua 책이 필요할 수도 있습니다. 선택지는 많이 있습니다.

## Lua versions
우리는 Defold가 모든 플랫폼에서 같은 동작을 하는데 촛점을 맞추고 있습니다. 하지만 현재 Lua 버전간에 약간의 불일치가 있습니다.  HTML5와 iOS 64 비트 플랫폼의 경우 우리는 Lua 5.1을 사용하지만 다른 플랫폼에서는 LuaJIT을 사용합니다. LuaJIT은 5.1 기반이긴 하지만 몇가지 부가적인 기능이 더 추가되었습니다.

**게임이 모든 플랫폼에서 동일하게 작동하도록 하려면 Lua 5.1에 맞춰 개발하는것이 좋습니다.**

## Lua books and resources
- Programming in Lua (first edition) Later editions are available in print.
- Lua 5.1 reference manual
- Beginning Lua Programming (Wrox, 2007)
- Game Development with Lua (Charles River Media, 2005)

## Syntax
프로그램 문법은 간단하고 쉽게 읽을 수 있습니다. 명령문은 각 라인마다 하나씩 쓰여지며 명령문의 끝을 표시할 필요가 없습니다. 선택적으로 세미콜론;으로 명령문을 구분할 수 있습니다. 코드블록은 키워드로 구분되며 end 키워드로 끝을 구분합니다. 주석은 블록이나 각 줄의 끝에 쓸 수 있습니다.
```lua
--[[
이렇게 여러줄로 주석을 
쓸 수 있습니다.
--]]

a = 10
b = 20 ; c = 30 -- 한 줄에서 명령어 두 개 쓰기

if my_variable == 3 then
    call_some_function(true) -- 한 줄 주석 쓰기
else
    call_another_function(false)
end
```

## Variables and data types
Lua는 동적으로 자료형이 정해지는데 실제 값은 자료형이 있지만 변수는 없는 것을 의미합니다. 즉 다른 정적 타입언어와 달리 원하는대로 변수에 아무 값이나 할당할 수 있습니다. Lua에는 8가지 기본 자료형이 있습니다.

#### nil
이 자료형은 nil값을 가지고 있습니다.  일반적으로 할당되지 않은 변수와 같이 의미있는 값이 없음을 나타냅니다.
```lua
print(my_var) -- "my_var"변수에 아직 값이 지정되지 않았다면 "nil"이 출력됩니다.
```

#### boolean
불린은 true나 false값을 가지고 있습니다. false나 nil인 조건은 false값이 되며, 다른 모든 값은 true가 됩니다.
```lua
flag = true
if flag then
    print("flag는 true이다.")
else
    print("flag는 false이다.")
end

if my_var then
    print("my_var는 nil도 false도 아니다!")
end

if not my_var then
    print("my_var는 nil이거나 false이다!")
end
```

#### number
숫자형은 내부적으로 64비트 정수(integer) 또는 64비트 부동 소숫점(float)으로 표시됩니다. Lua는 필요에 따라 자동적으로 이러한 표현을 변환하므로 일반적으로 걱정할 필요가 없습니다.

```lua
print(10) --> prints '10'
print(10.0) --> '10'
print(10.000000000001) --> '10.000000000001'

a = 5 -- integer
b = 7/3 -- float
print(a - b) --> '2.6666666666667'
```

#### string
문자열은 널문자(\0)를 포함하는 8비트값을 가지는 불변의 바이트 시퀀스(immutable sequences of bytes)입니다. Lua는 문자열의 내용에 대해 아무런 추정을 하지 않으므로 어떠한 데이터든 저장할 수 있습니다. 문자열의 정의는 쌍따옴표(")나 싱글따옴표(')로 쓸 수 있습니다. Lua는 런타임에 숫자와 문자열을 변환합니다. 문자열은 .. 연산자에 의해 문자열 끼리 연결할 수 있습니다.

문자열은 C언어 스타일의 이스케이프 시퀀스를 따릅니다 :

| | |
| ------------ | ------------ |
|   \a  |   bell    |
|   \b  |   back space      |
|   \f  |   form feed   |
|   \n  |   newline |
|   \r  |   carriage return |
|   \t  |   horizontal tab  |
|   \v  |   vertical tab    |
|   \\\ |   backslash   |
|   \"  |   double quote    |
|   \'  |   single quote    |
|   \\[ |   left square bracket |
|   \\] |   right square bracket    |
|   \ddd    |   10진수를 표시하며 여기서 ddd는 최대 3자리로 표시됩니다.  |

```lua
my_string = "hello"
another_string = 'world'
print(my_string .. another_string) --> "helloworld"

print("10.2" + 1) --> 11.2
print(my_string + 1) -- 에러, "hello"를 숫자로 변환할 수 없음
print(my_string .. 1) --> "hello1"

print("one\nstring") --> one
                                 --> string

print("\097bc") --> "abc"

multi_line_string = [[
여러줄로 구성된 문자열입니다. 이것은 모두 문자열
변수에 저장되며 매우 유용합니다.
]]
```

#### function
함수는 Lua에서 최상위 값입니다. 즉 함수에 파라미터를 전달하거나 값을 반환 할 수 있습니다. 함수에 할당된 변수는 함수에 대한 참조(reference)를 포함합니다. 변수를 익명함수에 할당 할 수 있지만 Lua는 편의상  (function name(param1, param2) …? end) 와 같은 문법을 제공합니다.
```lua
-- 'my_plus'에 함수를 할당하기
my_plus = function(p, q)
    return p + q
end

print(my_plus(4, 5)) --> 9

-- 변수 'my_mult'에 함수를 할당하는 편리한 방법
function my_mult(p, q)
    return p * q
end

print(my_mult(4, 5)) --> 20

-- 함수를 'func' 매개변수로 가져옴
function operate(func, p, q)
    return func(p, q) -- 'p'와 'q' 매개변수를 제공된 함수로 호출
end

print(operate(my_plus, 4, 5)) --> 9
print(operate(my_mult, 4, 5)) --> 20

-- adder 함수를 생성하고 반환함
function create_adder(n)
    return function(a)
        return a + n
    end
end

adder = create_adder(2)
print(adder(3)) --> 5
print(adder(10)) --> 12
```

#### table
테이블은 Lua의 유일한 구조적 데이터 타입입니다. 이것은 리스트, 배열, 시퀀스, 심볼테이블, 세트, 레코드, 그래프, 트리 등을 표현하는데 사용되는 관계형 배열 객체(associative array object)입니다. 테이블은 항상 익명이며 테이블을 할당하는 변수는 테이블 자체값은 포함할 수 없지만 참조값은 포함 할 수 있습니다. 테이블을 시퀀스로(순서대로) 초기화 할 때, 첫 번째 인덱스 번호는 0이 아니라 1입니다.
```lua
-- 테이블을 시퀀스로 초기화
weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday"}
print(weekdays[1]) --> "Sunday"
print(weekdays[5]) --> "Thursday"

-- 시퀀스 값을 사용하여 테이블을 레코드로 초기화
moons = { Earth = { "Moon" }, Uranus = { "Puck", "Miranda", "Ariel", "Umbriel", "Titania", "Oberon" } }
print(moons.Uranus[3]) --> "Ariel"

-- 테이블을 빈 생성자{} 로 만들기
a = 1
t = {}
t[1] = "first"
t[a + 1] = "second"
t.x = 1 -- same as t["x"] = 1

-- 테이블의 키, 값을 쌍으로 반복하기
for key, value in pairs(t) do
    print(key, value)
end
--> 1   first
--> 2   second
--> x   1

u = t -- u는 이제 t와 같은 테이블을 참조함
u[1] = "changed"

for key, value in pairs(t) do -- 여전히 t로 반복중!
    print(key, value)
end
--> 1   changed
--> 2   second
--> x   1
```
#### userdata
유저데이터는 임의의 C 데이터를 Lua 변수에 저장 할 수 있도록 제공되고 있습니다. Defold는 Hash값(hash), URL 객체(url), 수학 객체(vertor3, vector4, matrix4, quaternion), 게임 객체, GUI노드(node), 렌더 서술자(predicate), 렌더 타겟 (render_target), 렌더 상수 버퍼(constant_buffer)을 저장하는데 유저데이터 객체를 사용합니다.

#### thread
스레드는 독립적인 실행 스레드를 나타내며 코루틴(coroutines)을 구현하는데 사용됩니다. 자세한 것은 아래를 참고 바랍니다.


## Operators
#### Arithmetic operators(산술 연산자)
수학 연산자 +, -, *, /, 단항- (부정), 지수 ^
```lua
a = -1
print(a * 2 + 3 / 4^5) --> -1.9970703125
```

#### Relational/comparison operators(관계/비교 연산자)
< (~보다 작은), > (~보다 큰), <= (~보다 작거나 같은), >= (~보다 크거나 같은), == (같은), ~= (같지 않은). 이 연산자들은 항상 true나 false를 반환합니다. 서로 다른 자료형의 값은 다른 것으로 간주됩니다. 만약 자료형이 같을 경우, 자료형에 맞게 비교됩니다.  Lua는 테이블, 유저데이터, 함수는 참조(reference)에 의해 비교합니다. 같은 오브젝트를 참조하는 경우에만 두 값이 같은 것으로 간주합니다.
```lua
a = 5
b = 6

if a <= b then
    print("a는 b보다 작거나 같다.")
end
```
논리 연산자: and, or, not. and연산자는 false일 경우 첫번째 인수를 반환하고, 그렇지 않으면 두번째 인수를 반환합니다. or연산자는 false가 아닐 경우 첫번째 인수를 반환하고, 그렇지 않으면 두번째 인수를 반환합니다.
```lua
print(true or false) --> true
print(true and false) --> false
print(not false) --> true

if a == 5 and b == 6 then
    print("a는 5이고 b는 6이다.")
end
```

#### Concatenation (연결)
문자열은 ..연산자로 연결할 수 있습니다. 숫자형을 연결하면 문자열로 변환됩니다.
```lua
print("donkey" .. "kong") --> "donkeykong"
print(1 .. 2) --> "12"
```

#### Length
단항 길이 연산자인 #은 문자열의 길이를 바이트 수로 계산합니다. 테이블의 길이는 시퀀스의 갯수로 계산되며, 인덱스 번호는 0이 아니라 1부터 색인됩니다. 주의: 만약 마지막 시퀀스가 nil값이라면 선행 시퀀스의 인덱스가 길이가 됩니다.
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

## Flow control (흐름제어)
Lua는 일반적인 흐름제어를 제공합니다.

#### if then else
조건을 테스트할 때, 조건이 true이면 then구문을 실행하고, 그렇지 않으면 (선택적으로) else구문을 실행합니다. if문을 중첩하는 대신 elseif 구문을 사용할 수 있습니다. 이것은 Lua가 가지고 있지 않은 switch문을 대체합니다.
```lua
a = 5
b = 4

if a < b then
    print("a는 b보다 작습니다.")
end

if a == '1' then
    print("a는 1이다.")
elseif a == '2' then
    print("a는 2이다.")
elseif a == '3' then
    print("a는 3이다.")
else
    print("이게 뭔지 모르겠어...")
end
```

#### while
조건이 true일 동안 구간을 반복 실행합니다.
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

#### repeat until
조건이 true일때까지 구간이 반복됩니다. 이 조건은 구간 뒤에 계산되므로 적어도 한 번은 실행 됩니다.
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

#### for
Lua는 for반복문을 위해 numeric과 generic 방식이 있습니다. numeric은 2나 3 같은 숫자값을 취하는 반면, generic은 iterator 함수에 의해 모든 값들을 반복순환하며 반환합니다.
```lua
-- 1에서 10까지 숫자 출력하기
for i = 1, 10 do
    print(i)
end

-- 1에서 10까지 2씩 건너뛰며 숫자 출력하기
for i = 1, 10, 2 do
    print(i)
end

-- 10에서 1까지 출력하기
for i=10, 1, -1 do
    print(i)
end

t = { "a", "b", "c", "d" }
-- 시퀀스를 반복하며 값 출력하기
for i, v in ipairs(t) do
    print(v)
end
```

#### break and return
break구문은 for, while, repeat같은 반복문 블록 안에서 빠져나올 때 사용됩니다. return구문은 함수가 값을 반환하거나 실행을 끝내야 할 때 사용됩니다. break와 return은 블록에서 마지막 명령어로 사용되어야 합니다.
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

## Locals, globals and lexical scoping
모든 변수는 기본적으로 global 변수이며 Lua 런타임 컨텍스트의 모든 곳에서 접근 할 수 있습니다. 아니면 명확하게 현재 범위에서만 접근 할 수 있게 local 변수를 선언 할 수도 있습니다.

Lua는 소스 파일에 따라 분리된 영역을 가지고 있습니다. 한 파일에서 최상위 레벨의 local변수 선언은 Lua 스크립트 파일의 local 변수임을 의미합니다. 각 함수는 또다른 중첩 영역을 생성하며 각 제어 구조 블록은 추가적인 영역을 생성합니다. do와 end 키워드를 사용하여 명확한 별도 영역을 만들 수도 있습니다. Lua는 언어적인 영역(lexical scope)를 가지고 있으며 이는 둘러싸인 영역으로부터 local변수에 모든 접근을 할 수 있다는 것을 의미합니다. local변수는 사용하기 전에 선언부터 해야함을 알아두기 바랍니다.

```lua
function my_func(a, b)
    -- 'a'와 'b'는 이 함수의 local변수이며 이 영역 안에서 사용 가능합니다.
    do
        local x = 1
    end

    print(x) --> nil. 'x'는 do-end구문 안에서 선언되었으므로 사용할 수 없습니다.
    print(foo) --> nil. 'foo'는 'my_func'이후에 선언되었습니다.
    print(foo_global) --> "value 2"
end

local foo = "value 1"
foo_global = "value 2"

print(foo) --> "value 1". 'foo'는 선언 이후이고 최상위 영역에 있으므로 사용가능합니다.
```
스크립트 파일에서 local함수를 선언하는 것은(일반적으로 좋은 방법입니다.) 코드의 순서를 주의깊게 살펴볼 필요가 있습니다. 서로 호출되는 함수가 필요할 경우엔 전방선언(forward declarations)이 필요할 수도 있습니다.
```lua
local func2 -- 'func2'를 전방선언함

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
만약 다른 함수에 둘러싸인 함수를 만든다면, 안쪽 함수 역시  local 변수들에 모든 접근이 가능합니다. 이 방식은 다양한 생성자를 만드는데 매우 유용합니다.
```lua
function create_counter(x)
    -- 'x'는 'create_counter'함수의 로컬변수입니다.
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
#### Variable shadowing
같은 이름으로 재선언된 변수는 그림자효과가 발생하게 되어 재설정됩니다.
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

## Coroutines
함수는 처음부터 끝까지 실행되며 중간에 멈출 방법이 없지만, 코루틴은 편리한 방법으로 그것을 가능하게 합니다. 만약 게임 오브젝트의 y좌표를 특정한 위치로 이동시키며 프레임마다 애니메이션 효과를 줘야 한다고 생각해봅시다. 아래에서 보는 것 처럼 update() 함수를 활용하여 이 문제를 해결 할 수 있지만 코루틴을 사용하여 쉬운 방법으로 더 확장 할 수도 있습니다. 모든 상태값은 코루틴 안에 저장됩니다.

코루틴에서 yield가 호출될 때 제어권이 호출자에게 반환되지만 실행 지점이 기억되어 나중에 계속 실행되게 됩니다.
```lua
-- 이것이 바로 우리의 코루틴!
local function sequence(self)
    coroutine.yield(120)
    coroutine.yield(320)
    coroutine.yield(510)
    coroutine.yield(240)
    return 440 -- 마지막 값을 반환한다.
end

function init(self)
    self.co = coroutine.create(sequence) -- 코루틴을 생성하여 'self.co'를 스레드 오브젝트로 만든다.
    go.set_position(vmath.vector3(100, 0, 0)) -- 위치 초기화하기
end

function update(self, dt)
    local status, y_pos = coroutine.resume(self.co, self) -- 코루틴을 재실행한다.
    if status then
        -- 코루틴이 아직 살아 있다면 yield가 새 위치값을 반환할 것이다.
        go.set_position(vmath.vector3(100, y_pos, 0))
    end
end
```

## Defold scripts
Defold 에디터는 Lua 스크립팅을 위해 문법 컬러링과 자동완성 기능을 지원합니다. Defold 함수 이름을 완성시키기 위해 Ctrl+Space를 누르면 입력중인 함수명에 알맞은 함수 목록을 보여줍니다.

![Auto completion](images/lua/lua_completion.png)

Defold의 Lua 스크립트는 3가지 형식으로 구분되며, 각각 다른 Defold 라이브러리를 사용할 수 있습니다.

#### Logic scripts
확장자는 .script 이며 게임 오브젝트의 스크립트 컴포넌트에 의해 실행됩니다. 로직 스크립트는 일반적으로 게임 오브젝트를 제어하거나 레벨을 로딩하여 게임 규칙 등과 엮는 로직을 구현하는데 사용됩니다. 로직 스크립트는 GUI나 Render 함수를 제외한 모든 Defold 라이브러리 함수에 접근 할 수 있습니다. 

#### GUI scripts
확장자는 .guiscript 이며 GUI컴포넌트에 의해 실행되고 일반적으로 HUD나 메뉴 같은 GUI요소들을 표시하는데 요구되는 로직을 포함하고 있습니다. GUI스크립트는 GUI라이브러리 함수에 접근 할 수 있습니다.

#### Render scripts
확장자는 .renderscript 이며 렌더링 파이프라인에 의해 실행되고 각 프레임마다 게임의 모든 그래픽을 렌더링하는데 필요한 로직을 포함하고 있습니다. 렌더 스크립트는 Render 라이브러리 함수에 접근 할 수 있습니다.

## Script execution and callbacks
Defold는 Lua 스크립트를 엔진 라이프사이클의 일부로 실행하며 미리 정의된 콜백 함수들을 노출합니다. 게임 오브젝트에 스크립트 컴포넌트를 추가하면 이 스크립트는 해당 게임오브젝트와 컴포넌트의 수명주기의 일부가 됩니다. 이 스크립트는 로드될 때 루아 컨텍스트에 의해 평가되고, 엔진은 아래 함수들을 실행하고 현재 스크립트 컴포넌트의 인스턴스의 참조값을 매개변수로 전달합니다. 여기서 "self" 명령어를 이용하여 컴포넌트 인스턴스 상태에 접근할 수 있습니다. "self"는 Lua의 table과 비슷한 userdata 오브젝트이지만 pairs()나 ipairs()같은 반복문으로 접근할 수는 없습니다.

#### init(self)
컴포넌트가 초기화 될때 호출됩니다.
```lua
function init(self)
    -- 현재 컴포넌트와 생명주기를 함께 하는 변수들
    self.my_var = "something"
    self.age = 0
end
```
#### final(self)
컴포넌트가 삭제될 때 호출됩니다. 예를 들어 스폰된 게임 오브젝트가 컴포넌트와 함께 삭제 처리가 필요한 경우에 유용합니다.
```lua
function final(self)
    if self.my_var == "something" then
        -- 이것저것 삭제 처리
    end
end
```
#### update(self, dt)
매 프레임마다  한번씩 호출됩니다. dt는 최근 프레임 이후의 delta time입니다.
```lua
function update(self, dt)
    self.age = self.age + dt -- 흐른 시간만큼 age 값이 증가함
end
```
#### on_message(self, message_id, message, sender)
msg.post()를 이용하여 스크립트 컴포넌트로 메세지를 보내면, 게임엔진은 수신자 컴포넌트의 이 함수를 호출합니다.
#### on_input(self, action_id, action)
인풋 설정 후에 이 컴포넌트에서 입력이 감지되면 (acquire_input_focus 참고), 게임엔진은 이 함수를 실행합니다.
#### on_reload(self)
이 함수는 에디터에서 (Edit ▸ Reload Resource) 메뉴를 실행하면 핫리로드 기능을 통해 스크립트가 재 로딩될 때 호출됩니다. 이 기능은 디버깅, 테스트, 최적화가 목적일 때 유용한 기능입니다.
```lua
function on_reload(self)
    print(self.age) -- 게임오브젝트의 age값을 출력하기
end
```

## Reactive logic(반응형 로직)
스크립트 컴포넌트가 있는 게임 오브젝트는 몇 가지 로직을 구현합니다. 이 로직은 종종 몇가지 외부 요인에 의존하는데, 예를 들어 적 AI가 특정 반경 내에 있는 플레이어에 반응 한다던지 플레이어 상호작용으로 문이 잠기고 열리는 반응 등이 있을 수 있습니다.

update() 함수는 상태머신(state machine)을 정의하는 복합적인 기능들을 매 프레임 마다 구현할 수 있게 해 주며 때때로 이것은 적절한 접근 방법입니다. 하지만 매번 update() 를 호출하는 것은 성능상 비용이 드는 일이므로 꼭 필요한 경우가 아니라면 반응형 로직을 구현하여 사용하길 권장합니다. 응답을 위해 게임 월드의 모든 데이터들을 매 프레임마다 조사하는 것 보다 응답을 트리거 하는 특정 메세지를 기다리는 방법이 더욱 성능에 도움이 됩니다. 더 나아가서, 이 방법은 종종 로직 설계 문제를 해결하기도 하므로 더 깔끔하고 안정적인 설계 및 구현을 이끌어 내기도 합니다.

구체적인 예제를 봅시다. 스크립트 컴포넌트가 시작 된 후 2초 후에 메세지를 보내고, 특정 응답 메세지를 기다리고, 특정 응답 메세지를 받은 후 5초 후에 또 다른 메세지를 보내야 한다고 가정해 봅시다. 아래는 이를 비반응형 방식으로 구현한 예제입니다.:

```lua
function init(self)
        -- 시간값을 추적하기 위한 카운터 셋팅
        self.counter = 0
        -- 상태값을 추적하기 위해 필요한 값
        self.state = "first"
end

function update(self, dt)
        self.counter = self.counter + dt
        if self.counter >= 2.0 and self.state == "first" then
                -- 2초 후에 메세지 보내기
                msg.post("some_object", "some_message")
        end
        if self.counter >= 5.0 and self.state == "second" then
                -- "response" 메세지를 받은 후 5초 후에 보내기
                msg.post("another_object", "another_message")
                -- state를 nil로 셋팅해서 이 블록이 또 실행되지 않게 함
                self.state = nil
        end
end

function on_message(self, message_id, message, sender)
        if message_id == hash("response") then
                -- “first”상태의 처리들이 완료되었으므로 다음 상태로 넘어가자
                self.state = "second"
                -- 카운터 초기화
                self.counter = 0
        end
end
```

꽤 간단한 케이스임에도 불구하고 로직이 상당히 꼬이게 됩니다. 우리는 코루틴의 도움을 받아 더 나은 코드를 짤 수 있습니다. 대신 애니메이션 속성 기능인 타이밍 메커니즘을 사용하여 반응형 로직을 구현해야만 합니다.

```lua
-- 타이밍을 위한 Dummy 속성값
go.property("dummy", 0)
function init(self)
        -- 2초 후에 send_first() 호출
        go.animate("#", "dummy", go.PLAYBACK_ONCE_FORWARD, 0,
                     go.EASING_LINEAR, 2.0, 0, send_first)
end

function send_first()
        msg.post("some_object", "some_message")
end

function send_second()
        msg.post("another_object", "another_message")
end

function on_message(self, message_id, message, sender)
        if message_id == hash("response") then
                -- 5초 후에 send_second() 호출
                go.animate("#", "dummy", go.PLAYBACK_ONCE_FORWARD, 0,
                            go.EASING_LINEAR, 5.0, 0, send_second)
        end
end
```
이 방식은 깔끔하며 논리적인 흐름을 따라가기 쉽습니다. 또한 로직을 따라가기 어렵고 미묘한 버그를 유발할 수 있는 내부 상태 변수들을 처리하는데에도 좋습니다. 또한 update() 함수를 완전히 제거하여 초당 60회의 스크립트 호출을 줄이는데 도움이 됩니다.

## Lua contexts in Defold
선언한 모든 변수들은 기본적으로 전역(global)변수이므로 Lua 런타임 컨텍스트의 모든 부분에서 사용할 수 있습니다. Defold에는 이 컨텍스트를 제어하는 "game.project"에 shared_state 설정이 있습니다. 이 옵션을 설정하면 스크립트, GUI스크립트, 렌더스크립트 모두는 같은 Lua 컨텍스트에서 실행되고 global변수들은 어디에서든 사용 가능해 집니다. 이 옵션을 설정하지 않으면 게임 엔진은 스크립트들과 GUI스크립트, 렌더스크립트들을 각각의 컨텍스트에서 실행합니다.

![Contexts](images/lua/lua_contexts.png)

Defold allows you to use the same script file in several separate game object components. Any locally declared variables are shared between components that runs the same script file.
Defold는 여러 개의 게임 오브젝트 컴포넌트에서 같은 스크립트 파일을 사용할 수도 있습니다. 로컬로 선언된 변수들은 같은 스크립트 파일을 실행하는 컴포넌트간에 공유됩니다.

```lua
-- 'my_global_value'는 스크립트, gui스크립트,렌더스크립트,모듈(루아 파일)들 모두에서 사용 가능함
my_global_value = "global scope"

-- 이 값은 이 스크립트 파일을 사용하는 모든 컴포넌트 인스턴스들에게 공유됨
local script_value = "script scope"

function init(self, dt)
    -- 이 값은 이 스크립트 컴포넌트 인스턴스에서 사용 가능함
    self.foo = "self scope"

    -- 이 값은 선언 이후에 init()함수 안에서만 사용 가능함
    local local_foo = "local scope"
    print(local_foo)
end

function update(self, dt)
    print(self.foo)
    print(my_global_value)
    print(script_value)
    print(local_foo) -- local_foo는 init()함수 안에서만 존재하므로 nil이 출력될거임
end
```

## Performance considerations(성능 고려사항)
60FPS로 매끄럽게 동작해야만 하는 고성능 게임에서는 자그마한 실수로 유저 경험에 크게 악영향을 끼칠 수도 있습니다. 여기서는 몇가지 간단한 고려사항을 살펴보고, 문제가 없어 보이는 듯한 몇가지 사항도 살펴보도록 합시다.

간단한 것부터 시작해보자면, 불필요한 반복문을 쓰지 않고 간단한 코드를 작성하는 것이 일반적으로 좋은 방법입니다. 가끔은 리스트를 반복해야 하기도 하지만 어느정도 큰 리스트를 반복하는 경우엔 주의할 필요가 있습니다. 만약 아래 예제를 각 프레임이 16밀리초(60FPS)인 게임엔진, 렌더스크립트, 물리 시뮬레이션과 함께 실행한다면 성능을 왕창 잡아먹게 되어 꽤 괜찮은 노트북에서마저 약 1밀리초 가량 더 걸리게 될 것입니다.

```lua
local t = os.clock()
local table = {}
for i=1,2000 do
    table[i] = vmath.vector3(i, i, i)
end
print((os.clock() - t) * 1000)

-- DEBUG:SCRIPT: 1.18
```

os.clock()에서 반환 된 값 (프로그램의 CPU시간(초))을 사용하여 의심스러운 코드를 벤치 마크하시기 바랍니다.

## Memory and garbage collection(메모리와 가비지 컬렉션)
Lua의 가비지 컬렉션은 기본적으로 백그라운드에서 자동적으로 실행되며 Lua런타임이 할당한 메모리를 회수합니다. 많은 가비지를 수집하는 것은 시간을 꽤 소모하는 작업이 될 수 있으므로 오브젝트의 수를 필요한 만큼만 유지하는 것이 좋습니다:

- local 변수는 스스로 해제되며 가비지를 생성하지 않습니다. (예: ``local v = 42``)
- 각각의 새로운 고유한 문자열은 새로운 오브젝트를 생성합니다. ``local s = "some_string"`` 는 새 오브젝트를 생성하고 ``s``에 할당합니다. ``local s`` 는 가비지를 생성하지는 않지만 문자열 오브젝트는 가비지를 생성합니다. 동일한 문자열을 여러번 사용하는 것은 메모리 비용이 추가되지 않습니다.
- ``{ …​ }``로 테이블 생성자가 실행될 때마다 새 테이블이 생성됩니다.
- function 구문을 실행하면 클로저 오브젝트(closure object)가 생성됩니다. (즉 정의된 함수를 호출하는 것이 아니라 ``function() ... end`` 구문을 실행함)
- ``function(v, …​) end``와 같이 인자의 수가 가변인 함수(Vararg functions)는 함수가 호출될 때마다 인자값을 담는 테이블을 생성합니다. (Lua 5.2 이전 버전 혹은 LuaJIT을 사용하지 않을 경우)
- 파일을 다루거나 문자열을 다루는 함수들
- Userdata 오브젝트

새로운 오브젝트를 생성하지 않고 이미 만들어진 오브젝트를 재사용할 수 있는 방법이 많이 있습니다. 아래는 update() 함수의 끝부분에 나타나는 일반적인 실수에 대한 예제입니다:

```lua
-- 속도 초기화 하기
self.velocity = vmath.vector3()
```
종종 vmath.vector3()가 호출될 때 새로운 오브젝트가 생성된다는 것을 깜빡하기 쉽습니다. vector3가 사용하는 메모리의 양을 한 번 알아 봅시다:

```lua
print(collectgarbage("count") * 1024)       -- 88634
local v = vmath.vector3()
print(collectgarbage("count") * 1024)       -- 총 88704. 70바이트가 할당됨
```

collectgarbage()함수 사이에 약 70바이트가 추가되었지만 이는 순수한 vector3 오브젝트보다 더 많이 할당되었습니다. collectgarbage()함수의 결과를 출력할 문자열을 만드는데 가비지의 약 22바이트가 추가되었습니다.

```lua
print(collectgarbage("count") * 1024)       -- 88611
print(collectgarbage("count") * 1024)       -- 88633. 22바이트가 할당됨
```

따라서 vector3는 70-22=48 byte입니다. 많은 양은 아니지만 60FPS의 게임에서 매 프레임마다 생성한다면 갑자기 초당 2.8kb의 가비지가 생기게 됩니다. 매 프레임마다 하나의 vector3를 생성하는 스크립트 컴포넌트를 360개 사용한다면 초당 1MB씩 생성되는 가비지를 만나게 될 수도 있습니다.  이 가비지는 매우 빠르게 누적 증가하게 되어 Lua 런타임이 가비지를 수집하게 될 때, 특히 모바일 플랫폼에서 매우 소중한 시간들을 잡아먹어 버릴 수 있습니다.

vector3가 생성되는 것을 피하는 방법은 동일한 오브젝트를 유지하는 것입니다. 예를 들어, vector3를 초기화 하기 위해 아래의 방법을 사용할 수 있습니다:

```lua
-- 새로운 객체가 생성되는 self.velocity = vmath.vector3() 대신에
-- 이미 존재하는 vector 객체의 값을 0으로 셋팅하자
self.velocity.x = 0
self.velocity.y = 0
self.velocity.z = 0
```

시간이 중요한 일부 프로그램의 경우는 기본적인 가비지 수집 방식이 최적의 방법이 아닐 수도 있습니다. 만약 게임이 버벅인다면 collectgarbage() 함수를 활용해 Lua의 가비지 수집 방식을 조정할 수 있습니다. 예를 들어, 낮은 "step" 값으로 매 프레임 마다 짧은 시간에 가비지 컬렉터를 실행 할 수 있습니다. 게임이나 앱이 얼마나 많은 메모리를 먹고 있는지 알기 위해 현재 가비지의 양을 아래 방법으로 출력할 수 있습니다:

```lua
print(collectgarbage("count") * 1024)
```

## Best practices
일반적인 구현 및 설계의 고려사항은 공유된 동작(Behaviors)을 위한 코드를 구조화 하는데 있습니다. 여기에는 여러가지 접근 방법이 있습니다.

#### Behaviors in a module (모듈에서 동작을 사용하기)
![Module](images/lua/lua_module.png)

모듈에서의 캡슐화 된 동작은 각기 다른 게임 오브젝트의 스크립트 컴포넌트(GUI스크립트 포함) 간에 쉽게 코드를 공유할 수 있게 해 줍니다. 모듈에 함수를 작성하는 것은 엄격하게 기능적인 코드를 작성하는 것이 일반적인 최선의 방법입니다. 저장된 상태 또는 부작용이 필수적인 경우(또는 깔끔한 설계를 이끄는 경우)가 있습니다. 만약 모듈에서 내부 상태값을 저장해야 한다면 컴포넌트들은 Lua컨텍스트를 공유한다는 것을 알아두기 바랍니다. 자세한 것은 모듈에 관한 문서를 참고 바랍니다.

또한, 모듈 코드가 게임 오브젝트의 내부를 직접 수정하는 것이 가능하더라도 ("self"값을 모듈 함수에 전달하는 방법으로) 이 방법은 너무 강력한 결합(coupling)이 되므로 권장하지 않습니다.

#### A helper game object with encapsulated behavior (캡슐화된 동작을 헬퍼 게임오브젝트로 사용하기)
![Helper](images/lua/lua_helper.png)

Lua 모듈에 스크립트 코드를 추가할 수 있는 것 처럼, 스크립트 컴포넌트를 사용하여 게임 오브젝트에도 스크립트 코드를 추가할 수 있습니다. 차이점은 게임 오브젝트에 추가된다는 것과 이럴 경우 메세지 전달을 통해 엄격하게 통신해야 한다는 점이 다릅니다.

#### Grouping game object with helper behavior object inside a collection (동작을 처리하는 헬퍼 게임오브젝트를 컬렉션에서 그룹화하여 사용하기)
![Collection](images/lua/lua_collection.png)

이 설계방법에서는 미리 정의된 이름으로(사용자가 직접 대상 게임 오브젝트의 이름을 일치시켜야함) 혹은 go.property() URL을 통해 다른 대상의 게임 오브젝트를 자동으로 실행하는 동작 게임 오브젝트(behavior game object)를 생성할 수 있습니다. 

이 방식의 이점으로는 동작 게임 오브젝트를 대상 오브젝트(target object)가 포함된 컬렉션에 그냥 떨구기만 하면 된다는 것입니다. 추가 코드가 필요 없습니다.

많은 수의 게임 오브젝트를 관리해야하는 상황에서는 동작 오브젝트가 복제되고 각 오브젝트가 메모리를 소모하므로 이 설계는 바람직 하지 않습니다.