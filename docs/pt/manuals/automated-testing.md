---
title: Testes automatizados e verificação
brief: Este manual explica como projetar, executar e relatar testes determinísticos do Defold localmente, em um jogo em execução, em navegadores e em integração contínua.
---

# Testes automatizados e verificação {#automated-testing-and-verification}

Os testes automatizados verificam o código e o conteúdo do Defold com evidências explícitas e legíveis por máquina. Use este manual para projetar testes que funcionem igualmente com scripts locais, executores de CI (integração contínua) e agentes de programação. Ele aborda testes de módulos, execução de coleções, testes em navegador, automação em tempo de execução, verificações visuais, builds headless e apresenta boas práticas úteis.

## Níveis de verificação {#verification-levels}

Bons níveis de testes automatizados seguem o modelo da pirâmide de testes, que divide os testes em três camadas principais: testes unitários, testes de integração e testes de ponta a ponta (E2E). No Defold, você pode separar os testes em coleções específicas que podem ser carregadas no bootstrap. Em geral, é bom começar com a verificação mais restrita e rápida capaz de detectar o problema e depois adicionar testes de tempo de execução ou de plataforma quando necessário.

| Nível | Evidência adequada |
| --- | --- |
| Validação estática | Parser, formatador, validador de recursos ou comparação de arquivo gerado |
| Teste de módulo | Resultados de asserções para lógica Lua reutilizável com dependências mínimas do engine |
| Coleção em execução | Mensagens, componentes, entrada, física, ciclo de vida e comportamento do engine |
| Automação em tempo de execução | Estado ativo da cena, entrada injetada, estado da aplicação e capturas de tela em tempo de execução |
| Teste em navegador HTML5 | Entrada no canvas, integração com o navegador, comportamento da viewport e saída web |
| Teste de plataforma | Comportamento e renderização na plataforma-alvo real |
| Build e pacote | Status de saída do Bob, relatório de build, arquivo de dados e artefatos de pacote |

Uma compilação bem-sucedida comprova que o projeto pode ser compilado, mas não comprova que o comportamento do jogo está correto. Uma captura de tela não comprova transições, animações, interações ou o fluxo do jogo complexos, mas pode ser usada por soluções multimodais modernas para inspecionar a aparência de um frame e verificar se os shaders e o layout visual estão corretos. No entanto, para testes automatizados, prefira asserções determinísticas sempre que a condição puder ser expressa diretamente.

## Código Lua reutilizável e testável {#reusable-and-testable-lua-code}

Mantenha a lógica reutilizável em módulos Lua com dependências mínimas do engine. Transformações de dados puras, regras, máquinas de estado e cálculos podem então ser exercitados sem construir um mundo de jogo completo.

Separe o código voltado ao engine da lógica que ele chama. Um script pode traduzir mensagens e estados de componentes em chamadas a um módulo, enquanto os testes chamam o módulo diretamente com entradas controladas.

Consulte o [manual de escrita de código](/manuals/writing-code) para obter mais detalhes.

## Testes em uma coleção em execução {#tests-in-a-running-collection}

Use uma coleção de teste dedicada quando o comportamento depender de objetos de jogo, componentes, mensagens, entrada, física ou outros sistemas do engine.

Cada teste deve:

1. estabelecer um estado conhecido;
2. executar um comportamento;
3. declarar e avaliar o resultado esperado;
4. limpar os recursos criados;
5. emitir uma descrição estruturada do resultado.

Prefira coleções de teste isoladas para os testes. Um projeto pode selecionar uma coleção bootstrap de teste por meio de uma configuração temporária em `game.project`:

```ini
[bootstrap]
main_collection = /test/test.collectionc
```

Não deixe um bootstrap de teste temporário na configuração normal do projeto. Em CI, prefira um arquivo de configurações dedicado passado ao Bob. A CI não pode alterar o estado do repositório; ela deve fazer apenas alterações temporárias quando necessário.

Para jogos complexos, você pode criar pequenas coleções de "salas de desenvolvimento" com cenários predefinidos e blockouts simples. Elas tornam as mecânicas reproduzíveis e facilitam os testes durante o desenvolvimento sem a necessidade de navegar por estados e seções não relacionados do jogo.

### Frameworks de teste {#test-frameworks}

