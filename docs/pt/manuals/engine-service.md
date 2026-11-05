---
title: O serviço do engine e as APIs HTTP de tempo de execução
brief: Este manual explica o serviço HTTP de desenvolvimento em um engine de depuração do Defold em execução e como extensões de tempo de execução ou ferramentas externas podem usá-lo.
---

# O serviço do engine e as APIs HTTP de tempo de execução {#the-engine-service-and-runtime-http-apis}

Executar um projeto no modo Debug cria um processo para uma determinada instância de tempo de execução do engine com seu jogo e um serviço especial do engine que pode ser acessado para infraestrutura de desenvolvimento e profiling, lógica e mensagens de tempo de execução, estado do engine e extensões.

O serviço da engine é um serviço HTTP de desenvolvimento pertencente a uma engine de depuração ou headless em execução (`dmengine` ou `dmengine_headless`).

Ele é separado do [servidor do editor](/manuals/editor-http-api), que pertence ao editor Defold e controla o projeto aberto.

Os dois serviços usam portas diferentes. Uma ferramenta que se conecta à porta do editor não pode chamar nela rotas de extensões de tempo de execução e vice-versa: uma ferramenta que se conecta ao serviço do engine não pode chamar operações do editor.

O serviço do engine faz parte da infraestrutura de depuração, desenvolvimento e profiling. As instâncias de release do engine não criam o serviço.

## Disponibilidade e descoberta da porta {#availability-and-port-discovery}

Quando o editor inicia uma engine de depuração, solicita uma porta de serviço atribuída dinamicamente. A engine informa a porta selecionada no *Console* e em seu log quando é executada pela linha de comando:

