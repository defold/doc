---
title: Defold 中的逐帧动画
brief: 本教程介绍了如何在 Defold 中使用逐帧动画.
---

# 逐帧动画

逐帧动画就是由一些列静态图片轮流显示生成的动画. 这种技术类似于老式翻页动画 (详见 http://en.wikipedia.org/wiki/Traditional_animation). 由于每帧的独立性使得这种技术很自由. 但是每帧一张图片会很耗费内存. 相似图片越多动画过渡越平滑同时也带来了巨大的工作量. Defold 逐帧动画使用来自于 [图集](/manuals/atlas), 或者 [瓷砖图源](/manuals/tilesource) 里水平排列的图片.

![Animation sheet](images/animation/animsheet.png){.inline}
![Run loop](images/animation/runloop.gif){.inline}

## 播放逐帧动画

Sprite 和 GUI 方块节点可以用来播放逐帧动画而且可以在运行时进行控制.

Sprites
: 通过调用 [`sprite.play_flipbook()`](/ref/sprite/?q=play_flipbook#sprite.play_flipbook:url-id-[complete_function]-[play_properties]) 函数播放逐帧动画. 示例见下文.

GUI 方块节点
: 通过调用 [`gui.play_flipbook()`](/ref/gui/?q=play_flipbook#gui.play_flipbook:node-animation-[complete_function]-[play_properties]) 函数播放逐帧动画. 示例见下文.

::: 注意
ping-pong 播放模式把动画从第一帧播放到最后一帧再反向播放到 **第二帧** , 而不是第一帧. 这样便于连续播放的衔接.
:::

### Sprite 示例

假设你的游戏有个 "dodge" 功能, 按下指定的键主角就进行闪避动作. 为此你建立了四组动画:

"idle"
: 主角待机的循环动画.

"dodge_idle"
: 主角闪避动作的循环动画.

"start_dodge"
: 主角从站立姿态到闪避动作的一次性动画.

"stop_dodge"
: 主角从闪避动作到站立姿态的一次性动画.

逻辑代码如下:

```lua

local function play_idle_animation(self)
    if self.dodge then
        sprite.play_flipbook("#sprite", hash("dodge_idle"))
    else
        sprite.play_flipbook("#sprite", hash("idle"))
    end
end

function on_input(self, action_id, action)
    -- "dodge" 就是输入动作
    if action_id == hash("dodge") then
        if action.pressed then
            sprite.play_flipbook("#sprite", hash("start_dodge"), play_idle_animation)
            -- 记录闪避动作已开始
            self.dodge = true
        elseif action.released then
            sprite.play_flipbook("#sprite", hash("stop_dodge"), play_idle_animation)
            -- 记录闪避动作完成
            self.dodge = false
        end
    end
end
```

### GUI 方块节点示例

给节点选择图片或者动画时, 实际上也同时指定了图片来源 (图集或者瓷砖图源) 以及默认动画. 节点图源是静态的, 但是当前播放的动画是可以在运行时指定的. 静态图片被视作单帧动画, 所以运行时切换图片相当于播放另一个动画:

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    local character_node = gui.get_node("character")
    -- 新动画/图片播放时
    -- 节点图源要存在默认动画.
    gui.play_flipbook(character_node, "jump_left", flipbook_done)
end
```


## 播放完成回调函数

动画函数 (`sprite.play_flipbook()` 和 `gui.play_flipbook()`) 可以在最后一个参数上传入Lua回调函数. 当动画播放完成时会调用这个函数. 对于循环动画, 和使用 `go.cancel_animations()` 手动取消播放的动画, 不会调用回调函数. 动画播放完成的回调函数里可以发送消息或者继续播放其他动画. 例如:

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    sprite.play_flipbook("#character", "jump_left", flipbook_done)
end
```

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    gui.play_flipbook(gui.get_node("character"), "jump_left", flipbook_done)
end
```
