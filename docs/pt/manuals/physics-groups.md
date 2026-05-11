---
title: Grupos de colisão no Defold
brief: A engine de física permite agrupar seus objetos de física e filtrar como eles devem colidir.
---

# Grupo e máscara

A engine de física permite agrupar seus objetos de física e filtrar como eles devem colidir. Isso é tratado por _grupos de colisão_ nomeados. Para cada objeto de colisão, você cria duas propriedades que controlam como o objeto colide com outros objetos: *Group* e *Mask*.

Para que uma colisão entre dois objetos seja registrada, ambos os objetos devem especificar mutuamente os grupos um do outro em seu campo *Mask*.

![Physics collision group](images/physics/collision_group.png)

O campo *Mask* pode conter vários nomes de grupos, permitindo cenários de interação complexos.

## Detectando colisões
Quando dois objetos de colisão com grupos e máscaras correspondentes colidem, a engine de física gera [mensagens de colisão](/manuals/physics-messages) que podem ser usadas em jogos para reagir às colisões.
