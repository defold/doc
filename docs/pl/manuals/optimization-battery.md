---
title: Optymalizacja zużycia baterii w grze stworzonej w Defold
brief: Ta instrukcja opisuje, jak zoptymalizować zużycie baterii w grze stworzonej w Defold.
---

# Optymalizuj zużycie baterii
Zużycie baterii jest przede wszystkim istotne, jeśli tworzysz grę na urządzenia mobilne lub przenośne. Wysokie użycie CPU lub GPU szybko rozładuje baterię i przegrzeje urządzenie.

Zapoznaj się z instrukcjami dotyczącymi [optymalizacji wydajności w czasie działania](/manuals/optimization-speed) gry, aby dowiedzieć się, jak zmniejszyć użycie CPU i GPU.

## Wyłącz akcelerometr
Jeśli tworzysz grę mobilną, która nie korzysta z akcelerometru urządzenia, zaleca się [wyłączenie go w *game.project*](/manuals/project-settings/#use-accelerometer), aby zmniejszyć liczbę generowanych zdarzeń wejściowych.

# Optymalizacje specyficzne dla platformy

## Android Dynamic Performance Framework

Android Dynamic Performance Framework to zestaw API, które pozwalają grom i aplikacjom wchodzić w bardziej bezpośrednią interakcję z systemami zasilania i zarządzania temperaturą na urządzeniach z systemem Android. Można monitorować dynamiczne zachowanie w systemie Android i optymalizować wydajność gry na poziomie, który jest zrównoważony i nie przegrzewa urządzeń. Użyj rozszerzenia [Android Dynamic Performance Framework](https://defold.com/extension-adpf/), aby monitorować i optymalizować wydajność swojej gry stworzonej w Defold na urządzeniach z systemem Android.
