---
brief: Defold가 처음이라면 이 가이드는 Defold의 몇 가지 빌딩 블록과 스크립트 로직을 함께 사용해 Snake 클론을 처음부터 만드는 데 도움이 됩니다.
layout: tutorial
title: Defold에서 Snake 게임 만들기
difficulty: Beginner
---

# Snake

이 튜토리얼에서는 재현해 볼 수 있는 가장 흔한 고전 게임 중 하나를 만드는 과정을 안내합니다. 이 게임에는 여러 변형이 있는데, 여기서는 "먹이"를 먹고, 먹을 때만 길어지는 뱀이 등장합니다. 이 뱀은 장애물이 있는 플레이필드 위를 기어갑니다.

![썸네일](images/snake/thumbnail.png)

### 배우는 내용

이 튜토리얼에서는 다음을 배웁니다:
- Defold에서 게임을 처음부터 만들기
- 입력을 설정하고 처리하기
- 타일 맵을 만들고 런타임에 수정하기
- Lua로 스크립트 작성하기

### 초보자를 위한 참고

이 튜토리얼은 초보자를 위해 설계되었지만, Defold와 게임 개발이 완전히 처음이라면 먼저 몇 가지 입문 매뉴얼, 특히 [Defold의 빌딩 블록](/manuals/building-blocks/)과 [용어집](/manuals/glossary/)을 읽는 것을 권장합니다. 아직 Defold를 다운로드하지 않았다면 [설치 매뉴얼](/manuals/install/)을 확인하세요. 에디터 자체를 빠르게 파악할 수 있도록 [에디터 개요](/manuals/editor/)도 확인하는 것이 좋습니다. 다만 여기에서도 각 단계마다 스크린샷을 제공합니다.

## 프로젝트 만들기

Defold를 시작하고:

1. 왼쪽에서 *Create From* ▸ *Templates*를 선택합니다.
2. *Empty Project*를 선택합니다.
3. *Title* 필드에 프로젝트 이름을 입력합니다.
4. 프로젝트의 *Location*을 선택합니다.
5. *Create New Project*를 클릭합니다.

![시작](images/snake/1.png)

<input type="checkbox"/> 완료!

## 프로젝트 설정

먼저 게임의 해상도를 정의합니다.

1. 에디터가 열리면 왼쪽 *Assets* pane에서 `game.project` 파일을 찾습니다. 더블 클릭해서 엽니다.
2. `game.project` 파일의 *Display* 섹션으로 이동합니다.
3. 게임의 크기(`Width`와 `Height`)를 768⨉768 또는 16의 다른 배수로 설정합니다.

![디스플레이](images/snake/2.png)

이렇게 하는 이유는 게임이 각 세그먼트가 16x16 픽셀인 그리드에 그려지기 때문입니다. 이렇게 하면 게임 화면이 세그먼트 일부를 잘라내지 않습니다. `game.project` 파일에는 프로젝트의 모든 중요한 설정이 들어 있습니다. 자세한 내용은 [프로젝트 설정 매뉴얼](/manuals/project-settings/)에서 읽을 수 있습니다.

<input type="checkbox"/> 완료!

## Assets pane에서 새 폴더 만들기

미니멀한 Snake 클론에는 그래픽이 거의 필요하지 않습니다. 뱀을 위한 16⨉16 초록색 세그먼트 하나, 장애물을 위한 흰색 블록 하나, 먹이를 나타내는 더 작은 빨간색 블록 하나면 됩니다.

먼저 Defold 에디터에서 에셋용 디렉토리를 만듭니다:

1. `main` 폴더를 <kbd>오른쪽 클릭</kbd>합니다.
2. `New Folder`를 선택합니다.
3. 이름을 묻는 팝업이 나타납니다. `assets`를 입력하고 `Create Folder`를 클릭합니다.

![새 폴더](images/snake/3.png)

<input type="checkbox"/> 완료!

## 게임에 그래픽 추가하기

아래 이미지만 있으면 됩니다:

![snake_sprites](images/snake/snake.png)

