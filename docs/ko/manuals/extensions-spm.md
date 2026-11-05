---
title: iOS 및 macOS 빌드에서 Swift Package Manager 종속성 사용하기
brief: 이 매뉴얼은 Swift Package Manager로 iOS 및 macOS 빌드의 종속성을 해결하는 방법을 설명합니다.
---

# Swift Package Manager {#swift-package-manager}

[Swift Package Manager](https://www.swift.org/documentation/package-manager/)는 Swift와 Xcode에 내장된 종속성 관리자입니다. 많은 iOS 및 macOS SDK가 Swift 패키지로 배포되며, 일부는 더 이상 CocoaPods로 배포되지 않습니다. Defold는 엔진을 빌드할 때 Xcode를 사용하지 않지만, 빌드 서버는 익스텐션이 의존하는 Swift 패키지를 다운로드하고 빌드할 때 Xcode를 사용합니다. 결과는 [CocoaPods 종속성](/manuals/extensions-cocoapods)과 같은 방식으로 엔진에 링크됩니다.

CocoaPods와 Swift 패키지는 같은 프로젝트에서, 심지어 같은 익스텐션에서도 함께 사용할 수 있습니다.

## 종속성 선언하기 {#declaring-dependencies}

네이티브 익스텐션은 `manifests/ios`와 `manifests/osx` 폴더에 `SwiftPackages.json` 파일을 포함하여 필요한 Swift 패키지를 지정할 수 있습니다. 예:

```json
{
  "platform": "ios",
  "minVersion": "15.0",
  "packages": [
    {
      "url": "https://github.com/firebase/firebase-ios-sdk.git",
      "version": "12.16.0",
      "products": ["FirebaseCore", "FirebaseInstallations"]
    }
  ]
}
```

파일은 일반 JSON입니다. `Package.swift`를 직접 작성할 필요는 없으며, 빌드 서버가 모든 익스텐션의 `SwiftPackages.json` 파일에서 생성합니다.

파일에는 다음 필드가 들어 있습니다:

* `platform` - 필수입니다. `manifests/ios/SwiftPackages.json`에서는 `"ios"`, `manifests/osx/SwiftPackages.json`에서는 `"osx"`입니다.
* `minVersion` - 선택 사항입니다. 패키지를 빌드할 최소 iOS 또는 macOS 버전으로, 예를 들어 `"15.0"`입니다. 패키지 빌드와 엔진 링크 모두에서 모든 익스텐션의 값과 엔진이 지원하는 최소 버전 중 가장 높은 값을 사용합니다.
* `wrapperType` - 선택 사항입니다. `"static"`(기본값) 또는 `"dynamic"`입니다. 아래의 [정적 및 동적 링크](#static-and-dynamic-linking)를 참고하세요.
* `packages` - 필수입니다. 패키지 목록입니다. 각 패키지에는 다음 필드가 있습니다:
  * `url` - 패키지 git 저장소의 `https://` URL입니다. 자격 증명, 사용자 지정 포트, 쿼리 문자열이 있는 URL과 `ssh` URL은 허용하지 않으므로 저장소에 공개적으로 접근할 수 있어야 합니다.
  * `products` - 엔진에 링크할 패키지의 제품입니다. 패키지의 `Package.swift` 파일에서 `products` 섹션에 나열된 라이브러리 제품입니다. 제품 이름이 패키지 이름이나 임포트할 모듈 이름과 반드시 같은 것은 아닙니다.
  * 정확히 하나의 버전 요구 사항:
    * `version` - 정확히 이 버전입니다. 예: `"12.16.0"`.
    * `from` - 이 버전 또는 같은 주 버전을 갖는 이후 버전입니다. 예를 들어 `"9.0.0"`은 최신 `9.x.x` 릴리스로 해결됩니다.
    * `branch` - 지정 브랜치의 최신 커밋입니다. 예: `"main"`.
    * `revision` - 전체 40자 커밋 해쉬로 지정한 특정 커밋입니다.

빌드 서버는 모든 익스텐션의 `SwiftPackages.json` 파일을 모아 패키지 자체의 종속성을 포함한 모든 종속성을 해결하고, 네이티브 코드 빌드에 포함합니다.

## 익스텐션 코드에서 패키지 사용하기 {#using-packages-from-extension-code}

익스텐션 소스 코드에서 제품의 헤더를 사용할 수 있습니다. Objective-C++(`.mm`) 소스 파일에서 사용하세요. 다음 예제는 어플리케이션이 시작될 때 [Sentry](https://github.com/getsentry/sentry-cocoa) SDK를 시작합니다:

`manifests/ios/SwiftPackages.json`:

```json
{
  "platform": "ios",
  "minVersion": "15.0",
  "packages": [
    {
      "url": "https://github.com/getsentry/sentry-cocoa.git",
      "from": "9.0.0",
      "products": ["Sentry"]
    }
  ]
}
```

`src/myextension.mm`:

```cpp
#include <dmsdk/sdk.h>

#if defined(DM_PLATFORM_IOS)
#import <UIKit/UIKit.h>
#import <Sentry/Sentry.h>
#import <Sentry/Sentry-Swift.h>
#endif

static dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
#if defined(DM_PLATFORM_IOS)
    [SentrySDK startWithConfigureOptions:^(SentryOptions* options) {
        options.dsn = @"https://examplePublicKey@o0.ingest.sentry.io/0";
    }];
#endif
    return dmExtension::RESULT_OK;
}
```

* Objective-C 헤더는 `#import <Module/Header.h>`로 임포트하며, `Module`은 헤더를 제공하는 모듈 이름입니다.
* Swift로 구현된 클래스는 생성된 `<Module/Module-Swift.h>` 헤더에 선언됩니다. 여기에는 모듈이 Objective-C에 노출하는 클래스와 메서드(Swift에서 `@objc`로 표시)만 포함됩니다. 생성된 헤더는 `UIKit`(macOS에서는 `AppKit`)의 타입을 사용하므로 이를 먼저 임포트하세요.

## 여러 익스텐션의 종속성 {#dependencies-of-several-extensions}

프로젝트의 여러 익스텐션이 Swift 패키지를 사용하면 해당 플랫폼의 모든 `SwiftPackages.json` 파일이 하나의 패키지 그래프로 결합됩니다:

* URL이 같은 패키지는 병합하고 요청된 제품을 합칩니다.
* 여러 익스텐션이 공유하는 패키지는 모든 익스텐션에서 같은 버전 요구 사항을 사용해야 합니다. 예를 들어 한 익스텐션의 `"version": "12.16.0"`과 다른 익스텐션의 `"from": "12.0.0"`처럼 요구 사항이 다르면 `Conflicting requirements for Swift package` 오류로 빌드가 실패합니다.
* 가장 높은 `minVersion`을 사용합니다.
* `wrapperType`을 설정하는 모든 익스텐션은 같은 값을 설정해야 합니다.

프로젝트에서 CocoaPods를 사용하는 익스텐션과 Swift 패키지를 사용하는 익스텐션을 함께 사용할 수도 있습니다. 두 방식 모두 종속성을 해결하여 엔진에 링크합니다. 단, 같은 SDK를 두 곳에서 가져오면 안 됩니다. 한 익스텐션이 `Podfile`에서 Firebase를 가져오고 다른 익스텐션이 `SwiftPackages.json`에서 가져오면 중복 심볼 오류로 엔진 링크가 실패합니다. SDK를 공유하는 익스텐션은 같은 종속성 관리자를 사용해야 합니다.

## 패키지 버전 잠그기 {#locking-package-versions}

빌드에 성공하면 빌드 서버는 패키지의 종속성을 포함하여 그래프의 모든 패키지의 정확한 버전과 커밋을 나열한 `Package.resolved` 파일을 반환합니다. 이 파일은 `build/arm64-ios/Package.resolved` 같은 프로젝트의 빌드 폴더에 저장됩니다.

패키지 버전을 잠그려면 이 파일을 익스텐션의 `SwiftPackages.json` 옆(예: `manifests/ios/Package.resolved`)에 복사합니다. 빌드 서버는 잠긴 버전이 `SwiftPackages.json`의 요구 사항과 일치하는 동안 그 버전을 사용합니다. 빌드도 빨라집니다. `Package.resolved`가 없으면 빌드 서버가 패키지 종속성을 단계적으로 찾아야 하므로 종속성이 많은 패키지에는 오랜 시간이 걸릴 수 있습니다.

여러 익스텐션이 같은 플랫폼의 `Package.resolved` 파일을 포함하면 그중 하나만 사용합니다.

## 정적 및 동적 링크 {#static-and-dynamic-linking}

기본적으로 모든 Swift 패키지를 하나의 정적 라이브러리로 결합하여 엔진 실행 파일에 링크합니다.

일부 SDK는 정적 라이브러리로 결합할 수 없어서 중복 심볼 오류로 엔진 링크가 실패합니다. 이 경우 `SwiftPackages.json`에서 `"wrapperType": "dynamic"`을 설정하세요. 패키지는 어플리케이션 번들에 포함되는 동적 프레임워크로 빌드됩니다.

## 리소스와 개인정보 보호 메니페스트 {#resources-and-privacy-manifests}

패키지의 리소스 번들과 개인정보 보호 메니페스트(`PrivacyInfo.xcprivacy`)는 CocoaPods 종속성과 같은 방식으로 어플리케이션 번들에 포함됩니다.

## CocoaPods에서 이전하기 {#migrating-from-cocoapods}

많은 SDK는 pod와 Swift 패키지로 모두 배포됩니다. 익스텐션을 `Podfile`에서 `SwiftPackages.json` 파일로 이전하려면:

1. SDK 문서에서 Swift 패키지의 git 저장소를 찾습니다. 보통 pod의 저장소와 같습니다.
2. 패키지의 `Package.swift` 파일에서 제품 이름을 찾습니다. pod 이름과 제품 이름은 다른 경우가 많습니다.
3. `Podfile`을 `SwiftPackages.json` 파일로 교체합니다. `Podfile`의 `platform :ios` 버전은 `minVersion`이 됩니다.
4. 익스텐션의 `#import` 줄이 여전히 제품의 모듈 이름과 일치하는지 확인합니다.

예를 들어 다음 `Podfile`은:

```
platform :ios, '12.0'
pod 'FBSDKCoreKit', '17.0.0'
pod 'FBSDKLoginKit', '17.0.0'
pod 'FBSDKShareKit', '17.0.0'
pod 'FBSDKGamingServicesKit', '17.0.0'
```

다음 `SwiftPackages.json`이 됩니다:

```json
{
  "platform": "ios",
  "minVersion": "12.0",
  "packages": [
    {
      "url": "https://github.com/facebook/facebook-ios-sdk.git",
      "version": "17.0.0",
      "products": ["FacebookCore", "FacebookLogin", "FacebookShare", "FacebookGamingServices"]
    }
  ]
}
```

이 경우 모듈 이름이 유지되므로 `#import <FBSDKCoreKit/FBSDKCoreKit.h>`가 두 방식에서 모두 동작합니다.

## 제한 사항 {#limitations}

* `https://`로 공개적으로 접근할 수 있는 패키지 저장소만 지원합니다. Swift 패키지 레지스트리는 지원하지 않습니다.
* 패키지의 `Package.swift` 파일과 플러그인은 빌드 서버에서 네트워크 접근 없이 실행됩니다. 빌드 서버가 패키지를 빌드하기 전에 패키지와 바이너리 프레임워크를 직접 다운로드합니다.
* iOS용으로 에셋 카탈로그(`.xcassets`)가 있는 패키지를 빌드하려면 Xcode 27 이상을 사용하는 빌드 서버가 필요합니다. 이전 Xcode에서는 해당 패키지 이름을 표시하는 오류와 함께 빌드가 실패합니다.
* 프로젝트의 `SwiftPackages.json` 파일은 플랫폼당 최대 32개 패키지와 64개 제품을 선언할 수 있습니다.

## 문제 해결 {#troubleshooting}

`'Module/Header.h' file not found` 또는 정의되지 않은 심볼
: `SwiftPackages.json`의 `products`가 `Package.swift`의 제품 이름인지, 헤더가 그중 하나에 속하는지 확인하세요. Swift Package Manager를 지원하지 않는 빌드 서버는 `SwiftPackages.json`을 무시하므로 익스텐션의 컴파일이나 링크가 같은 방식으로 실패합니다.

`The Swift package graph did not resolve within the ... time budget`
: 패키지의 종속성이 너무 많아 잠금 파일 없이 찾아낼 수 없습니다. [패키지 버전 잠그기](#locking-package-versions)에 설명된 대로 `SwiftPackages.json` 옆에 `Package.resolved`를 추가하세요. 빌드가 완료되지 않았으므로, 같은 패키지를 Xcode 프로젝트에 추가하는 등의 방법으로 로컬에서 파일을 만듭니다. Xcode는 `<project>.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved`에 파일을 저장합니다.

## 로컬 빌드 서버 {#local-build-server}

Swift 패키지는 macOS 빌드 서버에서 빌드합니다. [로컬 빌드 서버](/manuals/extender-local-setup)에서 Swift 패키지를 사용하려면 전체 Xcode 설치(Command Line Tools만으로는 부족함), [XcodeGen](https://github.com/yonaskolb/XcodeGen), `extender.spm.enabled` 설정으로 활성화한 Swift Package Manager 지원이 필요합니다. 자세한 내용은 [GitHub의 빌드 서버 문서](https://github.com/defold/extender)를 참고하세요.
