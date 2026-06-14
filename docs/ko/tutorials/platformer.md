---
title: Defold 플랫포머 튜토리얼
brief: 이 글에서는 Defold에서 기본적인 타일 기반 2D 플랫포머를 구현하는 과정을 살펴봅니다. 여기서 배우는 메커니즘은 좌우 이동, 점프, 낙하입니다.
---

# 플랫포머

이 글에서는 Defold에서 기본적인 타일 기반 2D 플랫포머를 구현하는 과정을 살펴봅니다. 여기서 배울 메커니즘은 좌우 이동, 점프, 낙하입니다.

플랫포머를 만드는 방법은 아주 다양합니다. Rodrigo Monteiro가 이 주제와 그 이상의 내용에 대해 방대한 분석을 [여기](http://higherorderfun.com/blog/2012/05/20/the-guide-to-implementing-2d-platformers/)에 작성했습니다.

플랫포머 제작이 처음이라면 유용한 정보가 많이 들어 있으므로 읽어 보는 것을 강력히 권장합니다. 여기서는 그 글에서 설명한 몇 가지 방법과 이를 Defold에서 구현하는 방법을 조금 더 자세히 살펴보겠습니다. 다만 모든 내용은 다른 플랫폼과 언어로도 쉽게 포팅할 수 있을 것입니다(Defold에서는 Lua를 사용합니다).

약간의 벡터 수학(선형대수)에 익숙하다고 가정합니다. 익숙하지 않다면 게임 개발에 매우 유용하므로 관련 내용을 읽어 두는 것이 좋습니다. Wolfire의 David Rosen이 이에 대해 아주 좋은 시리즈를 [여기](http://blog.wolfire.com/2009/07/linear-algebra-for-game-developers-part-1/)에 작성했습니다.

이미 Defold를 사용하고 있다면 _Platformer_ 템플릿 프로젝트를 기반으로 새 프로젝트를 만들고, 이 글을 읽으면서 직접 다뤄 볼 수 있습니다.

::: sidenote
몇몇 독자들이 우리가 제안한 방법은 Box2D의 기본 구현으로는 불가능하다고 지적했습니다. 이 동작을 가능하게 하려고 Box2D를 조금 수정했습니다.

kinematic 오브젝트와 static 오브젝트 사이의 충돌은 무시됩니다. `b2Body::ShouldCollide`와 `b2ContactManager::Collide`의 검사를 변경하세요.

또한 접촉 거리(Box2D에서는 separation이라고 부름)는 콜백 함수에 제공되지 않습니다.
`b2ManifoldPoint`에 distance 멤버를 추가하고 `b2Collide*` 함수에서 이 값이 업데이트되도록 하세요.
:::

## 충돌 감지

충돌 감지는 플레이어가 레벨 지오메트리를 통과해 움직이지 못하게 하는 데 필요합니다.
게임과 게임의 구체적인 요구사항에 따라 이를 처리하는 방법은 여러 가지입니다.
가능하다면 가장 쉬운 방법 중 하나는 물리 엔진이 처리하도록 맡기는 것입니다.
Defold에서는 2D 게임에 [Box2D](http://box2d.org/) 물리 엔진을 사용합니다.
Box2D의 기본 구현에는 필요한 모든 기능이 없으므로, 우리가 어떻게 수정했는지는 이 글의 맨 아래를 참고하세요.

물리 엔진은 물리 동작을 시뮬레이션하기 위해 물리 오브젝트의 상태와 모양을 함께 저장합니다. 또한 시뮬레이션 중 충돌을 보고하므로, 게임은 충돌이 발생하는 즉시 반응할 수 있습니다. 대부분의 물리 엔진에는 _static_, _dynamic_, _kinematic_ 오브젝트라는 세 가지 타입의 오브젝트가 있습니다(다른 물리 엔진에서는 이름이 다를 수 있습니다). 다른 타입의 오브젝트도 있지만 지금은 무시하겠습니다.

- *static* 오브젝트는 절대 움직이지 않습니다(예: 레벨 지오메트리).
- *dynamic* 오브젝트는 힘과 토크의 영향을 받으며, 이는 시뮬레이션 중 속도로 변환됩니다.
- *kinematic* 오브젝트는 어플리케이션 로직으로 제어되지만, 다른 dynamic 오브젝트에는 여전히 영향을 줍니다.

이런 게임에서는 현실 세계의 물리 동작과 비슷한 무언가를 원하지만, 반응성 좋은 조작과 균형 잡힌 메커니즘이 훨씬 더 중요합니다. 느낌이 좋은 점프가 물리적으로 정확하거나 현실 세계의 중력 아래에서 동작할 필요는 없습니다. 다만 [이](http://hypertextbook.com/facts/2007/mariogravity.shtml) 분석에 따르면 Mario 게임의 중력은 버전이 거듭될수록 9.8 m/s<sup>2</sup>에 가까워진다고 합니다. :-)

의도한 경험을 만들기 위해 메커니즘을 설계하고 조정할 수 있도록, 현재 일어나는 일을 완전히 제어하는 것이 중요합니다. 그래서 플레이어 캐릭터를 kinematic 오브젝트로 모델링하기로 합니다. 그러면 물리 힘을 다루지 않고도 원하는 대로 플레이어 캐릭터를 움직일 수 있습니다. 이는 캐릭터와 레벨 지오메트리 사이의 분리를 직접 해결해야 한다는 뜻이지만(자세한 내용은 뒤에서 설명), 감수할 만한 단점입니다. 물리 월드에서는 플레이어 캐릭터를 box shape으로 표현합니다.

## 이동

플레이어 캐릭터를 kinematic 오브젝트로 표현하기로 했으므로, 포지션을 설정해서 자유롭게 움직일 수 있습니다. 좌우 이동부터 시작하겠습니다.

이동은 캐릭터에 무게감을 주기 위해 가속도 기반으로 처리합니다. 일반적인 차량과 마찬가지로, 가속도는 플레이어 캐릭터가 최대 속도에 얼마나 빨리 도달하고 방향을 바꿀 수 있는지를 정의합니다. 가속도는 프레임 time-step에 걸쳐 작용하며, 보통 `dt`(delta-`t`) 파라미터로 제공되고, 그 결과가 속도에 더해집니다. 마찬가지로 속도는 프레임에 걸쳐 작용하고, 그 결과로 생긴 이동량이 포지션에 더해집니다. 수학에서는 이를 [시간에 대한 적분](http://en.wikipedia.org/wiki/Integral)이라고 합니다.

![근사 속도 적분](images/platformer/integration.png)

두 개의 세로선은 프레임의 시작과 끝을 표시합니다. 선의 높이는 이 두 시점에서 플레이어 캐릭터가 가진 속도입니다. 이 속도를 `v0`와 `v1`이라고 하겠습니다. `v1`은 time-step `dt` 동안 가속도(곡선의 기울기)를 적용해서 얻습니다.

![속도 방정식](images/platformer/equationofvelocity.png)

주황색 영역은 현재 프레임 동안 플레이어 캐릭터에 적용해야 하는 이동량입니다. 기하학적으로 이 영역은 다음과 같이 근사할 수 있습니다.

![이동량 방정식](images/platformer/equationoftranslation.png)

update 루프에서 캐릭터를 움직이기 위해 가속도와 속도를 적분하는 방식은 다음과 같습니다.

1. 입력에 따라 목표 속도를 결정합니다.
2. 현재 속도와 목표 속도의 차이를 계산합니다.
3. 차이의 방향으로 작용하도록 가속도를 설정합니다.
4. 이 프레임의 속도 변화량을 계산합니다(`dv`는 delta-velocity의 약자). 위와 같습니다.

    ```lua
    local dv = acceleration * dt
    ```

5. `dv`가 의도한 속도 차이를 초과하는지 확인하고, 그렇다면 clamp합니다.
6. 나중에 사용하기 위해 현재 속도를 저장합니다(`self.velocity`는 현재 시점에서 이전 프레임에 사용된 속도입니다).

    ```lua
    local v0 = self.velocity
    ```

7. 속도 변화량을 더해 새 속도를 계산합니다.

    ```lua
    self.velocity = self.velocity + dv
    ```

8. 위와 같이 속도를 적분해서 이 프레임의 x 이동량을 계산합니다.

    ```lua
    local dx = (v0 + self.velocity) * dt * 0.5
    ```

9. 이를 플레이어 캐릭터에 적용합니다.

Defold에서 입력을 처리하는 방법이 확실하지 않다면 [여기](/manuals/input)의 가이드를 참고하세요.

이 단계에서는 캐릭터를 좌우로 움직일 수 있고, 조작에 무게감 있고 부드러운 느낌을 줄 수 있습니다. 이제 중력을 추가해 보겠습니다!

중력도 가속도이지만, 플레이어에게 y축 방향으로 영향을 줍니다. 즉 위에서 설명한 이동 가속도와 같은 방식으로 적용됩니다. 위 계산을 벡터로 바꾸고 3단계에서 가속도의 y 컴포넌트에 중력을 포함하기만 하면 동작합니다. 벡터 수학은 참 좋습니다! :-)

## 충돌 반응

이제 플레이어 캐릭터가 움직이고 떨어질 수 있으므로, 충돌 반응을 살펴볼 차례입니다.
당연히 레벨 지오메트리 위에 착지하고 그 위를 따라 움직일 수 있어야 합니다. 아무것과도 겹치지 않도록 물리 엔진이 제공하는 접촉점을 사용하겠습니다.

접촉점은 접촉의 _normal_(충돌한 오브젝트에서 바깥쪽을 향하지만, 다른 엔진에서는 다를 수 있음)과 _distance_를 가집니다. distance는 다른 오브젝트 안으로 얼마나 파고들었는지를 측정합니다. 플레이어를 레벨 지오메트리에서 분리하는 데 필요한 것은 이것이 전부입니다.
box를 사용하기 때문에 한 프레임 동안 여러 접촉점이 생길 수 있습니다. 예를 들어 box의 두 모서리가 수평 지면과 교차하거나, 플레이어가 모서리 안으로 움직일 때 이런 일이 발생합니다.

![플레이어 캐릭터에 작용하는 접촉 normal](images/platformer/collision.png)

같은 보정을 여러 번 적용하지 않도록 보정값을 벡터에 누적하여 과도하게 보정하지 않게 합니다. 과도하게 보정하면 충돌한 오브젝트에서 너무 멀리 떨어진 위치에 놓이게 됩니다. 위 이미지에서는 현재 두 개의 접촉점이 있고, 두 화살표(normal)로 표시되어 있습니다. 두 접촉의 침투 거리는 같습니다. 이를 매번 그대로 사용하면 의도한 양의 두 배만큼 플레이어를 움직이게 됩니다.

::: sidenote
누적된 보정값을 매 프레임 0-vector로 리셋하는 것이 중요합니다.
`update()` 함수의 끝에 다음과 같은 코드를 넣으세요.
`self.corrections = vmath.vector3()`
:::

각 접촉점마다 호출되는 콜백 함수가 있다고 가정하면, 그 함수에서 분리를 처리하는 방법은 다음과 같습니다.

```lua
local proj = vmath.dot(self.correction, normal) -- <1>
local comp = (distance - proj) * normal -- <2>
self.correction = self.correction + comp -- <3>
go.set_position(go.get_position() + comp) -- <4>
```

1. 보정 벡터를 접촉 normal에 투영합니다(첫 번째 접촉점에서는 보정 벡터가 0-vector입니다).
2. 이 접촉점에 필요한 보정량을 계산합니다.
3. 이를 보정 벡터에 더합니다.
4. 보정량을 플레이어 캐릭터에 적용합니다.

접촉점을 향해 움직이는 플레이어 속도의 성분도 제거해야 합니다.

```lua
proj = vmath.dot(self.velocity, message.normal) -- <1>
if proj < 0 then
    self.velocity = self.velocity - proj * message.normal -- <2>
end
```
1. 속도를 normal에 투영합니다.
2. 투영값이 음수라면 속도의 일부가 접촉점을 향하고 있다는 뜻입니다. 이 경우 해당 컴포넌트를 제거합니다.

## 점프

이제 레벨 지오메트리 위를 달리고 아래로 떨어질 수 있으니, 점프할 차례입니다! 플랫포머 점프는 여러 가지 방식으로 만들 수 있습니다. 이 게임에서는 Super Mario Bros와 Super Meat Boy와 비슷한 느낌을 목표로 합니다. 점프할 때 플레이어 캐릭터는 임펄스로 위쪽으로 밀려 올라가며, 이는 기본적으로 고정된 속도입니다.

중력은 계속해서 캐릭터를 다시 아래로 끌어당기고, 그 결과 보기 좋은 점프 궤적이 만들어집니다. 공중에 있는 동안에도 플레이어는 캐릭터를 제어할 수 있습니다. 플레이어가 점프 궤적의 정점에 도달하기 전에 점프 버튼을 놓으면, 위쪽 속도를 줄여 점프를 일찍 멈춥니다.

1. 입력이 눌리면 다음을 실행합니다.

    ```lua
    -- jump_takeoff_speed는 다른 곳에 정의된 상수입니다.
    self.velocity.y = jump_takeoff_speed
    ```

    이 코드는 입력이 계속 _held down_된 매 프레임이 아니라, 입력이 _pressed_된 순간에만 실행해야 합니다.

2. 입력이 놓이면 다음을 실행합니다.

    ```lua
    -- 아직 올라가는 중이라면 점프를 일찍 끊습니다.
    if self.velocity.y > 0 then
        -- 위쪽 속도를 줄입니다.
        self.velocity.y = self.velocity.y * 0.5
    end
    ```

ExciteMike가 [Super Mario Bros 3](http://meyermike.com/wp/?p=175)와 [Super Meat Boy](http://meyermike.com/wp/?p=160)의 점프 궤적에 대한 좋은 그래프를 만들었으니 살펴볼 만합니다.

## 레벨 지오메트리

레벨 지오메트리는 플레이어 캐릭터(그리고 다른 것들)가 충돌하는 환경의 충돌 모양입니다. Defold에서는 이 지오메트리를 만드는 방법이 두 가지 있습니다.

하나는 빌드한 레벨 위에 별도의 충돌 모양을 만드는 방법입니다. 이 방법은 매우 유연하며 그래픽을 세밀하게 배치할 수 있습니다. 부드러운 경사를 만들고 싶을 때 특히 유용합니다.
[Braid](http://braid-game.com/) 게임은 이 방법으로 레벨을 만들었고, 이 튜토리얼의 예제 레벨도 이 방법으로 만들어졌습니다. Defold 에디터에서는 다음과 같이 보입니다.

![레벨 지오메트리와 플레이어가 월드에 배치된 Defold 에디터](images/platformer/editor.png)

다른 방법은 타일로 레벨을 만들고, 에디터가 타일 그래픽을 기반으로 물리 모양을 자동 생성하게 하는 것입니다. 이렇게 하면 레벨을 변경할 때 레벨 지오메트리가 자동으로 업데이트되므로 매우 유용할 수 있습니다.

배치된 타일이 정렬되어 있으면 물리 모양이 자동으로 하나로 병합됩니다.
이렇게 하면 플레이어 캐릭터가 여러 수평 타일 위를 미끄러져 이동할 때 멈추거나 튀게 만들 수 있는 틈이 제거됩니다. 이는 로드 시점에 Box2D에서 타일 폴리곤을 edge shape으로 교체하여 처리됩니다.

![하나로 이어 붙인 여러 타일 기반 폴리곤](images/platformer/stitching.png)

위는 플랫포머 그래픽 조각으로 이웃한 타일 다섯 개를 만든 예입니다. 이미지에서 배치된 타일(위쪽)이 하나로 이어 붙여진 단일 모양(아래쪽 회색 윤곽)에 어떻게 대응하는지 볼 수 있습니다.

자세한 내용은 [물리](/manuals/physics)와 [타일](/manuals/2dgraphics) 가이드를 확인하세요.

## 마무리

플랫포머 메커니즘에 대한 더 많은 정보가 필요하다면, [Sonic](http://info.sonicretro.org/Sonic_Physics_Guide)의 물리에 관한 매우 방대한 정보를 참고하세요.

iOS 기기나 마우스로 템플릿 프로젝트를 실행해 보면 점프가 꽤 어색하게 느껴질 수 있습니다.
이는 원터치 입력으로 플랫포밍을 구현하려는 우리의 부족한 시도일 뿐입니다. :-)

이 게임에서 애니메이션을 어떻게 처리했는지는 다루지 않았습니다. 아래의 *player.script*를 확인하고 `update_animations()` 함수를 찾아보면 감을 잡을 수 있습니다.

이 정보가 유용했기를 바랍니다!
멋진 플랫포머를 만들어서 모두가 플레이할 수 있게 해 주세요! <3

## 코드

다음은 *player.script*의 내용입니다.

```lua
-- player.script

-- 메커니즘을 조정하는 값입니다. 다른 느낌을 원한다면 자유롭게 변경하세요.
-- 오른쪽/왼쪽으로 이동하는 가속도
local move_acceleration = 3500
-- 공중에 있을 때 사용할 가속도 계수
local air_acceleration_factor = 0.8
-- 오른쪽/왼쪽 최대 속도
local max_speed = 450
-- 픽셀 단위로 플레이어를 아래로 끌어당기는 중력
local gravity = -1000
-- 점프할 때 픽셀 단위의 이륙 속도
local jump_takeoff_speed = 550
-- 더블 탭이 점프로 간주되기 위해 발생해야 하는 시간(마우스/터치 컨트롤에서만 사용)
local touch_jump_timeout = 0.2

-- id를 미리 해쉬하면 성능이 향상됩니다.
local msg_contact_point_response = hash("contact_point_response")
local msg_animation_done = hash("animation_done")
local group_obstacle = hash("obstacle")
local input_left = hash("left")
local input_right = hash("right")
local input_jump = hash("jump")
local input_touch = hash("touch")
local anim_run = hash("run")
local anim_idle = hash("idle")
local anim_jump = hash("jump")
local anim_fall = hash("fall")

function init(self)
    -- 이 스크립트에서 입력을 처리할 수 있게 합니다.
    msg.post(".", "acquire_input_focus")

    -- 플레이어의 초기 속도
    self.velocity = vmath.vector3(0, 0, 0)
    -- 충돌과 분리를 추적하기 위한 보조 변수
    self.correction = vmath.vector3()
    -- 플레이어가 지면 위에 서 있는지 여부
    self.ground_contact = false
    -- [-1,1] 범위의 이동 입력
    self.move_input = 0
    -- 현재 재생 중인 애니메이션
    self.anim = nil
    -- 마우스/터치를 사용할 때 점프 가능 시간을 제어하는 타이머
    self.touch_jump_timer = 0
end

local function play_animation(self, anim)
    -- 이미 재생 중이지 않은 애니메이션만 재생합니다.
    if self.anim ~= anim then
        -- 스프라이트에 애니메이션을 재생하라고 알립니다.
        sprite.play_flipbook("#sprite", anim)
        -- 어떤 애니메이션이 재생 중인지 기억합니다.
        self.anim = anim
    end
end

local function update_animations(self)
    -- 플레이어 캐릭터가 올바른 방향을 바라보게 합니다.
    sprite.set_hflip("#sprite", self.move_input < 0)
    -- 올바른 애니메이션이 재생되도록 합니다.
    if self.ground_contact then
        if self.velocity.x == 0 then
            play_animation(self, anim_idle)
        else
            play_animation(self, anim_run)
        end
    else
        if self.velocity.y > 0 then
            play_animation(self, anim_jump)
        else
            play_animation(self, anim_fall)
        end
    end
end

function update(self, dt)
    -- 입력에 따라 목표 속도를 결정합니다.
    local target_speed = self.move_input * max_speed
    -- 현재 속도와 목표 속도의 차이를 계산합니다.
    local speed_diff = target_speed - self.velocity.x
    -- 이 프레임에 걸쳐 적분할 전체 가속도
    local acceleration = vmath.vector3(0, gravity, 0)
    if speed_diff ~= 0 then
        -- 차이의 방향으로 작용하도록 가속도를 설정합니다.
        if speed_diff < 0 then
            acceleration.x = -move_acceleration
        else
            acceleration.x = move_acceleration
        end
        -- 공중에 있을 때는 더 느린 느낌을 주기 위해 가속도를 줄입니다.
        if not self.ground_contact then
            acceleration.x = air_acceleration_factor * acceleration.x
        end
    end
    -- 이 프레임의 속도 변화량을 계산합니다(dv는 delta-velocity의 약자입니다).
    local dv = acceleration * dt
    -- dv가 의도한 속도 차이를 초과하는지 확인하고, 그렇다면 clamp합니다.
    if math.abs(dv.x) > math.abs(speed_diff) then
        dv.x = speed_diff
    end
    -- 나중에 사용하기 위해 현재 속도를 저장합니다.
    -- (self.velocity는 현재 시점에서 이전 프레임에 사용된 속도입니다.)
    local v0 = self.velocity
    -- 속도 변화량을 더해 새 속도를 계산합니다.
    self.velocity = self.velocity + dv
    -- 속도를 적분해서 이 프레임의 이동량을 계산합니다.
    local dp = (v0 + self.velocity) * dt * 0.5
    -- 이를 플레이어 캐릭터에 적용합니다.
    go.set_position(go.get_position() + dp)

    -- 점프 타이머를 업데이트합니다.
    if self.touch_jump_timer > 0 then
        self.touch_jump_timer = self.touch_jump_timer - dt
    end

    update_animations(self)

    -- 휘발성 상태를 리셋합니다.
    self.correction = vmath.vector3()
    self.move_input = 0
    self.ground_contact = false

end

local function handle_obstacle_contact(self, normal, distance)
    -- 보정 벡터를 접촉 normal에 투영합니다.
    -- (첫 번째 접촉점에서는 보정 벡터가 0-vector입니다.)
    local proj = vmath.dot(self.correction, normal)
    -- 이 접촉점에 필요한 보정량을 계산합니다.
    local comp = (distance - proj) * normal
    -- 이를 보정 벡터에 더합니다.
    self.correction = self.correction + comp
    -- 보정량을 플레이어 캐릭터에 적용합니다.
    go.set_position(go.get_position() + comp)
    -- 플레이어가 지면 위에 서 있다고 간주할 만큼 normal이 충분히 위를 향하는지 확인합니다.
    -- (0.7은 순수한 수직 방향에서 약 45도 벗어난 것과 거의 같습니다.)
    if normal.y > 0.7 then
        self.ground_contact = true
    end
    -- 속도를 normal에 투영합니다.
    proj = vmath.dot(self.velocity, normal)
    -- 투영값이 음수라면 속도의 일부가 접촉점을 향하고 있다는 뜻입니다.
    if proj < 0 then
        -- 이 경우 해당 컴포넌트를 제거합니다.
        self.velocity = self.velocity - proj * normal
    end
end

function on_message(self, message_id, message, sender)
    -- 접촉점 메세지를 받았는지 확인합니다.
    if message_id == msg_contact_point_response then
        -- 오브젝트가 장애물로 간주하는 대상인지 확인합니다.
        if message.group == group_obstacle then
            handle_obstacle_contact(self, message.normal, message.distance)
        end
    end
end

local function jump(self)
    -- 지면에서만 점프를 허용합니다.
    -- (더블 점프 같은 동작을 만들려면 카운터를 추가해 확장하세요.)
    if self.ground_contact then
        -- 이륙 속도를 설정합니다.
        self.velocity.y = jump_takeoff_speed
        -- 애니메이션을 재생합니다.
        play_animation(self, anim_jump)
    end
end

local function abort_jump(self)
    -- 아직 올라가는 중이라면 점프를 일찍 끊습니다.
    if self.velocity.y > 0 then
        -- 위쪽 속도를 줄입니다.
        self.velocity.y = self.velocity.y * 0.5
    end
end

function on_input(self, action_id, action)
    if action_id == input_left then
        self.move_input = -action.value
    elseif action_id == input_right then
        self.move_input = action.value
    elseif action_id == input_jump then
        if action.pressed then
            jump(self)
        elseif action.released then
            abort_jump(self)
        end
    elseif action_id == input_touch then
        -- 터치 지점을 향해 이동합니다.
        local diff = action.x - go.get_position().x
        -- 멀리 떨어져 있을 때만 입력을 줍니다(10픽셀 초과).
        if math.abs(diff) > 10 then
            -- 100픽셀보다 가까워지면 감속합니다.
            self.move_input = diff / 100
            -- 입력을 [-1,1]로 clamp합니다.
            self.move_input = math.min(1, math.max(-1, self.move_input))
        end
        if action.released then
            -- 점프하려는지 확인하기 위해 마지막 release의 시간을 재기 시작합니다.
            self.touch_jump_timer = touch_jump_timeout
        elseif action.pressed then
            -- 더블 탭하면 점프합니다.
            if self.touch_jump_timer > 0 then
                jump(self)
            end
        end
    end
end
```
