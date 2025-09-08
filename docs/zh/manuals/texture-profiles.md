---
title: Defold 中的纹理配置文件
brief: Defold 支持自动纹理处理和图像数据压缩。本手册介绍了可用的功能。
---

# 纹理配置文件

Defold 支持自动纹理处理和图像数据压缩（用于*图集*、*瓦片图源*、*立方体贴图*以及用于模型、GUI等的独立纹理）。

有两种压缩类型，软件图像压缩和硬件纹理压缩。

1. 软件压缩（如PNG和JPEG）减少了图像资源的存储大小。这使得最终打包大小更小。然而，当图像文件读入内存时需要解压，因此即使图像在磁盘上很小，它也可能占用大量内存空间。

2. 硬件纹理压缩也减少了图像资源的存储大小。但是，与软件压缩不同，它减少了纹理的内存占用。这是因为图形硬件能够直接管理压缩纹理，而无需先解压它们。

纹理的处理通过特定的纹理配置文件进行配置。在此文件中，您可以创建_配置文件_，表达在为特定平台创建包时应使用哪种压缩格式和类型。然后，_配置文件_与匹配的文件_路径模式_绑定，允许精细控制项目中哪些文件应该被压缩以及如何压缩。

由于所有可用的硬件纹理压缩都是有损的，您的纹理数据将会出现伪影。这些伪影高度依赖于您的源材料外观以及使用的压缩方法。您应该测试您的源材料并进行实验以获得最佳结果。Google是您的好帮手。

