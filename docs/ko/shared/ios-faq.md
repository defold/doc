#### Q: 무료 Apple Developer 계정으로 Defold 게임을 설치할 수 없습니다.
A: mobile provisioning profile을 생성할 때 Xcode 프로젝트에서 사용한 bundle identifier와 Defold 프로젝트에서 사용하는 bundle identifier가 같은지 확인하세요.

#### Q: 번들된 어플리케이션의 entitlements는 어떻게 확인할 수 있나요?
A: [빌드된 앱의 entitlements 검사](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-APPENTITLEMENTS)에서:

```sh
codesign -d --ent :- /path/to/the.app
```

#### Q: provisioning profile의 entitlements는 어떻게 확인할 수 있나요?
A: [프로파일의 entitlements 검사](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-PROFILESENTITLEMENTS)에서:

```sh
security cms -D -i /path/to/iOSTeamProfile.mobileprovision
```
