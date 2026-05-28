---
title: Perfis de textura no Defold
brief: O Defold suporta processamento automático de texturas e compressão de dados de imagem. Este manual descreve a funcionalidade disponível.
---

# Perfis de textura

O Defold suporta processamento automático de texturas e compressão de dados de imagem (em *Atlas*, *Tile sources*, *Cubemaps* e texturas independentes usadas para modelos, GUI etc).

Há dois tipos de compressão: compressão de imagem por software e compressão de textura por hardware.

1. Compressão por software (como PNG e JPEG) reduz o tamanho de armazenamento dos recursos de imagem. Isso torna o tamanho final do bundle menor. No entanto, os arquivos de imagem precisam ser descomprimidos ao serem lidos para a memória; portanto, mesmo que uma imagem seja pequena em disco, ela pode ter um grande uso de memória.

2. Compressão de textura por hardware também reduz o tamanho de armazenamento dos recursos de imagem. Mas, ao contrário da compressão por software, ela reduz o uso de memória das texturas. Isso acontece porque o hardware gráfico consegue gerenciar diretamente texturas comprimidas sem precisar descomprimi-las antes.

O processamento de texturas é configurado por meio de um perfil de textura específico. Nesse arquivo, você cria _profiles_ que expressam quais formato(s) e tipo comprimidos devem ser usados ao criar bundles para uma plataforma específica. _Profiles_ são então vinculados a _patterns_ de caminhos de arquivo correspondentes, permitindo controle refinado sobre quais arquivos no seu projeto devem ser comprimidos e exatamente como.

Como toda compressão de textura por hardware disponível é com perdas, você terá artefatos nos dados de textura. Esses artefatos dependem muito da aparência do material de origem e do método de compressão usado. Você deve testar seu material de origem e experimentar para obter os melhores resultados. O Google é seu amigo aqui.

