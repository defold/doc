---
title: 어플리케이션 메니페스트
brief: 이 매뉴얼은 어플리케이션 메니페스트를 사용해 엔진에서 기능을 제외하는 방법을 설명합니다.
---

# 어플리케이션 메니페스트

어플리케이션 메니페스트는 엔진에 포함할 기능을 제외하거나 제어하는 데 사용됩니다. 사용하지 않는 엔진 기능을 제외하면 게임의 최종 바이너리 크기가 줄어들기 때문에 권장되는 모범 사례입니다.
또한 어플리케이션 메니페스트에는 HTML5 플랫폼용 코드 컴파일을 제어하는 몇 가지 옵션도 포함되어 있습니다. 예를 들어 지원되는 최소 브라우저 버전과 메모리 설정이 있으며, 이 설정도 결과 바이너리 크기에 영향을 줄 수 있습니다.

![](images/app_manifest/create-app-manifest.png)

![](images/app_manifest/app-manifest.png)

# 메니페스트 적용

`game.project`에서 메니페스트를 `Native Extensions` -> `App Manifest`에 지정합니다.

## Physics

사용할 물리 엔진을 제어하거나 None을 선택해 물리를 완전히 제외합니다.

## Physics 2d

사용할 Box2D 버전을 선택합니다.

## Rig + Model

리그와 모델 기능을 제어하거나 None을 선택해 모델과 리그를 완전히 제외합니다. ([`Model`](https://defold.com/manuals/model/#model-component) 문서를 참고하세요).


## Exclude Record

엔진에서 비디오 녹화 기능을 제외합니다([`start_record`](https://defold.com/ref/stable/sys/#start_record) 메세지 문서를 참고하세요).


## Exclude Profiler

엔진에서 프로파일러를 제외합니다. 프로파일러는 성능 및 사용량 카운터를 수집하는 데 사용됩니다. [프로파일링 매뉴얼](/manuals/profiling/)에서 프로파일러 사용법을 알아보세요.


## Exclude Sound

엔진에서 모든 사운드 재생 기능을 제외합니다.


## Exclude Input

엔진에서 모든 입력 처리를 제외합니다.


## Exclude Live Update

엔진에서 [Live Update 기능](/manuals/live-update)을 제외합니다.


## Exclude Image

엔진에서 `image` 스크립트 모듈 [link](https://defold.com/ref/stable/image/)를 제외합니다.


## Exclude Types

엔진에서 `types` 스크립트 모듈 [link](https://defold.com/ref/stable/types/)를 제외합니다.


## Exclude Basis Universal

엔진에서 Basis Universal [텍스쳐 압축 라이브러리](/manuals/texture-profiles)를 제외합니다.


## Use Android Support Lib

Android X 대신 더 이상 사용되지 않는 Android Support Library를 사용합니다. [자세한 정보](https://defold.com/manuals/android/#using-androidx).


## Graphics

사용할 그래픽 백엔드를 선택합니다.

* OpenGL - OpenGL만 포함합니다.
* Vulkan - Vulkan만 포함합니다.
* OpenGL and Vulkan - OpenGL과 Vulkan을 모두 포함합니다. Vulkan이 기본값이며, Vulkan을 사용할 수 없으면 OpenGL로 대체됩니다.

## Use full text layout system

활성화하면(`true`) 프로젝트에서 True Type Fonts(`.ttf`)를 사용할 때 SDF 타입 폰트의 런타임 생성을 사용할 수 있습니다. [Font Manual](https://defold.com/manuals/font/#enabling-runtime-fonts)에서 자세한 내용을 확인하세요.


## Minimum Safari version (wasm-web only)
YAML 필드 이름: **`minSafariVersion`**
기본값: **90000**

지원되는 Safari의 최소 버전입니다. 90000보다 작을 수 없습니다. 자세한 내용은 Emscripten 컴파일러 옵션 [link](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#min-safari-version)를 참고하세요.

## Minimum Firefox version (wasm-web only)
YAML 필드 이름: **`minFirefoxVersion`**
기본값: **34**

지원되는 Firefox의 최소 버전입니다. 34보다 작을 수 없습니다. 자세한 내용은 Emscripten 컴파일러 옵션 [link](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#min-firefox-version)를 참고하세요.

## Minimum Chrome version (wasm-web only)
YAML 필드 이름: **`minChromeVersion`**
기본값: **32**

지원되는 Chrome의 최소 버전입니다. 32보다 작을 수 없습니다. 자세한 내용은 Emscripten 컴파일러 옵션 [link](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#min-chrome-version)를 참고하세요.

## Initial memory (wasm-web only)
YAML 필드 이름: **`initialMemory`**
기본값: **33554432**

웹 어플리케이션에 할당되는 메모리 크기입니다. `ALLOW_MEMORY_GROWTH=0`이면 웹 어플리케이션이 사용할 수 있는 전체 메모리 양입니다. 자세한 내용은 [link](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#initial-memory)를 참고하세요. 값은 바이트 단위입니다. 값은 WebAssembly 페이지 크기(64KiB)의 배수여야 합니다.
이 옵션은 *game.project*의 `html5.heap_size` [link](https://defold.com/manuals/html5/#heap-size)와 관련이 있습니다. 어플리케이션 메니페스트로 구성한 옵션은 컴파일 중 설정되며 `INITIAL_MEMORY` 옵션의 기본값으로 사용됩니다. *game.project*의 값은 어플리케이션 메니페스트의 값을 덮어쓰며 런타임에 사용됩니다.

## Stack size (wasm-web only)
YAML 필드 이름: **`stackSize`**
기본값: **5242880**

어플리케이션의 스택 크기입니다. 자세한 내용은 [link](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#stack-size)를 참고하세요. 값은 바이트 단위입니다.
