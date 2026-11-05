---
title: Live Update 컨텐츠 스크립팅
brief: Live Update 컨텐츠를 사용하려면 데이터를 게임에 다운로드하고 마운트해야 합니다. 이 매뉴얼에서는 Live Update를 스크립트로 사용하는 방법을 알아봅니다.
---

# Live Update 스크립팅

핵심 마운트 워크플로우에서는 `liveupdate.add_mount()`, `liveupdate.remove_mount()`, `liveupdate.get_mounts()`를 사용합니다. 사용 가능한 모든 함수는 전체 [`liveupdate` API 레퍼런스](/ref/liveupdate/)를 참고하세요.

코드에서 빌드 manifest가 제외된 Live Update 컨텐츠를 요구하는 번들인지 구분해야 한다면 `liveupdate.is_built_with_excluded_files()`를 사용하세요.

```lua
if liveupdate.is_built_with_excluded_files() then
    print("The bundle expects excluded Live Update content")
end
```

이 함수는 빌드 manifest 메타데이터만 보고합니다. 현재 아카이브가 마운트되었거나 특정 리소스를 사용할 수 있다는 뜻은 아닙니다. 활성 마운트는 `liveupdate.get_mounts()`로, 컬렉션 프록시에 대해 manifest에 기록된 리소스 해쉬는 [`collectionproxy.get_resources()`](/ref/collectionproxy/#collectionproxy.get_resources)로 검사하세요.

권장 방식은 전체 Zip 아카이브를 다운로드하고 `zip:` URI로 마운트하는 것입니다.

## 마운트 가져오기

`liveupdate.get_mounts()`는 현재 세션에서 활성화된 마운트를 반환합니다. 각 항목에는 `uri` 문자열, 숫자 `priority`, `name` 해쉬가 있습니다. 목록에는 우선순위가 0 미만이며 제거할 수 없는 엔진의 기본 마운트도 포함됩니다.

엔진은 재시작 후 마운트를 복원하지 않습니다. 다음 세션에서 이전에 다운로드한 컨텐츠가 필요하다면 어플리케이션이 자체 저장 데이터에 패키지 URI, 이름, 우선순위를 보관하고 시작 시 `liveupdate.add_mount()`를 다시 호출해야 합니다.

여러 패키지를 마운트할 때는 어플리케이션이 정의한 메타데이터를 검증하는 것이 좋습니다. `mount.name`은 해쉬이므로 테이블 키로 사용하거나 `hash("mount-name")`과 비교하세요. 리소스 경로에 이어 붙이면 안 됩니다. 다음 예제는 각 이름 해쉬를 고유한 메타데이터 리소스 경로에 매핑합니다:

```lua
local function remove_old_mounts()
	local mounts = liveupdate.get_mounts() -- 마운트가 담긴 테이블
	local version_resources = {
		[hash("level-pack")] = "/version_level_pack.json",
		[hash("season-pack")] = "/version_season_pack.json",
	}

	for _, mount in ipairs(mounts) do
		local version_resource = version_resources[mount.name]
		local version_data = version_resource and sys.load_resource(version_resource)

		if version_data then
			version_data = json.decode(version_data)
		elseif mount.priority >= 0 then
			version_data = {version = 0} -- 버전 파일이 없다면 오래되었거나 유효하지 않은 아카이브일 가능성이 큽니다
		end

		-- 우선순위가 음수인 엔진의 기본 마운트는 무시합니다.
		if version_data and version_data.version < sys.get_config_int("game.minimum_lu_version") then
			liveupdate.remove_mount(mount.name)
		end
	end
end
```

패키지마다 고유한 메타데이터 경로를 사용하세요. 리소스 조회는 마운트 우선순위를 따르므로 여러 패키지에서 같은 경로를 사용하면 가장 높은 우선순위의 마운트에 있는 복사본을 읽게 됩니다.

## 제외된 컬렉션 프록시로 스크립팅하기

번들링에서 제외된 컬렉션 프록시는 일반 컬렉션 프록시처럼 동작하지만, 한 가지 중요한 차이가 있습니다. 번들 스토리지에 아직 사용할 수 없는 리소스가 남아 있는 상태에서 `load` 메세지를 보내면 실패합니다.

아카이브 기반 워크플로우에서는 보통 프록시에 필요한 아카이브를 미리 결정하고, 로드하기 전에 해당 아카이브를 마운트합니다. 알려진 제외 프록시에 대해 manifest에 기록된 리소스 해쉬를 검사하려면 `collectionproxy.get_resources()`를 사용하세요.

패키지를 마운트한 뒤에는 제외되어 있고 로드되지 않은 프록시를 `collectionproxy.set_collection()`으로 다른 컴파일된 컬렉션으로 전환할 수도 있습니다. 제한사항과 로드 순서는 [제외된 프록시의 컬렉션 변경하기](/manuals/collection-proxy/#changing-an-excluded-proxys-collection)를 참고하세요.

Live Update 컨텐츠를 게시하는 아카이브 빌드에서는 번들된 메인 manifest에서 제외된 Live Update 항목을 생략하지만 게시된 패키지 manifest에는 유지합니다. `collectionproxy.get_resources()`는 manifest의 종속성 메타데이터를 읽으며, 참조된 모든 데이터 blob을 실제로 사용할 수 있는지는 확인하지 않습니다.

* 프록시의 제외 항목을 포함하는 패키지 manifest를 마운트하기 전에는 `collectionproxy.get_resources("#proxy")`가 빈 테이블 `{}`를 반환합니다.
* 관련 패키지를 마운트한 뒤에는 해당 프록시의 리소스 해쉬가 담긴 비어 있지 않은 테이블을 반환합니다. 예:

```lua
{
    "a1b2c3...",
    "d4e5f6...",
    "7890ab...",
    ...
}
```

다음 예제 코드는 설정값 `game.http_url`에 지정된 URL을 통해 리소스를 사용할 수 있다고 가정합니다.

```lua

-- 어떤 아카이브가 어떤 컨텐츠를 포함하는지 추적해야 합니다
-- 이 예제에서는 누락된 모든 리소스를 포함하는 liveupdate 아카이브 하나만 사용합니다.
-- 여러 아카이브를 사용하는 경우 그에 맞게 다운로드를 구성해야 합니다
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

        -- Live Update 컨텐츠를 게시하는 빌드는 번들된 manifest에서 제외 항목을
        -- 생략하므로, 관련 패키지 manifest가 마운트될 때까지 이 테이블은 비어 있습니다.
        -- 마운트 후에는 프록시의 리소스 해쉬가 들어 있습니다.
        if message.info and #proxy_resources == 0 and not has_mount(message.info.name) then
            msg.post("#", "download_archive", message) -- <6>
        else
            msg.post("#" .. message.level, "load")
        end

    elseif message_id == hash("download_archive") then
        local zip_filename = message.info.name .. ".zip"
        local download_path = sys.get_save_file("mygame", zip_filename)
        local url = self.http_url .. "/" .. zip_filename

        -- 아카이브가 이미 존재하는지 확인합니다. 있다면 마운트를 시도합니다!
        if sys.exists(download_path) then
            mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                if result == liveupdate.LIVEUPDATE_OK then
                    msg.post("#", "load_level", message) -- 레벨 로드를 다시 시도합니다
                else
                    os.remove(download_path)             -- 파일을 삭제하고 다시
                    msg.post("#", "load_level", message) -- 다운로드를 시도합니다
                end
            end)
        else
            -- 요청을 보냅니다. 자격 증명을 사용할 수 있습니다
            http.request(url, "GET", function(self, id, response) -- <7>
                if response.status == 200 or response.status == 304 then
                    mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                        if result == liveupdate.LIVEUPDATE_OK then
                            msg.post("#", "load_level", message) -- 레벨 로드를 다시 시도합니다
                        else
                            print("Failed to mount archive", download_path, ":", result)
                        end
                    end)
                else
                    print("Failed to download archive", download_path, "from", url, ":", response.status)
                end
            end, nil, nil, {path=download_path})
        end

    elseif message_id == hash("proxy_loaded") then -- 레벨이 로드되었으므로 활성화할 수 있습니다
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

1. `liveupdate.add_mount()`는 지정된 이름, 우선순위, zip 파일을 사용해 단일 아카이브를 마운트합니다. 그러면 데이터를 즉시 로드할 수 있습니다(엔진을 재시작할 필요가 없습니다). 마운트는 현재 세션에서만 활성화됩니다. 다운로드한 패키지 경로와 원하는 마운트 설정을 자체 저장 데이터에 유지하고 재시작할 때마다 `liveupdate.add_mount()`를 다시 호출하세요.
2. 아카이브는 다운로드할 수 있는 온라인 위치(예: S3)에 저장해야 합니다.
3. 컬렉션 프록시 이름이 주어지면 어떤 아카이브를 다운로드해야 하는지, 그리고 어떻게 마운트해야 하는지 알아내야 합니다.
4. 시작 시 레벨 로드를 시도합니다.
5. 이 아카이브 게시 워크플로우에서는 `collectionproxy.get_resources()`를 사용해 프록시의 제외된 컨텐츠 메타데이터를 검사합니다. 관련 패키지 manifest가 마운트될 때까지 `{}`를 반환하고, 마운트 후에는 리소스 해쉬가 담긴 비어 있지 않은 테이블을 반환합니다. 이 해쉬는 종속성을 설명하며, 반환 결과 자체가 모든 데이터 blob을 사용할 수 있음을 검증하지는 않습니다.
6. 프록시가 Live Update 컨텐츠를 사용하고 일치하는 아카이브가 아직 마운트되지 않았다면 프록시를 로드하기 전에 해당 아카이브를 다운로드하고 마운트합니다.
7. HTTP 요청을 보내고 아카이브를 `download_path`에 다운로드합니다.
8. 데이터가 다운로드되었으므로 실행 중인 엔진에 마운트할 차례입니다.


로드 코드가 준비되었으니 어플리케이션을 테스트할 수 있습니다. 하지만 에디터에서 실행하면 아무것도 다운로드하지 않습니다. Live Update는 번들 기능이기 때문입니다. 에디터 환경에서 실행할 때는 어떤 리소스도 제외되지 않습니다. 모든 것이 제대로 동작하는지 확인하려면 번들을 만들어야 합니다.
