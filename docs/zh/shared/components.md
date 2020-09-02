组件是用来给与游戏对象各种功能与表现的程序. 组件位于游戏对象之下, 游戏对象受控于组件:

![Components](../shared/images/components.png){srcset="../shared/images/components@2x.png 2x"}

许多组件含有某些属性是可以在运行时控制的, 根据组件属性的不同类型, 调用交换的函数也不一样:

```lua
-- 关闭 "body" 精灵
msg.post("can#body", "disable")

-- 1 秒以后在 "bean" 上播放 "hoohoo" 声音
sound.play("bean#hoohoo", { delay = 1, gain = 0.5 } )
```

组件要么直接依附于游戏对象, 要么作为一个文件被游戏对象引用:

<kbd>右键点击</kbd> *Outline* 视图里的游戏对象, 选择 <kbd>Add Component</kbd> (直接依附) 或者 <kbd>Add Component File</kbd> (引用文件).

一般认为直接依附就够了, 但是以下组件类型必须保存为各种不同的文件以便被游戏对象引用:

* Script
* GUI
* Particle FX
* Tile Map
