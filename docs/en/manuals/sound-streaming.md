---
title: Sound Streaming in Defold
brief: This manual explains how to stream sounds into the Defold game engine
---

# Sound Streaming

While the default behaviour is to load sound data in full, it may also be beneficial to load the data in chunks, prior to their use. This is often called "streaming".

One benefit of sound streaming is that less runtime memory is required, another is if you are streaming content from e.g. a http url, you can update the content at any time, and also avoid the initial download.

### Example

There is an example project showcasing this setup: [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming)

## How to enable streaming sounds

### Easy way

The simplest way to use sound streaming, is by enabling the [`sound.stream_enabled` setting](https://defold.com/manuals/project-settings/#stream-enabled) in *game.project*. When this option is enabled the engine will start streaming the sounds.

Note: If you have lots of sound files loaded at the same time, you may need to increase the `sound.stream_cache_size` value (see below).

### Runtime resources

You can also create a new sound data resource, and set it to a sound component.

You do this by:
* Load the initial part of the sound file data
    * Note: This is the raw sound file, including the ogg/wav header
* Create a new sound data resource by calling [`resource.create_sound_data()`](/ref/resource/#resource.create_sound_data).
* Set the new sound data resource to the sound component using [`go.set()`](/ref/go#go.set)

Here is an excerpt from the example project, using a `http.request()` to get the initial sound file.

::: sidenote
Actual streaming requires the web server to honor [HTTP range requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Range_requests) and return status `206`. If the server ignores the `Range` header and returns status `200`, the example below creates a normal non-streaming resource from the complete response instead.
:::

```lua
local function play_sound(self, hash)
    go.set(self.component, "sound", hash) -- override the resource data on the component
    sound.play(self.component)            -- start playing the sound
end

local function parse_content_range(value)
    if not value then
        return nil
    end
    local rstart, rend, filesize = value:match("^bytes%s+(%d+)%-(%d+)/(%d+)$")
    return tonumber(rstart), tonumber(rend), tonumber(filesize)
end

-- Callback for the http response.
local function http_result(self, _id, response)
    if response.status ~= 200 and response.status ~= 206 then
        return
    end

    local options = {
        data = response.response,
    }

    if response.status == 206 then
        local rstart, _, filesize = parse_content_range(response.headers["content-range"])
        if rstart ~= 0 or not filesize then
            print("Invalid Content-Range response")
            return
        end

        -- A partial resource enables streaming. filesize is the size of the
        -- complete file, not only the returned range.
        if #response.response < filesize then
            options.filesize = filesize
            options.partial = true
        end
    end

    local relative_path = self.filename
    print("Creating resource", relative_path)
    local resource_hash = resource.create_sound_data(relative_path, options)
    play_sound(self, resource_hash)
end

local function load_web_sound(base_url, relative_path)
    local url = base_url .. "/" .. relative_path
    local headers = {}
    headers['Range'] = string.format("bytes=%d-%d", 0, 16384-1)

    http.request(url, "GET", http_result, headers, nil, { ignore_cache = true })
end
```

## Resource providers

You can use other means to load the initial chunk of the sound file. The important thing to remember is that the rest of the chunks are loaded from the resource system and its resource providers. In this example, we add a new (http) file provider by adding a live update mount, by calling using [liveupdate.add_mount()](/ref/liveupdate/#liveupdate.add_mount).

You can find a working example in [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming).

```lua
-- See http_result() from above example

local function load_web_sound(base_url, relative_path)
    local url = base_url .. "/" .. relative_path
    local headers = {}
    -- Request the initial part of the file
    headers['Range'] = string.format("bytes=%d-%d", 0, 16384-1)

    http.request(url, "GET", http_result, headers, nil, { ignore_cache = true })
end

function init(self)
    self.base_url = "http://my.server.com"
    self.filename = "/path/to/sound.ogg"

    liveupdate.add_mount("webmount", self.base_url, 100, function (_self, _name, _uri, _result)
                    -- once the mount is ready, we can start our request for downloading the first chunk
                    load_web_sound(self.base_url, self.filename)
                end)
end

function final(self)
    liveupdate.remove_mount("webmount")
end
```

## Sound chunk cache

The amount of memory consumed by the sounds at runtime is controlled by the [`sound.stream_cache_size` setting](https://defold.com/manuals/project-settings/#stream-cache-size) in *game.project*. Given this limit, the loaded sound data will never exceed this limit.

The initial chunk of each sound file cannot be evicted and they will occupy the cache for as long as the resources are loaded. The size of the initial chunk is controlled by the [`sound.stream_preload_size` setting](https://defold.com/manuals/project-settings/#stream-preload-size) in *game.project*.

You can also control the size of each sound chunk by changing the [`sound.stream_chunk_size` setting](https://defold.com/manuals/project-settings/#stream-chunk-size) in *game.project*. This may help you get the sound cache size down even further if you have many sound files loaded at the same time. Sound files smaller than the sound chunk size, aren't streamed and if a new chunk doesn't fit into the cache, the oldest chunk is evicted

::: important
The total size of the sound chunk cache should be larger than the number of loaded sound files times the stream chunk size. Otherwise, you risk evicting new chunks each frame and sounds won't play properly
:::
