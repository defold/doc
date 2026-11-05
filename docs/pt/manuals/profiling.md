---
title: Profiling no Defold
brief: Este manual explica os recursos de profiling presentes no Defold.
---

# Profiling

O Defold inclui ferramentas de profiling integradas à engine e ao pipeline de build. Elas ajudam a encontrar problemas de desempenho, memória e uso de recursos. Os dados de profiling em tempo de execução podem ser consumidos por vários recursos:

* O profiler básico e o profiler visual dentro do jogo estão disponíveis em todas as plataformas.
* O [profiler Remotery](https://github.com/Celtoys/Remotery) e o profiler de frames web interativo estão disponíveis em plataformas desktop e mobile.
* Builds de depuração macOS que usam Metal podem salvar [rastreamentos de GPU](#metal-gpu-trace-capture) para inspeção no Xcode.
* Builds HTML5 podem publicar escopos do Defold na API Web Performance do navegador.

A configuração **Profiler** no [Manifesto do aplicativo](/manuals/app-manifest/#profiler) controla se o código do profiler é vinculado a um build. **Debug Only** é o padrão, **None** o exclui e **Always** o inclui em builds debug e release. As configurações `profiler` no *game.project* controlam o comportamento em tempo de execução, mas não vinculam novamente a um build o código do profiler que foi excluído. Em particular, **Track CPU** controla a amostragem de uso da CPU; ela é separada da escolha feita no Manifesto do aplicativo.

## O perfilador visual em tempo de execução

Builds que incluem suporte ao profiler têm um profiler visual em tempo de execução que exibe informações ao vivo sobre a aplicação em execução:

```lua
function on_reload(self)
    -- Alterna o perfilador visual no hot reload.
    profiler.enable_ui(true)
end
```

![Visual profiler](images/profiling/visual_profiler.png)

O perfilador visual fornece várias funções diferentes que podem ser usadas para alterar como ele apresenta seus dados:

```lua

profiler.set_ui_mode()
profiler.set_ui_view_mode()
profiler.view_recorded_frame()
```

Consulte a [referência da API do profiler](/ref/profiler/) para mais informações sobre as funções do perfilador.

## O perfilador web
Enquanto uma build desktop ou mobile com suporte ao profiler está em execução, os profilers interativos de frames e recursos podem ser acessados por um navegador.

### Profiler de frames Remotery
O Frame profiler permite amostrar seu jogo enquanto ele está em execução e analisar frames individuais em detalhe. Para acessar o perfilador:

1. Inicie seu jogo no dispositivo-alvo.
2. Selecione o menu <kbd> Debug ▸ Open Web Profiler</kbd>.

O perfilador de frames é dividido em várias seções que fornecem diferentes visões do jogo em execução. Pressione o botão Pause no canto superior direito para interromper temporariamente a atualização das visualizações pelo perfilador.

![Web profiler](images/profiling/webprofiler_page.png)

::: sidenote
Quando você usa vários alvos simultaneamente, pode alternar manualmente entre eles alterando o campo Connection Address no topo da página para corresponder à URL do perfilador Remotery mostrada no console quando o alvo foi iniciado:

```
INFO:ENGINE: Defold Engine 1.3.4 (80b1b73)
INFO:DLIB: Initialized Remotery (ws://127.0.0.1:17815/rmt)
INFO:ENGINE: Loading data from: build/default
```
:::

Sample Timeline
: Sample Timeline mostra os frames de dados capturados na engine, uma linha do tempo horizontal por Thread. Main é a thread principal onde toda a lógica do jogo e a maior parte do código da engine é executada. Remotery é para o próprio perfilador e Sound é para a thread de mixagem e reprodução de som. Você pode aproximar e afastar o zoom (usando a roda do mouse) e selecionar frames individuais para ver os detalhes de um frame na visualização Frame Data.

  ![Sample Timeline](images/profiling/webprofiler_sample_timeline.png)


Frame Data
: A visualização Frame Data é uma tabela onde todos os dados do frame atualmente selecionado são detalhados. Você pode ver quantos milissegundos são gastos em cada escopo da engine.

  ![Frame data](images/profiling/webprofiler_frame_data.png)


Global Properties
: A visualização Global Properties mostra uma tabela de contadores. Eles tornam fácil, por exemplo, acompanhar o número de draw calls ou o número de componentes de determinado tipo.

  ![Global Properties](images/profiling/webprofiler_global_properties.png)

::: sidenote
O valor LuaMem é a quantidade de memória em kilobytes usada pela VM Lua conforme relatado pelo coletor de lixo do Lua. Memory é a quantidade de memória em kilobytes usada pela engine.
:::

::: important
A [configuração Max Sample Count](/manuals/project-settings/#max-sample-count) limita o número de amostras do profiler registradas por thread e por frame. Se o profiler informar que o limite foi excedido, primeiro verifique se o código de profiling das extensões nativas tem algum par de início/fim de escopo sem correspondência. Aumente o limite somente quando um frame legítimo contiver mais escopos do que o limite configurado.
:::

### Perfilador de recursos
O Resource profiler permite inspecionar seu jogo enquanto ele está em execução e analisar o uso de recursos em detalhe. Para acessar o perfilador:

1. Inicie um build de depuração do jogo no dispositivo-alvo.
2. Abra o [endereço do serviço da engine](/manuals/engine-service/#availability-and-port-discovery) em um navegador: `http://<address>:<port>/`. Use o endereço e a porta informados no console pela engine em execução.

O perfilador de recursos é dividido em 2 seções, uma mostrando uma visualização hierárquica das coleções, objetos de jogo e componentes atualmente instanciados no seu jogo, e a outra mostrando todos os recursos atualmente carregados.

![Resource profiler](images/profiling/webprofiler_resources_page.png)

Collection view
: A visualização de coleção mostra uma lista hierárquica de todos os objetos de jogo e componentes atualmente instanciados no jogo e de qual coleção eles se originam. Essa é uma ferramenta muito útil quando você precisa investigar e entender o que está instanciado no jogo em um determinado momento e de onde os objetos se originam.

Resources view
: A visualização de recursos mostra todos os recursos atualmente carregados na memória, seu tamanho e o número de referências a cada recurso. Isso é útil ao otimizar o uso de memória na sua aplicação, quando você precisa entender o que está carregado na memória em um determinado momento.

#### Tempos de carregamento de recursos {#resource-loading-times}

Você também pode inspecionar quanto tempo cada recurso leva para carregar. Habilite [Resource → Profile](/manuals/project-settings/#profile) em *game.project* antes de iniciar o jogo. Na visualização de texto, a configuração é:

```ini
[resource]
profile = 1
```

A configuração está desabilitada por padrão. Reinicie o jogo após habilitá-la para medir os carregamentos da inicialização. Cada carregamento concluído ou com falha grava uma entrada de log no nível INFO com o caminho do recurso, o tempo total e os tempos das etapas de pré-carregamento, leitura, criação, pós-criação, fila e espera. Acertos no cache não produzem novos registros de carregamento.

No profiler de recursos, clique em **Capture** e depois em **Show load times** para revelar as colunas de tempo. **Capture** atualiza a visualização das medições armazenadas; não habilita o profiling nem mede retroativamente carregamentos anteriores.

| Coluna | Significado |
| --- | --- |
| **Load (ms)** | Tempo total decorrido no carregamento inicial, incluindo dependências, trabalho de pós-criação, enfileiramento e espera. |
| **Preload (ms)** | Tempo gasto preparando o recurso em seu callback de pré-carregamento. |
| **Read (ms)** | Tempo gasto lendo os dados do recurso. |
| **Create (ms)** | Tempo gasto criando o recurso de runtime em seu callback de criação. |

Exibir os tempos de carregamento ordena a tabela pelo tempo total, com os recursos mais lentos primeiro. Clique no cabeçalho de uma coluna de tempo para ordenar por essa etapa; clique novamente para inverter a ordem. As barras da coluna **Load** mostram cada total em relação ao recurso visível mais lento. Clique em **Hide load times** para ocultar as colunas novamente.

Os tempos de carregamento e de callbacks incluem o trabalho de dependências aninhadas. Não some os totais dos recursos para calcular o tempo de inicialização, pois o mesmo trabalho pode aparecer na medição de mais de um recurso. As colunas **Preload**, **Read** e **Create** também não representam todo o tempo total de carregamento; o log fornece as etapas adicionais.

Um travessão (`—`) significa que nenhuma medição concluída está disponível, por exemplo porque o profiling estava desabilitado ou o carregamento inicial ainda não terminou. Um zero medido é exibido como `0.000`. As medições descrevem o carregamento inicial: acertos no cache e hot reloads não as alteram, e descarregar um recurso remove sua medição armazenada.

## Captura de rastreamentos da GPU Metal {#metal-gpu-trace-capture}

O [serviço HTTP da engine](/manuals/engine-service/#metal-gpu-trace-endpoint) pode capturar comandos da GPU Metal em um documento *.gputrace* no macOS. Abra o rastreamento concluído no Xcode para inspecionar os frames capturados. Esse recurso está integrado à engine de depuração.

### Inicializando e verificando o suporte {#launch-and-check-support}

Crie um [bundle de depuração](/manuals/bundling/#release-vs-debug) macOS com o backend gráfico Metal nativo incluído. Se usar um App Manifest, selecione uma opção de **Graphics (macOS)** que inclua Metal; consulte [backends gráficos](/manuals/app-manifest/#graphics).

Inicie o executável do bundle em um terminal com `METAL_CAPTURE_ENABLED=1` e selecione o adaptador Metal. Substitua o caminho do bundle e o nome do executável neste exemplo:

```sh
METAL_CAPTURE_ENABLED=1 \
    "/absolute/path/MyGame.app/Contents/MacOS/MyGame" --graphics-adapter=metal
```

A variável de ambiente deve estar definida quando a engine iniciar. Defini-la apenas em um terminal usado para requisições HTTP não habilita a captura em uma engine já em execução.

Em um segundo terminal, use a [porta do serviço da engine impressa no log](/manuals/engine-service/#availability-and-port-discovery). Os exemplos abaixo usam `curl` e `jq`:

```sh
ENGINE_URL="http://127.0.0.1:<port>"
curl -fsS "$ENGINE_URL/openapi.json" | jq '.paths["/profiler/gputrace"]'
curl -sS -i "$ENGINE_URL/profiler/gputrace"
```

A rota é registrada apenas no macOS. Uma entrada `null` no documento OpenAPI significa que essa engine não a expõe. Mesmo quando a rota está presente, o suporte à captura depende do adaptador gráfico e do ambiente de inicialização. `GET /profiler/gputrace` retorna HTTP 501 com `error.code: "gputrace_unsupported"` quando a captura Metal está indisponível. Verifique se a engine está usando Metal e foi iniciada com `METAL_CAPTURE_ENABLED=1` antes de prosseguir. Uma requisição compatível retorna HTTP 200 com o status da captura.

### Capturando e inspecionando frames {#capture-and-inspect-frames}

Escolha um caminho absoluto de saída com permissão de escrita que termine em `.gputrace`, com um diretório pai existente e sem um rastreamento já presente nesse caminho. O caminho se refere ao computador que executa a engine. Para uma engine local, este exemplo cria um novo diretório temporário e solicita um frame:

```sh
GPU_TRACE_DIR=$(mktemp -d /tmp/defold-gputrace.XXXXXX)
GPU_TRACE_PATH="$GPU_TRACE_DIR/frame.gputrace"
GPU_TRACE_REQUEST=$(jq -n --arg path "$GPU_TRACE_PATH" '{path: $path, frames: 1}')
curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    --data "$GPU_TRACE_REQUEST" \
    "$ENGINE_URL/profiler/gputrace" | jq
```

`frames` é opcional, tem valor padrão `1` e aceita inteiros de `1` a `10000`. A captura começa antes do próximo frame renderizado e termina após o envio da quantidade solicitada de frames completos. Mantenha o jogo renderizando durante a espera. Apenas uma captura pode estar pendente ou ativa; outra solicitação de início retorna HTTP 409 com `error.code: "gputrace_active"`.

`POST` retorna HTTP 200 com `ok: true` e `data.state: "pending"` quando a captura é agendada. A conclusão é informada por requisições posteriores de status. Repita a requisição de status até que `data.state` se torne `complete`, `canceled` ou `failed`:

```sh
curl -fsS "$ENGINE_URL/profiler/gputrace" | jq
```

| `data.state` | Significado |
| --- | --- |
| `idle` | Nenhuma captura foi agendada. |
| `pending` | A captura aguarda o início da renderização. |
| `capturing` | A captura está ativa; `data.frames_captured` informa os frames concluídos. |
| `complete` | A captura terminou e o rastreamento pode ser aberto. |
| `canceled` | Uma captura pendente foi cancelada antes de iniciar. |
| `failed` | A captura não conseguiu iniciar; inspecione `data.error` para ver o erro nativo. |

`GET` descreve a captura atual ou mais recente. Verifique se `data.path` corresponde ao caminho solicitado. Uma captura com falha ainda retorna HTTP 200 com `ok: true`; inspecione `data.state` e `data.error` para determinar o resultado. Em um cliente automatizado, consulte com intervalo e limite de tempo.

Quando o estado for `complete`, abra o rastreamento no Xcode no Mac da engine:

```sh
open -a Xcode "$GPU_TRACE_PATH"
```

O endpoint HTTP retorna o status; o rastreamento é salvo em `data.path` no host da engine. Para uma engine remota, recupere o documento concluído desse host antes de abri-lo localmente.

### Cancelando ou encerrando uma captura {#cancel-or-stop-a-capture}

Para cancelar uma captura pendente ou encerrar antecipadamente uma captura ativa:

```sh
curl -fsS -X DELETE "$ENGINE_URL/profiler/gputrace" | jq
```

Uma captura pendente muda para `canceled`. Em uma captura ativa, `data.stop_requested` passa a ser `true`, e a captura termina após o envio do frame renderizado atual. Continue consultando `GET` até atingir um estado final. `DELETE` mantém qualquer rastreamento já gravado em disco. Se não houver captura pendente ou ativa, retorna HTTP 409 com `error.code: "gputrace_inactive"`.

## Timeline de desempenho do navegador em HTML5

O HTML5 usa a API Web Performance em vez do Remotery para a timeline do navegador. Para registrar escopos do Defold:

1. Certifique-se de que o modo de profiler selecionado no Manifesto do aplicativo inclua suporte ao profiler na variante de build em execução.
2. Ative **Performance Timeline Enabled** (`profiler.performance_timeline_enabled`) em *game.project*.
3. Inicie a build HTML5 e abra as ferramentas de desenvolvimento do navegador.
4. Grave uma sessão no painel **Performance** do navegador e examine os escopos do Defold na timeline resultante.

Essa timeline do navegador é separada tanto do profiler visual dentro do jogo quanto do profiler web interativo Remotery.


## Relatórios de build {#build-reports}
Ao empacotar seu jogo, há uma opção para criar um relatório de build. Isso é muito útil para entender o tamanho de todos os assets que fazem parte do pacote do seu jogo. Basta marcar a caixa de seleção *Generate build report* ao empacotar o jogo.

![build report](images/profiling/build_report.png)

O builder produzirá um arquivo chamado `report.html` ao lado do pacote do jogo. Abra o arquivo em um navegador web para inspecionar o relatório:

![build report](images/profiling/build_report_html.png)

*Overview* fornece uma decomposição visual geral do tamanho do projeto com base no tipo de recurso.

*Resources* mostra uma lista detalhada de recursos que você pode ordenar por tamanho, taxa de compressão, criptografia, tipo e nome de diretório. Use o campo "search" para filtrar as entradas de recursos exibidas.

A seção *Structure* mostra tamanhos com base em como os recursos estão organizados na estrutura de arquivos do projeto. As entradas são codificadas por cor, de verde (leve) a azul (pesado), de acordo com o tamanho relativo do conteúdo de arquivos e diretórios.


## Ferramentas externas
Além das ferramentas integradas, há uma ampla variedade de ferramentas gratuitas de tracing e profiling de alta qualidade disponíveis. Aqui está uma seleção:

ProFi (Lua)
: Não incluímos nenhum perfilador Lua integrado, mas há bibliotecas externas fáceis de usar. Para descobrir onde seus scripts gastam tempo, insira medições de tempo no seu próprio código ou use uma biblioteca de profiling Lua como [ProFi](https://github.com/jgrahamc/ProFi).

  Observe que perfiladores em Lua pura adicionam bastante overhead a cada hook que instalam. Por esse motivo, você deve ter certa cautela com os perfis de tempo obtidos por esse tipo de ferramenta. Perfis de contagem, porém, são suficientemente precisos.

Instruments (macOS e iOS)
: Este é um analisador e visualizador de desempenho que faz parte do Xcode. Ele permite rastrear e inspecionar o comportamento de um ou mais apps ou processos, examinar recursos específicos do dispositivo (como Wi-Fi e Bluetooth) e muito mais.

  ![instruments](images/profiling/instruments.png)

OpenGL profiler (macOS)
: Parte do pacote "Additional Tools for Xcode", que você pode baixar da Apple (selecione <kbd>Xcode ▸ Open Developer Tool ▸ More Developer Tools...</kbd> no menu do Xcode).

  Esta ferramenta permite inspecionar uma aplicação Defold em execução e ver como ela usa OpenGL. Ela permite fazer traces de chamadas de função OpenGL, definir breakpoints em funções OpenGL, investigar recursos da aplicação (texturas, programas, shaders etc.), examinar o conteúdo de buffers e verificar outros aspectos do estado do OpenGL.

  ![opengl profiler](images/profiling/opengl.png)

Android Profiler (Android)
: https://developer.android.com/studio/profile/android-profiler.html

  Um conjunto de ferramentas de profiling que captura dados em tempo real da atividade de CPU, memória e rede do seu jogo. Você pode realizar tracing de métodos baseado em amostras da execução do código, capturar heap dumps, ver alocações de memória e inspecionar os detalhes de arquivos transmitidos pela rede. Usar a ferramenta exige que você defina `android:debuggable="true"` em `AndroidManifest.xml`.

  ![android profiler](images/profiling/android_profiler.png)

  Observação: desde o Android Studio 4.1, também é possível [executar as ferramentas de profiling sem iniciar o Android Studio](https://developer.android.com/studio/profile/android-profiler.html#standalone-profilers).

Graphics API Debugger (Android)
: https://github.com/google/gapid

  Esta é uma coleção de ferramentas que permite inspecionar, ajustar e reproduzir chamadas de uma aplicação para um driver gráfico. Usar a ferramenta exige que você defina `android:debuggable="true"` em `AndroidManifest.xml`.

  ![graphics api debugger](images/profiling/gapid.png)
