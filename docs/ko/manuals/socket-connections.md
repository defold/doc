---
title: 소켓 연결
brief: 이 매뉴얼은 소켓 연결을 만드는 방법을 설명합니다.
---

## 소켓 연결

Defold에는 TCP 및 UDP 소켓 연결을 만들기 위한 [LuaSocket 라이브러리](https://lunarmodules.github.io/luasocket/)가 포함되어 있습니다. 다음은 소켓 연결을 만들고, 일부 데이터를 보내고, 응답을 읽는 예제입니다:

```Lua
local client = socket.tcp()
client:connect("127.0.0.1", 8123)
client:settimeout(0)
client:send("foobar")
local response = client:receive("*l")
```

이 코드는 TCP 소켓을 만들고 IP 127.0.0.1(localhost) 및 포트 8123에 연결합니다. 소켓을 논블로킹(non-blocking)으로 만들기 위해 타임아웃을 0으로 설정하고, 소켓을 통해 문자열 "foobar"를 보냅니다. 또한 소켓에서 데이터 한 줄(줄바꿈 문자로 끝나는 바이트)을 읽습니다. 위 예제에는 어떤 종류의 오류 처리도 포함되어 있지 않다는 점에 유의하세요.

### API 레퍼런스 및 예제

LuaSocket을 통해 사용할 수 있는 기능에 대해 자세히 알아보려면 [API 레퍼런스](/ref/socket/)를 참고하세요. [공식 LuaSocket 문서](https://lunarmodules.github.io/luasocket/)에도 이 라이브러리로 작업하는 방법에 대한 많은 예제가 포함되어 있습니다. [DefNet 라이브러리](https://github.com/britzl/defnet/)에도 몇 가지 예제와 헬퍼 모듈이 있습니다.