1. 위 이미지를 <kbd>오른쪽 클릭</kbd>하고 로컬 디스크에 저장합니다. 그런 다음 다운로드한 이미지를 방금 만든 프로젝트 폴더의 새 위치로 드래그-앤-드롭하거나 복사해서 붙여넣습니다.

![새 폴더](images/snake/4.png)

[에셋 임포트에 대한 자세한 내용](/manuals/importing-graphics/)도 읽어 볼 수 있습니다.

<input type="checkbox"/> 완료!

## 타일 소스(Tile Source) 추가하기

Defold는 그리드에 정렬된 *타일*로 구성된 플레이필드를 만드는 데 사용할 수 있는 내장 [타일 맵](/manuals/tilemap/) 컴포넌트를 제공합니다. 타일 맵을 사용하면 개별 타일을 설정하고 읽을 수 있으므로 이 게임에 매우 잘 맞습니다. 타일 맵은 [타일 소스(Tile Source)](/manuals/tilesource/)에서 그래픽을 가져오므로 먼저 하나 만들어야 합니다:

1. `assets` 폴더를 <kbd>오른쪽 클릭</kbd>합니다.
2. "Resources" 섹션에서 `New` ▸ `Tile Source`를 선택합니다.
3. 새 파일 이름을 "snake"로 지정합니다(에디터는 파일을 `snake.tilesource`로 저장합니다).

![새 tilesource](images/snake/5.png)

타일 소스는 이 파일 타입 전용 Tile Source Editor에서 열리며, 동작하려면 사용할 이미지를 지정하라는 요청을 받습니다. 오른쪽에서 `Properties` pane을 찾을 수 있습니다:

4. `Image` 프로퍼티를 방금 임포트한 그래픽 파일로 설정합니다.
![tilesource](images/snake/6.png)

5. `Width`와 `Height` 프로퍼티는 16(기본값)으로 유지해야 합니다. 그러면 32⨉32 픽셀 이미지가 1-4번으로 번호가 매겨진 4개의 타일로 나뉩니다.

![tilesource 프로퍼티](images/snake/7.png)

*Extrude Borders* 프로퍼티가 2픽셀로 설정되어 있다는 점에 주의하세요. 이는 그래픽이 가장자리까지 채워진 타일 주변에 시각적 아티팩트가 생기지 않도록 하기 위한 것입니다.

파일을 변경하면 해당 탭의 파일 이름 옆에 별표 `*`가 나타납니다. 모든 파일을 저장하려면 `File` ▸ `Save All`을 선택하거나 단축키 <kbd>Ctrl</kbd>+<kbd>S</kbd>(Mac에서는 <kbd>⌘Cmd</kbd> + <kbd>S</kbd>)를 사용합니다.

<input type="checkbox"/> 완료!

## 플레이필드 타일 맵 만들기

이제 사용할 타일 소스가 준비되었으므로 플레이필드 타일 맵 컴포넌트를 만들 차례입니다:

1. `main` 폴더를 <kbd>오른쪽 클릭</kbd>하고 "Components" 섹션에서 <kbd>New</kbd> ▸ <kbd>Tile Map</kbd>을 선택합니다. 새 파일 이름을 "grid"로 지정합니다(에디터는 파일을 "grid.tilemap"으로 저장합니다).
![타일 맵 추가](images/snake/8.png)

2. 파일이 Tile Map Editor에서 열리고 **Tile Source**가 필요하다는 표시가 나타납니다. 따라서 *Tile Source* 프로퍼티를 앞서 만든 "snake.tilesource"로 설정합니다.
![타일 소스 설정](images/snake/9.png)

<input type="checkbox"/> 완료!

## 타일 맵에 타일 그리기

Defold는 실제로 사용되는 타일 맵 영역만 저장하므로 화면 경계를 채울 만큼 충분한 타일을 추가해야 합니다.

1. 오른쪽 `Outline` pane에서 `layer1` 레이어를 선택합니다.
2. 메뉴 옵션 `Edit` ▸ `Select Tile...` 또는 단축키 <kbd>Space</kbd>를 선택해 타일 팔레트를 표시한 다음, 칠할 때 사용할 타일을 클릭합니다.
![타일맵](images/snake/10.png)

