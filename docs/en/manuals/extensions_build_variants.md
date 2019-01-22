# Native Extensions - Build Variants

## Build Variants

When you bundle a game, you need to choose what type of engine you wish to use.

  * Debug
  * Release
  * Headless

These different versions are also referred to as `Build variants`

Note: When you choose `Build and run` you'll get the debug version.

### Debug

This type of executable still has the debugging feature left inside it, such as:
profiling, logging and hot reload.

This variant is chosen during development of the game.

### Release

This variant has the debugging features disabled.
This options is chosen when the game is ready to be released to the app store.

### Headless

This executable runs without any graphics. It means that you can run the game unit/smoke tests on a CI server,
or even have it as a game server in the cloud.

## App Manifest

Not only can you add native code to the engine with the Native Extensions feature, you can also remove standard parts of the engine.
E.g. if you don't need a physics engine, you can remove that from the executable.

We support this via a file called an `App Manifest` (.appmanifest).
In such a file, you can configure what libraries or symbols to remove, or perhaps add compile flags

This feature is still in the works, and needs more attention.

### Editing

Currently, the process can be done manually, but we recommend our users to use the [Manifestation](https://britzl.github.io/manifestation/) tool
to create their app manifest.

Eventually, the creation and modification of the app manifests will be done in the Editor.

### Syntax

...

