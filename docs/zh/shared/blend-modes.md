*Blend Mode* 属性定义了组件图形应如何与其后面的图形进行混合。以下是可用的混合模式及其计算方式：

Alpha
: 正常混合：`src.a * src.rgb + (1 - src.a) * dst.rgb`

Add
: 使用组件相应像素的颜色值提亮背景：`src.rgb + dst.rgb`

Multiply
: 使用组件相应像素的值调暗背景：`src.rgb * dst.rgb`

Screen
: Multiply 的相反操作。提亮背景和组件相应像素的值：`src.rgb - dst.rgb * dst.rgb`
