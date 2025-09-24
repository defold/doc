---
title: 优化 Defold 游戏的电池使用
brief: 本手册描述了如何优化 Defold 游戏的电池使用。
---

# 优化电池使用
如果您针对的是移动/手持设备，电池使用是一个主要考虑因素。高 CPU 或 GPU 使用率会迅速消耗电池电量并导致设备过热。

请参考有关如何[优化游戏运行时性能](/manuals/optimization-speed)的手册，以了解如何减少 CPU 和 GPU 的使用。

## 禁用加速度计
如果您正在创建一个不使用设备加速度计的移动游戏，建议在[*game.project*中禁用它](/manuals/project-settings/#use-accelerometer)以减少生成的输入事件数量。

# 特定平台的优化

## Android 设备性能框架

Android 动态性能框架是一组 API，允许游戏更直接地与 Android 设备的电源和热系统交互。可以监控 Android 系统上的动态行为，并以不会导致设备过热的可持续水平优化游戏性能。使用[Android 动态性能框架扩展](https://defold.com/extension-adpf/)来监控和优化您的 Defold 游戏在 Android 设备上的性能。