---
title: 编写代码
brief: 本教程简述了Defold中编写代码的事项.
---

# 编写代码

Defold 可以让你使用编辑器的可视工具来创建许多游戏必要的东西, 比如瓷砖地图和粒子特效, 但是对于游戏逻辑还是得写代码. 游戏逻辑使用 [Lua 语言](https://www.lua.org/) , 引擎扩展使用目标平台的原生开发语言.

## 编写Lua脚本

Defold 使用 Lua 5.1 和 LuaJIT (与目标平台相关) 并且需要遵循 Lua 该版本的书写规范来编写代码. 关于 Defold 中 Lua 使用详情请见 [Defold中Lua使用教程](/manuals/lua).

## 编写原生代码

Defold 允许使用原生代码来扩展游戏引擎以使用引擎所不具备的特定功能. 或者 Lua 性能不良时 (密集计算, 图像处理等) 考虑使用原生扩展. 详情请见 [原生扩展教程](/manuals/extensions/).

## Using the built-in code editor

Defold 中内建编辑器可以打开和编辑 Lua 文件 (.lua), Defold 脚本文件 (.script, .gui_script 与 .render_script) 或者其他各类文件. 但只对Lua和脚本文件提供代码高亮.

![](/images/editor/code-editor.png)


### 代码补全

内置代码编辑器写代码时会出现代码补全功能:

![](/images/editor/codecompletion.png)

按 <kbd>CTRL</kbd> + <kbd>Space</kbd> 会出现函数, 参数和返回值的相关信息:

![](/images/editor/apireference.png)


### 使用 LSP 进行 Lua 代码 linting

Defold 支持 [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) 的子集, 可用于分析代码并将程序语句和错误进行高光显示, 这个处理被叫做 linting.

Lua language server 和 code linter 作为插件可用. 使用 [加入依赖](/manuals/libraries/#setting-up-library-dependencies) 的功能安装插件:

```
https://github.com/defold/lua-language-server/releases/download/v0.0.5/release.zip
```

可用的版本可以在插件的 [发布页面](https://github.com/defold/lua-language-server/releases) 上查看. 关于该插件详细信息参见 [Defold 论坛的插件支持页面](https://forum.defold.com/t/linting-in-the-code-editor/72465).


## 使用第三方代码编辑器

尽管 Defold 提供了编写脚本的基本功能, 但是对于需求更多功能的专业开发者来说还是希望让 Defold 使用自己喜欢的第三方编辑器. 在 [Code 页下的 Preferences 窗口 ](/manuals/editor-preferences/#code) 中可以指定使用第三方编辑器.

### Visual Studio Code - Defold Kit

Defold Kit 是一个 Visual Studio Code 插件, 其包含如下功能:

* 安装推荐扩展
* Lua 高光, 自动补全和 linting
* 将相关设置应用于工作区
* Defold API 的 Lua 提示
* 依赖库的 Lua 提示
* 编译和运行
* 断点和调试
* 跨平台编译
* 在连接的设备上运行应用

安装 Defold Kit 详情参考 [Visual Studio 商店页面](https://marketplace.visualstudio.com/items?itemName=astronachos.defold).


## 文档工具

社区创建的 API 参考包可用于 [Dash 和 Zeal](https://forum.defold.com/t/defold-docset-for-dash/2417).
