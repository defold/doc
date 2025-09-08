#### Q: 是否可以在 Android 上隐藏导航栏和状态栏？
A: 是的，在您的 *game.project* 文件的 *Android* 部分设置 *immersive_mode* 选项。这可以让您的应用程序占据整个屏幕并捕获屏幕上的所有触摸事件。


#### Q: 在设备上安装 Defold 游戏时，为什么会出现 "Failure [INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES]" 错误？
A: Android 检测到您尝试使用新证书安装应用程序。打包调试版本时，每个版本都将使用临时证书签名。在安装新版本之前，请卸载旧的应用程序：

```
$ adb uninstall com.defold.examples
Success
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
      pkg: /data/local/tmp/Defold examples.apk
Success
```

#### Q: 为什么在使用某些扩展构建时，会出现关于 AndroidManifest.xml 中属性冲突的错误？
A: 当两个或多个扩展提供包含相同属性标签但值不同的 Android Manifest 存根时，可能会发生这种情况。例如，Firebase 和 AdMob 就曾发生过这种情况。构建错误类似于以下内容：

```
SEVERE: /tmp/job4531953598647135356/upload/AndroidManifest.xml:32:13-58
Error: Attribute property#android.adservices.AD_SERVICES_CONFIG@resource
value=(@xml/ga_ad_services_config) from AndroidManifest.xml:32:13-58 is also
present at AndroidManifest.xml:92:13-59 value=(@xml/gma_ad_services_config).
Suggestion: add 'tools:replace="android:resource"' to <property> element at
AndroidManifest.xml to override. 
```

您可以在报告的 Defold 问题 [#9453](https://github.com/defold/defold/issues/9453#issuecomment-2367367269) 和 Google 问题 [#327696048](https://issuetracker.google.com/issues/327696048?pli=1) 中阅读有关此问题和解决方法的更多信息。