您可以选择在包存档中对最终纹理数据（压缩或原始）应用哪种软件图像压缩。Defold支持[Basis Universal](https://github.com/BinomialLLC/basis_universal)和[ASTC](https://www.khronos.org/opengl/wiki/ASTC_Texture_Compression)压缩格式。

::: sidenote
压缩是资源密集型和耗时的操作，根据要压缩的纹理图像数量以及所选纹理格式和软件压缩类型，可能会导致_非常_长的构建时间。
:::

### Basis Universal

Basis Universal（简称BasisU）将图像压缩为中间格式，在运行时转码为适合当前设备GPU的硬件格式。Basis Universal格式是一种高质量但有损的格式。
所有图像还使用LZ4进行压缩，以进一步减小存储在游戏存档中的文件大小。

### ASTC

ASTC是由ARM开发并由Khronos Group标准化的灵活高效的纹理压缩格式。它提供了广泛的块大小和比特率，允许开发人员有效地平衡图像质量和内存使用。ASTC支持各种块大小，从4×4到12×12个图素，对应的比特率从每个图素8位到每个图素0.89位不等。这种灵活性使得可以对纹理质量和存储需求之间的权衡进行细粒度控制。

ASTC支持各种块大小，从4×4到12×12个图素，对应的比特率从每个图素8位到每个图素0.89位不等。这种灵活性使得可以对纹理质量和存储需求之间的权衡进行细粒度控制。下表显示了支持的块大小及其对应的比特率：

| 块大小（宽 x 高） | 每像素比特数 |
| ----------------- | ------------ |
| 4x4               | 8.00         |
| 5x4               | 6.40         |
| 5x5               | 5.12         |
| 6x5               | 4.27         |
| 6x6               | 3.56         |
| 8x5               | 3.20         |
| 8x6               | 2.67         |
| 10x5              | 2.56         |
| 10x6              | 2.13         |
| 8x8               | 2.00         |
| 10x8              | 1.60         |
| 10x10             | 1.28         |
| 12x10             | 1.07         |
| 12x12             | 0.89         |

#### 支持的设备

虽然ASTC提供了很好的效果，但并非所有图形卡都支持它。以下是基于供应商的支持设备的小列表：

| GPU供应商         | 支持                                                               |
| ----------------- | ------------------------------------------------------------------ |
| ARM (Mali)        | 所有支持OpenGL ES 3.2或Vulkan的ARM Mali GPU都支持ASTC。           |
| Qualcomm (Adreno) | 支持OpenGL ES 3.2或Vulkan的Adreno GPU支持ASTC。                   |
| Apple             | 自A8芯片以来的Apple GPU都支持ASTC。                                |
| NVIDIA            | ASTC支持主要针对移动GPU（例如，基于Tegra的芯片）。                 |
| AMD (Radeon)      | 支持Vulkan的AMD GPU通常通过软件支持ASTC。                         |
| Intel (集成)      | 现代Intel GPU通过软件支持ASTC。                                    |

## 纹理配置文件

每个项目都包含一个特定的*.texture_profiles*文件，其中包含压缩纹理时使用的配置。默认情况下，此文件是*builtins/graphics/default.texture_profiles*，它具有将每个纹理资源匹配到使用RGBA且没有硬件纹理压缩并使用默认ZLib文件压缩的配置文件的配置。

要添加纹理压缩：

- 选择<kbd>文件 ▸ 新建...</kbd>并选择*纹理配置文件*来创建新的纹理配置文件。（或者将*default.texture_profiles*复制到*builtins*之外的位置）
- 为新文件选择名称和位置。
- 将*game.project*中的*texture_profiles*条目更改为指向新文件。
- 打开*.texture_profiles*文件并根据您的要求进行配置。

![新建配置文件](images/texture_profiles/texture_profiles_new_file.png)

![设置纹理配置文件](images/texture_profiles/texture_profiles_game_project.png)

您可以在编辑器偏好设置中打开和关闭纹理配置文件的使用。选择<kbd>文件 ▸ 偏好设置...</kbd>。*常规*选项卡包含一个复选框项目*启用纹理配置文件*。

![纹理配置文件偏好设置](images/texture_profiles/texture_profiles_preferences.png)

## 路径设置

纹理配置文件的*路径设置*部分包含路径模式列表以及处理匹配路径的资源时使用的*配置文件*。路径表示为"Ant Glob"模式（有关详细信息，请参阅[文档](http://ant.apache.org/manual/dirtasks.html#patterns)）。可以使用以下通配符表示模式：

`*`
: 匹配零个或多个字符。例如，`sprite*.png`匹配文件*`sprite.png`*、*`sprite1.png`*和*`sprite_with_a_long_name.png`*。

`?`
: 精确匹配一个字符。例如：`sprite?.png`匹配文件*sprite1.png*、*`spriteA.png`*，但不匹配*`sprite.png`*或*`sprite_with_a_long_name.png`*。

`**`
: 匹配完整的目录树，或者---当用作目录名时---零个或多个目录。例如：`/gui/**`匹配目录*`/gui`*及其所有子目录中的所有文件。

![路径](images/texture_profiles/texture_profiles_paths.png)

此示例包含两个路径模式及其对应的配置文件。

`/gui/**/*.atlas`
: 目录*`/gui`*或其任何子目录中的所有*.atlas*文件将根据配置文件"gui_atlas"进行处理。

`/**/*.atlas`
: 项目中任何位置的所有*.atlas*文件将根据配置文件"atlas"进行处理。

请注意，更通用的路径放在最后。匹配算法从上到下工作。将使用匹配资源路径的第一个匹配项。列表中更下方的匹配路径表达式永远不会覆盖第一个匹配项。如果路径以相反的顺序放置，每个图集都将使用配置文件"atlas"进行处理，即使是目录*`/gui`*中的那些。

在配置文件中_不_匹配任何路径的纹理资源将被编译并缩放到最接近的2的幂，但否则将保持不变。

## 配置文件

纹理配置文件的*配置文件*部分包含命名配置文件的列表。每个配置文件包含一个或多个*平台*，每个平台由属性列表描述。

![配置文件](images/texture_profiles/texture_profiles_profiles.png)

*平台*
: 指定匹配的平台。`OS_ID_GENERIC`匹配所有平台，`OS_ID_WINDOWS`匹配Windows目标包，`OS_ID_IOS`匹配iOS包等等。请注意，如果指定了`OS_ID_GENERIC`，它将包含在所有平台中。

::: important
如果两个[路径设置](#path-settings)匹配同一个文件并且路径使用具有不同平台的不同配置文件，**两个**配置文件都将被使用，并且将生成**两个**纹理。
:::

*格式*
: 要生成的一个或多个纹理格式。如果指定了多种格式，将为每种格式生成纹理并包含在包中。引擎选择运行时平台支持的格式的纹理。

*多级纹理*
: 如果选中，将为平台生成多级纹理。默认情况下未选中。

*预乘Alpha*
: 如果选中，Alpha将预乘到纹理数据中。默认情况下选中。

*最大纹理大小*
: 如果设置为非零值，纹理的像素大小将限制为指定的数字。任何宽度或高度大于指定值的纹理都将缩小。

添加到配置文件的每个*格式*都具有以下属性：

*格式*
: 编码纹理时要使用的格式。有关所有可用的纹理格式，请参见下文。

*压缩器*
: 编码纹理时要使用的压缩器。

*压缩器预设*
: 选择用于编码结果压缩图像的压缩预设。每个压缩器预设对于压缩器是唯一的，其设置取决于压缩器本身。为了简化这些设置，当前的压缩预设有四个级别：

| 预设     | 说明                                          |
| -------- | --------------------------------------------- |
| `LOW`    | 最快压缩。低图像质量                          |
| `MEDIUM` | 默认压缩。最佳图像质量                        |
| `HIGH`   | 最慢压缩。更小的文件大小                      |
| `HIGHEST`| 慢压缩。最小的文件大小                        |

请注意，`uncompressed`压缩器只有一个名为`uncompressed`的预设，这意味着不会对纹理应用压缩。
要查看可用压缩器的列表，请参见[压缩器](#compressors)

## 纹理格式

图形硬件纹理可以处理为未压缩或*有损*压缩数据，具有各种数量的通道和位深度。固定的硬件压缩意味着无论图像内容如何，结果图像将具有固定的大小。这意味着压缩期间的质量损失取决于原始纹理的内容。

由于Basis Universal压缩转码取决于设备的GPU功能，建议与Basis Universal压缩一起使用的格式是通用格式，如：
`TEXTURE_FORMAT_RGB`、`TEXTURE_FORMAT_RGBA`、`TEXTURE_FORMAT_RGB_16BPP`、`TEXTURE_FORMAT_RGBA_16BPP`、`TEXTURE_FORMAT_LUMINANCE`和`TEXTURE_FORMAT_LUMINANCE_ALPHA`。

Basis Universal转码器支持许多输出格式，如`ASTC4x4`、`BCx`、`ETC2`、`ETC1`和`PVRTC1`。

当前支持以下有损压缩格式：

| 格式                            | 压缩 | 详细说明  |
| ------------------------------- | ---- | -------------------------------- | ---- |
| `TEXTURE_FORMAT_RGB`            | 无   | 3通道颜色。Alpha被丢弃           |
| `TEXTURE_FORMAT_RGBA`           | 无   | 3通道颜色和完整alpha。           |
| `TEXTURE_FORMAT_RGB_16BPP`      | 无   | 3通道颜色。5+6+5位。             |
| `TEXTURE_FORMAT_RGBA_16BPP`     | 无   | 3通道颜色和完整alpha。4+4+4+4位。|
| `TEXTURE_FORMAT_LUMINANCE`      | 无   | 1通道灰度，无alpha。RGB通道合并为一个。Alpha被丢弃。|
| `TEXTURE_FORMAT_LUMINANCE_ALPHA`| 无   | 1通道灰度和完整alpha。RGB通道合并为一个。|

对于ASTC，通道数将始终为4（RGB + alpha），格式本身定义了块压缩的大小。
请注意，这些格式仅与ASTC压缩器兼容 - 任何其他组合都会产生构建错误。

`TEXTURE_FORMAT_RGBA_ASTC_4X4`
`TEXTURE_FORMAT_RGBA_ASTC_5X4`
`TEXTURE_FORMAT_RGBA_ASTC_5X5`
`TEXTURE_FORMAT_RGBA_ASTC_6X5`
`TEXTURE_FORMAT_RGBA_ASTC_6X6`
`TEXTURE_FORMAT_RGBA_ASTC_8X5`
`TEXTURE_FORMAT_RGBA_ASTC_8X6`
`TEXTURE_FORMAT_RGBA_ASTC_8X8`
`TEXTURE_FORMAT_RGBA_ASTC_10X5`
`TEXTURE_FORMAT_RGBA_ASTC_10X6`
`TEXTURE_FORMAT_RGBA_ASTC_10X8`
`TEXTURE_FORMAT_RGBA_ASTC_10X10`
`TEXTURE_FORMAT_RGBA_ASTC_12X10`
`TEXTURE_FORMAT_RGBA_ASTC_12X12`


## 压缩器

默认情况下支持以下纹理压缩器。当纹理文件加载到内存时，数据将被解压缩。

| 名称             | 格式                   | 说明                                                                                          |
| ---------------- | --------------------- | --------------------------------------------------------------------------------------------- |
| `Uncompressed`   | 所有格式               | 不会应用压缩。默认。                                                                          |
| `BasisU`         | 所有RGB/RGBA格式      | Basis Universal高质量，有损压缩。较低的质量级别导致较小的尺寸。                                |
| `ASTC`           | 所有ASTC格式          | ASTC有损压缩。较低的质量级别导致较小的尺寸。                                                  |

::: sidenote
Defold 1.9.7重构了纹理压缩器管道以支持可安装压缩器，这是在扩展中实现纹理压缩算法（如WEBP或完全自定义的算法）的第一步。
:::

## 示例图像

为了更好地理解输出，这里有一个示例。
请注意，图像质量、压缩时间和压缩大小始终取决于输入图像，可能会有所不同。

基础图像（1024x512）：
![新建配置文件](images/texture_profiles/kodim03_pow2.png)

### 压缩时间

| 预设     | 压缩时间     | 相对时间   |
| -------- | ------------ | ---------- |
| `LOW`    | 0分0.143秒   | 0.5x       |
| `MEDIUM` | 0分0.294秒   | 1.0x       |
| `HIGH`   | 0分1.764秒   | 6.0x       |
| `HIGHEST`| 0分1.109秒   | 3.8x       |

### 信号损失

比较是使用`basisu`工具完成的（测量PSNR）
100 dB表示没有信号损失（即它与原始图像相同）。

| 预设     | 信号                                          |
| ------------------------------------------------------- |
| `LOW`    | 最大值: 34 平均值: 0.470 均方根: 1.088 峰值信噪比: 47.399 dB |
| `MEDIUM` | 最大值: 35 平均值: 0.439 均方根: 1.061 峰值信噪比: 47.620 dB |
| `HIGH`   | 最大值: 37 平均值: 0.898 均方根: 1.606 峰值信噪比: 44.018 dB |
| `HIGHEST`| 最大值: 51 平均值: 1.298 均方根: 2.478 峰值信噪比: 40.249 dB |

### 压缩文件大小

原始文件大小为1572882字节。

| 预设     | 文件大小 | 比率    |
| -------- | -------- | ------- |
| `LOW`    | 357225   | 22.71%  |
| `MEDIUM` | 365548   | 23.24%  |
| `HIGH`   | 277186   | 17.62%  |
| `HIGHEST`| 254380   | 16.17%  |


### 图像质量

以下是结果图像（使用`basisu`工具从ASTC编码中检索）

`LOW`
![低压缩预设](images/texture_profiles/kodim03_pow2.fast.png)

`MEDIUM`
![中压缩预设](images/texture_profiles/kodim03_pow2.normal.png)

`HIGH`
![高压缩预设](images/texture_profiles/kodim03_pow2.high.png)

`HIGHEST`
![最佳压缩预设](images/texture_profiles/kodim03_pow2.best.png)
