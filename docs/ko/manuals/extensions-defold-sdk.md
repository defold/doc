---
title: 네이티브 익스텐션 - Defold SDK
brief: 이 매뉴얼은 네이티브 익스텐션을 만들 때 Defold SDK로 작업하는 방법을 설명합니다.
---

# Defold SDK

Defold SDK에는 네이티브 익스텐션을 선언하고, 어플리케이션이 실행되는 저수준 네이티브 플랫폼 레이어 및 게임 로직이 작성되는 고수준 Lua 레이어와 연동하는 데 필요한 기능이 포함되어 있습니다.

## 사용법

C++ 익스텐션은 통합 `dmsdk/sdk.h` 헤더 파일을 포함할 수 있습니다.

```cpp
#include <dmsdk/sdk.h>
```

통합 헤더에는 C++ 선언이 포함되어 있으므로 C 소스 파일에서는 포함할 수 없습니다. C 소스 파일은 필요한 개별 C 호환 `.h` 헤더를 포함해야 합니다. 예:

```c
#include <dmsdk/extension/extension.h>
#include <dmsdk/dlib/configfile.h>
#include <dmsdk/resource/resource.h>
```

현재 dmSDK의 일부만 순수 C 인터페이스를 제공하며, 모든 C++ 서브시스템에 대응하는 C 인터페이스가 있는 것은 아닙니다. 사용 가능한 함수와 타입은 [C API 개요](/ref/overview_defoldc/)와 [C++ API 개요](/ref/overview_defoldcpp/)에 문서화되어 있습니다. Defold SDK 헤더는 각 Defold [GitHub 릴리스](https://github.com/defold/defold/releases)마다 별도의 `defoldsdk_headers.zip` 아카이브로 포함되어 있습니다. 원하는 에디터에서 코드 완성에 이 헤더를 사용할 수 있습니다.
