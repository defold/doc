---
title: Live Update コンテンツのスクリプティング
brief: Live Update コンテンツを使うには、データをダウンロードしてゲームにマウントする必要があります。このマニュアルでは、Live Update をスクリプトで扱う方法を説明します。
---

# Live Update のスクリプティング {#scripting-live-update}

マウント（mount）の基本的なワークフローでは、`liveupdate.add_mount()`、`liveupdate.remove_mount()`、`liveupdate.get_mounts()` を使います。利用できるすべての関数については、[`liveupdate` API リファレンス](/ref/liveupdate/)を参照してください。

バンドル（bundle）のビルドマニフェストが、除外された Live Update コンテンツを前提としているかどうかをコードで判別する必要がある場合は、`liveupdate.is_built_with_excluded_files()` を使います。

```lua
if liveupdate.is_built_with_excluded_files() then
    print("The bundle expects excluded Live Update content")
end
```

この関数が返すのは、ビルドマニフェストのメタデータに関する情報だけです。現在アーカイブがマウントされていることや、特定のリソース（resource）が利用できることを意味するものではありません。有効なマウントを調べるには `liveupdate.get_mounts()` を使い、コレクションプロキシ（collection proxy）に対してマニフェストに記録されたリソースのハッシュ値を調べるには [`collectionproxy.get_resources()`](/ref/collectionproxy/#collectionproxy.get_resources) を使います。

推奨するワークフローは、完全な Zip アーカイブをダウンロードし、`zip:` URI を使ってマウントする方法です。

## マウントの取得 {#get-mounts}

`liveupdate.get_mounts()` は、現在のセッションで有効なマウントを返します。各エントリーには、文字列の `uri`、数値の `priority`、ハッシュ値の `name` があります。このリストには、優先度がゼロ未満で削除できない、エンジンの基本マウントも含まれます。

再起動後に、エンジンがマウントを復元することはありません。アプリケーションが後のセッションでダウンロード済みのコンテンツを必要とする場合は、パッケージの URI、名前、優先度を独自のセーブデータに永続化し、起動時に `liveupdate.add_mount()` を再度呼び出す必要があります。

複数のパッケージをマウントする場合は、それぞれのパッケージにある、アプリケーションで定義したメタデータを検証すると便利です。`mount.name` はハッシュ値なので、テーブルのキーとして使うか、`hash("mount-name")` と比較してください。リソースパスに連結しないでください。次の例では、各名前のハッシュ値を、一意のメタデータリソースパスに対応付けています。

```lua
local function remove_old_mounts()
	local mounts = liveupdate.get_mounts() -- table with mounts
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
			version_data = {version = 0} -- if it has no version file, it's likely an old/invalid archive
		end

		-- Ignore the engine's base mounts, which have negative priorities.
		if version_data and version_data.version < sys.get_config_int("game.minimum_lu_version") then
			liveupdate.remove_mount(mount.name)
		end
	end
end
```

パッケージごとに異なるメタデータパスを使ってください。リソースの検索はマウントの優先度に従うため、複数のパッケージで同じパスを使うと、最も優先度の高いマウントにあるデータが読み込まれます。

## 除外したコレクションプロキシのスクリプティング {#scripting-with-excluded-collection-proxies}

バンドル作成から除外したコレクションプロキシは、通常のコレクションプロキシと同じように動作しますが、重要な違いが1つあります。バンドルのストレージで利用できないリソースがまだある状態で `load` メッセージを送信すると、読み込みに失敗します。

アーカイブを使うワークフローでは、通常、プロキシに必要な1つまたは複数のアーカイブをあらかじめ決め、読み込みの前にマウントします。対象の除外済みプロキシについて、マニフェストに記録されたリソースのハッシュ値を調べるには、`collectionproxy.get_resources()` を使います。

パッケージをマウントした後は、除外されていて未読み込みのプロキシの参照先を、`collectionproxy.set_collection()` で別のコンパイル済みコレクション（collection）に変更することもできます。制約と読み込み順序については、[除外したプロキシのコレクションを変更する](/manuals/collection-proxy/#changing-an-excluded-proxys-collection)を参照してください。

Live Update コンテンツを公開するアーカイブビルドでは、バンドルに同梱されるメインマニフェストからは除外された Live Update のエントリーが省かれ、公開されるパッケージのマニフェストにはそれらが保持されます。`collectionproxy.get_resources()` はマニフェストの依存関係メタデータを読み取ります。参照先のすべてのデータブロブが利用できるかどうかを検証するものではありません。

* プロキシの除外されたエントリーを含むパッケージマニフェストがマウントされる前は、`collectionproxy.get_resources("#proxy")` は空のテーブル `{}` を返します。
* 該当するパッケージがマウントされると、そのプロキシのリソースのハッシュ値を含む、空ではないテーブルを返します。たとえば、次のようになります。

```lua
{
    "a1b2c3...",
    "d4e5f6...",
    "7890ab...",
    ...
}
```

 次のコード例では、設定 `game.http_url` で指定された URL からリソースを利用できることを前提としています。

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

        -- A build that publishes Live Update content omits excluded entries from the
        -- bundled manifest, so this table is empty until the relevant package manifest
        -- is mounted. After mounting, it contains the resource hashes for the proxy.
        if message.info and #proxy_resources == 0 and not has_mount(message.info.name) then
            msg.post("#", "download_archive", message) -- <6>
        else
            msg.post("#" .. message.level, "load")
        end

    elseif message_id == hash("download_archive") then
        local zip_filename = message.info.name .. ".zip"
        local download_path = sys.get_save_file("mygame", zip_filename)
        local url = self.http_url .. "/" .. zip_filename

        -- Check if the archive already exists. If it does, try to mount it!
        if sys.exists(download_path) then
            mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                if result == liveupdate.LIVEUPDATE_OK then
                    msg.post("#", "load_level", message) -- try to load the level again
                else
                    os.remove(download_path)             -- remove and try to
                    msg.post("#", "load_level", message) -- download again
                end
            end)
        else
            -- Make the request. You can use credentials
            http.request(url, "GET", function(self, id, response) -- <7>
                if response.status == 200 or response.status == 304 then
                    mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                        if result == liveupdate.LIVEUPDATE_OK then
                            msg.post("#", "load_level", message) -- try to load the level again
                        else
                            print("Failed to mount archive", download_path, ":", result)
                        end
                    end)
                else
                    print("Failed to download archive", download_path, "from", url, ":", response.status)
                end
            end, nil, nil, {path=download_path})
        end

    elseif message_id == hash("proxy_loaded") then -- the level is loaded, and we can enable it
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

