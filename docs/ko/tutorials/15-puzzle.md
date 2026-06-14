---
title: Defold에서 15 퍼즐 게임 만들기
brief: Defold가 처음이라면 이 가이드에서 Defold의 몇 가지 빌딩 블록을 실습하고 스크립트 로직을 실행하는 방법을 배울 수 있습니다.
---

# 클래식 15 퍼즐

이 유명한 퍼즐은 1870년대 미국에서 인기를 얻었습니다. 퍼즐의 목표는 타일을 가로와 세로로 밀어 보드 위의 타일을 정렬하는 것입니다. 퍼즐은 타일이 섞인 상태에서 시작합니다.

가장 일반적인 버전의 퍼즐은 타일에 1--15 숫자를 표시합니다. 하지만 타일을 이미지의 일부로 만들면 퍼즐을 조금 더 어렵게 만들 수 있습니다. 시작하기 전에 퍼즐을 풀어 보세요. 빈 칸과 인접한 타일을 클릭하면 해당 타일이 빈 위치로 미끄러집니다.

## 프로젝트 만들기

1. Defold를 시작합니다.
2. 왼쪽에서 *New Project*를 선택합니다.
3. *From Template* 탭을 선택합니다.
4. *Empty Project*를 선택합니다.
5. 로컬 드라이브에서 프로젝트 위치를 선택합니다.
6. *Create New Project*를 클릭합니다.

*game.project* 설정 파일을 열고 게임의 크기를 512⨉512로 설정합니다. 이 크기는 사용할 이미지와 일치합니다.

![디스플레이 설정](images/15-puzzle/display_settings.png)

다음 단계는 퍼즐에 알맞은 이미지를 다운로드하는 것입니다. 정사각형 이미지라면 무엇이든 사용할 수 있지만, 반드시 512⨉512 픽셀로 크기를 조정하세요. 이미지를 직접 찾아보기 싫다면 다음 이미지를 사용해도 됩니다.

![모나리자](images/15-puzzle/monalisa.png)

이미지를 다운로드한 다음 프로젝트의 *main* 폴더로 드래그합니다.

## 그리드 표현하기

Defold에는 퍼즐 보드를 시각화하기에 완벽한 내장 *Tilemap* 컴포넌트가 있습니다. Tilemap을 사용하면 개별 타일을 설정하고 읽을 수 있으며, 이 프로젝트에는 그 정도면 충분합니다.

하지만 tilemap을 만들기 전에, tilemap이 타일 이미지를 가져올 *Tilesource*가 필요합니다.

*main* 폴더를 <kbd>오른쪽 클릭</kbd>하고 <kbd>New ▸ Tile Source</kbd>를 선택합니다. 새 파일 이름을 `monalisa.tilesource`로 지정합니다.

타일의 *Width*와 *Height* 프로퍼티를 128로 설정합니다. 이렇게 하면 512⨉512 픽셀 이미지가 16개의 타일로 나뉩니다. tilemap에 배치하면 타일에는 1--16 번호가 붙습니다.

![타일 소스](images/15-puzzle/tilesource.png)

다음으로 *main* 폴더를 <kbd>오른쪽 클릭</kbd>하고 <kbd>New ▸ Tile Map</kbd>을 선택합니다. 새 파일 이름을 "grid.tilemap"으로 지정합니다.

Defold에서는 그리드를 초기화해야 합니다. 이를 위해 "layer1" 레이어를 선택하고 원점의 오른쪽 위에 4⨉4 타일 그리드를 그립니다. 타일을 어떤 값으로 설정하든 크게 중요하지 않습니다. 곧 이 타일의 컨텐츠를 자동으로 설정하는 코드를 작성할 것입니다.

![타일 맵](images/15-puzzle/tilemap.png)

## 조각 맞추기

*main.collection*을 엽니다. *Outline*의 루트 노드를 <kbd>오른쪽 클릭</kbd>하고 <kbd>Add Game Object</kbd>를 선택합니다. 새 게임 오브젝트의 *Id* 프로퍼티를 "game"으로 설정합니다.

게임 오브젝트를 <kbd>오른쪽 클릭</kbd>하고 <kbd>Add Component File</kbd>을 선택합니다. *grid.tilemap* 파일을 선택합니다. *Id* 프로퍼티를 "tilemap"으로 설정합니다.

게임 오브젝트를 <kbd>오른쪽 클릭</kbd>하고 <kbd>Add Component ▸ Label</kbd>을 선택합니다. 라벨의 *Id* 프로퍼티를 "done"으로, *Text* 프로퍼티를 "Well done"으로 설정합니다. 라벨을 tilemap의 중앙으로 이동합니다.

라벨이 그리드 위에 그려지도록 라벨의 Z position을 1로 설정합니다.

