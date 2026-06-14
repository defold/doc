---
title: 네이티브 익스텐션 - Defold SDK
brief: 이 매뉴얼은 네이티브 익스텐션을 만들 때 Defold SDK로 작업하는 방법을 설명합니다.
---

# Defold SDK

Defold SDK에는 네이티브 익스텐션을 선언하고, 어플리케이션이 실행되는 저수준 네이티브 플랫폼 레이어 및 게임 로직이 작성되는 고수준 Lua 레이어와 연동하는 데 필요한 기능이 포함되어 있습니다.

## 사용법

Defold SDK는 `dmsdk/sdk.h` 헤더 파일을 포함해서 사용합니다:

    #include <dmsdk/sdk.h>

사용 가능한 SDK 함수와 네임스페이스는 [API 레퍼런스](/ref/overview_cpp)에 문서화되어 있습니다. Defold SDK 헤더는 각 Defold [GitHub 릴리스](https://github.com/defold/defold/releases)마다 별도의 `defoldsdk_headers.zip` 아카이브로 포함되어 있습니다. 원하는 에디터에서 코드 완성에 이 헤더를 사용할 수 있습니다.
