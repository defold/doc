---
title: Programando conteúdo Live Update
brief: Para usar o conteúdo live update, você precisa baixar e montar os dados no seu jogo. Aprenda como programar com live update neste manual.
---

# Programando Live Update

O fluxo principal de montagem usa `liveupdate.add_mount()`, `liveupdate.remove_mount()` e `liveupdate.get_mounts()`. Consulte a [referência completa da API `liveupdate`](/ref/liveupdate/) para conhecer todas as funções disponíveis.

Use `liveupdate.is_built_with_excluded_files()` quando o código precisar identificar um pacote cujo manifesto de build espera conteúdo de Live Update excluído:

```lua
if liveupdate.is_built_with_excluded_files() then
    print("The bundle expects excluded Live Update content")
end
```

Essa função informa apenas os metadados do manifesto de build. Ela não significa que um arquivo está montado no momento nem que um recurso específico está disponível. Use `liveupdate.get_mounts()` para inspecionar mounts ativos e [`collectionproxy.get_resources()`](/ref/collectionproxy/#collectionproxy.get_resources) para inspecionar os hashes de recursos registrados no manifesto de um proxy de coleção.

O fluxo recomendado é baixar e montar um arquivo Zip completo usando uma URI `zip:`.

## Obter mounts

`liveupdate.get_mounts()` retorna os mounts ativos na sessão atual. Cada entrada contém uma string `uri`, uma prioridade numérica `priority` e um hash `name`. A lista também contém os mounts-base da engine, cujas prioridades são menores que zero e que não podem ser removidos.

Os mounts não são restaurados pela engine após uma reinicialização. Se a aplicação precisar usar conteúdo baixado anteriormente em uma sessão posterior, ela deverá persistir a URI, o nome e a prioridade do pacote em seus próprios dados salvos e chamar `liveupdate.add_mount()` novamente durante a inicialização.

Quando vários pacotes estão montados, é útil validar os metadados definidos pela aplicação. Como `mount.name` é um hash, use-o como chave de tabela ou compare-o com `hash("mount-name")`; não o concatene em um caminho de recurso. O exemplo a seguir mapeia cada hash de nome para um caminho de recurso de metadados exclusivo:

```lua
local function remove_old_mounts()
	local mounts = liveupdate.get_mounts() -- tabela com mounts
	local version_resources = {
		[hash("liveupdate")] = "/version_liveupdate.json",
	}

    -- Cada mount tem: mount.uri, mount.priority, mount.name
	for _,mount in ipairs(mounts) do

        -- Isto exige que o nome do arquivo seja único, para não obtermos um arquivo de outro arquivo compactado
        -- Estes dados são criados pelo desenvolvedor como forma de especificar metadados do arquivo
		local version_resource = version_resources[mount.name]
		local version_data = version_resource and sys.load_resource(version_resource)

		if version_data then
			version_data = json.decode(version_data)
		elseif mount.priority >= 0 then
			version_data = {version = 0} -- se não tiver arquivo de versão, provavelmente é um arquivo antigo/inválido
		end

        -- verifica a versão do arquivo contra a versão suportada pelo jogo
        if version_data and version_data.version < sys.get_config_int("game.minimum_lu_version") then
            -- era inválido, então vamos desmontá-lo!
            liveupdate.remove_mount(mount.name)
        end
	end
end
```

Use caminhos de metadados exclusivos para pacotes diferentes. A busca de recursos segue a prioridade dos mounts; portanto, usar o mesmo caminho em vários pacotes faria com que a cópia do mount de maior prioridade fosse lida.

## Programando com proxies de coleção excluídos

Um proxy de coleção que foi excluído do empacotamento funciona como um proxy de coleção normal, com uma diferença importante. Enviar uma mensagem `load` enquanto ele ainda tiver recursos indisponíveis no armazenamento do pacote fará com que ele falhe.

No fluxo baseado em arquivos, você geralmente decide com antecedência de qual arquivo ou arquivos um proxy precisa e os monta antes de carregar. Para inspecionar os hashes de recursos registrados no manifesto de um proxy excluído conhecido, use `collectionproxy.get_resources()`.

Depois que um pacote for montado, um proxy excluído e descarregado também pode ser redirecionado para outra coleção compilada com `collectionproxy.set_collection()`. Consulte [Alterando a coleção de um proxy excluído](/manuals/collection-proxy/#changing-an-excluded-proxys-collection) para conhecer as restrições e a sequência de carregamento.

Em um build baseado em arquivos que publica conteúdo Live Update, o manifesto principal empacotado omite as entradas de Live Update excluídas, enquanto o manifesto do pacote publicado as mantém. `collectionproxy.get_resources()` lê metadados de dependência do manifesto; ela não verifica se todos os blobs de dados referenciados estão disponíveis:

* Antes que um manifesto de pacote contendo as entradas excluídas do proxy seja montado, `collectionproxy.get_resources("#proxy")` retorna uma tabela vazia `{}`.
* Depois que o pacote relevante é montado, ela retorna uma tabela não vazia de hashes de recursos para esse proxy, por exemplo:

```lua
{
    "a1b2c3...",
    "d4e5f6...",
    "7890ab...",
    ...
}
```

 O código de exemplo a seguir pressupõe que os recursos estejam disponíveis pela url especificada na configuração `game.http_url`.

```lua

-- Você precisará acompanhar qual arquivo contém qual conteúdo
-- Neste exemplo, usamos apenas um único arquivo liveupdate, contendo todos os recursos ausentes.
-- Se você estiver usando múltiplos arquivos, precisa estruturar os downloads de acordo
local lu_infos = {
    liveupdate = {
        name = "liveupdate",
        priority = 10,
    }
}

local function get_lu_info_for_level(level_name)
    if level_name == "level1" then
        return lu_infos['liveupdate']
    end
end

local function mount_zip(self, name, priority, path, callback)
    liveupdate.add_mount(name, "zip:" .. path, priority, function(_self, _name, _uri, _result) -- <1>
        callback(_name, _uri, _result)
    end)
end

local function has_mount(name)
    local name_hash = hash(name)
    for _, mount in ipairs(liveupdate.get_mounts()) do
        if mount.name == name_hash then
            return true
        end
    end
    return false
end

function init(self)
    self.http_url = sys.get_config_string("game.http_url", nil) -- <2>

    local level_name = "level1"

    local info = get_lu_info_for_level(level_name) -- <3>

    msg.post("#", "load_level", {level = "level1", info = info }) -- <4>
end

function on_message(self, message_id, message, sender)
    if message_id == hash("load_level") then
        local proxy_resources = collectionproxy.get_resources("#" .. message.level) -- <5>

        -- Um build que publica conteúdo Live Update omite entradas excluídas do manifesto
        -- empacotado; portanto, esta tabela fica vazia até que o manifesto do pacote relevante
        -- seja montado. Após a montagem, ela contém os hashes de recursos do proxy.
        if message.info and #proxy_resources == 0 and not has_mount(message.info.name) then
            msg.post("#", "download_archive", message) -- <6>
        else
            msg.post("#" .. message.level, "load")
        end

    elseif message_id == hash("download_archive") then
        local zip_filename = message.info.name .. ".zip"
        local download_path = sys.get_save_file("mygame", zip_filename)
        local url = self.http_url .. "/" .. zip_filename

        -- Verifica se o arquivo já existe. Em caso afirmativo, tenta montá-lo!
        if sys.exists(download_path) then
            mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                if result == liveupdate.LIVEUPDATE_OK then
                    msg.post("#", "load_level", message) -- tenta carregar a fase novamente
                else
                    os.remove(download_path)             -- remove e tenta
                    msg.post("#", "load_level", message) -- baixar novamente
                end
            end)
        else
            -- Faz a requisição. Você pode usar credenciais
            http.request(url, "GET", function(self, id, response) -- <7>
                if response.status == 200 or response.status == 304 then
                    mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                        if result == liveupdate.LIVEUPDATE_OK then
                            msg.post("#", "load_level", message) -- tenta carregar a fase novamente
                        else
                            print("Failed to mount archive", download_path, ":", result)
                        end
                    end)
                else
                    print("Failed to download archive", download_path, "from", url, ":", response.status)
                end
            end, nil, nil, {path=download_path})
        end

    elseif message_id == hash("proxy_loaded") then -- a fase foi carregada, e podemos habilitá-la
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

1. `liveupdate.add_mount()` monta um único arquivo usando um nome, prioridade e arquivo zip especificados. Os dados ficam imediatamente disponíveis para carregamento (não é necessário reiniciar a engine). O mount fica ativo apenas na sessão atual. Salve o caminho do pacote e as configurações desejadas do mount nos dados persistentes da aplicação e chame `liveupdate.add_mount()` novamente após cada reinicialização.
2. Você precisa armazenar o arquivo online (por exemplo, no S3), de onde poderá baixá-lo.
3. Dado o nome de um proxy de coleção, você precisa descobrir qual ou quais arquivos baixar e como montá-los
4. Na inicialização, tentamos carregar a fase.
5. Neste fluxo de publicação baseado em arquivos, use `collectionproxy.get_resources()` para inspecionar os metadados do conteúdo excluído do proxy. Ela retorna `{}` até que o manifesto do pacote relevante seja montado, e uma tabela não vazia de hashes de recursos após a montagem. Esses hashes descrevem dependências; o resultado não verifica por si só se todos os blobs de dados estão disponíveis.
6. Se o proxy usa conteúdo Live Update e o arquivo correspondente ainda não está montado, baixamos e montamos antes de carregar o proxy.
7. Faça uma requisição http e baixe o arquivo para `download_path`
8. Os dados foram baixados, e é hora de montá-los na engine em execução.


Com o código de carregamento no lugar, podemos testar a aplicação. No entanto, executá-la a partir do editor não baixará nada. Isso acontece porque Live Update é um recurso de pacote. Ao executar no ambiente do editor, nenhum recurso é excluído. Para garantir que tudo funcione bem, precisamos criar um pacote.
