---
title: Automation in Defold
brief: This manual introduces Defold's automation interfaces and explains how to choose between editor, runtime, command-line, testing, and agent-driven workflows.
---

# Automation in Defold

This manual provides the overall mental model and links to the focused manuals for each interface.

Defold supports automation at several levels:

* [editor scripts](/manuals/editor-scripts) - allow you to customize editor workflows, add specific tools, and speed up the creation of levels, assets, etc.
* [editor UI scripts](/manuals/editor-scripts-ui/) - allow you to create custom visual tools, popups, configurators, etc.
* [editor HTTP API](/manuals/editor-http-api) - allows you to control an open project via OpenAPI operations.
* [Bob CLI](/manuals/bob) - can build a project and create data archives or standalone bundles from the command line.
* [engine HTTP service](/manuals/engine-service) - lets external tools query and send commands to a running debug build
* [Automation Bridge](https://github.com/defold/extension-automation-bridge) - official Defold extension provides additional runtime automation endpoints
* shell scripts can generate, validate, and perform ordinary file operations.
* external platform or web browser automation tools

The most important distinction is between the Defold editor and a running game. They are separate processes with separate HTTP servers:

| Layer | Process | Purpose |
| --- | --- | --- |
| Editor HTTP API | Defold editor | Project resources, builds, editor commands, previews, preferences, console output, and editor scripts |
| Engine service | Running Defold game engine (`dmengine`) | Development services, profiling, runtime messages, and extension-defined runtime automation APIs |

Use the [editor HTTP API](/manuals/editor-http-api) to control the open project. Use the [engine service](/manuals/engine-service) or a runtime automation extension when you must observe or control the running game.

## Choosing an automation interface

Choosing an interface appropriate to the task is one of the most important aspects of effective automation. The table below can help you choose the simplest interface for a given action:

| Interface | Suitable for |
| --- | --- |
| Shell script or task runner | Generation, formatting, validation, and repeatable local tasks |
| Bob | Editor-independent builds, bundles, reports, and CI |
| Editor script | Custom commands, resource tools, user interfaces, and editor integrations |
| Lifecycle hook | Validation or generation before and after editor builds or bundling |
| Editor HTTP API | External tools, IDE integrations, and test controllers for an open project |
| In-game test collection | Game logic, messages, components, input, physics, and engine behavior |
| Runtime automation API | Scene inspection, injected input, screenshots, and live application state |
| Browser automation | HTML5 interaction tests, screenshots, and web integrations |
| AI coding agent | Tasks where the relevant files and operations are not known in advance |
| Multimodal model | Semantic analysis of scenes, GUI layouts, and runtime screenshots |

For example:

* Need to automatically inspect visually a collection (e.g. level layout), a model (e.g. shaders correctness) or a GUI interface without running the game? Use an [editor preview](/manuals/editor-http-api/#rendering-scene-previews).
* Need to verify dynamically spawned game objects, physics, or runtime scripts? Use a [running test collection or runtime automation API](/manuals/automated-testing/#tests-in-a-running-collection).
* Need to build without a graphical editor e.g. during CI automated tests? Use [Bob](/manuals/bob).

## Deterministic automation or AI agents

Prefer a deterministic solution when the sequence of operations is already known, like e.g. in a level validator, formatter, build job, or regression test. These should normally have stable inputs, outputs, timeouts, and exit codes. It is good for automated hooks and tests, that can be reliably run on CI. A deterministic solution for procedural resource creation for your projects is also preferred, e.g. a tool to convert gltf objects to models with a given material, populate a level with e.g. trees, etc. These procedures can be easily created for every project with Editor Scripts and UI. Read more about them in [the manual](/manuals/editor-scripts-ui).

An agent can be useful when a task requires investigation or multimodal (e.g. including visual) analysis: locating relevant resources, selecting an implementation, modifying several files, interpreting errors, and iterating toward defined acceptance criteria. The agent should though still call deterministic interfaces and consume the same evidence as a local script or CI runner. See the manual on [using AI coding agents with Defold](/manuals/ai-agents).

## The automation loop

A reliable automation process forms a closed loop:

1. Inspect - read project files, the current interface description, and relevant documentation.
2. Change - use editor transactions, editor scripts, or file and shell tools.
3. Verify - build, run focused tests, and gather logs, reports, state, or images.
4. Evaluate - compare the evidence with acceptance criteria, then finish or retry.

![The inspect, change, verify, and evaluate automation loop](images/automation/automation_loop.png)

Verification should provide evidence from the actual environment. Suitable evidence includes:

* a successful build result;
* an explicitly completed test suite;
* expected state from the running game;
* a generated bundle or build report;
* a deterministic image comparison;
* a screenshot that satisfies defined visual criteria.

Define the expected result before making changes. Also define a timeout and a maximum number of repair attempts. An unattended process should not continue indefinitely when it cannot satisfy the acceptance criteria.

## Next steps

Find more details on specific topics regarding automation workflows in the given manuals:

* [Automating the Defold editor tasks with HTTP API](/manuals/editor-http-api)
* [The engine service and runtime HTTP API](/manuals/engine-service)
* [Automated testing and verification](/manuals/automated-testing)
* [Using AI coding agents with Defold](/manuals/ai-agents)
