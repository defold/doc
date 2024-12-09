---
title: Optimizing battery usage of a Defold game
brief: This manual describes how to optimize battery usage a Defold game.
---

# Optimize battery usage
Battery usage is mainly a concern if you are targeting mobile/handheld devices. High CPU or GPU usage will quickly drain battery and overheat the device.

Refer to the manuals on how to [optimize runtime performance](/manuals/optimization-speed) of a game to learn how to reduce CPU and GPU usage.

## Disable accelerometer
If you are creating a mobile game which doesn't make use of the device accelerometer it is recommended to [disable it in *game.project*](/manuals/project-settings/#use-accelerometer) to reduce the number of generated input events.
