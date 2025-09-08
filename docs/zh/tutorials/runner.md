# 无尽跑酷游戏教程

本教程将引导您创建一个简单的无尽跑酷游戏。游戏将包含一个不断向前奔跑的英雄角色，玩家需要控制角色跳跃避开障碍物。我们将使用Defold游戏引擎和Lua脚本语言来实现这个游戏。

## 设计步骤

1. 安装与设置
2. 编辑器介绍
3. 项目配置
4. 创建地面
5. 创建英雄角色
6. 地面物理与平台
7. 动画与死亡
8. 重置关卡
9. 收集金币

## STEP 1 - 安装与设置

1. 下载并安装[Defold编辑器](https://www.defold.com/download/)。
2. 启动编辑器并选择"Create New Project"（创建新项目）。
3. 为项目命名，例如"runner"，然后点击"Create"（创建）。
4. 等待项目创建完成，然后点击"Open Project"（打开项目）。

## STEP 2 - 编辑器介绍

Defold编辑器由几个主要部分组成：

- **Assets Pane（资源面板）**：显示项目中的所有文件和文件夹。
- **Outline（大纲）**：显示当前打开的文件的结构。
- **Editor（编辑器）**：显示当前打开的文件的内容。
- **Console（控制台）**：显示错误和警告信息。
- **Properties（属性）**：显示当前选中对象的属性。

## STEP 3 - 项目配置

1. 在Assets Pane中，双击打开"game.project"文件。
2. 在"Display"部分，设置"Width"为960，"Height"为640。
3. 在"Bootstrap"部分，设置"Main Collection"为"main.collection"。
4. 保存文件（Ctrl+S）。

## STEP 4 - 创建地面

1. 在Assets Pane中，右键点击"level"文件夹，选择"New ▸ Game Object File"（新建 ▸ 游戏对象文件）。
2. 将文件命名为"ground.go"。
3. 打开"ground.go"文件，在Outline中右键点击，选择"Add Component"（添加组件）。
4. 选择"Sprite"（精灵）组件。
5. 在Properties中，设置"Image"为"level.atlas"，"Default Animation"为"ground"。
6. 保存文件（Ctrl+S）。
7. 在Assets Pane中，右键点击"level"文件夹，选择"New ▸ Script File"（新建 ▸ 脚本文件）。
8. 将文件命名为"ground.script"。
9. 打开"ground.script"文件，将以下代码复制到文件中：

    ```lua
    -- ground.script
    function init(self)
        self.pieces = {} -- <1>
        self.speed = 540 -- Default speed in pixels/s
        self.gridw = 0
        self.gridh = 256
        self.grid = 460
    end

    function update(self, dt)
        self.gridw = self.gridw + self.speed * dt

        if self.gridw >= self.grid then
            self.gridw = 0
            local pos = go.get_position()
            pos.x = pos.x + self.grid
            local piece = factory.create("#ground_factory", pos) -- <2>
            table.insert(self.pieces, piece)
        end

        -- Move all pieces
        for i, p in ipairs(self.pieces) do
            local pos = go.get_position(p)
            pos.x = pos.x - self.speed * dt
            go.set_position(pos, p)

            -- Delete pieces that have moved off screen
            if pos.x < -self.grid then
                go.delete(p)
                table.remove(self.pieces, i)
            end
        end
    end
    ```
    1. 我们使用一个表来存储所有创建的地面片段
    2. 我们使用工厂组件来创建新的地面片段

10. 保存文件（Ctrl+S）。
11. 在Assets Pane中，打开"ground.go"文件，在Outline中右键点击，选择"Add Component"（添加组件）。
12. 选择"Factory"（工厂）组件。
13. 在Properties中，设置"Id"为"ground_factory"，"Prototype"为"ground.go"。
14. 保存文件（Ctrl+S）。
15. 在Assets Pane中，打开"main.collection"文件，将"ground.go"拖到场景中。
16. 保存文件（Ctrl+S）。

## STEP 5 - 创建英雄角色

1. 在Assets Pane中，右键点击"level"文件夹，选择"New ▸ Game Object File"（新建 ▸ 游戏对象文件）。
2. 将文件命名为"hero.go"。
3. 打开"hero.go"文件，在Outline中右键点击，选择"Add Component"（添加组件）。
4. 选择"Sprite"（精灵）组件。
5. 在Properties中，设置"Image"为"level.atlas"，"Default Animation"为"hero"。
6. 保存文件（Ctrl+S）。
7. 在Assets Pane中，右键点击"level"文件夹，选择"New ▸ Script File"（新建 ▸ 脚本文件）。
8. 将文件命名为"hero.script"。
9. 打开"hero.script"文件，将以下代码复制到文件中：

    ```lua
    -- hero.script
    go.property("gravity", -1000) -- <1>
    go.property("jump_speed", 400) -- <2>

    function init(self)
        -- this lets us handle input in this script
        msg.post(".", "acquire_input_focus")
        -- save position
        self.position = go.get_position()
        self.velocity = vmath.vector3(0, 0, 0)
        self.ground_contact = false
        self.anim = nil
    end

    function update(self, dt)
        -- Apply gravity
        self.velocity.y = self.velocity.y + self.gravity * dt

        -- Apply velocity to position
        local pos = go.get_position()
        pos = pos + self.velocity * dt
        go.set_position(pos)

        -- Update animation
        if self.ground_contact then
            if not self.anim then
                self.anim = hash("run")
                play_animation(self, self.anim)
            end
        else
            if self.anim ~= hash("jump") then
                self.anim = hash("jump")
                play_animation(self, self.anim)
            end
        end
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then
            -- Reset position
            go.set_position(self.position)
            -- Reset velocity
            self.velocity = vmath.vector3(0, 0, 0)
            -- Reset animation
            self.anim = nil
            go.set(".", "euler.z", 0)
            go.set_position(self.position)
            msg.post("#collisionobject", "enable")

        elseif message_id == hash("contact_point_response") then
            -- check if we received a contact point message
            if message.group == hash("danger") then
                -- Die and restart
                play_animation(self, hash("death"))
                msg.post("#collisionobject", "disable")
                -- <1>
                go.animate(".", "euler.z", go.PLAYBACK_ONCE_FORWARD, 160, go.EASING_LINEAR, 0.7)
                go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
                    function()
                        msg.post("controller#controller", "reset")
                    end)
            elseif message.group == hash("geometry") then
                handle_geometry_contact(self, message.normal, message.distance)
            end
        end
    end

    function on_input(self, action_id, action)
        if action_id == hash("jump") and action.pressed and self.ground_contact then
            -- Apply jump speed
            self.velocity.y = self.jump_speed
        end
    end

    function play_animation(self, anim)
        -- Play animation
        sprite.play_flipbook("#sprite", anim)
    end

    function handle_geometry_contact(self, normal, distance)
        -- Check if we're on the ground
        if normal.y > 0.7 then
            self.ground_contact = true
            -- Project the velocity onto the normal
            local proj = vmath.dot(self.velocity, normal)
            -- Remove the normal component of the velocity
            self.velocity = self.velocity - normal * proj
        end
    end
    ```
    1. 重力值，负值表示向下
    2. 跳跃速度

10. 保存文件（Ctrl+S）。
11. 在Assets Pane中，打开"hero.go"文件，在Outline中右键点击，选择"Add Component"（添加组件）。
12. 选择"Collision Object"（碰撞对象）组件。
13. 在Properties中，设置"Type"为"Kinematic"，"Group"为"hero"，"Mask"为"geometry"。
14. 在Outline中，右键点击"Collision Object"组件，选择"Add Shape"（添加形状）。
15. 选择"Box"（盒子）形状。
16. 使用Move Tool（场景 ▸ 移动工具）和Scale Tool调整盒子大小，使其覆盖英雄角色。
17. 保存文件（Ctrl+S）。
18. 在Assets Pane中，打开"main.collection"文件，将"hero.go"拖到场景中，放置在地面之上。
19. 保存文件（Ctrl+S）。
20. 在Assets Pane中，打开"game.project"文件，在"Input"部分，添加以下绑定：
    - Trigger: "KEY_SPACE", Action: "jump"
    - Trigger: "MOUSE_BUTTON_LEFT", Action: "touch"
21. 保存文件（Ctrl+S）。

## STEP 6 - 地面物理与平台

1. 在Assets Pane中，右键点击"level"文件夹，选择"New ▸ Game Object File"（新建 ▸ 游戏对象文件）。
2. 将文件命名为"platform.go"。
3. 打开"platform.go"文件，在Outline中右键点击，选择"Add Component"（添加组件）。
4. 选择"Sprite"（精灵）组件。
5. 在Properties中，设置"Image"为"level.atlas"，"Default Animation"为"platform"。
6. 保存文件（Ctrl+S）。
7. 在Assets Pane中，右键点击"level"文件夹，选择"New ▸ Game Object File"（新建 ▸ 游戏对象文件）。
8. 将文件命名为"platform_long.go"。
9. 打开"platform_long.go"文件，在Outline中右键点击，选择"Add Component"（添加组件）。
10. 选择"Sprite"（精灵）组件。
11. 在Properties中，设置"Image"为"level.atlas"，"Default Animation"为"platform_long"。
12. 保存文件（Ctrl+S）。
13. 在Assets Pane中，右键点击"level"文件夹，选择"New ▸ Script File"（新建 ▸ 脚本文件）。
14. 将文件命名为"platform.script"。
15. 打开"platform.script"文件，将以下代码复制到文件中：

    ```lua
    -- platform.script
    function init(self)
        self.speed = 540     -- Default speed in pixels/s
        self.coins = {}
    end

    function final(self)
        for i,p in ipairs(self.coins) do
            go.delete(p)
        end
    end

    function update(self, dt)
        local pos = go.get_position()
        if pos.x < -500 then
            msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
        end
        pos.x = pos.x - self.speed * dt
        go.set_position(pos)
    end

    function create_coins(self, params)
        local spacing = 56
        local pos = go.get_position()
        local x = pos.x - params.coins * (spacing*0.5) - 24
        for i = 1, params.coins do
            local coin = factory.create("#coin_factory", vmath.vector3(x + i * spacing , pos.y + 64, 1))
            msg.post(coin, "set_parent", { parent_id = go.get_id() }) -- <1>
            msg.post(coin, "start_animation", { delay = i/10 }) -- <2>
            table.insert(self.coins, coin)
        end
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("set_speed") then
            self.speed = message.speed
        elseif message_id == hash("create_coins") then
            create_coins(self, message)
        end
    end
    ```
    1. 通过设置生成金币的父对象为平台，金币将随着平台一起移动。
    2. 动画使金币上下跳动，相对于现在作为金币父对象的平台。

16. 保存文件（Ctrl+S）。
17. 在Assets Pane中，打开"platform.go"文件，在Outline中右键点击，选择"Add Component"（添加组件）。
18. 选择"Collision Object"（碰撞对象）组件。
19. 在Properties中，设置"Type"为"Static"，"Group"为"geometry"，"Mask"为"hero"。
20. 在Outline中，右键点击"Collision Object"组件，选择"Add Shape"（添加形状）。
21. 选择"Box"（盒子）形状。
22. 使用Move Tool（场景 ▸ 移动工具）和Scale Tool调整盒子大小，使其覆盖平台。
23. 保存文件（Ctrl+S）。
24. 在Assets Pane中，打开"platform_long.go"文件，重复步骤17-23。
25. 在Assets Pane中，右键点击"level"文件夹，选择"New ▸ Game Object File"（新建 ▸ 游戏对象文件）。
26. 将文件命名为"controller.go"。
27. 打开"controller.go"文件，在Outline中右键点击，选择"Add Component"（添加组件）。
28. 选择"Script"（脚本）组件。
29. 在Properties中，设置"Script"为"controller.script"。
30. 保存文件（Ctrl+S）。
31. 在Assets Pane中，右键点击"level"文件夹，选择"New ▸ Script File"（新建 ▸ 脚本文件）。
32. 将文件命名为"controller.script"。
33. 打开"controller.script"文件，将以下代码复制到文件中：

    ```lua
    -- controller.script
    go.property("speed", 360)

    local grid = 460
    local platform_heights = { 100, 200, 350 }
    local coins = 3 -- <1>

    function init(self)
        msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
        self.gridw = 0
        self.spawns = {} -- <2>
    end

    function update(self, dt)
        self.gridw = self.gridw + self.speed * dt

        if self.gridw >= grid then
            self.gridw = 0

            -- Maybe spawn a platform at random height
            if math.random() > 0.2 then
                local h = platform_heights[math.random(#platform_heights)]
                local f = "#platform_factory"
                local coins = coins
                if math.random() > 0.5 then
                    f = "#platform_long_factory"
                    coins = coins * 2 -- 长平台上的金币数量是普通平台的两倍
                end

                local p = factory.create(f, vmath.vector3(1600, h, 0), nil, {}, 0.6)
                msg.post(p, "set_speed", { speed = self.speed })
                msg.post(p, "create_coins", { coins = coins })
                table.insert(self.spawns, p) -- <2>
            end
        end
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then -- <3>
            -- Tell the hero to reset.
            msg.post("hero#hero", "reset")
            -- Delete all platforms
            for i,p in ipairs(self.spawns) do
                go.delete(p)
            end
            self.spawns = {}
        elseif message_id == hash("delete_spawn") then -- <4>
            for i,p in ipairs(self.spawns) do
                if p == message.id then
                    table.remove(self.spawns, i)
                    go.delete(p)
                end
            end
        end
    end
    ```
    1. 在普通平台上生成的金币数量
    2. 我们使用一个表来存储所有生成的平台
    3. "reset"消息删除表中存储的所有平台
    4. "delete_spawn"消息删除特定平台并将其从表中移除

34. 保存文件（Ctrl+S）。
35. 在Assets Pane中，打开"platform.go"文件，在Outline中右键点击，选择"Add Component"（添加组件）。
36. 选择"Factory"（工厂）组件。
37. 在Properties中，设置"Id"为"platform_factory"，"Prototype"为"platform.go"。
38. 保存文件（Ctrl+S）。
39. 在Assets Pane中，打开"platform_long.go"文件，在Outline中右键点击，选择"Add Component"（添加组件）。
40. 选择"Factory"（工厂）组件。
41. 在Properties中，设置"Id"为"platform_long_factory"，"Prototype"为"platform_long.go"。
42. 保存文件（Ctrl+S）。
43. 在Assets Pane中，打开"main.collection"文件，将"controller.go"拖到场景中。
44. 保存文件（Ctrl+S）。

## STEP 7 - 动画与死亡

1. 在Assets Pane中，打开"hero.script"文件，将以下代码添加到文件中：

    ```lua
    -- hero.script
    function play_animation(self, anim)
        -- Play animation
        sprite.play_flipbook("#sprite", anim)
    end

    function update_animation(self)
        -- Update animation
        if self.ground_contact then
            if not self.anim then
                self.anim = hash("run")
                play_animation(self, self.anim)
            end
        else
            if self.anim ~= hash("jump") then
                self.anim = hash("jump")
                play_animation(self, self.anim)
            end
        end
    end
    ```

2. 在Assets Pane中，打开"hero.script"文件，将update函数修改为：

    ```lua
    -- hero.script
    function update(self, dt)
        -- Apply gravity
        self.velocity.y = self.velocity.y + self.gravity * dt

        -- Apply velocity to position
        local pos = go.get_position()
        pos = pos + self.velocity * dt
        go.set_position(pos)

        -- Update animation
        update_animation(self)
    end
    ```

3. 保存文件（Ctrl+S）。
4. 在Assets Pane中，打开"platform.go"文件，在Outline中右键点击，选择"Add Component"（添加组件）。
5. 选择"Collision Object"（碰撞对象）组件。
6. 在Properties中，设置"Type"为"Static"，"Group"为"danger"，"Mask"为"hero"。
7. 在Outline中，右键点击"Collision Object"组件，选择"Add Shape"（添加形状）。
8. 选择"Box"（盒子）形状。
9. 使用Move Tool（场景 ▸ 移动工具）和Scale Tool调整盒子大小，使其覆盖平台边缘。
10. 保存文件（Ctrl+S）。
11. 在Assets Pane中，打开"platform_long.go"文件，重复步骤4-10。
12. 在Assets Pane中，打开"hero.go"文件，在Properties中，将"Collision Object"组件的"Mask"属性添加"danger"。
13. 保存文件（Ctrl+S）。

## STEP 8 - 重置关卡

1. 在Assets Pane中，打开"controller.script"文件，将以下代码添加到文件中：

    ```lua
    -- controller.script
    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then
            -- Tell the hero to reset.
            msg.post("hero#hero", "reset")
            -- Delete all platforms
            for i,p in ipairs(self.spawns) do
                go.delete(p)
            end
            self.spawns = {}
        elseif message_id == hash("delete_spawn") then
            for i,p in ipairs(self.spawns) do
                if p == message.id then
                    table.remove(self.spawns, i)
                    go.delete(p)
                end
            end
        end
    end
    ```

2. 保存文件（Ctrl+S）。
3. 在Assets Pane中，打开"platform.script"文件，将以下代码添加到文件中：

    ```lua
    -- platform.script
    function update(self, dt)
        local pos = go.get_position()
        if pos.x < -500 then
            msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
        end
        pos.x = pos.x - self.speed * dt
        go.set_position(pos)
    end
    ```

4. 保存文件（Ctrl+S）。
5. 在Assets Pane中，打开"hero.script"文件，将以下代码添加到文件中：

    ```lua
    -- hero.script
    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then
            -- Reset position
            go.set_position(self.position)
            -- Reset velocity
            self.velocity = vmath.vector3(0, 0, 0)
            -- Reset animation
            self.anim = nil
            go.set(".", "euler.z", 0)
            go.set_position(self.position)
            msg.post("#collisionobject", "enable")

        elseif message_id == hash("contact_point_response") then
            -- check if we received a contact point message
            if message.group == hash("danger") then
                -- Die and restart
                play_animation(self, hash("death"))
                msg.post("#collisionobject", "disable")
                -- <1>
                go.animate(".", "euler.z", go.PLAYBACK_ONCE_FORWARD, 160, go.EASING_LINEAR, 0.7)
                go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
                    function()
                        msg.post("controller#controller", "reset")
                    end)
            elseif message.group == hash("geometry") then
                handle_geometry_contact(self, message.normal, message.distance)
            end
        end
    end
    ```
    1. 为死亡中的英雄添加旋转和下落动作。这可以大大改进！

6. 保存文件（Ctrl+S）。
7. 在Assets Pane中，打开"hero.script"文件，将init函数修改为：

    ```lua
    -- hero.script
    function init(self)
        -- this lets us handle input in this script
        msg.post(".", "acquire_input_focus")
        -- save position
        self.position = go.get_position()
        msg.post("#", "reset")
    end
    ```

8. 保存文件（Ctrl+S）。

## STEP 9 - 收集金币

1. 在Assets Pane中，右键点击"level"文件夹，选择"New ▸ Game Object File"（新建 ▸ 游戏对象文件）。
2. 将文件命名为"coin.go"。
3. 打开"coin.go"文件，在Outline中右键点击，选择"Add Component"（添加组件）。
4. 选择"Sprite"（精灵）组件。
5. 在Properties中，设置"Image"为"level.atlas"，"Default Animation"为"coin"。
6. 保存文件（Ctrl+S）。
7. 在Assets Pane中，右键点击"level"文件夹，选择"New ▸ Script File"（新建 ▸ 脚本文件）。
8. 将文件命名为"coin.script"。
9. 打开"coin.script"文件，将以下代码复制到文件中：

    ```lua
    -- coin.script
    function init(self)
        self.collected = false
    end

    function on_message(self, message_id, message, sender)
        if self.collected == false and message_id == hash("collision_response") then
            self.collected = true
            msg.post("#sprite", "disable")
        elseif message_id == hash("start_animation") then
            pos = go.get_position()
            go.animate(go.get_id(), "position.y", go.PLAYBACK_LOOP_PINGPONG, pos.y + 24, go.EASING_INOUTSINE, 0.75, message.delay)
        end
    end
    ```

10. 保存文件（Ctrl+S）。
11. 在Assets Pane中，打开"coin.go"文件，在Outline中右键点击，选择"Add Component"（添加组件）。
12. 选择"Collision Object"（碰撞对象）组件。
13. 在Properties中，设置"Type"为"Kinematic"，"Group"为"pickup"，"Mask"为"hero"。
14. 在Outline中，右键点击"Collision Object"组件，选择"Add Shape"（添加形状）。
15. 选择"Sphere"（球体）形状。
16. 使用Move Tool（场景 ▸ 移动工具）和Scale Tool调整球体大小，使其覆盖金币。
17. 保存文件（Ctrl+S）。
18. 在Assets Pane中，打开"hero.go"文件，在Properties中，将"Collision Object"组件的"Mask"属性添加"pickup"。
19. 保存文件（Ctrl+S）。
20. 在Assets Pane中，打开"platform.go"文件，在Outline中右键点击，选择"Add Component"（添加组件）。
21. 选择"Factory"（工厂）组件。
22. 在Properties中，设置"Id"为"coin_factory"，"Prototype"为"coin.go"。
23. 保存文件（Ctrl+S）。
24. 在Assets Pane中，打开"platform_long.go"文件，重复步骤20-23。
25. 在Assets Pane中，打开"platform.script"文件，将以下代码添加到文件中：

    ```lua
    -- platform.script
    function init(self)
        self.speed = 540     -- Default speed in pixels/s
        self.coins = {}
    end

    function final(self)
        for i,p in ipairs(self.coins) do
            go.delete(p)
        end
    end

    function update(self, dt)
        local pos = go.get_position()
        if pos.x < -500 then
            msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
        end
        pos.x = pos.x - self.speed * dt
        go.set_position(pos)
    end

    function create_coins(self, params)
        local spacing = 56
        local pos = go.get_position()
        local x = pos.x - params.coins * (spacing*0.5) - 24
        for i = 1, params.coins do
            local coin = factory.create("#coin_factory", vmath.vector3(x + i * spacing , pos.y + 64, 1))
            msg.post(coin, "set_parent", { parent_id = go.get_id() }) -- <1>
            msg.post(coin, "start_animation", { delay = i/10 }) -- <2>
            table.insert(self.coins, coin)
        end
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("set_speed") then
            self.speed = message.speed
        elseif message_id == hash("create_coins") then
            create_coins(self, message)
        end
    end
    ```
    1. 通过设置生成金币的父对象为平台，金币将随着平台一起移动。
    2. 动画使金币上下跳动，相对于现在作为金币父对象的平台。

26. 保存文件（Ctrl+S）。
27. 在Assets Pane中，打开"controller.script"文件，将以下代码添加到文件中：

    ```lua
    -- controller.script
    local coins = 3 -- <1>
    ```
    1. 在普通平台上生成的金币数量

28. 在Assets Pane中，打开"controller.script"文件，将以下代码添加到update函数中：

    ```lua
    -- controller.script
    local coins = coins
    if math.random() > 0.5 then
        f = "#platform_long_factory"
        coins = coins * 2 -- 长平台上的金币数量是普通平台的两倍
    end
    ```

29. 在Assets Pane中，打开"controller.script"文件，将以下代码添加到update函数中：

    ```lua
    -- controller.script
    msg.post(p, "set_speed", { speed = self.speed })
    msg.post(p, "create_coins", { coins = coins })
    table.insert(self.spawns, p)
    ```

30. 保存文件（Ctrl+S）。

::: sidenote
父子关系严格来说是_场景图_的修改。子对象将随着其父对象一起变换（移动、缩放或旋转）。如果您需要在游戏对象之间添加额外的"所有权"关系，您需要在代码中专门跟踪这些关系。
:::

现在我们有了一个简单但功能齐全的游戏！如果您能做到这一步，您可能想要继续自行添加以下内容：

1. 分数和生命计数器
2. 收集和死亡的粒子效果
3. 精美的背景图像

> 在[这里](images/runner/sample-runner.zip)下载项目的完整版本

本入门教程到此结束。现在开始深入Defold吧。我们准备了许多[手册和教程](//www.defold.com/learn)来指导您，如果您遇到困难，欢迎来到[论坛](//forum.defold.com)。

祝您使用Defold愉快！