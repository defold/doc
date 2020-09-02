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
Just opening web pages inside a webview might be sufficient in most cases, but what happens if the
URL isn't accessible or something unforeseen happens while loading? Perhaps we want to show a
notification to the user if we encounter an error, or we want to perform some action if a user
navigates away from the web page. Thankfully the webview extension has functionality to trigger
events when errors, navigations and success occur! They are exposed through the callback function we
pass as argument to the `webview.create` call.

The callback function should have the following signature:
```lua
function callback(self, webview_id, request_id, type, data)
```

* **`self`** - This is the script instance from where the callback was set.
* **`webview_id`** - The callback can be reused for multiple webview instances, this argument let's
you keep track of from which instance the event originates from.
* **`request_id`** - Likewise, you can trigger multiple `webview.open` calls, and the request id
allows you to know which of the requests the event was triggered from.
* **`type`** - An enum describing what kind of event happened, we will go through them below in
*Callback types*.
* **`data`** - A table containing different information depending on what type of event occurred.

#### Callback types
The `type` argument of the callback are always set to one of the following enums:

* **`webview.CALLBACK_RESULT_URL_LOADING`** - When a navigation occurs inside the webview, the
loading event is triggered. This can happen either if you call `webview.open` or the user clicks
on a link that would result in a new URL being loaded. The result of the callback dictates if the
navigation is allowed. If you return `false` the navigation will be blocked, any other return value
will allow the navigation. To decide if the navigation should be allowed or not, you can inspect
the `url` field in the `data` table, also supplied in the callback.
* **`webview.CALLBACK_RESULT_URL_ERROR`** and **`webview.CALLBACK_RESULT_EVAL_ERROR`** - In case of
errors loading the URL, or errors when trying to evaluate JavaScript (we will go into details below
in *Running JavaScript*), an error event will be triggered. The `result` field in the `data` table
contains more information about the error, as a string.
* **`webview.CALLBACK_RESULT_URL_OK`** and **`webview.CALLBACK_RESULT_EVAL_OK`** - When a URL
navigation or JavaScript execution was successful, an ok event will be triggered. In the case of
a successful JavaScript evaluation the result will be available in the `result` field of the `data`
table.

Now that we know a bit more of how the callback is called, let's create a more advanced example.

Imagine if we want to show some player feedback webpage, where the player can report feedback about
the game through a HTML form. We want to know if the URL couldn't be loaded, instead of an empty
page we want to show some ingame notification and close the webview. And we probably don't want the
player to be able to navigate away from the form.

Our updated `webview.create` call and callback could looks something like this:
```lua
local player_feedback_url = "https://example.com/my_game_name/customer_feedback"

local function webview_callback(self, webview_id, request_id, type, data)
    if type == webview.CALLBACK_RESULT_URL_ERROR then
        -- An error occurred!
        -- Let's close the webview and set a label with some helpful text!
        webview.destroy(webview_id)
        label.set_text("#label", "Player feedback not available at this moment.")

    elseif type == webview.CALLBACK_RESULT_URL_LOADING then
        -- Make sure the player isn't navigating away from the feedback URL.
        if data.url ~= player_feedback_url then
            return false
        end
    end
end

local feedback_webview = webview.create(webview_callback)
webview.open(feedback_webview, player_feedback_url)
```

This will result in a full screen webview being shown, loading a remote web page with our player
feedback form. Depending of how we setup our player feedback webpage it will look something like
this:

![Player feedback web page](images/webview/webview_player_feedback1.png)

Note: In our example we also included a link to google.com, just to verify that blocking any navigation
that would lead away from our webpage.

We now have our first working player feedback prototype! But what should happen once the player has
provided feedback? Maybe the player changes their mind and don't want to provide any feedback,
how do they get back to your game? Lastly, a full screen webview might not be the best option in
this case, perhaps we still want to show that the game is still running in the background! We will
cover solutions for these issues in the *Running JavaScript* and
*Visibility and positioning control* sections below.

## Opening and displaying a custom HTML page
Before we continue with handling positioning/sizing and being able to close the webview, let's make
it a bit easier to iterate on the HTML page without having to update our webserver with each change.

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