3. 화면 가장자리에 테두리를 칠하고 장애물도 몇 개 칠합니다.
![최종 타일맵](images/snake/11.png)

게임 화면을 채우려면 48x48 타일 크기의 타일 맵이 필요합니다(디스플레이가 768이고 타일이 16px이므로 768/16 = 48입니다).

완료되면 타일 맵을 저장합니다.

<input type="checkbox"/> 완료!

## 게임에 타일 맵 추가하기

이제 게임에 타일 맵을 추가해야 합니다. Defold 빌딩 블록에 익숙하다면 컴포넌트는 게임 오브젝트의 일부이며, 게임 오브젝트는 컬렉션에서 정의할 수 있다는 것을 알고 있을 것입니다.

1. `Assets` pane에서 `main.collection`을 더블 클릭해 엽니다. Empty Project 템플릿에서는 기본적으로 이 컬렉션이 엔진 시작 시 로드되는 부트스트랩 컬렉션입니다.

2. `Outline`의 루트를 <kbd>오른쪽 클릭</kbd>하고 `Add Game Object`를 선택합니다. 그러면 게임이 시작될 때 로드되는 컬렉션 안에 새 게임 오브젝트가 생성됩니다.
![게임 오브젝트 추가](images/snake/12.png)

3. 새 게임 오브젝트를 <kbd>오른쪽 클릭</kbd>하고 `Add Component File`을 선택합니다. 방금 만든 "grid.tilemap" 파일을 선택합니다.
![컴포넌트 추가](images/snake/13.png)

이제 게임 컬렉션 안에 타일 맵이 있습니다. 에디터에서 게임을 실행하면 타일 맵이 보여야 합니다.

1. `Project` ▸ `Build`를 선택하거나 단축키 <kbd>Ctrl</kbd> + <kbd>B</kbd>(Mac에서는 <kbd>⌘Cmd</kbd> + <kbd>B</kbd>)를 사용합니다.

![게임 실행](images/snake/14.png)

<input type="checkbox"/> 완료!

## 게임에 스크립트 추가하기

1. `Assets` browser에서 `main` 폴더를 <kbd>오른쪽 클릭</kbd>하고 Scripts 섹션에서 `New` ▸ `Script`를 선택합니다. 새 스크립트 파일 이름을 "snake"로 지정합니다(파일은 "snake.script"로 저장됩니다). 이 파일에는 게임의 모든 로직이 들어갑니다.
![스크립트 추가](images/snake/15.png)

2. *main.collection*으로 돌아가서 타일 맵을 가진 게임 오브젝트를 <kbd>오른쪽 클릭</kbd>합니다. <kbd>Add&nbsp;Component&nbsp;File</kbd>을 선택하고 "snake.script" 파일을 선택합니다.

![main collection](images/snake/16.png)

이제 타일 맵 컴포넌트와 스크립트가 모두 제자리에 있습니다.

<input type="checkbox"/> 완료!

## 게임 스크립트

작성할 스크립트가 게임 전체를 구동합니다. 기능을 하나씩 추가해 나가겠습니다.

### 간단한 이동 알고리즘

동작 방식의 아이디어는 다음과 같습니다:

1. 스크립트는 현재 뱀이 차지하고 있는 타일 위치 목록을 유지합니다.
2. 플레이어가 방향키를 누르면 뱀이 이동해야 할 방향을 저장합니다.
3. 일정한 간격마다 현재 이동 방향으로 뱀을 한 칸 이동시킵니다.

### 초기화

*snake.script*를 열고 `init()` 함수를 찾습니다. 이 함수는 게임 시작 시 스크립트가 초기화될 때 엔진이 호출합니다. 코드를 다음과 같이 변경합니다:

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

이 코드에서는:

1. 뱀의 세그먼트를 `self.segments`라는 Lua 테이블에 저장합니다. 이 테이블은 각 세그먼트의 X와 Y 위치를 담은 테이블 목록입니다.
2. 현재 방향을 X와 Y 방향을 담은 `self.dir`이라는 테이블에 저장합니다.
3. 현재 이동 속도를 `self.speed`에 저장합니다. 단위는 초당 타일 수입니다.
4. 이동 속도를 추적하는 데 사용할 타이머 값을 `self.time`에 저장합니다.

