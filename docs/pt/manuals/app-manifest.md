---
title: Manifesto do aplicativo
brief: Este manual descreve como o manifesto do aplicativo pode ser usado para excluir recursos da engine.
---

# Manifesto do aplicativo

O manifesto do aplicativo é usado para excluir ou controlar quais recursos incluir na engine. Excluir recursos não utilizados da engine é uma prática recomendada, pois diminuirá o tamanho final do binário do seu jogo.
Além disso, o manifesto do aplicativo contém algumas opções para controlar a compilação de código para a plataforma HTML5, como versão mínima do navegador suportada/configurações de memória que também podem afetar o tamanho do binário resultante.

![](images/app_manifest/create-app-manifest.png)

![](images/app_manifest/app-manifest.png)


# Aplicando o manifesto

Em `game.project`, atribua o manifesto a `Native Extensions` -> `App Manifest`.

## Física

Controla qual engine de física usar, ou selecione None para excluir a física completamente.

## Física 2D

Seleciona qual versão do Box2D usar.

## Rig + Modelo

Controla a funcionalidade de rig e modelo, ou selecione None para excluir modelo e rig completamente. (Veja a documentação de [`Model`](https://defold.com/manuals/model/#model-component)).


## Excluir Gravação

Exclui a capacidade de gravação de vídeo da engine (veja a documentação da mensagem [`start_record`](https://defold.com/ref/stable/sys/#start_record)).


## Excluir Profiler

Exclui o profiler da engine. O profiler é usado para coletar contadores de desempenho e uso. Aprenda a usar o profiler no [manual de Profiling](/manuals/profiling/).

## Excluir Som

Exclui todas as capacidades de reprodução de som da engine.


## Excluir Input

Exclui todo o tratamento de entrada da engine.


## Excluir Live Update

Exclui a funcionalidade [Live Update](/manuals/live-update) da engine.


## Excluir Image

Exclui da engine o [módulo de script `image`](https://defold.com/ref/stable/image/).


## Excluir Types

Exclui da engine o [módulo de script `types`](https://defold.com/ref/stable/types/).


## Excluir Basis Universal

Exclui a biblioteca de compressão de textura [Basis Universal](/manuals/texture-profiles) da engine.


## Usar Android Support Lib

Usa a biblioteca Android Support Library obsoleta em vez do AndroidX. [Mais informações](https://defold.com/manuals/android/#using-androidx).


## Gráficos

Seleciona qual backend de gráficos usar.

* OpenGL - Inclui apenas OpenGL.
* Vulkan - Inclui apenas Vulkan.
* OpenGL e Vulkan - Inclui tanto OpenGL quanto Vulkan. Vulkan será o padrão e voltará para OpenGL se Vulkan não estiver disponível.


## Usar sistema completo de layout de texto

Se ativado (`true`), permite usar geração em tempo de execução para fontes do tipo SDF ao usar fontes True Type (`.ttf`) no projeto. Leia mais detalhes no [Manual de fontes](https://defold.com/manuals/font/#enabling-runtime-fonts).


## Versão mínima do Safari (apenas js-web e wasm-web)
Nome do campo YAML: **`minSafariVersion`**
Valor padrão: **90000**

Versão mínima suportada do Safari. Não pode ser menor que 90000. Para mais informações, consulte as [opções do compilador Emscripten](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#min-safari-version).

## Versão mínima do Firefox (apenas js-web e wasm-web)
Nome do campo YAML: **`minFirefoxVersion`**
Valor padrão: **34**

Versão mínima suportada do Firefox. Não pode ser menor que 34. Para mais informações, consulte as [opções do compilador Emscripten](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#min-firefox-version).

## Versão mínima do Chrome (apenas js-web e wasm-web)
Nome do campo YAML: **`minChromeVersion`**
Valor padrão: **32**

Versão mínima suportada do Chrome. Não pode ser menor que 32. Para mais informações, consulte as [opções do compilador Emscripten](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#min-chrome-version).

## Memória inicial (apenas js-web e wasm-web)
Nome do campo YAML: **`initialMemory`**
Valor padrão: **33554432**

O tamanho da memória alocada para a aplicação web. Quando ALLOW_MEMORY_GROWTH=0 (js-web), esta é a quantidade total de memória que a aplicação web pode usar. Para mais informações, consulte a [documentação do Emscripten](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#initial-memory). Valor em bytes. Observe que o valor deve ser um múltiplo do tamanho da página WebAssembly (64KiB).
Essa opção se relaciona com `html5.heap_size` em *game.project*; consulte a [documentação de HTML5](https://defold.com/manuals/html5/#heap-size). A opção configurada pelo manifesto do aplicativo é definida durante a compilação e usada como valor padrão para a opção `INITIAL_MEMORY`. O valor de *game.project* substitui o valor do manifesto do aplicativo e é usado em tempo de execução.

## Tamanho do stack (apenas js-web e wasm-web)
Nome do campo YAML: **`stackSize`**
Valor padrão: **5242880**

O tamanho do stack da aplicação. Para mais informações, consulte a [documentação do Emscripten](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#stack-size). Valor em bytes.
