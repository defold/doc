---
title: Defold HTML5平台开发
brief: 本手册描述了创建HTML5游戏的过程，以及已知问题和局限性。
---

# HTML5开发

Defold支持通过常规打包菜单为HTML5平台构建游戏，与其他平台一样。此外，生成的游戏会嵌入到一个常规HTML页面中，该页面可以通过简单的模板系统进行样式设置。

*game.project* 文件包含了 HTML5 相关设置:

![Project settings](images/html5/html5_project_settings.png)

## 堆大小

Defold对HTML5的支持由Emscripten驱动（参见http://en.wikipedia.org/wiki/Emscripten）。简而言之，它为应用程序运行的堆创建了一个内存沙箱。默认情况下，引擎分配了大量的内存（256MB）。这对于典型游戏来说应该绰绰有余。作为优化过程的一部分，您可以选择使用较小的值。为此，请按照以下步骤操作：

1. 将*heap_size*设置为您偏好的值。它应以兆字节表示。
2. 创建您的HTML5包（见下文）

## 测试HTML5构建

对于测试，HTML5构建需要一个HTTP服务器。如果您选择<kbd>Project ▸ Build HTML5</kbd>，Defold会为您创建一个。

![Build HTML5](images/html5/html5_build_launch.png)

如果您想测试您的包，只需将其上传到远程HTTP服务器或在包文件夹中创建本地服务器，例如，使用python：
Python 2：

```sh
python -m SimpleHTTPServer
```

Python 3：

```sh
python -m http.server
```

或者

```sh
python3 -m http.server
```

::: important
您不能通过在浏览器中打开`index.html`文件来测试HTML5包。这需要HTTP服务器。
:::

::: important
如果您在控制台中看到`"wasm streaming compile failed: TypeError: Failed to execute 'compile' on 'WebAssembly': Incorrect response MIME type. Expected 'application/wasm'."`错误，您必须确保您的服务器对`.wasm`文件使用`application/wasm` MIME类型。
:::

## 创建HTML5包

使用Defold创建HTML5内容很简单，并且遵循与所有其他支持平台相同的模式：从菜单中选择<kbd>Project ▸ Bundle... ▸ HTML5 Application...</kbd>：

![Create HTML5 bundle](images/html5/html5_bundle.png)

