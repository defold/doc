---
title: Manifesto do aplicativo
brief: Este manual descreve como o manifesto do aplicativo pode ser usado para excluir recursos da engine.
---

# Manifesto do aplicativo

O manifesto do aplicativo controla quais recursos e backends são vinculados à engine. Recomenda-se excluir recursos não utilizados, pois isso reduz o tamanho final do binário do jogo. O manifesto do aplicativo também contém opções usadas durante o build, como as versões mínimas dos navegadores compatíveis com HTML5 e as configurações de memória do WebAssembly.

![](images/app_manifest/create-app-manifest.png)

![](images/app_manifest/app-manifest.png)


# Aplicando o manifesto

Em `game.project`, atribua o manifesto a `Native Extensions` -> `App Manifest`.

## Física 2D {#physics-2d}

Selecione qual implementação do Box2D incluir:

* **Box2D Version 3** - Inclui o Box2D 3. Essa opção é opt-in e pode produzir resultados de simulação diferentes da implementação legada; portanto, projetos existentes talvez precisem reajustar suas configurações de física.
* **Box2D (Legacy Defold version)** - Inclui a implementação legada do Box2D do Defold. Esta é a opção padrão.
* **None** - Exclui a física 2D.

As configurações do solver do Box2D são específicas de cada versão. Consulte as [configurações de projeto do Box2D](/manuals/project-settings/#box2d) para obter detalhes.

## Física 3D

Inclui a implementação de física 3D Bullet. Ela é incluída por padrão; desative esta configuração para excluir a física 3D.

## Rig + Modelo

Controla a funcionalidade de rig e modelo, ou selecione None para excluir modelo e rig completamente. (Veja a documentação de [`Model`](https://defold.com/manuals/model/#model-component)).


## Excluir Gravação

Exclui a capacidade de gravação de vídeo da engine (veja a documentação da mensagem [`start_record`](https://defold.com/ref/stable/sys/#start_record)).


## Profiler

Controle quando a funcionalidade do profiler é vinculada à engine:

* **Debug Only** - Inclui o profiler apenas em builds debug. Esta é a opção padrão.
* **None** - Exclui a funcionalidade do profiler de todas as variantes de build.
* **Always** - Inclui o profiler em builds debug e release.

A configuração do manifesto do aplicativo controla se o código do profiler é vinculado a um build. As configurações em `profiler` no *game.project* controlam o comportamento do profiler em tempo de execução. Aprenda a usar os recursos disponíveis no [manual de Profiling](/manuals/profiling/).

## Som {#sound}

Os controles de som determinam quais sistemas e decodificadores de som são vinculados à engine.

### Excluir Som

Exclui todas as capacidades de reprodução de som da engine.

### Excluir decodificador de som: WAV

Exclui o suporte a recursos de som WAV.

### Excluir decodificador de som: OGG

Exclui o suporte a recursos de som Ogg Vorbis.

### Incluir decodificador de som: Opus

Inclui o suporte a recursos de som Ogg Opus. O decodificador Opus é excluído por padrão; portanto, esta opção deve ser ativada antes que recursos `.opus` possam ser reproduzidos. Consulte o [manual de Som](/manuals/sound/) para saber quais formatos são compatíveis.

## Excluir Input

Exclui todo o tratamento de entrada da engine.


## Exclude GUI {#exclude-gui}

Remove recursos, componentes e suporte Lua de GUI da engine. Ative esta opção somente se o projeto não usar cenas GUI ou scripts de GUI. Os componentes Label continuam disponíveis. Esta opção vem desativada por padrão.


## Exclude Particle FX {#exclude-particle-fx}

Remove recursos e componentes de efeitos de partículas e o módulo Lua `particlefx`. Isso também remove o suporte a nós de partículas em cenas GUI; cenas GUI sem nós de partículas continuam funcionando. Remova as referências a efeitos de partículas e as chamadas às suas APIs antes de ativar esta opção. Ela vem desativada por padrão.


## Exclude Tilemaps {#exclude-tilemaps}

Remove recursos e componentes de tilemap e o módulo Lua `tilemap`. Ative esta opção somente se o projeto não usar componentes de tilemap ou suas APIs. As tile sources usadas por outros componentes continuam disponíveis. Esta opção vem desativada por padrão.


## Excluir Live Update

Exclui a funcionalidade [Live Update](/manuals/live-update) da engine.


## Excluir Image

Exclui da engine o [módulo de script `image`](https://defold.com/ref/stable/image/).


## Excluir Types

Exclui da engine o [módulo de script `types`](https://defold.com/ref/stable/types/).


## Excluir Basis Transcoder

Exclui a biblioteca de compressão de textura [Basis Universal](/manuals/texture-profiles) da engine.


## Usar Android Support Lib

Usa a biblioteca Android Support Library obsoleta em vez do AndroidX. [Mais informações](https://defold.com/manuals/android/#using-androidx).


## Gráficos

Selecione quais backends gráficos incluir para cada plataforma. Uma opção combinada inclui os dois backends para que o backend preferencial possa recorrer ao outro quando não estiver disponível.

| Campo | Plataformas | Opções | Padrão |
|---|---|---|---|
| **Graphics** | Windows e Linux | OpenGL, Vulkan, OpenGL & Vulkan | OpenGL |
| **Graphics (macOS)** | macOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | Vulkan |
| **Graphics (iOS)** | iOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | OpenGL |
| **Graphics (Android)** | Android | OpenGL+Vulkan, OpenGL, Vulkan | OpenGL+Vulkan |
| **Graphics (HTML5)** | HTML5 | WebGL, WebGPU, WebGL & WebGPU | WebGL |

No Linux ARM64, a opção **OpenGL** usa o backend OpenGL ES. A opção combinada padrão do Android dá preferência ao Vulkan quando disponível e recorre ao OpenGL ES caso contrário.


## Usar sistema completo de layout de texto

Se ativado (`true`), inclui o sistema completo de layout de texto para modelagem de texto, incluindo idiomas escritos da direita para a esquerda. Ative esta opção junto com `font.runtime_generation` no *game.project* para usar a geração em tempo de execução de fontes SDF a partir de recursos TrueType (`.ttf`) ou OpenType (`.otf`). A geração em tempo de execução a partir de recursos `.otf` é compatível desde o Defold 1.13.2. Leia mais no [manual de fontes](/manuals/font/#enabling-runtime-fonts).


## Use Rich Text {#use-rich-text}

Inclui interpretação de texto formatado e efeitos de estilo para labels e texto de GUI. Esta opção vem ativada por padrão. Desative-a para reduzir o tamanho da engine quando o projeto precisar apenas de texto simples. Labels e texto de GUI continuam funcionando, mas a marcação é renderizada como texto simples em vez de aplicar formatação ou efeitos.


## Versões mínimas dos navegadores

Os campos YAML **`minSafariVersion`**, **`minFirefoxVersion`** e **`minChromeVersion`** especificam as versões mínimas dos navegadores usadas como alvo pelo Emscripten. Os padrões atuais e as versões mínimas compatíveis diferem entre os alvos com e sem threads:

| Alvo | Safari | Firefox | Chrome |
|---|---:|---:|---:|
| `wasm-web` | `101000` | `40` | `45` |
| `wasm_pthread-web` | `150000` | `79` | `75` |

Especifique as substituições no contexto do alvo relevante. O alvo com threads também tem [requisitos adicionais de hospedagem](/manuals/html5/#creating-html5-bundle). Consulte a referência de configurações do Emscripten para [`MIN_SAFARI_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-safari-version), [`MIN_FIREFOX_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-firefox-version) e [`MIN_CHROME_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-chrome-version).

## Memória inicial (HTML5)
Nome do campo YAML: **`initialMemory`**
Valor padrão: **33554432**

A quantidade inicial de memória alocada para a aplicação web, em bytes. O valor deve ser múltiplo do tamanho da página do WebAssembly (64 KiB). Consulte a configuração [`INITIAL_MEMORY`](https://emscripten.org/docs/tools_reference/settings_reference.html#initial-memory) do Emscripten.

Esta opção fornece o valor padrão durante a compilação. O valor de [`html5.heap_size`](/manuals/html5/#heap-size) no *game.project* o substitui em tempo de execução.

## Tamanho do stack (HTML5)
Nome do campo YAML: **`stackSize`**
Valor padrão: **5242880**

O tamanho do stack da aplicação, em bytes. Consulte a configuração [`STACK_SIZE`](https://emscripten.org/docs/tools_reference/settings_reference.html#stack-size) do Emscripten.
