---
title: 移植指南
brief: 本手册重点介绍了将游戏移植到新平台时需要考虑的一些事项
---

# 移植指南

本教程包含了游戏跨平台发布的教程和步骤.

将 Defold 游戏移植到新平台通常是一个比较简单的过程. 理论上只要在 *game.project* 文件里配置好就行了, 但是处于对平台充分利用的考量还是推荐针对目标平台进行适配. 本教程包含一些通用移植的最佳实践和一些平台相关的细节.


## 输入
确保游戏适配平台的输入法. 只要支持 [游戏手柄](/manuals/input-gamepads) 的平台就做好手柄支持! 确保游戏有一个暂停菜单 - 万一输入控制器突然断掉, 游戏有必要暂停!

## 本地化
本地化翻译游戏中的任何文本以及商店页面中的文本，因为这将对销售产生积极影响! 对于本地化, 确保玩家可以在游戏的不同语言之间轻松切换 (通过暂停菜单).

::: important
仅 iOS - 确保在 `game.project` 里指定了 [Localizations](/manuals/project-settings/#localizations), 因为语言不在列表中的话 sys.get_info() 会返回空值.
:::

翻译应用页面上的文字因为这样会对销售产生积极意义! 一些平台要求为游戏发售的每个国家翻译页面文字.

## 商店资料

### 应用图标
确保您的游戏在竞争中脱颖而出. 图标通常是您与潜在玩家的第一个接触点. 要在充满游戏图标的页面上很容易找到才好.

### 商店横幅和图像
确保为您的游戏使用有影响力和令人兴奋的美术资源. 花一些钱与艺术家合作创作吸引玩家的图像可能是件值得的事.


## 保存游戏进度

### 在桌面设备, 手机和 web 游戏里保存进度
保存游戏状态可以使用 Defold API 函数 `sys.save(filename, data)` 然后使用 `sys.load(filename)` 加载. 可以使用 `sys.get_save_file(application_id, name)` 获取不同系统上文件保存的路径, 一般就是登录用户的 home 文件夹.

### 在游戏主机里保存进度
用 `sys.get_save_file()` 和 `sys.save()` 能在大多数平台上顺利工作, 但是在游戏主机上推荐另一个方法. 游戏主机平台通常将用户与每个连接的手柄相关联, 这样当保存进度时, 成就和其他功能应与其各自的用户相关联.

游戏手柄输入事件将包含一个用户 id, 可用于将手柄的操作与控制台上的用户关联起来.

主机平台及其原生扩展会暴露相关 API 函数，以保存和加载与特定用户关联的数据. 在主机上使用这些 API 以实现保存和载入游戏.

主机平台的文件操作 API 通常都是异步的. 在给主机开发跨平台游戏时推荐把所有文件操作做成异步的, 不管目标是哪个平台. 例如:

```lua
local function save_game(data, user_id, cb)
	if console then
		local filename = "savegame"
		consoleapi.save(user_id, filename, data, cb)
	else
		local filename = sys.get_save_file("mygame", "savegame" .. user_id)
		local success = sys.save(filename, data)
		cb(success)
	end
end
```


## Build artifacts

确保为每个版本发布 [生成 debug symbols](/manuals/debugging-native-code/#symbolicate-a-callstack) 以便你能对它们进行崩溃调试. 将它们与应用包保存在一起.

确保储存初次打包时在项目根目录生成的 `manifest.private.der` 和 `manifest.public.der` 文件. 它们是游戏包和 manifest 的公钥和私钥. 您需要这些文件才能重新创建游戏的上一个版本.


## 应用优化

参考 [优化教程](/manuals/optimizations) 优化应用的性能, 大小, 内存占用和耗电量.



## 性能
用真机进行调试! 必要的话查找性能瓶颈然后进行优化. 可以使用 [性能分析器](/manuals/profiling) 分析找出代码性能瓶颈.


## 屏幕分辨率
对于具有固定方向和屏幕分辨率的平台: 检查游戏能否在目标平台屏幕分辨率和长宽比上正常运行. 对于具有可变屏幕分辨率和长宽比的平台: 检查游戏是否适用于各种屏幕分辨率和长宽比. 考虑在渲染脚本和摄像机中使用什么样的 [视口映射](/manuals/render/#default-view-projection) 最好.

移动平台可以在 *game.project* 配置中锁定屏幕方向, 或者做好适配确保游戏在横向和纵向模式下都能运行.

* **Display sizes** - 在游戏设计宽高之外的大屏或者小屏上是否显示正常?
  * 渲染脚本中使用的映射和 gui 中的布局会在这里发挥作用.
* **Aspect ratios** - 在游戏设计屏幕比例之外的屏幕上是否显示正常?
  * 渲染脚本中使用的映射和 gui 中的布局会在这里发挥作用.
* **Refresh rate** - 在刷新率高于 60 Hz 的屏幕上是否显示正常?
  * 调整配置 *game.project* 里 Display 部分的 vsync 和 swap interval.  


## 手机刘海和打孔屏
在显示屏上使用小切口 (也叫刘海或者打孔屏) 来安装前置摄像头和传感器变得越来越流行. 将游戏移植到移动设备时, 建议确保没有关键信息放置在刘海 (屏幕上边中间) 或打孔(屏幕左上角) 的位置. 还可以使用 [安全区域扩展](/extension-safearea) 将游戏视图限制在任何刘海或打孔摄像机之外的区域.


## 平台相关指导

### Android
确保你的 [keystore](/manuals/android/#creating-a-keystore) 保存在安全的地方以便后面可以更新你的游戏.


### Consoles
保存每个版本的完整游戏包. 如果要给游戏发补丁就要用到这些文件.


### Nintendo Switch
集成目标平台代码 - 对于 Nintendo Switch 就有一个特殊的扩展包以及很多工具供用户使用.

Defold 的 Nintendo Switch 使用 Vulkan 作为图形后端 - 要使用 [Vulkan 图形后端](https://github.com/defold/extension-vulkan) 测试游戏.


### PlayStation®4
集成目标平台代码 - 对于 PlayStation®4 就有一个特殊的扩展包以及很多工具供用户使用.


### HTML5
在手机上玩网页游戏正越来越流行 - 当然前提是要确保游戏在手机浏览器可以流畅运行! 还要注意的是网页游戏要能快速载入! - 换句话说就是优化游戏体积. 同时还要考虑加载速度，以免造成不必要的玩家流失.

2018 年, 浏览器引入了声音自动播放策略. 该策略阻止游戏和其他 Web 内容播放声音, 直到用户交互事件 (触摸, 按钮, 游戏手柄事件等) 发生. 在移植到 HTML5 时必须考虑到这一点, 仅在第一次用户交互时才开始播放声音和音乐. 尝试在任何用户交互之前就播放声音, 将在浏览器开发人员控制台中记录为错误, 但不会影响游戏运行.

还要确保显示广告的时候暂停掉游戏里的所有声音.
