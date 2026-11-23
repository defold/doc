---
title: iOS 및 macOS용 네이티브 익스텐션에서 Swift 사용하기
brief: 이 매뉴얼은 iOS 및 macOS 빌드에 사용할 네이티브 익스텐션 코드를 Swift로 작성하는 방법을 설명합니다.
---

# 네이티브 익스텐션에서 Swift 사용하기 {#swift-in-native-extensions}

StoreKit 2나 CryptoKit처럼 Swift에서만 사용할 수 있는 Apple API가 많습니다. 네이티브 익스텐션(native extension)에는 Objective-C++ 파일과 함께 직접 작성한 Swift 소스 파일을 넣을 수 있습니다. 빌드 서버는 이 파일들을 익스텐션의 나머지 코드와 함께 컴파일한 뒤 그 결과를 엔진에 링크합니다. 이 기능은 [Swift 패키지](/manuals/extensions-spm)나 [CocoaPods](/manuals/extensions-cocoapods)로 미리 만들어진 종속성을 가져오는 것과는 별개입니다.

Swift 코드는 macOS(`arm64` 및 `x86_64`)와 iOS(기기 및 시뮬레이터)용으로 컴파일됩니다. 다른 플랫폼용으로 빌드할 때는 Swift 파일을 무시합니다.


## Swift 소스 파일 추가하기 {#adding-swift-sources}

`.swift` 파일은 C++ 및 Objective-C++ 파일과 함께 익스텐션의 `src` 폴더에 넣습니다.

```
myextension/
├── ext.manifest
└── src/
    ├── myextension.mm
    └── Greeter.swift
```

모든 Swift 파일은 `src`에 두세요. `commonsrc`나 `pluginsrc`에 Swift 파일이 있으면 macOS 또는 iOS 빌드가 실패합니다.

익스텐션에 있는 모든 Swift 파일은 하나의 Swift 모듈로 컴파일됩니다. 모듈 이름은 `ext.manifest`의 `name` 값에서 가져옵니다. 이때 문자, 숫자, 밑줄 이외의 문자는 각각 `_`로 바뀝니다. 예를 들어 `My-Extension`은 `My_Extension`이 됩니다. Swift 언어 모드는 Swift 5입니다.

모듈 이름은 코드에서 임포트하는 다른 모듈의 이름과 달라야 합니다. 예를 들어 `StoreKit`이라는 익스텐션에서는 `import StoreKit`을 사용할 수 없습니다. 컴파일러가 현재 모듈을 다시 임포트하려는 것으로 해석하기 때문입니다.


## Objective-C++에서 Swift 호출하기 {#calling-swift-from-objective-c}

익스텐션의 진입점(entry point)은 여전히 `DM_DECLARE_EXTENSION`으로 등록하는 C++ 함수이므로, 익스텐션에는 `.cpp` 또는 `.mm` 파일이 하나 이상 필요합니다. 이 파일에서 자동으로 생성된 `<Module>-Swift.h` 헤더를 통해 Swift 코드를 호출합니다.

Objective-C에서는 `@objc`로 표시한 클래스, 프로토콜, 메서드만 볼 수 있습니다. 클래스는 `public`으로 선언하고 `NSObject`를 상속하세요.

`src/Greeter.swift`:

```swift
import Foundation

@objc(MyExtensionGreeter)
public class Greeter: NSObject {
    @objc public func message() -> String {
        return "Hello from Swift"
    }
}
```

`src/myextension.mm`:

```cpp
#include <dmsdk/sdk.h>
#import <Foundation/Foundation.h>
#import "MyExtension-Swift.h"

static dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
    MyExtensionGreeter* greeter = [[MyExtensionGreeter alloc] init];
    dmLogInfo("%s", [[greeter message] UTF8String]);
    return dmExtension::RESULT_OK;
}

DM_DECLARE_EXTENSION(MyExtension, "MyExtension", AppInitializeMyExtension, 0, 0, 0, 0, 0)
```

