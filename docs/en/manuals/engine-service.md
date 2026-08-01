---
title: The engine service and runtime HTTP APIs
brief: This manual explains the development HTTP service in a running Defold debug engine and how runtime extensions such as Automation Bridge use it.
---

# The engine service and runtime HTTP APIs

The engine service is a development HTTP service owned by a running debug engine (`dmengine`). Use it for engine development services, profiling, runtime messages, or extension-defined runtime automation. It is separate from the [editor server](/manuals/editor-http-api), which belongs to the Defold editor and controls the open project.

## Editor server and engine service

Building and running a project creates two processes with different responsibilities:

| Service | Owner | Typical responsibility |
| --- | --- | --- |
| Editor server | Defold editor | Project resources, editor commands, builds, console history, reference search, previews, preferences, and editor scripts |
| Engine service | Running debug engine | Development and profiling infrastructure, runtime messages, engine state, and extension-defined routes |

The two services use different ports. A tool that connects to the editor port cannot call runtime extension routes there, and a tool that connects to the engine service cannot call editor operations such as `/preview` or `/prefs`.

## Availability and port discovery

The engine service is part of development and profiling infrastructure. Debug engine instances create the service; release builds do not provide it.

When the editor starts a debug engine, it requests a dynamically assigned service port. The engine reports the selected port in its log:

```text
INFO:ENGINE: Engine service started on port <port>
```

The line appears in the editor console when the game was launched from the editor. A simple local controller can parse this line, but a reusable integration should let the editor or its wrapper track the engine instance and registered port. This avoids confusing an old port with a newly started or reused process.

The engine also advertises development targets through service discovery on supported platforms. That mechanism is primarily used by Defold tooling and should not be replaced with a permanently hard-coded port.

Use `127.0.0.1` when controlling a local desktop engine:

```sh
ENGINE_PORT=51337
ENGINE_URL="http://127.0.0.1:$ENGINE_PORT"
```

The number above is only an example. Always use the port selected by the running engine.

## Built-in endpoints

The current debug engine registers a small set of core routes. Their conceptual purposes are:

| Endpoint | Purpose |
| --- | --- |
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

The `/post` route is used by development operations such as hot reload, reboot, resize, and process control. Its body is a binary Protobuf message of the type named in the route; it is not a JSON message API.

These routes are development infrastructure, and additional profiler and resource-inspection routes exist in the engine implementation. Do not treat every observed route or response field as a permanent public guarantee. The engine service does not currently publish an OpenAPI document. Integrations should limit themselves to documented behavior or to an extension's versioned API.

## Extension-defined runtime routes

In debug builds, the native extension SDK can provide access to the engine web server. An extension can register a route prefix on that server and expose operations that depend on runtime data.

This is useful for development tools because an extension can share the existing engine service instead of opening another HTTP server. The route design, response format, versioning, and capabilities belong to the extension, not to the core engine.

An extension-defined runtime automation API should:

* use a distinct, versioned route prefix;
* expose a health operation and supported capabilities;
* return structured errors;
* handle unavailable platform or engine features explicitly;
* keep operations local to development and testing;
* document whether it is omitted from release builds.

## Automation Bridge extension

The official Defold [Automation Bridge](https://github.com/defold/extension-automation-bridge) extension is a debug-only native extension built on the engine service. It is not part of the core engine. It registers a versioned runtime automation API under:

```text
http://127.0.0.1:<engine-service-port>/automation-bridge/v1
```

Its runtime API provides capabilities such as scene and node inspection, input, screen information, screenshots, recording, lifecycle information, and optional application-defined synchronization. Representative operations include:

```text
GET  /automation-bridge/v1/health
GET  /automation-bridge/v1/scene
POST /automation-bridge/v1/input/click
GET  /automation-bridge/v1/screenshot
```

This is not a complete endpoint reference. Use the extension's [native API documentation](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge) and [Python helper documentation](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python) for the version installed in the project.

Automation Bridge exposes neither its HTTP API nor its Lua module in release builds. Its health response reports API compatibility and supported capabilities. Clients should check that response instead of assuming that every route, graphics feature, input backend, or screenshot implementation is available.

### Editor and runtime clients

The Automation Bridge Python helpers illustrate the two-client architecture. `editor.open_project()` returns an editor project client, and `project.build_and_run()` returns a separate engine client:

```text
Python test or automation script
    |
    +-- project --> editor HTTP API
    |               commands, debugger, console, preferences,
    |               reference, previews, build, and port discovery
    |
    +-- game --> engine service
                 |
                 +-- /automation-bridge/v1
                     scene, input, screenshots,
                     runtime state, and synchronization
```

The transition from `project` to `game` makes the process boundary explicit:

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()
```

This division is useful even when using another language or client library: editor operations remain on the editor server, while observations and actions against the live game remain on the engine service.

## Choosing the correct interface

| Task | Interface |
| --- | --- |
| Compile and run the project from an open editor | Editor HTTP API |
| Modify editor resources | Editor HTTP API or editor script |
| Render an editor preview | Editor HTTP API |
| Read editor build errors | Editor HTTP API |
| Inspect the running scene | Runtime automation API |
| Inject input into the game | Runtime automation API |
| Capture a runtime screenshot or state | Runtime automation API |
| Read live engine development state | Engine service or runtime automation API |
| Build in headless CI | Bob |

An editor preview can answer questions about a loaded resource without starting the game. Runtime scripts, physics, input, dynamically created objects, and platform rendering require a running engine and should be verified through [automated runtime testing](/manuals/automated-testing).

## Limitations and security

The engine service and extension-defined routes are development tools, not application networking or a game backend.

* Connect locally through `127.0.0.1`; do not publish the service through a router, public interface, or untrusted tunnel.
* Do not assume that engine service routes require authentication.
* Release builds may omit the engine service and debug extensions entirely.
* Runtime routes can vary by extension version, platform, graphics backend, and engine capabilities.
* Use version or capability negotiation for extension-defined APIs.
* Do not claim OpenAPI support unless a particular extension explicitly provides it.
* Use normal, secured application networking for shipped game features.

If tests need runtime inspection, input, screenshots, or application synchronization, install a purpose-built debug extension and follow its security and compatibility documentation.
