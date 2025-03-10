---
title: Defold 中的碰撞对象
brief: 碰撞对象是能给与游戏对象物理行为的组件. 碰撞对象包含许多物理属性和空间形状.
---

# 碰撞对象

碰撞对象是能给与游戏对象物理行为的组件. 碰撞对象包含许多物理属性比如重量, 弹性, 阻力等等. 组件上定义的一个或多个 _形状_ 决定了它在物理空间中的样子. Defold 支持以下的碰撞对象:

Static objects
: 静态对象不会移动但是能和移动物体进行碰撞. 静态对象很适合制作游戏固定场景元素 (比如地板和墙). 它们比动态对象性能消耗少. 静态对象不能被移动和修改.

Dynamic objects
: 动态对象由物理引擎负责计算位移. 处理碰撞然后给予力. 动态对象看起来很有真实感但是你 *不能* 直接控制它的位置与方向. 要想对其施加影响, 只能向它[施加力的作用](/ref/physics/#apply_force).

Kinematic objects
: 动画对象可以和其他对象产生碰撞, 但是物理引擎并不处理它们. 忽略碰撞, 或者交给你来处理. 动画对象很适合用作由脚本控制的又能对物理做出反应的物体, 比如游戏角色.

Triggers
: 触发器是记录碰撞的物体. 很适合用作碰撞检测 (比如子弹碰撞) 或者接触后触发时间的场景. 触发器比动画对象节省性能所以可以多用一些.


## 加入碰撞對象组件

碰撞对象组件包含一系列 *属性* 用以设定其类型和物理特性. 还包含一个或多个 *形状* 用以定义这个物体的物理形态.

在游戏对象上添加碰撞对象组件:

1. 在 *大綱* 視圖中, <kbd>右鍵點擊</kbd> 游戲對象然後在上下文菜單中選擇 <kbd>Add Component ▸ Collision Object</kbd>. 新添加的組件沒有形狀.
2. 在組件上 <kbd>右鍵點擊</kbd> 然後選擇 <kbd>Add Shape ▸ Box / Capsule / Sphere</kbd>. 來為組件添加形狀. 一個組件可以有多個形狀. 還可以使用瓷磚地圖或者凸多邊形頂點文件定義物理對象的形狀.
3. 可以使用移動, 旋轉, 縮放工具修改形狀.
4. 點選組件后可在 *大綱* 視圖中編輯其 *屬性*.

![Physics collision object](images/physics/collision_object.png)


## 加入碰撞形状

碰撞组件可包含多个简单形状或者一个复杂形状. 详见 [碰撞形状教程](/manuals/physics-shapes).


## 碰撞對象屬性

Id
: 组件名.

Collision Shape
: 这个是针对瓷砖地图的几何形状设置. 详见 [碰撞形状教程](/manuals/physics-shapes).

Type
: 碰撞对象的类型有: `Dynamic`, `Kinematic`, `Static` 和 `Trigger`. 如果设为动态就 _必须_ 设置其 *Mass* 属性为非0的值. 动态静态碰撞对象都需要为其设置适当的 *Friction* 和 *Restitution* 值.

Friction
: 摩擦可以做出一个物体在另一个物体上滑动的效果. 一般摩擦系数取值范围从 `0` (无摩擦---超级光滑) 到 `1` (强摩擦---超级粗糙) 之间. 但其实任何正数值都有效.

  摩擦力于法方向上的力成正比 (称为库伦摩擦). 计算两个物体 (`A` 和 `B`) 间的摩擦力时, 摩擦系数取两个物体的几何平均值:

```math
  F = sqrt( F_A * F_B )
```

  也就是说只要有一个物体是0摩擦的, 两个物体之间就不会有摩擦力.

Restitution
: 弹性是物体的 "反弹性能". 一般取值范围从 0 (非弹性碰撞—一点也不反弹) 到 1 (完全弹性碰撞---物体速度在碰撞后完全反向)

  两个物体 (`A` 和 `B`) 之间的弹性计算基于以下公式:

```math
  R = max( R_A, R_B )
```

  当一个形状发生多处碰撞时, 弹性模拟并不精确因为 Box2D 使用的是迭代解算器. Box2D 在碰撞相对速度很小时也使用非弹性碰撞代替, 以防止反弹抖动.

Linear damping
: 线性阻尼会减小刚体的线性速度. 不像摩擦只在物体接触时产生, 线性阻尼始终应用与线性移动的物体上, 给人一种物体飘进比空气密度大的环境中的感觉. 取值范围 0 到 1.

  Box2D 并不精确计算阻尼. 值很小时阻尼与时间无关, 值很大时阻尼随时间变化. 如果时间步固定, 这不会造成问题.

Angular damping
: 角阻尼与线性阻尼类似, 不同的是它减小的是刚体角速度. 取值范围 0 到 1.

Locked rotation
: 关闭碰撞对象的旋转, 无论力如何施加都不会旋转.

Bullet
: 开启此项将会在该碰撞物体和其他动态碰撞物体直接进行连续碰撞检测 (CCD). 如果一方碰撞物体不是 `Dynamic` 的, 则忽略该选项.

Group
: 此碰撞对象所归属的碰撞组. 可以自由定义16个组. 比如 "players", "bullets", "enemies" 或 "world". 如果瓷砖地图上设置了 *Collision Shape*, 则使用的是瓷砖图源里的组名而不是该属性定义的组名.

Mask
: 可以与此对象进行碰撞的 _组_. 如果指定多个, 组名以逗号分割. 如果值为空, 则此对象不与任何物体进行碰撞.


## 運行時屬性

可以使用 `go.get()` 和 `go.set()` 來存取物理對象的一系列屬性:

`angular_damping`
: 碰撞對象的旋轉阻尼 (`number`). [API reference](/ref/physics/#angular_damping).

`angular_velocity`
: 碰撞對象的旋轉速度 (`vector3`). [API reference](/ref/physics/#angular_velocity).

`linear_damping`
: 碰撞對象的綫性阻尼 (`number`). [API reference](/ref/physics/#linear_damping).

`linear_velocity`
: 碰撞對象的綫性速度 (`vector3`). [API reference](/ref/physics/#linear_velocity).

`mass`
: 碰撞對象的物理質量 (`number`). [API reference](/ref/physics/#mass).
