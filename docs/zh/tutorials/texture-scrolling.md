---
title: 纹理滚动着色器
brief: 在本教程中，你将学习如何使用着色器来滚动重复纹理。
---

致谢：本教程由论坛用户MasterMind贡献（[原论坛帖子](https://forum.defold.com/t/texture-scrolling-shader-tutorial-example/71553)）。

# 纹理滚动着色器教程

通过着色器滚动纹理是许多着色器效果中的基本技术。让我们来制作一个！使用[示例项目](https://github.com/FlexYourBrain/Texture_Scrolling_Example)来跟随并亲自尝试。将要使用的方法是在着色器中使用常量进行UV偏移。

对于那些想要查看这个简短教程/指南结果的人，还可以在itch.io上查看[示例项目的演示](https://flexyourbrain.itch.io/texture-scrolling-in-defold)：

## 设置

项目设置如下：

* 一个细分的3D平面（.dae），将用于显示滚动的纹理。
* 一个分配了3D平面（.dae文件）的模型组件。
* 两个64x64的纹理图像（`water_bg.png`和`water_wave.png`），创建为无缝平铺，在.model属性中分配。
* 一个分配给平面模型的着色器（材质+顶点程序+片段程序）。
* 一个在材质和着色器中设置的常量。
* 一个附加到模型游戏对象的脚本组件，用于启动动画循环。

![](images/texture-scrolling/model_setup.png)

_注意：`water_bg`分配给`tex0`插槽，`water_wave`设置到`tex1`插槽。在下面显示的材质采样器属性中分配了两个采样器插槽。_

![](images/texture-scrolling/material_setup.png)

_当前`tex1`将是滚动的纹理，因此Wrap U & V设置为Repeat。_

这就是基本设置，现在我们可以继续处理`water_scroll.vp`（顶点）和`water_scroll.fp`（片段）程序。你可以在上图中看到这些被设置到材质中。

## 着色器代码

如果可以避免，最好在片段程序中避免进行过多的计算，所以我们在顶点程序中计算UV偏移，然后再将坐标发送到片段程序。我们还在材质中创建了一个类型为user的常量"animation_time"（如上所示）。该常量是一个向量4，但我们只使用第一个值。如果我们把这个向量4表示为`vector4(x,y,z,w)`，我们将在着色器中只使用x值，如下所示。


```glsl
// water_scroll.vp

// UV / 纹理滚动
attribute highp vec4 position;
attribute mediump vec2 texcoord0;

uniform mediump mat4 mtx_worldview;
uniform mediump mat4 mtx_proj;
uniform mediump vec4 animation_time; // 在材质中设置为类型user的顶点常量。

varying mediump vec2 var_texcoord0; // 设置变量纹理坐标0
varying mediump vec2 var_texcoord1; // 设置变量纹理坐标1

void main()
{
    vec4 p = mtx_worldview * vec4(position.xyz, 1.0);
    var_texcoord0 = texcoord0;
    var_texcoord1 = vec2(texcoord0.x - animation_time.x, texcoord0.y); // 计算变量纹理坐标1在U(x)轴上的UV偏移，发送到片段程序
    gl_Position = mtx_proj * p;
}
```

模型提供了属性`texcoord0`，这是我们的纹理UV坐标。我们声明了名为animation_time的`vec4` uniform，还有两个`vec2` varying变量`var_texcoord0`和`var_texcoord1`，我们在`void main()`中为它们分配属性UV坐标`texcoord0`后将它们传递给片段程序。正如你所见，`var_texcoord1`是不同的，因为我们在发送到片段程序之前对其进行了偏移。分配一个`vec2`，这样我们可以根据需要将`animation_time`分别分配给x和y。在这种情况下，我们只取`texcoord0.x`并减去我们的常量`animation_time.x`，当动画化时，这将在负U轴（水平向左）上偏移，我们设置`texcoord0.y`以保持其属性位置。


```glsl
// water_scroll.fp

varying mediump vec2 var_texcoord0; // 变量纹理坐标0与water_bg采样器一起使用
varying mediump vec2 var_texcoord1; // 变量纹理坐标1与water_waves采样器一起使用，UV动画计算在顶点程序中完成

uniform lowp sampler2D tex0; // 材质采样器插槽0 = 水背景 / 在plane.model中设置
uniform lowp sampler2D tex1; // 材质采样器插槽1 = 水波纹 / 在plane.model中设置

void main()
{
    vec4 water_bg = texture2D(tex0, var_texcoord0.xy);
    vec4 water_waves = texture2D(tex1, var_texcoord1.xy);
    
    gl_FragColor = vec4(water_bg.rgb + water_waves.rgb ,1.0); // 使用加法(+)将纹理波纹添加到背景，alpha设置为1.0，因为没有使用透明度
}
```

现在到片段程序，我们有一个简单的设置。两个"in" varying `vec2`变量，我们从顶点程序发送的`var_textcoord0`和`var_texcoord1`，然后我们为我们在模型和材质中设置的采样器纹理提供uniform，它们被命名为`tex0`和`tex1`。然后在`void main()`中，我们创建向量4来使用`texture2d()`分配给我们的纹理，图像是RGBA（红、绿、蓝、alpha）通道格式。我们分配采样器名称，然后是我们希望它们使用的纹理坐标。正如你在上图中看到的，"water_waves"分配了`var_texcoord1`。这是我们正在动画化/滚动的纹理，而分配给`water_bg`的`var_texcoord0`我们保持原样。对于全局保留变量`gl_FragColor`，这是像素颜色被分配的地方，使用相同的`vec4(r,g,b,a)`格式。我们想要将两个纹理组合在一起，所以我们使用加法将每个纹理的rgb通道混合在一起，此外我们没有使用纹理的alpha通道，所以我们分配一个1.0的浮点值，这等于完全不透明。


## 着色器动画脚本

```lua
-- animate_shader.script
local animate = 1.0
-- local float将用于设置滚动材质中的animation_time常量，着色器中只使用x常量值
-- 所以没有必要创建向量4

function init(self)
    go.animate("/scroll#plane", "animation_time.x", go.PLAYBACK_LOOP_FORWARD, animate, go.EASING_LINEAR, 4.0)
end
```

动画化常量值的方法不止一种，如果你愿意，可以在渲染脚本或普通脚本中计算时间步长并使用这些值更新常量。在这种情况下，我们只动画化一个着色器，如果你想要在几个着色器中有一个时间步长，在`update()`中计算可能更理想。然而我们将使用`go.animate()`，因为我们可以使用很多功能。使用`go.animate()`，我们可以只使用"animation_time.x"来动画化我们常量的x值。如果我们选择，我们还可以使用持续时间、延迟和缓动。我们还可以设置播放为循环或播放一次，并在需要时取消动画。这些在动画化我们的着色器时都非常方便。

`local animate`浮点数1.0是我们在"animation_time.x"中动画化的目标值。在着色器中，我们大多处理标准化的浮点值0.0到1.0。注意材质中我们的`animation_time`的默认常量值是(0,0,0,0)，我们正在将第一个零从0.0动画化到1.0。这意味着我们的偏移UV坐标将动画化到边缘，然后一次又一次地循环，这正是我们想要的！

## 下一步

作为练习，你可以尝试在相反方向动画化`water_bg`纹理坐标，就像示例演示中一样！

希望这对你有帮助。如果你制作了滚动的效果，请分享！

/ MasterMind