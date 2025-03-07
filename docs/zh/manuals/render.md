---
title: Defold 中的渲染过程
brief: 本教程介绍了 Defold 的渲染流程及其编程方法.
---

# 渲染

引擎在屏幕上显示的每个对象：精灵,模型,图块,粒子或GUI节点均由渲染器绘制.渲染器的核心是控制渲染流程的渲染脚本.默认情况下,每个2D均使用指定混合和正确Z深度来进行绘制-因此,除了顺序和简单混合之外您可能不需要了解渲染.对于大多数2D游戏,默认流程功能良好,但是您的游戏可能有特殊要求.在这种情况下,Defold允许您编写量身定制的渲染程序.

### 渲染管线是什么东东?

渲染管线决定了渲染什么, 何时渲染以及渲染哪里. 渲染什么由 [渲染优先级](#render-predicates) 决定. 什么时候渲染由 [渲染脚本](#the-render-script) 决定, 渲染哪里由 [视口映射](#default-view-projection) 决定. 渲染管线还能剔除基于渲染优先级所渲染的的那些位于边界框或视锥体之外的图像. 这个过程称为视锥体剔除.


## 默认渲染器

渲染文件保存有当前渲染脚本的引用, 还确定了该渲染脚本可以使用的材质 (使用 [`render.enable_material()`](/ref/render/#render.enable_material) 函数)

渲染管线的核心就是 _渲染脚本_. 它是包含 `init()`, `update()` 与 `on_message()` 函数的 Lua 脚本, 主要用于与 OpenGL 渲染 API 的底层交互. 渲染脚本生命周期有其特殊之处. 详情请见 [应用生命周期教程](/manuals/application-lifecycle).

在 "Builtins" 文件夹中放有默认渲染器资源文件 ("default.render") 和默认渲染脚本 ("default.render_script").

![Builtin render](images/render/builtin.png)

使用自定义渲染器:

1. 把 "default.render" 和 "default.render_script" 复制到项目目录某个位置. 当然自己从头开始写也没问题, 但是拷贝出来能有个参考, 尤其是对于 Defold 或 OpenGL ES 渲染编写的新手来说.

2. 编辑 "default.render" 文件, 指定 *Script* 项为自定义的脚本.

3. 在 *game.project* 的 *bootstrap* 部分里的 *Render* 项上设置刚才修改好的 "default.render" 文件.


## 渲染优先级

可视对象的渲染顺序, 是基于渲染 _优先级_ 的. 优先级的确定基于材质 _标签_.

可是对象都有材质用以确定如何在屏幕上进行绘制. 材质之中, 可以指定一个或多个 _标签_ 与材质相对应.

在你的渲染脚本中, 你可以创建一组 *渲染优先级* 然后指定什么标签归于那个优先级. 当你告诉引擎渲染它们的时候, 每个材质里包含该优先级的所有标签的对象会被渲染.

```
Sprite 1        Sprite 2        Sprite 3        Sprite 4
Material A      Material A      Material B      Material C
  outlined        outlined        greyscale       outlined
  tree            tree            tree            house
```

```lua
-- 一个优先级对应所有标签为 "tree" 的 sprites
local trees = render.predicate({"tree"})
-- 渲染 Sprite 1, 2 和 3
render.draw(trees)

-- 一个优先级对应所有标签为 "outlined" 的 sprites
local outlined = render.predicate({"outlined"})
-- 渲染 Sprite 1, 2 和 4
render.draw(outlined)

-- 一个优先级对应所有包含标签为 "outlined" 的且包含标签为 "tree" 的 sprites
local outlined_trees = render.predicate({"outlined", "tree"})
-- 渲染 Sprite 1 和 2
render.draw(outlined_trees)
```

关于材质详情请见 [材质教程](/manuals/material).


## 默认视口映射

默认渲染脚本使用2D游戏常用的平视透视. 填充方式有三种: `Stretch` (默认), `Fixed Fit` 和 `Fixed`. 除了默认渲染脚本使用的平时透视之外, 还可以使用摄像机组件提供的透视矩阵.

### Stretch

无论应用窗口怎样改变, 渲染视口大小总是等于在 *game.project* 里面设置的分辨率. 所以一旦宽高比例改变, 就会造成视口拉伸现象:

![Stretch projection](images/render/stretch_projection.png)

*原窗口大小*

![Stretch projection when resized](images/render/stretch_projection_resized.png)

*横向拉伸*

视口拉伸是默认选项, 其对应命令脚本是:

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

### Fixed Fit 映射

跟 Stretch 一样 Fixed Fit 也是使用 *game.project* 里设置的分辨率, 不同的是一旦窗口大小改变游戏内容会缩放但是始终保持原比例, 这样一来本来不应被渲染的内容也可能会被显示出来:

![Fixed fit projection](images/render/fixed_fit_projection.png)

*原窗口大小*

![Fixed fit projection when resized](images/render/fixed_fit_projection_resized.png)

*横向拉伸*

![Fixed fit projection when smaller](images/render/fixed_fit_projection_resized_smaller.png)

*窗体缩小一半*

等比缩放对应命令脚本是:

```lua
msg.post("@render:", "use_fixed_fit_projection", { near = -1, far = 1 })
```

### Fixed 映射

以一个固定倍数按比例缩放视口. 也就是说倍数不是 100% 的话就会自行多显示或少显示内容, 而不按照 *game.project* 的设定分辨率渲染:

![Fixed projection](images/render/fixed_projection_zoom_2_0.png)

*缩放倍数为2*

![Fixed projection](images/render/fixed_projection_zoom_0_5.png)

*缩放倍数为0.5*

![Fixed projection](images/render/fixed_projection_zoom_2_0_resized.png)

*缩放倍数为2窗体缩小一半*

其对应命令脚本是:

```lua
msg.post("@render:", "use_fixed_projection", { near = -1, far = 1, zoom = 2 })
```

### 摄像机透视

还可以使用 [摄像机组件](/manuals/camera)提供的透视矩阵. 用以下代码开启摄像机透视:

```lua
msg.post("@render:", "use_camera_projection")
```


## 视锥体剔除

Defold 的渲染 API 能让开发者做到叫做视锥体剔除的功能. 视锥体剔除能忽视位于定义好的边界框之外或者视锥体之外的图像. 在超大游戏世界中每次只显示其中一部分, 视锥体剔除能极大地减少发送给 GPU 的待渲染数据, 从而提高了效率并节省了电量 (移动设备中). 常见用摄像机视口和透视映射来创建边界框. 默认渲染脚本使用视口和透视映射 (来自摄像机) 的数据计算出视锥体.

视锥体剔除在引擎里的实现基于组件类型. 目前的状况是 (Defold 1.9.0):

| 组件          | 是否支持  |
|-------------|-------|
| Sprite      | 是     |
| Model       | 是     |
| Mesh        | 是 (1) |
| Label       | 是     |
| Spine       | 是     |
| Particle fx | 否     |
| Tilemap     | 是    |
| Rive        | 否    |

1 = Mesh 的边界框需要开发者手动设置. [详情请见](/manuals/mesh/#frustum-culling).


## 坐标系统

提到渲染就不得不说其基于的坐标系统. 一般游戏都有世界坐标系和屏幕坐标系.

GUI 组件节点基于屏幕坐标系渲染, 屏幕左下角是坐标原点 (0,0) 右上角是最大值 (screen width, screen height). 游戏和摄像机如何改变都不会改变屏幕坐标系. 这样就能保证用户界面不受游戏世界的影响.

Sprite, 瓷砖地图和其他游戏组件都是使用游戏世界坐标系. 既不改变渲染脚本又不使用摄像机组件改变映射方式的话游戏世界坐标系和屏幕坐标系数值上是相同的, 但是一旦视口移动或者映射方式改变, 两者就会偏离. 摄像机移动时屏幕坐标原点 (0, 0) 会跟着改变. 映射方式改变原点和偏移量都会由于缩放系数而改变.


## 渲染脚本

下面展示一个对默认渲染脚本稍经修改的版本.

init()
: 函数 `init()` 用来设定优先级, 视口和视口颜色. 这些渲染时都会被用到.

```lua
function init(self)
  -- 定义渲染优先级. 每个优先级的绘制不相干所以绘制时可以任意修改 OpenGL 的状态.
    self.predicates = create_predicates("tile", "gui", "text", "particle", "model")

    -- 创建和填充数据表将在 update() 中使用
    local state = create_state()
    self.state = state
    local camera_world = create_camera(state, "camera_world", true)
    init_camera(camera_world, get_stretch_projection)
    local camera_gui = create_camera(state, "camera_gui")
    init_camera(camera_gui, get_gui_projection)
    update_state(state)
end
```

update()
: 函数 `update()` 每帧都会被调用. 用于调用底层 OpenGL ES API (OpenGL 嵌入系统 API) 以实现渲染. 想了解 `update()` 函数, 先要了解 OpenGL 工作原理. 对于 OpenGL ES 有许多教程. 官方网站就是个不错的学习之地. 参考 https://www.khronos.org/opengles/

  本例中函数里设置了渲染 3D 模型必须的两部分内容. `init()` 定义了 `self.predicates.model` 优先级. 含有 "model" 标签的材质被建立. 以及使用此材质的模型组件:

```lua
function update(self)
    local state = self.state
     if not state.valid then
        if not update_state(state) then
            return
        end
    end

    local predicates = self.predicates
    -- clear screen buffers
    --
    render.set_depth_mask(true)
    render.set_stencil_mask(0xff)
    render.clear(state.clear_buffers)

    local camera_world = state.cameras.camera_world
    render.set_viewport(0, 0, state.window_width, state.window_height)
    render.set_view(camera_world.view)
    render.set_projection(camera_world.proj)


    -- render models
    --
    render.set_blend_func(render.BLEND_SRC_ALPHA, render.BLEND_ONE_MINUS_SRC_ALPHA)
    render.enable_state(render.STATE_CULL_FACE)
    render.enable_state(render.STATE_DEPTH_TEST)
    render.set_depth_mask(true)
    render.draw(predicates.model_pred)
    render.set_depth_mask(false)
    render.disable_state(render.STATE_DEPTH_TEST)
    render.disable_state(render.STATE_CULL_FACE)

     -- render world (sprites, tilemaps, particles etc)
     --
    render.set_blend_func(render.BLEND_SRC_ALPHA, render.BLEND_ONE_MINUS_SRC_ALPHA)
    render.enable_state(render.STATE_DEPTH_TEST)
    render.enable_state(render.STATE_STENCIL_TEST)
    render.enable_state(render.STATE_BLEND)
    render.draw(predicates.tile)
    render.draw(predicates.particle)
    render.disable_state(render.STATE_STENCIL_TEST)
    render.disable_state(render.STATE_DEPTH_TEST)

    -- debug
    render.draw_debug3d()

    -- render GUI
    --
    local camera_gui = state.cameras.camera_gui
    render.set_view(camera_gui.view)
    render.set_projection(camera_gui.proj)
    render.enable_state(render.STATE_STENCIL_TEST)
    render.draw(predicates.gui, camera_gui.frustum)
    render.draw(predicates.text, camera_gui.frustum)
    render.disable_state(render.STATE_STENCIL_TEST)
end
```

上面是一个简单版的渲染脚本. 每帧工作都一样. 然而有些时候需要对不同的游戏状态进行不同的渲染操作. 可能还需要与游戏代码脚本进行交互.

on_message()
: 渲染脚本有一个 `on_message()` 函数用来接收游戏其他脚本发来的消息. 典型的例子比如 _摄像机_. 摄像机组件每一帧都把视口和映射发给渲染脚本. 消息名为 `"set_view_projection"`:

```lua
local MSG_CLEAR_COLOR =         hash("clear_color")
local MSG_WINDOW_RESIZED =      hash("window_resized")
local MSG_SET_VIEW_PROJ =       hash("set_view_projection")

function on_message(self, message_id, message)
  if message_id == MSG_CLEAR_COLOR then
      -- 根据消息命令清空屏幕.
      self.clear_color = message.color
  elseif message_id == MSG_SET_VIEW_PROJ then
      -- 焦点摄像机每一帧都发送 set_view_projection
      -- 消息到 @render 端口. 使用摄像机发来的数据可以
      -- 设置渲染视口 (及映射).
      camera.view = message.view
      self.camera_projection = message.projection or vmath.matrix4()
      update_camera(camera, state)
  end
end
```

GUI 脚本同样可以向 `@render` 端口发送消息:

```lua
-- 更改清屏颜色.
msg.post("@render:", "clear_color", { color = vmath.vector4(0.3, 0.4, 0.5, 0) })
```

## 渲染资源
要将某些引擎资源传入渲染脚本, 你可以把它们添加进项目 .render 文件里的 `Render Resoures` 表里:

![Render resources](images/render/render_resources.png)

在渲染脚本里使用这些资源:

```lua
-- "my_material" 现在将用于优先级关联的所有绘制调用
render.enable_material("my_material")
-- 谓词绘制的任何内容都将以 "my_render_target" 结尾
render.set_render_target("my_render_target")
render.draw(self.my_full_screen_predicate)
render.set_render_target(render.RENDER_TARGET_DEFAULT)
render.disable_material()

-- 将渲染目标结果纹理绑定到通过优先级渲染的任何内容
render.enable_texture(0, "my_render_target", render.BUFFER_COLOR0_BIT)
render.draw(self.my_tile_predicate)
```

::: sidenote
Defold 目前仅支持 `Materials` 和 `Render Targets` 作为引用的渲染资源, 但后续会加入支持更多资源类型.
:::

## 纹理句柄

Defold 中的纹理在内部表示为一个句柄, 这实质上等同于一个数字, 该数字应该唯一地标识引擎中任何位置的纹理对象. 这意味着你可以通过在渲染系统和游戏对象脚本之间传递这些句柄来桥接游戏对象世界和渲染世界. 比如, 脚本可以在附加到游戏对象的脚本中动态创建纹理, 并将其发送到渲染器, 以用作绘制命令中的全局纹理.

在 `.script` 文件中:

```lua
local my_texture_resource = resource.create_texture("/my_texture.texture", tparams)
-- 注意: my_texture_resource 是资源路径的哈希值, 不能用作句柄!
local my_texture_handle = resource.get_texture_info(my_texture_resource)
-- my_texture_handle 包含纹理的信息, 比如宽度, 高度等等
-- 它还包含句柄, 这就是我们所需要的
msg.post("@render:", "set_texture", { handle = my_texture_handle.handle })
```

In a .render_script file:

```lua
function on_message(self, message_id, message)
    if message_id == hash("set_texture") then
        self.my_texture = message.handle
    end
end

function update(self)
    -- 将自定义纹理绑定到绘制状态
    render.enable_texture(0, self.my_texture)
    -- 进行绘制..
end
```

::: sidenote
目前无法更改资源应指向的纹理, 你只能在渲染脚本中使用这样的原始句柄.
:::

## 受支持的图像 API
Defold 渲染脚本 API 把渲染操作转换为如下图像 API:

:[Graphics API](../shared/graphics-api.md)


## 系统消息

`"set_view_projection"`
: 焦点摄像机发给渲染脚本的消息.

`"window_resized"`
: 窗体大小变化时系统发送给渲染脚本的消息. 监听此消息以便在窗体大小变化时采取相应的渲染方案. 桌面设备窗口大小改变和移动设备屏幕方向改变都会触发此消息发送.

```lua
local MSG_WINDOW_RESIZED =      hash("window_resized")
  
function on_message(self, message_id, message)
  if message_id == MSG_WINDOW_RESIZED then
    -- 窗体变化. message.width 与 message.height 保存了变化后的窗体尺寸.
  ...
  end
end
```

`"draw_line"`
: 调试用画线. 可以用来检查射线, 向量等等. 线的绘制调用了 `render.draw_debug3d()` 函数.

```lua
-- 绘制白线
local p1 = vmath.vector3(0, 0, 0)
local p2 = vmath.vector3(1000, 1000, 0)
local col = vmath.vector4(1, 1, 1, 1)
msg.post("@render:", "draw_line", { start_point = p1, end_point = p2, color = col } )  
```

`"draw_text"`
: 调试用文字绘制. 可以用来展示一些调试信息. 文字使用自带 "always_on_top.font" 字体. 使用材质标签 "debug_text" 于渲染脚本里进行绘制.

```lua
-- 文字信息绘制
local pos = vmath.vector3(500, 500, 0)
msg.post("@render:", "draw_text", { text = "Hello world!", position = pos })  
```

可视分析器通过发送 `"toggle_profile"` 消息到 `@system` 端口显示出来, 它不是在渲染脚本里进行绘制的, 而是在系统内部其他脚本里进行绘制的.


## Draw call 与合批

Draw call 众所周知是调用 GPU 使用指定材质和纹理以及各种参数设置进行一次屏幕渲染的过程. 这个过程比较耗时所以游戏 draw call 数量应该尽可能地小. 可以使用 [内置分析器](/manuals/profiling/) 来查看 draw call 数量与耗时.

Defold 基于下列规则自动进行合批渲染操作以达到减少 draw call 的目的. 其中 GUI 组件与其他组件类型的规则不同.


### 非 GUI 组件合批

渲染基于Z轴位置, 从小到大进行. 引擎会将物体按照Z轴位置由小到大排序. 如果一个物体遇到以下情形, 就把当前物体与上一个物体打包合批在一个 draw call 中渲染:

* 属于同一个集合代理
* 属于同一种组件类型 (都是 sprite, particle fx, tilemap 等等)
* 使用同一个纹理 (图集或者瓷砖图源)
* 使用同一个材质
* 使用同一个材质参数值 (例如 tint)

注意两个物体要满足上述全部条件才能进行合批操作.


### GUI 组件合批

GUI 组件按照节点树从上到下进行渲染. 如果一个节点遇到以下情形, 就把当前节点与上一个节点打包合批在一个 draw call 中渲染:

* 属于同一种组件类型 (都是 box, text, pie 等等)
* 使用同一个纹理 (图集或者瓷砖图源)
* 使用同一种混合模式.
* 使用同一个字体 (仅针对文本节点)
* 使用同样的绘制参数

::: sidenote
节点按组件逐个渲染. 也就是说不同 GUI 组件的节点不会合批.
:::

节点树直观的反映用户界面节点的关系. 但是这种树形结构有可能会打破合批. 树形结构下 GUI 要使节点高效渲染推荐使用 GUI 层. 关于层的使用及其对合批的影响详见 [GUI 教程](/manuals/gui#layers-and-draw-calls).
