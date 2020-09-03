---
title: Defold 的 WebViews
brief: "WebViews 可以在你的手机上显示一个网页层. 同时支持在后台运行用户定义的js代码. 本教程介绍了 Defold 的官方 WebView 扩展, API 和功能."
---

# WebViews
WebView 提供了一套特殊的 API 用来在手机上显示一个网页层. 首先让我们来实现一个简单的 webview.
然后我们会讨论如何使用一套简单的控制按钮控制这个 webview.

## 安装扩展

在你的 `game.project` 文件中设置 webview 依赖.
最新版本位于如下 URL:
```
https://github.com/defold/extension-webview/archive/master.zip
```

API文档位于 [扩展首页](https://defold.github.io/extension-webview/).

## 打开 webview
使用 `webview.create` 就能创建一个网页层, 并且返回一个唯一id. 下文中我们把这个 ID 称为 `webview_id`,
多个 `webview` 之间进行交互时会用到这个id. 也就是说创建和维护多个 webview 是可行的.

`webview.create` 带着一个函数参数, 待会儿我们再来仔细看看这个回调, 现在先给它留空.
```lua
local webview_id = webview.create(function()
        -- 目前无代码
    end)
```
默认状况下新建的 webview 都是不可见的, 因为它还没有加载任何内容. 其主要功能就是显示网页, 现在就来加载个超酷的网页吧!

调用 `webview.open` 函数, 第一个参数就是上文的那个 `webview_id`, 第二个参数是要打开的URL.

```lua
local request_id = webview.open(webview_id, "http://www.defold.com") --广告无处不在
```

这个函数返回网页请求的id, 这个id我们稍后也会用到.

如果一切顺利你将看到神奇的网页占满了屏幕, 就是 Defold 官方首页.

::: 注意
要在 iOS 里访问的网页必须遵循在 `Info.plist` 文件中的 `NSAppTransportSecurity` 里面设置好的键值对.
```
<key>NSAllowsArbitraryLoads</key>
<true/>
```

开发的时候可以随便设置, 但是发布到 App Store 之后就只能通过使用 `NSExceptionDomains` 键代替. 这有点超出本教程讨论范围,
详情可以参考 [Apple 开发者文档](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CocoaKeys.html#//apple_ref/doc/uid/TP40009251-SW35).
:::

## 回调函数
顺利打开网页固然是好, 但要是 URL 无效或者出现其他不可预知的问题时要给用户显示错误信息怎么办? 或者要在用户离开网页时做些什么该怎么办?
幸运的是 webview 扩展程序具备了报错, 导航, 载入成功等等事件回调功能. 只需在调用 `webview.create` 时传入回调函数作为参数即可.

回调函数特征如下:
```lua
function callback(self, webview_id, request_id, type, data)
```

* **`self`** - 回调函数所处的脚本引用.
* **`webview_id`** - 回调函数可以做到多个webview共用, 这个参数引用的是回调事件发生的那个webview的id.
* **`request_id`** - 同样 `webview.open` 也可以共用一个回调回调函数, 这个参数引用的是回调事件发生的那个载入请求的id.
* **`type`** - 事件的类型, 枚举类型, 下文 *回调类型* 章节会详细探讨.
* **`data`** - 不同时间连带的各种数据信息.

#### 回调类型
回调的 `type` 参数可以被设置为以下枚举之一：

* **`webview.CALLBACK_RESULT_URL_LOADING`** - 在 webview 内导航时, 载入事件被触发. 调用 `webview.open` 或者
用户点击页面上的超级链接都会造成事件触发. 事件的处理结果决定了载入请求是否被允许. 如果返回 `false` 则载入终止, 其他值则是允许载入.
被允许的链接也会记录在回调函数 `data` 表的 `url` 项里.
* **`webview.CALLBACK_RESULT_URL_ERROR`** 和 **`webview.CALLBACK_RESULT_EVAL_ERROR`** -一旦载入出错, 或者
执行JavaScript脚本出错 (下文 *运行JavaScript脚本* 章节会详细探讨), 错误事件就会被触发. `data` 表的 `result` 项用一个字符串记录了错误的详细内容.
* **`webview.CALLBACK_RESULT_URL_OK`** 和 **`webview.CALLBACK_RESULT_EVAL_OK`** - 一旦载入成功, 或者执行JavaScript脚本成功,
OK事件就会被触发. 对于成功执行的JavaScript程序, 其执行结果会被保存在 `data` 表的 `result` 项之中.

事件触发介绍完了, 现在我们来看一个复杂点的例子.

比如我们要向玩家展示一个反馈页面, 玩家通过一个 HTML 表格发送反馈意见. 我们要在载入不成功的时候要提示友好的错误信息并关闭webview而不是把白屏留给玩家.
接下来我们尽量不让玩家离开这个反馈页面.

升级版的 `webview.create` 调用和回调被设计成下面这样:
```lua
local player_feedback_url = "https://example.com/my_game_name/customer_feedback"

local function webview_callback(self, webview_id, request_id, type, data)
    if type == webview.CALLBACK_RESULT_URL_ERROR then
        -- 遇到错误!
        -- 关闭 webview 然后显示提示文本!
        webview.destroy(webview_id)
        label.set_text("#label", "Player feedback not available at this moment.")

    elseif type == webview.CALLBACK_RESULT_URL_LOADING then
        -- 不让玩家离开这个页面.
        if data.url ~= player_feedback_url then
            return false
        end
    end
end

local feedback_webview = webview.create(webview_callback)
webview.open(feedback_webview, player_feedback_url)
```

一个反馈页面展示就完成了. 网页自己做, 打开后大概像这个样子:

![Player feedback web page](images/webview/webview_player_feedback1.png)

注意: 我们的例子里有一个指向 google.com 的超级链接, 目的是试试玩家点别的链接出不出的去. --牛虻

强制反馈功能完成! 但是怎么提交反馈呢? 也许玩家不想提交反馈呢, 怎么返回游戏? 再说, 全屏的网页真的合适吗? 后面的游戏界面全都被挡住了啊!
我们会在下文的 *运行 JavaScript 脚本* 和 *可视定位控制面板* 章节继续探讨.

## 载入展示自己的 HTML 网页
继续深入探讨之前, 我们来动手做一个可以用来交互的 HTML 简单网页.

With `webview.open_raw` we can provide a HTML source directly instead of loading it from a remote
URL. This means that even if the webserver is down, or the player have a slow internet connection,
we can still show the feedback form.

The first argument to `webview.open_raw` is just like `webview.open`, the `webview_id`. The second
argument is a string with raw HTML source, instead of an URL as in the previous function.

Let's recreate the previous example but inline the HTML directly in our Lua source:
```lua
local feedback_html = [[
<html>
<script type="text/javascript">
    function closeWebview() {
        // TODO
    }
    function submitFeedback() {
        // do something with the feedback here
        // ...
    }
</script>
<body>
    <center>
    <h4>Hello Player!</h4>
    <p>Please provide some feedback for my awesome game!</p>
    <form>
        <label>Game feedback:<br><textarea placeholder="Is it fun? What can be improved?" style="width: 300px; height: 80px"></textarea></label><br>
        <input type="button" onclick="submitFeedback()" value="Submit feedback">
        <br>
        <input type="button" onclick="closeWebview()" value="Cancel">
    </form>
</center>
</body>
</html>
]]

local function webview_callback(self, webview_id, request_id, type, data)
    -- ...
end

local webview_id = webview.create(webview_callback)
webview.open_raw(webview_id, feedback_html)
```

This should give us a similar webview as in the previous example, with the added benefit that we
can edit the HTML directly in our game source code. **Note:** The contents of `webview_callback` has
only been removed for readability.

Since we know that the HTML source is going to grow a bit once we start adding JavaScript code and
CSS, it now makes sense to separate the HTML data into its own file and load it dynamically during
runtime using [`sys.load_resource`](https://www.defold.com/ref/sys/#sys.load_resource:filename).
This also means that we more easily can view the HTML file in a desktop browser while we are
developing.

Let's create a new directory (`custom_resources`), and a HTML file (`feedback.html`) with the data
instead and set the `feedback_html` variable dynamically instead.

```lua
local feedback_html = sys.load_resource("/custom_resources/feedback.html")
-- ...
webview.open_raw(webview_id, feedback_html)
```

## Visibility and positioning control
Now let's tackle the issue of the webview being full screen.

To get a more immersive interaction we might want the webview only cover the upper part of the
screen. We can use the `webview.set_position` function to both set the position and width of a
webview. Passing in `-1` as either width or height will make the webview take up the full space on the
corresponding axis.

```lua
local webview_id = webview.create(webview_callback)
-- Position: top left corner of screen (0, 0)
-- Size: we want full with, but only 500px height
webview.set_position(webview_id, 0, 0, -1, 500)
```

![Resized feedback page](images/webview/webview_player_feedback2.png)

If the user is on a device with poor performance, the page might not load instantly and display as
white while loading. This might be jarring to our player, so let's hide the webview until the page
has loaded. This also gives us the opportunity to show a loading indication in-game to reassure the
player that the game is actually doing something.

To hide the webview we can pass along an options table to the third argument of our
`webview.open_raw` (or `webview.open`) call, with the field `hidden` set to `true`. The default
value of this field is `false` as we have seen before, once we opened a URL or HTML the webview
was immediately visible.

```lua
webview.open_raw(webview_id, feedback_html, {hidden = true})
```

To make sure the webview successfully loaded the URL or HTML we want to wait for the callback to
trigger with an event of type `webview.CALLBACK_RESULT_URL_OK`. Once we get this we know that we can
unhide the webview, which can be accomplished with the `webview.set_visible` function.

Let's update our callback with this new logic:
```lua
local function webview_callback(self, webview_id, request_id, type, data)
    if type == webview.CALLBACK_RESULT_URL_OK then
        -- No errors, let's present the webview!
        webview.set_visible(webview_id, 1)
    elseif type == webview.CALLBACK_RESULT_URL_ERROR then
        -- ...
```

## Running JavaScript
Now we have managed to fix most of our issues, but one last thing is still unsolved; being able to
close the webview.

We have already seen and used the function that will close and remove the webview in our callback
when we encounter an error, `webview.destroy`. But we need a way from inside the webview to trigger
the function call. Thankfully we there is a way from Lua to call JavaScript that will run inside the
webview and read the result. With this we should be able to poll for changes inside the webview.

Let's start with adding some state inside the JavaScript tag of the HTML that we can change when
the buttons are pressed on the web page.
```js
var shouldClose = false;
function closeWebview() {
    shouldClose = true;
}
function submitFeedback() {
    // do something with the feedback here
    // ...
    closeWebview();
}

```

Now once the player presses either the "Submit feedback" or "Cancel" button we update the
`shouldClose` variable.

Now somewhere in our Lua script we need to check for this state and call `webview.destroy`. A naive
place would be to check for this every frame, in our `update` function.

```lua
function update(self, dt)
    if not self.closeCheckRequest then
        self.closeCheckRequest = webview.eval(webview_id, "shouldClose")
    end
end
```

It's important to note here that the result from `webview.eval` is not the result from the
JavaScript being evaluated, but a *request id*. We need to update our callback to check against this
request id, and inspect the `data.result` field, which is where the actual JavaScript result will be
stored.

```lua
local function webview_callback(self, webview_id, request_id, type, data)
    if type == webview.CALLBACK_RESULT_EVAL_OK and
        request_id == self.closeCheckRequest then

        -- Compare the JavaScript result, if it's "true" we should
        -- close the webview!
        if data.result == "true" then
            webview.destroy(webview_id)
        end

    elseif type == webview.CALLBACK_RESULT_URL_OK then
        -- ...
```

Now we know if a form button was pressed from inside the webview and the player is able to get back
to the game!