![메인 컬렉션](images/15-puzzle/main_collection.png)

다음으로 퍼즐 로직을 위한 Lua 스크립트 파일을 만듭니다. *main* 폴더를 <kbd>오른쪽 클릭</kbd>하고 <kbd>New ▸ Script</kbd>를 선택합니다. 새 파일 이름을 "game.script"로 지정합니다.

그런 다음 *main.collection*에서 "game"이라는 게임 오브젝트를 <kbd>오른쪽 클릭</kbd>하고 <kbd>Add Component File</kbd>을 선택합니다. *game.script* 파일을 선택합니다.

게임을 실행합니다. 직접 그린 그리드와 그 위에 "Well done" 메세지가 있는 라벨이 보여야 합니다.

## 퍼즐 로직

이제 모든 조각이 제자리에 있으므로, 튜토리얼의 나머지 부분에서는 퍼즐 로직을 조립합니다.

스크립트는 tilemap과 별도로 보드 타일에 대한 자체 표현을 가지고 있습니다. 이렇게 하면 다루기 더 쉬워질 수 있기 때문입니다. 타일을 2차원 배열에 저장하는 대신, Lua 테이블 안의 1차원 리스트로 저장합니다. 이 리스트는 그리드의 왼쪽 위부터 오른쪽 아래까지 순서대로 타일 번호를 담습니다.

```lua
-- 완성된 보드는 다음과 같습니다.
self.board = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0}
```

이런 타일 리스트를 받아 tilemap에 그리는 코드는 꽤 간단하지만, 리스트 안의 위치를 x와 y 위치로 변환해야 합니다.

```lua
-- 타일의 테이블 리스트를 4x4 tilemap에 그립니다.
local function draw(t)
    for i=1, #t do
        local y = 5 - math.ceil(i/4) -- <1>
        local x = i - (math.ceil(i/4) - 1) * 4
        tilemap.set_tile("#tilemap","layer1",x,y,t[i])
    end
end
```
1. tilemap에서는 x 값이 1이고 y 값이 1인 타일이 왼쪽 아래에 있습니다. 따라서 y 위치를 뒤집어야 합니다.

테스트용 `init()` 함수를 만들어 함수가 의도대로 작동하는지 확인할 수 있습니다.

```lua
function init(self)
    -- 테스트용 뒤집힌 보드
    self.board = {15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0}
    draw(self.board)
end
```

타일이 Lua 테이블 리스트에 있으면 순서를 섞는 일은 매우 쉽습니다. 코드는 리스트의 각 요소를 순회하며 각 타일을 무작위로 선택한 다른 타일과 교환하기만 합니다.

```lua
-- 테이블 리스트의 두 항목을 교환합니다.
local function swap(t, i, j)
    local tmp = t[i]
    t[i] = t[j]
    t[j] = tmp
    return t
end

-- 테이블 리스트 요소의 순서를 무작위로 섞습니다.
local function scramble(t)
    local n = #t
    for i = 1, n - 1 do
        t = swap(t, i, math.random(i, n))
    end
    return t
end
```

계속하기 전에 15 퍼즐에서 꼭 고려해야 할 점이 있습니다. 위와 같이 타일 순서를 무작위로 섞으면 퍼즐이 *풀 수 없는* 상태가 될 확률이 50%입니다.

풀 수 없는 퍼즐을 플레이어에게 보여주고 싶지는 않을 것이므로, 이것은 좋지 않습니다.

다행히 어떤 배치가 풀 수 있는지 아닌지 알아낼 수 있습니다. 방법은 다음과 같습니다.

## 풀 수 있는지 판단하기

4⨉4 퍼즐의 위치가 풀 수 있는지 알아내려면 두 가지 정보가 필요합니다.

1. 배치 안의 "역전(inversions)" 수입니다. 역전(inversion)은 어떤 타일 뒤에 그보다 낮은 숫자의 타일이 오는 경우입니다. 예를 들어 `{1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 11, 10, 13, 14, 15, 0}` 리스트에는 역전이 3개 있습니다.

    - 숫자 12 뒤에는 11과 10이 오므로 역전 2개가 생깁니다.
    - 숫자 11 뒤에는 10이 오므로 역전이 1개 더 생깁니다.

    (완성된 퍼즐 상태의 역전 수는 0입니다)

2. 빈 칸이 있는 행입니다(리스트에서는 `0`으로 표시).

이 두 숫자는 다음 함수로 계산할 수 있습니다.

```lua
-- 타일 리스트 안의 역전 수를 셉니다.
local function inversions(t)
    local inv = 0
    for i=1, #t do
        for j=i+1, #t do
            if t[i] > t[j] and t[j] ~= 0 then -- <1>
                inv = inv + 1
            end
        end
    end
    return inv
end
```
1. 빈 칸은 세지 않는다는 점에 주의하세요.

