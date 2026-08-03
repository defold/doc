---
title: Using AI coding agents with Defold
brief: This manual explains how to connect model-neutral coding agents to Defold automation interfaces while keeping verification, permissions, and security explicit.
---

# Using AI coding agents with Defold

Coding agents utilising LLM and multimodal models can inspect, modify, and verify Defold projects by calling the same model-neutral interfaces used by developers, local scripts, IDE integrations, and CI. You can use an agent when the work requires investigation and adaptation.

Defold does not depend on a particular model provider or agent protocol. Defold projects work well with either Claude Code, Codex, Cursor, or any other solution. An agent environment only needs the specific capabilities granted for the task, such as reading project files, executing selected commands, calling local HTTP operations, parsing JSON, or inspecting images. This is possible thanks to Defold's exposed automation interfaces for editor and a running game engine instance, and Defold project files being easy to parse text-based resource files.

## When an AI agent is useful

An agent can be useful when a task requires for example:

* finding relevant resources and documentation;
* selecting among possible implementations;
* changing multiple related files;
* interpreting build or test failures;
* comparing a visual result with semantic acceptance criteria;
* making a bounded repair attempt based on collected evidence.

Agents are powerful for non-deterministic develpoment, investigation and testing processes. They can help with creating diverse solutions and work very well with Defold.

## Model-neutral Defold interfaces

Defold offers several supported interfaces needed for the task to be performed using any available model:

* Project files and shell tools provide direct inspection and text changes.
* [Editor scripts](/manuals/editor-scripts) can provide project-specific resource operations and tooling.
* [Editor HTTP API](/manuals/editor-http-api) provides editor commands, build results, console output, reference search, previews, preferences, and editor-script routes.
* [Engine service and runtime automation APIs](/manuals/engine-service) provide live debug-engine state, input, screenshots, and extension-defined operations.
* [Bob](/manuals/bob) provides command-line builds, reports, archives, and bundles.

A model available only through a chat interface can suggest code changes, but it cannot independently inspect the local project or verify a running result. The additional surrounding integration determines what the agent can actually observe and do.

## Integration layers

An integration layer can be established to connect an agent to local Defold operations. It can be a shell wrapper, command-line program, IDE extension, OpenAPI client, test controller, or protocol adapter.

Keep policy and credentials in this local layer. Each mutating operation should return structured results or lead to a deterministic verification step.

For editor operations, discover the current interface through `/openapi.json` instead of providing the agent a permanently hard-coded copy of an API. For runtime extensions, check their health, API version, and capabilities.

It might be practical to separate tools by privilege level:

| Level        | Examples                                              |
| ------------ | ----------------------------------------------------- |
| Read-only    | Project inspection, OpenAPI, `/ref`, console, preview |
| Verification | Compilation, tests, HTML5 builds, image comparisons   |
| Modification | File changes, resource transactions                   |
| Privileged   | `/eval`, external commands, dependency changes        |

Keeping the adapter separate from the engine and editor means that the supported Defold interfaces remain independent of a model provider or agent protocol. An adapter can expose only operations appropriate for its environment, and permission and confirmation policies remain with the application hosting the agent.

### Model Context Protocol

