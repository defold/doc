---
title: Automated testing and verification
brief: This manual explains how to design, run, and report deterministic Defold tests locally, in a running game, in browsers, and in continuous integration.
---

# Automated testing and verification

Automated testing verifies Defold code and content with explicit, machine-readable evidence. Use this manual to design tests that work with local scripts, CI (Continuous Integration) runners, and coding agents alike. It covers module tests, running collections, browser tests, runtime automation, visual checks, headless builds, and provides useful good practices.

## Verification levels

Good automated testing levels follow the testing pyramid framework, which divides tests into three main layers: unit tests, integration tests, and end-to-end (E2E) tests. In Defold you can separate tests into specific collections that can be loaded at boostrap. Usually, it's good to begin with the narrowest and fastest check that can detect the problem, then add runtime or platform tests where needed.

| Level | Suitable evidence |
| --- | --- |
| Static validation | Parser, formatter, resource validator, or generated-file comparison |
| Module test | Assertion results for reusable Lua logic with minimal engine dependencies |
| Running collection | Messages, components, input, physics, lifecycle, and engine behavior |
| Runtime automation | Live scene state, injected input, application state, and runtime screenshots |
| HTML5 browser test | Canvas input, browser integration, viewport behavior, and web output |
| Platform test | Behavior and rendering from the actual target platform |
| Build and bundle | Bob exit status, build report, archive, and bundle artifacts |

A successful compilation proves that the project builds, but it does not prove correct gameplay behavior. A screenshot does not prove complex transitions, animations, interactions, or gameplay flow, but it can be used by modern multimodal solutions to inspect what one frame looked like and if shaders and visual layout is correct. For automated tests though prefer deterministic assertions whenever the condition can be expressed directly.

## Reusable and testable Lua code

Keep reusable logic in Lua modules with minimal engine dependencies. Pure data transformations, rules, state machines, and calculations can then be exercised without constructing a complete game world.

Separate engine-facing code from the logic it invokes. A script can translate messages and component state into calls to a module, while tests call the module directly with controlled inputs.

See the [Writing Code manual](/manuals/writing-code) for more details.

## Tests in a running collection

Use a dedicated test collection when the behavior depends on game objects, components, messages, input, physics, or other engine systems.

Each test should:

1. establish a known state;
2. execute one behavior;
3. assert and assess the expected result;
4. clean up created resources;
5. emit a structured result description.

Prefer isolated test collections for tests. A project can select a test bootstrap collection through a temporary project setting in `game.project`:

```ini
[bootstrap]
main_collection = /test/test.collectionc
```

Do not leave a temporary test bootstrap in the project's normal configuration. In CI, prefer a dedicated settings file passed to Bob. CI can't change the state of the repository, it should only make temporary changes when needed.

For complex games, you can create small "development room" collections with predefined scenarios and simple blockouts. They make mechanics reproducible and make development easier for testing without navigating through unrelated game state and sections.

### Test frameworks

