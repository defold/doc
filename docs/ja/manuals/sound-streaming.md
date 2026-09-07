---
title: Defold のサウンドストリーミング
brief: このマニュアルでは、Defold ゲームエンジンにサウンドをストリーミングする方法を説明します
---

# サウンドストリーミング {#sound-streaming}

既定の動作ではサウンドデータをすべて読み込みますが、使用する前にチャンク単位でデータを読み込むことが役立つ場合もあります。これは一般に「ストリーミング（streaming）」と呼ばれます。

サウンドストリーミングの利点の1つは、実行時に必要なメモリを減らせることです。また、たとえば HTTP URL からコンテンツをストリーミングする場合は、いつでもコンテンツを更新でき、最初のダウンロードも避けられます。

### サンプル {#example}

この構成を紹介するサンプルプロジェクトがあります: [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming)

## サウンドストリーミングを有効にする方法 {#how-to-enable-streaming-sounds}

### 簡単な方法 {#easy-way}

サウンドストリーミングを使う最も簡単な方法は、*game.project* の [`sound.stream_enabled` 設定](https://defold.com/manuals/project-settings/#stream-enabled)を有効にすることです。このオプションを有効にすると、エンジンはサウンドのストリーミングを開始します。

注意: 多数のサウンドファイルを同時に読み込む場合は、`sound.stream_cache_size` の値を増やす必要があるかもしれません（後述）。

### 実行時のリソース {#runtime-resources}

新しいサウンドデータリソース（sound data resource）を作成し、サウンドコンポーネント（sound component）に設定することもできます。

手順は次のとおりです:
* サウンドファイルのデータの先頭部分を読み込みます
    * 注意: これは ogg/wav ヘッダーを含む、加工されていないサウンドファイルです
* [`resource.create_sound_data()`](/ref/resource/#resource.create_sound_data) を呼び出して、新しいサウンドデータリソースを作成します。
* [`go.set()`](/ref/go#go.set) を使って、新しいサウンドデータリソースをサウンドコンポーネントに設定します

以下はサンプルプロジェクトからの抜粋で、`http.request()` を使ってサウンドファイルの先頭部分を取得します。

::: sidenote
実際にストリーミングするには、ウェブサーバーが [HTTP 範囲リクエスト](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Range_requests)に従い、ステータス `206` を返す必要があります。サーバーが `Range` ヘッダーを無視してステータス `200` を返す場合、以下のサンプルでは、代わりにレスポンス全体からストリーミングしない通常のリソースを作成します。
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

## リソースプロバイダー {#resource-providers}

サウンドファイルの最初のチャンクは、ほかの方法でも読み込めます。覚えておくべき重要な点は、残りのチャンクがリソースシステムとそのリソースプロバイダー（resource provider）から読み込まれることです。このサンプルでは、[liveupdate.add_mount()](/ref/liveupdate/#liveupdate.add_mount) を呼び出して Live Update のマウントを追加することで、新しい HTTP ファイルプロバイダーを追加します。

動作するサンプルは [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming) にあります。

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

## サウンドチャンクのキャッシュ {#sound-chunk-cache}

サウンドが実行時に消費するメモリ容量は、*game.project* の [`sound.stream_cache_size` 設定](https://defold.com/manuals/project-settings/#stream-cache-size)で制御します。この上限により、読み込まれたサウンドデータがこの上限を超えることはありません。

各サウンドファイルの最初のチャンクはキャッシュから削除できず、リソースが読み込まれている間はキャッシュを占有します。最初のチャンクのサイズは、*game.project* の [`sound.stream_preload_size` 設定](https://defold.com/manuals/project-settings/#stream-preload-size)で制御します。

*game.project* の [`sound.stream_chunk_size` 設定](https://defold.com/manuals/project-settings/#stream-chunk-size)を変更することで、各サウンドチャンクのサイズも制御できます。多数のサウンドファイルを同時に読み込む場合に、サウンドキャッシュのサイズをさらに小さくできる可能性があります。サウンドチャンクのサイズより小さいサウンドファイルはストリーミングされません。また、新しいチャンクがキャッシュに収まらない場合は、最も古いチャンクが削除されます。

::: important
サウンドチャンクキャッシュの合計サイズは、読み込まれたサウンドファイルの数にストリームチャンクのサイズを掛けた値より大きくしてください。そうしないと、毎フレーム新しいチャンクがキャッシュから削除されるおそれがあり、サウンドが正しく再生されなくなります。
:::
