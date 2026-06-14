---
title: 네이티브 익스텐션 - 익스텐션 메니페스트
brief: 이 매뉴얼은 익스텐션 메니페스트와 어플리케이션 메니페스트 및 엔진 메니페스트의 관계를 설명합니다.
---

# 익스텐션, 어플리케이션 및 엔진 메니페스트 파일

익스텐션 메니페스트는 단일 익스텐션을 빌드할 때 사용되는 flags와 defines가 들어 있는 설정 파일입니다. 이 설정은 어플리케이션 레벨 설정 및 Defold 엔진 자체의 기본 레벨 설정과 결합됩니다.

## 어플리케이션 메니페스트

어플리케이션 메니페스트(파일 확장자 `.appmanifest`)는 빌드 서버에서 게임을 빌드하는 방법을 정의하는 어플리케이션 레벨 설정입니다. 어플리케이션 메니페스트를 사용하면 사용하지 않는 엔진 일부를 제거할 수 있습니다. 물리 엔진이 필요하지 않다면 실행 파일에서 제거해 크기를 줄일 수 있습니다. 사용하지 않는 기능을 제외하는 방법은 [어플리케이션 메니페스트 매뉴얼](/manuals/app-manifest)에서 알아보세요.

## 엔진 메니페스트

Defold 엔진에는 엔진과 Defold SDK의 각 릴리스에 포함되는 빌드 메니페스트(`build.yml`)가 있습니다. 이 메니페스트는 사용할 SDK 버전, 실행할 컴파일러, 링커 및 기타 도구, 그리고 이 도구들에 전달할 기본 빌드 및 링크 flags를 제어합니다. 이 메니페스트는 share/extender/build_input.yml [GitHub에서](https://github.com/defold/defold/blob/dev/share/extender/build_input.yml) 확인할 수 있습니다.

## 익스텐션 메니페스트

반면 익스텐션 메니페스트(`ext.manifest`)는 익스텐션 전용 설정 파일입니다. 익스텐션 메니페스트는 익스텐션의 소스 코드를 컴파일하고 링크하는 방법과 포함할 추가 라이브러리를 제어합니다.

세 가지 메니페스트 파일은 모두 같은 문법을 공유하므로 병합할 수 있으며, 익스텐션과 게임이 빌드되는 방식을 완전히 제어할 수 있습니다.

빌드되는 각 익스텐션에 대해 메니페스트는 다음과 같이 결합됩니다:

	manifest = merge(game.appmanifest, ext.manifest, build.yml)

이를 통해 사용자는 엔진과 각 익스텐션의 기본 동작을 덮어쓸 수 있습니다. 또한 최종 링크 단계에서는 어플리케이션 메니페스트와 Defold 메니페스트를 병합합니다:

	manifest = merge(game.appmanifest, build.yml)


### ext.manifest 파일

익스텐션 이름 외에도 메니페스트 파일에는 플랫폼별 컴파일 flags, 링크 flags, 라이브러리, 프레임워크가 포함될 수 있습니다. *ext.manifest* 파일에 "platforms" 세그먼트가 없거나 목록에서 플랫폼이 누락되어도 번들링 대상 플랫폼은 계속 빌드되지만 추가 flags는 설정되지 않습니다.

예제는 다음과 같습니다:

```yaml
name: "AdExtension"

platforms:
    arm64-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]

    armv7-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]
```

#### 허용되는 키

플랫폼별 컴파일 flags에 허용되는 키는 다음과 같습니다:

* `frameworks` - 빌드할 때 포함할 Apple 프레임워크(iOS 및 macOS)
* `weakFrameworks` - 빌드할 때 선택적으로 포함할 Apple 프레임워크(iOS 및 macOS)
* `flags` - 컴파일러에 전달할 flags
* `linkFlags` - 링커에 전달할 flags
* `libs` - 링크할 때 포함할 추가 라이브러리
* `defines` - 빌드할 때 설정할 defines
* `aaptExtraPackages` - 생성해야 하는 추가 패키지 이름(Android)
* `aaptExcludePackages` - 제외할 패키지의 정규식(regexp) 또는 정확한 이름(Android)
* `aaptExcludeResourceDirs` - 제외할 리소스 디렉토리의 정규식(regexp) 또는 정확한 이름(Android)
* `excludeLibs`, `excludeJars`, `excludeSymbols` - 이 flags는 플랫폼 context에 이전에 정의된 항목을 제거하는 데 사용됩니다.

모든 키워드에는 화이트리스트 필터가 적용됩니다. 이는 허용되지 않는 경로 처리와 빌드 업로드 폴더 외부 파일 접근을 방지하기 위한 것입니다.
