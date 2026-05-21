---
title: Filtragem de textura
brief: Este manual descreve as opções disponíveis para filtragem de textura ao renderizar gráficos.
---

# Filtragem e amostragem de texturas

A filtragem de textura decide o resultado visual em casos em que um _texel_ (um pixel em uma textura) não está perfeitamente alinhado com um pixel da tela. Isso acontece quando você move um elemento gráfico que contém a textura por menos de um pixel. Os seguintes métodos de filtro estão disponíveis:

Nearest
: O texel mais próximo será escolhido para colorir o pixel da tela. Esse método de amostragem deve ser escolhido se você quer um mapeamento perfeito de um pixel para um pixel entre suas texturas e o que vê na tela. Com filtragem nearest, tudo salta de pixel em pixel ao se mover. Isso pode parecer tremido se o Sprite se mover lentamente.

Linear
: O texel será calculado pela média com seus vizinhos antes de colorir o pixel da tela. Isso produz uma aparência suave para movimentos lentos e contínuos, pois um Sprite começará a aparecer nos pixels antes de colori-los completamente - assim é possível mover um Sprite por menos que um pixel inteiro.

A configuração de qual filtragem usar é armazenada no arquivo [Project Settings](/manuals/project-settings/#graphics). Há duas configurações:

default_texture_min_filter
: A filtragem de minificação se aplica sempre que o texel é menor que o pixel da tela.

default_texture_mag_filter
: A filtragem de magnificação se aplica sempre que o texel é maior que o pixel da tela.

Ambas as configurações aceitam os valores `linear`, `nearest`, `nearest_mipmap_nearest`, `nearest_mipmap_linear`, `linear_mipmap_nearest` ou `linear_mipmap_linear`. Por exemplo:

```ini
[graphics]
default_texture_min_filter = nearest
default_texture_mag_filter = nearest
```

Se você não especificar nada, ambas são definidas como `linear` por padrão.

Observe que a configuração em *game.project* é usada pelos samplers padrão. Se você especificar samplers em um material personalizado, poderá definir o método de filtro em cada sampler especificamente. Veja o [manual de Materials](/manuals/material/) para detalhes.
