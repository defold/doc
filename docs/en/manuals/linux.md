---
title: Defold development for the Linux platform
brief: This manual describes how to build and run Defold applications on Linux
---

# Linux development

Developing Defold applications for the Linux platform is a straight forward process with very few considerations to make.

## Graphics backends

From Defold 1.14.2, Linux builds include Vulkan and an OpenGL fallback by default. The engine tries Vulkan first, then OpenGL on x86-64 or OpenGL ES on ARM64 if Vulkan is unavailable or graphics startup fails. In 1.14.1, the default is OpenGL on x86-64 and OpenGL ES on ARM64.

Use **Graphics (Linux)** in an [application manifest](/manuals/app-manifest/#graphics) to select **OpenGL & Vulkan**, **Vulkan**, or **OpenGL**. A single-backend engine cannot fall back to a backend it does not include. An explicit engine argument such as `--graphics-adapter=vulkan` also disables automatic fallback.

The Vulkan runtime is loaded dynamically in 1.14.2. A missing Vulkan loader does not by itself prevent the combined engine from starting with its OpenGL fallback. To run with Vulkan, the system still needs a working Vulkan loader and compatible driver. Check the engine log to see which backend was selected and why an initialization attempt failed.

These defaults describe the game engine. The editor's own graphics requirements are separate; see the FAQ below for editor troubleshooting.

## FAQ
:[Linux FAQ](../shared/linux-faq.md)