* 생성된 헤더는 `Foundation`을 임포트합니다. 다른 프레임워크의 타입은 이 헤더에 전방 선언(forward declaration)만 되어 있습니다. 이런 타입을 사용하는 메서드를 호출하기 전에 `.mm` 파일에서 해당 프레임워크(예: `UIKit`)의 헤더를 임포트하세요.
* `throws` 함수는 `NSError **` 매개변수가 있는 메서드로, `async` 함수는 완료 핸들러(completion handler)가 있는 메서드로 노출됩니다.
* 제네릭, 연관 값이 있는 열거형, 구조체 등 Swift 전용 기능은 Objective-C에서 볼 수 없습니다. 이런 기능은 `@objc` 클래스로 감싸세요.
* `.mm` 파일은 iOS 및 macOS용으로만 컴파일되므로, `.mm` 파일과 `.swift` 파일만 있는 익스텐션을 다른 플랫폼용으로 빌드하면 `Extension has no source!` 오류가 발생합니다. 다른 플랫폼용으로도 빌드하려면 `DM_DECLARE_EXTENSION`을 `.cpp` 파일에 두고, 그 안에서 `DM_PLATFORM_IOS` 또는 `DM_PLATFORM_OSX`를 검사하는 조건부 컴파일 구역에서만 `.mm` 파일에 구현한 함수를 호출하세요.


## Swift에서 Objective-C 호출하기 {#calling-objective-c-from-swift}

Swift에서 Objective-C 또는 C 선언을 사용하려면 `src` 폴더에 `<Module>-Bridging-Header.h`라는 이름의 브리징 헤더(bridging header)를 추가합니다. 예를 들어 `src/MyExtension-Bridging-Header.h`에 다음과 같이 작성합니다.

```cpp
#import "mynative.h"
```

브리징 헤더가 있으면 Swift 모듈에서 자동으로 임포트합니다. 빌드 시에는 브리징 헤더가 포함하는 다른 헤더를 익스텐션의 `include` 폴더와 아래에서 설명하는 `additionalSwiftIncludePaths`에 지정한 폴더에서 찾습니다.

`Foundation`, `UIKit`, `StoreKit` 같은 Apple 프레임워크는 Swift에서 일반 `import` 구문으로 임포트합니다. `ext.manifest`의 `frameworks` 및 `weakFrameworks`에 나열한 프레임워크는 평소와 같이 링크됩니다. 대부분의 시스템 프레임워크는 Swift 코드에서 임포트하면 자동으로 링크됩니다.


## Swift 코드에서 Swift 패키지 사용하기 {#using-swift-packages-from-swift}

익스텐션의 `SwiftPackages.json`에 선언한 [Swift 패키지](/manuals/extensions-spm)의 제품(product)은 해당 익스텐션의 Swift 코드에서 사용할 수 있습니다. 다음과 같이 Swift 파일에서 모듈을 임포트합니다.

```swift
import Foundation
import Sentry

@objc(MyExtensionCrashReporter)
public class CrashReporter: NSObject {
    @objc public func start(dsn: String) {
        SentrySDK.start { options in
            options.dsn = dsn
        }
    }
}
```

패키지의 Objective-C 헤더는 `.mm` 파일에서와 같은 방식으로 브리징 헤더에서 임포트할 수 있습니다.

`src/MyExtension-Bridging-Header.h`:

```cpp
#import <Sentry/Sentry.h>
```

패키지를 사용하는 익스텐션의 `SwiftPackages.json`에 해당 패키지를 선언하세요. 빌드 서버는 패키지를 먼저 빌드하고 그다음에 익스텐션의 Swift 코드를 빌드합니다. 패키지에 필요한 OS 버전이 엔진의 최소 지원 버전보다 높으면 `SwiftPackages.json`의 `minVersion`에 그 버전을 지정하세요. 그러면 익스텐션의 Swift 코드도 해당 버전을 대상으로 빌드됩니다. Swift 코드에서 CocoaPods 종속성을 직접 사용하는 것은 지원되지 않습니다. Objective-C++ 파일에서 사용하고 Swift 코드에는 필요한 내용을 전달하세요.


## 컴파일러 옵션 {#compiler-options}

Swift 컴파일러 옵션은 `ext.manifest` 파일에서 C++ 컴파일러 옵션과 같은 `context`에 설정합니다.

```yaml
name: MyExtension

platforms:
    ios:
        context:
            defines: ["MY_DEFINE"]
            swiftFlags: ["-strict-concurrency=complete"]
            additionalSwiftIncludePaths: ["include/vendor/headers"]
            additionalFrameworkSearchPaths: ["lib/ios/vendor/frameworks"]
    osx:
        context:
            defines: ["MY_DEFINE"]
```

