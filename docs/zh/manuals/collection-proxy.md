---
title: 集合代理手册
brief: 本手册解释了如何动态创建新游戏世界以及在游戏世界间进行切换.
---

# 集合代理

集合代理组件用于基于集合文件内容动态加载和卸载新的游戏"世界"。它们可以用来实现游戏关卡之间的切换、GUI屏幕、在关卡中加载和卸载叙事"场景"、加载/卸载迷你游戏等等。

Defold将所有游戏对象组织在集合中。一个集合可以包含游戏对象和其他集合（即子集合）。集合代理允许您将内容拆分为单独的集合，然后通过脚本动态管理这些集合的加载和卸载。

集合代理与[集合工厂组件](/manuals/collection-factory/)不同。集合工厂将集合的内容实例化到当前游戏世界中。集合代理在运行时创建一个新的游戏世界，因此有不同的用例。

## 创建集合代理组件

1. 通过<kbd>右键点击</kbd>游戏对象并从上下文菜单中选择<kbd>Add Component ▸ Collection Proxy</kbd>，将集合代理组件添加到游戏对象。

2. 将*Collection*属性设置为您希望稍后动态加载到运行时中的集合的引用。该引用是静态的，确保所引用集合的所有内容最终都会出现在游戏中。

![add proxy component](images/collection-proxy/create_proxy.png)

（您可以通过勾选*Exclude*框并使用[实时更新功能](/manuals/live-update/)在构建中排除内容，然后通过代码下载。）

## 引导集合

