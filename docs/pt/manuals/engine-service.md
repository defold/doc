---
title: O serviço do engine e as APIs HTTP de tempo de execução
brief: Este manual explica o serviço HTTP de desenvolvimento em um engine de depuração do Defold em execução e como extensões de tempo de execução ou ferramentas externas podem usá-lo.
---

# O serviço do engine e as APIs HTTP de tempo de execução {#the-engine-service-and-runtime-http-apis}

Executar um projeto no modo Debug cria um processo para uma determinada instância de tempo de execução do engine com seu jogo e um serviço especial do engine que pode ser acessado para infraestrutura de desenvolvimento e profiling, lógica e mensagens de tempo de execução, estado do engine e extensões.

O serviço do engine é um serviço HTTP de desenvolvimento que pertence a um engine de depuração (`dmengine`) em execução.

Ele é separado do [servidor do editor](/manuals/editor-http-api), que pertence ao editor Defold e controla o projeto aberto.

Os dois serviços usam portas diferentes. Uma ferramenta que se conecta à porta do editor não pode chamar nela rotas de extensões de tempo de execução e vice-versa: uma ferramenta que se conecta ao serviço do engine não pode chamar operações do editor.

O serviço do engine faz parte da infraestrutura de depuração, desenvolvimento e profiling. As instâncias de release do engine não criam o serviço.

## Disponibilidade e descoberta da porta {#availability-and-port-discovery}

Quando o editor inicia um engine de depuração, ele solicita uma porta de serviço atribuída dinamicamente. O engine informa a porta selecionada no `Console` (e em seu log, se executado por uma CLI):

![Informações da porta do serviço do engine em um build de depuração do Defold](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

A linha aparece no console do editor quando o jogo foi iniciado a partir dele. Um controlador local simples pode analisar essa linha, mas uma integração reutilizável deve permitir que o editor ou seu wrapper acompanhe a instância do engine e a porta registrada. Isso evita confundir uma porta antiga com um processo recém-iniciado ou reutilizado.

O engine também anuncia alvos de desenvolvimento por meio da descoberta de serviços nas plataformas compatíveis. Esse mecanismo é usado principalmente pelas ferramentas do Defold e não deve ser substituído por uma porta codificada permanentemente.

O servidor pode ser acessado em localhost (`127.0.0.1`) em uma determinada porta:

![Acesso ao servidor do engine](images/automation/engine-server.png)

## Endpoints integrados {#built-in-endpoints}

O engine de depuração atual registra um pequeno conjunto de rotas principais.

| Endpoint | Finalidade |
| --- | --- |
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
Atualmente, o serviço do engine não publica um documento OpenAPI. As integrações devem se limitar ao comportamento documentado ou à API versionada de uma extensão.
:::

Scripts de tempo de execução, física, entrada, objetos criados dinamicamente e renderização de plataforma exigem um engine em execução e devem ser verificados por meio de [testes automatizados em tempo de execução](/manuals/automated-testing).

* Não publique o serviço por meio de um roteador, interface pública ou túnel não confiável.
* Não presuma que as rotas do serviço do engine exijam autenticação.
* As rotas de tempo de execução podem variar de acordo com a versão da extensão, plataforma, backend gráfico e recursos do engine.
* Use negociação de versão ou recursos para APIs atualizadas definidas por extensões.
