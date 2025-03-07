---
title: 集合代理教程
brief: 本教程介绍了如何动态创建新游戏世界以及在游戏世界间进行切换.
---

# 集合代理

集合代理组件用于基于集合文件内容动态加载卸载新的游戏 "世界". 可以用来实现切换关卡, GUI 屏幕, 在关卡里加载卸载插播 "场景", 加载卸载迷你游戏等等功能.

Defold 把所有游戏对象组织在集合里. 集合可以包含游戏对象和其他集合 (即子集合). 集合代理可以让你把内容拆分到各个集合然后用脚本动态加载卸载这些集合.

集合代理不像 [集合工厂组件](/manuals/collection-factory/). 集合工厂用于在当前游戏世界创建集合. 集合代理用于运行时创建全新游戏世界, 它们用处不同.

## 创建集合代理组件

1. 把一个集合代理组件加入到游戏对象上 <kbd>右键点击</kbd> 并从上下文菜单中选择 <kbd>Add Component ▸ Collection Proxy</kbd>.

2. 设置 *Collection* 属性来引用一个集合, 就是你希望动态加载进运行环境的集合. 这些引用是静态的, 所以确保把游戏所需的各个部分都通过集合引用到.

![add proxy component](images/collection-proxy/create_proxy.png)

(也可以编译时排除一部分内容需要的时候用代码下载而不使用 *Exclude* 选项和 [热更新功能](/manuals/live-update/).)

## 启动集合

