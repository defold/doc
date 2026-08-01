---
title: Automated testing and verification
brief: This manual explains how to design, run, and report deterministic Defold tests locally, in a running game, in browsers, and in continuous integration.
---

# Automated testing and verification

Automated testing verifies Defold code and content with explicit, machine-readable evidence. Use this manual to design tests that work with local scripts, CI runners, and coding agents alike. It covers module tests, running collections, browser tests, runtime automation, visual checks, headless builds, and provides useful good practices.

## Verification levels

Begin with the narrowest and fastest check that can detect the problem, then add runtime or platform tests where needed:

| Level | Suitable evidence |
| --- | --- |
| Static validation | Parser, formatter, resource validator, or generated-file comparison |
| Module test | Assertion results for reusable Lua logic with minimal engine dependencies |
| Running collection | Messages, components, input, physics, lifecycle, and engine behavior |
| Runtime automation | Live scene state, injected input, application state, and runtime screenshots |
| HTML5 browser test | Canvas input, browser integration, viewport behavior, and web output |
| Platform test | Behavior and rendering from the actual target platform |
| Build and bundle | Bob exit status, build report, archive, and bundle artifacts |

A successful compilation proves that the project builds; it does not prove gameplay behavior. A screenshot proves what one frame looked like; it does not prove a hidden state transition, calculation, or message exchange. Prefer deterministic assertions whenever the condition can be expressed directly.

## Reusable and testable Lua

Keep reusable logic in Lua modules with minimal engine dependencies. Pure data transformations, rules, state machines, and calculations can then be exercised without constructing a complete game world.

Separate engine-facing code from the logic it invokes. A script can translate messages and component state into calls to a module, while tests call the module directly with controlled inputs. See the [Writing Code manual](/manuals/writing-code).

## Tests in a running collection

Use a dedicated test collection when the behavior depends on game objects, components, messages, input, physics, or other engine systems.

Each test should:

1. establish a known state;
2. execute one behavior;
3. assert the expected result;
4. clean up created resources;
5. emit a structured result.

Prefer isolated test collections over starting the entire game. A project can select a test bootstrap collection through a settings file or a temporary project setting:

```ini
[bootstrap]
main_collection = /test/test.collectionc
```

Do not leave a temporary test bootstrap in the project's normal configuration. In CI, prefer a dedicated settings file passed to Bob.

For complex games, create small "development room" collections with predefined scenarios and simple blockouts. They make mechanics reproducible without navigating through unrelated game state.

### Test frameworks

