---
title: Streaming de som no Defold
brief: Este manual explica como fazer streaming de sons para a engine de jogos Defold
---

# Streaming de som

Embora o comportamento padrão seja carregar os dados de som por completo, também pode ser vantajoso carregar os dados em partes, antes de serem usados. Isso costuma ser chamado de "streaming".

Um benefício do streaming de som é que ele exige menos memória em tempo de execução. Outro é que, se você estiver transmitindo conteúdo de, por exemplo, uma url http, pode atualizar esse conteúdo a qualquer momento e também evitar o download inicial.

### Exemplo

Há um projeto de exemplo demonstrando essa configuração: [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming)

## Como ativar streaming de sons

### Forma fácil

A forma mais simples de usar streaming de som é ativar a configuração [`sound.stream_enabled`](https://defold.com/manuals/project-settings/#stream-enabled) em *game.project*. Quando essa opção é ativada, a engine começará a transmitir os sons.

Observação: se você tiver muitos arquivos de som carregados ao mesmo tempo, talvez precise aumentar o valor de `sound.stream_cache_size` (veja abaixo).

### Recursos em tempo de execução

Você também pode criar um novo recurso de dados de som e atribuí-lo a um componente de som.

Faça isso assim:
* Carregue a parte inicial dos dados do arquivo de som
    * Observação: este é o arquivo de som bruto, incluindo o cabeçalho ogg/wav
* Crie um novo recurso de dados de som chamando [`resource.create_sound_data()`](/ref/resource/#resource.create_sound_data).
* Atribua o novo recurso de dados de som ao componente de som usando [`go.set()`](/ref/go#go.set)

Aqui está um trecho do projeto de exemplo, usando `http.request()` para obter o arquivo de som inicial.

::: sidenote
O servidor web do qual você está carregando conteúdo precisa suportar [requisições HTTP range](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Range_requests).
:::

```lua
local function play_sound(self, hash)
    go.set(self.component, "sound", hash) -- sobrescreve os dados de recurso no componente
    sound.play(self.component)            -- começa a tocar o som
end

local function parse_range(s)
    local _, _, rstart, rend, size = string.find(s, "(%d+)-(%d+)/(%d+)") -- "bytes 0-16383/103277"
    return rstart, rend, size
end

-- Callback da resposta http.
local function http_result(self, _id, response, extra)
    if response.status == 200 or response.status == 206 then
        -- Requisição bem-sucedida
        local relative_path = self.filename
        local range = response.headers['content-range'] -- content-range = "bytes 0-16383/103277"
        local rstart, rend, filesize = parse_range(range)
        -- Cria o recurso Defold
        --   "partial" ativa o modo de streaming
        print("Creating resource", relative_path)
        local hash = resource.create_sound_data(relative_path, { data = response.response, filesize = filesize, partial = true })
        -- envia "play_sound" ao componente
        play_sound(self, hash)
    end
end

local function load_web_sound(base_url, relative_path)
    local url = base_url .. "/" .. relative_path
    local headers = {}
    headers['Range'] = string.format("bytes=%d-%d", 0, 16384-1)

    http.request(url, "GET", http_result, headers, nil, { ignore_cache = true })
end
```

## Provedores de recursos

Você pode usar outros meios para carregar o bloco inicial do arquivo de som. O ponto importante é lembrar que o restante dos blocos é carregado pelo sistema de recursos e seus provedores de recursos. Neste exemplo, adicionamos um novo provedor de arquivos (http) ao adicionar uma montagem de live update, chamando [liveupdate.add_mount()](/ref/liveupdate/#liveupdate.add_mount).

Você pode encontrar um exemplo funcional em [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming).

```lua
-- Veja http_result() no exemplo acima

local function load_web_sound(base_url, relative_path)
    local url = base_url .. "/" .. relative_path
    local headers = {}
    -- Solicita a parte inicial do arquivo
    headers['Range'] = string.format("bytes=%d-%d", 0, 16384-1)

    http.request(url, "GET", http_result, headers, nil, { ignore_cache = true })
end

function init(self)
    self.base_url = "http://my.server.com"
    self.filename = "/path/to/sound.ogg"

    liveupdate.add_mount("webmount", self.base_url, 100, function ()
                    -- quando a montagem estiver pronta, podemos iniciar a requisição para baixar o primeiro bloco
                    load_web_sound(self.base_url, self.filename)
                end)
end

function final(self)
    liveupdate.remove_mount("webmount")
end
```

## Cache de blocos de som

A quantidade de memória consumida pelos sons em tempo de execução é controlada pela configuração [`sound.stream_cache_size`](https://defold.com/manuals/project-settings/#stream-cache-size) em *game.project*. Dado esse limite, os dados de som carregados nunca excederão esse valor.

O bloco inicial de cada arquivo de som não pode ser removido e ocupará o cache enquanto os recursos estiverem carregados. O tamanho do bloco inicial é controlado pela configuração [`sound.stream_preload_size`](https://defold.com/manuals/project-settings/#stream-preload-size) em *game.project*.

Você também pode controlar o tamanho de cada bloco de som alterando a configuração [`sound.stream_chunk_size`](https://defold.com/manuals/project-settings/#stream-chunk-size) em *game.project*. Isso pode ajudar a reduzir ainda mais o tamanho do cache de som se você tiver muitos arquivos de som carregados ao mesmo tempo. Arquivos de som menores que o tamanho do bloco de som não são transmitidos e, se um novo bloco não couber no cache, o bloco mais antigo é removido

::: important
O tamanho total do cache de blocos de som deve ser maior que o número de arquivos de som carregados multiplicado pelo tamanho do bloco de streaming. Caso contrário, você corre o risco de remover novos blocos a cada frame e os sons não tocarão corretamente
:::