위 스크립트 코드는 Lua 언어로 작성되었습니다. 코드에서 알아둘 몇 가지가 있지만, 아래 내용을 아직 이해하지 못해도 걱정하지 마세요. 따라 해 보고, 실험하고, 시간을 두면 결국 익숙해질 것입니다. 지금은 `init()`에서 앞으로 사용할 변수를 초기화했다는 것만 기억하면 됩니다.

- Defold는 스크립트 컴포넌트의 수명 동안 호출되는 내장 콜백 *함수* 집합을 예약해 둡니다. 이들은 메서드가 아니라 일반 함수입니다.
- 런타임은 현재 스크립트 컴포넌트 인스턴스에 대한 참조를 `self` 파라미터로 전달합니다. `self` 참조는 인스턴스 데이터를 저장하는 데 사용됩니다.
- `self` 참조는 데이터를 저장할 수 있는 Lua 테이블처럼 사용할 수 있습니다. 다른 테이블에서 하듯 점 표기법을 사용하면 됩니다: `self.data = "value"`. 이 참조는 스크립트의 수명 전체, 이 경우 게임 시작부터 종료할 때까지 유효합니다.
- Lua 테이블 리터럴은 중괄호 `{}`로 감싸서 작성합니다.
- 테이블 항목은 키/값 쌍(`{x = 10, y = 20}`), 중첩된 Lua 테이블(`{ {a = 1}, {b = 2} }`) 또는 다른 데이터 타입일 수 있습니다.

<input type="checkbox"/> 완료!

### Update

`init()` 함수는 스크립트 컴포넌트가 실행 중인 게임에 인스턴스화될 때 정확히 한 번 호출됩니다. 반면 `update()` 함수는 **매 프레임마다** 한 번 호출됩니다. 따라서 이 함수는 실시간 게임 로직에 이상적입니다.

업데이트의 아이디어는 다음과 같습니다. 일정한 간격마다 다음을 수행합니다:

1. 뱀의 머리가 어디에 있는지 찾은 다음, 현재 이동 방향만큼 오프셋된 옆 위치에 새 머리를 만듭니다. 예를 들어 뱀이 X=1, Y=0 방향으로 이동 중이고 현재 머리가 X=0, Y=0 위치에 있다면, 새 머리는 X=1, Y=0에 있어야 합니다.
2. 새 머리 위치를 뱀을 구성하는 세그먼트 목록에 저장합니다.
3. 세그먼트 테이블에서 꼬리 위치를 가져옵니다.
4. 이 위치의 꼬리 타일을 지웁니다.
5. 테이블의 위치에 모든 뱀 세그먼트(타일)를 그립니다.

![알고리즘](images/snake/17.png)

:::sidenote
뱀의 머리는 테이블의 끝에 있고 꼬리는 시작 부분에 있다는 점을 기억하세요.
:::

1. *snake.script*에서 `update()` 함수를 찾아 코드를 다음과 같이 변경합니다:

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

이 코드에서는:

1. 마지막으로 `update()`가 호출된 이후의 시간 차이(초), 즉 "delta time" 또는 `dt`만큼 타이머를 진행합니다.
2. 타이머가 충분히 진행되었다면:
3. 현재 머리 위치를 가져옵니다. `#`는 배열처럼 사용되는 테이블의 길이를 가져오는 연산자입니다. 이 경우 모든 세그먼트가 지정된 키가 없는 테이블 값이므로 배열처럼 사용됩니다.
4. 현재 머리 위치와 이동 방향(`self.dir`)을 바탕으로 새 머리 세그먼트를 만듭니다.
5. 새 머리를 세그먼트 테이블의 끝에 추가합니다.
6. 세그먼트 테이블의 시작 부분에서 꼬리를 제거합니다.
7. 제거한 꼬리 위치의 타일을 지웁니다. 타일 맵 `#grid`에는 `layer1`이라는 레이어가 하나만 있습니다.
8. 세그먼트 테이블의 요소를 반복합니다. 각 반복에서 `i`는 테이블 안의 위치(1부터 시작), `s`는 현재 세그먼트로 설정됩니다.
9. 세그먼트 위치의 타일 값을 2로 설정합니다(초록색 뱀 색상의 타일입니다).
10. 완료되면 타이머를 0으로 재설정합니다.

