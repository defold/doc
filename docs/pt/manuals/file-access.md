---
title: Trabalhando com arquivos
brief: Este manual explica como salvar e carregar arquivos e realizar outros tipos de operações de arquivo.
---

# Trabalhando com arquivos
Há muitas formas diferentes de criar e/ou acessar arquivos. Os caminhos de arquivo e as formas de acessar esses arquivos variam dependendo do tipo de arquivo e de sua localização.

## Funções para acesso a arquivos e pastas
O Defold fornece várias funções diferentes para trabalhar com arquivos:

* Você pode usar as funções padrão [`io.*`](https://defold.com/ref/stable/io/) para ler e escrever arquivos. Essas funções oferecem controle muito detalhado sobre todo o processo de I/O.

```lua
-- abre myfile.txt para escrita em modo binário
-- retorna nil mais uma mensagem de erro em caso de falha
local f, err = io.open("path/to/myfile.txt", "wb")
if not f then
	print("Something went wrong while opening the file", err)
	return
end

-- escreve no arquivo, faz flush para o disco e então fecha o arquivo
f:write("Foobar")
f:flush()
f:close()

-- abre myfile.txt para leitura em modo binário
-- retorna nil mais uma mensagem de erro em caso de falha
local f, err = io.open("path/to/myfile.txt", "rb")
if not f then
	print("Something went wrong while opening the file", err)
	return
end

-- lê o arquivo inteiro como uma string
-- retorna nil em caso de falha
local s = f:read("*a")
if not s then
	print("Error while reading file")
	return
end

print(s) -- Foobar
```

* Você pode usar [`os.rename()`](https://defold.com/ref/stable/os/#os.rename:oldname-newname) e [`os.remove()`](https://defold.com/ref/stable/os/#os.remove:filename) para renomear e remover arquivos.

* Você pode usar [`sys.save()`](https://defold.com/ref/stable/sys/#sys.save:filename-table) e [`sys.load()`](https://defold.com/ref/stable/sys/#sys.load:filename) para ler e escrever tabelas Lua. Funções adicionais [`sys.*`](https://defold.com/ref/stable/sys/) existem para ajudar na resolução de caminhos de arquivo independente de plataforma.

```lua
-- obtém um caminho independente de plataforma para o arquivo "highscore" da aplicação "mygame"
local path = sys.get_save_file("mygame", "highscore")

-- salva uma tabela Lua com alguns dados
local ok = sys.save(path, { highscore = 100 })
if not ok then
	print("Failed to save", path)
	return
end

-- carrega os dados
local data = sys.load(path)
print(data.highscore) -- 100
```


## Localizações de arquivos e pastas
Localizações de arquivos e pastas podem ser divididas em três categorias:

* Arquivos específicos da aplicação criados pela sua aplicação
* Arquivos e pastas empacotados com sua aplicação
* Arquivos específicos do sistema acessados pela sua aplicação

### Como salvar e carregar arquivos específicos da aplicação
Ao salvar e carregar arquivos específicos da aplicação, como recordes, configurações do usuário e estado do jogo, recomenda-se usar uma localização fornecida pelo sistema operacional e destinada especificamente a essa finalidade. Você pode usar [`sys.get_save_file()`](https://defold.com/ref/stable/sys/#sys.get_save_file:application_id-file_name) para obter o caminho absoluto específico do sistema operacional para um arquivo. Depois de ter o caminho absoluto, você pode usar as funções `sys.*`, `io.*` e `os.*` (veja acima).

[Veja o exemplo que mostra como usar `sys.save()` e `sys.load()`](/examples/file/sys_save_load/).

### Como acessar arquivos empacotados com a aplicação {#how-to-access-files-bundled-with-the-application}
Você pode incluir arquivos com sua aplicação usando bundle resources e custom resources.

#### Custom Resources
:[Custom Resources](../shared/custom-resources.md)

```lua
-- Carrega dados de nível em uma string
local data, error = sys.load_resource("/assets/level_data.json")
-- Decodifica a string json para uma tabela Lua
if data then
  local data_table = json.decode(data)
  pprint(data_table)
else
  print(error)
end
```

#### Bundle Resources
:[Bundle Resources](../shared/bundle-resources.md)

```lua
local path = sys.get_application_path()
local f = io.open(path .. "/mycommonfile.txt", "rb")
local txt, err = f:read("*a")
if not txt then
	print(err)
	return
end
print(txt)
```

::: sidenote
Por motivos de segurança, navegadores (e, por extensão, qualquer JavaScript executado em um navegador) são impedidos de acessar arquivos do sistema. Operações de arquivo em builds HTML5 no Defold ainda funcionam, mas apenas em um "sistema de arquivos virtual" usando a API IndexedDB no navegador. Isso significa que não há como acessar bundle resources usando funções `io.*` ou `os.*`. No entanto, você pode acessar bundle resources usando `http.request()`.
:::


#### Recursos Custom e Bundle - comparação

| Característica              | Custom Resources                          | Bundle Resources                               |
|-----------------------------|-------------------------------------------|------------------------------------------------|
| Velocidade de carregamento  | Mais rápida - arquivos carregados do arquivo binário | Mais lenta - arquivos carregados do sistema de arquivos |
| Carregar arquivos parciais  | Não - apenas arquivos inteiros            | Sim - ler bytes arbitrários do arquivo         |
| Modificar arquivos após empacotar | Não - arquivos armazenados dentro de um arquivo binário | Sim - arquivos armazenados no sistema de arquivos local |
| Suporte a HTML5             | Sim                                       | Sim - mas acesso via http, não I/O de arquivo  |


### Acesso a arquivos do sistema
O acesso a arquivos do sistema pode ser restrito pelo sistema operacional por motivos de segurança. Você pode usar a extensão nativa [`extension-directories`](https://defold.com/assets/extensiondirectories/) para obter o caminho absoluto de alguns diretórios comuns do sistema (por exemplo, `documents`, `resource`, `temp`). Depois de ter o caminho absoluto desses arquivos, você pode usar as funções `io.*` e `os.*` para acessá-los (veja acima).

::: sidenote
Por motivos de segurança, navegadores (e, por extensão, qualquer JavaScript executado em um navegador) são impedidos de acessar arquivos do sistema. Operações de arquivo em builds HTML5 no Defold ainda funcionam, mas apenas em um "sistema de arquivos virtual" usando a API IndexedDB no navegador. Isso significa que não há como acessar arquivos do sistema em builds HTML5.
:::

## Extensões
O [Portal de Assets](https://defold.com/assets/) contém vários assets para simplificar o acesso a arquivos e pastas. Alguns exemplos:

* [Lua File System (LFS)](https://defold.com/assets/luafilesystemlfs/) - Funções para trabalhar com diretórios, permissões de arquivo etc.
* [DefSave](https://defold.com/assets/defsave/) - Um módulo para ajudar você a salvar/carregar configurações e dados do jogador entre sessões.
