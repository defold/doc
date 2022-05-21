#### Q: 为什么编辑器中无纹理的 GUI box 节点透明显示, 但是构建运行后能正常显示?

A: 这个错误发生在 [使用 AMD Radeon GPU 的机器](https://github.com/defold/editor2-issues/issues/2723) 上. 注意更新显卡驱动.

#### Q: 打开图集或者场景视图时报错 'com.sun.jna.Native.open.class java.lang.Error: Access is denied'?

A: 试试以管理员身份打开 Defold. 右键点击 Defold 可执行程序选择 "以管理员身份运行".

#### Q: 爲什麽在 Windows 上使用 Intel UHD 集成 GPU 渲染不正常 (但是 HTML5 版本正常)?

A: 確保你的驅動版本大於等於 27.20.100.8280. 參見 [Intel Driver Support Asistant](https://www.intel.com/content/www/us/en/search.html?ws=text#t=Downloads&layout=table&cf:Downloads=%5B%7B%22actualLabel%22%3A%22Graphics%22%2C%22displayLabel%22%3A%22Graphics%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%7D%5D). 更多信息請見 [這個帖子](https://forum.defold.com/t/sprite-game-object-is-not-rendering/69198/35?u=britzl).