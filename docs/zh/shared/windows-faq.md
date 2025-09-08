#### Q: 为什么编辑器中无纹理的 GUI 框节点透明显示，但是构建运行后能正常显示？

A: 这个错误发生在 [使用 AMD Radeon GPU 的计算机](https://github.com/defold/editor2-issues/issues/2723) 上。请确保更新您的显卡驱动。

#### Q: 打开图集或者场景视图时报错 `com.sun.jna.Native.open.class java.lang.Error: Access is denied`？

A: 尝试以管理员身份运行 Defold。右键点击 Defold 可执行程序并选择"以管理员身份运行"。

#### Q: 为什么在 Windows 上使用 Intel UHD 集成 GPU 渲染不正常（但是 HTML5 版本正常）？

A: 确保您的驱动版本高于或等于 27.20.100.8280。请查看 [Intel 驱动程序支持助手](https://www.intel.com/content/www/us/en/search.html?ws=text#t=Downloads&layout=table&cf:Downloads=%5B%7B%22actualLabel%22%3A%22Graphics%22%2C%22displayLabel%22%3A%22Graphics%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%7D%5D)。更多信息请参见 [此论坛帖子](https://forum.defold.com/t/sprite-game-object-is-not-rendering/69198/35?u=britzl)。

#### Q: Defold 编辑器崩溃，日志显示 `AWTError: Assistive Technology not found`

如果编辑器崩溃，日志提示 `Caused by: java.awt.AWTError: Assistive Technology not found: com.sun.java.accessibility.AccessBridge`，请按照以下步骤操作：

* 导航到 `C:\Users\<用户名>`
* 使用标准文本编辑器（记事本即可）打开名为 `.accessibility.properties` 的文件
* 在配置中找到以下几行：

```
assistive_technologies=com.sun.java.accessibility.AccessBridge
screen_magnifier_present=true
```

* 在这些行的前面添加井号（`#`）
* 保存对文件的更改并重新启动 Defold
