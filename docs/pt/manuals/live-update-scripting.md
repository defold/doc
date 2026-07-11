---
title: Programando conteúdo Live Update
brief: Para usar o conteúdo live update, você precisa baixar e montar os dados no seu jogo. Aprenda como programar com live update neste manual.
---

# Programando Live Update

A API consiste apenas em algumas funções:

* `liveupdate.add_mount()`
* `liveupdate.remove_mount()`
* `liveupdate.get_mounts()`.

O fluxo recomendado é baixar e montar um arquivo Zip completo usando uma URI `zip:`.

## Obter mounts

`liveupdate.get_mounts()` retorna os mounts ativos na sessão atual. Cada entrada contém uma URI `mount.uri`, uma prioridade numérica `mount.priority` e um hash `mount.name`. Os mounts não são restaurados após reiniciar; a aplicação deve salvar as configurações necessárias e chamar `liveupdate.add_mount()` novamente.

Como `mount.name` é um hash, use-o como chave de tabela ou compare-o com `hash("name")`; não o concatene em um caminho. Mapeie cada hash de nome para um caminho de metadados exclusivo:

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

## Programando com proxies de coleção excluídos

Um proxy de coleção que foi excluído do empacotamento funciona como um proxy de coleção normal, com uma diferença importante. Enviar uma mensagem `load` enquanto ele ainda tiver recursos indisponíveis no armazenamento do pacote fará com que ele falhe.

No fluxo baseado em arquivos, você geralmente decide com antecedência de qual arquivo ou arquivos um proxy precisa e os monta antes de carregar. Se precisar inspecionar se um proxy tem conteúdo excluído, use `collectionproxy.get_resources()`.

Com *Strip Live Update Entries from Main Manifest* habilitado, que é o padrão ao publicar conteúdo Live Update baseado em arquivos:

* Se nenhum arquivo montado contiver o conteúdo excluído do proxy, `collectionproxy.get_resources("#proxy")` retorna uma tabela vazia `{}`.
* Depois que o arquivo relevante for montado, `collectionproxy.get_resources("#proxy")` retorna uma tabela não vazia de hashes de recursos para esse proxy, por exemplo:

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

        -- Com Strip Live Update Entries from Main Manifest habilitado, esta tabela
        -- fica vazia até que o arquivo relevante seja montado. Após a montagem, ela contém
        -- os hashes de recursos pertencentes ao proxy.
        if message.info and #proxy_resources == 0 and not has_mount(message.info.name) then
            msg.post("#", "download_archive", message) -- <6>
        else
            msg.post("#" .. message.level, "load")
        end

    elseif message_id == hash("download_archive") then
		local zip_filename = message.info.name .. ".zip"
		local download_path = sys.get_save_file("mygame", zip_filename)
        local url = self.http_url .. "/" .. zip_filename

        -- Faz a requisição. Você pode usar credenciais
        http.request(url, "GET", function(self, id, response) -- <7>
			if response.status == 200 or response.status == 304 then
				mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
					msg.post("#", "load_level", message) -- tenta carregar a fase novamente
				end)

			else
				print("Failed to download archive ", download_path, "from", url, ":", response.status)
			end
		end, nil, nil, {path=download_path})

    elseif message_id == hash("proxy_loaded") then -- a fase foi carregada, e podemos habilitá-la
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

1. `liveupdate.add_mount()` monta um único arquivo usando um nome, prioridade e arquivo zip especificados. Os dados ficam imediatamente disponíveis para carregamento (não é necessário reiniciar a engine).
O mount fica ativo apenas na sessão atual. Salve o caminho do pacote e as configurações do mount nos dados persistentes da aplicação e chame `liveupdate.add_mount()` novamente após cada reinicialização.
2. Você precisa armazenar o arquivo online (por exemplo, no S3), de onde poderá baixá-lo.
3. Dado o nome de um proxy de coleção, você precisa descobrir qual ou quais arquivos baixar e como montá-los
4. Na inicialização, tentamos carregar a fase.
5. Use `collectionproxy.get_resources()` para inspecionar o conteúdo excluído do proxy. Com a configuração padrão de manifesto reduzido habilitada, ela retorna `{}` até que o arquivo relevante seja montado, e uma tabela não vazia de hashes de recursos após a montagem.
6. Se o proxy usa conteúdo Live Update e o arquivo correspondente ainda não está montado, baixamos e montamos antes de carregar o proxy.
7. Faça uma requisição http e baixe o arquivo para `download_path`
8. Os dados foram baixados, e é hora de montá-los na engine em execução.


Com o código de carregamento no lugar, podemos testar a aplicação. No entanto, executá-la a partir do editor não baixará nada. Isso acontece porque Live Update é um recurso de pacote. Ao executar no ambiente do editor, nenhum recurso é excluído. Para garantir que tudo funcione bem, precisamos criar um pacote.
