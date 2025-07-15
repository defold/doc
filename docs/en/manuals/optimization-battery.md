---
title: Optimizing battery usage of a Defold game
brief: This manual describes how to optimize battery usage a Defold game.
---

# Optimize battery usage
Battery usage is mainly a concern if you are targeting mobile/handheld devices. High CPU or GPU usage will quickly drain battery and overheat the device.

Refer to the manuals on how to [optimize runtime performance](/manuals/optimization-speed) of a game to learn how to reduce CPU and GPU usage.

## Disable accelerometer
If you are creating a mobile game which doesn't make use of the device accelerometer it is recommended to [disable it in *game.project*](/manuals/project-settings/#use-accelerometer) to reduce the number of generated input events.

# Platform specific optimizations

## Android Device Performance Framework

Android Dynamic Performance Framework is a set of APIs that allow games and to interact more directly with power and thermal systems of Android devices. It is possible to monitor the dynamic behavior on Android systems and optimize game performance at a sustainable level that doesn’t overheat devices. Use the [Android Dynamic Performance Framework extension](https://defold.com/extension-adpf/) to monitor and optimize performance in your Defold game for Android devices.