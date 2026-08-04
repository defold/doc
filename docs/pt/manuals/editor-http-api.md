---
title: Automação do editor Defold com HTTP
brief: Este manual explica como ferramentas externas podem descobrir e usar a API HTTP local de um projeto aberto no editor Defold.
---

# Automação do editor Defold {#automating-the-defold-editor}

O editor Defold abre um servidor especial para ações automatizadas. A API HTTP controla o projeto aberto. Use-a para comandos do editor, builds, recursos do projeto, pré-visualizações, preferências, saída do console, busca na documentação ou integrações de scripts do editor. Para inspecionar ou controlar o jogo em execução, use o [serviço do engine ou uma API de automação em tempo de execução](/manuals/engine-service).

::: important
A API HTTP do editor é experimental e pode mudar entre versões do Defold. O documento `/openapi.json` gerado pelo editor em execução é a fonte da verdade sobre as operações e os esquemas disponíveis.
:::

## Inicialização do editor por uma ferramenta externa {#starting-the-editor-from-an-external-tool}

Uma ferramenta externa precisa do arquivo executável do editor e do caminho absoluto para o arquivo `game.project` do projeto.

As versões instaladas do Defold podem ser localizadas por meio de `installations.json`, conforme descrito no [manual do editor](/manuals/editor/#editor-installation-metadata). Seu campo `launcherPath` contém o executável a ser iniciado. Passe o caminho de `game.project` como o primeiro argumento posicional para abrir esse projeto diretamente.

O argumento opcional `--port` ou `-p` seleciona a porta do servidor do editor. Omiti-lo permite que o Defold escolha uma porta disponível e geralmente é preferível quando vários projetos podem estar abertos.

```sh
# Linux
/path/to/Defold/Defold --port 8181 /absolute/path/to/project/game.project
```

```sh
# macOS
/path/to/Defold.app/Contents/MacOS/Defold --port 8181 /absolute/path/to/project/game.project
```

```powershell
# Windows
C:\path\to\Defold\Defold.exe --port 8181 C:\absolute\path\to\project\game.project
```

O editor é uma aplicação gráfica para desktop. Inicie-o em uma sessão interativa do usuário com acesso ao display. Use o [Bob](/manuals/bob) quando uma sessão gráfica não estiver disponível, como em CI headless, ou para automação apenas de compilação e criação de pacotes autônomos.

Depois de iniciar o editor, aguarde até que o projeto tenha sido aberto e `.internal/editor.port` exista. Então, consulte `/openapi.json` até que ele retorne um documento válido. Não presuma que a criação do processo significa que o projeto está pronto.

## Localização do servidor do editor {#locating-the-editor-server}

O editor inicia um servidor HTTP local enquanto um projeto está aberto. Selecione <kbd>Ajuda ▸ Abrir Servidor do Editor</kbd> para abrir a página inicial no navegador padrão:

![A página inicial do servidor local do editor](images/automation/editor_server.png)

A porta selecionada é gravada dentro do projeto em:

```text
.internal/editor.port
```

Daqui em diante, os exemplos e comandos deste manual se referem a estas variáveis do shell:

```sh
PORT="$(cat .internal/editor.port)"
BASE_URL="http://127.0.0.1:$PORT"
```

O arquivo da porta pertence à sessão atual do editor. Leia-o novamente depois de reiniciar o editor.

::: important
O servidor do editor é uma interface local confiável de controle. Não o exponha por meio de um endereço público, redirecionamento de porta ou túnel não confiável.
:::

## Descoberta de operações por meio de OpenAPI {#discovering-operations-through-openapi}

As únicas informações de inicialização específicas do Defold de que uma ferramenta externa deve precisar são a porta do editor e o documento OpenAPI:

```sh
curl -sS "http://127.0.0.1:$(cat .internal/editor.port)/openapi.json"
```

O documento OpenAPI 3.0.3 retornado descreve as operações compatíveis com a versão do editor em execução, incluindo caminhos, métodos, parâmetros, nomes de comandos, formatos de solicitação, respostas, códigos de status e requisitos de autenticação.

Liste os caminhos documentados:

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '.paths | keys[]'
```

Liste os comandos disponíveis do editor:

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '
    .paths["/command/{command}"].post.parameters[]
    | select(.name == "command")
    | .schema.enum[]
  '
```

Uma integração ciente da versão deve verificar cada operação necessária e configurar as solicitações com base no esquema retornado. Não recomendamos manter uma cópia supostamente completa dos nomes de endpoints ou comandos, pois ela pode ficar desatualizada.

Rotas definidas pelo projeto também aparecem em `/openapi.json` quando seus scripts do editor fornecem uma descrição de operação OpenAPI.

## Execução de comandos do editor {#executing-editor-commands}

Os comandos do editor são chamados por meio de:

```text
POST /command/{command}
```

Por exemplo, o comando atual `build` compila e executa o projeto:

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/build" |
  jq
```

Um build bem-sucedido retorna um resultado estruturado:

```json
{
  "success": true,
  "issues": []
}
```

Um build com falha retorna o status HTTP `422` com problemas como:

```json
{
  "success": false,
  "issues": [
    {
      "message": "Example compiler message",
      "severity": "error",
      "resource": "/main/player.script",
      "range": {
        "start": {
          "line": 12,
          "character": 4
        },
        "end": {
          "line": 12,
          "character": 17
        }
      }
    }
  ]
}
```

Os campos disponíveis dependem do erro. Use o caminho do recurso e o intervalo do código-fonte quando estiverem presentes, mas também trate problemas que contenham apenas uma mensagem.

Comandos normalmente úteis, quando listados pelo editor em execução, incluem:

`build`
: Compila e executa o projeto.

`clean-build`
: Limpa o cache de build e depois compila e executa. Use esse comando apenas quando um build comum se comportar de maneira inconsistente ou parecer ignorar alterações.

`build-html5`
: Compila o projeto para HTML5 e disponibiliza a saída por meio do servidor do editor.

`fetch-libraries`
: Baixa e recarrega as dependências do projeto.

`hot-reload`
: Recarrega recursos modificados em um jogo em execução.

`reload-extensions`
: Recarrega scripts do editor.

`debugger-start`, `debugger-stop` e os comandos de passo do depurador
: Controlam uma sessão de depuração e o projeto em execução.

Os nomes exatos e a disponibilidade dependem da versão e do estado atual do editor; descubra-os em `/openapi.json`.

Os comandos que operam nos recursos do projeto sincronizam as alterações externas nos arquivos antes da execução.

### Respostas de comandos e trabalho assíncrono {#command-responses-and-asynchronous-work}

A operação de comando documenta os códigos de resposta no esquema OpenAPI atual.

| Status | Significado |
| --- | --- |
| `200` | O comando foi concluído e retornou um resultado |
| `202` | O comando foi aceito e continua de forma assíncrona |
| `403` | O comando não está ativo no estado atual do editor |
| `404` | O comando não está disponível |
| `422` | O build ou a validação falhou |
| `500` | Ocorreu um erro interno do editor |

Uma resposta HTTP `202` não comprova que o resultado solicitado existe. Aguarde a saída, o recurso, o marcador do console ou a URL servida relevante e aplique um tempo limite.

### Build para HTML5 {#building-html5}

Se o documento OpenAPI atual listar `build-html5`, chame-o por meio da operação de comando:

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/build-html5"
```

O comando é executado de forma assíncrona e normalmente retorna HTTP `202`. Após a conclusão do build, o editor o disponibiliza em:

```text
http://127.0.0.1:<editor-port>/html5/
```

Aguarde até que a URL esteja disponível antes de iniciar os testes de navegador. Consulte [Testes em navegador para HTML5](/manuals/automated-testing/#browser-tests-for-html5) para obter mais detalhes.

## Busca na documentação de API {#searching-api-documentation}

Quando presente em `/openapi.json`, a operação `/ref` pesquisa a documentação de API incluída na versão do editor em execução. Ela fornece nomes e assinaturas que correspondem a essa versão.

Por exemplo, para pesquisar uma função, use:

```sh
curl -sS \
  --get \
  --data-urlencode "q=go.animate" \
  "$BASE_URL/ref" |
  jq
```

Filtre por ambiente e linguagem:

```sh
curl -sS \
  --get \
  --data-urlencode "environment=runtime" \
  --data-urlencode "language=Lua" \
  --data-urlencode "q=collision message|raycast" \
  "$BASE_URL/ref" |
  jq
```

Os parâmetros de busca são:

`environment`
: `editor`, `runtime` ou valores separados por vírgula.

`language`
: `Lua`, `C`, `C++` ou valores separados por vírgula.

`q`
: Uma expressão que não diferencia maiúsculas e minúsculas. Espaços em branco representam AND, enquanto `|` representa OR.

Também existem recursos de documentação condensada: o [índice de documentação para LLMs](https://defold.com/llms.txt) contém links para manuais oficiais, namespaces de API e exemplos, e a [documentação completa para LLMs](https://defold.com/llms-full.txt) apresenta a documentação completa para permitir busca offline e indexação local.

No entanto, os agentes de IA devem preferir buscas específicas em vez de recuperar uma referência inteira quando apenas uma API ou mensagem for necessária, para economizar tokens e ter um contexto mais bem preparado e limpo para determinada tarefa.

## Leitura da saída do console {#reading-console-output}

Leia o console do editor como JSON:

```sh
curl -sS "$BASE_URL/console" | jq
```

A resposta contém o texto do console em `lines` e regiões semânticas em `regions`, incluindo erros, resultados de avaliação e referências a recursos.

Para acompanhar continuamente a saída do console, use:

```sh
curl -N "$BASE_URL/console/stream"
```

O stream inclui as linhas atuais do console e então permanece aberto para novas saídas. Feche-o após receber um marcador de conclusão ou erro, detectar o encerramento do processo ou atingir um tempo limite ou limite de linhas.

Para enquadramento de resultados de teste e classificação de falhas, consulte [Testes automatizados e verificação](/manuals/automated-testing/#structured-test-results).

## Renderização de pré-visualizações de cenas {#rendering-scene-previews}

O editor Defold (desde a versão 1.13.1) pode renderizar uma "captura de tela" de um recurso de cena compatível como PNG por meio do comando `/preview/{path}`:

```sh
mkdir -p build/automation

curl -sS \
  "$BASE_URL/preview/main/main.collection?width=1280&height=720" \
  --output build/automation/main-preview.png
```

Isso renderiza a coleção principal do projeto aberto do modelo Basic 3D em uma visualização inicial padrão:

![Uma pré-visualização da coleção principal renderizada pelo editor](images/automation/main-preview.png)

Você pode usar a renderização para obter pré-visualizações de recursos que utilizam o editor visual de cenas. Por exemplo, é possível renderizar um componente de modelo da mesma maneira, o que permite verificar sua aparência ou, por exemplo, a correção do shader:

```sh
curl -sS \
  "$BASE_URL/preview/assets/models/cube.model?width=1280&height=720" \
  --output build/automation/cube-preview.png
```

![Uma pré-visualização do modelo de cubo renderizada pelo editor](images/automation/cube-preview.png)

O caminho após `/preview/` não inclui uma barra inicial. Por padrão, as dimensões opcionais usam o tamanho de display do projeto e devem estar entre `1` e `4096`.

| Status | Significado |
| --- | --- |
| `200` | A pré-visualização foi renderizada |
| `400` | As dimensões são inválidas |
| `404` | O recurso não foi encontrado |
| `422` | O recurso não está carregado ou não oferece suporte a pré-visualizações de cena |

As pré-visualizações podem ser muito úteis para a análise visual do projeto: verificação de layouts de níveis e GUI, configuração de shaders e iluminação, regressões visuais ou criação de miniaturas para a documentação.

::: important
Uma pré-visualização do editor não é uma captura de tela do jogo em execução. Ela não verifica objetos criados dinamicamente, pós-processamento em tempo de execução nem renderização específica da plataforma. Use uma [captura de tela em tempo de execução](/manuals/automated-testing/#editor-previews-and-runtime-screenshots) quando esses elementos forem necessários.
:::

## Execução de Lua no editor {#executing-editor-lua}

A operação autenticada `POST /eval` executa Lua no ambiente de extensões do editor. O bearer token de cada sessão é armazenado em:

```text
.internal/editor.token
```

Leia o token e execute o código:

```sh
TOKEN="$(cat .internal/editor.token)"

curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary 'print(editor.version) return editor.platform' \
  "$BASE_URL/eval"
```

A saída impressa e os valores retornados são devolvidos como texto. As respostas típicas são:

| Status | Significado |
| --- | --- |
| `200` | O código foi executado |
| `401` | O bearer token está ausente ou é inválido |
| `422` | O código Lua não pôde ser analisado ou executado |
| `503` | O ambiente de extensões do editor não está pronto |

Um cliente pode tentar novamente após `503`, mas deve usar um número limitado de tentativas. Corrija o código antes de repetir uma solicitação que retornou `422`.

O código avaliado pode usar a [API do editor](https://defold.com/ref/editor-lua/) e o ambiente de scripts do editor. Ele não pode usar APIs de tempo de execução do jogo, como `go.*`, para manipular um jogo em execução. Use um teste de tempo de execução, depurador, teste em navegador ou uma [API de automação em tempo de execução](/manuals/engine-service/#automation-bridge-extension) para a jogabilidade.

### Modificação de recursos e arquivos {#modifying-resources-and-files}

Muitos recursos de código-fonte do Defold usam formatos de texto e podem ser editados com qualquer ferramenta de edição de texto. Para modificar recursos estruturados do projeto Defold, prefira transações do editor.

| Alteração | Método preferido |
| --- | --- |
| Lua, shader, JSON ou outro formato de texto conhecido | Modificação direta do arquivo |
| Texto não salvo em uma aba aberta do editor | `editor.get()` e `editor.transact()` |
| Coleção, objeto de jogo, GUI, atlas ou outro recurso estruturado | Transação do editor |
| Conteúdo gerado repetidamente | Gerador autônomo |
| Operação de projeto repetível | Comando do editor ou endpoint HTTP personalizado |
| Transformação exclusiva de CI | Script autônomo executado antes do Bob |

Inspecione um recurso antes de alterá-lo:

```sh
curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary '
    local path = "/game.project"
    pprint(editor.properties(path))
    return editor.get(path, "path")
  ' \
  "$BASE_URL/eval"
```

Verifique `editor.can_get()`, `editor.can_set()` e as outras funções `editor.can_*()` antes de executar uma transação.

Use `editor.execute()` em Lua no editor para executar um formatador, validador ou gerador:

```lua
local output = editor.execute(
  "python3",
  "scripts/generate_levels.py",
  {
    out = "capture"
  }
)

print(output)
```

Quando o comando não modificar recursos do projeto, defina `reload_resources = false` para evitar um recarregamento desnecessário.

::: important
Não modifique arquivos em `.internal/` nem conteúdo gerado em `build/`.
:::

## Preferências {#preferences}

As preferências do editor podem ser lidas e gravadas pelo caminho documentado no OpenAPI, atualmente `/prefs/{path}`.

Por exemplo, você pode ler o tamanho configurado da fonte do código:

```sh
curl -sS "$BASE_URL/prefs/code/font/size" | jq
```

Ou defini-lo como, por exemplo, 16:

```sh
curl -sS \
  -X POST \
  -H "Content-Type: application/json" \
  --data '16' \
  "$BASE_URL/prefs/code/font/size"
```

O editor valida o valor de acordo com seu esquema de preferências. Um caminho ou valor inválido retorna HTTP `400`.

As preferências são configurações persistentes do usuário ou do usuário no projeto, e não configurações do projeto armazenadas em `game.project`. Se a automação precisar alterar temporariamente uma preferência, salve o valor anterior e restaure-o depois.

## Rotas definidas pelo projeto {#project-defined-routes}

Os scripts do editor podem definir rotas adicionais com [`get_http_server_routes()`](/manuals/editor-scripts/#http-server). Uma tabela opcional de operações OpenAPI expõe uma rota por meio do mesmo documento `/openapi.json` que as operações integradas.

As rotas definidas pelo projeto podem fornecer geração de conteúdo, validação, relatórios, verificações de localização, análise de recursos, testes específicos do projeto ou uma interface menor para uma IDE ou controlador externo.

Uma boa rota deve executar uma operação com nome claro, validar sua entrada, retornar um resultado estruturado, ser idempotente quando possível e limitar trabalhos custosos.

As rotas definidas pelo projeto não são protegidas automaticamente pelo token de `/eval`. Adicione autenticação e verificações de segurança específicas do projeto quando uma rota executar operações sensíveis.

## Hooks de ciclo de vida {#lifecycle-hooks}

Hooks são funções que podem ser executadas antes e depois de builds, antes e depois da criação de pacotes e quando um processo do jogo é iniciado ou encerrado. Um projeto pode conter um arquivo `hooks.editor_script` em sua raiz. Somente o arquivo de hook raiz recebe esses eventos, oferecendo ao projeto um único local para definir a ordem deles.

```lua
local M = {}

local function validate_project()
  print(editor.execute(
    "python3",
    "scripts/validate_project.py",
    {
      out = "capture",
      reload_resources = false
    }
  ))
end

function M.on_build_started(opts)
  validate_project()
end

function M.on_build_finished(opts)
  print("Build successful:", opts.success)
end

return M
```

Um erro gerado em `on_build_started()` interrompe o build do editor. Os hooks de ciclo de vida são executados apenas no editor; coloque a lógica compartilhada de validação e geração em scripts autônomos que também possam ser chamados pela CI.

## Segurança e compatibilidade {#security-and-compatibility}

Trate todo o servidor do editor como uma interface local confiável:

* Não exponha publicamente o acesso à porta.
* Proteja `.internal/editor.token`; ele autoriza `/eval` para a sessão atual.
* Não conceda acesso externo irrestrito a `/eval`.
* Mantenha o token na camada de integração local, e não em prompts, relatórios ou logs.
* Lembre-se de que as rotas definidas pelo projeto não herdam a autenticação de `/eval`.
* Use um `/openapi.json` atualizado.
* Use esperas limitadas para comandos automáticos assíncronos e para a inicialização do editor.

## Servidor do engine {#engine-server}

O servidor do editor pertence ao processo do editor. Um jogo em execução tem uma porta diferente e responsabilidades distintas, descritas no [manual do serviço do engine e da API HTTP de tempo de execução](/manuals/engine-service).