1. `liveupdate.add_mount()` は、指定した名前、優先度、zip ファイルを使って1つのアーカイブをマウントします。これにより、データはすぐに読み込み可能になります（エンジンを再起動する必要はありません）。マウントは現在のセッションでのみ有効です。ダウンロードしたパッケージのパスと必要なマウント設定を独自のセーブデータに永続化し、再起動するたびに `liveupdate.add_mount()` を再度呼び出してください。
2. ダウンロードできるように、アーカイブをオンライン（たとえば S3）に保存する必要があります。
3. コレクションプロキシの名前から、ダウンロードするアーカイブと、そのマウント方法を判断する必要があります。
4. 起動時に、レベルの読み込みを試みます。
5. このアーカイブを公開するワークフローでは、`collectionproxy.get_resources()` を使って、プロキシの除外されたコンテンツのメタデータを調べます。該当するパッケージマニフェストがマウントされるまでは `{}` を返し、マウント後はリソースのハッシュ値を含む、空ではないテーブルを返します。これらのハッシュ値は依存関係を表しており、この結果自体がすべてのデータブロブの利用可否を検証するものではありません。
6. プロキシが Live Update コンテンツを使っていて、対応するアーカイブがまだマウントされていない場合は、プロキシを読み込む前にアーカイブをダウンロードしてマウントします。
7. HTTP リクエストを送信し、アーカイブを `download_path` にダウンロードします。
8. データのダウンロードが完了したら、実行中のエンジンにマウントします。


読み込みコードを用意できたので、アプリケーションをテストできます。ただし、エディターから実行しても何もダウンロードされません。これは、Live Update がバンドルの機能だからです。エディター環境で実行する場合は、リソースが除外されることはありません。すべてが正常に動作することを確認するには、バンドルを作成する必要があります。
