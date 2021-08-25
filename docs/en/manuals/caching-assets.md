---
title: Caching assets
brief: This manual explains how to use the asset cache to speed up builds.
---

# Caching assets

Games created with Defold usually build in a matter of seconds, but as a project grows so does the amount of assets. Compiling fonts and compressing textures can take a significant amount of time in a large project and the asset cache exists to speed up builds by only rebuilding assets that have changed while using already compiled assets from the cache for assets that hasn't changed.

Defold uses a three-tiered cache:

1. Project cache
2. Local cache
3. Remote cache


## Project cache

Defold will by default cache compiled assets in the `build/default` folder of a Defold project. The project cache will speed up subsequent builds as it is only modified assets that have to be recompiled, while assets with no changes will be used from the project cache. This cache is always enabled and it used by both the editor and the command line tools.

The project cache can be deleted manually by deleting the files in `build/default` or by issuing the `clean` command from the [command line build tool Bob](/manuals/bob).


## Local cache

Added in Defold 1.2.187

The local cache is an optional second cache where compiled assets are stored in an external file location on the same machine or on a network drive. Thanks to its external location the contents of the cache survives a cleanup of the project cache. It can also be shared by multiple developers working on the same project. The cache is currently only available when building using the command line tools. It is enabled through the `resource-cache-local` option:

```sh
java -jar bob.jar --resource-cache-local /Users/john.doe/defold_local_cache
```

Compiled assets are accessed from the local cache based on a computed checksum which takes into account the Defold engine version, the names and the contents of the source assets as well as project build options. This will guarantee that cached assets are unique and that the cache can be shared between multiple versions of Defold.

::: sidenote
Files stored in the local cache are stored indefinitely. It is up to the developer to manually remove old/unused files.
:::


## Remote cache

Added in Defold 1.2.187

The remote cache is an optional third cache where compiled assets are stored on a server and accessed through HTTP request. The cache is currently only available when building using the command line tools. It is enabled through the `resource-cache-remote` option:

```sh
java -jar bob.jar --resource-cache-remote https://http://192.168.0.100/
```

As with the local cache all assets are accessed from the remote cache based on a computed checksum. Cached assets are accessed through the HTTP request methods GET, PUT and HEAD. Defold does not provide the remote cache server. It is up to each developer to set this up. An example of [a basic Python server can be seen here](https://github.com/britzl/httpserver-python).
