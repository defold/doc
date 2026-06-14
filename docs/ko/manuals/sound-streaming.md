---
title: Defold의 사운드 스트리밍
brief: 이 매뉴얼은 Defold 게임엔진에서 사운드를 스트리밍하는 방법을 설명합니다.
---

# 사운드 스트리밍

기본 동작은 사운드 데이터를 전체 로드하는 것이지만, 사용하기 전에 데이터를 청크 단위로 로드하는 것이 유용할 수도 있습니다. 이를 보통 "스트리밍"이라고 합니다.

사운드 스트리밍의 한 가지 장점은 필요한 런타임 메모리가 적다는 것입니다. 또 다른 장점은 예를 들어 HTTP URL에서 컨텐츠를 스트리밍하는 경우 언제든지 컨텐츠를 업데이트할 수 있고, 초기 다운로드도 피할 수 있다는 점입니다.

### 예제

이 설정을 보여 주는 예제 프로젝트가 있습니다: [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming)

## 스트리밍 사운드 활성화하기

### 쉬운 방법

사운드 스트리밍을 사용하는 가장 간단한 방법은 *game.project*에서 [`sound.stream_enabled` 설정](https://defold.com/manuals/project-settings/#stream-enabled)을 활성화하는 것입니다. 이 옵션이 활성화되면 엔진은 사운드 스트리밍을 시작합니다.

참고: 동시에 로드된 사운드 파일이 많다면 `sound.stream_cache_size` 값을 늘려야 할 수 있습니다(아래 참고).

### 런타임 리소스

새 사운드 데이터 리소스를 생성한 다음 사운드 컴포넌트에 설정할 수도 있습니다.

방법은 다음과 같습니다:
* 사운드 파일 데이터의 초기 부분을 로드합니다
    * 참고: 이는 ogg/wav 헤더를 포함한 원시 사운드 파일입니다
* [`resource.create_sound_data()`](/ref/resource/#resource.create_sound_data)를 호출해 새 사운드 데이터 리소스를 생성합니다.
* [`go.set()`](/ref/go#go.set)을 사용해 새 사운드 데이터 리소스를 사운드 컴포넌트에 설정합니다

다음은 `http.request()`를 사용해 초기 사운드 파일을 가져오는 예제 프로젝트의 발췌입니다.

::: sidenote
컨텐츠를 로드하는 웹 서버는 [HTTP range requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Range_requests)를 지원해야 합니다.
:::

```lua
local function play_sound(self, hash)
    go.set(self.component, "sound", hash) -- 컴포넌트의 리소스 데이터를 오버라이드합니다
    sound.play(self.component)            -- 사운드 재생을 시작합니다
end

local function parse_range(s)
    local _, _, rstart, rend, size = string.find(s, "(%d+)-(%d+)/(%d+)") -- "bytes 0-16383/103277"
    return rstart, rend, size
end

-- HTTP 응답을 위한 콜백입니다.
local function http_result(self, _id, response, extra)
    if response.status == 200 or response.status == 206 then
        -- 요청 성공
        local relative_path = self.filename
        local range = response.headers['content-range'] -- content-range = "bytes 0-16383/103277"
        local rstart, rend, filesize = parse_range(range)
        -- Defold 리소스를 생성합니다
        --   "partial"이 스트리밍 모드를 활성화합니다
        print("Creating resource", relative_path)
        local hash = resource.create_sound_data(relative_path, { data = response.response, filesize = filesize, partial = true })
        -- 컴포넌트에 "play_sound"를 보냅니다
        play_sound(self, hash)
    end
end

local function load_web_sound(base_url, relative_path)
    local url = base_url .. "/" .. relative_path
    local headers = {}
    headers['Range'] = string.format("bytes=%d-%d", 0, 16384-1)

    http.request(url, "GET", http_result, headers, nil, { ignore_cache = true })
end
```

## 리소스 프로바이더

사운드 파일의 초기 청크를 로드하는 데 다른 방법을 사용할 수도 있습니다. 기억해야 할 중요한 점은 나머지 청크가 리소스 시스템과 그 리소스 프로바이더에서 로드된다는 것입니다. 이 예제에서는 [liveupdate.add_mount()](/ref/liveupdate/#liveupdate.add_mount)를 호출해 live update 마운트를 추가함으로써 새 (http) 파일 프로바이더를 추가합니다.

동작하는 예제는 [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming)에서 볼 수 있습니다.

```lua
-- 위 예제의 http_result()를 참고하세요

local function load_web_sound(base_url, relative_path)
    local url = base_url .. "/" .. relative_path
    local headers = {}
    -- 파일의 초기 부분을 요청합니다
    headers['Range'] = string.format("bytes=%d-%d", 0, 16384-1)

    http.request(url, "GET", http_result, headers, nil, { ignore_cache = true })
end

function init(self)
    self.base_url = "http://my.server.com"
    self.filename = "/path/to/sound.ogg"

    liveupdate.add_mount("webmount", self.base_url, 100, function (_self, _name, _uri, _result)
                    -- 마운트 준비가 끝나면 첫 번째 청크를 다운로드하기 위한 요청을 시작할 수 있습니다
                    load_web_sound(self.base_url, self.filename)
                end)
end

function final(self)
    liveupdate.remove_mount("webmount")
end
```

## 사운드 청크 캐쉬

런타임에서 사운드가 소비하는 메모리 양은 *game.project*의 [`sound.stream_cache_size` 설정](https://defold.com/manuals/project-settings/#stream-cache-size)으로 제어됩니다. 이 제한이 주어지면 로드된 사운드 데이터는 이 제한을 절대 초과하지 않습니다.

각 사운드 파일의 초기 청크는 제거될 수 없으며, 리소스가 로드되어 있는 동안 캐쉬를 차지합니다. 초기 청크의 크기는 *game.project*의 [`sound.stream_preload_size` 설정](https://defold.com/manuals/project-settings/#stream-preload-size)으로 제어됩니다.

*game.project*의 [`sound.stream_chunk_size` 설정](https://defold.com/manuals/project-settings/#stream-chunk-size)을 변경해 각 사운드 청크의 크기도 제어할 수 있습니다. 동시에 로드된 사운드 파일이 많다면 사운드 캐쉬 크기를 더 줄이는 데 도움이 될 수 있습니다. 사운드 청크 크기보다 작은 사운드 파일은 스트리밍되지 않으며, 새 청크가 캐쉬에 들어가지 못하면 가장 오래된 청크가 제거됩니다

::: important
사운드 청크 캐쉬의 전체 크기는 로드된 사운드 파일 수에 stream chunk size를 곱한 값보다 커야 합니다. 그렇지 않으면 매 프레임 새 청크가 제거될 위험이 있고 사운드가 제대로 재생되지 않습니다
:::
