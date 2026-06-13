---
title: Nodos caja GUI en Defold
brief: Este manual explica cómo usar los nodos caja GUI.
---

# Nodos caja GUI

Un nodo caja (box-node) es un rectángulo relleno con un color, una textura o una animación.

## Agregar nodos caja

Agrega nuevos nodos caja haciendo <kbd>click derecho</kbd> en *Outline* y seleccionando <kbd>Add ▸ Box</kbd>, o presiona <kbd>A</kbd> y selecciona <kbd>Box</kbd>.

Puedes usar imágenes y animaciones de atlas o tile sources que se hayan agregado a la GUI. Para agregar texturas, haz <kbd>click derecho</kbd> en el icono de carpeta *Textures* en *Outline* y selecciona <kbd>Add ▸ Textures...</kbd>. Luego configura la propiedad *Texture* del nodo caja:

![Texturas](images/gui-box/create.png)

Ten en cuenta que el color del nodo caja teñirá los gráficos. El color de tinte se multiplica sobre los datos de la imagen, lo que significa que si configuras el color en blanco (el valor predeterminado), no se aplica ningún tinte.

![Textura teñida](images/gui-box/tinted.png)

Los nodos caja siempre se renderizan, incluso si no tienen una textura asignada, si tienen su alfa configurado en `0` o si tienen tamaño `0, 0, 0`. Los nodos caja siempre deben tener una textura asignada para que el renderer pueda agruparlos correctamente y reducir el número de draw calls.

## Reproducir animaciones

Los nodos caja pueden reproducir animaciones de atlas o tile sources. Consulta el [manual de animación flipbook](/manuals/flipbook-animation) para obtener más información.

:[Slice-9](../shared/slice-9-texturing.md)