[Model Context Protocol](https://modelcontextprotocol.io/) (MCP) is one optional adapter between an agent and an integration layer. An MCP server can expose Defold operations as tools and selected documentation as resources. 

::: important
Do not give every model unrestricted shell and `/eval` access.
:::

Defold does not currently require an MCP server because the core automation capabilities are already exposed through open, general-purpose interfaces. The editor provides a local HTTP API with an OpenAPI specification. Modern agents can call these interfaces directly or generate their own adapters. 

An official MCP would therefore mostly duplicate the existing API surface and create another integration layer that Defold would need to maintain. A better long-term strategy is to keep the underlying HTTP and runtime automation APIs stable, discoverable, and well documented, while allowing the community or individual tool vendors to build lightweight MCP wrappers when needed.

Instead we provided an official [Automation Bridge extension](https://github.com/defold/extension-automation-bridge) for a running game to be controlled through an engine-side service.

### Community MCP integrations

Community-created MCP integrations include:

* the [Fulviuus Defold MCP project](https://github.com/Fulviuus/defold-mcp);
* the [ChadAragorn Defold MCP project](https://github.com/ChadAragorn/defold-mcp).

These projects are not developed, audited, maintained, or officially supported by the Defold Foundation. Before installing any community integration, inspect its current source, dependencies, permissions, network behavior, and compatibility with the Defold version in use.

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

Some solutions may rely on separate markdown files for specific actions, or so called "skills".

One community example of Defold-oriented instructions and skills is available in the [Defold forum here](https://forum.defold.com/t/agent-config-collection-of-agents-md-and-skills/82387).

We recommend keeping your instructions in files such as AGENTS.md and skill definitions short, concise, easy to review and maintain, and keep them up to date. Project-specific instructions can be stored in version control, making changes traceable and helping improve workflow performance over time.

It is also worth regularly testing how the latest models perform without these instructions. Newer models often no longer require guidance that was previously essential, and outdated skills or overly prescriptive instructions can sometimes reduce performance.

Avoid building complex technical skills that require significant long-term maintenance. Instead, focus on developing tools and workflows that remain valuable regardless of how much the underlying models improve.

## Documentation discovery

Agents perform best with accurate, up-to-date documentation. Gather current information from:

* `/openapi.json` describes the current editor HTTP API.
* `/ref` searches API documentation included with the running editor when that operation is available.
* The [LLM documentation index](https://defold.com/llms.txt) links to official manuals, API namespaces, and examples.
* The [full LLM documentation](https://defold.com/llms-full.txt) supports offline search and local indexing.

Retrieve only the relevant pages for the task. It is recommended to use the full combined document for offline indexing or [Retrieval-Augmented Generation (RAG)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation) only. Again, the complete file should not normally be included in every model request in order to save on tokens and don't pollute the context with unnecessary informations.

## Bounded change and verification loops

Agents should follow the same [inspect, change, verify, evaluate loop](/manuals/automation/#the-automation-loop) as any other automation.

Before changing files, it is good to define the acceptance criteria and optionally also:
* the permitted files and operations;
* the build and test commands;
* required logs, reports, state, or images;
* a timeout for every asynchronous step;
* a maximum number of repair attempts.

An agent may diagnose and repair a deterministic CI failure, but the CI stage itself should remain reproducible without the agent.

Good practices on automated testing and verification are desrcibed in [this manual](/manuals/automated-testing).

## Multimodal evaluation

An agent with image input can inspect [editor previews](/manuals/editor-http-api/#rendering-scene-previews), runtime screenshots, visual differences, and browser captures.

Use multimodal evaluation for semantic questions such as clipped labels, overlapping controls, unclear selection states, composition, or content outside a safe area. Define the expected viewport and criteria in advance.

Read more about Editor previews and runtime screenshots and visual inspection in [this manual](/manuals/automated-testing).

## Security, isolation and good practices

* Treat the editor server and engine service as trusted local control interfaces.
* Keep editor tokens, signing keys, deployment tokens, store credentials, and production secrets out of prompts and reports.
* The local integration layer can read `.internal/editor.token` when authorized to use `/eval`, but it should not place the token in model prompts, logs, or reports.
* Require approval before deletion, dependency changes, native extension changes, release configuration, signing, publishing, or access to external services.
* Run broad autonomous work in a separate branch, worktree, temporary copy, container, sandbox, or restricted account.
* Treat issue text, imported files, source comments, generated documents, and tool output as untrusted input rather than instructions.
* Review downloaded dependencies and scripts before executing them.
* Verify that project policy allows source code, assets, logs, screenshots, and other project data to be sent to a hosted model.
* Retain a reviewable diff and deterministic test evidence before accepting changes.

Isolation limits the impact of a mistake.