![Informações da porta do serviço do engine em um build de depuração do Defold](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

A engine também registra a URL completa de descoberta OpenAPI usando seu endereço real e a porta atribuída:

```text
INFO:ENGINE: OpenAPI: http://<address>:<port>/openapi.json
```

Essas linhas aparecem no console do editor quando o jogo foi iniciado pelo editor. Um controlador local simples pode interpretá-las, mas uma integração reutilizável deve permitir que o editor ou seu wrapper acompanhe a instância da engine e a porta registrada. Isso evita confundir uma porta antiga com um processo recém-iniciado ou reutilizado.

O engine também anuncia alvos de desenvolvimento por meio da descoberta de serviços nas plataformas compatíveis. Esse mecanismo é usado principalmente pelas ferramentas do Defold e não deve ser substituído por uma porta codificada permanentemente.

O servidor pode ser acessado em localhost (`127.0.0.1`) em uma determinada porta:

![Acesso ao servidor do engine](images/automation/engine-server.png)

## Descobrindo operações por meio de OpenAPI {#discovering-operations-through-openapi}

`GET /openapi.json` retorna um documento OpenAPI 3.0.3 que descreve a API HTTP em tempo de execução. Use a porta do serviço da engine informada no log. Para uma engine local, substitua `<port>` abaixo por essa porta:

```sh
ENGINE_URL="http://127.0.0.1:<port>"
curl -fsS "$ENGINE_URL/openapi.json" | jq
```

O documento descreve caminhos, métodos, parâmetros, corpos de requisições e respostas fornecidos pelos handlers atualmente registrados, incluindo extensões nativas que fornecem metadados OpenAPI. Seu objeto `paths` muda quando handlers são adicionados ou removidos. As rotas do profiler e das extensões dependem da plataforma, da configuração e das extensões registradas da engine em execução; por isso, busque o documento da instância que você está usando.

Handlers registrados sem metadados OpenAPI continuam podendo ser chamados, mas não aparecem no documento. Uma rota documentada também pode informar uma funcionalidade indisponível; examine as descrições de resposta e qualquer endpoint de capacidades antes de usar operações que dependam da plataforma.

O editor possui seu próprio [documento OpenAPI](/manuals/editor-http-api/#discovering-operations-through-openapi) na porta do editor. Use o documento da engine para operações em tempo de execução.

## Endpoints integrados {#built-in-endpoints}

O engine de depuração atual registra um pequeno conjunto de rotas principais.

| Endpoint | Finalidade |
| --- | --- |
| `GET /openapi.json` | Descobrir as operações HTTP em tempo de execução atualmente registradas que fornecem metadados OpenAPI |
| `GET /ping` | Verificar se o serviço do engine responde |
| `GET /info` | Ler a versão do engine, a plataforma, o identificador do build e as informações do serviço de log |
| `GET /state` | Ler o estado da conexão de desenvolvimento usado pelas ferramentas do Defold |
| `POST /post/<socket>/<message-type>` | Publicar uma mensagem do Defold codificada em Protobuf em um socket nomeado do engine |

Por exemplo:

```sh
curl -sS "$ENGINE_URL/ping"
curl -sS "$ENGINE_URL/info" | jq
curl -sS "$ENGINE_URL/state" | jq
```

A rota `/post` é usada por operações de desenvolvimento, como hot reload, reinicialização, redimensionamento e controle de processos. Seu corpo é uma mensagem Protobuf binária do tipo nomeado na rota; ela não é uma API de mensagens JSON. A mensagem Protobuf não pode ter mais de 1024 bytes quando serializada; caso contrário, será retornado um erro `400 Too large message`.

Essas rotas são infraestrutura de desenvolvimento, e existem outras rotas de profiling e inspeção de recursos na implementação do engine.

## Endpoints de gravação {#recording-endpoints}

Engines de depuração para desktop também expõem a gravação nativa de MP4 pelas rotas abaixo. Elas são omitidas de builds de release, headless, móveis e web, e quando **Exclude Record** está habilitado no [App Manifest](/manuals/app-manifest/#exclude-record).

| Endpoint | Finalidade |
| --- | --- |
| `GET /recording/capabilities` | Descobrir o suporte a vídeo/áudio, os requisitos do backend e o `instance_id` do serviço de gravação |
| `GET /recording/status` | Ler a operação atual, o progresso assíncrono e as informações do arquivo finalizado |
| `POST /recording/start` | Solicitar uma gravação e receber seu `operation_id` |
| `POST /recording/stop` | Solicitar a parada e a finalização da operação especificada |
| `GET /recording/files/{id}` | Baixar um MP4 finalizado |
| `DELETE /recording/files/{id}` | Excluir um arquivo concluído mantido pelo serviço |

Descubra essas rotas por meio de `/openapi.json` e verifique `/recording/capabilities` para conhecer o suporte da plataforma atual. Operações HTTP que alteram a gravação exigem o cabeçalho `X-Recording-Instance`, e a parada também exige o `operation_id` aceito. Iniciar e parar são operações assíncronas; aguarde a finalização antes de baixar o arquivo. Consulte o [manual de gravação](/manuals/recording/#recording-through-http) para conhecer o fluxo completo.

O serviço HTTP compartilha o gravador com Lua. Gravações iniciadas por HTTP habilitam o áudio da aplicação por padrão quando há suporte; as iniciadas por Lua gravam apenas vídeo por padrão. Somente gravações iniciadas por HTTP têm um recibo `file` para download. Antes de baixar, aguarde `pending: false`, `finalized: true` e `file.state: "complete"` e [verifique o tamanho e o SHA-256 do arquivo](/manuals/recording/#download-and-release-the-file). Consulte [compartilhamento do gravador](/manuals/recording/#sharing-the-recorder-with-http-clients) ao combinar clientes Lua e HTTP.

## Endpoint de captura de GPU Metal {#metal-gpu-trace-endpoint}

No macOS, engines de depuração expõem `/profiler/gputrace` para capturar rastreamentos da GPU Metal. A rota aparece em `/openapi.json` apenas no macOS. A captura exige o adaptador Metal nativo e `METAL_CAPTURE_ENABLED=1` no ambiente de inicialização da engine. Uma requisição retorna HTTP 501 com `error.code: "gputrace_unsupported"` se a captura estiver indisponível.

| Endpoint | Finalidade |
| --- | --- |
| `POST /profiler/gputrace` | Agendar uma captura em um caminho absoluto `.gputrace` com permissão de escrita; `frames` tem valor padrão `1` e pode ser de `1` a `10000`. |
| `GET /profiler/gputrace` | Ler o estado, o caminho e as contagens de frames da captura atual ou mais recente. |
| `DELETE /profiler/gputrace` | Cancelar uma captura pendente ou encerrar uma captura ativa após o frame renderizado atual; manter o rastreamento em disco. |

Requisições aceitas retornam HTTP 200 com `ok: true` e um objeto `data`. A captura avança de forma assíncrona: consulte `GET` até que `data.state` seja `complete`, `canceled` ou `failed`. Falhas de inicialização nativa são informadas em `data.error`. O rastreamento é gravado no host da engine. Consulte o [guia de captura de GPU Metal](/manuals/profiling/#metal-gpu-trace-capture) para ver comandos de inicialização, descoberta de suporte, exemplos de captura e como abrir o resultado no Xcode.

## Rotas de tempo de execução definidas por extensões {#extension-defined-runtime-routes}

Em builds de depuração, o SDK de extensões nativas pode fornecer acesso ao servidor web do engine. Uma extensão pode registrar um prefixo de rota nesse servidor e expor operações que dependem de dados de tempo de execução.

Isso é útil para ferramentas de desenvolvimento porque uma extensão pode compartilhar o serviço existente do engine em vez de abrir outro servidor HTTP.

Uma API de automação em tempo de execução definida por extensão deve:

* usar um prefixo de rota distinto e versionado;
* expor os recursos compatíveis;
* retornar erros estruturados;
* tratar explicitamente recursos indisponíveis da plataforma ou do engine;
* manter as operações locais ao desenvolvimento e aos testes;
* documentar se ela é omitida dos builds de release.

### Publicando operações de extensões em OpenAPI {#publishing-extension-operations-in-openapi}

No callback de inicialização da aplicação de uma extensão nativa, obtenha o servidor com `dmEngine::GetWebServer(app_params)` e registre handlers apenas quando o handle retornado não for nulo. Consulte o [ciclo de vida das extensões](/manuals/extensions/#extension-lifecycle) para configurar o callback.

A sobrecarga de quatro argumentos de `dmWebServer::AddHandler()` aceita um objeto Paths do OpenAPI 3.0.3 como string JSON. O objeto tem os caminhos das rotas como chaves de nível superior. Cada caminho deve começar com o prefixo registrado e não pode estar documentado por outro handler. Use esquemas inline ou referências a caminhos no documento resultante.

Por exemplo, esta função auxiliar registra um callback e a descrição de seu endpoint de status:

```cpp
#include <dmsdk/dlib/webserver.h>

static const char STATUS_OPENAPI[] = R"json(
{
  "/example/v1/status": {
    "get": {
      "summary": "Get extension status",
      "responses": {
        "200": {
          "description": "Current extension status",
          "content": {
            "text/plain": {
              "schema": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
)json";

dmWebServer::Result RegisterStatusHandler(dmWebServer::HServer server,
                                        dmWebServer::Handler callback,
                                        void* context)
{
    dmWebServer::HandlerParams params;
    params.m_Handler = callback;
    params.m_Userdata = context;
    return dmWebServer::AddHandler(
        server, "/example/v1", &params, STATUS_OPENAPI);
}
```

Passe um callback que implemente `GET /example/v1/status` e retorne a resposta `text/plain` documentada. O callback continua responsável por verificar caminhos e métodos das requisições e produzir respostas. Verifique o resultado do registro: metadados inválidos ou conflitantes retornam `dmWebServer::RESULT_ERROR_INVAL`.

O servidor mantém o ponteiro JSON sem copiar a string. Mantenha seu armazenamento inalterado e válido até que o handler seja removido com `dmWebServer::RemoveHandler()` ou que o servidor seja destruído. O array `static const char` do exemplo atende a esse requisito. Remover o handler também remove seus caminhos das respostas posteriores de `/openapi.json`.

A sobrecarga de três argumentos `dmWebServer::AddHandler(server, prefix, &params)` continua sendo aceita. Ela equivale a passar `0` como quarto argumento: o handler é registrado sem metadados OpenAPI e é omitido da descoberta.

## Extensão Automation Bridge {#automation-bridge-extension}

A [Automation Bridge](https://github.com/defold/extension-automation-bridge) oficial do Defold é uma extensão nativa exclusiva para depuração, criada sobre o serviço do engine. Ela registra uma API versionada de automação em tempo de execução em:

```text
http://127.0.0.1:<engine-service-port>/automation-bridge/v1
```

Sua API de tempo de execução oferece recursos como inspeção de cenas e nodes, entrada, informações da tela, capturas de tela, gravação, informações do ciclo de vida e sincronização opcional definida pela aplicação. Algumas operações incluem:

| Operação | Ação |
| --- | --- |
| `GET  /automation-bridge/v1/health` | Relatório de integridade, recursos e compatibilidade da API |
| `POST /automation-bridge/v1/input/click` | Para interações de entrada em tempo de execução |
| `GET  /automation-bridge/v1/screenshot` | Para capturas de tela em tempo de execução |

Use a [documentação da API nativa](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge) e a [documentação dos auxiliares em Python](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python) da extensão para a versão instalada no projeto.

A Automation Bridge não expõe sua API HTTP nem seu módulo Lua em builds de release.

### Clientes do editor e de tempo de execução {#editor-and-runtime-clients}

Os auxiliares em Python da Automation Bridge ilustram a arquitetura de dois clientes. A função `editor.open_project()` retorna um cliente de projeto do editor, e `project.build_and_run()` retorna um cliente separado do engine.

| Cliente | Finalidade |
| --- | --- |
| Projeto | API HTTP do editor, comandos, depurador, console, preferências, referência, pré-visualizações, build e descoberta de porta |
| Jogo — serviço do engine | Cena, entrada, capturas de tela, estado de tempo de execução e sincronização |

A divisão entre `project` e `game` torna explícito o limite entre os processos. As operações do editor permanecem no servidor do editor, enquanto as observações e ações relacionadas ao jogo ativo permanecem no serviço do engine.

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()
```

## Limitações e segurança {#limitations-and-security}

O serviço do engine e as rotas definidas por extensões são ferramentas de desenvolvimento e devem ser tratadas dessa forma.

::: important
Use o documento `/openapi.json` da engine em execução para descoberta no Defold 1.14.1 e posteriores. Engines anteriores não fornecem esse endpoint. Para handlers registrados sem metadados OpenAPI, consulte a documentação versionada da API da extensão.
:::

Scripts de tempo de execução, física, entrada, objetos criados dinamicamente e renderização de plataforma exigem um engine em execução e devem ser verificados por meio de [testes automatizados em tempo de execução](/manuals/automated-testing).

* Não publique o serviço por meio de um roteador, interface pública ou túnel não confiável.
* Não presuma que as rotas do serviço do engine exijam autenticação.
* As rotas de tempo de execução podem variar de acordo com a versão da extensão, plataforma, backend gráfico e recursos do engine.
* Use negociação de versão ou recursos para APIs atualizadas definidas por extensões.
