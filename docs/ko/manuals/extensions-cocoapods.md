---
title: iOS 및 macOS 빌드에서 CocoaPods 종속성 사용하기
brief: 이 매뉴얼은 iOS 및 macOS 빌드에서 CocoaPods로 종속성을 해결하는 방법을 설명합니다.
---

# CocoaPods

[CocoaPods](https://cocoapods.org/)는 Swift 및 Objective-C Cocoa 프로젝트용 종속성 관리자입니다. CocoaPods는 일반적으로 Xcode 프로젝트에서 종속성을 관리하고 통합하는 데 사용됩니다. Defold는 iOS 및 macOS용으로 빌드할 때 Xcode를 사용하지 않지만, 빌드 서버에서 종속성을 해결하기 위해 여전히 CocoaPods를 사용합니다.


## 종속성 해결하기

네이티브 익스텐션은 익스텐션 종속성을 지정하기 위해 `manifests/ios` 및 `manifests/osx` 폴더에 `Podfile` 파일을 포함할 수 있습니다. 예:

```
platform :ios '11.0'

pod 'FirebaseCore', '10.22.0'
pod 'FirebaseInstallations', '10.22.0'
```

빌드 서버는 모든 익스텐션에서 `Podfile` 파일을 수집하고, 이를 사용해 모든 종속성을 해결한 뒤 네이티브 코드를 빌드할 때 포함합니다.

예:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/ios/Podfile)
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/ios/Podfile)
