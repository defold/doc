---
title: Native Erweiterungen - Defold SDK
brief: Dieses Handbuch beschreibt, wie du beim Erstellen nativer Erweiterungen mit dem Defold SDK arbeitest.
---

# Das Defold SDK {#the-defold-sdk}

Das Defold SDK enthält die erforderlichen Funktionen, um eine native Erweiterung (native extension) zu deklarieren und sowohl mit der systemnahen nativen Plattformschicht, auf der die Anwendung läuft, als auch mit der übergeordneten Lua-Schicht, in der die Spiellogik erstellt wird, zu interagieren.

## Verwendung {#usage}

C++-Erweiterungen können die Sammelheaderdatei `dmsdk/sdk.h` einbinden:

```cpp
#include <dmsdk/sdk.h>
```

Der Sammelheader enthält C++-Deklarationen und kann nicht in eine C-Quelldatei eingebunden werden. C-Quelldateien sollten die einzelnen C-kompatiblen `.h`-Headerdateien einbinden, die sie benötigen, zum Beispiel:

```c
#include <dmsdk/extension/extension.h>
#include <dmsdk/dlib/configfile.h>
#include <dmsdk/resource/resource.h>
```

Nur ein Teil von dmSDK verfügt derzeit über eine reine C-Schnittstelle; nicht jedes C++-Subsystem hat eine Entsprechung in C. Die verfügbaren Funktionen und Typen sind in der [Übersicht der C-API](/ref/overview_defoldc/) und der [Übersicht der C++-API](/ref/overview_defoldcpp/) dokumentiert. Die Headerdateien des Defold SDK sind als separates Archiv `defoldsdk_headers.zip` in jeder [Defold-Veröffentlichung auf GitHub](https://github.com/defold/defold/releases) enthalten. Du kannst diese Headerdateien für die Codevervollständigung im Editor deiner Wahl verwenden.