지금 게임을 실행하면 4개 세그먼트 길이의 뱀이 플레이필드를 왼쪽에서 오른쪽으로 기어가는 것을 볼 수 있습니다.

![게임 실행](images/snake/snake_run_1.png)

<input type="checkbox"/> 완료!

## 플레이어 입력

플레이어 입력에 반응하는 코드를 추가하기 전에 입력 연결을 설정해야 합니다.

### 입력 바인딩

1. `input` 폴더에서 `game.input_binding` 파일을 찾아 <kbd>더블 클릭</kbd>해 엽니다.
2. 위, 아래, 왼쪽, 오른쪽 이동을 위한 *Key Trigger* 바인딩 집합을 추가합니다. *Input* 열에서는 키보드 키를 선택하고, *Action* 열에는 액션 이름을 입력합니다.

![입력](images/snake/18.png)

입력 바인딩 파일은 실제 사용자 입력(키, 마우스 이동 등)을 입력을 요청한 스크립트에 전달되는 동작 *이름*으로 매핑합니다.

<input type="checkbox"/> 완료!

### 입력 포커스 획득하기

바인딩이 준비되었으면 *snake.script*를 열고 `init()` 함수의 시작 부분에 다음 줄을 추가합니다:

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

추가한 줄은:
1. 현재 게임 오브젝트("."은 현재 게임 오브젝트의 약칭입니다)에 메세지를 보내 엔진에서 입력을 받기 시작하라고 알립니다.

그런 다음 `on_input` 함수를 찾아 다음 코드를 입력합니다:

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

이 `if...elseif...` 분기들은 다음을 수행합니다:
1. 입력 바인딩에서 설정한 대로 "up" 입력 동작이 수신되고, `action` 테이블의 `pressed` 필드가 `true`(플레이어가 키를 누름)로 설정되어 있다면:
2. 이동 방향을 설정합니다.

게임을 다시 실행하고 뱀을 조종할 수 있는지 확인합니다.

<input type="checkbox"/> 완료!

### 입력 처리 개선하기

이제 두 키를 동시에 누르면 각 키 입력마다 하나씩, `on_input()`이 두 번 호출된다는 점에 주의하세요. 위 코드처럼 작성하면 마지막에 발생한 호출만 뱀의 방향에 영향을 줍니다. 이어지는 `on_input()` 호출이 `self.dir`의 값을 덮어쓰기 때문입니다.

또한 뱀이 왼쪽으로 이동 중일 때 <kbd>right</kbd> 키를 누르면 뱀이 자기 자신을 향해 방향을 틉니다. 이 문제에 대해 *겉보기에는* 명백한 해결책은 `on_input()`의 `if` 절에 추가 조건을 넣는 것입니다:

```lua
if action_id == hash("up") and self.dir.y ~= -1 and action.pressed then
    ...
elseif action_id == hash("down") and self.dir.y ~= 1 and action.pressed then
    ...
```

하지만 뱀이 왼쪽으로 이동 중이고 플레이어가 다음 이동 단계가 일어나기 전에 <kbd>up</kbd>을 먼저, 곧바로 <kbd>right</kbd>를 *빠르게* 누르면 <kbd>right</kbd> 입력만 효과를 내서 뱀이 자기 자신으로 이동하게 됩니다. 위와 같이 `if` 절에 조건을 추가하면 입력이 무시됩니다. *좋지 않습니다!*

이 문제의 올바른 해결책은 입력을 큐에 저장하고, 뱀이 이동할 때 그 큐에서 항목을 꺼내는 것입니다:

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

이번에는:
1. 빈 테이블로 초기화되는 `self.dirqueue` 변수를 추가했습니다.

`update()` 함수에 다음을 추가합니다:

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

