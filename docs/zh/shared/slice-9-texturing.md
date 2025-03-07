## 九宫格纹理

GUIs 对于其元素的大小改变是积极的: 面板和对话框总是应该填满其容纳的区域. 但是在缩放节点时纹理可能会产生问题.

通常, 引擎把纹理整个填充到方块节点的边界, 但是九宫格纹理可以指定纹理里的那些内容需要缩放:

![GUI 缩放](images/gui-box/scaling.png)

*九宫格* 方块节点包含4个像素数值分别代表左, 上, 右, 下有多少边缘不参与缩放:

![九宫格属性](images/gui-box/slice9_properties.png)

从左边开始, 顺时针设置:

![九宫格设置](images/gui-box/slice9.png)

- 角落部分不会被缩放.
- 边缘部分延单轴缩放. 左右边缘竖直缩放. 上下边缘水平缩放.
- 中央部分正常延两个轴缩放.

上述关于 *九宫格* 纹理缩放的描述仅在节点 size 改变时生效:

![GUI box node size](images/gui-box/slice9_size.png)

![Sprite size](../shared/images/sprite_slice9_size.png)

::: important
如果更改 sprite 或方块节点的缩放属性 (或者游戏对象自身的缩放属性) - sprite 或节点和纹理的缩放都不会带 *Slice9* 效果.
:::

::: important
要在 Sprite 上启用九宫格 [Sprite 图片的 Trim Mode](https://defold.com/manuals/atlas/#image-properties) 必须关闭.
:::


### Mipmaps 和 slice-9
因为渲染器里 mipmapping 的工作方式, 部分缩放纹理可能会造成小问题. 当你把纹理一部分 _缩小_ 到比本身小的时候. 渲染器会自动选择一个低分辨率的 mipmap 来渲染这部分, 导致了这个小问题.

![Slice 9 mipmapping](../shared/images/gui_slice9_mipmap.png)

为避免这类问题, 使用小图导进来之后只放大别缩小就行了.