Os projetos podem implementar um pequeno executor ou usar uma [biblioteca de testes da comunidade](https://defold.com/assets/?tag=testing).

Por exemplo, o [DefTest](https://defold.com/assets/deftest/) é uma biblioteca de testes unitários baseada no Telescope. Ela oferece suporte a suítes, funções de configuração e desmontagem, asserções, filtragem por nome, mocks de APIs selecionadas do Defold e cobertura opcional com LuaCov. Os testes podem ser executados a partir de uma coleção bootstrap dedicada, inclusive em um pacote headless criado com o Bob.

## Resultados de teste estruturados {#structured-test-results}

O resumo no console/log de um framework pode ser útil para os desenvolvedores, mas um controlador automático não assistido ainda precisa de um resultado de conclusão explícito. Se necessário, adicione um pequeno adaptador em torno do callback ou resumo do framework para que o controlador processe facilmente os resultados dos testes.

Uma descrição simples dos resultados pode usar um prefixo exclusivo seguido de um objeto JSON em cada linha física do console:

```text
TEST {"run":"8f13","event":"suite_start","tests":2}
TEST {"run":"8f13","event":"case","name":"player_moves","status":"pass","duration_ms":3}
TEST {"run":"8f13","event":"case","name":"player_stops","status":"pass","duration_ms":2}
TEST {"run":"8f13","event":"suite_end","status":"pass","passed":2,"failed":0}
```

Um coletor deve processar cada linha de modo independente, localizar o prefixo `TEST`, analisar o JSON que vem em seguida e ignorar saídas não relacionadas do engine.

Inclua um identificador exclusivo de execução para que a saída de um processo antigo ou simultâneo não possa concluir a execução atual. Cada suíte deve emitir um evento final inequívoco (como `Pass`, `Failure`, `Crash`, `Timeout` etc.).

### Coleta da saída do console {#collecting-console-output}

Quando um jogo é executado a partir do editor, ele fornece tanto o histórico atual do console quanto um stream contínuo. Feche o stream após um evento correspondente de conclusão da suíte, o encerramento do processo, um erro ou o tempo limite e o limite de linhas configurados.

Leia mais no [manual da API HTTP do editor](/manuals/editor-http-api/#reading-console-output).

### Logs persistidos {#persisted-logs}

O Defold também pode persistir o log do jogo ativando `Write Log File` em `game.project`. Consulte [Logs do jogo e do sistema](/manuals/debugging-game-and-system-logs/). O registro em arquivo é útil para aplicações empacotadas e para testar dispositivos-alvo nos quais o console do editor não está disponível.

O projeto pode usar as funções integradas `print()` e `pprint()` ou, por exemplo, qualquer outra [biblioteca de logging](https://defold.com/assets/?tag=logging) do nosso Portal de Assets.

## Teste de um jogo em execução por meio de uma API de tempo de execução {#testing-a-running-game-through-a-runtime-api}

Uma API de automação em tempo de execução pode inspecionar e controlar um engine de depuração ativo. Ela pode ser usada quando os testes precisam localizar objetos de tempo de execução, injetar entrada, aguardar um estado visível ou capturar o resultado renderizado.

Leia o [manual do serviço do engine](/manuals/engine-service/#automation-bridge-extension) para obter mais detalhes.

O exemplo a seguir usa a estrutura auxiliar em Python da [Automation Bridge](https://github.com/defold/extension-automation-bridge). O projeto deve incluir uma versão compatível da extensão de depuração, expor um elemento com o id de automação especificado e publicar o estado de aplicação `screen`:

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()

try:
    play = game.element(automation_id="play_button")
    game.click(play)
    game.wait_for_state("screen", "gameplay", timeout=5.0)
    screenshot = game.screenshot()
    print(screenshot.path)
finally:
    game.close_engine()
```

Os estados definidos pela aplicação e os ids de automação usam a API Lua opcional e exclusiva para depuração da Automation Bridge, que deve ser ativada e publicada pelo projeto. Uma espera fixa é vulnerável à velocidade da máquina e ao timing dos frames; a consulta limitada de um estado definido é mais confiável.

A Automation Bridge é uma extensão, não faz parte do engine principal. Consulte sua [documentação de referência da API Python](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python) para saber sobre seletores, esperas, estados, eventos, capturas de tela e diagnósticos da versão instalada.

## Testes em navegador para HTML5 {#browser-tests-for-html5}

O editor pode criar e servir um build HTML5 por meio de seu comando atual `build-html5`, conforme descrito no [manual da API HTTP do editor](/manuals/editor-http-api/#building-html5). O Bob também pode criar um pacote HTML5 sem o editor.

Ferramentas externas de automação de navegador, como Playwright, Puppeteer, Selenium, WebdriverIO ou Cypress, podem:

* aguardar o canvas do Defold e a aplicação estarem prontos;
* enviar entradas de teclado, mouse e toque emulado;
* redimensionar a viewport;
* coletar a saída do console do navegador e erros JavaScript;
* fazer capturas de tela e comparar artefatos.

A entrada direcionada ao canvas é processada pelos mapeamentos de entrada normais do projeto e callbacks `on_input()`. Teste tanto a resposta do jogo quanto os pontos de integração específicos do navegador.

A abordagem mais confiável é expor uma ponte de testes JavaScript explícita no `index.html` personalizado. No lado do Defold, os builds HTML5 podem executar JavaScript usando `html5.run()`, o que possibilita a comunicação com essa ponte do navegador. Para comandos que trafegam do JavaScript de volta ao Defold, use uma ponte dedicada de JavaScript para o engine.

Mantenha os testes de navegador limitados. Diferencie no relatório final uma falha de carregamento da página, canvas ausente, erro JavaScript, tempo limite do teste e asserção do jogo com falha.

## Pré-visualizações do editor e capturas de tela em tempo de execução para inspeção visual {#editor-previews-and-runtime-screenshots}

É possível criar uma captura de tela dos arquivos de recursos na visualização de cena padrão do editor aberto ou de um jogo em tempo de execução.

| Método | Finalidade |
| --- | --- |
| [Pré-visualização do editor](/manuals/editor-http-api/#rendering-scene-previews) | Layout de um recurso carregado, como nível ou GUI, composição de atlas, inspeção de tile map, composição estática da cena, correção da renderização e dos shaders no editor ou criação de miniaturas para a documentação |
| [Captura de tela em tempo de execução](/manuals/engine-service) | O estado renderizado de um build em execução em um cenário controlado |

Você pode usar a comparação de imagens, por exemplo, para testes de regressão. Armazene a imagem da diferença e as métricas de comparação quando uma verificação falhar.

Um modelo multimodal pode avaliar, durante a inspeção visual, condições semânticas que são difíceis de expressar de outra forma, como texto cortado, controles sobrepostos, estados de seleção pouco claros ou conteúdo fora de uma área segura. Recomenda-se tratar essa avaliação como um sinal adicional com critérios explícitos, mas não como substituta para verificações de lógica determinísticas ou comparação de imagens.

## Testes headless e CI {#headless-tests-and-ci}

Use a ferramenta CLI de build Bob para uma CI independente do editor.

Você pode usá-la para resolver dependências, compilar um jogo, um arquivo de dados ou um pacote autônomo e gerar um relatório JSON:

```sh
mkdir -p build/reports

java -jar bob.jar \
  --root . \
  --archive \
  --build-report-json build/reports/build-report.json \
  resolve build
```

Compile um pacote de teste headless com configurações dedicadas:

```sh
java -jar bob.jar \
  --root . \
  --settings test/test.settings \
  --platform x86_64-linux \
  --variant headless \
  --archive \
  --bundle-output build/test-bundle \
  resolve build bundle
```

Execute o arquivo executável resultante com um controlador de processos adequado à plataforma. Capture o status de saída e os logs, aplique um tempo limite e exija o evento estruturado de conclusão da suíte.

O [manual do Bob](/manuals/bob) descreve plataformas, arquivos de configurações, pacotes, caches, extensões nativas e relatórios de build.

## Relatórios de falhas e artefatos {#failure-reports-and-artifacts}

Bons resultados de teste devem manter evidências suficientes para reproduzir e diagnosticar uma falha:

* nome do teste, identificador da execução e detalhes da asserção;
* tempo decorrido e resultado classificado;
* log completo do console ou processo;
* versão do Defold, plataforma-alvo e configuração relevante;
* relatório de build do Bob e status de saída do processo;
* estado de tempo de execução ou snapshot da cena, quando disponível;
* capturas de tela, diferenças em relação à baseline, gravações ou traces do navegador;
* caminhos ou links para todos os artefatos gerados.

O mesmo formato deve poder ser usado por um desenvolvedor, script local, serviço de CI ou [agente de programação com IA](/manuals/ai-agents). Isso mantém a verificação determinística mesmo quando o diagnóstico ou a correção são delegados.