Você pode selecionar qual compressão de imagem por software será aplicada aos dados finais da textura (comprimidos ou brutos) nos arquivos de bundle. O Defold suporta os formatos de compressão [Basis Universal](https://github.com/BinomialLLC/basis_universal) e [ASTC](https://www.khronos.org/opengl/wiki/ASTC_Texture_Compression).

::: sidenote
Compressão é uma operação intensiva em recursos e demorada, que pode causar tempos de build _muito_ longos dependendo do número de imagens de textura a comprimir e também dos formatos de textura e do tipo de compressão por software escolhidos.
:::

### Basis Universal

Basis Universal (ou BasisU, abreviado) comprime a imagem em um formato intermediário que é transcodificado em tempo de execução para um formato de hardware apropriado para a GPU do dispositivo atual. O formato Basis Universal é de alta qualidade, mas com perdas.
Todas as imagens também são comprimidas usando LZ4 para reduzir ainda mais o tamanho de arquivo quando armazenadas no arquivo do jogo.

### ASTC

ASTC é um formato de compressão de textura flexível e eficiente desenvolvido pela ARM e padronizado pelo Khronos Group. Ele oferece uma ampla variedade de tamanhos de bloco e taxas de bits, permitindo que desenvolvedores equilibrem qualidade de imagem e uso de memória de forma eficiente. ASTC suporta vários tamanhos de bloco, de 4×4 a 12×12 texels, correspondendo a taxas de bits que vão de 8 bits por texel até 0.89 bits por texel. Essa flexibilidade permite controle refinado da troca entre qualidade da textura e requisitos de armazenamento.

ASTC suporta vários tamanhos de bloco, de 4×4 a 12×12 texels, correspondendo a taxas de bits que vão de 8 bits por texel até 0.89 bits por texel. Essa flexibilidade permite controle refinado da troca entre qualidade da textura e requisitos de armazenamento. A tabela a seguir mostra os tamanhos de bloco suportados e suas taxas de bits correspondentes:

| Block Size (width x height) | Bits per pixel |
| --------------------------- | -------------- |
| 4x4                         | 8.00           |
| 5x4                         | 6.40           |
| 5x5                         | 5.12           |
| 6x5                         | 4.27           |
| 6x6                         | 3.56           |
| 8x5                         | 3.20           |
| 8x6                         | 2.67           |
| 10x5                        | 2.56           |
| 10x6                        | 2.13           |
| 8x8                         | 2.00           |
| 10x8                        | 1.60           |
| 10x10                       | 1.28           |
| 12x10                       | 1.07           |
| 12x12                       | 0.89           |


#### Dispositivos suportados

Embora ASTC ofereça ótimos resultados, ele não é suportado por todas as placas gráficas. Aqui está uma pequena lista de dispositivos suportados por fornecedor:

| GPU vendor         | Support                                                               |
| ------------------ | --------------------------------------------------------------------- |
| ARM (Mali)         | Todas as GPUs ARM Mali com suporte a OpenGL ES 3.2 ou Vulkan suportam ASTC. |
| Qualcomm (Adreno)  | GPUs Adreno com suporte a OpenGL ES 3.2 ou Vulkan suportam ASTC.      |
| Apple              | GPUs Apple desde o chip A8 suportam ASTC.                             |
| NVIDIA             | O suporte a ASTC é principalmente para GPUs móveis (por exemplo, chips baseados em Tegra). |
| AMD (Radeon)       | GPUs AMD com suporte a Vulkan geralmente suportam ASTC via software.  |
| Intel (Integrated) | ASTC é suportado em GPUs Intel modernas via software.                 |

## Perfis de textura

Cada projeto contém um arquivo *.texture_profiles* específico que contém a configuração usada ao comprimir texturas. Por padrão, esse arquivo é *builtins/graphics/default.texture_profiles* e tem uma configuração que corresponde a todos os recursos de textura para um perfil usando RGBA, sem compressão de textura por hardware e usando a compressão de arquivo ZLib padrão.

Para adicionar compressão de textura:

- Selecione <kbd>File ▸ New...</kbd> e escolha *Texture Profiles* para criar um novo arquivo de perfis de textura. (Como alternativa, copie *default.texture_profiles* para um local fora de *builtins*)
- Escolha um nome e local para o novo arquivo.
- Altere a entrada *texture_profiles* em *game.project* para apontar para o novo arquivo.
- Abra o arquivo *.texture_profiles* e configure-o de acordo com seus requisitos.

![New profiles file](images/texture_profiles/texture_profiles_new_file.png)

![Setting the texture profile](images/texture_profiles/texture_profiles_game_project.png)

Você pode ativar e desativar o uso de perfis de textura nas preferências do editor. Selecione <kbd>File ▸ Preferences...</kbd>. A aba *General* contém a caixa de seleção *Enable texture profiles*.

![Texture profiles preferences](images/texture_profiles/texture_profiles_preferences.png)

## Configurações de caminho {#path-settings}

A seção *Path Settings* do arquivo de perfis de textura contém uma lista de padrões de caminho e qual *profile* usar ao processar recursos que correspondem ao caminho. Os caminhos são expressos como padrões "Ant Glob" (veja a [documentação](http://ant.apache.org/manual/dirtasks.html#patterns) para detalhes). Padrões podem ser expressos usando os seguintes curingas:

`*`
: Corresponde a zero ou mais caracteres. Por exemplo, `sprite*.png` corresponde aos arquivos *`sprite.png`*, *`sprite1.png`* e *`sprite_with_a_long_name.png`*.

`?`
: Corresponde exatamente a um caractere. Por exemplo: `sprite?.png` corresponde aos arquivos *sprite1.png*, *`spriteA.png`*, mas não a *`sprite.png`* ou *`sprite_with_a_long_name.png`*.

`**`
: Corresponde a uma árvore completa de diretórios ou, quando usado como nome de um diretório, a zero ou mais diretórios. Por exemplo: `/gui/**` corresponde a todos os arquivos no diretório */gui* e em todos os seus subdiretórios.

![Paths](images/texture_profiles/texture_profiles_paths.png)

Este exemplo contém dois padrões de caminho e seus perfis correspondentes.

`/gui/**/*.atlas`
: Todos os arquivos *.atlas* no diretório *`/gui`* ou em qualquer um de seus subdiretórios serão processados de acordo com o perfil "gui_atlas".

`/**/*.atlas`
: Todos os arquivos *.atlas* em qualquer lugar do projeto serão processados de acordo com o perfil "atlas".

Observe que o caminho mais genérico é colocado por último. O algoritmo de correspondência funciona de cima para baixo. A primeira ocorrência que corresponde ao caminho do recurso será usada. Uma expressão de caminho correspondente mais abaixo na lista nunca sobrescreve a primeira correspondência. Se os caminhos tivessem sido colocados na ordem oposta, todo atlas teria sido processado com o perfil "atlas", inclusive os do diretório *`/gui`*.

Recursos de textura que _não_ correspondem a nenhum caminho no arquivo de perfis serão compilados e escalados para a potência de 2 mais próxima, mas fora isso serão deixados intactos.

## Profiles

A seção *profiles* do arquivo de perfis de textura contém uma lista de perfis nomeados. Cada perfil contém uma ou mais *platforms*, cada plataforma descrita por uma lista de propriedades.

![Profiles](images/texture_profiles/texture_profiles_profiles.png)

*Platforms*
: Especifica uma plataforma correspondente. `OS_ID_GENERIC` corresponde a todas as plataformas, `OS_ID_WINDOWS` corresponde a bundles-alvo Windows, `OS_ID_IOS` corresponde a bundles iOS e assim por diante. Observe que, se `OS_ID_GENERIC` for especificado, ele será incluído para todas as plataformas.

::: important
Se duas [configurações de caminho](#path-settings) corresponderem ao mesmo arquivo e o caminho usar perfis diferentes com plataformas diferentes, **ambos** os perfis serão usados e **duas** texturas serão geradas.
:::

*Formats*
: Um ou mais formatos de textura a gerar. Se vários formatos forem especificados, texturas para cada formato serão geradas e incluídas no bundle. A engine seleciona texturas de um formato suportado pela plataforma em tempo de execução.

*Mipmaps*
: Se marcado, mipmaps são gerados para a plataforma. Desmarcado por padrão.

*Premultiply alpha*
: Se marcado, o alpha é pré-multiplicado nos dados da textura. Marcado por padrão.

*Max Texture Size*
: Se definido para um valor diferente de zero, as texturas são limitadas em tamanho de pixels ao número especificado. Qualquer textura com largura ou altura maior que o valor especificado será reduzida.

Os *Formats* adicionados a um perfil têm as seguintes propriedades:

*Format*
: O formato a usar ao codificar a textura. Veja abaixo todos os formatos de textura disponíveis.

*Compressor*
: O compressor a usar ao codificar a textura.

*Compressor Preset*
: Seleciona uma predefinição de compressão a usar na codificação da imagem comprimida resultante. Cada preset de compressor é único para o compressor e suas configurações dependem do próprio compressor. Para simplificar essas configurações, os presets de compressão atuais vêm em quatro níveis:

| Predefinição | Observação                                    |
| --------- | --------------------------------------------- |
| `LOW`     | Compressão mais rápida. Baixa qualidade de imagem |
| `MEDIUM`  | Compressão padrão. Melhor qualidade de imagem |
| `HIGH`    | Compressão mais lenta. Tamanho de arquivo menor |
| `HIGHEST` | Compressão lenta. Menor tamanho de arquivo    |

Observe que o compressor `uncompressed` tem apenas um preset chamado `uncompressed`, o que significa que nenhuma compressão será aplicada às texturas.
Para ver a lista de compressores disponíveis, veja [Compressors](#compressors)

## Formatos de textura

Texturas de hardware gráfico podem ser processadas em dados sem compressão ou comprimidos com *perdas*, com vários números de canais e profundidades de bits. Compressão de hardware fixa significa que a imagem resultante terá tamanho fixo, independentemente do conteúdo da imagem. Isso significa que a perda de qualidade durante a compressão depende do conteúdo da textura original.

Como a transcodificação da compressão Basis Universal depende das capacidades da GPU do dispositivo, os formatos recomendados para uso com compressão Basis Universal são formatos genéricos como:
`TEXTURE_FORMAT_RGB`, `TEXTURE_FORMAT_RGBA`, `TEXTURE_FORMAT_RGB_16BPP`, `TEXTURE_FORMAT_RGBA_16BPP`, `TEXTURE_FORMAT_LUMINANCE` e `TEXTURE_FORMAT_LUMINANCE_ALPHA`.

O transcodificador Basis Universal suporta muitos formatos de saída, como `ASTC4x4`, `BCx`, `ETC2`, `ETC1` e `PVRTC1`.

Os seguintes formatos de compressão com perdas são suportados atualmente:

| Formato                           | Compressão  | Detalhes                         |
| --------------------------------- | ----------- | -------------------------------- |
| `TEXTURE_FORMAT_RGB`              | none        | Cor de 3 canais. Alpha é descartado |
| `TEXTURE_FORMAT_RGBA`             | none        | Cor de 3 canais e alpha completo. |
| `TEXTURE_FORMAT_RGB_16BPP`        | none        | Cor de 3 canais. 5+6+5 bits. |
| `TEXTURE_FORMAT_RGBA_16BPP`       | none        | Cor de 3 canais e alpha completo. 4+4+4+4 bits. |
| `TEXTURE_FORMAT_LUMINANCE`        | none        | Escala de cinza de 1 canal, sem alpha. Canais RGB multiplicados em um. Alpha é descartado. |
| `TEXTURE_FORMAT_LUMINANCE_ALPHA`  | none        | Escala de cinza de 1 canal e alpha completo. Canais RGB multiplicados em um. |

Para ASTC, o número de canais sempre será 4 (RGB + alpha), e o próprio formato define o tamanho do bloco de compressão.
Observe que esses formatos só são compatíveis com um compressor ASTC - qualquer outra combinação produzirá um erro de build.

`TEXTURE_FORMAT_RGBA_ASTC_4X4`
`TEXTURE_FORMAT_RGBA_ASTC_5X4`
`TEXTURE_FORMAT_RGBA_ASTC_5X5`
`TEXTURE_FORMAT_RGBA_ASTC_6X5`
`TEXTURE_FORMAT_RGBA_ASTC_6X6`
`TEXTURE_FORMAT_RGBA_ASTC_8X5`
`TEXTURE_FORMAT_RGBA_ASTC_8X6`
`TEXTURE_FORMAT_RGBA_ASTC_8X8`
`TEXTURE_FORMAT_RGBA_ASTC_10X5`
`TEXTURE_FORMAT_RGBA_ASTC_10X6`
`TEXTURE_FORMAT_RGBA_ASTC_10X8`
`TEXTURE_FORMAT_RGBA_ASTC_10X10`
`TEXTURE_FORMAT_RGBA_ASTC_12X10`
`TEXTURE_FORMAT_RGBA_ASTC_12X12`


## Compressores {#compressors}

Os seguintes compressores de textura são suportados por padrão. Os dados são descomprimidos quando o arquivo de textura é carregado na memória.

| Nome                              | Formatos                  | Observação                                                                                    |
| --------------------------------- | ------------------------- | --------------------------------------------------------------------------------------------- |
| `Uncompressed`                    | Todos os formatos         | Nenhuma compressão será aplicada. Padrão.                                                     |
| `BasisU`                          | Todos os formatos RGB/RGBA | Basis Universal de alta qualidade, compressão com perdas. Nível de qualidade menor resulta em tamanho menor. |
| `ASTC`                            | Todos os formatos ASTC    | Compressão ASTC com perdas. Nível de qualidade menor resulta em tamanho menor.                |

::: sidenote
O Defold suporta compressores instaláveis no pipeline de compressores de textura. Isso permite implementar um algoritmo de compressão de textura em uma extensão, como WEBP ou algo completamente personalizado.
:::

## Imagem de exemplo

Para ajudar a entender melhor a saída, aqui está um exemplo.
Observe que a qualidade da imagem, o tempo de compressão e o tamanho comprimido sempre dependem da imagem de entrada e podem variar.

Imagem base (1024x512):
![New profiles file](images/texture_profiles/kodim03_pow2.png)

### Tempos de compressão

| Predefinição | Tempo de compressão | Tempo relativo |
| ------------- | ------------------- | -------------- |
| `LOW`     | 0m0.143s         | 0.5x            |
| `MEDIUM`  | 0m0.294s         | 1.0x            |
| `HIGH`    | 0m1.764s         | 6.0x            |
| `HIGHEST` | 0m1.109s         | 3.8x            |

### Perda de sinal

A comparação é feita usando a ferramenta `basisu` (medindo o PSNR)
100 dB significa nenhuma perda de sinal (ou seja, é igual à imagem original).

| Predefinição | Sinal                                            |
| ------------- | ------------------------------------------------ |
| `LOW`     | Max:  34 Mean: 0.470 RMS: 1.088 PSNR: 47.399 dB |
| `MEDIUM`  | Max:  35 Mean: 0.439 RMS: 1.061 PSNR: 47.620 dB |
| `HIGH`    | Max:  37 Mean: 0.898 RMS: 1.606 PSNR: 44.018 dB |
| `HIGHEST` | Max:  51 Mean: 1.298 RMS: 2.478 PSNR: 40.249 dB |

### Tamanhos dos arquivos comprimidos

O tamanho do arquivo original é 1572882 bytes.

| Predefinição | Tamanho de arquivo | Proporção |
| ------------- | ------------------ | --------- |
| `LOW`     | 357225     | 22.71 %  |
| `MEDIUM`  | 365548     | 23.24 %  |
| `HIGH`    | 277186     | 17.62 %  |
| `HIGHEST` | 254380     | 16.17 %  |


### Qualidade da imagem

Aqui estão as imagens resultantes (recuperadas da codificação ASTC usando a ferramenta `basisu`)

`LOW`
![low compression preset](images/texture_profiles/kodim03_pow2.fast.png)

`MEDIUM`
![medium compression preset](images/texture_profiles/kodim03_pow2.normal.png)

`HIGH`
![high compression preset](images/texture_profiles/kodim03_pow2.high.png)

`HIGHEST`
![best compression preset](images/texture_profiles/kodim03_pow2.best.png)
