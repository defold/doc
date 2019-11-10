---
title: 编写代码
brief: 本教程简述了Defold中编写代码的事项.
---

# 编写代码

Defold 可以让你使用编辑器的可视工具来创建许多游戏必要的东西，比如瓷砖地图和粒子特效，但是对于游戏逻辑还是得写代码. 游戏逻辑使用 [Lua 语言](https://www.lua.org/) ，引擎扩展使用目标平台的原生开发语言.

Defold 中内建编辑器可以打开和编辑 Lua 文件 (.lua), Defold 脚本文件 (.script, .gui_script 与 .render_script) 或者其他各类文件. 但只对Lua和脚本文件提供代码高亮.

## 编写Lua脚本

Defold 使用 Lua 5.1 和 LuaJIT (与目标平台相关) 并且需要遵循 Lua 该版本的书写规范来编写代码. 关于 Defold 中 Lua 使用详情请见 [Defold中Lua使用手册](/manuals/lua).

## 编写扩展代码

Defold 允许使用原生代码来扩展游戏引擎以使用引擎所不具备的特定功能. 或者 Lua 性能不良时 (密集计算, 图像处理等) 考虑使用原生扩展. 详情请见 [原生扩展手册](/manuals/extensions/).

## 使用第三方代码编辑器

尽管 Defold 提供了编写脚本的基本功能, 但是对于需求更多功能的专业开发者来说还是希望让 Defold 使用自己喜欢的第三方编辑器. 在 Code 页的 Preferences 窗口中可以指定使用第三方编辑器.

Defold 社区为许多编辑器提供了代码提示支持，如 [Atom](https://atom.io/packages/defold-ide), [Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=selimanac.defold-vsc-snippets) 和 [Sublime](https://forum.defold.com/t/full-autocomplete-defold-api-for-sublime-text-3/10910). 此外还有API参照表 [Dash and Zeal](https://forum.defold.com/t/defold-docset-for-dash/2417).