当Defold引擎启动时，它会从*引导集合*加载并实例化所有游戏对象到运行时。然后初始化并启用游戏对象及其组件。引擎应该使用哪个引导集合是在[项目设置](/manuals/project-settings/#main-collection)中设置的。按照惯例，这个集合文件通常命名为"main.collection"。

![bootstrap](images/collection-proxy/bootstrap.png)

为了容纳游戏对象及其组件，引擎为整个"游戏世界"分配所需的内存，引导集合的内容被实例化到这个世界中。还为任何碰撞对象和物理模拟创建了一个单独的物理世界。

由于脚本组件需要能够处理游戏中的所有对象，即使是来自引导世界之外的对象，它被赋予一个唯一的名称：您在集合文件中设置的*Name*属性：

![bootstrap](images/collection-proxy/collection_id.png)

如果加载的集合包含集合代理组件，那些代理引用的集合*不会*被自动加载。您需要通过脚本控制这些资源的加载。

## 加载集合

通过代理动态加载集合是通过从脚本向代理组件发送名为`"load"`的消息来完成的：

```lua
-- 告诉代理 "myproxy" 开始加载。
msg.post("#myproxy", "load")
```

![load](images/collection-proxy/proxy_load.png)

代理组件将指示引擎为新世界分配空间。还会创建一个单独的运行时物理世界，并且集合`"mylevel.collection"`中的所有游戏对象都被实例化。

新世界从集合文件中的*Name*属性获取其名称，在本示例中设置为`"mylevel"`。名称必须是唯一的。如果在集合文件中设置的*Name*已被用于已加载的世界，引擎将发出名称冲突错误：

```txt
ERROR:GAMEOBJECT: The collection 'default' could not be created since there is already a socket with the same name.
WARNING:RESOURCE: Unable to create resource: build/default/mylevel.collectionc
ERROR:GAMESYS: The collection /mylevel.collectionc could not be loaded.
```

当引擎完成加载集合后，集合代理组件将向发送`"load"`消息的脚本发送一个名为`"proxy_loaded"`的消息。然后脚本可以初始化并启用集合作为对该消息的响应：

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        -- 新世界已加载。初始化并启用它。
        msg.post(sender, "init")
        msg.post(sender, "enable")
        ...
    end
end
```

`"load"`
: 此消息告诉集合代理组件开始将其集合加载到新世界中。完成后，代理将发送回一个名为 `"proxy_loaded"` 的消息。

`"async_load"`
: 此消息告诉集合代理组件开始在后台将其集合加载到新世界中。完成后，代理将发送回一个名为 `"proxy_loaded"` 的消息。

`"init"`
: 此消息告诉集合代理组件所有已实例化的游戏对象和组件应该被初始化。此时会调用所有脚本的`init()`函数。

`"enable"`
: 此消息告诉集合代理组件所有游戏对象和组件应该被启用。例如，所有精灵组件在启用时开始绘制。

## 定位到新世界

在集合文件属性中设置的*Name*用于定位已加载世界中的游戏对象和组件。例如，如果您在引导集合中创建了一个加载器对象，您可能需要从任何已加载的集合中与它通信：

```lua
-- 告诉加载器加载下一关：
msg.post("main:/loader#script", "load_level", { level_id = 2 })
```

![load](images/collection-proxy/message_passing.png)

如果您需要从加载器与已加载集合中的游戏对象通信，您可以使用[对象的完整URL](/manuals/addressing/#urls)发送消息：

```lua
msg.post("mylevel:/myobject", "hello")
```

::: important
无法从集合外部直接访问已加载集合中的游戏对象：

```lua
local position = go.get_position("mylevel:/myobject")
-- loader.script:42: function called can only access instances within the same collection.
```
:::

## 卸载世界

要卸载已加载的集合，您发送与加载步骤相反的消息：

```lua
-- 卸载关卡
msg.post("#myproxy", "disable")
msg.post("#myproxy", "final")
msg.post("#myproxy", "unload")
```

`"disable"`
: 此消息告诉集合代理组件禁用世界中的所有游戏对象和组件。精灵在此阶段停止渲染。

`"final"`
: 此消息告诉集合代理组件完成世界中的所有游戏对象和组件。此时会调用所有脚本的`final()`函数。

`"unload"`
: 此消息告诉集合代理将世界完全从内存中移除。

如果您不需要更细粒度的控制，可以直接发送`"unload"`消息，而无需先禁用和完成集合。代理将在卸载之前自动禁用并完成集合。

当集合代理完成卸载集合后，它将向发送`"unload"`消息的脚本发送一个`"proxy_unloaded"`消息：

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_unloaded") then
        -- 好的，世界已卸载...
        ...
    end
end
```


## 时间步

集合代理更新可以通过改变_时间步_来进行缩放。这意味着即使游戏以稳定的60 FPS运行，代理也可以以更高或更低的速度更新，影响诸如：

* 物理模拟速度
* 传递给`update()`的`dt`
* [游戏对象和GUI属性动画](https://defold.com/manuals/animation/#property-animation-1)
* [翻页动画](https://defold.com/manuals/animation/#flip-book-animation)
* [粒子FX模拟](https://defold.com/manuals/particlefx/)
* 计时器速度

您还可以设置更新模式，这允许您控制缩放是否应该离散执行（仅在缩放因子低于1.0时才有意义）或连续执行。

您通过向代理发送`set_time_step`消息来控制缩放因子和缩放模式：

```lua
-- 以五分之一速度更新已加载的世界。
msg.post("#myproxy", "set_time_step", {factor = 0.2, mode = 1})
```

为了了解更改时间步时发生的情况，我们可以创建一个对象，在其脚本组件中放置以下代码，并将其放在我们正在更改时间步的集合中：

```lua
function update(self, dt)
    print("update() with timestep (dt) " .. dt)
end
```

时间步为0.2时，我们在控制台中得到以下结果：

```txt
INFO:DLIB: SSDP started (ssdp://192.168.0.102:54967, http://0.0.0.0:62162)
INFO:ENGINE: Defold Engine 1.2.37 (6b3ae27)
INFO:ENGINE: Loading data from: build/default
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
```

`update()`仍然每秒调用60次，但`dt`的值发生了变化。我们看到只有1/5（0.2）的`update()`调用会有1/60（对应60 FPS）的`dt`——其余为零。所有物理模拟也将根据该`dt`更新，并且仅在五分之一的帧中前进。

::: sidenote
您可以使用集合时间步功能来暂停游戏，例如在显示弹出窗口或窗口失去焦点时。使用`msg.post("#myproxy", "set_time_step", {factor = 0, mode = 0})`暂停，使用`msg.post("#myproxy", "set_time_step", {factor = 1, mode = 1})`恢复。
:::

有关更多详细信息，请参见[`set_time_step`](/ref/collectionproxy#set_time_step)。

## 注意事项和常见问题

物理
: 通过集合代理，可以将多个顶级集合或*游戏世界*加载到引擎中。这样做时，重要的是要知道每个顶级集合都是一个单独的物理世界。物理交互（碰撞、触发、射线投射）只发生在属于同一世界的对象之间。因此，即使来自两个世界的碰撞对象在视觉上恰好彼此重叠，它们之间也不会有任何物理交互。

内存
: 每个加载的集合都会创建一个新的游戏世界，这带来了相对较大的内存占用。如果您通过代理同时加载几十个集合，您可能需要重新考虑您的设计。要生成游戏对象层级的许多实例，[集合工厂](/manuals/collection-factory)更适合。

输入
: 如果您在加载的集合中有需要输入操作的对象，您需要确保包含集合代理的游戏对象获取输入。当游戏对象接收到输入消息时，这些消息会传播到该对象的组件，即集合代理。输入操作通过代理发送到加载的集合中。
