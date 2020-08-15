*Blend Mode* 属性定义了可视组件如何与其后面的图像混合. 以下列举了支持的混合模式及其混合算法:

Alpha
: 普通混合: a~0~ * rgb~0~ + (1 - a~0~) * rgb~1~

Add
: 使用相应的 sprite 像素颜色值提亮背景: rgb~0~ + rgb~1~

Add Alpha (废弃!)
: 使用相应的可见 sprite 像素颜色值提亮背景: a~0~ * rgb~0~ + rgb~1~

Multiply
: 使用相应的 sprite 像素颜色值调暗背景: rgb~0~ * rgb~1~
