---
title: 네이티브 익스텐션에 에디터 자동 완성 추가하기
brief: 이 매뉴얼은 Defold 에디터가 익스텐션 사용자에게 자동 완성을 제공할 수 있도록 스크립트 API 정의를 만드는 방법을 설명합니다.
---

# 네이티브 익스텐션 자동 완성

Defold 에디터는 모든 Defold API 함수에 대해 자동 완성 제안을 제공하며, 스크립트에서 필요로 하는 Lua 모듈에 대한 제안도 생성합니다. 하지만 네이티브 익스텐션이 노출하는 기능에 대해서는 에디터가 자동으로 자동 완성 제안을 제공할 수 없습니다. 네이티브 익스텐션은 별도 파일에 API 정의를 제공하여 익스텐션 API에도 자동 완성 제안이 활성화되도록 할 수 있습니다.


## 스크립트 API 정의 만들기

스크립트 API 정의 파일의 확장자는 `.script_api`입니다. 이 파일은 [YAML 포멧](https://yaml.org/)이어야 하며 익스텐션 파일들과 함께 위치해야 합니다. 스크립트 API 정의의 예상 포멧은 다음과 같습니다:

```yml
- name: 익스텐션 이름
  type: table
  desc: 익스텐션 설명
  members:
  - name: 첫 번째 멤버의 이름
    type: 멤버 타입
    desc: 멤버 설명
    # 멤버 타입이 "function"인 경우
    parameters:
    - name: 첫 번째 파라미터의 이름
      type: 파라미터 타입
      desc: 파라미터 설명
    - name: 두 번째 파라미터의 이름
      type: 파라미터 타입
      desc: 파라미터 설명
    # 멤버 타입이 "function"인 경우
    returns:
    - name: 첫 번째 반환값의 이름
      type: 반환값 타입
      desc: 반환값 설명
    examples:
    - desc: 멤버 사용법 첫 번째 예제
    - desc: 멤버 사용법 두 번째 예제

  - name: 두 번째 멤버의 이름
    ...
```

타입은 `table, string , boolean, number, function` 중 하나일 수 있습니다. 값이 여러 타입을 가질 수 있다면 `[type1, type2, type3]`처럼 작성합니다.
::: sidenote
타입은 현재 에디터에 표시되지 않습니다. 에디터가 타입 정보 표시를 지원하게 되었을 때 사용할 수 있도록 타입을 계속 제공하는 것을 권장합니다.
:::

## 예제

실제 사용 예제는 다음 프로젝트를 참고하세요:

* [Facebook extension](https://github.com/defold/extension-facebook/tree/master/facebook/api)
* [WebView extension](https://github.com/defold/extension-webview/blob/master/webview/api/webview.script_api)
