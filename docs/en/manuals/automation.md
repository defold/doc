---
title: Automation in Defold
brief: This manual introduces Defold's automation interfaces and explains how to choose between editor, runtime, command-line, testing, and agent-driven workflows.
---

# Automation in Defold

This manual provides the overall description and links to the separate manuals for each topic.

Defold supports automation at several levels. Choosing an interface appropriate to the task is one of the most important aspects of effective automation. The table below can help you choose the simplest interface for a given action:

| Layer | Purpose |
| --- | --- |
| [Editor Scripts](/manuals/editor-scripts) | Custom commands and Editor workflows or integrations to speed up testing and development, e.g. creation of levels, assets |
| [Editor UI scripts](/manuals/editor-scripts-ui/) | Custom visual tools, popups, configurators, or user interfaces utilizing Editor Scripts |
| [Editor HTTP API](/manuals/editor-http-api) | Control the open game project in the Defold Editor via OpenAPI operations, project resources, builds, editor commands, previews, preferences, console output, or editor scripts for custom operations, external tools, IDE integrations, and test controllers |
| [Bob CLI](/manuals/bob) | Building a project, creating data archives or standalone bundles from the command line, reports, CI |
| [Lifecycle hooks](/manuals/editor-http-api#lifecycle-hooks) | Validation or generation before and after editor builds or bundling |
| [Engine HTTP service](/manuals/engine-service) | Running Defold game engine (`dmengine`) inspection, development services, profiling, runtime messages, or extension-defined runtime automation APIs, external tools querying, sending commands to a running debug build |
| [Automation Bridge](https://github.com/defold/extension-automation-bridge) | official Defold extension that provides additional engine runtime automation endpoints |
| [Automated tests](/manuals/automated-testing) | Testing game logic, messages, components, input, physics, and engine behavior, scene inspection, visual feedback e.g. via [editor preview](/manuals/editor-http-api/#rendering-scene-previews), injected input, live application state, [running test collections](/manuals/automated-testing/#tests-in-a-running-collection) |
| Shell scripts or task runners | Generation, formatting, validation, and repeatable tasks, ordinary file operations |
| External platform-specific and web browser automation tools | Desktop testing tools, HTML5 interaction tests, screenshots, web integrations |
| AI coding agents and multimodal models | Tasks where a deterministic approach is difficult or impossible to implement, semantic analysis of scenes, GUI layouts, or runtime screenshots |

The most important distinction is between the Defold editor and a running game. They are separate processes with separate HTTP servers.

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
