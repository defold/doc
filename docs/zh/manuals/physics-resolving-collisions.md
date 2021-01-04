---
title: Defold 中的碰撞处理
brief: 本教程介绍了动画物理对象的碰撞处理方法.
---

# 處理动画碰撞

对于动画碰撞对象的碰撞必须手动处理. 一个想当然的处理方法如下:

```lua
function on_message(self, message_id, message, sender)
  -- 处理碰撞
  if message_id == hash("contact_point_response") then
    local newpos = go.get_position() + message.normal * message.distance
    go.set_position(newpos)
  end
end
```

动画碰撞对象的确离开了碰撞穿透, 但是分离之后经常会过冲, 这在许多情况下会产生抖动. 为了便于理解, 想象游戏主角碰到了两个物体, *A* 和 *B*:

![Physics collision](images/physics/collision_multi.png){srcset="images/physics/collision_multi@2x.png 2x"}

碰撞发生的那一帧里, 物理引擎发出多个 `"contact_point_response"` 消息, 一个给 *A* 一个给 *B*. 如果按上面那样移动角色, 结果会是这样:

- 根据 *A* 的穿透距离把角色向上移 (黑色箭头)
- 根据 *B* 的穿透距离把角色向左上移 (黑色箭头)

顺序无所谓结果是一样的: 最终位移是 *每个穿透向量的矢量和*:

![Physics separation naive](images/physics/separation_naive.png){srcset="images/physics/separation_naive@2x.png 2x"}

要想正确地将角色移出 *A* 和 *B*, 需要处理碰撞点的穿透距离并检测上一个位移是否, 完全或部分, 分离了它们.

假设第一次碰撞从 *A* 开始, 然后针对 *A* 做位移:

![Physics separation step 1](images/physics/separation_step1.png){srcset="images/physics/separation_step1@2x.png 2x"}

这样一来角色也部分离开了 *B*. 最后只剩下 *B* 黑色箭头那点穿透. 这段位移应该是 *A* 向量映射到 *B* 剩余的补偿:

![Projection](images/physics/projection.png){srcset="images/physics/projection@2x.png 2x"}

$$l = vmath.project(A, B) \times vmath.length(B)$$

补偿向量等于 *B* 向量减去 *l* 向量. 所以计算位移的时候, 对于每个碰撞点, 可以引入矫正向量按以下步骤进行矫正:

1. 把当前矫正向量映射到碰撞穿透向量上.
2. 计算穿透向量的补偿 (按照上述公式).
3. 依照补偿向量移动对象.
4. 把补偿向量累加到矫正向量中.

完整的代码实现如下:

```lua
function init(self)
  -- 校正向量
  self.correction = vmath.vector3()
end

function update(self, dt)
  -- 重置矫正向量
  self.correction = vmath.vector3()
end

function on_message(self, message_id, message, sender)
  -- 处理碰撞
  if message_id == hash("contact_point_response") then
    -- 获取位移计算所需数据. 
    -- 当前帧可能有多个碰撞点需要处理,
    -- 通过累积矫正向量,
    -- 达到正确计算位移的目的:
    if message.distance > 0 then
      -- 第一步, 把矫正向量投射到
      -- 穿透向量上.
      local proj = vmath.project(self.correction, message.normal * message.distance)
      if proj < 1 then
        -- 没有过冲的才需要补偿.
        local comp = (message.distance - message.distance * proj) * message.normal
        -- 应用补偿向量.
        go.set_position(go.get_position() + comp)
        -- 积累矫正向量.
        self.correction = self.correction + comp
      end
    end
  end
end
```
