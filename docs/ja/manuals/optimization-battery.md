---
title: Defold ゲームのバッテリー消費量の最適化
brief: このマニュアルでは、Defold ゲームのバッテリー消費量を最適化する方法を説明します。
---

# バッテリー消費量の最適化 {#optimize-battery-usage}
バッテリー消費量は、主にモバイルデバイスや携帯型デバイスを対象とする場合に考慮すべき点です。CPU や GPU の使用率が高いと、バッテリーが急速に消耗し、デバイスが過熱します。

CPU と GPU の使用率を減らす方法については、ゲームの[実行時のパフォーマンスを最適化する](/manuals/optimization-speed)方法を説明したマニュアルを参照してください。

## 加速度センサーの無効化 {#disable-accelerometer}
デバイスの加速度センサーを使用しないモバイルゲームを作成する場合は、生成される入力イベントの数を減らすために、[*game.project* で加速度センサーを無効にする](/manuals/project-settings/#use-accelerometer)ことをお勧めします。

# プラットフォーム固有の最適化 {#platform-specific-optimizations}

## Android Device Performance Framework

Android Dynamic Performance Framework は、ゲームが Android デバイスの電力管理システムや温度管理システムと、より直接的にやり取りできるようにする API 群です。Android システムの動的な挙動を監視し、デバイスが過熱しない、持続可能な水準でゲームのパフォーマンスを最適化できます。[Android Dynamic Performance Framework 拡張機能](https://defold.com/extension-adpf/)を使用して、Android デバイス向けの Defold ゲームのパフォーマンスを監視し、最適化します。
