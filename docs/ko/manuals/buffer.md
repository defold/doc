---
title: Buffer 매뉴얼
brief: 이 매뉴얼은 Defold에서 Buffer 리소스가 작동하는 방식을 설명합니다.
---

# Buffer

Buffer 리소스는 위치나 색상과 같은 값 스트림을 하나 이상 기술하는 데 사용됩니다. 각 스트림에는 이름, 데이터 타입, 개수 및 데이터 자체가 있습니다. 예:

```
[
  {
    "name": "position",
    "type": "float32",
    "count": 3,
    "data": [
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      1.0,
      ...
    ]
  }
]
```

위 예제는 32비트 부동 소수점 숫자로 표현된 3차원 위치 스트림을 설명합니다. Buffer 파일의 포멧은 JSON이며 파일 확장자는 `.buffer`입니다.

Buffer 리소스는 보통 Blender 같은 모델링 도구에서 익스포트할 때처럼 외부 도구나 스크립트를 사용해 생성합니다.

Buffer 리소스는 [Mesh 컴포넌트](/manuals/mesh)의 입력으로 사용할 수 있습니다. Buffer 리소스는 런타임에 `buffer.create()`와 [관련 API 함수](/ref/stable/buffer/#buffer.create:element_count-declaration)를 사용해 생성할 수도 있습니다.
