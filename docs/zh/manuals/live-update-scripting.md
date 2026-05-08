---
title: Live Update脚本编写
brief: 要使用 live update 内容，您需要将数据下载并挂载到游戏中。在本手册中学习如何使用 live update 进行脚本编写。
---

# Live Update 脚本编写

API 仅包含几个函数：

* `liveupdate.add_mount()`
* `liveupdate.remove_mount()`
* `liveupdate.get_mounts()`。

::: important
旧的按单个资源处理的 Live Update 流程已弃用。新代码中不要再使用 `collectionproxy.missing_resources()` 以及旧的 `resource.*` 辅助别名。当前的 Live Update 工作流应下载并挂载整个归档文件；如果需要检查某个代理关联了哪些被排除的内容，可以使用 `collectionproxy.get_resources()`。
:::

## 获取挂载点

如果您使用多个 live update 归档文件，建议在启动时遍历每个挂载点
并确定是否仍应使用该挂载点。

这很重要，因为由于文件格式更改，内容可能对引擎不再有效。

```lua
local function remove_old_mounts()
	local mounts = liveupdate.get_mounts() -- 包含挂载点的表

    -- 每个挂载点包含：mount.uri, mount.priority, mount.name
	for _,mount in ipairs(mounts) do

        -- 这需要文件名是唯一的，这样我们就不会从不同的归档文件中获取文件
        -- 这些数据由开发人员创建，作为为归档文件指定元数据的方式
		local version_data = sys.load_resource("/version_" .. mount.name .. ".json")

		if version_data then
			version_data = json.decode(version_data)
		else
			version_data = {version = 0} -- 如果没有版本文件，它可能是旧的/无效的归档文件
		end

        -- 验证归档文件版本与游戏支持的版本
        if version_data.version < sys.get_config_int("game.minimum_lu_version") then
            -- 它无效，所以我们卸载它！
            liveupdate.remove_mount(mount.name)
        end
	end
end
```

## 使用排除的集合代理进行脚本编写

被排除在打包之外的集合代理与普通集合代理的工作方式类似，但有一个重要区别。当它仍然有在捆绑存储中不可用的资源时，向它发送 `load` 消息将导致它失败。

在当前基于归档的工作流中，通常应预先确定某个代理需要哪个或哪些归档文件，并在加载之前先挂载它们。如果需要检查代理是否引用了被排除的内容，请使用 `collectionproxy.get_resources()`。较旧的 `collectionproxy.missing_resources()` 属于已弃用的单资源 Live Update 流程。

当启用 *Strip Live Update Entries from Main Manifest* 时，也就是发布基于归档的 Live Update 内容时的默认设置：

* 如果当前没有任何已挂载归档包含该代理所需的被排除内容，`collectionproxy.get_resources("#proxy")` 会返回空表 `{}`；
* 挂载相关归档后，`collectionproxy.get_resources("#proxy")` 会返回一个非空表，其中包含该代理的资源哈希，例如：

```lua
{
    "a1b2c3...",
    "d4e5f6...",
    "7890ab...",
    ...
}

以下示例代码假设资源可以通过设置 `game.http_url` 中指定的 URL 获得。

```lua

-- 您需要跟踪哪个归档文件包含哪些内容
-- 在本例中，我们只使用一个 liveupdate 归档文件，包含所有缺失的资源。
-- 如果您使用多个归档文件，您需要相应地构建下载
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

        -- 启用 Strip Live Update Entries from Main Manifest 后，
        -- 在相关归档挂载之前这个表会保持为空。
        -- 挂载之后，它会包含属于该代理的资源哈希。
        if message.info and #proxy_resources == 0 and not has_mount(message.info.name) then
            msg.post("#", "download_archive", message) -- <6>
        else
            msg.post("#" .. message.level, "load")
        end

    elseif message_id == hash("download_archive") then
		local zip_filename = message.info.name .. ".zip"
		local download_path = sys.get_save_file("mygame", zip_filename)
        local url = self.http_url .. "/" .. zip_filename

        -- 发出请求。您可以使用凭据
        http.request(url, "GET", function(self, id, response) -- <7>
			if response.status == 200 or response.status == 304 then
				mount_zip(self, message.info.name, message.info.priority, download_path, function(uri, path, status) -- <8>
					msg.post("#", "load_level", message) -- 再次尝试加载关卡
				end)

			else
				print("Failed to download archive ", download_path, "from", url, ":", response.status)
			end
		end, nil, nil, {path=download_path})

    elseif message_id == hash("proxy_loaded") then -- 关卡已加载，我们可以启用它
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

1. `liveupdate.add_mount()` 使用指定的名称、优先级和 zip 文件挂载单个归档文件。数据立即可用于加载（无需重启引擎）。
挂载点信息被存储，并在下次引擎重启时自动重新添加（无需在同一挂载点上再次调用 liveupdate.add_mount()）
2. 您需要将归档文件在线存储（例如在 S3 上），以便您可以从中下载。
3. 给定集合代理名称，您需要确定要下载哪些归档文件，以及如何挂载它们
4. 在启动时，我们尝试加载关卡。
5. 使用 `collectionproxy.get_resources()` 检查该代理的被排除内容。在默认的 stripped-manifest 设置下，它会在相关归档挂载前返回 `{}`，挂载后则返回一个包含该代理资源哈希的非空表。
6. 如果该代理使用 Live Update 内容且相关归档尚未挂载，则先下载并挂载该归档，再加载代理。
7. 发出 http 请求并将归档文件下载到 `download_path`
8. 数据已下载，是时候将其挂载到正在运行的引擎上了。


有了加载代码，我们就可以测试应用程序了。但是，从编辑器运行它不会下载任何内容。这是因为 Live update 是一个捆绑功能。在编辑器环境中运行时，资源永远不会被排除。为了确保一切正常，我们需要创建一个捆绑包。
