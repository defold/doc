---
title: 热更新脚本
brief: 使用热更新, 需要下载并挂载游戏数据. 本手册介绍了热更新脚本.
---

# 热更新脚本
[live-update-scripting.md](live-update-scripting.md)
热更新API只是如下几个函数:

* `liveupdate.add_mount()`
* `liveupdate.remove_mount()`
* `liveupdate.get_mounts()`.

## 得到 mounts

如果使用一个以上的热更新卷, 推荐在启动时遍历每个 mount
来检测这个 mount 是否还在使用中.

这很重要因为内容可能对于引擎来说不在可用, 因为文件格式改变了.

```lua
local function remove_old_mounts()
	local mounts = liveupdate.get_mounts() -- 得到 mounts 表

    -- 每个 mount 包含: mount.uri, mount.priority, mount.name
	for _,mount in ipairs(mounts) do

        -- 这需要文件名是唯一的, 以便我们不会从不同卷里获得同名文件
        -- 这里数据由开发者创建作为给卷指定元数据的方法
		local version_data = sys.load_resource("/version_" .. mount.name .. ".json")

		if version_data then
			version_data = json.decode(version_data)
		else
			version_data = {version = 0} -- 没有版本文件的话, 很可能是老旧/不可用卷
		end

        -- 指定卷版本到游戏支持的版本
        if version_data.version < sys.get_config_int("game.minimum_lu_version") then
            -- 不可用的话, 卸载它!
            liveupdate.remove_mount(mount.name)
        end
	end
end
```

## 排除的集合代理脚本

被打包排除的集合代理使用上跟普通集合代理类似, 但有一个重要区别. 当它还有资源没就位的时候给它发送 `load` 消息会直接报错.

所以在给它发送 `load` 之前, 我们检查是否有遗漏的资源. 如果有, 我们需要下载包含这些资源的卷并保存起来.

 下例代码默认资源依照 `game.http_url` 的地址下可得到.

```lua

-- 你要跟踪哪个卷里有那些内容
-- 本例中, 我们只用一个热更新卷, 包含所有遗漏资源.
-- 如果需要用多个卷, 必须相应地构建好下载表
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

function init(self)
    self.http_url = sys.get_config_string("game.http_url", nil) -- <2>

    local level_name = "level1"

    local info = get_lu_archive_for_level(level_name) -- <3>

    msg.post("#", "load_level", {level = "level1", info = info }) -- <4>
end

function on_message(self, message_id, message, sender)
    if message_id == hash("load_level") then
        local missing_resources = collectionproxy.missing_resources("#" .. message.level) -- <5>

        if #missing_resources then
            msg.post("#", "download_archive", message) -- <6>
        else
            msg.post("#" .. message.level, "load")
        end

    elseif message_id == hash("download_archive") then
		local zip_filename = message.info.name .. ".zip"
		local download_path = sys.get_save_file("mygame", zip_filename)
        local url = self.http_url .. "/" .. zip_filename

        -- 开始请求. 可以使用 credentials
        http.request(url, "GET", function(self, id, response) -- <7>
			if response.status == 200 or response.status == 304 then
				mount_zip(self, message.info.name, message.info.priority, download_path, function(uri, path, status) -- <8>
					msg.post("#", "load_level", message) -- 尝试重新加载 level
				end)

			else
				print("Failed to download archive ", download_path, "from", url, ":", get_status_string(status))
			end
		end, nil, nil, {path=download_path})

    elseif message_id == hash("proxy_loaded") then -- level 已加载, 可以 enable 了
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

1. 依照指定名称, 优先级和 zip 文件, 使用 `liveupdate.add_mount()` 挂载一个卷. 数据马上便可以用于加载 (不用重启引擎).
mount 信息被保存然后下次引擎重启便会被自动读取 (同一 mount 不必再一次调用 liveupdate.add_mount())
2. 线上保存卷 (比如放在 S3 上), 以便等待下载.
3. 提供集合代理名, 要指出哪个卷需要下载, 然后如何挂载
4. 游戏开始, 尝试载入 level.
5. 检查集合代理的所有资源已就位.
6. 如果有遗漏资源, 需要下载卷然后挂载它.
7. 提出 http 请求, 下载卷到 `download_path`
8. 数据已下载, 应该给当前引擎挂载它.


载入代码完成后, 我们就可以测试游戏了. 然而, 从编辑器里运行游戏不会下载任何东西. 这是因为热更新是一个游戏包特性. 在编辑器环境运行游戏所有资源都就位. 为了测试该特性, 我们需要打游戏包.
