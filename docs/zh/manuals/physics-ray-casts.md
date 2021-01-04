---
title: Defold 中的物理投射
brief: 投射用于收集延一条投射射线所遇到的物理世界的物体. 本教程介绍了其用法.
---

## 投射

投射用于收集延一条投射射线所遇到的物理世界的物体. 只要提供起止点和 [碰撞组](/manuals/physics-groups) , 就可以投射射线了.

射线碰到的物体数据都会被记录下来. 包括动态, 静态和动画碰撞对象. 不包括触发器对象.


```lua
function update(self, dt)
  -- 投射射线
  local my_start = vmath.vector3(0, 0, 0)
  local my_end = vmath.vector3(100, 1000, 1000)
  local my_groups = { hash("my_group1"), hash("my_group2") }

  local result = physics.raycast(my_start, my_end, my_groups)
  if result then
      -- 处理射线碰撞结果 (所有数据参见 'ray_cast_response' 消息)
      print(result.id)
  end
end
```

::: 注意
结果不包括射线起始点位置的碰撞物体. 这是 Box2D 做的限制.
:::
