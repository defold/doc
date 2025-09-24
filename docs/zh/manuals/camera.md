---
title: 摄像机组件手册
brief: 本手册描述了Defold摄像机组件的功能.
---

# 摄像机

Defold中的摄像机是一种改变游戏世界视口和投影的组件。摄像机组件定义了一个基本的透视或正交摄像机，它为渲染脚本提供视图和投影矩阵。

透视摄像机通常用于3D游戏，其中摄像机的视图以及物体的大小和透视基于视锥体以及从摄像机到游戏中物体的距离和视角。

对于2D游戏，通常希望使用正交投影来渲染场景。这意味着摄像机的视图不再由视锥体决定，而是由一个立方体决定。正交投影是不现实的，因为它不会根据物体的距离改变物体的大小。一个1000单位远的物体将与摄像机正前方的物体以相同的大小渲染。

![projections](images/camera/projections.png)

## 创建摄像机

要创建摄像机，<kbd>右键点击</kbd>一个游戏对象并选择<kbd>Add Component ▸ Camera</kbd>。您也可以在项目层次结构中创建一个组件文件，并将该组件文件添加到游戏对象中。

![create camera component](images/camera/create.png)

摄像机组件具有以下定义摄像机*视锥体*的属性：

![camera settings](images/camera/settings.png)

Id
: 组件的ID

Aspect Ratio
: (**仅透视摄像机**) - 视锥体宽度和高度之间的比率。1.0表示您假设的是方形视图。1.33适用于4:3视图，如1024x768。1.78适用于16:9视图。如果设置了*自动宽高比*，则此设置将被忽略。

Fov
: (**仅透视摄像机**) - 以_弧度_表示的摄像机*垂直*视野。视野越宽，摄像机将看到的内容越多。

Near Z
: 近裁剪平面的Z值。

Far Z
: 远裁剪平面的Z值。

Auto Aspect Ratio
: (**仅透视摄像机**) - 设置此项以让摄像机自动计算宽高比。

Orthographic Projection
: 设置此项以将摄像机切换到正交投影（见下文）。

Orthographic Zoom
: (**仅正交摄像机**) - 用于正交投影的缩放（> 1 = 放大，< 1 = 缩小）。


## 使用摄像机

所有摄像机都会在帧期间自动启用和更新，并且lua `camera`模块在所有脚本上下文中都可用。自Defold 1.8.1起，不再需要通过向摄像机组件发送`acquire_camera_focus`消息来显式启用摄像机。旧的获取和释放消息仍然可用，但建议改为使用"enable"和"disable"消息，就像您希望启用或禁用的任何其他组件一样：

```lua
msg.post("#camera", "disable")
msg.post("#camera", "enable")
```

要列出所有当前可用的摄像机，您可以使用camera.get_cameras()：

```lua
-- 注意：渲染调用仅在渲染脚本中可用。
--       camera.get_cameras()函数可以在任何地方使用，
--       但render.set_camera只能在渲染脚本中使用。

for k,v in pairs(camera.get_cameras()) do
    -- 摄像机表包含所有摄像机的URL
    render.set_camera(v)
    -- 在这里进行渲染 - 这里渲染的任何使用指定了
    -- 视图和投影矩阵的材质的内容，都将使用来自摄像机的矩阵。
end
-- 要禁用摄像机，将nil（或根本不传递参数）传递给render.set_camera。
-- 此调用后，所有渲染调用将使用在渲染上下文中指定的
-- 视图和投影矩阵（render.set_view和render.set_projection）
render.set_camera()
```

脚本`camera`模块有多个可用于操作摄像机的函数。这里只是几个可以使用的函数，要查看所有可用函数，请查阅[API文档](/ref/camera/)中的手册。

```lua
camera.get_aspect_ratio(camera) -- 获取宽高比
camera.get_far_z(camera) -- 获取远z值
camera.get_fov(camera) -- 获取视野
camera.set_aspect_ratio(camera, ratio) -- 设置宽高比
camera.set_far_z(camera, far_z) -- 设置远z值
camera.set_near_z(camera, near_z) -- 设置近z值
... 等等
```

摄像机通过URL标识，它是组件的完整场景路径，包括集合、它所属的游戏对象和组件ID。在这个例子中，您将使用URL `/go#camera` 来从同一集合中标识摄像机组件，而在从不同集合或渲染脚本访问摄像机时使用 `main:/go#camera`。

