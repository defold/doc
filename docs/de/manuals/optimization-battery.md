---
title: Den Akkuverbrauch eines Defold-Spiels optimieren
brief: Dieses Handbuch beschreibt, wie du den Akkuverbrauch eines Defold-Spiels optimierst.
---

# Den Akkuverbrauch optimieren {#optimize-battery-usage}
Der Akkuverbrauch ist vor allem dann relevant, wenn du Mobilgeräte oder Handhelds als Zielplattform verwendest. Eine hohe CPU- oder GPU-Auslastung entlädt den Akku schnell und lässt das Gerät überhitzen.

In den Handbüchern dazu, wie du die [Leistung eines Spiels zur Laufzeit optimierst](/manuals/optimization-speed), erfährst du, wie du die CPU- und GPU-Auslastung reduzierst.

## Den Beschleunigungssensor deaktivieren {#disable-accelerometer}
Wenn du ein mobiles Spiel entwickelst, das den Beschleunigungssensor des Geräts nicht verwendet, solltest du [ihn in *game.project* deaktivieren](/manuals/project-settings/#use-accelerometer), um die Anzahl der erzeugten Eingabeereignisse zu reduzieren.

# Plattformspezifische Optimierungen {#platform-specific-optimizations}

## Android Device Performance Framework

Das Android Dynamic Performance Framework umfasst eine Reihe von APIs, über die Spiele direkter mit den Systemen für Energie- und Wärmeverwaltung von Android-Geräten interagieren können. Du kannst das dynamische Verhalten von Android-Systemen überwachen und die Spielleistung auf ein dauerhaft aufrechterhaltbares Niveau optimieren, bei dem die Geräte nicht überhitzen. Verwende die [Erweiterung für das Android Dynamic Performance Framework](https://defold.com/extension-adpf/), um die Leistung deines Defold-Spiels für Android-Geräte zu überwachen und zu optimieren.
