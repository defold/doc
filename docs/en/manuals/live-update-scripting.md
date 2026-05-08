---
title: Scripting Live Update content
brief: To use the live update content, you need to download and mount the data to your game. Learn how to script with live update in this manual.
---

# Scripting Live Update

The api only consists of a few functions:

* `liveupdate.add_mount()`
* `liveupdate.remove_mount()`
* `liveupdate.get_mounts()`.

::: important
The legacy single-resource Live Update flow is deprecated. Avoid `collectionproxy.missing_resources()` and the old `resource.*` helper aliases in new code. Current Live Update workflows download and mount whole archives, optionally using `collectionproxy.get_resources()` to inspect which excluded content belongs to a proxy.
:::

## Get mounts

If you are using more than one live update archive, it is recommended to loop over each mount
at startup and determine if the mount should still be used.

This is important as the content may be not be valid for the engine anymore, due to file format changes.

```lua
local function remove_old_mounts()
	local mounts = liveupdate.get_mounts() -- table with mounts

    -- Each mount has: mount.uri, mount.priority, mount.name
	for _,mount in ipairs(mounts) do

        -- This requires the file name to be unique, so that we don't get a file from a different archive
        -- This data is created by the developer as a way to specify meta data for the archive
		local version_data = sys.load_resource("/version_" .. mount.name .. ".json")

		if version_data then
			version_data = json.decode(version_data)
		else
			version_data = {version = 0} -- if it has no version file, it's likely an old/invalid archive
		end

        -- verify the archive version against the version supported by the game
        if version_data.version < sys.get_config_int("game.minimum_lu_version") then
            -- it was invalid, so we'll unmount it!
            liveupdate.remove_mount(mount.name)
        end
	end
end
```

## Scripting with excluded collection proxies

A collection proxy that has been excluded from bundling works as a normal collection proxy, with one important difference. Sending it a `load` message while it still has resources not available in the bundle storage will cause it to fail.

In the current archive-based workflow, you generally decide which archive or archives a proxy needs ahead of time and mount them before loading. If you need to inspect whether a proxy has excluded content, use `collectionproxy.get_resources()`. The older `collectionproxy.missing_resources()` function belongs to the deprecated single-resource Live Update flow.

With *Strip Live Update Entries from Main Manifest* enabled, which is the default when publishing archive-based Live Update content:

* If no mounted archive contains the proxy's excluded content, `collectionproxy.get_resources("#proxy")` returns an empty table `{}`.
* After the relevant archive has been mounted, `collectionproxy.get_resources("#proxy")` returns a non-empty table of resource hashes for that proxy, for example:

```lua
{
    "a1b2c3...",
    "d4e5f6...",
    "7890ab...",
    ...
}
```

 The following example code assumes that the resources are available via the url specified in the setting `game.http_url`.

```lua

-- You'll need to track which archive contains which content
-- In this example, we only use a single liveupdate archive, containing all missing resource.
-- If you are using multiple archive, you need to structure the downloads accordingly
local lu_infos = {
    liveupdate = {
        name = "liveupdate",
        priority = 10,
    }
}

local function get_lu_info_for_level(level_name)
    if level_name == "level1" then
        return lu_infos['liveupdate']
    end
end

local function mount_zip(self, name, priority, path, callback)
	liveupdate.add_mount(name, "zip:" .. path, priority, function(_uri, _path, _status) -- <1>
		callback(_uri, _path, _status)
	end)
end

local function has_mount(name)
    for _, mount in ipairs(liveupdate.get_mounts()) do
        if mount.name == name then
            return true
        end
    end
    return false
end

function init(self)
    self.http_url = sys.get_config_string("game.http_url", nil) -- <2>

    local level_name = "level1"

    local info = get_lu_info_for_level(level_name) -- <3>

    msg.post("#", "load_level", {level = "level1", info = info }) -- <4>
end

function on_message(self, message_id, message, sender)
    if message_id == hash("load_level") then
        local proxy_resources = collectionproxy.get_resources("#" .. message.level) -- <5>

        -- With Strip Live Update Entries from Main Manifest enabled, this table is
        -- empty until the relevant archive is mounted. After mounting, it contains
        -- the resource hashes belonging to the proxy.
        if message.info and #proxy_resources == 0 and not has_mount(message.info.name) then
            msg.post("#", "download_archive", message) -- <6>
        else
            msg.post("#" .. message.level, "load")
        end

    elseif message_id == hash("download_archive") then
		local zip_filename = message.info.name .. ".zip"
		local download_path = sys.get_save_file("mygame", zip_filename)
        local url = self.http_url .. "/" .. zip_filename

        -- Make the request. You can use credentials
        http.request(url, "GET", function(self, id, response) -- <7>
			if response.status == 200 or response.status == 304 then
				mount_zip(self, message.info.name, message.info.priority, download_path, function(uri, path, status) -- <8>
					msg.post("#", "load_level", message) -- try to load the level again
				end)

			else
				print("Failed to download archive ", download_path, "from", url, ":", response.status)
			end
		end, nil, nil, {path=download_path})

    elseif message_id == hash("proxy_loaded") then -- the level is loaded, and we can enable it
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

1. The `liveupdate.add_mount()` mounts a single archive using a specified name, priority and a zip file. The data is then immediately available for loading (there is no need to restart the engine).
The mount info is stored and will be automatically re-added upon next engine restart (no need to call liveupdate.add_mount() again on the same mount)
2. You need to store the archive online (e.g. on S3), where you can download it from.
3. Given a collection proxy name, you need to figure our which archive(s) to download, and how to mount them
4. At startup, we try to load the level.
5. Use `collectionproxy.get_resources()` to inspect the proxy's excluded content. With the default stripped-manifest setting enabled, it returns `{}` until the relevant archive is mounted, and a non-empty table of resource hashes after mounting.
6. If the proxy uses Live Update content and the matching archive is not mounted yet, we download and mount it before loading the proxy.
7. Make a http request and download the archive to `download_path`
8. The data is downloaded, and it's time to mount it to the running engine.


With the loading code in place, we can test the application. However, running it from the editor will not download anything. This is because Live update is a bundle feature. When running in the editor environment no resources are ever excluded. To make sure everything works fine, we need to create a bundle.
