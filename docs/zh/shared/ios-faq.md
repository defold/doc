#### Q: 我无法使用免费的 Apple Developer 账户安装我的 Defold 游戏。
A: 请确保您在 Defold 项目中使用的 bundle identifier 与您在生成移动设备配置文件时在 Xcode 项目中使用的 bundle identifier 相同。

#### Q: 如何检查捆绑应用程序的权限？
A: 来自 [检查构建应用程序的权限](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-APPENTITLEMENTS)：

```sh
codesign -d --ent :- /path/to/the.app
```

#### Q: 如何检查配置文件的权限？
A: 来自 [检查配置文件的权限](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-PROFILESENTITLEMENTS)：

```sh
security cms -D -i /path/to/iOSTeamProfile.mobileprovision
```
