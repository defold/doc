组件用于赋予游戏对象特定的表达和/或功能。组件必须包含在游戏对象内部，并受包含该组件的游戏对象的位置、旋转和缩放的影响：

![Components](../shared/images/components.png)

许多组件具有可在运行时操作的特定属性，并且有特定于组件类型的函数可用于在运行时与它们交互：

```lua
-- 禁用 "can" 的 "body" 精灵
msg.post("can#body", "disable")

-- 1 秒后在 "bean" 上播放 "hoohoo" 声音
sound.play("bean#hoohoo", { delay = 1, gain = 0.5 } )
```

组件可以直接添加到游戏对象中，也可以作为组件文件的引用添加到游戏对象：

在 *Outline* 视图中<kbd>右键点击</kbd>游戏对象，然后选择 <kbd>Add Component</kbd>（原地添加）或 <kbd>Add Component File</kbd>（添加为文件引用）。

在大多数情况下，原地创建组件是最有意义的，但以下组件类型必须先创建为单独的资源文件，然后才能通过引用添加到游戏对象：

* 脚本 (Script)
* 图形用户界面 (GUI)
* 粒子效果 (Particle FX)
* 瓦片地图 (Tile Map)