您可以选择在HTML5包中同时包含`asm.js`和WebAssembly（wasm）版本的Defold引擎。在大多数情况下，只选择WebAssembly就足够了，因为[所有现代浏览器都支持WebAssembly](https://caniuse.com/wasm)。

::: important
即使您同时包含`asm.js`和`wasm`版本的引擎，启动游戏时浏览器只会下载其中一个。如果浏览器支持WebAssembly，将下载WebAssembly版本，而在不支持WebAssembly的极少数情况下，将使用`asm.js`版本作为后备。
:::

当您单击<kbd>Create bundle</kbd>按钮时，系统将提示您选择一个文件夹来创建您的应用程序。导出过程完成后，您将找到运行应用程序所需的所有文件。

## 已知问题和局限性

* 热重载 - 热重载在HTML5构建中不起作用。Defold应用程序必须运行自己的小型Web服务器才能从编辑器接收更新，这在HTML5构建中是不可能的。
* Internet Explorer 11
  * 音频 - Defold使用HTML5 _WebAudio_（参见http://www.w3.org/TR/webaudio）处理音频播放，而Internet Explorer 11目前不支持。使用此浏览器时，应用程序将回退到空音频实现。
  * WebGL - Microsoft尚未完成实现_WebGL_ API的工作（参见https://www.khronos.org/registry/webgl/specs/latest/）。因此，它的性能不如其他浏览器。
  * 全屏 - 浏览器中的全屏模式不可靠。
* Chrome
  * 调试构建缓慢 - 在HTML5的调试构建中，我们验证所有WebGL图形调用以检测错误。不幸的是，在Chrome上测试时这非常慢。可以通过将*game.project*的*Engine Arguments*字段设置为`--verify-graphics-calls=false`来禁用此功能。
* 游戏手柄支持 - 有关HTML5上可能需要采取的特殊考虑和步骤，请[参阅游戏手柄文档](/manuals/input-gamepads/#gamepads-in-html5)。

## 自定义HTML5包

当生成游戏的HTML5版本时，Defold提供了一个默认网页。它引用了样式和脚本资源，这些资源决定了游戏的呈现方式。

每次导出应用程序时，都会重新创建此内容。如果您希望自定义这些元素中的任何一个，您必须对项目设置进行修改。为此，请在Defold编辑器中打开*game.project*并滚动到*html5*部分：

![HTML5 Section](images/html5/html5_section.png)

有关每个选项的更多信息，请参见[项目设置手册](/manuals/project-settings/#html5)。

::: important
您不能修改`builtins`文件夹中的默认html/css模板文件。要应用您的修改，请从`builtins`复制所需的文件，并在*game.project*中设置此文件。
:::

::: important
画布不应使用任何边框或内边距进行样式设置。如果这样做，鼠标输入坐标将会出错。
:::

在*game.project*中，可以关闭`Fullscreen`按钮和`Made with Defold`链接。
Defold为index.html提供了深色和浅色主题。默认情况下设置浅色主题，但可以通过更改`Custom CSS`文件来更改。在`Scale Mode`字段中还有四种预定义的缩放模式可供选择。

::: important
如果您在*game.project*（`Display`部分）中打开`High Dpi`选项，所有缩放模式的计算都包括当前屏幕DPI。
:::

### Downscale Fit和Fit

对于`Fit`模式，画布大小将更改为以原始比例在屏幕上显示完整游戏画布。`Downscale Fit`的唯一区别是，仅当网页内部大小小于游戏的原始画布时才更改大小，但当网页大于原始游戏画布时不会放大。

![HTML5 Section](images/html5/html5_fit.png)

### Stretch

对于`Stretch`模式，画布大小将更改为完全填充网页的内部大小。

![HTML5 Section](images/html5/html5_stretch.png)

### No Scale
使用`No Scale`模式，画布大小与您在*game.project*文件`[display]`部分中预定义的大小完全相同。

![HTML5 Section](images/html5/html5_no_scale.png)

## 标记

我们使用[Mustache模板语言](https://mustache.github.io/mustache.5.html)来创建`index.html`文件。当您构建或打包时，HTML和CSS文件会通过一个编译器，该编译器能够用取决于您的项目设置的值替换某些标记。这些标记总是用双大括号或三重大括号（`{{TOKEN}}`或`{{{TOKEN}}}`）括起来，取决于字符序列是否应该被转义。如果您经常更改项目设置或打算材料在其他项目中重用，此功能可能很有用。

::: sidenote
有关Mustache模板语言的更多信息，请参见[手册](https://mustache.github.io/mustache.5.html)。
:::

任何*game.project*都可以是一个标记。例如，如果您想使用`Display`部分中的`Width`值：

![Display section](images/html5/html5_display.png)

将*game.project*作为文本打开，并检查您想使用的字段的`[section_name]`和字段名称。然后您可以将其用作标记：`{{section_name.field}}`或`{{{section_name.field}}}`。

![Display section](images/html5/html5_game_project.png)

例如，在HTML模板中的JavaScript中：

```javascript
function doSomething() {
    var x = {{display.width}};
    // ...
}
```

此外，我们还有以下自定义标记：

DEFOLD_SPLASH_IMAGE
: 写入启动图像文件的文件名，如果*game.project*中的`html5.splash_image`为空，则为`false`


```css
{{#DEFOLD_SPLASH_IMAGE}}
		background-image: url("{{DEFOLD_SPLASH_IMAGE}}");
{{/DEFOLD_SPLASH_IMAGE}}
```

exe-name
: 不包含不可接受符号的项目名称


DEFOLD_CUSTOM_CSS_INLINE
: 这是我们在*game.project*设置中指定的CSS文件内联的地方。


```html
<style>
{{{DEFOLD_CUSTOM_CSS_INLINE}}}
</style>
```

::: important
这个内联块出现在主应用程序脚本加载之前很重要。由于它包含HTML标签，此宏应该出现在三重大括号`{{{TOKEN}}}`中，以防止字符序列被转义。
:::

DEFOLD_SCALE_MODE_IS_DOWNSCALE_FIT
: 如果`html5.scale_mode`是`Downscale Fit`，则此标记为`true`。

DEFOLD_SCALE_MODE_IS_FIT
: 如果`html5.scale_mode`是`Fit`，则此标记为`true`。

DEFOLD_SCALE_MODE_IS_NO_SCALE
: 如果`html5.scale_mode`是`No Scale`，则此标记为`true`。

DEFOLD_SCALE_MODE_IS_STRETCH
: 如果`html5.scale_mode`是`Stretch`，则此标记为`true`。

DEFOLD_HEAP_SIZE
: 在*game.project*`html5.heap_size`中指定的堆大小，转换为字节。

DEFOLD_ENGINE_ARGUMENTS
: 在*game.project*`html5.engine_arguments`中指定的引擎参数，以`,`符号分隔。

build-timestamp
: 当前构建时间戳（以秒为单位）。


## 额外参数

如果您创建自定义模板，可以重新定义引擎加载器的参数集。为此，您需要添加`<script>`部分并在`CUSTOM_PARAMETERS`内重新定义值。
::: important
您的自定义`<script>`应放在引用`dmloader.js`的`<script>`部分之后，但在调用`EngineLoader.load`函数之前。
:::
例如：
```
    <script id='custom_setup' type='text/javascript'>
        CUSTOM_PARAMETERS['disable_context_menu'] = false;
        CUSTOM_PARAMETERS['unsupported_webgl_callback'] = function() {
            console.log("Oh-oh. WebGL not supported...");
        }
    </script>
```

`CUSTOM_PARAMETERS`可能包含以下字段：

```
'archive_location_filter':
    将为每个存档路径运行的过滤函数。

'unsupported_webgl_callback':
    如果不支持WebGL则调用的函数。

'engine_arguments':
    将传递给引擎的参数列表（字符串）。

'custom_heap_size':
    指定内存堆大小的字节数。

'disable_context_menu':
    如果为true，则在canvas元素上禁用右键单击上下文菜单。

'retry_time':
    错误后重试文件加载之前的暂停时间（以秒为单位）。

'retry_count':
    尝试下载文件时我们进行多少次尝试。

'can_not_download_file_callback':
    如果在'retry_count'尝试后无法下载文件则调用的函数。

'resize_window_callback':
    当发生调整大小/方向更改/焦点事件时调用的函数。

'start_success':
    成功加载后调用main之前调用的函数。

'update_progress':
    进度更新时调用的函数。参数进度更新为0-100。
```

## HTML5中的文件操作

HTML5构建支持诸如`sys.save()`、`sys.load()`和`io.open()`之类的文件操作，但这些操作的内部处理方式与其他平台不同。当Javascript在浏览器中运行时，没有真正的文件系统概念，并且出于安全原因阻止了本地文件访问。相反，Emscripten（因此Defold）使用[IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB)，这是一个用于持久存储数据的浏览器内数据库，在浏览器中创建虚拟文件系统。与其他平台文件系统访问的重要区别在于，写入文件和更改实际存储在数据库之间可能存在轻微延迟。浏览器开发者控制台通常允许您检查IndexedDB的内容。


## 向HTML5游戏传递参数

有时有必要在游戏启动之前或启动时向游戏提供额外的参数。例如，这可能是用户ID、会话令牌或游戏启动时要加载的关卡。这可以通过多种不同的方式实现，其中一些在此描述。

### 引擎参数

可以在配置和加载引擎时指定额外的引擎参数。这些额外的引擎参数可以在运行时使用`sys.get_config()`检索。要添加键值对，请修改传递给`index.html`中加载的引擎的`extra_params`对象的`engine_arguments`字段：


```
    <script id='engine-setup' type='text/javascript'>
    var extra_params = {
        ...,
        engine_arguments: ["--config=foo1=bar1","--config=foo2=bar2"],
        ...
    }
```

您也可以将`--config=foo1=bar1, --config=foo2=bar2`添加到*game.project*的HTML5部分的引擎参数字段中，它将被注入到生成的index.html文件中。

在运行时，您可以这样获取值：

```lua
local foo1 = sys.get_config("foo1")
local foo2 = sys.get_config("foo2")
print(foo1) -- bar1
print(foo2) -- bar2
```


### URL中的查询参数

您可以将参数作为页面URL中查询参数的一部分传递，并在运行时读取这些参数：

```
https://www.mygame.com/index.html?foo1=bar1&foo2=bar2
```

```lua
local url = html5.run("window.location")
print(url)
```

一个完整的辅助函数，用于将所有查询参数作为Lua表获取：

```lua
local function get_query_parameters()
    local url = html5.run("window.location")
    -- 获取url的查询部分（？号后面的部分）
    local query = url:match(".*?(.*)")
    if not query then
        return {}
    end

    local params = {}
    -- 迭代所有键值对
    for kvp in query:gmatch("([^&]+)") do
        local key, value = kvp:match("(.+)=(.+)")
        params[key] = value
    end
    return params
end

function init(self)
    local params = get_query_parameters()
    print(params.foo1) -- bar1
end
```


## 优化
HTML5游戏通常对初始下载大小、启动时间和内存使用有严格要求，以确保游戏在低端设备和慢速互联网连接上加载快速并运行良好。要优化HTML5游戏，建议重点关注以下领域：

* [内存使用](/manuals/optimization-memory)
* [引擎大小](/manuals/optimization-size)
* [游戏大小](/manuals/optimization-size)

## 常见问题
:[HTML5 常见问题](../shared/html5-faq.md)
