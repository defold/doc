*Blend Mode* 属性定义了可视组件如何与其后面的图像混合. 以下列举了支持的混合模式及其混合算法:

Alpha
: 普通混合: `src.a * src.rgb + (1 - src.a) * dst.rgb`

Add
: 使用相应的 sprite 像素颜色值提亮背景: `src.rgb + dst.rgb`

Multiply
: 使用相应的 sprite 像素颜色值调暗背景: `src.rgb * dst.rgb`
