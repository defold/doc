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
The web server you're loading content from has to support [HTTP range requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Range_requests).
:::

```lua
local function parse_range(s)
    local _, _, rstart, rend, size = string.find(s, "(%d+)-(%d+)/(%d+)") -- "bytes 0-16383/103277"
    return rstart, rend, size
end

local function http_result(self, _id, response, extra)
    if response.status == 200 or response.status == 206 then
        local relative_path = self.filename
        local range = response.headers['content-range'] -- content-range = "bytes 0-16383/103277"
        local rstart, rend, filesize = parse_range(range)

        -- Create the Defold resource, "partial" will enable the streaming mode
        print("Creating resource", relative_path)
        local hash = resource.create_sound_data(relative_path, { data = response.response, filesize = filesize, partial = true })

        go.set(self.component, "sound", hash) -- override the resource data on the component
        sound.play(self.component) -- start the playing
    end
end

local function load_web_sound(base_url, relative_path)
    local url = base_url .. "/" .. relative_path
    local headers = {}
    headers['Range'] = string.format("bytes=%d-%d", 0, 16384-1)

    http.request(url, "GET", http_result, headers, nil, { ignore_cache = true })
end
```

## Resource providers

You can of course use other means to load the initial chunk of the sound file. The important thing to remember is that the rest of the chunks are loaded from the resource system and it's resource providers.

In this example, we have added a new file provider by adding a live update mount, by calling using [liveupdate.add_mount()](/ref/liveupdate/#liveupdate.add_mount).


## Sound chunk cache

The amount of memory consumed by the sounds at runtime is controlled by the [`sound.stream_cache_size` setting](https://defold.com/manuals/project-settings/#stream-cache-size) in *game.project*. Given this limit, the loaded sound data will never exceed this limit.

The initial chunk of each sound file cannot be evicted and they will occupy the cache for as long as the resources are loaded. The size of the initial chunk is controlled by the [`sound.stream_preload_size` setting](https://defold.com/manuals/project-settings/#stream-preload-size) in *game.project*.

You can also control the size of each sound chunk by changing the [`sound.stream_chunk_size` setting](https://defold.com/manuals/project-settings/#stream-chunk-size) in *game.project*. This may help you get the sound cache size down even further if you have many sound files loaded at the same time. Sound files smaller than the sound chunk size, aren't streamed and if a new chunk doesn't fit into the cache, the oldest chunk is evicted

::: important
The total size of the sound chunk cache should be larger than the number of loaded sound files times the stream chunk size. Otherwise, you risk evicting new chunks each frame and sounds won't play properly
:::