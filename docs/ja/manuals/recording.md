---
title: Defold での動画録画
brief: このマニュアルでは、Lua またはエンジンの HTTP サービスを使って、ゲームウィンドウを MP4 に録画する方法を説明します。
---

# 動画の録画 {#video-recording}

Defold は、[`recorder` Lua モジュール](/ref/recorder/)または[エンジンの HTTP サービス](/manuals/engine-service/#recording-endpoints)を通じて、ゲームウィンドウを MP4 ファイルの H.264 動画に録画できます。両方のインターフェースは1つのレコーダーを共有するため、一度に開始、実行、確定できる録画は1つだけです。

## 利用条件 {#availability}

録画機能は、デスクトップの**デバッグ**エンジンに含まれます。リリース、ヘッドレス、モバイル、Web の各ビルドには含まれません。[App Manifest](/manuals/app-manifest/#exclude-record) の **Exclude Record** を有効にした場合も、Lua モジュールと HTTP ルートを除外します。

| プラットフォーム | 動画の要件 | アプリケーション音声 |
| --- | --- | --- |
| macOS | macOS 15 以降。ScreenCaptureKit を使用 | 対応 |
| Windows | Windows 10 バージョン 1903 以降。Windows Graphics Capture と Media Foundation を使用 | Windows ビルド 20348 以降で対応 |
| Linux | OpenGL、OpenGL ES、Vulkan。フレームバッファーのキャプチャを使用 | 非対応 |

動画と音声の対応状況は、個別に確認します。HTTP クライアントは `/recording/capabilities` を調べられます。Lua の呼び出しでは、要求したキャプチャが非対応ならエラーを返します。開始要求が受理された後でも、OS の権限やキャプチャデバイスの障害によって、非同期のエラーが発生することがあります。

レコーダーは、ゲームウィンドウの内容を、物理ピクセル単位の実際のサイズでキャプチャします。動画の寸法を偶数にするため、1行または1列を切り取る場合があります。ウィンドウのリサイズやピクセル密度の変更は、録画を停止してファイルを確定させます。キャプチャレートは毎秒1～60フレームで、デフォルトは30です。

## Lua からの録画 {#recording-from-lua}

書き込み可能な出力パスとコールバックを指定して、[`recorder.start()`](/ref/recorder/#recorder.start) を使います。親ディレクトリは存在する必要があります。[`sys.get_save_file()`](/ref/sys/#sys.get_save_file) は、アプリケーションに適した保存パスを提供します。既存の出力ファイルは上書きされる場合があります。Lua の録画ファイルは呼び出し側が管理し、エンジンの終了後もディスクに残ります。

Lua のファイル入出力と同様、パスには Windows では Windows ANSI コードページを、それ以外では UTF-8 を使います。コールバックの `result.path` は、`recorder.start()` に渡したパスを保持します。

次の `.script` の例は、キャプチャ開始から5秒間録画します。

```lua
local function on_recording_event(self, event, result)
    if event == recorder.EVENT_STARTED then
        self.recording = true
        timer.delay(5, false, function(self)
            if self.recording then
                local ok, err = recorder.stop()
                if not ok then
                    print("Could not stop recording:", err)
                end
            end
        end)
    elseif event == recorder.EVENT_STOPPED then
        self.recording = false
        print("MP4 ready:", result.path)
    elseif event == recorder.EVENT_ERROR then
        self.recording = false
        print("Recording failed:", result.error)
    end
end

function init(self)
    self.recording = false
    if not recorder then
        print("Recording is not included in this engine build")
        return
    end

    local ok, err = recorder.start({
        path = sys.get_save_file("recording_example", "capture.mp4"),
        fps = 30,
        audio = false,
    }, on_recording_event)
    if not ok then
        print("Could not start recording:", err)
    end
end
```

`recorder.start()` と [`recorder.stop()`](/ref/recorder/#recorder.stop) は、受理された場合は `true`、拒否された場合は `nil, error` を返します。受理されても、キャプチャやファイルの確定が終わったとは限りません。不正なオプションは Lua エラーを発生させます。

コールバックは、エンジンの更新中に実行します。

| イベント | 意味 |
| --- | --- |
| `recorder.EVENT_STARTED` | キャプチャ中です。停止できるようになります。 |
| `recorder.EVENT_STOPPED` | MP4 が確定し、読み取り可能になりました。リサイズによる自動停止後にも発生します。 |
| `recorder.EVENT_ERROR` | キャプチャに失敗しました。`result.error` を確認します。起動に失敗すると、`EVENT_STARTED` なしで発生することがあります。 |

結果には、`path`、`width`、`height`、`fps`、`audio` も含まれます。出力の読み取りやアップロードは、`EVENT_STOPPED` の後で行ってください。コールバックを受け取るには、開始したスクリプトを存続させます。削除すると、キャプチャは止まらずにコールバックが破棄されます。エンジンの終了では、Lua コールバックを呼ばずにキャプチャを確定します。

音声は、**Lua ではデフォルトで無効**です。対応プラットフォームでアプリケーション音声を要求するには、`audio = true` を設定します。非対応の音声を要求すると、エラーを返します。

### HTTP クライアントとのレコーダーの共有 {#sharing-the-recorder-with-http-clients}

`recorder.stop()` は、HTTP から開始したものも含め、現在の共有録画を対象とします。操作が保留中、または録画が実行中でない場合は、エラーを返します。HTTP クライアントが Lua の録画を停止しても、元の Lua コールバックは完了イベントを受け取ります。HTTP から開始しても Lua コールバックは作成されません。完了の確認には HTTP の状態取得を使います。

HTTP の状態には Lua の録画も表示できますが、その `file` フィールドは `null` です。サービスがダウンロードを準備するのは、HTTP から開始した録画のみです。Lua の録画は、`EVENT_STOPPED` の後で `result.path` から読み取ります。

## HTTP 経由の録画 {#recording-through-http}

録画用ルートは、ゲームログに表示されたエンジンサービスのポートを使います。[エンジンサービスマニュアル](/manuals/engine-service/#discovering-operations-through-openapi)に従い、`/openapi.json` で検出します。ヘッドレスエンジンとリリースエンジンは、これらを公開しません。

以下のコマンドは、POSIX シェル、`curl`、`jq` を使います。ダウンロードの検証では Python 3 も使います。同じシェルで実行し、`<port>` を実行中のエンジンのポートに置き換えます。まず、利用可能な機能を問い合わせ、サービスの識別情報を保持します。

```sh
set -eu
ENGINE_URL="http://127.0.0.1:<port>"
CAPABILITIES=$(curl -fsS "$ENGINE_URL/recording/capabilities")
printf '%s\n' "$CAPABILITIES" | jq
INSTANCE_ID=$(printf '%s\n' "$CAPABILITIES" | jq -er 'select(.supported) | .instance_id')
```

`supported` が `true` の場合のみ先に進みます。それ以外は `unsupported_reason` と `minimum_platform_version` を確認します。`audio` フィールドは音声の対応状況を示します。Lua と異なり、**HTTP 録画は、バックエンドが対応していればデフォルトで音声を有効にします**。以下の例では、明示的に音声を無効にします。

### 録画の開始と確認 {#start-and-inspect-the-recording}

任意で `fps` や `audio` を含む JSON オブジェクトを指定して開始します。出力ファイルはサービスが選択します。パス、幅、高さ、スケールは受け付けません。

```sh
START=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data '{"fps":30,"audio":false}' \
    "$ENGINE_URL/recording/start")
OPERATION_ID=$(printf '%s\n' "$START" | jq -er '.operation_id')
printf '%s\n' "$START" | jq
```

HTTP 202 は、リクエストが受理されたことを示します。`pending` が `false`、`active` が `true` になるまで、次の状態取得コマンドを繰り返します。このチェックは、別の操作のレスポンスを拒否し、キャプチャやファイル準備の失敗を報告します。自動停止によりすでに録画が確定していた場合は、ダウンロードの前に[確定の手順](#stop-and-wait-for-finalization)へ進みます。

```sh
STATUS=$(curl -fsS \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL/recording/status")
printf '%s\n' "$STATUS" | jq -e --argjson id "$OPERATION_ID" '
    if .operation_id != $id then error("Recording operation changed")
    elif .state == "failed" then error(.failure)
    elif .file.state == "failed" then error("Recording file preparation failed")
    else . end'
```

録画したい時間だけゲームを実行し、停止を要求します。ウィンドウのリサイズですでに録画が完了している場合は、停止要求を省略し、以下の確定の手順に進みます。

### 停止と確定の待機 {#stop-and-wait-for-finalization}

開始時のレスポンスから保持した ID の操作を停止します。

```sh
STOP_BODY=$(jq -n --argjson id "$OPERATION_ID" '{operation_id: $id}')
STOP=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data "$STOP_BODY" \
    "$ENGINE_URL/recording/stop")
printf '%s\n' "$STOP" | jq
```

HTTP 202 は、停止要求の受理だけを意味します。`pending` が `false`、`finalized` が `true`、`file.state` が `complete` になるまで、状態取得コマンドを繰り返します。サービスは、ネイティブのキャプチャが終了してからファイルサイズと SHA-256 を準備するため、`state: "complete"` と `finalized: true` だけでは、ダウンロードの準備完了を意味しません。`state` または `file.state` が `failed` になったら待機を終了し、状態が `pending` や `failed` のファイルはダウンロードしないでください。

自動化クライアントでは、待機間隔とタイムアウトを設けてポーリングし、すべてのレスポンスで保持した操作 ID を確認します。キャプチャと確定を待つ間も、エンジンの更新を続けられるようにしてください。

### ファイルのダウンロードと解放 {#download-and-release-the-file}

状態レスポンスから、完了済みファイルの相対 URL を使います。以下のチェックでは、レスポンスが引き続き自分の操作のものであることも確認します。

```sh
FILE_URL=$(printf '%s\n' "$STATUS" | jq -er --argjson id "$OPERATION_ID" \
    'select(.operation_id == $id and .pending == false and .finalized == true and .file.state == "complete") | .file.url')
curl -fsS -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL" -o capture.mp4
printf '%s\n' "$STATUS" > capture.json
```

完了時の状態情報を `capture.json` として MP4 と一緒に保存します。`/recording/status` は現在の操作を表すため、以前の HTTP ファイルが利用可能なままでも、後の録画によって状態レスポンスは置き換わります。

ダウンロードしたファイルを使ったり、サービス側のコピーを削除したりする前に、バイト単位のサイズと SHA-256 を検証します。

```sh
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

receipt = json.loads(Path("capture.json").read_text(encoding="utf-8"))
capture = Path("capture.mp4")
if capture.stat().st_size != receipt["file"]["size"]:
    raise SystemExit("Recording download size mismatch")

digest = hashlib.sha256()
with capture.open("rb") as stream:
    for chunk in iter(lambda: stream.read(65536), b""):
        digest.update(chunk)
if digest.hexdigest() != receipt["file"]["sha256"]:
    raise SystemExit("Recording download SHA-256 mismatch")
print("Verified capture.mp4")
PY
```

`Range` ヘッダーなしの GET は、MP4 全体をダウンロードします。部分的なダウンロードが必要なクライアント向けに、`Range: bytes=0-1023` のような始点と終点を指定したバイト範囲にも対応します。結合したファイルを、同じ保存済みの状態情報に照らして検証します。

ダウンロードと検証が完了したら、サービスが保持するコピーを解放できます。

```sh
curl -fsS -X DELETE -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL"
```

HTTP 録画ファイルは、明示的に削除するか、エンジンが終了または再起動するまで利用できます。エンジンを閉じる前にダウンロードしてください。サービスが保持できるのは最大128ファイルです。次の録画の空きを作るため、保存済みの完了ファイルを削除します。

### 操作の識別情報をまとめて保持する {#keeping-operation-identities-together}

すべての POST と DELETE に `X-Recording-Instance` が必要です。例では、置き換わったエンジンからのレスポンスを拒否するため、状態取得とダウンロードにも送信します。`instance_id`、`operation_id`、ファイル情報をまとめて保持してください。再起動やリブートでサービスの識別情報は変わり、新しいプロセスが操作番号を再利用することがあります。

識別情報がない場合は HTTP 400 を返します。古い識別情報、古い停止操作、削除済みのファイルには HTTP 410 を返します。新しい識別情報を取得し、それを使って古い操作を再試行しないでください。新しいサービスを検出して、新しい録画を開始します。

### HTTP の失敗への対処 {#handling-http-failures}

拒否されたリクエストには、`error.code` と `error.message` を含む JSON を返します。原因を調べるには、個々の `curl` リクエストを `-i` 付き、`-f` なしで実行し、HTTP ステータスとエラーボディを確認します。

| HTTP ステータス | 確認事項 |
| --- | --- |
| 409 | 別の録画が実行中または保留中、現在の録画が停止可能な状態にない、またはファイルを準備中です。再試行の前に状態を確認します。 |
| 500 | 録画の起動、ストレージの初期化、ファイルの準備または読み取りに失敗しました。エラーメッセージを確認します。キャプチャ失敗は状態の `failure` にも報告されます。 |
| 501 | 動画または要求した音声に対応していません。利用可能な機能を確認し、音声のみが非対応なら `audio: false` を使います。 |
| 507 | サービスの保持ファイル数の上限に達しました。次の録画を始める前に、完了済みのファイルをダウンロードして削除します。 |
