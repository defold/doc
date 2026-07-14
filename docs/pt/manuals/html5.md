---
title: Desenvolvimento Defold para a plataforma HTML5
brief: Este manual descreve o processo de criação de jogos HTML5, junto com problemas conhecidos e limitações.
---

# Desenvolvimento para HTML5

O Defold oferece suporte à criação de jogos para a plataforma HTML5 pelo menu normal de empacotamento, assim como para outras plataformas. Além disso, o jogo resultante é incorporado a uma página HTML comum, que pode ser estilizada por meio de um sistema simples de templates.

O arquivo *game.project* contém as configurações específicas de HTML5:

![Project settings](images/html5/html5_project_settings.png)

## Tamanho do heap {#heap-size}

O suporte do Defold a HTML5 é fornecido pelo Emscripten (veja http://en.wikipedia.org/wiki/Emscripten). Em resumo, ele cria uma área isolada de memória para o heap em que a aplicação opera. Por padrão, a engine aloca uma quantidade generosa de memória (256 MB). Isso deve ser mais que suficiente para um jogo típico. Como parte do seu processo de otimização, você pode optar por usar um valor menor. Para fazer isso, siga estes passos:

1. Defina *heap_size* para o valor desejado. Ele deve ser expresso em megabytes.
2. Crie seu pacote HTML5 (veja abaixo)

## Testando uma build HTML5

Para testes, uma build HTML5 precisa de um servidor HTTP. O Defold cria um para você se escolher <kbd>Projeto ▸ Compilar HTML5</kbd>.

![Build HTML5](images/html5/html5_build_launch.png)

Se você quiser testar seu pacote, basta enviá-lo para seu servidor HTTP remoto ou criar um servidor local, por exemplo usando python na pasta do pacote.
Python 2:

```sh
python -m SimpleHTTPServer
```

Python 3:

```sh
python -m http.server
```

ou

```sh
python3 -m http.server
```

::: important
Você não pode testar o pacote HTML5 abrindo o arquivo `index.html` em um navegador. Isso exige um servidor HTTP.
:::

::: important
Se você vir um erro `"wasm streaming compile failed: TypeError: Failed to execute ‘compile’ on ‘WebAssembly’: Incorrect response MIME type. Expected ‘application/wasm’."` no console, certifique-se de que seu servidor usa o tipo MIME `application/wasm` para arquivos `.wasm`.
:::

## Criando um pacote HTML5 {#creating-html5-bundle}

Criar conteúdo HTML5 com o Defold é simples e segue o mesmo padrão de todas as outras plataformas compatíveis: selecione <kbd>Projeto ▸ Empacotar... ▸ Aplicação HTML5...</kbd> no menu:

![Create HTML5 bundle](images/html5/html5_bundle.png)

Os pacotes HTML5 oferecem suporte a duas arquiteturas WebAssembly:

* `wasm-web` - a engine WebAssembly comum, sem threads.
* `wasm_pthread-web` - uma engine WebAssembly que pode usar threads.

Você pode incluir uma das arquiteturas ou ambas. Quando as duas são incluídas, o loader seleciona `wasm_pthread-web` se houver suporte no navegador e no ambiente de hospedagem; caso contrário, usa `wasm-web` como fallback. Consulte o [manual do Bob](/manuals/bob/#usage) para ver os nomes canônicos dos alvos.

::: important
A engine com threads requer `SharedArrayBuffer` em uma página segura e [isolada entre origens](https://developer.mozilla.org/en-US/docs/Web/API/Window/crossOriginIsolated). Sirva o pacote por HTTPS (ou localhost) e configure o servidor com cabeçalhos de isolamento entre origens compatíveis, normalmente:

```txt
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

Recursos de outras origens carregados pela página também devem usar cabeçalhos CORS ou Cross-Origin-Resource-Policy compatíveis. Um pacote que contenha apenas `wasm_pthread-web` não poderá ser executado se esses requisitos não forem atendidos; inclua `wasm-web` como fallback se o jogo puder ser hospedado em um site sem suporte ao isolamento entre origens.
:::

Os pacotes HTML5 do Defold exigem um navegador moderno com suporte a WebAssembly. O Internet Explorer 11 não é compatível.

Ao clicar no botão <kbd>Criar Pacote…</kbd>, você será solicitado a selecionar uma pasta onde a aplicação será criada. Depois que o processo de exportação terminar, você encontrará todos os arquivos necessários para executar a aplicação.

## Problemas conhecidos e limitações

* Hot Reload - Hot Reload não funciona em builds HTML5. Aplicações Defold precisam executar seu próprio mini servidor web para receber atualizações do editor, o que não é possível em uma build HTML5.
* Chrome
  * Builds de depuração lentas - Em builds de depuração no HTML5, verificamos todas as chamadas gráficas WebGL para detectar erros. Infelizmente, isso é muito lento ao testar no Chrome. É possível desativar isso definindo o campo *`Engine Arguments`* de *game.project* como `--verify-graphics-calls=false`.
* Suporte a gamepad - [Consulte a documentação de Gamepad](/manuals/input-gamepads/#gamepads-in-html5) para considerações especiais e passos que talvez você precise seguir no HTML5.

## Personalizando o pacote HTML5

Ao gerar uma versão HTML5 do seu jogo, o Defold fornece uma página web padrão. Ela referencia recursos de estilo e script que ditam como seu jogo é apresentado.

Cada vez que a aplicação é exportada, esse conteúdo é criado novamente. Se quiser personalizar qualquer um desses elementos, você precisa fazer modificações nas configurações do projeto. Para isso, abra o *game.project* no editor Defold e role até a seção *html5*:

![HTML5 Section](images/html5/html5_section.png)

Mais informações sobre cada opção estão disponíveis no [manual de configurações do projeto](/manuals/project-settings/#html5).

::: important
Você não pode modificar arquivos do template padrão html/css na pasta `builtins`. Para aplicar suas modificações, copie/cole o arquivo necessário de `builtins` e defina esse arquivo em *game.project*.
:::

::: important
O canvas não deve ser estilizado com borda ou padding. Se você fizer isso, as coordenadas de entrada do mouse ficarão incorretas.
:::

Em *game.project*, é possível desativar o botão `Fullscreen` e o link `Made with Defold`.
O Defold fornece um tema escuro e um claro para o `index.html`. O tema claro é definido por padrão, mas é possível alterá-lo mudando o arquivo `Custom CSS`. Também existem quatro modos de escala predefinidos para escolher no campo `Scale Mode`.

::: important
Os cálculos de todos os modos de escala incluem o DPI atual da tela caso você ative a opção `High Dpi` em *game.project* (seção `Display`)
:::

### Downscale Fit e Fit

No modo `Fit`, o tamanho do canvas será alterado para mostrar todo o canvas do jogo na tela com as proporções originais. A única diferença em `Downscale Fit` é que o tamanho só muda se o tamanho interno da página web for menor que o canvas original do jogo, mas ele não aumenta a escala quando a página web é maior que o canvas original do jogo.

![HTML5 Section](images/html5/html5_fit.png)

### Stretch

No modo `Stretch`, o tamanho do canvas será alterado para preencher completamente o tamanho interno da página web.

![HTML5 Section](images/html5/html5_stretch.png)

### No Scale
Com o modo `No Scale`, o tamanho do canvas é exatamente o mesmo que você predefiniu no arquivo *game.project*, seção `[display]`.

![HTML5 Section](images/html5/html5_no_scale.png)

## Tokens

Usamos a [linguagem de template Mustache](https://mustache.github.io/mustache.5.html) para criar o arquivo `index.html`. Quando você está compilando ou empacotando, os arquivos HTML e CSS passam por um compilador capaz de substituir certos tokens por valores que dependem das configurações do seu projeto. Esses tokens sempre ficam entre chaves duplas ou triplas (`{{TOKEN}}` ou `{{{TOKEN}}}`), dependendo de sequências de caracteres precisarem ser escapadas ou não. Esse recurso pode ser útil se você faz alterações frequentes nas configurações do projeto ou pretende que o material seja reutilizado em outros projetos.

::: sidenote
Mais informações sobre a linguagem de template Mustache estão disponíveis no [manual](https://mustache.github.io/mustache.5.html).
:::

Qualquer valor de *game.project* pode ser um token. Por exemplo, se você quiser usar o valor `Width` da seção `Display`:

![Display section](images/html5/html5_display.png)

Abra *game.project* como texto e confira `[section_name]` e o nome do campo que deseja usar. Então você pode usá-lo como um token: `{{section_name.field}}` ou `{{{section_name.field}}}`.

![Display section](images/html5/html5_game_project.png)

Por exemplo, em um template HTML em JavaScript:

```javascript
function doSomething() {
    var x = {{display.width}};
    // ...
}
```

Também temos os seguintes tokens personalizados:

DEFOLD_SPLASH_IMAGE
: Escreve o nome do arquivo da imagem de splash ou `false` se `html5.splash_image` em *game.project* estiver vazio


```css
{{#DEFOLD_SPLASH_IMAGE}}
		background-image: url("{{DEFOLD_SPLASH_IMAGE}}");
{{/DEFOLD_SPLASH_IMAGE}}
```

exe-name
: O nome do projeto sem símbolos não aceitos


DEFOLD_CUSTOM_CSS_INLINE
: Este é o local em que inserimos inline o conteúdo do arquivo CSS especificado nas configurações do seu *game.project*.


```html
<style>
{{{DEFOLD_CUSTOM_CSS_INLINE}}}
</style>
```

::: important
É importante que este bloco inline apareça antes de o script principal da aplicação ser carregado. Como ele inclui tags HTML, essa macro deve aparecer entre chaves triplas `{{{TOKEN}}}` para impedir que sequências de caracteres sejam escapadas.
:::

DEFOLD_SCALE_MODE_IS_DOWNSCALE_FIT
: Este token é `true` se `html5.scale_mode` for `Downscale Fit`.

DEFOLD_SCALE_MODE_IS_FIT
: Este token é `true` se `html5.scale_mode` for `Fit`.

DEFOLD_SCALE_MODE_IS_NO_SCALE
: Este token é `true` se `html5.scale_mode` for `No Scale`.

DEFOLD_SCALE_MODE_IS_STRETCH
: Este token é `true` se `html5.scale_mode` for `Stretch`.

DEFOLD_HEAP_SIZE
: Tamanho do heap especificado em *game.project* `html5.heap_size`, convertido para bytes.

DEFOLD_ENGINE_ARGUMENTS
: Argumentos da engine especificados em *game.project* `html5.engine_arguments`, separados pelo símbolo `,`.

build-timestamp
: Timestamp da build atual em segundos.


## Parâmetros extras

Se você criar um template personalizado, poderá alterar os parâmetros do carregador da engine atribuindo valores ao objeto global `CUSTOM_PARAMETERS`. O template integrado fornece um bloco `<script id="engine-setup">` intencionalmente vazio para essas personalizações.
::: important
Mantenha o bloco `engine-setup` depois do script que carrega `dmloader.js` e antes do bloco `engine-start` que chama `EngineLoader.load()`.
:::
Por exemplo:

```html
    <script id="engine-setup" type="text/javascript">
        CUSTOM_PARAMETERS.disable_context_menu = false;
        CUSTOM_PARAMETERS.unsupported_webgl_callback = function() {
            console.log("Oh-oh. WebGL not supported...");
        };
    </script>
```

`CUSTOM_PARAMETERS` pode conter campos como:

```
'archive_location_filter':
    Função de filtro que será executada para cada caminho de arquivo.

'unsupported_webgl_callback':
    Função chamada se WebGL não tiver suporte.

'engine_arguments':
    Lista de argumentos (strings) que serão passados para a engine.

'custom_heap_size':
    Número de bytes que especifica o tamanho do heap de memória.

'disable_context_menu':
    Desativa o menu de contexto do clique direito no elemento canvas se true.

'retry_time':
    Pausa em segundos antes de tentar carregar o arquivo novamente após erro.

'retry_count':
    Quantas tentativas fazemos ao tentar baixar um arquivo.

'can_not_download_file_callback':
    Função chamada se você não conseguir baixar o arquivo após as tentativas de 'retry_count'.

'resize_window_callback':
    Função chamada quando eventos de resize/orientationchanges/focus acontecerem

'start_success':
    Função chamada pouco antes de main ser chamada após um carregamento bem-sucedido.

'update_progress':
    Função chamada à medida que o progresso é atualizado. O parâmetro progress é atualizado de 0 a 100.
```

## Operações de arquivo em HTML5

Builds HTML5 oferecem suporte a operações de arquivo como `sys.save()`, `sys.load()` e `io.open()`, mas a forma como essas operações são tratadas internamente é diferente de outras plataformas. Quando JavaScript roda em um navegador, não existe um conceito real de sistema de arquivos, e o acesso a arquivos locais é bloqueado por motivos de segurança. Em vez disso, o Emscripten (e portanto o Defold) usa [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB), um banco de dados dentro do navegador usado para armazenar dados de forma persistente, para criar um sistema de arquivos virtual no navegador. A diferença importante em relação ao acesso ao sistema de arquivos em outras plataformas é que pode haver um pequeno atraso entre gravar em um arquivo e a alteração ser realmente armazenada no banco de dados. O console de desenvolvedor do navegador geralmente permite inspecionar o conteúdo do IndexedDB.


## Passando argumentos para um jogo HTML5

Às vezes é necessário fornecer argumentos adicionais a um jogo antes dele iniciar ou enquanto ele é iniciado. Isso pode ser, por exemplo, um id de usuário, token de sessão ou qual fase carregar quando o jogo começa. Isso pode ser feito de várias formas diferentes, algumas delas descritas aqui.

### Argumentos da engine

É possível especificar argumentos adicionais da engine quando ela é configurada e carregada. Esses argumentos extras podem ser recuperados em tempo de execução usando `sys.get_config_string()`. Atribua os argumentos diretamente a `CUSTOM_PARAMETERS.engine_arguments` no bloco `engine-setup` de `index.html`:

```html
    <script id="engine-setup" type="text/javascript">
        CUSTOM_PARAMETERS.engine_arguments = [
            "--config=example.foo1=bar1",
            "--config=example.foo2=bar2"
        ];
    </script>
```

A atribuição de um novo array substitui qualquer argumento da engine configurado em *game.project*. Para preservar esses argumentos e adicionar outro, use `CUSTOM_PARAMETERS.engine_arguments.push("--config=example.foo3=bar3")`.

Você também pode adicionar `--config=example.foo1=bar1, --config=example.foo2=bar2` ao campo *Engine Arguments* na seção HTML5 de *game.project*. Os valores separados por vírgulas são adicionados a `CUSTOM_PARAMETERS.engine_arguments` no arquivo `dmloader.js` gerado.

Em tempo de execução, você obtém os valores assim:

```lua
local foo1 = sys.get_config_string("example.foo1")
local foo2 = sys.get_config_string("example.foo2")
print(foo1) -- bar1
print(foo2) -- bar2
```


### Argumentos de query na URL

Você pode passar argumentos como parte dos parâmetros de query na URL da página e lê-los em tempo de execução:

```
https://www.mygame.com/index.html?foo1=bar1&foo2=bar2
```

```lua
local url = html5.run("window.location")
print(url)
```

Uma função auxiliar completa para obter todos os parâmetros de query como uma tabela Lua:

```lua
local function get_query_parameters()
    local url = html5.run("window.location")
    -- obtém a parte de query da url (a parte depois de ?)
    local query = url:match(".*?(.*)")
    if not query then
        return {}
    end

    local params = {}
    -- itera por todos os pares chave-valor
    for kvp in query:gmatch("([^&]+)") do
        local key, value = kvp:match("(.+)=(.+)")
        params[key] = value
    end
    return params
end

function init(self)
    local params = get_query_parameters()
    print(params.foo1) -- bar1
end
```

## Otimizações
Jogos HTML5 geralmente têm requisitos rígidos de tamanho inicial de download, tempo de inicialização e uso de memória para garantir que carreguem rápido e rodem bem em dispositivos mais simples e conexões de internet lentas. Para otimizar um jogo HTML5, recomenda-se focar nas seguintes áreas:

* [Uso de memória](/manuals/optimization-memory)
* [Tamanho da engine](/manuals/optimization-size)
* [Tamanho do jogo](/manuals/optimization-size)

## FAQ
:[HTML5 FAQ](../shared/html5-faq.md)
