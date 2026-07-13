---
title: Profiling no Defold
brief: Este manual explica os recursos de profiling presentes no Defold.
---

# Profiling

O Defold inclui ferramentas de profiling integradas à engine e ao pipeline de build. Elas ajudam a encontrar problemas de desempenho, memória e uso de recursos. Os dados de profiling em tempo de execução podem ser consumidos por vários recursos:

* O profiler básico e o profiler visual dentro do jogo estão disponíveis em todas as plataformas.
* O [profiler Remotery](https://github.com/Celtoys/Remotery) e o profiler de frames web interativo estão disponíveis em plataformas desktop e mobile.
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

Consulte a [referência da API do profiler](/ref/stable/profiler/) para mais informações sobre as funções do perfilador.

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

1. Inicie seu jogo no dispositivo-alvo.
2. Abra um navegador e acesse http://localhost:8002

O perfilador de recursos é dividido em 2 seções, uma mostrando uma visualização hierárquica das coleções, objetos de jogo e componentes atualmente instanciados no seu jogo, e a outra mostrando todos os recursos atualmente carregados.

![Resource profiler](images/profiling/webprofiler_resources_page.png)

Collection view
: A visualização de coleção mostra uma lista hierárquica de todos os objetos de jogo e componentes atualmente instanciados no jogo e de qual coleção eles se originam. Essa é uma ferramenta muito útil quando você precisa investigar e entender o que está instanciado no jogo em um determinado momento e de onde os objetos se originam.

Resources view
: A visualização de recursos mostra todos os recursos atualmente carregados na memória, seu tamanho e o número de referências a cada recurso. Isso é útil ao otimizar o uso de memória na sua aplicação, quando você precisa entender o que está carregado na memória em um determinado momento.

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

O builder produzirá um arquivo chamado "report.html" ao lado do pacote do jogo. Abra o arquivo em um navegador web para inspecionar o relatório:

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

  Um conjunto de ferramentas de profiling que captura dados em tempo real da atividade de CPU, memória e rede do seu jogo. Você pode realizar tracing de métodos baseado em amostras da execução do código, capturar heap dumps, ver alocações de memória e inspecionar os detalhes de arquivos transmitidos pela rede. Usar a ferramenta exige que você defina `android:debuggable="true"` em "AndroidManifest.xml".

  ![android profiler](images/profiling/android_profiler.png)

  Observação: desde o Android Studio 4.1, também é possível [executar as ferramentas de profiling sem iniciar o Android Studio](https://developer.android.com/studio/profile/android-profiler.html#standalone-profilers).

Graphics API Debugger (Android)
: https://github.com/google/gapid

  Esta é uma coleção de ferramentas que permite inspecionar, ajustar e reproduzir chamadas de uma aplicação para um driver gráfico. Usar a ferramenta exige que você defina `android:debuggable="true"` em "AndroidManifest.xml".

  ![graphics api debugger](images/profiling/gapid.png)