* `defines` - C++용 전처리기 정의는 Swift에 조건부 컴파일 식별자로 전달되므로 Swift에서도 `#if MY_DEFINE`를 사용할 수 있습니다. Swift는 이름만 지원하므로 `MY_DEFINE=1`과 같이 값을 지정하면 값은 제외됩니다.
* `swiftFlags` - Swift 컴파일러에 전달할 추가 플래그입니다. 플래그와 값은 각각 별도의 목록 항목으로 지정합니다. 허용 목록에 없는 플래그를 지정하면 `Invalid flag - 'swiftFlags'` 오류로 빌드가 실패합니다. 값에 공백 문자, 역슬래시, 템플릿 구문이 포함되어 있거나 값이 응답 파일(response file)을 가리키면 `invalid 'swiftFlags' value` 오류로 실패합니다. 허용되는 플래그는 다음과 같습니다.
  * `-enable-upcoming-feature <Feature>` - 향후 도입될 언어 기능을 활성화합니다. 예를 들어 `["-enable-upcoming-feature", "ExistentialAny"]`와 같이 지정합니다.
  * `-strict-concurrency=minimal|targeted|complete`
  * `-enforce-exclusivity=checked|unchecked`
  * `-O`, `-Osize`, `-Onone` - 최적화 수준입니다. 기본값은 `-O`입니다.
  * `-suppress-warnings`
* `additionalSwiftIncludePaths` - Swift 컴파일러가 헤더와 모듈을 찾을 때 익스텐션의 `include` 폴더 외에 추가로 검색할 폴더입니다.
* `additionalFrameworkSearchPaths` - 익스텐션의 `lib/<platform>` 폴더 외에 프레임워크를 추가로 검색할 폴더입니다. Swift 컴파일러뿐 아니라 익스텐션의 소스 파일을 컴파일하는 C++ 및 Objective-C++ 컴파일러와 링커도 이 폴더를 검색합니다.

경로는 익스텐션 폴더를 기준으로 하는 상대 경로여야 하며, 이 폴더 밖을 가리킬 수 없습니다. 경로에는 문자, 숫자, `._+-/`만 사용할 수 있습니다. 빌드 서버에는 익스텐션의 `include`, `src`, `commonsrc`, `pluginsrc`, `lib/<platform>`, `manifests/<platform>`, `res/<platform>` 폴더만 전송되므로 경로는 이 폴더 중 하나를 가리키거나 그 안에 있어야 합니다. 익스텐션 최상위의 `vendor` 폴더처럼 다른 폴더에 있는 파일은 빌드 중에 사용할 수 없습니다.

`ios` 플랫폼의 Swift 키는 기기와 시뮬레이터 빌드에 모두 적용됩니다. Swift를 지원하기 전의 빌드 서버는 이 키를 거부하고 `Manifest context variable unsupported` 오류를 냅니다. 이 경우 Defold 버전과 빌드 서버를 모두 업데이트해야 프로젝트를 빌드할 수 있습니다.


## 최소 OS 버전 {#minimum-os-versions}

Defold가 지원하는 모든 iOS 및 macOS 버전에는 Swift 런타임이 포함되어 있습니다. Swift 코드는 빌드에 지정된 최소 iOS 또는 macOS 버전을 대상으로 컴파일되며, 어플리케이션은 운영 체제의 Swift 런타임을 사용합니다. 최소 버전보다 나중에 추가된 API를 호출하기 전에는 `#available`로 사용 가능 여부를 확인하세요.

런타임의 일부 기능은 더 높은 버전의 운영 체제에만 포함되어 있습니다. 예를 들어 `MutableSpan`과 관련 타입은 iOS 26 및 macOS 26부터 제공됩니다. 최소 버전이 이보다 낮은데 Swift 코드나 패키지의 동적 프레임워크에서 이런 기능을 사용한다면, 이전 OS를 사용하는 기기에서 어플리케이션을 실행할 때 추가 라이브러리가 필요할 수 있습니다. 이를 위해 따로 설정할 필요는 없습니다. 빌드 서버가 Xcode와 같은 방식으로 엔진과 번들에 포함된 동적 라이브러리를 검사해 이들이 사용하는 라이브러리를 찾아 어플리케이션에 추가합니다. iOS에서는 이 라이브러리들이 어플리케이션의 `Frameworks` 폴더에 들어가며 나머지 코드와 함께 서명됩니다.

