---
title: Live Update脚本编写
brief: 要使用 live update 内容，您需要将数据下载并挂载到游戏中。在本手册中学习如何使用 live update 进行脚本编写。
---

# Live Update 脚本编写

核心挂载工作流程使用 `liveupdate.add_mount()`、`liveupdate.remove_mount()` 和 `liveupdate.get_mounts()`。所有可用函数请参阅完整的 [`liveupdate` API 参考](/ref/liveupdate/)。

当代码需要判断某个包的构建清单是否预期存在被排除的 Live Update 内容时，请使用 `liveupdate.is_built_with_excluded_files()`：

```lua
if liveupdate.is_built_with_excluded_files() then
    print("The bundle expects excluded Live Update content")
end
```

该函数只报告构建清单元数据。它并不表示当前已挂载归档，也不表示某个特定资源可用。请使用 `liveupdate.get_mounts()` 检查活动挂载点，并使用 [`collectionproxy.get_resources()`](/ref/collectionproxy/#collectionproxy.get_resources) 检查清单中记录的集合代理资源哈希。

推荐的流程是下载完整的 Zip 归档，并使用 `zip:` URI 挂载。

## 获取挂载点

`liveupdate.get_mounts()` 返回当前会话中的活动挂载点。每个条目包含 URI `mount.uri`、数字优先级 `mount.priority` 和哈希值 `mount.name`。重启后挂载点不会恢复；应用必须自行保存所需设置，并再次调用 `liveupdate.add_mount()`。

由于 `mount.name` 是哈希值，请将其用作表的键，或与 `hash("name")` 比较；不要将其拼接到路径字符串中。请把每个名称哈希映射到唯一的元数据路径：

```lua
local function remove_old_mounts()
	local mounts = liveupdate.get_mounts() -- 包含挂载点的表
	local version_resources = {
		[hash("liveupdate")] = "/version_liveupdate.json",
	}

    -- 每个挂载点包含：mount.uri, mount.priority, mount.name
	for _,mount in ipairs(mounts) do

        -- 这需要文件名是唯一的，这样我们就不会从不同的归档文件中获取文件
        -- 这些数据由开发人员创建，作为为归档文件指定元数据的方式
		local version_resource = version_resources[mount.name]
		local version_data = version_resource and sys.load_resource(version_resource)

		if version_data then
			version_data = json.decode(version_data)
		elseif mount.priority >= 0 then
			version_data = {version = 0} -- 如果没有版本文件，它可能是旧的/无效的归档文件
		end

        -- 验证归档文件版本与游戏支持的版本
        if version_data and version_data.version < sys.get_config_int("game.minimum_lu_version") then
            -- 它无效，所以我们卸载它！
            liveupdate.remove_mount(mount.name)
        end
	end
end
```

## 使用排除的集合代理进行脚本编写

被排除在打包之外的集合代理与普通集合代理的工作方式类似，但有一个重要区别。当它仍然有在捆绑存储中不可用的资源时，向它发送 `load` 消息将导致它失败。

在基于归档的工作流程中，通常应预先确定某个代理需要哪个或哪些归档文件，并在加载之前先挂载它们。要检查某个已知被排除代理在清单中记录的资源哈希，请使用 `collectionproxy.get_resources()`。

挂载内容包后，还可以使用 `collectionproxy.set_collection()` 将被排除且未加载的代理重定向到另一个已编译集合。有关限制和加载顺序，请参阅[更改被排除代理的集合](/manuals/collection-proxy/#changing-an-excluded-proxys-collection)。

对于发布 Live Update 内容的归档构建，打包在主包中的清单会省略被排除的 Live Update 条目，而发布的内容包清单仍保留这些条目。`collectionproxy.get_resources()` 读取清单依赖元数据；它不会验证每个被引用的数据块是否可用：

* 在包含代理被排除条目的内容包清单挂载之前，`collectionproxy.get_resources("#proxy")` 会返回空表 `{}`。
* 挂载相关内容包后，它会返回一个非空表，其中包含该代理的资源哈希，例如：

```lua
{
    "a1b2c3...",
    "d4e5f6...",
    "7890ab...",
    ...
}
```

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
    liveupdate.add_mount(name, "zip:" .. path, priority, function(_self, _name, _uri, _result) -- <1>
        callback(_name, _uri, _result)
    end)
end

local function has_mount(name)
    local name_hash = hash(name)
    for _, mount in ipairs(liveupdate.get_mounts()) do
        if mount.name == name_hash then
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

        -- 发布 Live Update 内容的构建会从打包的清单中省略被排除条目，
        -- 因此相关内容包清单挂载之前，此表为空。挂载后，
        -- 它会包含该代理的资源哈希。
        if message.info and #proxy_resources == 0 and not has_mount(message.info.name) then
            msg.post("#", "download_archive", message) -- <6>
        else
            msg.post("#" .. message.level, "load")
        end

    elseif message_id == hash("download_archive") then
        local zip_filename = message.info.name .. ".zip"
        local download_path = sys.get_save_file("mygame", zip_filename)
        local url = self.http_url .. "/" .. zip_filename

        -- 检查归档是否已存在。如果存在，请尝试挂载它！
        if sys.exists(download_path) then
            mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                if result == liveupdate.LIVEUPDATE_OK then
                    msg.post("#", "load_level", message) -- 再次尝试加载关卡
                else
                    os.remove(download_path)             -- 删除后尝试
                    msg.post("#", "load_level", message) -- 重新下载
                end
            end)
        else
            -- 发出请求。您可以使用凭据
            http.request(url, "GET", function(self, id, response) -- <7>
                if response.status == 200 or response.status == 304 then
                    mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                        if result == liveupdate.LIVEUPDATE_OK then
                            msg.post("#", "load_level", message) -- 再次尝试加载关卡
                        else
                            print("Failed to mount archive", download_path, ":", result)
                        end
                    end)
                else
                    print("Failed to download archive", download_path, "from", url, ":", response.status)
                end
            end, nil, nil, {path=download_path})
        end

    elseif message_id == hash("proxy_loaded") then -- 关卡已加载，我们可以启用它
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

1. `liveupdate.add_mount()` 使用指定的名称、优先级和 zip 文件挂载单个归档文件。数据立即可用于加载（无需重启引擎）。挂载点仅在当前会话中有效。请在应用自己的持久数据中保存已下载内容包的路径和所需挂载设置，并在每次重启后再次调用 `liveupdate.add_mount()`。
2. 您需要将归档文件在线存储（例如在 S3 上），以便您可以从中下载。
3. 给定集合代理名称，您需要确定要下载哪些归档文件，以及如何挂载它们
4. 在启动时，我们尝试加载关卡。
5. 在这个归档发布工作流程中，使用 `collectionproxy.get_resources()` 检查该代理的被排除内容元数据。相关内容包清单挂载前它返回 `{}`，挂载后则返回一个包含资源哈希的非空表。这些哈希用于描述依赖关系；该结果本身不会验证每个数据块是否可用。
6. 如果该代理使用 Live Update 内容且相关归档尚未挂载，则先下载并挂载该归档，再加载代理。
7. 发出 http 请求并将归档文件下载到 `download_path`
8. 数据已下载，是时候将其挂载到正在运行的引擎上了。


有了加载代码，我们就可以测试应用程序了。但是，从编辑器运行它不会下载任何内容。这是因为 Live update 是一个捆绑功能。在编辑器环境中运行时，资源永远不会被排除。为了确保一切正常，我们需要创建一个捆绑包。
