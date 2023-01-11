---
title: Defold 游戏优化
brief: 本教程介绍了如何优化 Defold 应用的包体和性能.
---

# Defold 游戏优化
开发时就要考虑游戏在目标平台上的运行和优化. 需要考虑以下几个方面:

* 应用大小
* 运行速度
* 内存占用
* 耗电情况

## 应用大小优化
Defold 编译和打包时建立了一个依赖树. 编译系统从 *game.project* 文件指定的启动集合开始检查每个被引用的集合, 游戏对象及组件需要的资源. 这些被依赖的资源才会最终被导入包内. 没被引用的被排除在包外. 即使这样开发者还应该考虑包内资源空间占用情况. 有些平台与发布渠道限制了应用包体大小:

* Apple 和 Google 规定了设备使用移动网络 (而不是 Wifi) 下载应用的大小限制.
  * 2019 年夏 Google Play 限制 100 MB, Apple App Store 限制 150 MB.
* Facebook 建议 Facebook Instant Game 要在 5 秒内最好是 3 秒内启动.
  * 这虽然没有直接规定大小, 我们讨论认为大小应该限制在 20 MB 以内.
* Playable ads 基于广告商网络一般限制在 2 到 5 MB.

:::注意
根据 2017 年一项研究表明 "APK 文件大小每增加 6 MB, 安装率就会相应降低 1%." ([source](https://medium.com/googleplaydev/shrinking-apks-growing-installs-5d3fcba23ce2))
:::

为了更好的分析包体空间占用可以在编译时 [生成编译报告](/manuals/bundling/#编译报告). 通常声音和图片占游戏空间最大部分.

### 缩减引擎
可以使用 [application manifest 文件](https://defold.com/manuals/project-settings/#app-manifest) 去掉引擎中不需要的功能. 比如游戏不用物理效果就去掉物理引擎. 使用 [Manifestation 在线工具](https://britzl.github.io/manifestation/) 可以方便配置和生成这个文件.

### 声音优化
Defold 支持 .ogg 和 .wav 文件其中 .ogg 一般用于音乐 .wav 一般用于音效. Sounds 必须是 16-bit 采样率 44100 所以编码前就要对其做好优化. 可以使用第三方软件降低音质或者把 .wav 转换成 .ogg.

### 图片优化
对游戏的图片优化有几种办法, 首先要做的就是检查图集和瓷砖图源内容图片的大小. 导入的图片尺寸不要超过游戏所需大小. 导入大图片再缩小使用是现存资源的浪费. 可以使用第三方图片编辑器先把图片修改成所需大小. 对于背景图之类的有时可以导入小图片再放大使用. 小图改好了还要考虑图集和瓷砖图源本身的大小. 不同平台和显示硬件的纹理尺寸限制可能不一样.

::: sidenote
[这个帖子](https://forum.defold.com/t/texture-management-in-defold/8921/17?u=britzl) 在使用脚本与第三方软件修改图片大小的方面给出了许多建议.
:::

* HTML5 游戏最大纹理: https://webglstats.com/webgl/parameter/MAX_TEXTURE_SIZE
* iOS 游戏最大纹理:
  * iPad: 2048x2048
  * iPhone 4: 2048x2048
  * iPad 2, 3, Mini, Air, Pro: 4096x4096
  * iPhone 4s, 5, 6+, 6s: 4096x4096
* Android 各不相同但是新设备基本都支持 4096x4096.

如果图集太大就需要切分成小图集或者使用 texture profile 缩小整个图集. Defold 的 texture profile 系统不但可以缩小图集还可以通过应用压缩算法减小图集占用空间. 详见 [纹理档教程](/manuals/texture-profiles/).

::: sidenote
优化和管理纹理可以参考 [这个帖子](https://forum.defold.com/t/texture-management-in-defold/8921).
:::

### 排除内容按需下载
另一个减小包体的办法是打包时把部分内容排除在外, 需要时再下载. 一开始被排除的东西可以是锁住的关卡, 未激活的角色, 皮肤, 武器或者是车辆. Defold 提供了叫做热更新的按需下载内容的方案. 详情请见 [热更新教程](/manuals/live-update/).


## 应用运行速度优化
你要知道游戏运行效率瓶颈在哪才能进行优化. 每帧的什么操作最耗时间? 与渲染有关吗? 与游戏逻辑有关吗? 与场景图有关吗? 建议使用内置的分析工具分析这些事情. 使用 [屏幕或者网页分析器](/manuals/profiling/) 对游戏进行采样再分析哪里应该优化. 发现最耗时的操作就找到了优化方向.

### 减少脚本运行时间
如果分析工具指出 `Script` 部分耗时太多. 当然每帧运行脚本越少越好. 要是 `update()` 和 `on_input()` 里面代码太多很可能影响每帧运行性能, 尤其是对于低端设备. 一些建议是:

#### 代码有效率
用回调别用轮询. 引擎提供的功能别自己手动实现 (比如用 go.animate 别用手动实现动画等等).

#### 减少垃圾回收
每帧创建大量临时 Lua 表之类的对象会激发 Lua 的垃圾回收机制. 垃圾回收可能会造成卡一下. 尽可能重用表别在循环里创建很多表.

#### 预哈希消息与行为id
如果要处理很多消息处理很多输入的话推荐把字符串提前哈希保存. 比如如下代码:

```
function on_message(self, message_id, message, sender)
    if message_id == hash("message1") then
        msg.post(sender, hash("message3"))
    elseif message_id == hash("message2") then
        msg.post(sender, hash("message4"))
    end
end
```

这样每次接收消息都要调用很多哈希函数. 预先把哈希字符串保存起来就可以提高效率:

```
local MESSAGE1 = hash("message1")
local MESSAGE2 = hash("message2")
local MESSAGE3 = hash("message3")
local MESSAGE4 = hash("message4")

function on_message(self, message_id, message, sender)
    if message_id == MESSAGE1 then
        msg.post(sender, MESSAGE3)
    elseif message_id == MESSAGE2 then
        msg.post(sender, MESSAGE4)
    end
end
```

#### Prefer and cache URLs
定位一个游戏对象和组件可以使用它的 id 的字符串或者哈希或者 URL. 字符串和哈希在内部被转换成 URL. 对于经常要使用的 URL 建议预先保存, 利于提高性能. 如下例:

```
    local pos = go.get_position("enemy")
    local pos = go.get_position(hash("enemy"))
    local pos = go.get_position(msg.url("enemy"))
    -- 处理位置变量
```

以上三个定位 id 都是 `enemy`. 第一第二行 id (字符串或哈希) 使用前会转换为 URL. 所以预先保存 URL 在需要时使用就能提高效率:

```
    function init(self)
        self.enemy_url = msg.url("enemy")
    end

    function update(self, dt)
        local pos = go.get_position(self.enemy_url)
        -- 处理位置变量
    end
```

### 减少渲染一帧的时间
分析工具可以在 `Render` 和 `Render Script` 部分指明哪些渲染耗时较长. 考虑以下方面来改善渲染耗时:

* 减少 draw calls - 减少 draw call 可以参考 [这个帖子](https://forum.defold.com/t/draw-calls-and-defold/4674)
* 减少 overdraw
* 减少 着色器复杂度 - 对于 GLSL 优化可以参考 [Kronos 的这个文章](https://www.khronos.org/opengl/wiki/GLSL_Optimizations). 还可以修改 Defold 的默认着色器 (位于 `builtins/materials`) 或者针对低端设备降低着色器精确度. 所有着色器都使用 `highp` 精确度, 如果改成 `mediump` 可能会提升一些性能.

### 降低场景图复杂度
如果分析器指出 `GameObject` 部分, 尤其是 `UpdateTransform` 取样耗时较高就需要进行一定的优化. 方法如下:

* 剔除 - 如果游戏对象不可见, 关闭游戏对象 (及其组件). 基于游戏类型采取不同方法. 对于 2D 游戏视口内看不到的东西都可以关闭. 可以使用物理 trigger 进行检测或者把所有东西分为若干组群分别检测. 碰到需要关闭或者开启的情况就向游戏对象发送 `disable` 或者 `enable` 消息即可.


## 优化内存使用
此部分教程未完成. 讨论涵盖以下方面:

* [纹理压缩](/manuals/texture-profiles/)
* [动态加载集合](https://www.defold.com/manuals/collection-proxy/)
* [动态加载工厂资源](https://www.defold.com/manuals/collection-factory/#dynamic-loading-of-factory-resources)
* [性能分析](/manuals/profiling/)


## 优化耗电
此部分教程未完成. 讨论涵盖以下方面:

* 每帧的脚本运行
* 手机的加速度计
* [性能分析](/manuals/profiling/)
