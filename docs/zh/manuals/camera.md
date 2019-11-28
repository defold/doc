---
title: 摄像机组件教程
brief: 本教程介绍了 Defold 摄像机组件的功能.
---

# 摄像机

Defold 的摄像机组件控制游戏世界的视口与映射. 摄像机组件定义了透视和平视的视口与映射矩阵用于渲染脚本进行渲染. 透视摄像机一般服务于 3D 游戏, 平视摄像机一般服务员 2D 游戏. 如果需要摄像机追随, 缩放, 震动之类的功能需要自己来实现 (可以参考下面的 [第三方摄像机解决方案](https://www.defold.com/manuals/camera/#third-party-camera-solutions)).

## 创建摄像机

要创建摄像机, 在游戏对象上 <kbd>右键点击</kbd> 选择 <kbd>Add Component ▸ Camera</kbd>. 或者先创建组件文件再链接到游戏对象上.

![create camera component](images/camera/create.png){srcset="images/camera/create@2x.png 2x"}

摄像机有以下属性用以建立 *视锥* (透视摄像机可用):

![camera settings](images/camera/settings.png){srcset="images/camera/settings@2x.png 2x"}

Id
: 组件id

Aspect Ratio
: (**透视摄像机可用**) - 视锥宽高比. 1.0 代表正方形视口.  4:3 显示器 1024x768 这样的分辨率用 1.33. 16:9 的显示器用 1.78. 如果设置了 *Auto Aspect Ratio* 则此属性无效.

Fov
: (**透视摄像机可用**) - 以 _弧度_ 表示的摄像机 *垂直* 视域. 视域越宽, 摄像机看到的内容越多. 注意目前默认值 (45) 有点误导. 要 45 度的视域, 要设置值为 0.785 ($\pi / 4$).

Near Z
: (**透视摄像机可用**) - 近端裁剪平面z值.

Far Z
: (**透视摄像机可用**) - 远端裁剪平面z值.

Auto Aspect Ratio
: (**透视摄像机可用**) - 自动设置宽高比.

## 使用摄像机

通过发送 acquire_camera_focus 消息, 激活摄像机并填充视口同时向渲染脚本提供映射矩阵:

```lua
msg.post("#camera", "acquire_camera_focus")
```

被激活的摄像机, 会在每一帧向 "@render" 接口发送 `"set_view_projection"` 消息, 也就是说渲染脚本会接收此消息:

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
1. 这个消息中包含一个视口矩阵和一个映射矩阵.

### 摄像机平移

平移摄像机所在游戏对象就相当于平移摄像机. 摄像机会根据当前x和y坐标更新视口矩阵.

### 摄像机缩放

延 z 轴移动透视摄像机所在游戏对象就相当于缩放摄像机. 摄像机会根据当前z坐标更新视口矩阵.

对于平视摄像机只有将其映射类型设置为 `Fixed` 才可以进行视口缩放, 此时要向 "@render" 接口发送缩放等级进行视口缩放:

```Lua
msg.post("@render:", "use_fixed_projection", { zoom = 2, near = -1, far = 1 })
```

### 摄像机跟随

把摄像机对象放在要跟随的游戏对象子级就能实现摄像机跟随:

![follow game object](images/camera/follow.png)

或者自己写脚本每帧更新摄像机位置也可以.

### 鼠标位置转换为世界坐标

摄像机平移缩放后 on_input() 函数提供的鼠标位置就不再与世界坐标匹配了. 此时需要进行手动矫正. 默认渲染脚本里把鼠标/屏幕坐标转换为世界坐标的代码如下:

::: 注意
[本教程第三方摄像机解决方案部分](/manuals/camera/#第三方摄像机解决方案) 提供了坐标转换方法.
:::

```Lua
-- builtins/render/default.render_script
--
local function screen_to_world(x, y, z)
	local inv = vmath.inv(self.projection * self.view)
	x = (2 * x / render.get_width()) - 1
	y = (2 * y / render.get_height()) - 1
	z = (2 * z) - 1
	local x1 = x * inv.m00 + y * inv.m01 + z * inv.m02 + inv.m03
	local y1 = x * inv.m10 + y * inv.m11 + z * inv.m12 + inv.m13
	local z1 = x * inv.m20 + y * inv.m21 + z * inv.m22 + inv.m23
	return x1, y1, z1
end
```

## 映射

摄像机提供了用于透视映射的渲染脚本. 非常适合 3D 游戏. 对于 2D 游戏, 通常使用的是 *平视映射*. 这种摄像机的视口不是视锥, 而是方盒. 平视口没有近大远小. 同样大小的东西无论离摄像机远还是近映射出来都一样大.

![projections](images/camera/projections.png){srcset="images/camera/projections@2x.png 2x"}

### 平视映射 (2D)
平视映射的渲染脚本不采用摄像机发来的映射矩阵自己实现渲染算法. 默认提供三种适配方式: `Stretch`, `Fixed` 和 `Fixed Fit`. 可以通过发送消息设置适配方式:

```lua
msg.post("@render:", "use_fixed_fit_projection", { near = -1, far = 1 })
```

::: 注意
消息里近远端裁剪平面深度还是需要的. 但是摄像机属性里的近远端裁剪平面设置只在透视摄像机里有效.
:::

::: 注意
平时摄像机渲染视口的左下角对应摄像机所在游戏对象的位置.
:::

渲染脚本及适配方式详情请见 [渲染手册](/manuals/render/#默认视口映射).

### 透视映射 (3D)
透视映射渲染脚本采用摄像机发来的视口与映射矩阵信息实现渲染. 通过发送如下消息使渲染脚本使用来自摄像机的映射信息:

```lua
msg.post("@render:", "use_camera_projection")
```

渲染脚本详情请见 [渲染手册](/manuals/render/#透视映射).


## 第三方摄像机解决方案

有一些第三方库实现了诸如游戏对象跟随, 坐标转换等摄像机功能. 可以在 Defold 社区资源库找到:

- [Rendercam](https://defold.com/assets/rendercam/) (2D 和 3D) 由 Ross Grams 开发.
- [Ortographic camera](https://defold.com/assets/orthographic/) (仅 2D) 由 Björn Ritzl 开发.
