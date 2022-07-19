---
title: 编辑器配置
brief: 可以通过设置窗口修改编辑器配置.
---

# 编辑器配置

可以通过设置窗口修改编辑器配置. 选择菜单栏 <kbd>File -> Preferences</kbd> 即可打开设置窗口.

## General

![](images/editor/preferences_general.png)

Enable Texture Compression
: 开启编译 [纹理压缩](/manuals/texture-profiles).

Escape Quits Game
: 用 <kbd>Esc</kbd> 键关闭正在运行的编译好的游戏.

Track Active Tab in Asset Browser
: 在 *编辑器* 面板编辑的文件自动在资源浏览器 (也叫 *Asset* 面板) 中选中.

Path to custom keymap
: [自定义快捷键](/manuals/editor-keyboard-shortcuts) 配置文件的绝对路径.

Code editor font
: 编码窗口所使用的系统字体.


## Code

![](images/editor/preferences_code.png)

Custom Editor
: 自定义编辑器的绝对路径. 在 macOS 上应指向 .app 内的可执行程序 (比如 `/Applications/Atom.app/Contents/MacOS/Atom`).

Open File
: 自定义编辑器开启时要打开的文件的表达式. 其中 `{file}` 在开启时会被真实文件名代替.

Open File at Line
: 自定义编辑器开启时要打开的文件以及指定光标放置的行数. 表达式 `{file}` 在开启时会被真是文件名代替, 而 `{line}` 被行号代替.


## Extensions

![](images/editor/preferences_extensions.png)

Build Server
: 编译包含 [原生扩展](/manuals/extensions) 项目时使用的编译服务器的 URL. 可以在编译服务器的请求 URL 中加入用户名和验证令牌. 使用格式举例: `username:token@build.defold.com`. 在使用用户自己的编译服务器并开启认证时, 任天堂 Switch 编译需要这种用户认证 ([更多信息详见编译服务器文档](https://github.com/defold/extender/blob/dev/README_SECURITY.md)). 其中用户名和密码可以用系统环境变量 `DM_EXTENDER_USERNAME` 和 `DM_EXTENDER_PASSWORD` 来设置.