![create camera component](images/camera/create.png)

```lua
-- 从同一集合中的脚本访问摄像机：
camera.get_fov("/go#camera")

-- 从不同集合中的脚本访问摄像机：
camera.get_fov("main:/go#camera")

-- 从渲染脚本访问摄像机：
render.set_camera("main:/go#camera")
```

每帧，当前具有摄像机焦点的摄像机组件将向"@render"套接字发送`set_view_projection`消息：

```lua
-- builtins/render/default.render_script
--
function on_message(self, message_id, message)
    if message_id == hash("set_view_projection") then
        self.view = message.view                    -- [1]
        self.projection = message.projection
    end
end
```
1. 从摄像机组件发布的消息包括一个视图矩阵和一个投影矩阵。

摄像机组件根据摄像机的*正交投影*属性为渲染脚本提供透视或正交投影矩阵。投影矩阵还考虑了定义的近和远裁剪平面、摄像机的视野和宽高比设置。

摄像机提供的视图矩阵定义了摄像机的位置和方向。具有*正交投影*的摄像机将视图居中在它所附加的游戏对象的位置上，而具有*透视投影*的摄像机将视图的左下角定位在它所附加的游戏对象上。


### 渲染脚本

从Defold 1.9.6开始，当使用默认渲染脚本时，Defold将自动设置应使用的最后启用的摄像机。在此更改之前，项目中的某个脚本需要显式地向渲染器发送`use_camera_projection`消息，以通知它应使用摄像机组件的视图和投影。这不再必要，但为了向后兼容性，仍然可以这样做。

或者，您可以在渲染脚本中设置应使用的特定摄像机。这在需要更具体控制应使用哪个摄像机进行渲染的情况下可能很有用，例如在多人游戏中。

```lua
-- render.set_camera将自动使用视图和投影矩阵
-- 用于任何渲染，直到调用render.set_camera()。
render.set_camera("main:/my_go#camera")
```

