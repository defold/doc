---
title: Defold 中的射线投射
brief: 射线投射用于沿线性射线读取物理世界。本手册解释了其工作原理。
---

## 射线投射

射线投射用于沿线性射线读取物理世界。要将射线投射到物理世界中，您需要提供起始和结束位置以及[一组碰撞组](/manuals/physics-groups)来进行测试。

如果射线击中物理对象，您将获得有关它击中的对象的信息。射线与动态、运动学和静态对象相交。它们不与触发器交互。

```lua
function update(self, dt)
  -- 请求射线投射
  local my_start = vmath.vector3(0, 0, 0)
  local my_end = vmath.vector3(100, 1000, 1000)
  local my_groups = { hash("my_group1"), hash("my_group2") }

  local result = physics.raycast(my_start, my_end, my_groups)
  if result then
      -- 对命中做出反应（所有值请参见 'ray_cast_response' 消息）
      print(result.id)
  end
end
```

::: sidenote
射线投射将忽略包含射线起始点的碰撞对象。这是 Box2D 中的一个限制。
:::
