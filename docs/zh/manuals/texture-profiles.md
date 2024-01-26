---
title: Defold 中的纹理档案
brief: Defold 支持自动纹理处理和数据压缩. 本教程介绍了这类功能.
---

# 纹理档案

Defold 可以自动把图片数据处理成纹理并进行压缩 (称为 *Atlas*, *Tile sources*, *Cubemaps* 和模型纹理, GUI资源等等).

压缩有两种, 图片软件压缩与纹理硬件压缩.

1. 软件压缩 (比如 PNG 和 JPEG) 减少了图片占用空间. 可以让成品打包小一点. 但是读取到内存的时候必须解压, 硬盘上很小的图片, 都可能占用大量内存空间.

2. 硬件压缩也是减小图片占用空间. 区别于软件压缩的是, 纹理的内存占用也能减少. 这是因为图像硬件可以直接处理压缩图片而省去了解压过程.

纹理的处理基于纹理档案的设定. _Profiles_ 描述了不同平台下使用哪种压缩格式和纹理类型. _Profiles_ 绑定了 _paths patterns_, 用以微调和确定实际的压缩算法.

因为所有硬件压缩都是有损的, 纹理数据可能会不如压缩前好看. 造成这种现象的原因高度取决于材质和压缩算法. 为了得到最好的效果就需要多多尝试. 别忘了 Google 是你的好伙伴.

