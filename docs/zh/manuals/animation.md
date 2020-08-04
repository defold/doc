---
title: Defold 动画教程
brief: 本教程介绍了 Defold 的动画支持.
---

# 动画

Defold 内置支持多种动画:

* 逐帧动画
* Spine 动画
* 3D 蒙皮动画
* 属性动画

## 逐帧动画

逐帧动画就是由一些列静态图片轮流显示生成的动画. 这种技术类似于老式翻页动画 (详见 http://en.wikipedia.org/wiki/Traditional_animation). 由于每帧的独立性使得这种技术很自由. 但是每帧一张图片会很耗费内存. 相似图片越多动画过渡越平滑同时也带来了巨大的工作量. Defold 逐帧动画使用来自于 [图集](/manuals/atlas), 或者 [瓷砖图源](/manuals/tilesource) 里水平排列的图片.

  ![Animation sheet](images/animation/animsheet.png){.inline}
  ![Run loop](images/animation/runloop.gif){.inline}

## Spine 动画

Spine 动画提供 2D _骨骼动画_ 支持 (详见 http://en.wikipedia.org/wiki/Skeletal_animation). 这是一种类似于剪裁动画的技术. 剪裁动画把对象分成各部分 (比如身体, 眼睛, 嘴巴之类的) 在每帧上独立运动. Spine 动画可以建立隐藏的, 树形关联的虚拟 _骨骼_. 骨架, 或称 _绑定_, 来为骨骼上添加的图片单独做动画. Defold 支持以 [Spine JSON 格式](http://esotericsoftware.com/spine-json-format) 输出的动画. Skeletal 动画都很平滑因为骨骼动画关键帧之间可以自动进行插值.

  关于导入 Spine 数据作为 Spine 模型和动画, 详见 [Spine 教程](/manuals/spine).

  ![Spine animation](images/animation/spine_animation.png){.inline}
  ![Run loop](images/animation/frog_runloop.gif){.inline}

## 3D 蒙皮动画

3D 模型的骨骼动画和 Spine 动画类似但是是针对于 3D 空间的. 3D 模型不是像剪裁动画那样先分成各个部分然后用骨骼连起来做动画. 而是使用骨骼精细控制模型上各个三角形如何移动.

  关于如何导入 3D 模型动画, 详情请见 [模型教程](/manuals/model).

  ![Blender animation](images/animation/blender_animation.png){.inline srcset="images/animation/blender_animation@2x.png 2x"}
  ![Wiggle loop](images/animation/suzanne.gif){.inline}

## 属性动画

数值类的属性 (numbers, vector3, vector4 和 quaterions) 以及着色器常量都可以由内置的属性动画系统制作属性动画, 即使用 `go.animate()` 函数. 引擎会在属性值之间进行 "补间" 依照指定的播放和缓动模式进行播放. 你也可以自定义缓动函数.

  ![Property animation](images/animation/property_animation.png){.inline srcset="images/animation/property_animation@2x.png 2x"}
  ![Bounce loop](images/animation/bounce.gif){.inline}

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

动画播放完成时可以提供一个回调函数. 如果动画是以 `ONCE_*` 模式播放, 播放完成后会调用这个回调函数.

## Spine model 动画

在 Spine 模型上播放动画, 只需调用 [`spine.play_anim()`](/ref/spine#spine.play_anim) 函数:

```lua
local function anim_done(self)
    -- 动画播放完成, 做其他事情...
end

function init(self)
    -- 在 "spinemodel" 组件上播放 "walk" 动画同时与上一个动画
    -- 在前 0.1 内混合, 然后进行回调.
    local anim_props = { blend_duration = 0.1 }
    spine.play_anim("#spinemodel", "run", go.PLAYBACK_LOOP_FORWARD, anim_props, anim_done)
end
```

![Spine model in game](images/animation/spine_ingame.png){srcset="images/animation/spine_ingame@2x.png 2x"}

如果动画是以 `go.PLAYBACK_ONCE_*` 模式播放, 然后在 `spine.play_anim()` 里指定回调函数, 则动画播放完成后会调用回调函数. 关于回调函数详见下文.

### Spine model - 播放头

除了 `spine.play_anim()` 还有更高级的方法, *Spine Model* 组件暴露了一个 "cursor" 属性可以通过 `go.animate()` 进行控制:

```lua
-- 设置 spine model 动画但是不播放.
spine.play_anim("#spinemodel", "run_right", go.PLAYBACK_NONE)

-- 设置播放头为 0
go.set("#spinemodel", "cursor", 0)

-- 基于 in-out quad 缓动慢慢对播放头进行从 0 到 1 的 pingpong 补间.
go.animate("#spinemodel", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 6)
```

::: 注意
补间和设置播放头时, 时间轴事件不会被触发.
:::

### Spine model - 骨骼层级

Spine 骨架的各个骨骼实例在游戏对象内展示出来. 在 Spine model 组件的 *Outline* 视图内, 可以看到完整的嵌套关系. 在此层级嵌套关系中你可以看到骨骼的名称和其所在的位置.

![Spine model hierarchy](images/animation/spine_bones.png){srcset="images/animation/spine_bones@2x.png 2x"}

通过骨骼名称, 就可以在运行时得到骨骼实例. 函数 [`spine.get_go()`](/ref/spine#spine.get_go) 返回指定骨骼的 id, 然后就可以用来进行设置父级之类的操作:

```lua
-- 把手枪绑定到英雄手上
local hand = spine.get_go("heroine#spinemodel", "front_hand")
msg.post("pistol", "set_parent", { parent_id = hand })
```

### Spine model - 时间轴事件

Spine 动画可以基于精确的时间触发事件. 对于需要做同步行为的功能非常有帮助, 例如播放走路声音, 场景粒子效果, 在骨骼层级上进行绑定和解绑或者实现你需要的其他功能.

在 Spine 软件里可以使用时间轴设置事件:

![Spine events](images/animation/spine_events.png)

各种事件由事件 id 表示 (上例中是 "bump") 而且时间轴上的事件可以包含一些数据:

Integer
: 整数值.

Float
: 浮点数值.

String
: 字符串值.

动画播放遇到事件时, `spine_event` 消息会被发回到调用 `spine.play()` 函数的脚本上. 消息数据参数就是事件附带的数据, 连同其他一些有用的数据:

`t`
: 自动画播放第一帧开始经过的时间.

`animation_id`
: 动画名, 哈希值.

`string`
: 事件附带字符串值, 哈希值.

`float`
: 事件附带浮点数值.

`integer`
: 事件附带整数值.

`event_id`
: 事件 id, 哈希值.

`blend_weight`
: 此时动画混合情况. 0 表示动画还没有被混合, 1 当前动画混合 100%.

```lua
-- Spine 动画包含与动画同步的音效.
-- 作为消息传到这里.
function on_message(self, message_id, message, sender)
  if message_id == hash("spine_event") and message.event_id == hash("play_sound") then
    -- 播放动画音效. 事件数据包括声音组件和声音增益.
    local url = msg.url("sounds")
    url.fragment = message.string
    sound.play(url, { gain = message.float })
  end
end
```

## 3D Model 动画

通过调用 [`model.play_anim()`](/ref/model#model.play_anim) 函数播放模型动画:

```lua
function init(self)
    -- 在 #model 上来回播放 "wiggle" 动画
    model.play_anim("#model", "wiggle", go.PLAYBACK_LOOP_PINGPONG)
end
```

::: 注意
Defold 目前只支持烘焙动画. 动画每个骨骼每一帧都要有矩阵数据, 而不是单独的位置, 旋转和缩放数据.

动画是线性插值的. 如果需要曲线插值动画要在输出时烘焙.

不支持 Collada 中的动画剪辑. 想要一个模型多个动画, 就要分别导出为 *.dae* 文件然后在 Defold 里组成 *.animationset* 文件.
:::

### 3D Model - 骨骼层级

模型骨骼作为游戏对象展示出来.

通过骨骼名称, 就可以在运行时得到骨骼实例. 函数 [`model.get_go()`](/ref/model#model.get_go) 返回指定骨骼的 id.

```lua
-- 得到 wiggler 模型的中央骨骼
local bone_go = model.get_go("#wiggler", "Bone_002")

-- 然后可以任意操作该游戏对象...
```

### 3D Model - 播放头

像 Spine 模型一样, 3D 模型也可以通过控制 `cursor` 属性播放动画:

```lua
-- 设置 #model 上的动画但不播放
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- 把播放头设置为动画起始位置
go.set("#model", "cursor", 0)
-- 基于 in-out quad 缓动对播放头进行从 0 到 1 的 pingpong 补间.
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## 属性动画

制作游戏对象或者组件的属性动画, 可以使用函数 `go.animate()`. 对于 GUI 节点属性, 可以使用函数 `gui.animate()`.

```lua
-- 设置 y 轴位置为 200
go.set(".", "position.y", 200)
-- 制作动画
go.animate(".", "position.y", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_OUTBOUNCE, 2)
```

停止某个属性的所有动画, 调用 `go.cancel_animations()`, 对于 GUI 节点, 调用 `gui.cancel_animation()`:

```lua
-- 停止当前游戏对象欧拉 z 轴旋转动画
go.cancel_animation(".", "euler.z")
```

如果取消组合属性的动画, 例如 `position`, 其所有子属性 (`position.x`, `position.y` 和 `position.z`) 动画也会一同取消.

[属性教程](/manuals/properties) 涵盖游戏对象, 组件和 GUI 节点的所有属性.

## GUI 节点属性动画

几乎所有 GUI 节点属性都可以制作动画. 比如说, 把一个节点的 `color` 设置成透明看不见然后制作属性动画到全白使其可见 (也就是没有染色).

```lua
local node = gui.get_node("button")
local color = gui.get_color(node)
-- 节点白色动画
gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_INOUTQUAD, 0.5)
-- 边框红色动画
gui.animate(node, "outline.x", 1, gui.EASING_INOUTQUAD, 0.5)
-- 位置延 x 轴移动 100 像素动画
gui.animate(node, hash("position.x"), 100, gui.EASING_INOUTQUAD, 0.5)
```

## 播放模式

动画可以单次播放也可以循环播放. 取决于播放模式:

* go.PLAYBACK_NONE
* go.PLAYBACK_ONCE_FORWARD
* go.PLAYBACK_ONCE_BACKWARD
* go.PLAYBACK_ONCE_PINGPONG
* go.PLAYBACK_LOOP_FORWARD
* go.PLAYBACK_LOOP_BACKWARD
* go.PLAYBACK_LOOP_PINGPONG

pingpong 模式先正向播放, 再反向播放. GUI 属性动画也有这些播放模式:

* gui.PLAYBACK_NONE
* gui.PLAYBACK_ONCE_FORWARD
* gui.PLAYBACK_ONCE_BACKWARD
* gui.PLAYBACK_ONCE_PINGPONG
* gui.PLAYBACK_LOOP_FORWARD
* gui.PLAYBACK_LOOP_BACKWARD
* gui.PLAYBACK_LOOP_PINGPONG

## 缓动

缓动决定动画基于时间的变化. 下面列出了内置的缓动函数.

以下可用于 `go.animate()` 函数:

|---|---|
| go.EASING_LINEAR | |
| go.EASING_INBACK | go.EASING_OUTBACK |
| go.EASING_INOUTBACK | go.EASING_OUTINBACK |
| go.EASING_INBOUNCE | go.EASING_OUTBOUNCE |
| go.EASING_INOUTBOUNCE | go.EASING_OUTINBOUNCE |
| go.EASING_INELASTIC | go.EASING_OUTELASTIC |
| go.EASING_INOUTELASTIC | go.EASING_OUTINELASTIC |
| go.EASING_INSINE | go.EASING_OUTSINE |
| go.EASING_INOUTSINE | go.EASING_OUTINSINE |
| go.EASING_INEXPO | go.EASING_OUTEXPO |
| go.EASING_INOUTEXPO | go.EASING_OUTINEXPO |
| go.EASING_INCIRC | go.EASING_OUTCIRC |
| go.EASING_INOUTCIRC | go.EASING_OUTINCIRC |
| go.EASING_INQUAD | go.EASING_OUTQUAD |
| go.EASING_INOUTQUAD | go.EASING_OUTINQUAD |
| go.EASING_INCUBIC | go.EASING_OUTCUBIC |
| go.EASING_INOUTCUBIC | go.EASING_OUTINCUBIC |
| go.EASING_INQUART | go.EASING_OUTQUART |
| go.EASING_INOUTQUART | go.EASING_OUTINQUART |
| go.EASING_INQUINT | go.EASING_OUTQUINT |
| go.EASING_INOUTQUINT | go.EASING_OUTINQUINT |

以下可用于 `gui.animate()` 函数:

|---|---|
| gui.EASING_LINEAR | |
| gui.EASING_INBACK | gui.EASING_OUTBACK |
| gui.EASING_INOUTBACK | gui.EASING_OUTINBACK |
| gui.EASING_INBOUNCE | gui.EASING_OUTBOUNCE |
| gui.EASING_INOUTBOUNCE | gui.EASING_OUTINBOUNCE |
| gui.EASING_INELASTIC | gui.EASING_OUTELASTIC |
| gui.EASING_INOUTELASTIC | gui.EASING_OUTINELASTIC |
| gui.EASING_INSINE | gui.EASING_OUTSINE |
| gui.EASING_INOUTSINE | gui.EASING_OUTINSINE |
| gui.EASING_INEXPO | gui.EASING_OUTEXPO |
| gui.EASING_INOUTEXPO | gui.EASING_OUTINEXPO |
| gui.EASING_INCIRC | gui.EASING_OUTCIRC |
| gui.EASING_INOUTCIRC | gui.EASING_OUTINCIRC |
| gui.EASING_INQUAD | gui.EASING_OUTQUAD |
| gui.EASING_INOUTQUAD | gui.EASING_OUTINQUAD |
| gui.EASING_INCUBIC | gui.EASING_OUTCUBIC |
| gui.EASING_INOUTCUBIC | gui.EASING_OUTINCUBIC |
| gui.EASING_INQUART | gui.EASING_OUTQUART |
| gui.EASING_INOUTQUART | gui.EASING_OUTINQUART |
| gui.EASING_INQUINT | gui.EASING_OUTQUINT |
| gui.EASING_INOUTQUINT | gui.EASING_OUTINQUINT |

<div id="game-container" class="game-container">
<canvas id="game-canvas" tabindex="1" width="640" height="512"></canvas>
<script src="//storage.googleapis.com/defold-doc/assets/easier/dmloader.js"></script>
<script>
  var extra_params = {
   archive_location_filter: function( path ) { return ('//storage.googleapis.com/defold-doc/assets/easier/archive' + path + ''); },
   splash_image: '//storage.googleapis.com/defold-doc/assets/easier/preview.jpg',
   custom_heap_size: 268435456,
   disable_context_menu: true,
   game_start: function() {}
  };
  Module['onRuntimeInitialized'] = function() { Module.runApp("game-canvas", extra_params); };
  Module['locateFile'] = function(path, scriptDirectory) {
   if (path == "dmengine.wasm" || path == "dmengine_release.wasm" || path == "dmengine_headless.wasm") { path = "easier.wasm"; }
   return scriptDirectory + path;
  };
  function load_engine() {
   var engineJS = document.createElement('script');
   engineJS.type = 'text/javascript';
   if (Module['isWASMSupported']) {
   engineJS.src = '//storage.googleapis.com/defold-doc/assets/easier/easier_wasm.js';
   } else {
   engineJS.src = '//storage.googleapis.com/defold-doc/assets/easier/easier_asmjs.js';
   }
   document.head.appendChild(engineJS);
  }
  load_engine();
</script>
</div>

![Linear interpolation](images/properties/easing_linear.png){.inline}
![In back](images/properties/easing_inback.png){.inline}
![Out back](images/properties/easing_outback.png){.inline}
![In-out back](images/properties/easing_inoutback.png){.inline}
![Out-in back](images/properties/easing_outinback.png){.inline}
![In bounce](images/properties/easing_inbounce.png){.inline}
![Out bounce](images/properties/easing_outbounce.png){.inline}
![In-out bounce](images/properties/easing_inoutbounce.png){.inline}
![Out-in bounce](images/properties/easing_outinbounce.png){.inline}
![In elastic](images/properties/easing_inelastic.png){.inline}
![Out elastic](images/properties/easing_outelastic.png){.inline}
![In-out elastic](images/properties/easing_inoutelastic.png){.inline}
![Out-in elastic](images/properties/easing_outinelastic.png){.inline}
![In sine](images/properties/easing_insine.png){.inline}
![Out sine](images/properties/easing_outsine.png){.inline}
![In-out sine](images/properties/easing_inoutsine.png){.inline}
![Out-in sine](images/properties/easing_outinsine.png){.inline}
![In exponential](images/properties/easing_inexpo.png){.inline}
![Out exponential](images/properties/easing_outexpo.png){.inline}
![In-out exponential](images/properties/easing_inoutexpo.png){.inline}
![Out-in exponential](images/properties/easing_outinexpo.png){.inline}
![In circlic](images/properties/easing_incirc.png){.inline}
![Out circlic](images/properties/easing_outcirc.png){.inline}
![In-out circlic](images/properties/easing_inoutcirc.png){.inline}
![Out-in circlic](images/properties/easing_outincirc.png){.inline}
![In quadratic](images/properties/easing_inquad.png){.inline}
![Out quadratic](images/properties/easing_outquad.png){.inline}
![In-out quadratic](images/properties/easing_inoutquad.png){.inline}
![Out-in quadratic](images/properties/easing_outinquad.png){.inline}
![In cubic](images/properties/easing_incubic.png){.inline}
![Out cubic](images/properties/easing_outcubic.png){.inline}
![In-out cubic](images/properties/easing_inoutcubic.png){.inline}
![Out-in cubic](images/properties/easing_outincubic.png){.inline}
![In quartic](images/properties/easing_inquart.png){.inline}
![Out quartic](images/properties/easing_outquart.png){.inline}
![In-out quartic](images/properties/easing_inoutquart.png){.inline}
![Out-in quartic](images/properties/easing_outinquart.png){.inline}
![In quintic](images/properties/easing_inquint.png){.inline}
![Out quintic](images/properties/easing_outquint.png){.inline}
![In-out quintic](images/properties/easing_inoutquint.png){.inline}
![Out-in quintic](images/properties/easing_outinquint.png){.inline}

## 自定义缓动

可以使用 `vector` 和其中的一系列值代替预置缓动函数. 矢量值从 (`0`) 过渡到 (`1`). 引擎会从矢量中取样并自动线性插值生成缓动曲线.

示例如下:

```lua
local values = { 0, 0.4, 0.2, 0.2, 0.5. 1 }
local my_easing = vmath.vector(values)
```

生成的缓动曲线如下:

![Custom curve](images/animation/custom_curve.png)

下面的例子是让游戏对象的 y 轴位置依照自定义曲线从当前位置到 200 来回跳跃:

```lua
local values = { 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1 }
local square_easing = vmath.vector(values)
go.animate("go", "position.y", go.PLAYBACK_LOOP_PINGPONG, 200, square_easing, 2.0)
```

![Square curve](images/animation/square_curve.png)

## 播放完成回调函数

所有动画函数 (`go.animate()`, `gui.animate()`, `gui.play_flipbook()`, `gui.play_spine_anim()`, `sprite.play_flipbook()`, `spine.play_anim()` 和 `model.play_anim()`) 可以在最后一个参数上传入Lua回调函数. 当动画播放完成时会调用这个函数. 对于循环动画, 和使用 `go.cancel_animations()` 手动取消播放的动画, 不会调用回调函数. 动画播放完成的回调函数里可以发送消息或者继续播放其他动画.

不同动画函数的回调函数参数有些许区别. 具体请参照动画函数的 API 文档.

```lua
local function done_bouncing(self, url, property)
    -- 动画播放完成. 进行各种处理...
end

function init(self)
    go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, 100, go.EASING_OUTBOUNCE, 2, 0, done_bouncing)
end
```
