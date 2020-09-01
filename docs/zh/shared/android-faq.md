#### Q: 安卓系统有办法隐藏导航栏和状态栏吗?
A: 有, 在你的 *game.project* 文件的 *Android* 部分的 *immersive_mode* 项. 这项可以使你获得全部的屏幕及屏幕触摸事件.


#### Q: 在设备上安装 Defold 游戏时总是出现 "Failure [INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES]" 错误?
A: 安卓系统发现你的更新app使用了新的证书. 打包调试版本时, 使用的是一个临时证书. 所以在更新版本前要删除旧版本:

```
$ adb uninstall com.defold.examples
Success
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
      pkg: /data/local/tmp/Defold examples.apk
Success
```