Projects can implement a small runner or use a [community testing library](https://defold.com/assets/?tag=testing).

For example, [DefTest](https://defold.com/assets/deftest/) is a unit-testing library based on Telescope. It supports suites, setup and teardown functions, assertions, name filtering, mocks for selected Defold APIs, and optional LuaCov coverage. Tests can run from a dedicated bootstrap collection, including in a headless bundle created with Bob.

## Structured test results

A framework's console/log summary can be useful to developers, but an unattended automatic controller still needs an explicit completion result. Add a small adapter around the framework callback or summary if necessary, for the controller to process the tests results easily.

A simple results description can use a unique prefix followed by one JSON object on each physical console line:

```text
TEST {"run":"8f13","event":"suite_start","tests":2}
TEST {"run":"8f13","event":"case","name":"player_moves","status":"pass","duration_ms":3}
TEST {"run":"8f13","event":"case","name":"player_stops","status":"pass","duration_ms":2}
TEST {"run":"8f13","event":"suite_end","status":"pass","passed":2,"failed":0}
```

A collector should process each line independently, find the `TEST` prefix, parse the JSON that follows, and ignore unrelated engine output.

Include a unique run identifier so output from an old or concurrent process cannot complete the current run. Every suite should emit one unambiguous final event (like `Pass`, `Failure`, `Crash`, `Timeout` etc).

### Collecting console output

When a game runs from the editor, it provides both current console history and a continuous stream. Close the stream after a matching suite completion event, process termination, an error, or a configured timeout and line limit.

Read more in the [editor HTTP API manual](/manuals/editor-http-api/#reading-console-output).

### Persisted logs

Defold can also persist the game log by enabling `Write Log File` in `game.project`. See [Game and system logs](/manuals/debugging-game-and-system-logs/). File logging is useful for packaged applications and for testing target devices where the editor console is unavailable.

The project can use built-in `print()` and `pprint()` functions, or e.g. any other [logging library](https://defold.com/assets/?tag=logging) from our Asset Portal.

## Testing a running game through a runtime API

A runtime automation API can inspect and control a live debug engine. It can be used when tests must find runtime objects, inject input, wait for visible state, or capture the rendered result.

Read the [engine service manual](/manuals/engine-service/#automation-bridge-extension) for more details.

The following example uses the [Automation Bridge](https://github.com/defold/extension-automation-bridge) Python helper structure. The project must include a compatible version of the debug extension, expose an element with the given automation id, and publish the `screen` application state:

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

External browser automation tools such as Playwright, Puppeteer, Selenium, WebdriverIO or Cypress can:

* wait for the Defold canvas and application readiness;
* send keyboard, mouse, and emulated touch input;
* resize the viewport;
* collect browser console output and JavaScript errors;
* take screenshots and compare artifacts.

Input directed at the canvas is processed through the project's normal input bindings and `on_input()` callbacks. Test both the game response and browser-specific integration points.

The most reliable approach is to expose an explicit JavaScript testing bridge in the custom `index.html`. On the Defold side, HTML5 builds can execute JavaScript using `html5.run()`, which makes communication with such a browser-side bridge possible. For commands travelling from JavaScript back into Defold, use a dedicated JavaScript-to-engine bridge.

Keep browser tests bounded. Distinguish a page-load failure, missing canvas, JavaScript error, test timeout, and failed game assertion in the final report.

## Editor previews and runtime screenshots for visual inspection {#editor-previews-and-runtime-screenshots}

One can create screenshot of the resource files in the default scene view in the open editor or in a game in runtime.

| Method | Purpose |
| --- | --- |
| [Editor preview](/manuals/editor-http-api/#rendering-scene-previews) | Loaded resource layout e.g. level or GUI, atlas composition, tilemap inspection, static scene composition, editor rendering and shaders correctness, or making documentation thumbnails |
| [Runtime screenshot](/manuals/engine-service) | The rendered state of a running build in a controlled scenario |

You can use image comparison e.g. for regression tests. Store the difference image and comparison metrics when a check fails.

A multimodal model can evaluate semantic conditions in visual inspection that are difficult to express otherwise, such as clipped text, overlapping controls, unclear selection states, or content outside a safe area. It is advised to treat that evaluation as an additional signal with explicit criteria, but not as a substitute for deterministic logic checks or image comparison.

## Headless tests and CI

Use Bob the builder CLI tool for editor-independent CI.

You can use it to resolve dependencies, build a game, an archive, or a standalone bundle, and generate a JSON report:

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

Run the resulting executable with a platform-appropriate process controller. Capture its exit status and logs, enforce a timeout, and require the structured suite completion event.

The [Bob manual](/manuals/bob) describes platforms, settings files, bundles, caches, native extensions, and build reports.

## Failure reports and artifacts

Good test results should retain enough evidence to reproduce and diagnose a failure:

* test name, run identifier, and assertion details;
* elapsed time and classified outcome;
* complete console or process log;
* Defold version, target platform, and relevant configuration;
* Bob build report and process exit status;
* runtime state or scene snapshot when available;
* screenshots, baseline differences, recordings, or browser traces;
* paths or links to all generated artifacts.

The same format should be usable by a developer, local script, CI service, or [AI coding agent](/manuals/ai-agents). This keeps verification deterministic even when diagnosis or repair is delegated.
