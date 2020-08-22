---
title: Defold HTML5 平台开发
brief: 本教程介绍了 HTML5 游戏开发, 及其已知问题和局限性.
---

# HTML5 开发

通过编辑器编译菜单可以看到, Defold 支持导出 HTML5 游戏. 进一步说, 游戏会通过一个模板系统嵌入到一个 HTML 页面之中.

*game.project* 文件包含了 HTML5 相关设置:

![Project settings](images/html5/html5_project_settings.png)

## Heap size

Defold 通过 Emscripten (详见 http://en.wikipedia.org/wiki/Emscripten) 支持 HTML5 导出. 简单地说, 它为应用的运行建立了一个虚拟内存堆. 默认情况下, 引擎分配了一块内存 (256MB). 这对一般游戏足够了. 通过游戏优化, 可以做到申请内存最小化. 要调整内存分配, 步骤如下:

1. 设置 *heap_size* 为需要的值. 以兆字节表示.
2. 打包 HTML5 游戏 (见下文)

## 测试 HTML5 游戏

要测试 HTML5 游戏, 需要先启动一个 HTTP 服务程序. Defold 可以通过 <kbd>Project ▸ Build HTML5</kbd> 启动内建 HTTP 服务.

![Build HTML5](images/html5/html5_build_launch.png)

要测试 HTML5 游戏, 把游戏上传到远程 HTTP 服务器或者使用本地服务程序, 比如, 使用 python 自带的 HTTP 服务.
Python 2:
> python -m SimpleHTTPServer

Python 3:
> python -m http.server

或者
> python3 -m http.server

::: 注意
不能直接用浏览器打开 HTML5 游戏的 `index.html` 文件. 要通过服务器访问打开.
:::

## 打包 HTML5 游戏

Defold 打包 HTML5 游戏很简单, 跟其他平台一样: 从菜单栏选择 <kbd>Project ▸ Bundle...​ ▸ HTML5 Application...</kbd>:

![Application files](images/html5/html5_bundle.png)

会弹出提示框让你选择游戏存放位置. 打包结束后, 就可以看到输出的所有文件.

## 已知问题和局限性

* Hot Reload - HTML5 游戏不支持热更新. Defold 应用必须通过服务器加载运行才能接收热更新. 纯浏览器网页无法获得热更新.
* Internet Explorer 11
  * Audio - Defold 使用 HTML5 _WebAudio_ (详见 http://www.w3.org/TR/webaudio) 来处理声音, 目前 Internet Explorer 11 还不支持. 所以这种情况下没有声音.
  * WebGL - Microsoft 没有完全实现 _WebGL_ API (详见 https://www.khronos.org/registry/webgl/specs/latest/). 所以, 较其他浏览器而言对WebGL支持不好.
  * Full screen - 全屏模式在浏览器中不可靠.
* Chrome
  * Slow debug builds - 为了在 HTML5 平台更好地调试我们开启了校验所有 WebGL 图像调用来检测错误. 但是这样做在 Chrome 上会运行缓慢. 可以把 *game.project* 里的 *Engine Arguments* 部分设置为 `–-verify-graphics-calls=false` 来关闭图像调用校验.

## 自定义 HTML5 打包

针对 HTML5 版本的游戏, Defold 提供了一个默认模板网页. 其中包含的样式和脚本代码决定了游戏的显示方式.

游戏输出时, 这个页面也会重新生成. 如果想要自定义网页模板需要在项目设置里手动配置. 要配置的话, 打开 Defold 编辑器的 *game.project* 文件然后找到 *html5* 部分:

![HTML5 Section](images/html5/html5_section.png)

关于每个选项详情请见 [形目设置教程](/manuals/project-settings/#html5).

::: 注意
`builtins` 文件夹下的默认 html/css 模板文件是不能直接修改的. 要先从 `builtins` 里把文件拷贝出来然后再在 `game.project` 文件里指明要使用的文件的位置.
:::

::: 注意
网页 canvas 不能有 border 或者 padding. 否则的话, 鼠标输入坐标会产生偏差.
:::

可以在 `game.project` 文件里禁用 `Fullscreen` 按钮以及 `Made with Defold` 链接.
Defold 提供了 index.html 文件的亮暗两种风格. 默认亮风格但是可以在 `Custom CSS` 修改成暗风格. 在 `Scale Mode` 部分还预定义了四种缩放模式可供选择.

::: 注意
各种缩放模式计算时考虑了当前屏幕 DPI 以支持 `game.project` 里的 `High Dpi` 选项 (在 `Display` 部分)
:::

### Fit 和 Downscale Fit

使用 `Fit` 模式 canvas 会以原始比例缩放来适配当前屏幕. `Downscale Fit` 的区别在于, 如果内嵌网页比游戏 canvas 小, 则游戏缩小；反之则以原始大小显示而并不放大=.

![HTML5 Section](images/html5/html5_fit.png)

### Stretch

使用 `Stretch` 模式 canvas 会充满整个内嵌网页.

![HTML5 Section](images/html5/html5_stretch.png)

### No Scale
使用 `No Scale` 模式游戏 canvas 大小保持在 `game.project` 文件里 `[display]` 部分设置的值.

![HTML5 Section](images/html5/html5_no_scale.png)

## Tokens

使用 [Mustache 模板语言](https://mustache.github.io/mustache.5.html) 创建 `index.html` 文件. 编译或打包时, HTML 和 CSS 文件会基于项目设置填充模板里面对应的 Tokens. 这些 Tokens 通常使用双大括号或者三层大括号标注 (`{{TOKEN}}` 或者 `{{{TOKEN}}}`), 用哪种取决于标注里面有没有转义字符. 这种方法便于频繁修改以及代码重用.

::: 注意
关于 Mustache 模板语言详情请见 [官方手册](https://mustache.github.io/mustache.5.html).
:::

`game.project` 里的设置都可以使用标注来引用. 比如说, 引用 `Display` 里 `Width` 的值:

![Display section](images/html5/html5_display.png)

用普通文本编辑器打开 `game.project` 找到想引用的 `[section_name]` 部分. 像这样引用设置的值: `{{section_name.field}}` 或者 `{{{section_name.field}}}`.

![Display section](images/html5/html5_game_project.png)

比如, 在 HTML 模板的 JavaScript 里:

```javascript
function doSomething() {
    var x = {{display.width}};
    // ...
}
```

而且, 我们还可以自定义标注:

DEFOLD_SPLASH_IMAGE
: 溅射屏幕图片文件名, 如果 `game.project` 里的 `html5.splash_image` 为空, 则设置为 `false`.


```css
{{#DEFOLD_SPLASH_IMAGE}}
		background-image: url("{{DEFOLD_SPLASH_IMAGE}}");
{{/DEFOLD_SPLASH_IMAGE}}
```

exe-name
: 不包含任何非法符号的项目名


DEFOLD_CUSTOM_CSS_INLINE
: 这里就是在 `game.project` 里设置的内联 CSS 文件的地方.


```html
<style>
{{{DEFOLD_CUSTOM_CSS_INLINE}}}
</style>
```

::: 注意
内联块要出现在主程序脚本加载之前. 因为里面有 HTML 标签, 所以要用三层大括号 `{{{TOKEN}}}` 来引用它.
:::

DEFOLD_SCALE_MODE_IS_DOWNSCALE_FIT
: 如果 `html5.scale_mode` 是 `Downscale Fit` 的话则值为 `true`.

DEFOLD_SCALE_MODE_IS_FIT
: 如果 `html5.scale_mode` 是 `Fit` 的话则值为 `true`.

DEFOLD_SCALE_MODE_IS_NO_SCALE
: 如果 `html5.scale_mode` 是 `No Scale` 的话则值为 `true`.

DEFOLD_SCALE_MODE_IS_STRETCH
: 如果 `html5.scale_mode` 是 `Stretch` 的话则值为 `true`.

DEFOLD_HEAP_SIZE
: 在 `game.project` 里设置的内存大小, `html5.heap_size` 的值以字节为单位.

DEFOLD_ENGINE_ARGUMENTS
: 在 `game.project` 里设置的引擎参数, `html5.engine_arguments` 以逗号 `,` 分隔.


## 额外参数

要创建自定义模板, 可以为引擎加载提供额外参数:
```
`Module.runApp("canvas", extra_params) - 通过指定canvas启动游戏

'extra_params' 可选的额外参数, 如下:

'archive_location_filter':
    包地址过滤.

'unsupported_webgl_callback':
    如果不支持 WebGL 则需调用的回调函数.

'engine_arguments':
    传入引擎的参数列表 (字符串).

'persistent_storage':
    是否使用持久化存储的布尔值.

'custom_heap_size':
    自定义内存使用的大小.

'disable_context_menu':
    为 true 的话则在canvas上关闭右键上下文弹出菜单.

'retry_time':
    文件下载失败重试时间间隔.

'retry_count':
    文件下载失败充实次数.

'can_not_download_file_callback':
    如果重试次数已满但是仍没有得到文件则需调用的回调函数.
*/
```

## HTML5 的文件操作

HTML5 支持 `sys.save()`, `sys.load()` 和 `io.open()` 之类的文件操作, 但是与其他平台实现方法不同. 基于安全考虑浏览器里运行的 Javascript 无权直接读写本地文件. Emscripten (即 Defold) 使用 [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB) 代替, 它是基于浏览器的持久化存储方案, 基于浏览器的虚拟文件系统. 与其他平台的区别主要是比直接读写文件要慢而且实质上读写的是一个数据库. 浏览器开发者工具通常都提供了 IndexedDB 的读写功能.
