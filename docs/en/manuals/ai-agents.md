---
title: Using AI coding agents with Defold
brief: This manual explains how to connect model-neutral coding agents to Defold automation interfaces while keeping verification, permissions, and security explicit.
---

# Using AI coding agents with Defold

AI coding agents can inspect, modify, and verify Defold projects by calling the same model-neutral interfaces used by developers, local scripts, IDE integrations, and CI. Use an agent when the work requires investigation and adaptation; keep known build, test, validation, and deployment stages deterministic.

Defold does not depend on a particular model provider or agent protocol. An agent environment only needs the specific capabilities granted for the task, such as reading project files, executing selected commands, calling local HTTP operations, parsing JSON, and inspecting images.

## When an agent is appropriate

Prefer an ordinary script or test when the sequence of operations is known. Stable generators, formatters, validators, builds, and regression tests should have predictable inputs, outputs, timeouts, and exit codes.

An agent can be useful when a task requires these activities:

* finding relevant resources and documentation;
* selecting among possible implementations;
* changing related files whose locations were not known in advance;
* interpreting build or test failures;
* comparing a visual result with semantic acceptance criteria;
* making a bounded repair attempt based on collected evidence.

The agent should not invent its own definition of success. Define acceptance criteria and the available verification steps before it begins changing the project.

## Model-neutral Defold interfaces

You can build an integration from the smallest set of supported interfaces needed for the task using any available model:

* Project files and shell tools provide direct inspection and controlled text changes.
* [Editor scripts](/manuals/editor-scripts) provide project-specific resource operations and tools.
* The [editor HTTP API](/manuals/editor-http-api) provides editor commands, build results, console output, reference search, previews, preferences, and editor-script routes.
* The [engine service and runtime automation APIs](/manuals/engine-service) provide live debug-engine state, input, screenshots, and extension-defined operations.
* [Bob](/manuals/bob) provides command-line builds, reports, archives, and bundles.
* [Automated tests](/manuals/automated-testing) provide deterministic completion events and failure evidence.

A model available only through a chat interface can suggest code, but it cannot independently inspect the local project or verify a running result. The surrounding integration determines what the agent can actually observe and do.

## Integration layers

An integration layer connects an agent to local Defold operations. It can be a shell wrapper, command-line program, IDE extension, OpenAPI client, test controller, or protocol adapter.

Keep policy and credentials in this local layer. Expose small, well-named operations rather than unrestricted access when possible. Each mutating operation should return structured results or lead to a deterministic verification step.

For editor operations, discover the current interface through `/openapi.json`; do not give the agent a permanently hard-coded copy of an experimental API. For runtime extensions, check their health, API version, and capabilities.

### Model Context Protocol

