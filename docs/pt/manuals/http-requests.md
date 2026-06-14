---
title: Requisições HTTP
brief: Este manual explica como fazer requisições HTTP.
---

## Requisições HTTP

O Defold pode fazer requisições HTTP normais usando a função `http.request()`.

### HTTP GET

Esta é a requisição mais básica para obter alguns dados do servidor. Exemplo:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

http.request("https://www.defold.com", "GET", handle_response)
```

Isso fará uma requisição HTTP GET para https://www.defold.com. A função é assíncrona e não bloqueará enquanto faz a requisição. Depois que a requisição for feita e um servidor enviar uma resposta, ela invocará/chamará a função de callback fornecida. A função de callback receberá a resposta completa do servidor, incluindo código de status e cabeçalhos de resposta. Veja abaixo informações adicionais sobre como trabalhar com a tabela de resposta.

::: sidenote
Requisições HTTP são armazenadas automaticamente em cache no cliente para melhorar o desempenho de rede. Os arquivos em cache são armazenados em um caminho de suporte de aplicação específico do sistema operacional, em uma pasta chamada `defold/http-cache`. Normalmente você não precisa se preocupar com o cache HTTP, mas se precisar limpar o cache durante o desenvolvimento, pode excluir manualmente a pasta que contém os arquivos em cache. No macOS, essa pasta fica em `%HOME%/Library/Application Support/Defold/http-cache/` e no Windows em `%APP_DATA%/defold/http-cache`.
:::

### HTTP POST

Ao enviar dados, como uma pontuação ou alguns dados de autenticação, para um servidor, isso normalmente é feito usando uma requisição POST:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

local body = "12345"
http.request("https://www.myserver.com/score", "POST", handle_response, nil, body)
```


### Outros métodos HTTP

As requisições HTTP do Defold também dão suporte aos métodos HEAD, DELETE e PUT. O método CONNECT também é compatível (veja a seção sobre conexões por proxy abaixo).

### Como trabalhar com a resposta HTTP

A tabela `response` retornada no callback contém todas as informações necessárias para implementar um tratamento granular da resposta. Dois dos campos principais são `status` e `response`:

```lua

local function handle_response(self, id, response)
	-- verifique o código de status da resposta. Códigos de resposta comuns:
	-- 200 OK - a requisição foi concluída com sucesso
	-- 301 Moved permanently - os dados solicitados foram movidos, veja o cabeçalho de redirecionamento
	-- 307 Temporary redirect - igual ao anterior
	-- 208 Permanent redirect - igual ao anterior
	-- 400 Bad Request - a requisição foi malformada
	-- 401 Unauthorized - o cliente precisa se autenticar
	-- 404 Not Found - o servidor não consegue encontrar as informações
	-- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
	if response.status == 200 then
		-- os dados da resposta
		-- isto pode ser qualquer coisa, desde texto simples, dados codificados em json ou dados binários
		print(response.response)
		json.decode(response.response)
		sys.save(..., response.response)
	end
end
```

Quando a resposta contém um grande bloco de dados binários, como uma imagem ou uma faixa de música, pode fazer sentido gravar os dados em um arquivo em vez de carregá-los na memória:

```lua
-- neste exemplo, baixamos myimage.png e o gravamos diretamente em um arquivo no disco

local options = {
	path = sys.get_save_file("mygame", "myimage.png")
}

local function handle_response(self, id, response)
	if response.status == 200 then
		print("File was successfully written to:", response.path)
		print("File size:", response.document_size)
		print("File path:", response.path)
	else
		print("File was not written to disk:", response.error)
	end
end

http.request("https://www.foobar.com/myimage.png", "GET", handle_response, nil, nil, options)
```

Outro caso de uso para carregar grandes quantidades de dados pela rede é o streaming de som, quando "chunks" de dados de som são carregados de uma URL e alimentam um recurso de som. Um exemplo completo pode ser encontrado no [manual de Sound Streaming](/sound-streaming#sound-streaming).


### Cabeçalhos de requisição

É possível definir cabeçalhos adicionais ao enviar uma requisição. Isso pode, por exemplo, ser usado para definir um cabeçalho `Authorization` ou `Content-Type` para informar ao servidor o formato dos dados.

```Lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

-- envie alguns dados de formulário
local headers = {
	["Content-Type"] = "application/x-www-form-urlencoded"
}
local body = "key1=value1&key2=value2"
http.request("https://www.myserver.com/post", "POST", handle_response, headers, body)

-- envie alguns dados codificados em json
local headers = {
	["Content-Type"] = "application/json"
}
local body = json.encode({ key1 = value1, key2 = value2 })
http.request("https://www.myserver.com/post", "POST", handle_response, headers, body)

-- solicite alguns dados que exigem autorização de acesso
local token = ... -- gere um token de acesso (JWT, OAuth etc)
local headers = {
	["Authorization"] = "Bearer " .. token
}
http.request("https://www.myserver.com/content", "GET", handle_response, headers)
```

O Defold definirá automaticamente alguns cabeçalhos de requisição:

* `If-None-Match: <etag>` será definido com o ETag de qualquer resposta previamente armazenada em cache.
* `Transfer-Encoding: chunked` será definido se o corpo da requisição for maior que 16384 bytes.
* `Content-Length` será definido com o tamanho do corpo da requisição (a menos que a requisição seja em chunks).
* `Range: bytes=<from>-<to>` será definido ao solicitar uma resposta parcial, por exemplo ao fazer [streaming de sons](/sound-streaming#sound-streaming).


### Cabeçalhos de resposta

A resposta do servidor pode conter um ou mais cabeçalhos de resposta. Eles ficam disponíveis na tabela `response`:

```lua
local function handle_response(self, id, response)
	for header,value in pairs(response.headers) do
		print(header, value)
	end
end

http.request("https://www.defold.com", "GET", handle_response)
```


### Proxy HTTP

Às vezes é desejável enviar uma requisição por meio de um servidor proxy. Isso pode ser feito especificando um servidor proxy a ser usado ao conectar ao servidor de destino. Quando um proxy é usado, a conexão com o servidor de destino é estabelecida usando um túnel HTTP pelo proxy. O túnel HTTP é estabelecido usando o método HTTP CONNECT. Exemplo:


```lua
-- conectar a www.defold.com via proxy localhost na porta 8888
local url = "https://www.defold.com:443"
local method = "GET"
local headers = {}
local post_data = nil
local options = {
	proxy = "https://127.0.0.1:8888"
}
http.request(url, method, function(self, id, response)
	pprint(response)
end, headers, post_data, options)
```

### Referência da API

Consulte a [referência da API](/ref/http/) para saber mais.

### Extensões

Uma implementação alternativa de requisições HTTP pode ser encontrada na [extensão TinyHTTP](https://defold.com/assets/tinyhttp/).
