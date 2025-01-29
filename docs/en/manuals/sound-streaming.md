---
title: Sound Streaming in Defold
brief: This manual explains how to stream sounds into the Defold game engine
---

# Sound Streaming

While the default behaviour is to load sound data in full, it may also be beneficial to load the data in chunks, prior to their use. This is often called "streaming".

One benefit is that the runtime memory is kept low.

Another benefit is that, if you are streaming content from e.g. a http url, you can update the content at any time, and also avoid the initial download.

### Example

There is an example project showcasing this setup: https://github.com/defold/example-sound-streaming

## How to enable streaming sounds

### Easy way

The simplest way to use sound streaming, is by setting the `sound.stream_enabled` to true.
By simply switching on this flag, your project will start streaming the sounds.

Note: If you have lots of sound files loaded at the same time, you may need to up the `sound.stream_cache_size` value.

### Runtime resources

You can also create a new sound data resource, and set it to a sound component.

You do this by:
* Load the initial part of the sound file data
    * Note: This is the raw sound file, including the ogg/wav header
* Calling [resource.create_sound_data()](/ref/resource/#resource.create_sound_data) to get a resource
* Setting the resource to the sound component

Here is an excerpt from the example project, using a `http.request()` to get the initial sound file.
Note that the web server you're loading content from has to support ranged requests.

```Lua
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


You can of course use other means to load the initial chunk of the sound file.
The important thing to remember is that the rest of the chunks are loaded from the resource system and our resource providers.

In this example, we have added a new file provider by adding a live update mount, by calling using [liveupdate.add_mount()](/ref/liveupdate/#liveupdate.add_mount).


## Sound chunk cache

You can control how much memory will be consumed by the sounds at runtime, by setting the size of the "sound chunk cache".
Given this limit, the loaded sound data will never exceed this limit.

Some things to note:

* Sound files smaller than the sound chunk size, aren't streamed.
* If a new chunk doesn't fit into the cache, the oldest chunk is evicted
* If the cache is too small, chunks may get evicted the same frame, and the sound won't play properly.

The initial chunk of each sound file cannot be evicted, so they will occupy the cache as long as the resources are loaded.
You can also control the size of each sound chunk. This may help you get the sound cache size down even further if you have many sound files loaded at the same time.

## Configuration

Currently, the streaming is enabled on all sound resources.
We may improve upon this in the future, allowing settings on individual sound files.

The game project supports these settings:

* `sound.stream_enabled` (default 0) - If enabled, enables streaming of all sound files
* `sound.stream_cache_size` (default 2097152 bytes) - The max size of the cache containing _all_ chunks.
* `sound.stream_chunk_size` (default 16384 bytes) - Determines size of each chunk that is loaded from a file at a time

