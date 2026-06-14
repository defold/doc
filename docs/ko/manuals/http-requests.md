---
title: HTTP 요청
brief: 이 매뉴얼은 HTTP 요청을 보내는 방법을 설명합니다.
---

## HTTP 요청

Defold는 `http.request()` 함수를 사용해 일반적인 HTTP 요청을 보낼 수 있습니다.

### HTTP GET

서버에서 데이터를 가져오는 가장 기본적인 요청입니다. 예:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

http.request("https://www.defold.com", "GET", handle_response)
```

이 코드는 https://www.defold.com으로 HTTP GET 요청을 보냅니다. 이 함수는 비동기 함수이므로 요청을 보내는 동안 실행을 차단하지 않습니다. 요청이 만들어지고 서버가 응답을 보내면 제공된 콜백 함수를 호출합니다. 콜백 함수는 상태 코드와 응답 헤더를 포함한 전체 서버 응답을 받습니다. 응답 테이블을 다루는 방법에 대한 추가 정보는 아래를 참고하세요.

::: sidenote
네트워크 성능을 높이기 위해 HTTP 요청은 클라이언트에서 자동으로 캐쉬됩니다. 캐쉬된 파일은 OS별 어플리케이션 지원 경로의 `defold/http-cache`라는 폴더에 저장됩니다. 일반적으로 HTTP 캐쉬를 신경 쓸 필요는 없지만, 개발 중 캐쉬를 지워야 한다면 캐쉬된 파일이 들어 있는 폴더를 수동으로 삭제할 수 있습니다. macOS에서는 이 폴더가 `%HOME%/Library/Application Support/Defold/http-cache/`에 있고, Windows에서는 `%APP_DATA%/defold/http-cache`에 있습니다.
:::

### HTTP POST

점수나 인증 데이터 같은 데이터를 서버로 보낼 때는 일반적으로 POST 요청을 사용합니다:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

local body = "12345"
http.request("https://www.myserver.com/score", "POST", handle_response, nil, body)
```


### 기타 HTTP 메서드

Defold HTTP 요청은 HEAD, DELETE, PUT 메서드도 지원합니다. CONNECT 메서드도 지원됩니다(아래 프록시 연결 섹션 참고).

### HTTP 응답 다루기

콜백에서 반환되는 `response` 테이블에는 세분화된 응답 처리를 구현하는 데 필요한 모든 정보가 들어 있습니다. 주요 필드 두 가지는 `status`와 `response`입니다:

```lua

local function handle_response(self, id, response)
	-- 응답 상태 코드를 확인합니다. 일반적인 응답 코드:
	-- 200 OK - 요청이 성공적으로 완료됨
	-- 301 Moved permanently - 요청한 데이터가 이동됨, 리다이렉트 헤더를 확인하세요
	-- 307 Temporary redirect - 위와 동일
	-- 208 Permanent redirect - 위와 동일
	-- 400 Bad Request - 요청 형식이 잘못됨
	-- 401 Unauthorized - 클라이언트가 스스로 인증해야 함
	-- 404 Not Found - 서버가 정보를 찾을 수 없음
	-- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
	if response.status == 200 then
		-- 응답 데이터
		-- 일반 텍스트, json 인코딩된 데이터, 바이너리 데이터 등 무엇이든 될 수 있습니다
		print(response.response)
		json.decode(response.response)
		sys.save(..., response.response)
	end
end
```

응답에 이미지나 음악 트랙 같은 큰 바이너리 데이터 덩어리가 포함되어 있다면, 데이터를 메모리에 로드하는 대신 파일에 쓰는 것이 적절할 수 있습니다:

```lua
-- 이 예제에서는 myimage.png를 다운로드하고 디스크의 파일에 직접 씁니다

local options = {
	path = sys.get_save_file("mygame", "myimage.png")
}

local function handle_response(self, id, response)
	if response.status == 200 then
		print("File was successfully written to:", response.path)
		print("File size:", response.document_size)
		print("File path:", response.path)
	else
		print("File was not written to disk:", response.error)
	end
end

http.request("https://www.foobar.com/myimage.png", "GET", handle_response, nil, nil, options)
```

네트워크를 통해 많은 양의 데이터를 로드하는 또 다른 사용 사례는 사운드 스트리밍입니다. 이 경우 URL에서 사운드 데이터의 "chunks"를 로드해 사운드 리소스에 공급합니다. 완전한 예제는 [사운드 스트리밍 매뉴얼](/sound-streaming#sound-streaming)에서 볼 수 있습니다.


### 요청 헤더

요청을 보낼 때 추가 헤더를 설정할 수 있습니다. 예를 들어 `Authorization` 헤더를 설정하거나, 서버에 데이터 형식을 알려 주는 `Content-Type`을 설정하는 데 사용할 수 있습니다.

```Lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

-- 일부 폼 데이터 보내기
local headers = {
	["Content-Type"] = "application/x-www-form-urlencoded"
}
local body = "key1=value1&key2=value2"
http.request("https://www.myserver.com/post", "POST", handle_response, headers, body)

-- json 인코딩된 데이터 보내기
local headers = {
	["Content-Type"] = "application/json"
}
local body = json.encode({ key1 = value1, key2 = value2 })
http.request("https://www.myserver.com/post", "POST", handle_response, headers, body)

-- 액세스하려면 인증이 필요한 데이터 요청하기
local token = ... -- 액세스 토큰(JWT, OAuth 등)을 생성합니다
local headers = {
	["Authorization"] = "Bearer " .. token
}
http.request("https://www.myserver.com/content", "GET", handle_response, headers)
```

Defold는 몇 가지 요청 헤더를 자동으로 설정합니다:

* `If-None-Match: <etag>`는 이전에 캐쉬된 응답의 ETag로 설정됩니다.
* 요청 본문이 16384바이트보다 크면 `Transfer-Encoding: chunked`가 설정됩니다.
* `Content-Length`는 요청 본문의 크기로 설정됩니다(요청이 `chunked` 방식이 아닌 경우).
* 부분 응답을 요청할 때, 예를 들어 [사운드를 스트리밍](/sound-streaming#sound-streaming)할 때 `Range: bytes=<from>-<to>`가 설정됩니다.


### 응답 헤더

서버 응답에는 하나 이상의 응답 헤더가 포함될 수 있습니다. 응답 헤더는 `response` 테이블에서 사용할 수 있습니다:

```lua
local function handle_response(self, id, response)
	for header,value in pairs(response.headers) do
		print(header, value)
	end
end

http.request("https://www.defold.com", "GET", handle_response)
```


### HTTP 프록시

요청을 프록시 서버를 통해 보내고 싶을 때가 있습니다. 대상 서버에 연결할 때 사용할 프록시 서버를 지정하면 됩니다. 프록시를 사용하면 프록시를 통한 HTTP 터널을 사용해 대상 서버와의 연결이 만들어집니다. HTTP 터널은 CONNECT HTTP 메서드를 사용해 만들어집니다. 예:


```lua
-- 포트 8888의 localhost 프록시를 통해 www.defold.com에 연결합니다
local url = "https://www.defold.com:443"
local method = "GET"
local headers = {}
local post_data = nil
local options = {
	proxy = "https://127.0.0.1:8888"
}
http.request(url, method, function(self, id, response)
	pprint(response)
end, headers, post_data, options)
```

### API 레퍼런스

자세한 내용은 [API 레퍼런스](/ref/http/)를 참고하세요.

### 익스텐션

대체 HTTP 요청 구현은 [TinyHTTP extension](https://defold.com/assets/tinyhttp/)에서 찾을 수 있습니다.