要检查摄像机是否处于活动状态，您可以使用[摄像机API](https://defold.com/ref/alpha/camera/#camera.get_enabled:camera)中的`get_enabled`函数：

```lua
if camera.get_enabled("main:/my_go#camera") then
    -- 摄像机已启用，使用它进行渲染！
    render.set_camera("main:/my_go#camera")
end
```

::: sidenote
要将`set_camera`函数与视锥体剔除一起使用，您需要将此作为选项传递给函数：
`render.set_camera("main:/my_go#camera", {use_frustum = true})`
:::

### 平移摄像机

您通过移动摄像机组件所附加到的游戏对象来在世界中平移/移动摄像机。摄像机组件将根据摄像机的当前x和y轴位置自动发送更新的视图矩阵。

### 缩放摄像机

使用透视摄像机时，您可以通过沿z轴移动摄像机所附加到的游戏对象来放大和缩小。摄像机组件将根据摄像机的当前z位置自动发送更新的视图矩阵。

使用正交摄像机时，您可以通过更改摄像机的*正交缩放*属性来放大和缩小：

```lua
go.set("#camera", "orthographic_zoom", 2)
```

### 自适应缩放

自适应缩放背后的概念是当显示分辨率从*game.project*中设置的初始分辨率改变时调整摄像机缩放值。

自适应缩放的两种常见方法是：

1. 最大缩放 - 计算一个缩放值，使得*game.project*中初始分辨率所覆盖的内容将填充并扩展到屏幕边界之外，可能会隐藏侧面或上方和下方的一些内容。
2. 最小缩放 - 计算一个缩放值，使得*game.project*中初始分辨率所覆盖的内容将完全包含在屏幕边界内，可能会在侧面或上方和下方显示额外内容。

示例：

```lua
local DISPLAY_WIDTH = sys.get_config_int("display.width")
local DISPLAY_HEIGHT = sys.get_config_int("display.height")

function init(self)
    local initial_zoom = go.get("#camera", "orthographic_zoom")
    local display_scale = window.get_display_scale()
    window.set_listener(function(self, event, data)
        if event == window.WINDOW_EVENT_RESIZED then
            local window_width = data.width
            local window_height = data.height
            local design_width = DISPLAY_WIDTH / initial_zoom
            local design_height = DISPLAY_HEIGHT / initial_zoom

            -- 最大缩放：确保初始设计尺寸将填充并扩展到屏幕边界之外
            local zoom = math.max(window_width / design_width, window_height / design_height) / display_scale

            -- 最小缩放：确保初始设计尺寸将缩小并包含在屏幕边界内
            --local zoom = math.min(window_width / design_width, window_height / design_height) / display_scale
            
            go.set("#camera", "orthographic_zoom", zoom)
        end
    end)
end
```

自适应缩放的完整示例可以在[此示例项目](https://github.com/defold/sample-adaptive-zoom)中看到。

### 跟随游戏对象

您可以通过将摄像机组件所附加到的游戏对象设置为要跟随的游戏对象的子对象来使摄像机跟随游戏对象：

![follow game object](images/camera/follow.png)

另一种方法是每帧更新摄像机组件所附加到的游戏对象的位置，随着要跟随的游戏对象移动。

### 将鼠标转换为世界坐标

当摄像机已经平移、缩放或将其投影从默认的正交Stretch投影更改时，`on_input()`生命周期函数中提供的鼠标坐标将不再与游戏对象的世界坐标匹配。您需要手动考虑视图或投影的变化。将鼠标/屏幕坐标转换为世界坐标的代码如下：

```Lua
--- 转换屏幕到世界坐标，考虑
-- 特定摄像机的视图和投影
-- @param camera 用于转换的摄像机URL
-- @param screen_x 要转换的屏幕x坐标
-- @param screen_y 要转换的屏幕y坐标
-- @param z 可选的z坐标以通过转换，默认为0
-- @return world_x 屏幕坐标的结果世界x坐标
-- @return world_y 屏幕坐标的结果世界y坐标
-- @return world_z 屏幕坐标的结果世界z坐标
function M.screen_to_world(camera, screen_x, screen_y, z)
    local projection = go.get(camera, "projection")
    local view = go.get(camera, "view")
    local w, h = window.get_size()

    -- https://defold.com/manuals/camera/#converting-mouse-to-world-coordinates
    local inv = vmath.inv(projection * view)
    local x = (2 * screen_x / w) - 1
    local y = (2 * screen_y / h) - 1
    local x1 = x * inv.m00 + y * inv.m01 + z * inv.m02 + inv.m03
    local y1 = x * inv.m10 + y * inv.m11 + z * inv.m12 + inv.m13
    return x1, y1, z or 0
end
```

请记住，来自`on_input()`的值`action.screen_x`和`action.screen_y`应该用作此函数的参数。访问[示例页面](https://defold.com/examples/render/screen_to_world/)以查看屏幕到世界坐标转换的实际操作。还有一个[示例项目](https://github.com/defold/sample-screen-to-world-coordinates/)展示了如何进行屏幕到世界坐标的转换。

::: sidenote
[本手册中提到的第三方摄像机解决方案](/manuals/camera/#third-party-camera-solutions)提供了用于屏幕坐标之间转换的函数。
:::

## 运行时操作
您可以通过多种不同的消息和属性在运行时操作摄像机（请参阅[API文档以了解用法](/ref/camera/)）。

摄像机有许多不同的属性可以使用`go.get()`和`go.set()`进行操作：

`fov`
: 摄像机视野（`number`）。

`near_z`
: 摄像机近Z值（`number`）。

`far_z`
: 摄像机远Z值（`number`）。

`orthographic_zoom`
: 正交摄像机缩放（`number`）。

`aspect_ratio`
: Defold 1.4.8中添加。视锥体宽度和高度之间的比率。用于计算透视摄像机的投影。（`number`）。

`view`
: Defold 1.4.8中添加。摄像机的计算视图矩阵。只读。（`matrix4`）。

`projection`
: Defold 1.4.8中添加。摄像机的计算投影矩阵。只读。（`matrix4`）。


## 第三方摄像机解决方案

有社区制作的摄像机解决方案实现了常见功能，如屏幕抖动、跟随游戏对象、屏幕到世界坐标转换等等。它们可以从Defold资产门户下载：

- [正交摄像机](https://defold.com/assets/orthographic/)（仅2D）由Björn Ritzl开发。
- [Defold Rendy](https://defold.com/assets/defold-rendy/)（2D和3D）由Klayton Kowalski开发。