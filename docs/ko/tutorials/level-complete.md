---
title: 레벨 완료 코드 샘플
brief: 이 샘플 프로젝트에서는 레벨이 완료되었을 때 점수가 올라가는 모습을 보여주는 효과를 배웁니다.
---
# 레벨 완료 - 샘플 프로젝트

<iframe width="560" height="315" src="https://www.youtube.com/embed/tSdTSvku1o8" frameborder="0" allowfullscreen></iframe>

에디터에서 [열거나](/manuals/project-setup/) [GitHub에서 다운로드할 수 있는](https://github.com/defold/sample-levelcomplete) 이 샘플 프로젝트에서는 레벨이 완료되었을 때 점수가 올라가는 모습을 보여주는 효과를 시연합니다. 총점이 올라가며, 서로 다른 점수 단계에 도달하면 별 세 개가 나타납니다. 이 샘플은 값을 조정할 때 빠르게 반복 작업할 수 있도록 리로드 기능도 사용합니다.

이 씬은 게임에서 보내는 메세지로 트리거됩니다.
메세지에는 획득한 총점과 별 세 개가 각각 나타날 점수 단계가 들어 있습니다.
이때 제목 텍스트("Level completed!")가 페이드 인되면서 일반 크기(100%)로 축소됩니다. 이 작업은 아래의 `on_message()`에서 수행됩니다.

제목 텍스트의 애니메이션이 완료되면 총점이 올라가기 시작합니다. 이때마다 현재 점수가 작은 단계만큼 증가합니다. 그런 다음 별 표시 단계 중 하나를 넘었는지 확인하고, 넘었다면 별 애니메이션이 시작됩니다(아래 참조). 목표 점수에 도달하지 않은 동안에는 총점이 튀는 효과로 애니메이션됩니다.
또한 총점에 가까워질수록 최대 스케일을 향해 커집니다. 같은 방식으로 색상도 흰색에서 녹색으로 점진적으로 바뀝니다. 이 작업은 `inc_score()`에서 수행됩니다.

별이 나타날 때마다 페이드 인되며 일반 크기로 축소됩니다. 이 작업은 `animate_star()`에서 수행됩니다.

별 애니메이션이 끝나면 더 작은 별들이 큰 별 주위에 원형으로 스폰됩니다. 이 작업은 `spawn_small_stars()`에서 수행됩니다.

그 다음 작은 별들이 별에서 무작위로 튀어나가도록 애니메이션됩니다. 바깥으로 퍼지는 동안 속도와 스케일이 모두 무작위로 정해집니다. 그런 다음 페이드 아웃되고 결국 삭제됩니다. 이 작업은 `animate_small_star()`와 `delete_small_star()`에서 수행됩니다.

점수가 총점에 도달하면 하이 스코어 표시가 페이드 인되고 제자리로 축소됩니다. 이 작업은 `inc_score()` 끝에서 시작되고 `animate_imprint()`에서 수행됩니다.

`setup()` 함수는 노드에 올바른 초기값이 들어가도록 합니다. `on_reload()`에서 `setup()`을 호출하면 Defold 에디터에서 스크립트가 리로드될 때마다 모든 것이 올바르게 설정되도록 할 수 있습니다.

```lua
-- file: level_complete.gui_script

-- 초당 점수가 증가하는 속도
local score_inc_speed = 51100
-- 점수를 업데이트하는 간격
local dt = 0.03
-- 카운트 시작 시 점수의 스케일
local score_start_scale = 0.7
-- 목표 점수에 도달했을 때 점수의 스케일
local score_end_scale = 1.0
-- 증가할 때마다 점수가 "튀는" 정도
local score_bounce_factor = 1.1
-- 큰 별마다 스폰할 작은 별의 수
local small_star_count = 16

local function setup(self)
    -- heading 색상을 투명하게 설정
    local c = gui.get_color(self.heading)
    c.w = 0
    gui.set_color(self.heading, c)
    -- heading 그림자를 투명하게 설정
    c = gui.get_shadow(self.heading)
    c.w = 0
    gui.set_shadow(self.heading, c)
    -- 초기에는 heading을 두 배 스케일로 설정
    local s = 2
    gui.set_scale(self.heading, vmath.vector3(s, s, s))
    -- 초기 score 설정 (0)
    gui.set_text(self.score, "0")
    -- score 색상을 불투명한 흰색으로 설정
    gui.set_color(self.score, vmath.vector4(1, 1, 1, 1))
    -- 카운트 중 score가 커질 수 있도록 스케일 설정
    gui.set_scale(self.score, vmath.vector4(score_start_scale, score_start_scale, 1, 0))

    -- 모든 큰 별을 투명하게 설정
    for i=1,#self.stars do
        gui.set_color(self.stars[i], vmath.vector4(1, 1, 1, 0))
    end
    -- imprint를 투명하게 설정
    gui.set_color(self.imprint, vmath.vector4(1, 1, 1, 0))
    -- 현재 표시 중인 점수
    self.current_score = 0
    -- 카운트할 목표 점수
    self.target_score = 0
end

function init(self)
    -- 더 쉽게 접근할 수 있도록 노드 가져오기
    self.heading = gui.get_node("heading")
    self.stars = {gui.get_node("star_left"), gui.get_node("star_mid"), gui.get_node("star_right")}
    self.score = gui.get_node("score")
    self.imprint = gui.get_node("imprint")
    -- score의 시작 색상
    self.score_start_color = vmath.vector4(1, 1, 1, 1)
    -- score 색상을 저장하고 나중에 카운트 중 이 색상으로 애니메이션
    self.score_end_color = gui.get_color(self.score)
    setup(self)
end

-- 작은 별 삭제, 별 애니메이션이 완료될 때 호출됨
local function delete_small_star(self, small_star)
    gui.delete_node(small_star)
end

-- 주어진 초기 위치와 각도에 따라 작은 별 애니메이션
local function animate_small_star(self, pos, angle)
    -- 작은 별이 이동할 방향
    local dir = vmath.vector3(math.cos(angle), math.sin(angle), 0, 0)
    -- 작은 별 생성
    local small_star = gui.new_box_node(pos + dir * 20, vmath.vector3(64, 64, 0))
    -- 텍스쳐 설정
    gui.set_texture(small_star, "small_star")
    -- 색상을 완전한 흰색으로 설정
    gui.set_color(small_star, vmath.vector4(1, 1, 1, 1))
    -- 시작 스케일을 작게 설정
    local start_s = 0.3
    gui.set_scale(small_star, vmath.vector3(start_s, start_s, 1))
    -- 각 작은 별의 스케일 변화량
    local end_s_var = 1
    -- 이 별의 실제 최종 스케일
    local end_s = 0.5 + math.random() * end_s_var
    gui.animate(small_star, gui.PROP_SCALE, vmath.vector4(end_s, end_s, 1, 0), gui.EASING_NONE, 0.5)
    -- 이동 거리의 변화량(사실상 별의 속도)
    local dist_var = 300
    -- 별이 실제로 이동할 거리
    local dist = 400 + math.random() * dist_var
    gui.animate(small_star, gui.PROP_POSITION, pos + dir * dist, gui.EASING_NONE, 0.5)
    gui.animate(small_star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0), gui.EASING_OUT, 0.3, 0.2, delete_small_star)
end

-- 여러 작은 별 스폰
local function spawn_small_stars(self, star)
    -- 작은 별이 주위에 스폰될 큰 별의 위치
    local p = gui.get_position(star)
    for i = 1,small_star_count do
        -- 해당 작은 별의 각도 계산
        local angle = 2 * math.pi * i/small_star_count
        -- 위치도 함께 설정
        local pos = vmath.vector3(p.x, p.y, 0)
        -- 작은 별을 스폰하고 애니메이션
        animate_small_star(self, pos, angle)
    end
end

-- 큰 별이 페이드 인되는 애니메이션 시작
local function animate_star(self, star)
    -- 페이드 인 지속 시간
    local fade_in = 0.2
    -- 투명하게 설정
    gui.set_color(star, vmath.vector4(1, 1, 1, 0))
    -- 페이드 인
    gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_IN, fade_in)
    -- 초기 스케일
    local scale = 5
    gui.set_scale(star, vmath.vector3(scale, scale, 1))
    -- 제자리로 축소
    gui.animate(star, gui.PROP_SCALE, vmath.vector4(1, 1, 1, 0), gui.EASING_IN, fade_in, 0, spawn_small_stars)
end

-- imprint가 페이드 인되는 애니메이션 시작
local function animate_imprint(self)
    -- imprint가 나타나기 전에 잠시 대기
    local delay = 0.8
    -- 페이드 인 지속 시간
    local fade_in = 0.2
    -- 초기 스케일
    local scale = 4
    gui.set_scale(self.imprint, vmath.vector4(scale, scale, 1, 0))
    -- 제자리로 축소
    gui.animate(self.imprint, gui.PROP_SCALE, vmath.vector4(1, 1, 1, 0), gui.EASING_IN, fade_in, delay)
    -- 함께 페이드 인
    gui.animate(self.imprint, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_IN, fade_in, delay)
end

-- 목표를 향해 점수를 한 단계 증가
local function inc_score(self, node)
    -- 이 단계에서 증가할 점수량
    local score_inc = score_inc_speed * dt
    -- 증가 후 새 점수
    local new_score = self.current_score + score_inc
    for i = 1,#self.stars do
        -- 별이 나타날 점수 단계를 넘으면 큰 별 애니메이션 시작
        if self.current_score < self.star_levels[i] and new_score >= self.star_levels[i] then
            animate_star(self, self.stars[i])
        end
    end
    -- 점수를 업데이트하되 목표값을 넘지 않도록 제한
    self.current_score = math.min(new_score, self.target_score)
    -- 화면의 score 업데이트
    gui.set_text(self.score, tostring(self.current_score))
    -- 아직 끝나지 않았다면 계속 애니메이션하고 증가
    if self.current_score < self.target_score then
        -- 목표에 얼마나 가까운지
        local f = self.current_score / self.target_score
        -- 천천히 페이드되도록 색상 혼합
        local c = vmath.lerp(f, self.score_start_color, self.score_end_color)
        gui.animate(self.score, gui.PROP_COLOR, c, gui.EASING_NONE, dt, 0, inc_score)
        -- 이 단계의 새 스케일
        local s = vmath.lerp(f, score_start_scale, score_end_scale)
        -- 바운스 계수만큼 스케일 증가
        local sp = s * score_bounce_factor
        -- 튄 스케일에서 적절한 스케일로 되돌아가도록 애니메이션
        gui.set_scale(self.score, vmath.vector4(sp, sp, 1, 0))
        gui.animate(self.score, gui.PROP_SCALE, vmath.vector4(s, s, 1, 0), gui.EASING_NONE, dt)
    else
        -- 완료되었으므로 imprint 페이드 인
        -- 참고: 실제 사례에서는 저장된 실제 최고 점수와 비교해야 합니다
        animate_imprint(self)
    end
end

function on_message(self, message_id, message, sender)
    -- 레벨 완료 씬을 표시하라는 메세지를 받음
    if message_id == hash("level_completed") then
        -- 획득한 점수와 별을 표시할 점수 단계 가져오기
        self.target_score = message.score
        self.star_levels = message.star_levels
        -- heading 페이드 인("level completed")
        local c = gui.get_color(self.heading)
        c.w = 1
        gui.animate(self.heading, gui.PROP_COLOR, c, gui.EASING_IN, dt, 0.0, inc_score)
        c = gui.get_shadow(self.heading)
        c.w = 1
        gui.animate(self.heading, gui.PROP_SHADOW, c, gui.EASING_IN, dt, 0.0)
        -- 제자리로 축소
        gui.animate(self.heading, gui.PROP_SCALE, vmath.vector4(1, 1, 1, 0), gui.EASING_IN, 0.2, 0.0)
    end
end

-- 이 함수는 스크립트가 리로드될 때 호출됩니다
-- 씬을 설정하고 레벨 완료를 시뮬레이션하면 조정을 위한 매우 빠른 워크플로우를 얻을 수 있습니다
function on_reload(self)
    -- setup 변경사항이 반영되도록 합니다
    setup(self)
    -- 레벨이 완료된 상황을 시뮬레이션합니다
    msg.post("#gui", "level_completed", {score = 102000, star_levels = {40000, 70000, 100000}})
end
```
