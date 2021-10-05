#### Q: 使用免費 Apple Developer 賬戶無法安裝 Defold 游戲.
A: 請確保游戲包 id 與 Defold 導出的 Xcode 項目檔案裏設置的 id 是一致的.

#### Q: 如何查看应用包的权限?
A: 参见 [应用的权限检查](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-APPENTITLEMENTS):

> $ codesign -d --ent :- /path/to/the.app

#### Q: 如何查看配置档案的权限?
A: 参见 [档案设置的权限检查](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-PROFILESENTITLEMENTS):

> $ security cms -D -i /path/to/iOSTeamProfile.mobileprovision
