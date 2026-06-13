---
title: El diseño de Defold
brief: La filosofía detrás del diseño de Defold
---

# El diseño de Defold

Defold fue creado con los siguientes objetivos:

- Ser una plataforma de producción completa, profesional y lista para usar para equipos de juegos.
- Ser simple y claro, proporcionando soluciones explícitas para problemas comunes de arquitectura y flujo de trabajo en el desarrollo de juegos.
- Ser una plataforma de desarrollo extremadamente rápida, ideal para el desarrollo iterativo de juegos.
- Ofrecer alto rendimiento en tiempo de ejecución.
- Ser verdaderamente multiplataforma.

El diseño del editor y del motor se elaboró cuidadosamente para alcanzar esos objetivos. Algunas de nuestras decisiones de diseño difieren de lo que quizá conozcas si tienes experiencia con otras plataformas, por ejemplo:

- Requerimos una declaración estática del árbol de recursos y de toda la nomenclatura. Esto requiere algo de esfuerzo inicial por tu parte, pero ayuda enormemente al proceso de desarrollo a largo plazo.
- Fomentamos el paso de mensajes entre entidades simples y encapsuladas.
- No existe herencia de orientación a objetos.
- Nuestras API son asíncronas.
- El pipeline de renderizado está controlado por código y es completamente personalizable.
- Todos nuestros archivos de recursos están en formatos simples de texto plano, estructurados de forma óptima para merges de Git, así como para importación y procesamiento con herramientas externas.
- Los recursos se pueden cambiar y recargar en caliente en un juego en ejecución, lo que permite iteración y experimentación extremadamente rápidas.
