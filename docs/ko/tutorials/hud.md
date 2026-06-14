---
title: HUD 코드 샘플
brief: 이 샘플 프로젝트에서는 점수 카운팅 효과를 배웁니다.
---
# HUD - 샘플 프로젝트

<iframe width="560" height="315" src="https://www.youtube.com/embed/NoPHHG2kbOk" frameborder="0" allowfullscreen></iframe>

[에디터에서 열거나](/manuals/project-setup/) [GitHub에서 다운로드](https://github.com/defold/sample-hud)할 수 있는 이 샘플 프로젝트에서는 점수 카운팅 효과를 보여줍니다. 점수는 화면 곳곳에 무작위로 나타나며, 플레이어가 여러 위치에서 점수를 얻는 게임을 시뮬레이션합니다.

점수는 나타난 뒤 잠시 떠 있습니다. 이를 구현하기 위해 점수를 투명하게 설정한 다음 색상을 페이드 인합니다. 또한 점수를 위쪽으로 애니메이션합니다. 이 작업은 아래의 `on_message()`에서 수행됩니다.

그런 다음 점수는 화면 상단의 총점 위치로 이동하고, 그곳에서 합산됩니다.
점수는 위로 이동하는 동안 약간 페이드 아웃됩니다. 이 작업은 `float_done()`에서 수행됩니다.

점수가 상단의 총점에 도달하면 해당 값이 타겟 점수에 더해지고, 총점은 그 타겟 점수를 향해 카운트 업됩니다. 이 작업은 `swoosh_done()`에서 수행됩니다.

스크립트가 업데이트될 때 타겟 점수가 증가했는지, 그리고 총점을 카운트 업해야 하는지 확인합니다. 조건이 참이면 총점이 더 작은 단계로 증가합니다.
그런 다음 총점의 스케일을 애니메이션해 튀어 오르는 효과를 줍니다. 이 작업은 `update()`에서 수행됩니다.

총점이 증가할 때마다 더 작은 별 여러 개를 스폰하고, 총점 위치에서 바깥쪽으로 애니메이션합니다. 별은 `spawn_stars()`, `fade_out_star()`, `delete_star()`에서 스폰, 애니메이션, 삭제됩니다.

```lua
-- 파일: hud.gui_script
-- 초당 점수가 카운트 업되는 속도
local score_inc_speed = 1000

function init(self)
    -- 타겟 점수는 게임의 현재 점수입니다
    self.target_score = 0
    -- 타겟 점수를 향해 카운트 업되는 현재 점수입니다
    self.current_score = 0
    -- HUD에 표시되는 점수입니다
    self.displayed_score = 0
    -- 아래에서 나중에 사용하기 위해 점수를 표시하는 노드의 참조를 보관합니다
    self.score_node = gui.get_node("score")
end

local function delete_star(self, star)
    -- 별의 애니메이션이 끝났으므로 삭제합니다
    gui.delete_node(star)
end

local function fade_out_star(self, star)
    -- 삭제하기 전에 별을 페이드 아웃합니다
    gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0), gui.EASING_INOUT, 0.2, 0.0, delete_star)
end

local function spawn_stars(self, amount)
    -- 별을 배치하는 데 사용할 점수 노드의 위치입니다
    local p = gui.get_position(self.score_node)
    -- 별이 스폰되는 위치로부터의 거리입니다
    local start_distance = 0
    -- 별이 멈추는 거리입니다
    local end_distance = 240
    -- 별 원 안에서 각 별 사이의 각도 간격입니다
    local angle_step = 2 * math.pi / amount
    -- 시작 각도를 무작위로 정합니다
    local angle = angle_step * math.random()
    for i=1,amount do
        -- 별이 고르게 분포되도록 단계만큼 각도를 증가시킵니다
        angle = angle + angle_step
        -- 별 이동 방향입니다
        local dir = vmath.vector3(math.cos(angle), math.sin(angle), 0)
        -- 별의 시작/끝 위치입니다
        local start_p = p + dir * start_distance
        local end_p = p + dir * end_distance
        -- 별 노드를 생성합니다
        local star = gui.new_box_node(vmath.vector3(start_p.x, start_p.y, 0), vmath.vector3(30, 30, 0))
        -- 텍스쳐를 설정합니다
        gui.set_texture(star, "star")
        -- 투명하게 설정합니다
        gui.set_color(star, vmath.vector4(1, 1, 1, 0))
        -- 페이드 인합니다
        gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_OUT, 0.2, 0.0, fade_out_star)
        -- 위치를 애니메이션합니다
        gui.animate(star, gui.PROP_POSITION, end_p, gui.EASING_NONE, 0.55)
    end
end

function update(self, dt)
    -- 점수를 업데이트해야 하는지 확인합니다
    if self.current_score < self.target_score then
        -- 이 타임스텝 동안 점수를 증가시켜 타겟 점수에 가까워지게 합니다
        self.current_score = self.current_score + score_inc_speed * dt
        -- 점수가 타겟 점수를 넘지 않도록 제한합니다
        self.current_score = math.min(self.current_score, self.target_score)
        -- 소수점 없이 표시할 수 있도록 점수를 내림합니다
        local floored_score = math.floor(self.current_score)
        -- 표시된 점수를 업데이트해야 하는지 확인합니다
        if self.displayed_score ~= floored_score then
            -- 표시된 점수를 업데이트합니다
            self.displayed_score = floored_score
            -- 점수 노드의 텍스트를 업데이트합니다
            gui.set_text(self.score_node, string.format("%d p", self.displayed_score))
            -- 점수 노드의 스케일을 일반 크기보다 약간 크게 설정합니다
            local s = 1.3
            gui.set_scale(self.score_node, vmath.vector3(s, s, s))
            -- 그런 다음 스케일을 원래 값으로 되돌리는 애니메이션을 실행합니다
            s = 1.0
            gui.animate(self.score_node, gui.PROP_SCALE, vmath.vector3(s, s, s), gui.EASING_OUT, 0.2)
            -- 별을 스폰합니다
            spawn_stars(self, 4)
        end
    end
end

-- 이 함수는 표시 점수가 update 함수에서 카운트 업될 수 있도록 추가된 점수를 저장합니다
local function swoosh_done(self, node)
    -- 노드에서 점수를 가져옵니다
    local amount = tonumber(gui.get_text(node))
    -- 타겟 점수를 증가시킵니다. 타겟 점수에 맞게 점수가 업데이트되는 방식은 update 함수를 참고하세요
    self.target_score = self.target_score + amount
    -- 임시 점수를 제거합니다
    gui.delete_node(node)
end

-- 이 함수는 처음에 떠 있던 노드가 표시된 총점 쪽으로 휙 이동하도록 애니메이션합니다
local function float_done(self, node)
    local duration = 0.2
    -- 표시된 점수 쪽으로 휙 이동합니다
    gui.animate(node, gui.PROP_POSITION, gui.get_position(self.score_node), gui.EASING_IN, duration, 0.0, swoosh_done)
    -- 휙 이동하는 동안 일부 페이드 아웃도 적용합니다
    gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0.6), gui.EASING_IN, duration)
end

function on_message(self, message_id, message, sender)
    -- 추가된 점수를 등록합니다. 이 메세지는 점수를 증가시키려는 어떤 대상도 보낼 수 있습니다
    if message_id == hash("add_score") then
        -- 새 임시 점수 노드를 생성합니다
        local node = gui.new_text_node(message.position, tostring(message.amount))
        -- 작은 폰트를 사용합니다
        gui.set_font(node, "small_score")
        -- 처음에는 투명합니다
        gui.set_color(node, vmath.vector4(1, 1, 1, 0))
        gui.set_outline(node, vmath.vector4(0, 0, 0, 0))
        -- 페이드 인합니다
        gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_OUT, 0.3)
        gui.animate(node, gui.PROP_OUTLINE, vmath.vector4(0, 0, 0, 1), gui.EASING_OUT, 0.3)
        -- 떠오르게 합니다
        local offset = vmath.vector3(0, 20, 0)
        gui.animate(node, gui.PROP_POSITION, gui.get_position(node) + offset, gui.EASING_NONE, 0.5, 0.0, float_done)
    end
end
```

main.script에서는 터치/마우스 입력을 받은 뒤, 터치 위치를 사용해 새 점수를 생성하도록 GUI 스크립트에 메세지를 보냅니다.

```lua
-- 클릭/터치 시 터치 위치를 얻고, 획득한 점수 값과 함께 메세지로 hud GUI 스크립트에 보냅니다.

function init(self)
    msg.post(".", "acquire_input_focus")
end

function on_input(self, action_id, action)
    local pos = vmath.vector3(action.x, action.y, 0) -- input action.x와 action.y를 터치의 x와 y 위치로 사용합니다
    if action_id == hash("touch") then
        if action.pressed then
            msg.post("main:/hud#hud", "add_score" , { position = pos, amount = 1500})
        end
    end
end
```
