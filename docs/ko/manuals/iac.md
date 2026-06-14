---
title: Defold의 앱 간 통신
brief: 앱 간 통신을 사용하면 어플리케이션을 시작할 때 사용된 실행 인자를 받아올 수 있습니다. 이 매뉴얼은 이 기능에 사용할 수 있는 Defold API를 설명합니다.
---

# 앱 간 통신

대부분의 운영 체제에서 어플리케이션은 여러 방법으로 실행될 수 있습니다.

* 설치된 어플리케이션 목록에서 실행
* 어플리케이션 전용 링크에서 실행
* 푸시 알림에서 실행
* 설치 과정의 마지막 단계로 실행

어플리케이션이 링크나 알림에서 실행되거나 설치될 때는 추가 인자를 전달할 수 있습니다. 예를 들어 설치 시에는 install referrer를, 어플리케이션 전용 링크나 알림에서 실행할 때는 deep-link를 전달할 수 있습니다. Defold는 네이티브 익스텐션을 사용해 어플리케이션이 어떤 방식으로 호출되었는지에 대한 정보를 얻는 통합된 방법을 제공합니다.

## 익스텐션 설치

Inter-app communication 익스텐션을 사용하려면 먼저 *game.project* 파일에 종속성으로 추가해야 합니다. 최신 안정 버전은 다음 종속성 URL로 사용할 수 있습니다.
```
https://github.com/defold/extension-iac/archive/master.zip
```

[특정 릴리스](https://github.com/defold/extension-iac/releases)의 zip 파일 링크를 사용하는 것을 권장합니다.

## 익스텐션 사용

API는 사용하기 매우 쉽습니다. 익스텐션에 리스너 함수를 제공하고 리스너 콜백에 반응하면 됩니다.

```
local function iac_listener(self, payload, type)
     if type == iac.TYPE_INVOCATION then
         -- 호출입니다
         print(payload.origin) -- 해석할 수 없으면 origin은 빈 문자열일 수 있습니다
         print(payload.url)
     end
end

function init(self)
     iac.set_listener(iac_listener)
end
```

API의 전체 문서는 [extension GitHub page](https://defold.github.io/extension-iac/)에서 확인할 수 있습니다.