Projects can implement a small runner or use a [community testing library](https://defold.com/assets/?tag=testing).

For example, [DefTest](https://defold.com/assets/deftest/) is a unit-testing library based on Telescope. It supports suites, setup and teardown functions, assertions, name filtering, mocks for selected Defold APIs, and optional LuaCov coverage. Tests can run from a dedicated bootstrap collection, including in a headless bundle created with Bob.

A framework's normal console summary can be useful to developers, but an unattended controller still needs an explicit completion result. Add a small adapter around the framework callback or summary if necessary.

## Structured test results

Human-readable logs help with diagnosis, while automation needs a stable result protocol. One simple protocol uses a unique prefix followed by one JSON object on each physical console line:

```text
TEST {"run":"8f13","event":"suite_start","tests":2}
TEST {"run":"8f13","event":"case","name":"player_moves","status":"pass","duration_ms":3}
TEST {"run":"8f13","event":"case","name":"player_stops","status":"pass","duration_ms":2}
TEST {"run":"8f13","event":"suite_end","status":"pass","passed":2,"failed":0}
```

Do not pretty-print one event across several log lines. A collector should process each line independently, find the `TEST` prefix, parse the JSON that follows, and ignore unrelated engine output.

Include a unique run identifier so output from an old or concurrent process cannot complete the current run. Every suite must emit one unambiguous final event.

Report these outcomes separately:

| Outcome | Meaning |
| --- | --- |
| Pass | A matching final event reports success |
| Assertion failure | The suite completed and reported failed assertions |
| Crash | The engine process terminated unexpectedly |
| Timeout | The expected final event did not arrive before the deadline |
| Disconnected | The output channel closed while the process state remained uncertain |

A crash, timeout, or disconnected stream is not an ordinary assertion failure and must never be inferred as a pass.

## Collecting console output

When a game runs from the editor, the [editor HTTP API](/manuals/editor-http-api/#reading-console-output) provides both current console history and a continuous stream:

```sh
PORT="$(cat .internal/editor.port)"
BASE_URL="http://127.0.0.1:$PORT"

curl -sS "$BASE_URL/console" | jq
curl -N "$BASE_URL/console/stream"
```

Close the stream after a matching suite completion event, process termination, an error, or a configured timeout and line limit.

Defold can also persist the game log by enabling `Write Log File` in `game.project`. See [Game and system logs](/manuals/debugging-game-and-system-logs/). File logging is useful for packaged applications and target devices where the editor console is unavailable.

The project can use `print()` and `pprint()` or a [community logging library](https://defold.com/assets/?tag=logging). Keep diagnostic logging separate from the structured result prefix.

## Testing a running game through a runtime API

A runtime automation API can inspect and control a live debug engine. Use it when tests must find runtime objects, inject input, wait for visible state, or capture the rendered result. The [engine service manual](/manuals/engine-service/#automation-bridge-extension) explains how these routes differ from editor operations.

The following example uses the current Automation Bridge Python helper structure. The project must include a compatible version of the debug extension, expose an element with the given automation id, and publish the `screen` application state:

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()

try:
    play = game.element(automation_id="play_button")
    game.click(play)
    game.wait_for_state("screen", "gameplay", timeout=5.0)
    screenshot = game.screenshot()
    print(screenshot.path)
finally:
    game.close_engine()
```

Application-defined states and automation ids use Automation Bridge's optional debug-only Lua API, which the project must enable and publish. A fixed sleep is vulnerable to machine speed and frame timing; bounded polling for a defined state is more reliable.

Automation Bridge is an extension, not part of the core engine. Consult its [Python API reference](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python) for installed-version selectors, waits, state, events, screenshots, and diagnostics.

## Browser tests for HTML5

The editor can create and serve an HTML5 build through its current `build-html5` command, as described in the [editor HTTP API manual](/manuals/editor-http-api/#building-html5). Bob can also create an HTML5 bundle without the editor.

External browser automation can:

* wait for the Defold canvas and application readiness;
* send keyboard, mouse, and emulated touch input;
* resize the viewport;
* collect browser console output and JavaScript errors;
* take screenshots and compare artifacts.

Input directed at the canvas is processed through the project's normal input bindings and `on_input()` callbacks. Test both the game response and browser-specific integration points.

Keep browser tests bounded. Distinguish a page-load failure, missing canvas, JavaScript error, test timeout, and failed game assertion in the final report.

## Editor previews and runtime screenshots

The two image sources answer different questions:

| Image | Use it for | It does not prove |
| --- | --- | --- |
| [Editor preview](/manuals/editor-http-api/#rendering-scene-previews) | Loaded resource layout, static scene composition, editor rendering, and thumbnails | Runtime scripts, physics, input, dynamic objects, or target-platform rendering |
| Runtime screenshot | The rendered state of a running build after a controlled scenario | Hidden logic, complete interaction history, or state not visible in the frame |

Need to inspect a `.collection` without starting the game? Use an editor preview. Need to verify dynamically spawned objects or post-processing after gameplay input? Use a runtime screenshot after deterministic setup and assertions.

### Visual regression

For stable rendering, compare the produced image with an approved baseline. Fix the viewport, display settings, test content, frame or synchronization point, platform, and tolerance. Store the difference image and comparison metrics when a check fails.

A multimodal model can evaluate semantic conditions that are difficult to express as pixels, such as clipped text, overlapping controls, unclear selection states, or content outside a safe area. Treat that evaluation as an additional signal with explicit criteria, not as a substitute for deterministic logic checks or image comparison.

## Headless tests and CI

Use [Bob](/manuals/bob) for editor-independent CI.

A basic job can resolve dependencies, build an archive, and generate a JSON report:

```sh
mkdir -p build/reports

java -jar bob.jar \
  --root . \
  --archive \
  --build-report-json build/reports/build-report.json \
  resolve build
```

Build a headless test bundle with dedicated settings:

```sh
java -jar bob.jar \
  --root . \
  --settings test/test.settings \
  --platform x86_64-linux \
  --variant headless \
  --archive \
  --bundle-output build/test-bundle \
  resolve build bundle
```

Run the resulting executable with a platform-appropriate process controller. Capture its exit status and logs, enforce a timeout, and require the structured suite completion event. Headless builds do not provide graphical evidence, so run a separate graphical or platform test when rendering matters.

The Bob manual describes platforms, settings files, bundles, caches, native extensions, and build reports.

## Failure reports and artifacts

Retain enough evidence to reproduce and diagnose a failure:

* test name, run identifier, and assertion details;
* elapsed time and classified outcome;
* complete console or process log;
* Defold version, target platform, and relevant configuration;
* Bob build report and process exit status;
* runtime state or scene snapshot when available;
* screenshots, baseline differences, recordings, or browser traces;
* paths or links to all generated artifacts.

The same evidence format should be usable by a developer, local script, CI service, or [AI coding agent](/manuals/ai-agents). This keeps verification deterministic even when diagnosis or repair is delegated.
