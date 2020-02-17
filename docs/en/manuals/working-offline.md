---
title: Working offline
brief: This manual describes how to work offline in projects containing dependencies and in-particular native extensions
---

# Working offline

Defold does in most cases not require an internet connection to work. There is however a few situations when an internet connection is needed:

* Automatic updates
* Reporting issues
* Fetching dependencies
* Building native extensions


## Automatic updates

Defold will check periodically if new updates exist. Defold update checks are made to the [official download site](https://d.defold.com). If an update is detected it will automatically be downloaded.

If you only have an internet connection for limited periods of time and don't wish to wait for the automatic update to trigger you can manually download new versions of Defold from the [official download site](https://d.defold.com).


## Reporting issues

If a problem is detected in the editor you get a choice to report the issue to the Defold issue tracker. The issue tracker is [hosted on GitHub](https://www.github.com/defold/editor2-issues) which means you need an internet connection to report the issue.

If you encounter an issue while offline you can manually report it later using the [Report Issue option in the Help menu](/manuals/getting-help/#report-a-problem-from-the-editor) of the editor.


## Fetching dependencies

Defold supports a system where developers can share code and assets through something called [Library Projects](/manuals/libraries/). Libraries are zip files that can be hosted anywhere online. You typically find Defold library projects on GitHub and other online source code repositories.

A project can add a library as a [project dependency in the project settings](/manuals/project-settings/#dependencies). Dependencies are downloaded/updated when the project is opened or any time when the *Fetch Libraries* option is selected from the *Project* menu.

If you need to work offline and in multiple projects you can download dependencies in advance and then share them using a local server. Dependencies on GitHub are usually available from the Releases tab of the project repository:

![GitHub Library URL](images/libraries/libraries_library_url_github.png)

You can use Python to easily create a local server:

    python -m SimpleHTTPServer

This will create a server in the current directory serving files on `localhost:8000`. If the current directory contains downloaded dependencies you can add these to your *game.project* file:

    http://localhost:8000/extension-fbinstant-4.1.1.zip


## Building native extensions

Defold supports a system where developers can add native code to extend the functionality of the engine through a system called [Native Extensions](/manuals/extensions/). Defold provides a zero setup entry point to native extensions with a cloud based build solution.

The first time you build a project and the project contains a native extension the native code will get compiled into a custom Defold game engine on the Defold build servers and sent back to your PC. The custom engine will be cached in your project and reused for subsequent builds as long as you do not add, remove or change any native extensions and as long as you do not update the editor.

If you need to work offline and your project contains native extensions you must make sure to build successfully at least once to ensure that your project contains a cached copy of the custom engine.
