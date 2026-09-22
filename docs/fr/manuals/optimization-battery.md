---
title: Optimiser la consommation de la batterie d'un jeu Defold
brief: Ce manuel explique comment optimiser la consommation de la batterie d'un jeu Defold.
---

# Optimiser la consommation de la batterie {#optimize-battery-usage}
La consommation de la batterie est surtout un enjeu si vous ciblez des appareils mobiles ou portables. Une utilisation élevée du CPU ou du GPU décharge rapidement la batterie et provoque une surchauffe de l'appareil.

Consultez les manuels expliquant comment [optimiser les performances à l'exécution](/manuals/optimization-speed) d'un jeu pour savoir comment réduire l'utilisation du CPU et du GPU.

## Désactiver l'accéléromètre {#disable-accelerometer}
Si vous créez un jeu mobile qui n'utilise pas l'accéléromètre de l'appareil, il est recommandé de [le désactiver dans *game.project*](/manuals/project-settings/#use-accelerometer) pour réduire le nombre d'événements d'entrée générés.

# Optimisations propres à chaque plateforme {#platform-specific-optimizations}

## Android Device Performance Framework {#android-device-performance-framework}

Android Dynamic Performance Framework est un ensemble d'API qui permettent aux jeux d'interagir plus directement avec les systèmes de gestion de l'alimentation et de la température des appareils Android. Il est possible de surveiller le comportement dynamique des systèmes Android et d'optimiser les performances du jeu à un niveau soutenable qui ne provoque pas de surchauffe des appareils. Utilisez l'[extension Android Dynamic Performance Framework](https://defold.com/extension-adpf/) pour surveiller et optimiser les performances de votre jeu Defold sur les appareils Android.
