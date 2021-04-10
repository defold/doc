---
title: The design of Defold
brief: The philosophy behind Defold's design
---

# The design of Defold

Defold was created with the following goals:

- To be a complete professional turn-key production platform for game teams.
- To be simple and clear, providing explicit solutions to common game development architectural and workflow problems.
- To be a blazing fast development platform ideal for iterative game development.
- To be high-performance in runtime.
- To be truly multi-platform.

The design of the editor and engine is carefully crafted to reach those goals. Some of our design decisions differ from what you may be used to if you have experience with other platforms, for example:

- We require static declaration of the resource tree and all naming. This requires some initial effort from you, but helps the development process tremendously in the long run.
- We encourage message passing between simple encapsulated entities.
- There is no object orientation inheritance.
- Our APIs are asynchronous.
- The rendering pipeline is code driven and fully customizable.
- All our resource files are in simple plain text formats, optimally structured for Git merges as well as import and processing with external tools.
- Resources can be changed and hot reloaded into a running game allowing for extremely fast iteration and experimentation.
