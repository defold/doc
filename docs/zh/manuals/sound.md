---
title: Defold 中的声音
brief: 本教程介绍了如果把声音带入 Defold 项目, 进行播放和控制.
---

# 声音

Defold 支持声音但是不那么强大. 要注意两个概念:

声音组件
: 实际包含声音播放声音的组件.

声音组
: 每个声音组件在设计上都属于一个 _组_. 组比单独控制声音组件更方便. 比如, 建立一个 "sound_fx" 组可以调用一次函数关闭其中所有声音.

## 创建声音组件

声音组件只能在游戏对象里创建. 创建好游戏对象, 在其上面右键点击选择 <kbd>Add Component ▸ Sound</kbd> 然后点击 *OK*.

![Select component](images/sound/sound_add_component.jpg)

声音组件有一系列属性可以设置:

![Select component](images/sound/sound_properties.png)

*Sound*
: 从项目中选择一个声音文件. 文件需要 _Wave_ 或者 _Ogg Vorbis_ 格式. Defold 支持 16bit 位深和 44100 采样率的声音文件.

*Looping*
: 开启此选项声音会循环播放除非循環次數達到 _Loopcount_ 或者手动停止.

*Loopcount*
: 停止前要循環播放的次數 (0 表示除非手動停止否則永遠循環).

*Group*
: 声音属于的组. 如果置空, 此声音默认归属 "master" 组.

*Gain*
: 声音增益. 可以在这里直接设置声音增益而不用从声音软件再导出. 增益算法见下文.

*Pan*
: 声音生像. 范围从 -1 (左 -45 度) 到 1 (右 45 度).

*Speed*
: 声音速度. 一般速度为 1.0, 0.5 是半倍速 2.0 是二倍速.


## 播放声音

