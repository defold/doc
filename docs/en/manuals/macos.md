---
title: Defold development for the macOS platform
brief: This manual describes how to build and run Defold applications on macOS
---

# macOS development

Developing Defold applications for the macOS platform is a straight forward process with very few considerations to make.

## Project settings

macOS specific application configuration is done from the [OSX section](/manuals/project-settings/#osx) of the *game.project* settings file.

## Application icon

The application icon used for a macOS game must be in the .icns format. You can easily create a .icns file from a set of .png files collected as an iconset. Follow the [official instructions for creating a .icns file](https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Optimizing/Optimizing.html). Brief summary of the steps involved are:

* Create an iconset folder, eg `foobar.iconset`
* Copy icon files to the created folder:

    * `icon_16x16.png`
    * `icon_16x16@2x.png`
    * `icon_32x32.png`
    * `icon_32x32@2x.png`
    * `icon_128x128.png`
    * `icon_128x128@2x.png`
    * `icon_256x256.png`
    * `icon_256x256@2x.png`
    * `icon_512x512.png`
    * `icon_512x512@2x.png`

* Convert the .iconset folder to a .icns file using the `iconutil` command line tool:

```
iconutil -c icns -o foobar.icns foobar.iconset
```

## Publishing to the Mac App Store

The process when publishing to the Mac App Store is well documented in the [Apple Developer documentation](https://developer.apple.com/macos/submit/). Before submitting the application you need to perform a few additional steps:

* Make sure that anyone is able to run your game by adding the execute permissions (the default is that only the file owner has execute permissions):

```
$ chmod +x Game.app/Contents/MacOS/Game
```

* Sign your game using `codesign`:

```
$ codesign --force --sign "Developer ID Application: Company Name" --options runtime --deep --timestamp Game.app
```

* Follow the Mac App Store submission steps from here.

Note: The game does not have to be notarized when publishing to the Mac App Store.

## Publishing outside the Mac App Store

Apple requires all software distributed outside the Mac App Store to be notarized by Apple in order to run by default on macOS Catalina. Refer to the [official documentation](https://developer.apple.com/documentation/xcode/notarizing_macos_software_before_distribution/customizing_the_notarization_workflow) to learn how to add notarization to a scripted build environment outside of XCode. Brief summary of the steps involved are:

* Make sure that anyone is able to run your game by adding the execute permissions (the default is that only the file owner has execute permissions):

```
$ chmod +x Game.app/Contents/MacOS/Game
```

* Sign your game using `codesign`:

```
$ codesign --force --sign "Developer ID Application: Company Name" --options runtime --deep --timestamp Game.app
```

* Zip and upload your game for notarization using `altool`.

```
$ xcrun altool --notarize-app
               --primary-bundle-id "com.acme.foobar"
               --username "AC_USERNAME"
               --password "@keychain:AC_PASSWORD"
               --asc-provider <ProviderShortname>
               --file Game.zip

altool[16765:378423] No errors uploading 'Game.zip'.
RequestUUID = 2EFE2717-52EF-43A5-96DC-0797E4CA1041
```

* Check the status of your submission using the returned request UUID from the call to `altool --notarize-app`:

```
$ xcrun altool --notarization-info 2EFE2717-52EF-43A5-96DC-0797E4CA1041
               -u "AC_USERNAME"
```

* Wait until the status becomes `success` and staple the notarization ticket to the game:

```
$ xcrun stapler staple "Game.app"
```
