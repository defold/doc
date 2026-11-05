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
* *.gltf* é um arquivo JSON de texto. Normalmente referencia um arquivo *.bin* separado para os dados da malha e imagens de textura separadas como *.png*, *.jpg* ou *.ktx2*. Ao usar essa variante, adicione todos os arquivos referenciados ao projeto e mantenha seus caminhos relativos intactos.

Imagens incorporadas podem ser usadas diretamente de um arquivo glTF ou GLB sem extraí-las para assets separados. Arquivos externos de imagens e buffers ainda precisam ser importados com o modelo, preservando seus caminhos relativos.

::: sidenote
O Defold preserva as posições e transformações do arquivo glTF importado e não recentraliza automaticamente o modelo durante a importação. A prévia do editor e o runtime usam as transformações importadas de forma consistente: malhas com skinning ou vinculadas a ossos preservam suas transformações locais relativas ao esqueleto, enquanto malhas rígidas mantêm seu posicionamento global consolidado.

Um [componente Model](/manuals/model/#model-properties) pode selecionar uma única malha nomeada da cena importada. Deixar o campo *Mesh* vazio usa a cena inteira e preserva as transformações descritas acima. Selecionar uma malha usa sua geometria local sem as transformações dos nós glTF; portanto, posicione-a usando a transformação do componente Model ou do objeto de jogo.

Se um modelo criado com uma versão anterior do Defold mudar de posição ou orientação depois de ser reimportado, corrija a transformação no Blender ou em outra ferramenta de criação e exporte novamente o arquivo *.gltf* ou *.glb*.
:::

### Geometria comprimida {#compressed-geometry}

Arquivos de origem *.gltf* e *.glb* podem conter geometria comprimida com Draco ou Meshopt. As extensões de compressão glTF aceitas são:

| Compressão | Extensão glTF |
| --- | --- |
| Draco | `KHR_draco_mesh_compression` |
| Meshopt | `EXT_meshopt_compression` e `KHR_meshopt_compression` |

Exporte ou otimize seu asset glTF 2.0 usando uma dessas extensões e importe-o seguindo os mesmos passos de um modelo sem compressão. Inclua todos os buffers e texturas externos e preserve seus caminhos relativos. Atribua o arquivo importado à propriedade *Scene* de um componente Model como de costume.

O Defold decodifica a geometria comprimida durante a importação e o build. O modelo resultante usa a representação normal de geometria do Defold em tempo de execução. Esse suporte não habilita compressão Draco ou Meshopt na engine em execução, e um arquivo de origem menor não garante um bundle de jogo menor.

### Explorando a cena importada {#browsing-the-imported-scene}

Expanda um arquivo *.gltf* ou *.glb* no painel *Assets* para explorar suas malhas, materiais gerados e imagens incorporadas. Abrir a cena exibe uma prévia com seus materiais e texturas definidos. Você também pode abrir uma malha individual para visualizar uma prévia.

Os recursos expostos dentro do arquivo são somente leitura. Para criar um recurso Model editável de uma malha, copie a malha e cole-a em uma pasta do projeto. O arquivo *.model* resultante continua referenciando o arquivo glTF ou GLB importado. Para alterar a geometria de origem ou as imagens incorporadas, edite o asset em sua ferramenta de criação e exporte-o novamente.

Scripts do editor podem enumerar esses recursos com `editor.resource_children(path)`. Consulte [Percorrendo recursos do projeto](/manuals/editor-scripts/#traversing-project-resources) para ver um exemplo que visita recursivamente recursos dentro de pastas e arquivos glTF/GLB.

### Texturas KTX2 {#ktx2-textures}

Texturas de modelos podem usar fontes *.ktx2*, tanto como arquivos externos quanto como imagens incorporadas em um arquivo *.gltf* ou *.glb*. Importe os arquivos externos junto com o modelo. Imagens KTX2 incorporadas aparecem sob a cena no painel *Assets* e podem ser atribuídas diretamente aos campos de textura dos materiais ou por meio de <kbd>Auto Fill</kbd>.

[Perfis de textura](/manuals/texture-profiles/#ktx2-source-textures) determinam se o formato KTX2 de origem será mantido ou convertido para os formatos de saída configurados. **Keep KTX2 Format** preserva o formato de codificação de origem quando a compressão de texturas está habilitada, mas o processamento de imagens ainda pode exigir recodificação. Verifique o suporte ao formato nos dispositivos-alvo e considere a possível perda adicional de qualidade ao recomprimir uma textura já comprimida. Consulte [Formatos de entrada e prévias KTX2](/manuals/importing-graphics/#ktx2-textures).

<a id="using-a-model"></a>

## Usando um modelo
Depois de importar o modelo, use-o em um [componente de Modelo](/manuals/model):

1. Crie um arquivo Model no painel *Assets* com <kbd>New... ▸ Model</kbd>, ou adicione um componente Model diretamente a um objeto de jogo com <kbd>Add Component ▸ Model</kbd>.
2. Defina a propriedade *Scene* como o arquivo *.gltf* ou *.glb* importado.
3. Quando a caixa de diálogo *Auto Fill Model Fields?* aparecer, escolha <kbd>Auto Fill</kbd> para atribuir os materiais gerados e as texturas referenciadas da cena. Isso substitui os vínculos existentes de materiais e texturas. Escolha <kbd>Keep Current</kbd> para preservar seus vínculos; a nova seleção de cena ainda é aplicada.
4. Deixe *Mesh* vazio para usar a cena inteira ou selecione uma malha nomeada para usar apenas sua geometria local. Alterar a seleção de malha pode exibir a mesma caixa de diálogo: selecionar uma malha oferece seus materiais, enquanto limpar a seleção oferece todos os materiais da cena. <kbd>Keep Current</kbd> preserva os vínculos ao aplicar a nova seleção de malha.
5. Para um modelo animado, defina a propriedade *Skeleton* como o arquivo *.gltf* ou *.glb* que contém o esqueleto. Geralmente, é o mesmo arquivo usado em *Scene* quando malha, esqueleto e animações são exportados juntos.
6. Crie um arquivo *Animation Set* para as animações e atribua-o à propriedade *Animations*. Defina *Default Animation* se quiser que uma animação inicie automaticamente.

O editor oferece o preenchimento dos vínculos quando o arquivo glTF ou GLB selecionado expõe materiais. Ele resolve tanto imagens incorporadas quanto referências a imagens externas. Os materiais gerados usam os shaders glTF integrados; consulte o [manual de PBR](/manuals/physically-based-rendering/#built-in-pbr-materials) para conhecer a iluminação e os efeitos de material aceitos.

### Atribuindo materiais e texturas manualmente {#assigning-materials-and-textures-manually}

Se escolher <kbd>Keep Current</kbd> ou precisar de sombreamento personalizado, defina cada propriedade *Material* como um material adequado. Os materiais `gltf` integrados fornecem sombreamento PBR; os materiais `model` integrados e seus próprios materiais também estão disponíveis. Consulte o [manual de Model](/manuals/model/#material) para conhecer as variantes estáticas, com skinning e com instâncias e seus requisitos.

Atribua cada textura ao campo de textura correspondente do material. Você pode usar uma imagem incorporada exposta sob o arquivo glTF ou GLB no painel *Assets*, ou um asset de imagem separado no projeto. Para materiais com vários samplers, associe cada textura ao sampler pretendido; o [manual de PBR lista os nomes dos samplers glTF integrados](/manuals/physically-based-rendering/#built-in-pbr-materials).


## Exportando para glTF
O arquivo *.gltf* ou *.glb* exportado contém todos os vértices, arestas e faces que compõem o modelo, bem como _coordenadas UV_ (qual parte da imagem de textura mapeia para uma determinada parte da malha), se você as tiver definido, os ossos no esqueleto e os dados de animação.

* Uma descrição detalhada sobre malhas poligonais pode ser encontrada em http://en.wikipedia.org/wiki/Polygon_mesh.

* Coordenadas UV e mapeamento UV são descritos em http://en.wikipedia.org/wiki/UV_mapping.

O Defold impõe algumas limitações aos dados de animação exportados:

* Atualmente, o Defold oferece suporte apenas a animações baked. As animações precisam ter matrizes para cada osso animado em cada keyframe, e não posição, rotação e escala como chaves separadas.

* As animações também são interpoladas linearmente. Se você usar interpolação de curvas mais avançada, as animações precisam ser prebaked pelo exportador.

### Requisitos
Ao exportar um modelo, lembre-se de que o suporte a glTF pode variar entre ferramentas e engines. Use glTF 2.0 e verifique se o modelo tem coordenadas UV corretas caso use texturas. Imagens podem ser incorporadas ao arquivo glTF ou GLB ou armazenadas em arquivos separados referenciados pela cena. Inclua todos os arquivos externos de imagens e buffers ao importar o modelo para o Defold.

Embora nossa ambição seja oferecer suporte completo ao formato glTF, ainda não chegamos lá.
Se um recurso estiver faltando, faça uma solicitação de recurso em [nosso repositório](https://github.com/defold/defold/issues)

### Exportando uma textura
Se quiser criar uma imagem de textura manualmente, você pode exportar o layout UV do Blender como modelo. Comece selecionando a malha e todos os seus vértices:

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