设置好声音属性之后, 可以通过调用 [`sound.play()`](/ref/sound/#sound.play:url-[play_properties]-[complete_function]) 函数播放声音:

```lua
sound.play("go#sound", {delay = 1, gain = 0.5, pan = -1.0, speed = 1.25})
```

::: 注意
即使声音组件所在游戏对象被删除了, 声音也会继续播放. 可以通过调用 [`sound.stop()`](/ref/sound/#sound.stop:url) 函数停止播放 (见下文).
:::
只要发送消息到声音组件都会造成新声音实例的播放, 直到声音缓存满溢引擎报错. 所以建议自己实现一个控制或者分组机制.

## 停止播放声音

可以通过调用 [`sound.stop()`](/ref/sound/#sound.stop:url) 函数停止播放声音:

```lua
sound.stop("go#sound")
```

## 增益

![Gain](images/sound/sound_gain.png)

声音系统有 4 级增益:

- 声音组件增益属性设置.
- 调用 `sound.play()` 函数或者直接调用 `sound.set_gain()` 函数设置的增益.
- 调用 [`sound.set_group_gain()`](/ref/sound#sound.set_group_gain) 函数设置的增益.
- "master" 组上设置的增益. 可以通过调用 `sound.set_group_gain(hash("master"))` 函数修改设置.

结果是4级增益的乘积. 默认每个增益都是 1.0 (0 dB).

## 声音组

在声音组件上设置组名就把这个声音归到了那个组里. 如果不设置组名默认归到 "master" 组里. 设置组名为 "master" 效果相同.

有一系列函数用于获得声音组, 声音名, 获得/设置增益, 均方根 (见 http://en.wikipedia.org/wiki/Root_mean_square) 和峰值. 还有一个函数用于检测设备播放器是否正在运行:

```lua
-- 如果 iPhone/Android 设备的播放器正在播放引用, 则所有游戏声音静音
if sound.is_music_playing() then
    for i, group_hash in ipairs(sound.get_groups()) do
        sound.set_group_gain(group_hash, 0)
    end
end
```

组名是个哈希值. 其字符串值可以使用 [`sound.get_group_name()`](/ref/sound#sound.get_group_name) 获得, 可以用来显示音轨名称.

![Sound group mixer](images/sound/sound_mixer.png)

::: 注意
代码里不要依赖字符串组名因为编译后不保存字符串组名.
:::

所有值都是线性 0 到 1.0 (0 dB) 的范围. 要转换为分贝数, 可使用标准转换公式:

$$
db = 20 \times \log \left( gain \right)
$$

```lua
for i, group_hash in ipairs(sound.get_groups()) do
    -- 字符串组名只在调试时可用. 发布后会变成 "unknown_*".
    local name = sound.get_group_name(group_hash)
    local gain = sound.get_group_gain(group_hash)

    -- 转换为分贝.
    local db = 20 * math.log10(gain)

    -- 得到 RMS (增益均方根). 左右声道分开计算.
    local left_rms, right_rms = sound.get_rms(group_hash, 2048 / 65536.0)
    left_rmsdb = 20 * math.log10(left_rms)
    right_rmsdb = 20 * math.log10(right_rms)

    -- 得到峰值. 左右声道分开计算.
    left_peak, right_peak = sound.get_peak(group_hash, 2048 * 10 / 65536.0)
    left_peakdb = 20 * math.log10(left_peak)
    right_peakdb = 20 * math.log10(right_peak)
end

-- 设置主声道增益为 +6 dB (math.pow(10, 6/20)).
sound.set_group_gain("master", 1.995)
```

## 控制声音

如果用什么事件来触发声音播放, 就有可能造成同时播放2个或多个重复的声音. 这样的话, 声音会产生 _偏移重叠_ 现象效果非常不好.

![Phase shift](images/sound/sound_phase_shift.png)

最简单的办法是设置一个过滤时间段对最近播放过的声音进行过滤:

```lua
-- 在一定 "过滤时间段" 内不允许再次播放同一声音.
local gate_time = 0.3

function init(self)
    -- 把计时器保存到一个表里然后每帧计时递减
    -- 直到过了 "过滤时间段". 再删除它.
    self.sounds = {}
end

function update(self, dt)
    -- 计时器递减
    for k,_ in pairs(self.sounds) do
        self.sounds[k] = self.sounds[k] - dt
        if self.sounds[k] < 0 then
            self.sounds[k] = nil
        end
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("play_gated_sound") then
        -- 表里没有才能播放.
        if self.sounds[message.soundcomponent] == nil then
            -- 保存计时器
            self.sounds[message.soundcomponent] = gate_time
            -- 播放声音
            sound.play(message.soundcomponent, { gain = message.gain })
        else
            -- 过滤表里有的声音
            print("gated " .. message.soundcomponent)
        end
    end
end
```

这样, 只要把 `play_gated_sound` 消息连同增益发送给声音组件. 使用 `sound.play()` 播放函数前就会对声音进行过滤:

```lua
msg.post("/sound_gate#script", "play_gated_sound", { soundcomponent = "/sounds#explosion1", gain = 1.0 })
```

::: 注意
对于 `play_sound` 消息没法过滤因为该消息由 Defold 引擎内部保留. 如果使用引擎保留消息名会造成运行不正确.
:::


## 运行时控制
可以通关一些列属性在运行时控制声音 (用法参见 [API](/ref/sound/)). 以下属性可以使用 `go.get()` 和 `go.set()` 来进行操作:

`gain`
: 声音组件音量 (`number`).

`pan`
: 声音组件角度 (`number`). 取值从 -1 (向左-45度) 到 1 (向右45度).

`speed`
: 声音组件速度 (`number`). 取值 1.0 为一般速度, 0.5 半速, 2.0 两倍速.

`sound`
: 声音资源路径 (`hash`). 可以使用 `resource.set_sound(path, buffer)` 来变更声音资源. 例如:

```lua
local boom = sys.load_resource("/sounds/boom.wav")
local path = go.get("#sound", "sound")
resource.set_sound(path, boom)
```


## 相关项目配置

在 *game.project* 文件里有些关于声音组件的 [设置项目](/manuals/project-settings#sound).
