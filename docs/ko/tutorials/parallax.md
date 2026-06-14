---
title: 패럴랙스 코드 샘플
brief: 이 샘플에서는 패럴랙스 효과를 사용해 게임 월드의 깊이감을 시뮬레이션하는 방법을 배웁니다.
---
# 패럴랙스 - 샘플 프로젝트

<iframe width="560" height="315" src="https://www.youtube.com/embed/UdNA7kanRQE" frameborder="0" allowfullscreen></iframe>


이 샘플 프로젝트는 [에디터에서 열거나](/manuals/project-setup/) [GitHub에서 다운로드](https://github.com/defold/sample-parallax)할 수 있으며, 게임 월드의 깊이감을 시뮬레이션하기 위해 패럴랙스 효과를 사용하는 방법을 보여줍니다.
두 개의 구름 레이어가 있으며, 그중 한 레이어는 다른 레이어보다 더 뒤쪽에 있는 것처럼 보입니다. 분위기를 더하기 위한 애니메이션 비행접시도 있습니다.

구름 레이어는 각각 *Tile Map*과 *Script*를 포함하는 별도의 두 게임 오브젝트로 구성되어 있습니다.
패럴랙스 효과를 만들기 위해 레이어를 서로 다른 속도로 이동합니다. 이 동작은 아래 *background1.script*와 *background2.script*의 `update()`에서 처리합니다.

```lua
-- 파일: background1.script

function init(self)
    msg.post("@render:", "clear_color", { color = vmath.vector4(0.52, 0.80, 1, 0) } )
end

-- 배경은 게임 오브젝트 안의 타일 맵입니다
-- 패럴랙스 효과를 위해 게임 오브젝트를 이동합니다

function update(self, dt)
    -- 패럴랙스 효과를 위해 x 포지션을 프레임당 1 유닛 증가시킵니다
    local p = go.get_position()
    p.x = p.x + 1
    go.set_position(p)
end
```

```lua
-- 파일: background2.script

-- 배경은 게임 오브젝트 안의 타일 맵입니다
-- 패럴랙스 효과를 위해 게임 오브젝트를 이동합니다

function update(self, dt)
    -- 패럴랙스 효과를 위해 x 포지션을 프레임당 0.5 유닛 증가시킵니다
    local p = go.get_position()
    p.x = p.x + 0.5
    go.set_position(p)
end
```

비행접시는 *Sprite*와 *Script*를 포함하는 별도의 게임 오브젝트입니다.
일정한 속도로 왼쪽으로 이동합니다. 위아래 움직임은 Lua 사인 함수(`math.sin()`)를 사용해 고정값 주위에서 y 성분을 애니메이션하여 만듭니다. 이 동작은 *spaceship.script*의 `update()`에서 처리합니다.


```lua
-- 파일: spaceship.script

function init(self)
    -- 스크립트를 변경하지 않고 spaceship을 움직일 수 있도록
    -- 초기 y 포지션을 기억합니다
    self.start_y = go.get_position().y
    -- 카운터를 0으로 설정합니다. 아래 sin 이동에 사용합니다
    self.counter = 0
end

function update(self, dt)
    -- x 포지션을 프레임당 2 유닛 줄입니다
    local p = go.get_position()
    p.x = p.x - 2

    -- 초기 y를 기준으로 y 포지션을 이동합니다
    p.y = self.start_y + 8 * math.sin(self.counter * 0.08)

    -- 포지션을 업데이트합니다
    go.set_position(p)

    -- 화면 밖으로 나가면 spaceship을 제거합니다
    if p.x < - 32 then
        go.delete()
    end

    -- 카운터를 증가시킵니다
    self.counter = self.counter + 1
end
```
