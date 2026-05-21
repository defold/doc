---
title: Importando modelos
brief: Este manual aborda como importar modelos 3D usados pelo componente de modelo.
---

# Importando modelos 3D
Atualmente, o Defold oferece suporte a modelos, esqueletos e animações no formato GL Transmission Format *.glTF*. Você pode usar ferramentas como Maya, 3D Max, Sketchup e Blender para criar e/ou converter modelos 3D para o formato glTF. O Blender é um programa poderoso e popular de modelagem, animação e renderização 3D. Ele roda em Windows, macOS e Linux e está disponível gratuitamente para download em http://www.blender.org

![Model in Blender](images/model/blender.png)

## Importando para o Defold
Para importar o modelo, basta arrastar e soltar o arquivo *.gltf* ou *.dae* e a imagem de textura correspondente em algum lugar do *painel Conteúdo*.

![Imported model assets](images/model/assets.png)

## Usando um modelo
Depois de importar o modelo para o Defold, você pode usá-lo em um [componente de Modelo](/manuals/model).


## Exportando para glTF
O arquivo *.gltf* exportado contém todos os vértices, arestas e faces que compõem o modelo, bem como _coordenadas UV_ (qual parte da imagem de textura mapeia para uma determinada parte da malha), se você as tiver definido, os ossos no esqueleto e os dados de animação.

* Uma descrição detalhada sobre malhas poligonais pode ser encontrada em http://en.wikipedia.org/wiki/Polygon_mesh.

* Coordenadas UV e mapeamento UV são descritos em http://en.wikipedia.org/wiki/UV_mapping.

O Defold impõe algumas limitações aos dados de animação exportados:

* Atualmente, o Defold oferece suporte apenas a animações baked. As animações precisam ter matrizes para cada osso animado em cada keyframe, e não posição, rotação e escala como chaves separadas.

* As animações também são interpoladas linearmente. Se você usar interpolação de curvas mais avançada, as animações precisam ser prebaked pelo exportador.

### Requisitos
Ao exportar um modelo, é bom saber que ainda não temos suporte a todos os recursos.
Problemas conhecidos/recursos sem suporte do formato glTF:

* Animações de morph target
* Propriedades de material
* Texturas incorporadas

Embora nossa ambição seja oferecer suporte completo ao formato glTF, ainda não chegamos lá.
Se um recurso estiver faltando, faça uma solicitação de recurso em [nosso repositório](https://github.com/defold/defold/issues)

### Exportando uma textura
Se você ainda não tiver uma textura para o seu modelo, pode usar o Blender para gerar uma. Você deve fazer isso antes de remover materiais extras do modelo. Comece selecionando a malha e todos os seus vértices:

![Select all](images/model/blender_select_all_vertices.png)

Quando todos os vértices estiverem selecionados, você faz o unwrap da malha para obter o layout UV:

![Unwrap mesh](images/model/blender_unwrap_mesh.png)

Você pode então exportar o layout UV para uma imagem que pode ser usada como textura:

![Export UV layout](images/model/blender_export_uv_layout.png)

![Export UV layout settings](images/model/blender_export_uv_layout_settings.png)

![Export UV layout result](images/model/blender_export_uv_layout_result.png)

### Exportando usando o Blender
Você exporta seu modelo usando a opção de menu Export. Selecione o modelo antes de selecionar a opção de menu Export e marque "Selection Only" para exportar apenas o modelo.

![Exporting using Blender](images/model/blender_export.png)