빌드의 최소 OS 버전은 엔진이 지원하는 최소 버전이며, Defold 버전과 빌드 서버에 따라 결정됩니다. [Swift Package Manager 매뉴얼](/manuals/extensions-spm)에서 설명하듯이 `SwiftPackages.json`의 `minVersion`으로 이 버전을 높이면 패키지 빌드, Swift 코드 컴파일, 엔진 링크에 모두 적용됩니다. 최소 버전을 낮출 수는 없습니다.


## 제한 사항 {#limitations}

* 익스텐션에는 `DM_DECLARE_EXTENSION`이 있는 C++ 또는 Objective-C++ 파일이 여전히 필요합니다. Swift 코드에서는 익스텐션을 등록할 수 없고 Defold SDK(`dmsdk`)의 C++ API도 사용할 수 없으므로 이 API는 Objective-C++ 파일에서 호출하세요. `dmsdk/dlib/hash.h`처럼 C와 호환되는 `dmsdk` 헤더는 브리징 헤더에 포함할 수 있습니다. `.swift` 파일만 있으면 링크 단계에서 익스텐션 이름에 해당하는 심볼이 정의되지 않았다는 오류가 발생합니다.
* Swift 코드에서 CocoaPods 종속성을 직접 사용하는 것은 지원되지 않습니다. Objective-C++ 파일에서 사용하고 Swift 코드에는 필요한 내용을 전달하세요.
* Swift 5 언어 모드만 지원합니다. C++ 상호 운용 기능은 활성화되어 있지 않습니다.
* Swift 소스 파일은 Defold 1.14.2부터 지원합니다. 이전 버전의 SDK를 사용하는 빌드 서버에서는 `Swift sources are not supported by this Defold SDK version` 오류로 빌드가 실패합니다.
* `library` 빌드 산출물([Bob](/manuals/bob)의 `--build-artifacts library`)을 만들 때는 Swift 소스 파일이 컴파일되지 않습니다. 따라서 `<Module>-Swift.h`를 임포트하는 Objective-C++ 파일은 이 빌드에서 컴파일에 실패합니다.


## 문제 해결 {#troubleshooting}

`no such module 'Name'`
: `SwiftPackages.json`에 선언된 패키지의 제품 중 이 모듈을 제공하는 것이 없습니다. [Swift Package Manager 매뉴얼](/manuals/extensions-spm)을 참고하여 모듈을 제공하는 제품이 `products`에 있는지 확인하세요.

`Swift sources are only supported in the 'src' folder`
: `.swift` 파일을 익스텐션의 `src` 폴더로 옮기세요.

`'MyExtension-Swift.h' file not found`
: 모듈 이름은 `ext.manifest`의 `name` 값으로 정해집니다. `#import` 줄에 쓴 이름을 확인하세요.

`unknown type name 'MyExtensionGreeter'`
: 생성된 헤더에 클래스가 없습니다. 클래스에 `public`과 `@objc`를 표시했는지, `NSObject`를 상속하는지, `.mm` 파일에서 `@objc(...)`에 지정한 이름을 사용하는지 확인하세요.

`cannot find 'AppStore' in scope`와 `file 'A.swift' is part of module 'StoreKit'; ignoring import`가 함께 표시되는 경우
: 익스텐션의 이름이 임포트하는 모듈의 이름과 같습니다. `ext.manifest`에서 익스텐션 이름을 바꾸세요.

`Undefined symbols ... _MyExtension`
: 익스텐션에 `DM_DECLARE_EXTENSION`이 없습니다. 위에서 설명한 대로 익스텐션을 등록하는 `.mm` 파일을 추가하세요.

`Invalid flag - 'swiftFlags'`
: 허용 목록에 없는 플래그입니다. 해당 플래그를 제거하거나 목록에 있는 플래그를 사용하세요.

`invalid 'swiftFlags' value`
: 값에 공백 문자, 역슬래시, 템플릿 구문이 포함되어 있거나 값이 응답 파일을 가리킵니다. 각 플래그와 각 값을 별도의 목록 항목에 넣으세요.