[Model Context Protocol](https://modelcontextprotocol.io/) (MCP) is one optional adapter between an agent and an integration layer. An MCP server can expose Defold operations as tools and selected documentation as resources.

MCP is not required by Defold. Keeping the adapter separate from the engine and editor means that:

* the supported Defold interfaces remain independent of a model provider or agent protocol;
* non-AI clients can use OpenAPI and command-line tools directly;
* an adapter can expose only operations appropriate for its environment;
* permission and confirmation policies remain with the application hosting the agent;
* the adapter can translate stable agent tools into version-specific editor or extension requests.

Do not assume that installing an MCP server makes its operations official or safe. Review the adapter as executable third-party code.

## Privilege separation

Separate capabilities by risk and grant only the levels needed for the current task:

| Level | Examples |
| --- | --- |
| Read-only | Project inspection, OpenAPI, `/ref`, console, and editor previews |
| Verification | Builds, tests, HTML5 output, runtime observations, and image comparisons |
| Modification | File changes, resource transactions, and generated content |
| Privileged | `/eval`, arbitrary external commands, dependencies, signing, and publishing |

::: important
Do not give every model unrestricted shell and `/eval` access. The editor token and broad command execution can provide control over the local development environment.
:::

The local integration layer can read `.internal/editor.token` when authorized to use `/eval`, but it should not place the token in model prompts, logs, or reports.

## Project instructions

Available Large Language Models used for agentic workflows generally perform better with good instructions. Therefore, agents markdown files describing their desired behaviour, or skills are often being added to projects. It is good to design and write your own instructions for each project separately for best results, but some common knowledge and rules could be re-used.

A first file that many agents search for and read is a canonical file such as `AGENTS.md` that can describe:

* project structure and important entry points;
* formatting and naming conventions;
* commands for builds, tests, and validation;
* required completion events and artifact locations;
* files or directories that must not be changed;
* operations that require approval;
* platform assumptions and known limitations.

Keep the instructions up-to-date, specific, and short enough to review. You can store concise project-specific instructions in version control and manage their changes to increase performance of the workflows.

Where an agent platform supports reusable skills or workflows, make them call the same canonical project scripts rather than duplicating build and test logic in provider-specific configuration.

One community example of Defold-oriented instructions and skills is available in the [Defold forum here](https://forum.defold.com/t/agent-config-collection-of-agents-md-and-skills/82387).

## Documentation discovery

In order for agents to perform well, a good and actual documentation is needed. One can gather actual informations from:

* `/openapi.json` describes the current editor HTTP API.
* `/ref` searches API documentation included with the running editor when that operation is available.
* The [LLM documentation index](https://defold.com/llms.txt) links to official manuals, API namespaces, and examples.
* The [full LLM documentation](https://defold.com/llms-full.txt) supports offline search and local indexing.

Retrieve only the relevant pages for the task. Use the full combined document for offline indexing or or [Retrieval-Augmented Generation (RAG)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation). Again, the complete file should not normally be included in every model request in order to save tokens.

## Bounded change and verification loops

Agents should follow the same [inspect, change, verify, evaluate loop](/manuals/automation/#the-automation-loop) as any other automation.

Before changing files, define:

* the acceptance criteria;
* the permitted files and operations;
* the build and test commands;
* required logs, reports, state, or images;
* a timeout for every asynchronous step;
* a maximum number of repair attempts.

Compile or build after each coherent group of changes, then run the narrowest relevant test. A failed build should produce structured issues. A runtime suite should produce an explicit completion event. A timeout or crashed process must be classified separately from an assertion failure.

An agent may diagnose and repair a deterministic CI failure, but the CI stage itself should remain reproducible without the agent.

## Multimodal evaluation

An agent with image input can inspect [editor previews](/manuals/editor-http-api/#rendering-scene-previews), runtime screenshots, visual differences, and browser captures.

Use multimodal evaluation for semantic questions such as clipped labels, overlapping controls, unclear selection states, composition, or content outside a safe area. Define the expected viewport and criteria in advance.

Do not use a screenshot as the only proof for logic that can be asserted deterministically. An editor preview also cannot verify runtime scripts, physics, dynamic objects, or platform-specific rendering. See [Editor previews and runtime screenshots](/manuals/automated-testing/#editor-previews-and-runtime-screenshots).

## MCP integrations

[Model Context Protocol](https://modelcontextprotocol.io/) is one possible communication protocol between an AI agent and an integration layer. An MCP server can expose Defold operations as tools and project documentation as resources.

As of now, Defold does not provide an official MCP server. Official integration is based on the editor OpenAPI document, Bob, editor scripts, and project-defined tools.

Keeping MCP separate from the editor core provides several advantages:

* the editor remains independent of a specific model provider or agent protocol;
* the same interface supports automation unrelated to artificial intelligence;
* clients can use OpenAPI directly;
* an MCP adapter can expose only the operations appropriate for its environment;
* permission and confirmation policies remain under the control of the application hosting the agent.

It might be practical to separate tools by privilege level:

| Level        | Examples                                              |
| ------------ | ----------------------------------------------------- |
| Read-only    | Project inspection, OpenAPI, `/ref`, console, preview |
| Verification | Compilation, tests, HTML5 builds, image comparisons   |
| Modification | File changes, resource transactions                   |
| Privileged   | `/eval`, external commands, dependency changes        |


::: important
Do not give every model unrestricted shell and `/eval` access.
:::

### Community MCP integrations

Community-created MCP integrations include:

* the [Fulviuus Defold MCP project](https://github.com/Fulviuus/defold-mcp);
* the [ChadAragorn Defold MCP project](https://github.com/ChadAragorn/defold-mcp).

These projects are not developed, audited, maintained, or officially supported by the Defold Foundation. Before installing any community integration, inspect its current source, dependencies, permissions, network behavior, tests, and compatibility with the Defold version in use.

## Security and isolation

Agent-driven automation is part of the project's security model:

* Connect to editor and runtime development services through `127.0.0.1`; never expose them publicly.
* Treat the editor server and engine service as trusted local control interfaces.
* Keep editor tokens, signing keys, deployment tokens, store credentials, and production secrets out of prompts and reports.
* Require approval before deletion, dependency changes, native extension changes, release configuration, signing, publishing, or access to external services.
* Run broad autonomous work in a separate branch, worktree, temporary copy, container, sandbox, or restricted account.
* Treat issue text, imported files, source comments, generated documents, and tool output as untrusted input rather than instructions.
* Review downloaded dependencies and scripts before executing them.
* Verify that project policy allows source code, assets, logs, screenshots, and other project data to be sent to a hosted model.
* Retain a reviewable diff and deterministic test evidence before accepting changes.

Isolation limits the impact of a mistake; it does not expand the operations that an agent is authorized to perform.
