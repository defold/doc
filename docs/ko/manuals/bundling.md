---
title: 어플리케이션 번들링
brief: 이 매뉴얼은 어플리케이션 번들을 만드는 방법을 다룹니다.
---

# 어플리케이션 번들링

어플리케이션을 개발하는 동안에는 가능한 자주 타겟 플랫폼에서 게임을 테스트하는 습관을 들이는 것이 좋습니다. 이렇게 하면 개발 과정 초기에 성능 문제를 발견할 수 있으며, 이 시점에는 이런 문제를 훨씬 쉽게 수정할 수 있습니다. 쉐이더와 같은 항목의 차이를 찾기 위해 모든 타겟 플랫폼에서 테스트하는 것도 권장됩니다. 모바일에서 개발할 때는 전체 번들을 만들고 제거/설치하는 과정을 반복하는 대신 [모바일 개발용 앱](/manuals/dev-app/)을 사용해 컨텐츠를 앱으로 푸시할 수 있습니다.

Defold가 지원하는 모든 플랫폼의 어플리케이션 번들은 외부 도구 없이 Defold 에디터 안에서 만들 수 있습니다. 또한 커맨드 라인 도구를 사용해 커맨드 라인에서 번들링할 수도 있습니다. 프로젝트에 하나 이상의 [네이티브 익스텐션](/manuals/extensions)이 포함되어 있다면 어플리케이션 번들링에는 네트워크 연결이 필요합니다.

## 에디터 안에서 번들링하기

Project 메뉴의 Bundle 옵션에서 어플리케이션 번들을 만듭니다.

![](images/bundling/bundle_menu.png)

메뉴 옵션 중 하나를 선택하면 해당 플랫폼의 Bundle 다이얼로그가 열립니다.

### 빌드 리포트

게임을 번들링할 때 빌드 리포트를 만들 수 있는 옵션이 있습니다. 이 옵션은 게임 번들에 포함되는 모든 에셋의 크기를 파악하는 데 매우 유용합니다. 게임을 번들링할 때 *Generate build report* 체크박스를 선택하기만 하면 됩니다.

![빌드 리포트](images/profiling/build_report.png)

빌드 리포트에 대해 자세히 알아보려면 [프로파일링 매뉴얼](/manuals/profiling/#build-reports)을 참조하세요.

### Android

Android 어플리케이션 번들(.apk 파일)을 만드는 방법은 [Android 매뉴얼](/manuals/android/#creating-an-android-application-bundle)에 문서화되어 있습니다.

### iOS

iOS 어플리케이션 번들(.ipa 파일)을 만드는 방법은 [iOS 매뉴얼](/manuals/ios/#creating-an-ios-application-bundle)에 문서화되어 있습니다.

### macOS

macOS 어플리케이션 번들(.app 파일)을 만드는 방법은 [macOS 매뉴얼](/manuals/macos)에 문서화되어 있습니다.

### Linux

Linux 어플리케이션 번들을 만들 때는 별도의 설정이 필요 없으며, *game.project* [프로젝트 설정 파일](/manuals/project-settings/#linux)에 선택적인 플랫폼별 설정도 필요하지 않습니다.

### Windows

Windows 어플리케이션 번들(.exe 파일)을 만드는 방법은 [Windows 매뉴얼](/manuals/windows)에 문서화되어 있습니다.

### HTML5

HTML5 어플리케이션 번들을 만드는 방법과 선택적인 설정은 [HTML5 매뉴얼](/manuals/html5/#creating-html5-bundle)에 문서화되어 있습니다.

#### Facebook Instant Games

Facebook Instant Games 전용 HTML5 어플리케이션 번들의 특별 버전을 만들 수 있습니다. 이 과정은 [Facebook Instant Games 매뉴얼](/manuals/instant-games/)에 문서화되어 있습니다.

## 커맨드 라인에서 번들링하기

에디터는 어플리케이션을 번들링하기 위해 커맨드 라인 도구인 [Bob](/manuals/bob/)을 사용합니다.

어플리케이션을 일상적으로 개발할 때는 Defold 에디터 안에서 빌드하고 번들링하는 경우가 많습니다. 다른 상황에서는 어플리케이션 번들을 자동으로 생성하고 싶을 수 있습니다. 예를 들어 새 버전을 릴리스할 때 모든 타겟에 대해 배치 빌드를 수행하거나, CI 환경 등에서 최신 버전 게임의 nightly build를 만들 때가 그렇습니다. [Bob 커맨드 라인 도구](/manuals/bob/)를 사용하면 일반적인 에디터 워크플로우 밖에서 어플리케이션을 빌드하고 번들링할 수 있습니다.

## 번들 레이아웃

논리적인 번들 레이아웃은 다음과 같은 구조입니다.

![](images/bundling/bundle_schematic_01.png)

번들은 폴더로 출력됩니다. 플랫폼에 따라 이 폴더가 `.apk` 또는 `.ipa`로 zip 아카이브될 수도 있습니다.
폴더의 컨텐츠는 플랫폼에 따라 달라집니다.

실행 파일 외에도, Defold의 번들링 과정은 플랫폼에 필요한 에셋도 수집합니다(예: Android용 .xml 리소스 파일).

[bundle_resources](https://defold.com/manuals/project-settings/#bundle-resources) 설정을 사용하면 번들 안에 그대로 배치해야 하는 에셋을 구성할 수 있습니다.
이는 플랫폼별로 제어할 수 있습니다.

게임 에셋은 `game.arcd` 파일에 위치하며, LZ4 압축을 사용해 개별적으로 압축됩니다.
[custom_resources](https://defold.com/manuals/project-settings/#custom-resources) 설정을 사용하면 `game.arcd` 안에 배치해야 하는 에셋을 구성할 수 있습니다(압축 적용).
이 에셋들은 [`sys.load_resource()`](https://defold.com/ref/sys/#sys.load_resource) 함수를 통해 액세스할 수 있습니다.

## 릴리스 vs 디버그

어플리케이션 번들을 만들 때 디버그 번들이나 릴리스 번들을 만들 수 있는 옵션이 있습니다. 두 번들의 차이는 작지만 기억해 두어야 할 중요한 차이가 있습니다.

* 릴리스 빌드에는 [프로파일러](/manuals/profiling)가 포함되지 않습니다
* 릴리스 빌드에는 [스크린 레코더](/ref/stable/sys/#start_record)가 포함되지 않습니다
* 릴리스 빌드는 `print()` 호출의 출력이나 네이티브 익스텐션의 출력을 표시하지 않습니다
* 릴리스 빌드에서는 `sys.get_engine_info()`의 `is_debug` 값이 `false`로 설정됩니다
* 릴리스 빌드는 `tostring()`을 호출할 때 `hash` 값에 대한 역방향 조회를 수행하지 않습니다. 실제로는 `url` 또는 `hash` 타입 값에 대해 `tostring()`을 호출하면 원래 문자열이 아니라 숫자 표현이 반환된다는 뜻입니다(`'hash: [/camera_001]'` vs `'hash: [11844936738040519888 (unknown)]'`)
* 릴리스 빌드는 에디터에서 [핫 리로드](/manuals/hot-reload) 및 유사 기능의 대상으로 지정하는 것을 지원하지 않습니다
