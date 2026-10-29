---
title: Video recording in Defold
brief: This manual explains how to record the game window to MP4 using Lua or the engine HTTP service.
---

# Video recording

Defold can record the game window to an H.264 video in an MP4 file through the [`recorder` Lua module](/ref/recorder/) or the [engine HTTP service](/manuals/engine-service/#recording-endpoints). Both interfaces share one recorder, so only one recording can start, run or finalize at a time.

## Availability

Recording is included in desktop **debug** engines. It is omitted from release, headless, mobile and web builds. Enabling **Exclude Record** in an [App Manifest](/manuals/app-manifest/#exclude-record) also removes the Lua module and HTTP routes.

| Platform | Video requirements | Application audio |
| --- | --- | --- |
| macOS | macOS 15 or later, using ScreenCaptureKit | Supported |
| Windows | Windows 10 version 1903 or later, using Windows Graphics Capture and Media Foundation | Supported on Windows build 20348 or later |
| Linux | OpenGL, OpenGL ES or Vulkan, using framebuffer capture | Not supported |

Video and audio support are checked separately. HTTP clients can inspect `/recording/capabilities`; Lua callers receive an error if the requested capture is unsupported. Operating-system permissions and capture-device failures can also cause an asynchronous error after a start request is accepted.

The recorder captures the game window's content at its native size in physical pixels. It may crop one row or column to produce even video dimensions. Resizing the window or changing its pixel density stops and finalizes the recording. Capture rate is 1–60 frames per second, with a default of 30.

## Recording from Lua

Use [`recorder.start()`](/ref/recorder/#recorder.start) with a writable output path and a callback. The parent directory must exist; [`sys.get_save_file()`](/ref/sys/#sys.get_save_file) supplies a suitable application save path. An existing output file may be overwritten. Lua recordings belong to the caller and remain on disk after the engine exits.

Paths use the Windows ANSI code page on Windows and UTF-8 elsewhere, as with Lua file I/O. The callback's `result.path` preserves the path passed to `recorder.start()`.

This `.script` example records for five seconds after capture starts:

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

`recorder.start()` and [`recorder.stop()`](/ref/recorder/#recorder.stop) return `true` when accepted, or `nil, error` when rejected. Acceptance does not mean capture or file finalization has finished. Invalid options raise Lua errors.

Callbacks run during engine updates:

| Event | Meaning |
| --- | --- |
| `recorder.EVENT_STARTED` | Capture is active; it can now be stopped. |
| `recorder.EVENT_STOPPED` | The MP4 has been finalized and is ready to read. This also occurs after an automatic stop on resize. |
| `recorder.EVENT_ERROR` | Capture failed; inspect `result.error`. Startup failure can produce this event without `EVENT_STARTED`. |

The result also contains `path`, `width`, `height`, `fps` and `audio`. Read or upload the output only after `EVENT_STOPPED`. Keep the initiating script alive to receive the callback: deleting it discards callbacks without stopping capture. Engine shutdown finalizes capture without invoking Lua callbacks.

Audio is **disabled by default in Lua**. Set `audio = true` to request application audio on a supported platform. Requesting unsupported audio returns an error.

### Sharing the recorder with HTTP clients

`recorder.stop()` targets the current shared recording, including one started through HTTP. It returns an error while an operation is pending or when no recording is active. If an HTTP client stops a Lua recording, the original Lua callback still receives its completion event. Starting through HTTP does not create a Lua callback; use HTTP status to observe its completion.

HTTP status can describe a Lua recording, but its `file` field is `null`: the service only prepares downloads for recordings started through HTTP. Read a Lua recording from `result.path` after `EVENT_STOPPED`.

## Recording through HTTP

The recording routes use the engine service port printed in the game log. Discover them through `/openapi.json` as described in the [engine service manual](/manuals/engine-service/#discovering-operations-through-openapi). A headless or release engine will not expose them.

The following commands use a POSIX shell, `curl` and `jq`; the download verification step also uses Python 3. Run them in the same shell and replace `<port>` with the running engine's port. First query capabilities and retain the service identity:

```sh
set -eu
ENGINE_URL="http://127.0.0.1:<port>"
CAPABILITIES=$(curl -fsS "$ENGINE_URL/recording/capabilities")
printf '%s\n' "$CAPABILITIES" | jq
INSTANCE_ID=$(printf '%s\n' "$CAPABILITIES" | jq -er 'select(.supported) | .instance_id')
```

Proceed only if `supported` is `true`; otherwise inspect `unsupported_reason` and `minimum_platform_version`. The `audio` field reports audio support. Unlike Lua, **HTTP recording enables audio by default when the backend supports it**. The example below explicitly disables audio.

### Start and inspect the recording

Start with an optional JSON object containing `fps` and/or `audio`. The service chooses the output file; it does not accept a path, width, height or scale.

```sh
START=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data '{"fps":30,"audio":false}' \
    "$ENGINE_URL/recording/start")
OPERATION_ID=$(printf '%s\n' "$START" | jq -er '.operation_id')
printf '%s\n' "$START" | jq
```

HTTP 202 means the request was accepted. Re-run the following status command until `pending` is `false` and `active` is `true`. The check rejects a response for another operation and reports capture or file-preparation failures. If an automatic stop has already finalized the recording, continue with [finalization](#stop-and-wait-for-finalization) before downloading.

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

Let the game run for the duration you want to capture, then request a stop. If the window resized and the recording already completed, skip the stop request and continue with finalization below.

### Stop and wait for finalization

Stop the operation whose ID you retained from the start response:

```sh
STOP_BODY=$(jq -n --argjson id "$OPERATION_ID" '{operation_id: $id}')
STOP=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data "$STOP_BODY" \
    "$ENGINE_URL/recording/stop")
printf '%s\n' "$STOP" | jq
```

HTTP 202 only accepts the stop request. Repeat the status command until `pending` is `false`, `finalized` is `true`, and `file.state` is `complete`. The service prepares the file's size and SHA-256 after native capture finishes, so `state: "complete"` and `finalized: true` alone do not mean the download is ready. Stop waiting if `state` or `file.state` becomes `failed`; do not download a file whose state is `pending` or `failed`.

An automated client should poll with a delay and a timeout, checking the retained operation ID on every response. Allow the engine to keep updating while waiting for capture and finalization.

### Download and release the file

Use the completed file's relative URL from the status response. The check below also ensures that the response still belongs to your operation:

```sh
FILE_URL=$(printf '%s\n' "$STATUS" | jq -er --argjson id "$OPERATION_ID" \
    'select(.operation_id == $id and .pending == false and .finalized == true and .file.state == "complete") | .file.url')
curl -fsS -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL" -o capture.mp4
printf '%s\n' "$STATUS" > capture.json
```

Keep the completed status receipt in `capture.json` with the MP4. `/recording/status` describes the current operation, so a later recording replaces the status response even while earlier HTTP files remain available.

Verify the downloaded file's byte size and SHA-256 before using it or deleting the service's copy:

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

A GET without a `Range` header downloads the whole MP4. The service also supports closed byte ranges, such as `Range: bytes=0-1023`, if a client needs partial downloads. Verify the assembled file against the same receipt.

After downloading and verifying the file, you can release the service's retained copy:

```sh
curl -fsS -X DELETE -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL"
```

HTTP recording files remain available until explicitly deleted or the engine shuts down or reboots. Download them before closing the engine. The service retains at most 128 files; delete completed files you have saved to make room for further recordings.

### Keeping operation identities together

Every POST and DELETE requires `X-Recording-Instance`. The examples also send it on status and download requests to reject responses from a replacement engine. Keep `instance_id`, `operation_id` and the file information together: the service identity changes on restart or reboot, and a new process can reuse operation numbers.

A missing identity returns HTTP 400. A stale identity, stale stop operation or deleted file returns HTTP 410. Do not fetch a new identity and reuse it to retry an old operation. Discover the new service and start a new recording instead.

### Handling HTTP failures

Rejected requests return JSON with `error.code` and `error.message`. For troubleshooting, run the individual `curl` request with `-i` and without `-f` to see the HTTP status and error body.

| HTTP status | What to check |
| --- | --- |
| 409 | Another recording is active or pending, the current recording is not ready to stop, or the file is still being prepared. Read status before retrying. |
| 500 | Recording startup, storage initialization or file preparation/read failed. Inspect the error message; a failed capture also reports `failure` in status. |
| 501 | Video or the requested audio is unsupported. Inspect capabilities; use `audio: false` if only audio is unavailable. |
| 507 | The service's retained-file limit was reached. Download and delete completed files before starting another recording. |

## Migrating from older recording APIs

The native MP4 recorder replaces the VP8/IVF recorder. The `start_record` and `stop_record` system messages have been removed. Use `recorder.start()` and `recorder.stop()` or the HTTP routes above, and wait for their asynchronous completion before consuming the MP4.
