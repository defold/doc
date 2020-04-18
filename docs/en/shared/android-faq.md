Q: Is it possible to hide the navigation and status bars on Android?
: A: Yes, set the *immersive_mode* setting in the *Android* section of your *game.project* file. This lets your app take over the whole screen and capture all touch events on the screen.

Q: Why am I'm getting "Failure [INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES]" when installing a Defold game on device?
: A: Android detects that you try to install the app with a new certificate. When bundling debug builds, each build will be signed with a temporary certificate. Uninstall the old app before installing the new version:

  ```
  $ adb uninstall com.defold.examples
  Success
  $ adb install Defold\ examples.apk
  4826 KB/s (18774344 bytes in 3.798s)
          pkg: /data/local/tmp/Defold examples.apk
  Success
  ```
