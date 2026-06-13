---
title: Optimizar el uso de memoria de un juego Defold
brief: Este manual describe cómo optimizar el uso de memoria de un juego Defold.
---

# Optimizar el uso de memoria

## Compresión de texturas
El uso de compresión de texturas no solo reduce el tamaño de los recursos dentro del archivo del juego, sino que las texturas comprimidas también pueden reducir la cantidad de memoria de GPU necesaria.

## Carga dinámica
La mayoría de los juegos tienen al menos algo de contenido que se usa con poca frecuencia. Desde el punto de vista del uso de memoria, no tiene sentido mantener ese contenido cargado en memoria en todo momento, sino cargarlo y descargarlo cuando se necesita. Esto obviamente implica un equilibrio entre tener algo disponible de inmediato a costa de memoria en runtime y cargar algo a costa del tiempo de carga.

Defold tiene varias maneras de cargar contenido dinámicamente:

* [Proxies de colección](/manuals/collection-proxy/)
* [Factories de colección dinámicas](/manuals/collection-factory/#dynamic-loading-of-factory-resources)
* [Factories dinámicas](/manuals/factory/#dynamic-loading-of-factory-resources)
* [Live Update](/manuals/live-update/)

## Optimizar contadores de componentes
Defold asigna memoria para componentes y recursos una vez cuando se crea una colección, para reducir la fragmentación de memoria. La cantidad de memoria que se asigna depende de la configuración de varios contadores de componentes en *game.project*. Usa el [profiler](/manuals/profiling/) para obtener un uso preciso de componentes y recursos, y configura tu juego para usar valores máximos más cercanos al conteo real de componentes y recursos. Esto reducirá la cantidad de memoria que usa tu juego (consulta la información sobre las [optimizaciones de max count de componentes](/manuals/project-settings/#component-max-count-optimizations)).

## Optimizar el conteo de nodos GUI
Optimiza el conteo de nodos GUI configurando el número máximo de nodos en el archivo GUI solo con lo necesario. El campo `Current Nodes` de las [propiedades del componente GUI](https://defold.com/manuals/gui/#gui-properties) mostrará la cantidad de nodos usados por el componente GUI.

:[HTML5 Optimizations](../shared/optimization-memory-html5.md)