```lua
-- 주어진 타일의 x와 y 위치를 찾습니다.
local function find(t, tile)
    for i=1, #t do
        if t[i] == tile then
            local y = 5 - math.ceil(i/4) -- <1>
            local x = i - (math.ceil(i/4) - 1) * 4
            return x,y
        end
    end
end
```
1. 아래쪽을 기준으로 한 Y 위치입니다.

이제 이 두 숫자를 알면 퍼즐 상태를 풀 수 있는지 아닌지 판단할 수 있습니다. 4⨉4 보드 상태는 다음 조건에서 *풀 수 있습니다*.

- 빈 칸이 *홀수* 행(아래에서부터 세어 1 또는 3)에 있고 역전 수가 *짝수*인 경우.
- 빈 칸이 *짝수* 행(아래에서부터 세어 2 또는 4)에 있고 역전 수가 *홀수*인 경우.

## 어떻게 작동하나요?

각 합법적인 이동은 조각을 빈 칸과 가로 또는 세로로 위치를 바꿔 이동합니다.

조각을 가로로 이동해도 역전 수는 바뀌지 않으며, 빈 칸이 있는 행 번호도 바뀌지 않습니다.

하지만 조각을 세로로 이동하면 역전 수의 홀짝성(parity)이 바뀝니다(홀수에서 짝수로, 또는 짝수에서 홀수로). 또한 빈 칸 행의 홀짝성도 바뀝니다.

예를 들면 다음과 같습니다.

![조각 밀기](images/15-puzzle/slide.png)

이 이동은 타일 순서를 다음에서

`{ ... 0, 11, 2, 13, 6 ... }`

다음으로 바꿉니다.

`{ ... 6, 11, 2, 13, 0 ... }`

새 상태는 다음과 같이 역전 3개를 추가합니다.

- 숫자 6은 역전 1개를 추가합니다(숫자 2가 이제 6 뒤에 있습니다).
- 숫자 11은 역전 1개를 잃습니다(숫자 6이 이제 11 앞에 있습니다).
- 숫자 13은 역전 1개를 잃습니다(숫자 6이 이제 13 앞에 있습니다).

세로로 밀었을 때 역전 수가 바뀔 수 있는 경우는 ±1 또는 ±3입니다.

세로로 밀었을 때 빈 칸의 행이 바뀔 수 있는 경우는 ±1입니다.

퍼즐의 최종 상태에서 빈 칸은 오른쪽 아래 모서리(*홀수* 행 1)에 있고 역전 수는 *짝수* 값인 0입니다. 각 합법적인 이동은 이 두 값을 그대로 두거나(가로 이동), 둘의 홀짝성을 바꿉니다(세로 이동). 어떤 합법적인 이동도 역전 수와 빈 칸 행이 *홀수*, *홀수* 또는 *짝수*, *짝수*가 되게 만들 수 없습니다.

따라서 두 숫자가 모두 홀수이거나 모두 짝수인 퍼즐 상태는 풀 수 없습니다.

풀 수 있는지 확인하는 코드는 다음과 같습니다.

```lua
-- 주어진 4x4 타일 테이블 리스트를 풀 수 있나요?
local function solvable(t)
    local x,y = find(t, 0)
    if y % 2 == 1 and inversions(t) % 2 == 0 then
        return true
    end
    if y % 2 == 0 and inversions(t) % 2 == 1 then
        return true
    end
    return false
end
```

## 사용자 입력

이제 남은 일은 퍼즐을 상호작용 가능하게 만드는 것뿐입니다.

위에서 만든 함수를 사용해 런타임 설정을 모두 수행하는 `init()` 함수를 만듭니다.

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>
    math.randomseed(socket.gettime()) -- <2>
    self.board = scramble({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0}) -- <3>
    while not solvable(self.board) do -- <4>
        self.board = scramble(self.board)
    end
    draw(self.board) -- <5>
    self.done = false -- <6>
    msg.post("#done", "disable") -- <7>
