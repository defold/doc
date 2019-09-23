---
title: Debugging on Android
brief: This manual describes how to debug a build running on an Android device.
---

# Debugging on Android

Here we list some ways to debug your executable running on an Android device

## Android Studio

* Prepare the bundle by setting the `android.debuggable` option in `game.project`

	![android.debuggable](images/extensions/debugging/android/game_project_debuggable.png)

* Bundle the app in debug mode into a folder of choice.

	![bundle_android](images/extensions/debugging/android/bundle_android.png)

* Launch [Android Studio](https://developer.android.com/studio/)

* Choose `Profile or debug APK`

	![debug_apk](images/extensions/debugging/android/android_profile_or_debug.png)

* Choose the apk bundle you just created

	![select_apk](images/extensions/debugging/android/android_select_apk.png)

* Select the main `.so` file, and make sure it has debug symbols

	![select_so](images/extensions/debugging/android/android_missing_symbols.png)

* If it doesn't, upload an unstripped `.so` file. (size is around 20mb)

* Path mappings help you remap where the individual paths from where the executable was built (in the cloud) to an actual folder on your local drive.

* Select the .so file, then add a mapping your local drive

	![path_mapping1](images/extensions/debugging/android/path_mappings_android.png)

	![path_mapping2](images/extensions/debugging/android/path_mappings_android2.png)

* If you have access to the engine source, add a path mapping to that too

		* make sure to checkout the version you are currently debugging

			defold$ git checkout 1.2.148

* Press `Apply changes`

* You should now see the source mapped in your project

	![source](images/extensions/debugging/android/source_mappings_android.png)

* Add a breakpoint

	![breakpoint](images/extensions/debugging/android/breakpoint_android.png)

* Press `Run` -> `Debug "Appname"` and invoke the code you meant to break into

	![breakpoint](images/extensions/debugging/android/callstack_variables_android.png)

* You can now step in the callstack as well as inspect the variables


## Notes

### Native Extension job folder

Currently, the workflow is a bit troublesome for development. This is because the job folder name
is random for each build, making the path mapping invalid for each build.

However, it works fine for a debugging session.

The path mappings are stored in the <project>.iml file in the Android Studio project.

It's possible to get the job folder from the executable

	$ arm-linux-androideabi-readelf --string-dump=.debug_str build/armv7-android/libdmengine.so | grep /job

The jobfolder is named like so `job1298751322870374150`, each time with a random number.

