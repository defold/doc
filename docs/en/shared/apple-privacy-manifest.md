
## Apple Privacy Manifest

The privacy manifest is a property list that records the types of data collected by your app or third-party SDK, and the required reasons APIs your app or third-party SDK uses. For each type of data your app or third-party SDK collects and category of required reasons API it uses, the app or third-party SDK needs to record the reasons in its bundled privacy manifest file.

Defold provides a default privacy manifest through the Privacy Manifest field in the game.project file. When creating an application bundle the privacy manifest will be merged with any privacy manifests in the project dependencies and included in the application bundle.

Read more about privacy manifests in the [official documentation from Apple](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files?language=objc).