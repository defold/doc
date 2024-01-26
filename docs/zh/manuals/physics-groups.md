---
title: Defold 中的碰撞组
brief: 物理引擎使用组来划分物理对象碰撞双方.
---

# 碰撞组与碰撞掩码

物理引擎通过组与掩码处理碰撞. 这个组就是 _碰撞组_. 每个碰撞对象都有2个属性用以控制其与其他物体的碰撞, *Group* 和 *Mask*.

碰撞只发生在两个物体所处的组分别被包含在对方的 *碰撞掩码* 之中的情况下.

![Physics collision group](images/physics/collision_group.png){srcset="images/physics/collision_group@2x.png 2x"}

*掩码* 可包含多个组名, 以实现复杂的碰撞控制.

## 碰撞检测
当组码掩码都相匹配两个碰撞对象接触时, 游戏引擎就会发出 [碰撞消息](/manuals/physics-messages) 作为响应.
