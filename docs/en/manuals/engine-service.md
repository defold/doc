---
title: The engine service and runtime HTTP APIs
brief: This manual explains the development HTTP service in a running Defold debug engine and how runtime extensions or external tools can use it.
---

# The engine service and runtime HTTP APIs

Running a project in Debug mode creates a process for a given runtime instance of the engine with your game and a special engine service that can be accessed for development and profiling infrastructure, runtime logic and messages, engine state and extensions.

The engine service is a development HTTP service owned by a running debug or headless engine (`dmengine` or `dmengine_headless`).

It is separate from the [editor server](/manuals/editor-http-api), which belongs to the Defold editor and controls the open project.

The two services use different ports. A tool that connects to the editor port cannot call runtime extension routes there, and vice versa - a tool that connects to the engine service cannot call editor operations.

The engine service is part of debug, development and profiling infrastructure. Release engine instances do not create the service.

## Availability and port discovery

When the editor starts a debug engine, it requests a dynamically assigned service port. The engine reports the selected port in the *Console* and in its log when run from a CLI:

![Engine service port information in Defold debug build](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

Since Defold 1.14.1, the engine also logs the full OpenAPI discovery URL using its actual address and assigned port:

```text
INFO:ENGINE: OpenAPI: http://<address>:<port>/openapi.json
```

These lines appear in the editor console when the game was launched from the editor. A simple local controller can parse them, but a reusable integration should let the editor or its wrapper track the engine instance and registered port. This avoids confusing an old port with a newly started or reused process.

The engine also advertises development targets through service discovery on supported platforms. That mechanism is primarily used by Defold tooling and should not be replaced with a permanently hard-coded port.

Server is accessible on localhost (`127.0.0.1`) at a given port:

![Engine server access](images/automation/engine-server.png)

## Discovering operations through OpenAPI

Since Defold 1.14.1, `GET /openapi.json` returns an OpenAPI 3.0.3 document describing the runtime HTTP API. Use the engine service port from the log. For a local engine, replace `<port>` below with that port:

```sh
ENGINE_URL="http://127.0.0.1:<port>"
curl -fsS "$ENGINE_URL/openapi.json" | jq
```

The document describes paths, methods, parameters, request bodies, and responses supplied by currently registered handlers, including native extensions that provide OpenAPI metadata. Its `paths` object changes when handlers are added or removed. Profiler and extension routes depend on the running engine's platform, configuration, and registered extensions, so fetch the document from the instance you are using.

Handlers registered without OpenAPI metadata remain callable but do not appear in the document. A documented route can also report an unavailable capability; inspect its response descriptions and any capability endpoint before using platform-dependent operations.

The editor has its own [OpenAPI document](/manuals/editor-http-api/#discovering-operations-through-openapi) on the editor port. Use the engine's document for runtime operations.

## Built-in endpoints

The current debug engine registers a small set of core routes.

| Endpoint | Purpose |
| --- | --- |
| `GET /openapi.json` | Discover the currently registered runtime HTTP operations that provide OpenAPI metadata |
| `GET /ping` | Check that the engine service responds |
| `GET /info` | Read engine version, platform, build identifier, and log-service information |
| `GET /state` | Read development connection state used by Defold tooling |
| `POST /post/<socket>/<message-type>` | Post a Protobuf-encoded Defold message to a named engine socket |

For example:

```sh
curl -sS "$ENGINE_URL/ping"
curl -sS "$ENGINE_URL/info" | jq
curl -sS "$ENGINE_URL/state" | jq
```

The `/post` route is used by development operations such as hot reload, reboot, resize, and process control. Its body is a binary Protobuf message of the type named in the route; it is not a JSON message API. The Protobuf message can be no larger than 1024 bytes serialized, otherwise a `400 Too large message` will be returned.

These routes are development infrastructure, and additional profiler and resource-inspection routes exist in the engine implementation.

## Recording endpoints

Since Defold 1.14.1, desktop debug engines also expose native MP4 recording through the following routes. They are omitted from release, headless, mobile and web builds, and when **Exclude Record** is enabled in the [App Manifest](/manuals/app-manifest/#exclude-record).

| Endpoint | Purpose |
| --- | --- |
| `GET /recording/capabilities` | Discover video/audio support, backend requirements and the recording service's `instance_id` |
| `GET /recording/status` | Read the current operation, asynchronous progress and finalized file information |
| `POST /recording/start` | Request recording and receive its `operation_id` |
| `POST /recording/stop` | Request stopping and finalization for the specified operation |
| `GET /recording/files/{id}` | Download a finalized MP4 |
| `DELETE /recording/files/{id}` | Delete a completed file retained by the service |

Discover these routes through `/openapi.json`, then check `/recording/capabilities` for the current platform's support. Recording mutations require the `X-Recording-Instance` header, and stopping also requires the accepted `operation_id`. Start and stop are asynchronous; wait for finalization before downloading the file. See the [recording manual](/manuals/recording/#recording-through-http) for the complete workflow.

The HTTP service shares the recorder with Lua. HTTP starts enable application audio by default when supported; Lua starts default to video only. Only recordings started through HTTP have a downloadable `file` receipt. Before downloading, wait for `pending: false`, `finalized: true` and `file.state: "complete"`, then [verify the file's size and SHA-256](/manuals/recording/#download-and-release-the-file). See [sharing the recorder](/manuals/recording/#sharing-the-recorder-with-http-clients) when combining Lua and HTTP clients.

## Metal GPU trace endpoint

Since Defold 1.14.1, macOS debug engines expose `/profiler/gputrace` for capturing Metal GPU traces. The route appears in `/openapi.json` only on macOS. Capture requires the native Metal adapter and `METAL_CAPTURE_ENABLED=1` in the engine's launch environment. A request returns HTTP 501 with `error.code: "gputrace_unsupported"` if capture is unavailable.

| Endpoint | Purpose |
| --- | --- |
| `POST /profiler/gputrace` | Schedule capture to a writable absolute `.gputrace` path; `frames` defaults to `1` and may be `1`–`10000`. |
| `GET /profiler/gputrace` | Read the current or most recent capture's state, path and frame counts. |
| `DELETE /profiler/gputrace` | Cancel a pending capture or finish an active capture after the current rendered frame; retain the trace on disk. |

Accepted requests return HTTP 200 with `ok: true` and a `data` object. Capture progresses asynchronously: poll `GET` until `data.state` is `complete`, `canceled` or `failed`. Native startup failures are reported in `data.error`. The trace is written on the engine host. See the [Metal GPU trace capture guide](/manuals/profiling/#metal-gpu-trace-capture) for launch commands, support discovery, capture examples and opening the result in Xcode.

## Extension-defined runtime routes

In debug builds, the native extension SDK can provide access to the engine web server. An extension can register a route prefix on that server and expose operations that depend on runtime data.

This is useful for development tools because an extension can share the existing engine service instead of opening another HTTP server.

An extension-defined runtime automation API should:

* use a distinct, versioned route prefix;
* expose supported capabilities;
* return structured errors;
* handle unavailable platform or engine features explicitly;
* keep operations local to development and testing;
* document whether it is omitted from release builds.

### Publishing extension operations in OpenAPI

In a native extension's application initialization callback, obtain the server with `dmEngine::GetWebServer(app_params)` and register handlers only when the returned handle is non-null. See the [extension lifecycle](/manuals/extensions/#extension-lifecycle) for the callback setup.

Since Defold 1.14.1, the four-argument `dmWebServer::AddHandler()` overload accepts an OpenAPI 3.0.3 Paths Object as a JSON string. The object has route paths as its top-level keys. Each path must start with the registered prefix and must not already be documented by another handler. Use inline schemas, or references to paths in the resulting document.

For example, this helper registers a callback and its status endpoint description:

```cpp
#include <dmsdk/dlib/webserver.h>

static const char STATUS_OPENAPI[] = R"json(
{
  "/example/v1/status": {
    "get": {
      "summary": "Get extension status",
      "responses": {
        "200": {
          "description": "Current extension status",
          "content": {
            "text/plain": {
              "schema": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
)json";

dmWebServer::Result RegisterStatusHandler(dmWebServer::HServer server,
                                        dmWebServer::Handler callback,
                                        void* context)
{
    dmWebServer::HandlerParams params;
    params.m_Handler = callback;
    params.m_Userdata = context;
    return dmWebServer::AddHandler(
        server, "/example/v1", &params, STATUS_OPENAPI);
}
```

Pass a callback that implements `GET /example/v1/status` and returns the documented `text/plain` response. The callback remains responsible for checking request paths and methods and producing responses. Check the registration result: invalid or conflicting metadata returns `dmWebServer::RESULT_ERROR_INVAL`.

The server retains the JSON pointer without copying the string. Keep its storage unchanged and valid until the handler is removed with `dmWebServer::RemoveHandler()` or the server is destroyed. The `static const char` array in the example satisfies this requirement. Removing the handler also removes its paths from subsequent `/openapi.json` responses.

The three-argument `dmWebServer::AddHandler(server, prefix, &params)` overload remains supported. It is equivalent to passing `0` as the fourth argument: the handler is registered without OpenAPI metadata and is omitted from discovery.

## Automation Bridge extension

The official Defold [Automation Bridge](https://github.com/defold/extension-automation-bridge) is a debug-only native extension built on the engine service. It registers a versioned runtime automation API under:

```text
http://127.0.0.1:<engine-service-port>/automation-bridge/v1
```

Its runtime API provides capabilities such as scene and node inspection, input, screen information, screenshots, recording, lifecycle information, and optional application-defined synchronization. Some operations include:

| Operation | Action |
| --- | --- |
| `GET  /automation-bridge/v1/health` | health report, API capabilities and compatibility |
| `POST /automation-bridge/v1/input/click` | for runtime input interactions |
| `GET  /automation-bridge/v1/screenshot` | for runtime screenshots |

Use the extension's [native API documentation](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge) and [Python helper documentation](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python) for the version installed in the project.

Automation Bridge exposes neither its HTTP API nor its Lua module in release builds.

### Editor and runtime clients

The Automation Bridge Python helpers illustrate the two-client architecture. Function `editor.open_project()` returns an editor project client, and `project.build_and_run()` returns a separate engine client.

| Client | Purpose |
| --- | --- |
| Project | Editor HTTP API, commands, debugger, console, preferences, reference, previews, build, and port discovery |
| Game - engine service | Scene, input, screenshots, runtime state, and synchronization |

The division between `project` and `game` makes the process boundary explicit. Editor operations remain on the editor server, while observations and actions against the live game remain on the engine service.

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()
```

## Limitations and security

The engine service and extension-defined routes are development tools, and should be treated as such.

::: important
Use the running engine's `/openapi.json` document for discovery in Defold 1.14.1 and later. Earlier engines do not provide this endpoint. For handlers registered without OpenAPI metadata, consult the extension's versioned API documentation.
:::

Runtime scripts, physics, input, dynamically created objects, and platform rendering require a running engine and should be verified through [automated runtime testing](/manuals/automated-testing).

* Do not publish the service through a router, public interface, or untrusted tunnel.
* Do not assume that engine service routes require authentication.
* Runtime routes can vary by extension version, platform, graphics backend, and engine capabilities.
* Use version or capability negotiation for extension-defined up-to-date APIs.