软件压缩方面可以在打包时选择如何保存纹理数据 (压缩或者原图). Defold 支持 [基础通用](https://github.com/BinomialLLC/basis_universal) 纹理压缩, 它能把图片压缩为一个中间格式. 这种格式可以在运行时解码为适合硬件 GPU 使用的数据.
基础通用格式是高质量有损格式.
打包时还会使用 LZ4 算法进一步对图片进行压缩以减小包体.

::: sidenote
压缩属于资源密集型耗时操作, 图片多的话可以 _大大_ 增加编译时间, 还取决于你选择的纹理格式和压缩类型.
:::

## 纹理档案

每个项目都有 *.texture_profiles* 文件用来进行纹理压缩设置. 默认情况下, 这个文件位于 *builtins/graphics/default.texture_profiles* 并且设置为所有纹理都绑定一个档案就是使用 RGBA 不进行硬件压缩并且使用默认 ZLib 压缩算法.

新增纹理压缩:

- 点击 <kbd>File ▸ New...</kbd> 选择 *Texture Profiles* 来新建纹理档案文件. (或者把 *default.texture_profiles* 拷贝到 *builtins* 之外的项目文件夹下)
- 命名文件.
- 在 *game.project* 里的 *texture_profiles* 项上引用这个文件.
- 打开 *.texture_profiles* 文件进行自己需要的配置.

![New profiles file](images/texture_profiles/texture_profiles_new_file.png)

![Setting the texture profile](images/texture_profiles/texture_profiles_game_project.png)

你可以选择启用还是禁用纹理档案. 点击 <kbd>File ▸ Preferences...</kbd>. 在 *General* 部分就有 *Enable texture profiles* 选项.

![Texture profiles preferences](images/texture_profiles/texture_profiles_preferences.png)

## 路径设置

纹理档案的 *Path Settings* 部分是一个 *profile* 表格用以引用各种档案路径. 路径使用 "Ant Glob" 样式 (详情请见 http://ant.apache.org/manual/dirtasks.html#patterns) 表示. 样式中可以使用通配符:

`*`
: 匹配0个或多个字符. 例如 `sprite*.png` 匹配文件 *sprite.png*, *sprite1.png* 和 *sprite_with_a_long_name.png*.

`?`
: 匹配1个字符. 例如 `sprite?.png` 匹配文件 *sprite1.png*, *spriteA.png*, 但是不匹配文件 *sprite.png* 和 *sprite_with_a_long_name.png*.

`**`
: 匹配一个目录树, 或者在目录名中使用时可匹配多个目录. 例如 `/gui/**` 匹配 */gui* 及其所有子目录下的文件.

![Paths](images/texture_profiles/texture_profiles_paths.png)

本例中引用了两个档案路径.

`/gui/**/*.atlas`
: 在 */gui* 下及其子目录下的所有 *.atlas* 文件被描述为 "gui_atlas" 档案.

`/**/*.atlas`
: 项目中所有 *.atlas* 文件被描述为 "atlas" 档案.

注意把广泛匹配放在下面. 文件匹配是从上到下进行的. 上面的匹配优先与下面的. 下面的档案不会覆盖上面的. 否则的话所有 "atlas" 都被第二条匹配了, 包括第一条 */gui* 下的.

对于 _没有被_ 匹配到的纹理会被编译且缩放为最近的2次方幂大小, 或者不做任何压缩处理.

## 档案

*profiles* 包含与上述对应的档案表. 每个档案包含一个或多个 *platforms*, 每个平台又包括一系列属性设定.

![Profiles](images/texture_profiles/texture_profiles_profiles.png)

*Platforms*
: 指定平台. `OS_ID_GENERIC` 匹配所有平台, `OS_ID_WINDOWS` 对应 Windows 平台, `OS_ID_IOS` 对应 iOS 平台. 注意如果使用 `OS_ID_GENERIC`, 设定将会对所有平台生效.

::: important
如果两个 [路径样式](#path-settings) 匹配一个文件并且这两个路径分别指定不同的平台, 那么这两个档案 **都会** 生效, 所以会生成 **两个** 纹理.
:::

*Formats*
: 纹理格式. 如果指定多个, 每个格式都会生效. 引擎会在运行时选择合适的纹理格式.

*Mipmaps*
: 是否生成mipmap. 默认勾选.

*Premultiply alpha*
: 是否预乘alpha. 默认勾选.

*Max Texture Size*
: 如果填入非0值, 纹理将限制最大尺寸为填入值. 如果图片本身比填入值打, 纹理会被缩小.

对于每个档案的每个 *Formats*, 又有以下属性设定:

*Format*
: 纹理编码格式. 可用格式见下文.

*Compression*
: 选择图片压缩质量等级.

| 等级    |  说明                                         |
| -------- | --------------------------------------------- |
| `FAST`   | 压缩速度最快. 图片质量最低        |
| `NORMAL` | 默认压缩. 图片质量最高       |
| `HIGH`   | 最慢压缩. 缩小图片文件大小        |
| `BEST`   | 慢压缩. 图片文件大小最小          |

::: sidenote
为了避免歧义, 从版本 1.2.185 开始, 等级枚举用词做了调整.
:::

*Type*
: 压缩类型, 可选值有 `COMPRESSION_TYPE_DEFAULT`, `COMPRESSION_TYPE_WEBP` 和 `COMPRESSION_TYPE_WEBP_LOSSY`. 详见下文 [压缩类型](#compression-types).

## 纹理格式

硬件可以直接处理未压缩纹理以及 *有损* 压缩纹理. 固定硬件压缩意思是纹理大小是一定的, 而不论纹理的内容. 一定意义上原图内容决定了硬件压缩后纹理的质量.

因为基础通用压缩解码取决于设备的 GPU 功能, 推荐配合基础通用压缩的格式为:
`TEXTURE_FORMAT_RGB`, `TEXTURE_FORMAT_RGBA`, `TEXTURE_FORMAT_RGB_16BPP`, `TEXTURE_FORMAT_RGBA_16BPP`, `TEXTURE_FORMAT_LUMINANCE` 与 `TEXTURE_FORMAT_LUMINANCE_ALPHA`.

基础通用压缩解码支持各种输出格式, 例如 `ASTC4x4`, `BCx`, `ETC2`, `ETC1` 与 `PVRTC1`.
更多更新详情请见

::: sidenote
为了引入基础通用编码器, 目前指定硬件输出格式关闭.

如何同时支持这两种格式还在探索当中.
远期未来目标是引入内容管线插件来解决这个问题.
:::

目前支持以下有损压缩格式:

PVRTC
: 也是一种图块压缩方法. 在4比特模式 (4BPP) 下每个图块 4×4 像素. 在2比特模式 (2BPP) 下每个图块 8×4 像素. 每个图块占用 64 比特 (8 字节) 内存空间.  这种格式原本用于 iPhone, iPod Touch, 和 iPad. 目前使用 PowerVR GPU 的 Android 设备, 也支持这种格式. Defold 支持 PVRTC1, 在格式id中用后缀 "V1" 表示.

ETC
: 爱立信纹理压缩格式. 4×4 像素块再次压缩为 64 比特数据. 4×4 像素块一分为二然后给每块指定一个基础颜色. 每个像素编码为这个基础颜色的四通道偏移量. Android 从 2.2 版 (Froyo) 开始支持 ETC1. Defold 支持 ETC1 纹理压缩格式.

| 格式                            | 压缩 | 描述  |
| --------------------------------- | ----------- | -------------------------------- | ---- |
| `TEXTURE_FORMAT_RGB`              | none        | 3 颜色通道. Alpha 被丢弃 |
| `TEXTURE_FORMAT_RGBA`             | none        | 3 颜色通道和 1 alpha 通道.    |
| `TEXTURE_FORMAT_RGB_16BPP`        | none        | 3 颜色通道. 5+6+5 比特. |
| `TEXTURE_FORMAT_RGBA_16BPP`       | none        | 3 颜色通道和 1 alpha 通道. 4+4+4+4 比特. |
| `TEXTURE_FORMAT_LUMINANCE`        | none        | 1 灰度通道, 无 alpha 通道. RGB 编码为 1 颜色通道. Alpha 被丢弃. |
| `TEXTURE_FORMAT_LUMINANCE_ALPHA`  | none        | 1 灰度通道和 1 alpha 通道. RGB 编码为 1 颜色通道. |
| `TEXTURE_FORMAT_RGB_PVRTC2BPPV1`  | 1:16 固定. | 无 alpha 通道. 正方形图片. 非正方形图片会被裁剪. |
| `TEXTURE_FORMAT_RGB_PVRTC4BPPV1`  | 1:8 固定   | 无 alpha 通道. 正方形图片. 非正方形图片会被裁剪. |
| `TEXTURE_FORMAT_RGBA_PVRTC2BPPV1` | 1:16 固定 | 预乘 alpha. 正方形图片. 非正方形图片会被裁剪. |
| `TEXTURE_FORMAT_RGBA_PVRTC4BPPV1` | 1:8 固定. | 预乘 alpha. 正方形图片. 非正方形图片会被裁剪. |
| `TEXTURE_FORMAT_RGB_ETC1`         | 1:6 固定  | 无 alpha 通道. |


## 压缩类型

支持以下软件压缩类型. 载入内存时需要解压.

::: sidenote
目前 `WEBP` 压缩会回退为 `BASIS_UASTC` 压缩.

如何同时支持这两种格式还在探索当中.
远期未来目标是引入内容管线插件来解决这个问题.
:::

| 类型                              | 格式                   | 说明 |
| --------------------------------- | ------------------------- | ---- |
| `COMPRESSION_TYPE_DEFAULT`        | All formats               | 常见有损压缩. 默认类型. |
| `COMPRESSION_TYPE_BASIS_UASTC`    | All RGB/RGBA formats      | 基础通用高质, 有损压缩. 质量等级越低体积越小. |
| `COMPRESSION_TYPE_WEBP`           | All formats               | WebP 无损压缩. 质量等级越高体积越小. |
| `COMPRESSION_TYPE_WEBP_LOSSY`     | All non hardware compressed formats. | WebP 有损压缩. 质量等级越低体积越小. |

对于硬件压缩纹理格式PVRTC或ETC, WebP无损压缩过程使用内部中间格式将压缩的硬件纹理格式数据转换为更适合WebP图像压缩的数据. 然后在运行时加载时将其转换回压缩的硬件纹理格式. 硬件压缩纹理格式PVRTC和ETC目前不支持WebP有损类型.


## 图片压缩测试

为了便于更好地理解, 这里举了一个例子.
注意图片质量, 压缩时间和压缩量取决于原始图片, 不同图片可能效果不同.

原始图片 (1024x512):
![New profiles file](images/texture_profiles/kodim03_pow2.png)

### 压缩时间

| 等级      | 压缩时间 | 倍率   |
| ----------------------------- | --------------- |
| `FAST`     | 0m0.143s         | 0.5x            |
| `NORMAL`   | 0m0.294s         | 1.0x            |
| `HIGH`     | 0m1.764s         | 6.0x            |
| `BEST`     | 0m1.109s         | 3.8x            |

### 失真

这里使用 `basisu` 工具进行比较 (比较参数 PSNR)
100 dB 表示不失真 (也就是说和原始图片完全相同).

| 等级      | 数据                                          |
| ------------------------------------------------------------ |
| `FAST`     | Max:  34 Mean: 0.470 RMS: 1.088 PSNR: 47.399 dB |
| `NORMAL`   | Max:  35 Mean: 0.439 RMS: 1.061 PSNR: 47.620 dB |
| `HIGH`     | Max:  37 Mean: 0.898 RMS: 1.606 PSNR: 44.018 dB |
| `BEST`     | Max:  51 Mean: 1.298 RMS: 2.478 PSNR: 40.249 dB |

### 压缩文件大小

原始文件 1572882 字节.

| 等级      | 文件大小 | 压缩率    |
| ---------------------------------- |
| `FAST`     | 357225     | 22.71 %  |
| `NORMAL`   | 365548     | 23.24 %  |
| `HIGH`     | 277186     | 17.62 %  |
| `BEST`     | 254380     | 16.17 %  |


### 图片质量

下面给出压缩后的图片 (使用`basisu` 工具的 ASTC 编码进行了修正)

`FAST`
![fast compression level](images/texture_profiles/kodim03_pow2.fast.png)

`NORMAL`
![normal compression level](images/texture_profiles/kodim03_pow2.normal.png)

`HIGH`
![high compression level](images/texture_profiles/kodim03_pow2.high.png)

`BEST`
![best compression level](images/texture_profiles/kodim03_pow2.best.png)
