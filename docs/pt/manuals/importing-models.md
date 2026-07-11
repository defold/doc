---
title: Importando modelos
brief: Este manual aborda como importar modelos 3D usados pelo componente de modelo.
---

# Importando modelos 3D
O Defold oferece suporte a modelos, esqueletos e animações no formato glTF 2.0 (GL Transmission Format). Use arquivos *.gltf* ou *.glb* para modelos 3D. O glTF é um formato moderno criado para transferir e carregar dados 3D em motores de jogo e aplicações em tempo real.

Você pode usar ferramentas como Maya, 3ds Max, SketchUp e Blender para criar ou converter modelos 3D para glTF.

O Blender é um programa poderoso e popular de modelagem, animação e renderização 3D. Ele roda em Windows, macOS e Linux e está disponível gratuitamente em [https://www.blender.org](https://www.blender.org).

![Modelo no Blender](images/model/blender_gltf.png)

## Importando para o Defold
Para importar um modelo, arraste e solte o arquivo *.gltf* ou *.glb* no painel *Assets* do editor Defold.

O glTF pode ser armazenado de duas formas comuns:

* *.glb* é um único arquivo binário. Ele contém os dados do modelo e também pode conter imagens de textura empacotadas. Isso é conveniente quando você quer mover ou armazenar um modelo como um único arquivo.
* *.gltf* é um arquivo JSON baseado em texto. Ele geralmente referencia um arquivo *.bin* separado para os dados de malha e imagens de textura separadas, como *.png* ou *.jpg*. Ao usar essa variante, adicione todos os arquivos referenciados ao projeto e mantenha os caminhos relativos intactos.

Se o modelo deve usar uma textura no Defold, importe a imagem de textura como um asset separado. Mesmo quando o arquivo glTF/GLB de origem contém imagens incorporadas, as texturas devem ser atribuídas ao componente de Modelo pelas propriedades de textura do material do componente.

![Assets de modelo importados](images/model/assets_gltf.png)

::: sidenote
A partir do Defold 1.13.0, o Defold preserva as posições e transformações do arquivo glTF importado e não recentraliza automaticamente o modelo durante a importação. A prévia do editor e o runtime usam as transformações importadas de forma consistente: malhas com skinning ou vinculadas a ossos preservam suas transformações locais relativas ao esqueleto, enquanto malhas rígidas mantêm seu posicionamento global achatado.

Se um modelo criado com uma versão anterior do Defold mudar de posição ou orientação depois de ser reimportado, corrija a transformação no Blender ou em outra ferramenta de criação e exporte novamente o arquivo *.gltf* ou *.glb*.
:::

## Usando um modelo
Depois de importar o modelo, use-o em um [componente de Modelo](/manuals/model):

1. Crie um arquivo Model no painel *Assets* com <kbd>New... ▸ Model</kbd>, ou adicione um componente Model diretamente a um objeto de jogo com <kbd>Add Component ▸ Model</kbd>.
2. Defina a propriedade *Mesh* para o arquivo *.gltf* ou *.glb* importado que contém a malha.
3. Para um modelo animado, defina a propriedade *Skeleton* para o arquivo *.gltf* ou *.glb* que contém o esqueleto. Muitas vezes é o mesmo arquivo usado em *Mesh* quando malha, esqueleto e animações são exportados juntos.
4. Crie um arquivo *Animation Set* para as animações e atribua-o à propriedade *Animations*. Defina *Default Animation* se quiser que uma animação comece automaticamente.
5. Defina a propriedade *Material* para um material adequado ao modelo. Os arquivos integrados *model.material*, *model_instances.material*, *model_skinned.material* e *model_skinned_instances.material* são bons pontos de partida.
6. Defina as propriedades de textura do material, como *Texture*, para os arquivos de imagem de textura importados. Se o material usa várias texturas, atribua cada textura ao campo de textura de material correspondente.


## Exportando para glTF
O arquivo *.gltf* ou *.glb* exportado contém todos os vértices, arestas e faces que compõem o modelo, bem como _coordenadas UV_ (qual parte da imagem de textura mapeia para uma determinada parte da malha), se você as tiver definido, os ossos no esqueleto e os dados de animação.

* Uma descrição detalhada sobre malhas poligonais pode ser encontrada em http://en.wikipedia.org/wiki/Polygon_mesh.

* Coordenadas UV e mapeamento UV são descritos em http://en.wikipedia.org/wiki/UV_mapping.

O Defold impõe algumas limitações aos dados de animação exportados:

* Atualmente, o Defold oferece suporte apenas a animações baked. As animações precisam ter matrizes para cada osso animado em cada keyframe, e não posição, rotação e escala como chaves separadas.

* As animações também são interpoladas linearmente. Se você usar interpolação de curvas mais avançada, as animações precisam ser prebaked pelo exportador.

### Requisitos
Ao exportar um modelo, lembre-se de que o suporte a glTF pode variar entre ferramentas e motores. Use glTF 2.0, verifique se o modelo tem coordenadas UV corretas caso use texturas, e importe imagens de textura separadamente quando elas precisarem ser atribuídas a um componente de Modelo.

Embora nossa ambição seja oferecer suporte completo ao formato glTF, ainda não chegamos lá.
Se um recurso estiver faltando, faça uma solicitação de recurso em [nosso repositório](https://github.com/defold/defold/issues)

### Exportando uma textura
Se você ainda não tiver uma textura para o seu modelo, pode usar o Blender para gerar uma. Você deve fazer isso antes de remover materiais extras do modelo. Comece selecionando a malha e todos os seus vértices:

![Selecionar tudo](images/model/blender_select_all_vertices.png)

Quando todos os vértices estiverem selecionados, você faz o unwrap da malha para obter o layout UV:

![Fazer unwrap da malha](images/model/blender_unwrap_mesh.png)

Você pode então exportar o layout UV para uma imagem que pode ser usada como textura:

![Exportar layout UV](images/model/blender_export_uv_layout.png)

![Resultado da exportação do layout UV](images/model/blender_export_uv_layout_result.png)

### Exportando usando o Blender
Exporte seu modelo do Blender usando <kbd>File ▸ Export ▸ glTF 2.0 (.glb/.gltf)</kbd>.

![Exportando usando o Blender](images/model/export_gltf.png)

Selecione o objeto ou os objetos antes de exportar e habilite *Selected Objects* se quiser exportar apenas a seleção.

Escolha uma das opções de *Format*:

* *glTF Binary (.glb)* cria um único arquivo. Use esta opção quando quiser que o modelo seja fácil de mover ou armazenar como um único asset.
* *glTF Separate (.gltf + .bin + textures)* cria arquivos separados para a descrição do modelo, os dados binários e as texturas. Use esta opção quando quiser editar imagens de textura ou atribuí-las separadamente no Defold.

Se o modelo contém animações, habilite a exportação de animações e verifique se elas estão baked. Se o modelo usa texturas, verifique se a malha tem unwrap UV e se as imagens de textura são exportadas em um formato que o Defold possa importar, como PNG ou JPEG.

![Exportando usando o Blender](images/model/export_settings.png)