1. 방향 큐에서 첫 번째 항목을 꺼냅니다.
2. 항목이 있으면(`newdir`이 nil이 아니면) `newdir`이 `self.dir`의 반대 방향을 가리키는지 확인합니다.
3. 반대 방향을 가리키지 않을 때만 새 방향을 설정합니다.

그리고 `on_input`을 수정해 현재 입력을 직접 설정하는 대신 큐에 저장합니다:

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

1. `self.dir`를 직접 설정하는 대신 입력 방향을 방향 큐에 추가합니다.

게임을 시작하고 예상대로 플레이되는지 확인합니다.

<input type="checkbox"/> 완료!

## 먹이와 장애물 충돌

뱀이 길고 빠르게 자랄 수 있도록 맵에 먹이가 필요합니다. 추가해 보겠습니다!

### 먹이 스폰하기

`init()` 함수 위에 새 함수를 추가합니다:

```lua
local function put_food(self) -- <1>
    self.food = {x = math.random(2, 47), y = math.random(2, 47)} -- <2>
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3) -- <3>
end
```

이 함수에서는:
1. 맵에 먹이 하나를 놓는 `put_food()`라는 새 함수를 선언합니다.
2. 임의의 X와 Y 위치를 `self.food`라는 변수에 저장합니다.
3. X와 Y 위치의 타일을 먹이 그래픽인 값 3으로 설정합니다.

그런 다음 `init()` 함수 끝에서 호출합니다:
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

1. `math.random()`으로 난수 값을 뽑기 전에 난수 시드를 설정합니다. 그렇지 않으면 같은 난수 값 시리즈가 생성됩니다. 이 시드는 한 번만 설정해야 합니다.
2. 게임 시작 시 `put_food()` 함수를 호출해 플레이어가 맵의 먹이 아이템 하나와 함께 시작하도록 합니다.

<input type="checkbox"/> 완료!

### 먹이 먹기

이제 뱀이 무언가와 충돌했는지 감지하는 일은 뱀이 향하는 위치의 타일 맵에 무엇이 있는지 보고 반응하는 문제일 뿐입니다.

뱀이 살아 있는지 추적하는 변수를 추가합니다:

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

1. 뱀이 살아 있는지 여부를 알려 주는 플래그입니다.

그런 다음 벽/장애물 및 먹이와의 충돌을 검사하는 로직을 추가합니다:

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

1. 뱀이 살아 있을 때만 전진시킵니다.
2. 타일 맵에 그리기 전에 새 뱀 머리가 위치할 곳에 무엇이 있는지 읽습니다.
3. 타일이 장애물이거나 뱀의 다른 부분이면 게임 오버입니다!
4. 타일이 먹이면 속도를 올린 다음 새 먹이 아이템을 놓습니다.
5. 꼬리 제거는 충돌이 없을 때만 일어난다는 점에 주의하세요. 즉, 플레이어가 먹이를 먹으면 그 이동에서 꼬리가 제거되지 않으므로 뱀이 한 세그먼트만큼 길어집니다.

이제 게임을 실행해 잘 플레이되는지 확인해 보세요!

이것으로 튜토리얼은 끝났지만, 아래 연습 문제를 진행하면서 게임을 계속 실험해 보세요!

<input type="checkbox"/> 완료!

## 전체 스크립트

참고용 전체 스크립트 코드는 다음과 같습니다:

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

## 연습 문제

다음 개선 사항을 직접 구현해 보는 것도 좋은 연습입니다:

1. 게임이 끝났을 때 다시 시작할 수 있도록 키 입력 처리를 추가합니다.
2. 점수와 점수 카운터를 추가합니다. 간단히 라벨 컴포넌트만 사용해도 되고(더 쉽습니다), 전체 GUI를 사용해도 됩니다.
3. `put_food()` 함수는 뱀의 위치나 장애물을 고려하지 않습니다. 빈 위치에만 스폰되도록 수정합니다.
4. 게임이 끝나면 "Game Over" 메세지를 표시하고 플레이어가 다시 시도할 수 있게 합니다.
5. 추가 과제: 플레이어가 조종하는 두 번째 뱀을 추가합니다.
