---
title: Defold 中的声音流传输
brief: 本手册介绍了如何将声音流式传输到 Defold 游戏引擎中
---

# 声音流传输

虽然默认行为是完整加载声音数据，但在使用前分块加载数据可能也是有益的。这通常被称为"流传输"。

声音流传输的一个好处是需要更少的运行时内存，另一个好处是如果您从例如 http url 流式传输内容，您可以随时更新内容，并避免初始下载。

### 示例

有一个展示此设置的示例项目：[https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming)

## 如何启用声音流传输

### 简单方法

使用声音流传输的最简单方法是在 *game.project* 中启用 [`sound.stream_enabled` 设置](https://defold.com/manuals/project-settings/#stream-enabled)。启用此选项后，引擎将开始流式传输声音。

注意：如果您同时加载了许多声音文件，可能需要增加 `sound.stream_cache_size` 值（见下文）。

### 运行时资源

您也可以创建一个新的声音数据资源，并将其设置为声音组件。

您可以通过以下方式执行此操作：
* 加载声音文件数据的初始部分
    * 注意：这是原始声音文件，包括 ogg/wav 头部
* 通过调用 [`resource.create_sound_data()`](/ref/resource/#resource.create_sound_data) 创建一个新的声音数据资源
* 使用 [`go.set()`](/ref/go#go.set) 将新的声音数据资源设置为声音组件

以下是示例项目中的摘录，使用 `http.request()` 获取初始声音文件。

::: sidenote
您从中加载内容的 Web 服务器必须支持 [HTTP 范围请求](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Range_requests)。
:::

```lua
local function play_sound(self, hash)
    go.set(self.component, "sound", hash) -- 覆盖组件上的资源数据
    sound.play(self.component)            -- 开始播放声音
end

local function parse_range(s)
    local _, _, rstart, rend, size = string.find(s, "(%d+)-(%d+)/(%d+)") -- "bytes 0-16383/103277"
    return rstart, rend, size
end

-- http 响应的回调函数
local function http_result(self, _id, response, extra)
    if response.status == 200 or response.status == 206 then
        -- 成功的请求
        local relative_path = self.filename
        local range = response.headers['content-range'] -- content-range = "bytes 0-16383/103277"
        local rstart, rend, filesize = parse_range(range)
        -- 创建 Defold 资源
        --   "partial" 将启用流传输模式
        print("Creating resource", relative_path)
        local hash = resource.create_sound_data(relative_path, { data = response.response, filesize = filesize, partial = true })
        -- 发送 "play_sound" 到组件
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

## 资源提供者

您可以使用其他方式加载声音文件的初始块。重要的是要记住，其余的块是从资源系统及其资源提供者加载的。在此示例中，我们通过调用使用 [liveupdate.add_mount()](/ref/liveupdate/#liveupdate.add_mount) 添加一个新的 (http) 文件提供者，通过添加实时更新挂载点。

您可以在 [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming) 中找到一个工作示例。

```lua
-- 参见上面示例中的 http_result()

local function load_web_sound(base_url, relative_path)
    local url = base_url .. "/" .. relative_path
    local headers = {}
    -- 请求文件的初始部分
    headers['Range'] = string.format("bytes=%d-%d", 0, 16384-1)

    http.request(url, "GET", http_result, headers, nil, { ignore_cache = true })
end

function init(self)
    self.base_url = "http://my.server.com"
    self.filename = "/path/to/sound.ogg"

    liveupdate.add_mount("webmount", self.base_url, 100, function ()
                    -- 一旦挂载点准备就绪，我们就可以开始请求下载第一个块
                    load_web_sound(self.base_url, self.filename)
                end)
end

function final(self)
    liveupdate.remove_mount("webmount")
end
```

## 声音块缓存

运行时声音消耗的内存量由 *game.project* 中的 [`sound.stream_cache_size` 设置](https://defold.com/manuals/project-settings/#stream-cache-size) 控制。在此限制下，加载的声音数据永远不会超过此限制。

每个声音文件的初始块不能被驱逐，只要资源被加载，它们就会占用缓存。初始块的大小由 *game.project* 中的 [`sound.stream_preload_size` 设置](https://defold.com/manuals/project-settings/#stream-preload-size) 控制。

您还可以通过更改 *game.project* 中的 [`sound.stream_chunk_size` 设置](https://defold.com/manuals/project-settings/#stream-chunk-size) 来控制每个声音块的大小。如果您同时加载了许多声音文件，这可能有助于进一步降低声音缓存大小。小于声音块大小的声音文件不会被流式传输，如果新块不适合放入缓存中，最旧的块将被驱逐。

::: important
声音块缓存的总大小应大于加载的声音文件数量乘以流块大小。否则，您可能会冒着每帧驱逐新块的风险，声音将无法正常播放。
:::