当 Defold 引擎开始工作最先把 *启动集合* 导入运行环境并对其中的所有游戏对象进行初始化. 然后开启游戏对象和它们的组件. 在 [项目配置](/manuals/project-settings/#Main Collection) 里设置把哪个集合作为启动集合使用. 依照惯例启动集合都叫做 "main.collection".

![bootstrap](images/collection-proxy/bootstrap.png)

启动集合实例化时引擎会为 "游戏世界" 里的游戏对象和组件分配足够的内存空间. 对于物理模拟和碰撞对象, 引擎会为其建立另一个游戏世界.

因为脚本要能定位任何地方的游戏对象, 包括启动集合之外的集合里的对象, 所以集合必须有独立的属性: *Name*:

![bootstrap](images/collection-proxy/collection_id.png)

如果被加载集合里还有集合代理, 代理引用的集合 *不会* 被自动加载. 需要手动写代码进行加载.

## 载入集合

通过代理动态载入集合需要用脚本给代理发送 `"load"` 消息:

```lua
-- 让代理 "myproxy" 开始加载集合.
msg.post("#myproxy", "load")
```

![load](images/collection-proxy/proxy_load.png)

集合代理会告诉引擎需要为新游戏世界分配多大空间内存. 另一个物理世界也被建立起来连同集合 "mylevel.collection" 里的游戏对象都会被实例化.

新游戏世界的创建通过 *Name* 属性引用的集合文件为蓝图, 本例中是 "mylevel". 不能有重名. 如果集合文件 *Name* 重名, 引擎会报错:

```txt
ERROR:GAMEOBJECT: The collection 'default' could not be created since there is already a socket with the same name.
WARNING:RESOURCE: Unable to create resource: build/default/mylevel.collectionc
ERROR:GAMESYS: The collection /mylevel.collectionc could not be loaded.
```

当集合加载完毕, 集合代理会向发送 `"load"` 消息的脚本发回 `"proxy_loaded"` 消息. 收到此消息就可以进行集合初始化等工作了:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        -- 新集合已加载完毕. 初始化并激活它.
        msg.post(sender, "init")
        msg.post(sender, "enable")
        ...
    end
end
```

`"load"`
: 此消息通知集合代理组件开始为新游戏世界加载集合. 完成后会发送 `"proxy_loaded"` 消息.

`"async_load"`
: 此消息通知集合代理组件开始在后台为新游戏世界加载集合. 完成后会发送 `"proxy_loaded"` 消息.

`"init"`
: 此消息通知集合代理组件集合里的游戏对象和组件已实例化完毕, 可以进行初始化了. 此时所有脚本里的 `init()` 函数会被调用.

`"enable"`
: 此消息通知集合代理组件集合里的游戏对象和组件已实例化完毕, 可以激活它们了. 此时会进行sprite渲染等等工作.

## 新游戏世界定位

使用集合文件的 *Name* 属性用来定位其中的游戏对象和组件. 比如启动集合里有个加载器对象, 一关结束后让它加载下一关:

```lua
-- 告诉加载器加载下一关:
msg.post("main:/loader#script", "load_level", { level_id = 2 })
```

![load](images/collection-proxy/message_passing.png)

## 新游戏世界卸载

卸载需要发送的消息和加载相反:

```lua
-- 卸载当前关卡
msg.post("#myproxy", "disable")
msg.post("#myproxy", "final")
msg.post("#myproxy", "unload")
```

`"disable"`
: 此消息通知集合代理组件关闭游戏对象和组件. 此时sprite不再进行渲染工作.

`"final"`
: 此消息通知集合代理组件析构游戏对象和组件. 此时所有脚本里的 `final()` 函数会被调用.

`"unload"`
: 此消息通知集合代理组件把游戏世界从内存中清除.

如果不那么细致, 只发送 `"unload"` 消息就好. 在卸载前代理会自动进行关闭和析构工作.

当即和卸载完毕, 集合代理会向发送 `"unload"` 消息的脚本发回 `"proxy_unloaded"` 消息:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_unloaded") then
        -- Ok, 游戏世界卸载完成...
        ...
    end
end
```


## 时间步

集合代理的更新周期可以使用 _time step_ 进行缩放. 也就是说即使游戏是 60 FPS 的, 集合代理游戏世界的速度还是可以变得可以更快或者更慢, 收以下几方面影响: 

* 物理模拟器步进
* `update()` 函数里的 `dt`
* [游戏对象和gui属性动画](https://defold.com/manuals/animation/#property-animation-1)
* [逐帧动画](https://defold.com/manuals/animation/#flip-book-animation)
* [粒子特效模拟器](https://defold.com/manuals/particlefx/)
* lua逻辑计时器速度

还可以设置刷新执行模式, 可以控制游戏刷新是分散的(速度缩放小于1.0有效) 还是连续的.

通过发送 `set_time_step` 消息给集合代理组件来设置时间步缩放系数与执行模式:

```lua
-- 把加载的游戏世界时间放慢为1/5.
msg.post("#myproxy", "set_time_step", {factor = 0.2, mode = 1}
```

这样做的结果, 我们可以通过一段代码来进行观察:

```lua
function update(self, dt)
    print("update() with timestep (dt) " .. dt)
end
```

时间步系数为 0.2, 控制台打印如下输出:

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

`update()` 仍然是每秒调用 60 次, 但是 `dt` 值变了. 可以看到只有 1/5 (0.2) 的 `update()` 调用包含 1/60 秒的 `dt` 参数, 其他都是 0. 物理模拟也基于 dt 每 5 帧步进一次.

::: sidenote
可以使用集合的时间步功能来暂停游戏, 例如弹出窗口或者游戏窗口失去焦点时, 使用 `msg.post("#myproxy", "set_time_step", {factor = 0, mode = 0})` 暂停游戏, 然后使用 `msg.post("#myproxy", "set_time_step", {factor = 1, mode = 1})` 继续游戏.
:::

详情请见 [`set_time_step`](/ref/collectionproxy#set_time_step).

## 注意事项与常见问题

物理
: 通过集合代理可以导入多个集合, 或称 *游戏世界*. 要注意的是每个顶级集合都有自己的物理世界. 物理交互 (碰撞, 触发, 射线) 只发生与同一物理世界的物体之间. 所以即使分别来自两个游戏世界的两个物体即使被放在一起, 也不会有碰撞发生.

内存
: 被载入的游戏世界都要占不少内存. 如果同时加载了很多集合, 推荐优化你的游戏规则. 创建多个游戏对象实例的话, [集合工厂](/manuals/collection-factory) 更加适用.

输入
: 要让集合里的游戏对象获得输入信息, 首先要确保集合代理所在的游戏对象获得了输入焦点. 当游戏对象收到输入消息时, 这些消息将传播到该对象的组件也就是集合代理中去. 输入动作通过集合代理下发到其载入的集合里.