end
```
1. 이 게임 오브젝트가 입력을 받아야 한다고 엔진에 알립니다.
2. 난수 생성기의 seed를 설정합니다.
3. 보드의 초기 무작위 상태를 만듭니다.
4. 상태를 풀 수 없다면 다시 섞습니다.
5. 보드를 그립니다.
6. 완료 플래그를 설정해 승리 상태를 추적합니다.
7. 완료 메세지 라벨을 비활성화합니다.

*/input/game.input_bindings*를 열고 새 *Mouse Trigger*를 추가합니다. action의 이름을 "press"로 설정합니다.

![입력](images/15-puzzle/input.png)

스크립트로 돌아가 `on_input()` 함수를 만듭니다.

```lua
-- 사용자 입력을 처리합니다.
function on_input(self, action_id, action)
    if action_id == hash("press") and action.pressed and not self.done then -- <1>
        local x = math.ceil(action.x / 128) -- <2>
        local y = math.ceil(action.y / 128)
        local ex, ey = find(self.board, 0) -- <3>
        if math.abs(x - ex) + math.abs(y - ey) == 1 then -- <4>
            self.board = swap(self.board, (4-ey)*4+ex, (4-y)*4+x) -- <5>
            draw(self.board) -- <6>
        end
        ex, ey = find(self.board, 0)
        if inversions(self.board) == 0 and ex == 4 then -- <7>
            self.done = true
            msg.post("#done", "enable")
        end
    end
end
```
1. 마우스 버튼 누름이 있고 게임이 아직 진행 중이면 다음을 수행합니다.
2. 사용자가 클릭한 x와 y 칸을 계산합니다.
3. 현재 빈 칸(0)의 위치를 찾습니다.
4. 클릭한 칸이 빈 칸의 바로 위, 아래, 왼쪽 또는 오른쪽에 있으면 다음을 수행합니다.
5. 클릭한 칸과 빈 칸의 타일을 교환합니다.
6. 업데이트된 보드를 다시 그립니다.
7. 보드의 역전 수가 0, 즉 모든 것이 올바른 순서이고 빈 칸이 가장 오른쪽 열에 있으면(역전 수가 0이려면 반드시 마지막 행에 있어야 함) 퍼즐이 풀린 것이므로 다음을 수행합니다.
8. 완료 플래그를 설정합니다.
9. 완료 메세지를 활성화/표시합니다.

이것으로 끝입니다! 퍼즐 게임이 완성되었습니다!

## 전체 스크립트

참고용 전체 스크립트 코드는 다음과 같습니다.

```lua
local function inversions(t)
    local inv = 0
    for i=1, #t do
        for j=i+1, #t do
            if t[i] > t[j] and t[j] ~= 0 then
                inv = inv + 1
            end
        end
    end
    return inv
end

local function find(t, tile)
    for i=1, #t do
        if t[i] == tile then
            local y = 5 - math.ceil(i/4)
            local x = i - (math.ceil(i/4) - 1) * 4
            return x,y
        end
    end
end

local function solvable(t)
    local x,y = find(t, 0)
    if y % 2 == 1 and inversions(t) % 2 == 0 then
        return true
    end
    if y % 2 == 0 and inversions(t) % 2 == 1 then
        return true
    end
    return false
end

local function scramble(t)
    for i=1, #t do
        local tmp = t[i]
        local r = math.random(#t)
        t[i] = t[r]
        t[r] = tmp
    end
    return t
end

local function swap(t, i, j)
    local tmp = t[i]
    t[i] = t[j]
    t[j] = tmp
    return t
end

local function draw(t)
    for i=1, #t do
        local y = 5 - math.ceil(i/4)
        local x = i - (math.ceil(i/4) - 1) * 4
        tilemap.set_tile("#tilemap","layer1",x,y,t[i])
    end
end

function init(self)
    msg.post(".", "acquire_input_focus")
    math.randomseed(socket.gettime())
    self.board = scramble({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0})
    while not solvable(self.board) do
        self.board = scramble(self.board)
    end
    draw(self.board)
    self.done = false
    msg.post("#done", "disable")
end

function on_input(self, action_id, action)
    if action_id == hash("press") and action.pressed and not self.done then
        local x = math.ceil(action.x / 128)
        local y = math.ceil(action.y / 128)
        local ex, ey = find(self.board, 0)
        if math.abs(x - ex) + math.abs(y - ey) == 1 then
            self.board = swap(self.board, (4-ey)*4+ex, (4-y)*4+x)
            draw(self.board)
        end
        ex, ey = find(self.board, 0)
        if inversions(self.board) == 0 and ex == 4 then
            self.done = true
            msg.post("#done", "enable")
        end
    end
end

function on_reload(self)
    self.done = false
    msg.post("#done", "disable")
end
```

## 추가 연습

1. 5⨉5 퍼즐을 만들고, 그다음 6⨉5 퍼즐을 만들어 보세요. 풀 수 있는지 확인하는 검사가 일반적으로 작동하는지 확인하세요.
2. 슬라이딩 애니메이션을 추가해 보세요. 타일은 tilemap과 별도로 이동할 수 없으므로 이를 해결할 방법을 생각해 내야 합니다. 미끄러지는 조각만 포함하는 별도의 tilemap을 사용할 수도 있을까요?
