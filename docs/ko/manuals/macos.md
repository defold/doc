---
title: macOS 플랫폼을 위한 Defold 개발
brief: 이 매뉴얼은 macOS에서 Defold 어플리케이션을 빌드하고 실행하는 방법을 설명합니다.
---

# macOS 개발

macOS 플랫폼용 Defold 어플리케이션 개발은 고려할 사항이 거의 없어 간단한 과정입니다.

## 프로젝트 설정

macOS 전용 어플리케이션 구성은 *game.project* 설정 파일의 [macOS section](/manuals/project-settings/#macos)에서 수행합니다.

## 어플리케이션 아이콘

macOS 게임에 사용되는 어플리케이션 아이콘은 .`icns` 포멧이어야 합니다. `.iconset`으로 모은 `.png` 파일 세트에서 `.icns` 파일을 쉽게 만들 수 있습니다. [`.icns` 파일 생성에 대한 공식 안내](https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Optimizing/Optimizing.html)를 따르세요. 관련 단계의 간단한 요약은 다음과 같습니다.

* 아이콘용 폴더를 생성합니다. 예: `game.iconset`
* 생성한 폴더에 아이콘 파일을 복사합니다.

    * `icon_16x16.png`
    * `icon_16x16@2x.png`
    * `icon_32x32.png`
    * `icon_32x32@2x.png`
    * `icon_128x128.png`
    * `icon_128x128@2x.png`
    * `icon_256x256.png`
    * `icon_256x256@2x.png`
    * `icon_512x512.png`
    * `icon_512x512@2x.png`

* `iconutil` 커맨드 라인 도구를 사용해 `.iconset` 폴더를 `.icns` 파일로 변환합니다.

```
iconutil -c icns -o game.icns game.iconset
```

## 어플리케이션 배포하기
Mac App Store에 어플리케이션을 배포하거나, Steam 또는 itch.io 같은 서드파티 스토어 또는 포털을 사용하거나, 웹사이트를 통해 직접 배포할 수 있습니다. 어플리케이션을 배포하기 전에 제출을 위해 준비해야 합니다. 어플리케이션을 어떤 방식으로 배포하려는지와 관계없이 다음 단계가 필요합니다.

1. 실행 권한을 추가해 누구나 게임을 실행할 수 있게 합니다(기본값은 파일 소유자에게만 실행 권한이 있는 것입니다).

```
$ chmod +x Game.app/Contents/MacOS/Game
```

2. 게임에 필요한 권한을 지정하는 entitlements 파일을 생성합니다. 대부분의 게임에는 다음 권한이면 충분합니다.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.allow-dyld-environment-variables</key>
    <true/>
  </dict>
</plist>
```

  * `com.apple.security.cs.allow-jit` - 앱이 MAP_JIT 플래그를 사용해 쓰기와 실행이 가능한 메모리를 생성할 수 있는지를 나타냅니다.
  * `com.apple.security.cs.allow-unsigned-executable-memory` - 앱이 MAP_JIT 플래그 사용으로 부과되는 제한 없이 쓰기와 실행이 가능한 메모리를 생성할 수 있는지를 나타냅니다.
  * `com.apple.security.cs.allow-dyld-environment-variables` - 앱의 프로세스에 코드를 주입하는 데 사용할 수 있는 dynamic linker environment variables의 영향을 앱이 받을 수 있는지를 나타냅니다.

일부 어플리케이션은 추가 entitlements가 필요할 수도 있습니다. Steamworks 익스텐션에는 다음 추가 entitlement가 필요합니다.

```
<key>com.apple.security.cs.disable-library-validation</key>
<true/>
```

    * `com.apple.security.cs.disable-library-validation` - 앱이 code signing 없이 임의의 plug-in 또는 framework를 로드할 수 있는지를 나타냅니다.

어플리케이션에 부여할 수 있는 모든 entitlements는 공식 [Apple developer documentation](https://developer.apple.com/documentation/bundleresources/entitlements)에 나열되어 있습니다.

3. `codesign`을 사용해 게임에 서명합니다.

```
$ codesign --force --sign "Developer ID Application: Company Name" --options runtime --deep --timestamp --entitlements entitlement.plist Game.app
```

## Mac App Store 외부에 배포하기
Apple은 Mac App Store 외부에서 배포되는 모든 소프트웨어가 macOS Catalina에서 기본적으로 실행되려면 Apple의 공증(notarization)을 받아야 한다고 요구합니다. Xcode 외부의 스크립트 빌드 환경에 공증을 추가하는 방법은 [공식 문서](https://developer.apple.com/documentation/xcode/notarizing_macos_software_before_distribution/customizing_the_notarization_workflow)를 참고하세요. 관련 단계의 간단한 요약은 다음과 같습니다.

1. 위에서 설명한 권한 추가와 어플리케이션 서명 단계를 따릅니다.

2. `altool`을 사용해 게임을 zip으로 압축하고 공증을 위해 업로드합니다.

```
$ xcrun altool --notarize-app
               --primary-bundle-id "com.acme.foobar"
               --username "AC_USERNAME"
               --password "@keychain:AC_PASSWORD"
               --asc-provider <ProviderShortname>
               --file Game.zip

altool[16765:378423] No errors uploading 'Game.zip'.
RequestUUID = 2EFE2717-52EF-43A5-96DC-0797E4CA1041
```

3. `altool --notarize-app` 호출에서 반환된 request UUID를 사용해 제출 상태를 확인합니다.

```
$ xcrun altool --notarization-info 2EFE2717-52EF-43A5-96DC-0797E4CA1041
               -u "AC_USERNAME"
```

4. 상태가 `success`가 될 때까지 기다린 뒤 공증 티켓(notarization ticket)을 게임에 붙입니다.

```
$ xcrun stapler staple "Game.app"
```

5. 이제 게임을 배포할 준비가 되었습니다.

## Mac App Store에 배포하기
Mac App Store에 배포하는 과정은 [Apple Developer documentation](https://developer.apple.com/macos/submit/)에 잘 문서화되어 있습니다. 제출하기 전에 위에서 설명한 대로 어플리케이션에 권한을 추가하고 `codesign`을 수행해야 합니다.

참고: Mac App Store에 배포할 때는 게임을 공증하지 않아도 됩니다.

:[Apple Privacy Manifest](../shared/apple-privacy-manifest.md)
