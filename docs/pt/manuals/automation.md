---
title: Automação no Defold
brief: Este manual apresenta as interfaces de automação do Defold e explica como escolher entre os fluxos de trabalho do editor, de tempo de execução, de linha de comando, de testes e orientados por agentes.
---

# Automação no Defold {#automation-in-defold}

Este manual apresenta uma descrição geral e links para os manuais separados de cada tópico.

O Defold oferece suporte à automação em vários níveis. Escolher uma interface adequada à tarefa é um dos aspectos mais importantes de uma automação eficaz. A tabela abaixo pode ajudar você a escolher a interface mais simples para determinada ação:

| Camada | Finalidade |
| --- | --- |
| [Scripts do editor](/manuals/editor-scripts) | Comandos personalizados e fluxos de trabalho ou integrações do editor para acelerar testes e desenvolvimento, como a criação de níveis e assets |
| [Scripts da interface do editor](/manuals/editor-scripts-ui/) | Ferramentas visuais, popups, configuradores ou interfaces de usuário personalizadas que utilizam scripts do editor |
| [API HTTP do editor](/manuals/editor-http-api) | Controlar o projeto de jogo aberto no editor Defold por meio de operações OpenAPI, recursos do projeto, builds, comandos do editor, pré-visualizações, preferências, saída do console ou scripts do editor para operações personalizadas, ferramentas externas, integrações com IDEs e controladores de testes |
| [CLI Bob](/manuals/bob) | Compilar um projeto, criar arquivos de dados ou pacotes autônomos pela linha de comando, relatórios, CI |
| [Hooks de ciclo de vida](/manuals/editor-http-api#lifecycle-hooks) | Validação ou geração antes e depois de builds ou empacotamentos no editor |
| [Serviço HTTP do engine](/manuals/engine-service) | Inspeção do engine de jogo Defold (`dmengine`) em execução, serviços de desenvolvimento, profiling, mensagens de tempo de execução ou APIs de automação em tempo de execução definidas por extensões; ferramentas externas consultando e enviando comandos a um build de depuração em execução |
| [Automation Bridge](https://github.com/defold/extension-automation-bridge) | Extensão oficial do Defold que fornece endpoints adicionais de automação do engine em tempo de execução |
| [Testes automatizados](/manuals/automated-testing) | Testar lógica de jogo, mensagens, componentes, entrada, física e comportamento do engine, inspeção de cenas, feedback visual, por exemplo, por meio de [pré-visualização do editor](/manuals/editor-http-api/#rendering-scene-previews), entrada injetada, estado ativo da aplicação e [coleções de teste em execução](/manuals/automated-testing/#tests-in-a-running-collection) |
| Scripts de shell ou executores de tarefas | Geração, formatação, validação e tarefas repetíveis, operações comuns de arquivo |
| Ferramentas externas de automação específicas de plataforma e de navegador web | Ferramentas de teste para desktop, testes de interação HTML5, capturas de tela, integrações web |
| Agentes de programação com IA e modelos multimodais | Tarefas nas quais é difícil ou impossível implementar uma abordagem determinística, análise semântica de cenas, layouts de GUI ou capturas de tela em tempo de execução |

A distinção mais importante é entre o editor Defold e um jogo em execução. Eles são processos separados com servidores HTTP separados.

## Automação determinística ou agentes de IA {#deterministic-automation-or-ai-agents}

Prefira uma solução determinística quando a sequência de operações já for conhecida, como em um validador de níveis, formatador, tarefa de build ou teste de regressão. Normalmente, esses recursos devem ter entradas, saídas, tempos limite e códigos de saída estáveis. Isso é adequado para hooks e testes automatizados que podem ser executados de modo confiável em CI. Também é preferível usar uma solução determinística para a criação procedural de recursos dos seus projetos, como uma ferramenta para converter objetos glTF em modelos com determinado material, preencher um nível com árvores etc. Esses procedimentos podem ser facilmente criados para cada projeto com scripts do editor e scripts de interface. Leia mais sobre eles [no manual](/manuals/editor-scripts-ui).

Um agente pode ser útil quando uma tarefa exige investigação ou análise multimodal (por exemplo, com elementos visuais): localizar recursos relevantes, selecionar uma implementação, modificar vários arquivos, interpretar erros e iterar em direção a critérios de aceitação definidos. Ainda assim, o agente deve chamar interfaces determinísticas e consumir as mesmas evidências que um script local ou executor de CI. Consulte o manual sobre o [uso de agentes de programação com IA no Defold](/manuals/ai-agents).

## O loop de automação {#the-automation-loop}

Um processo de automação confiável forma um loop fechado:

1. Inspecionar — ler os arquivos do projeto, a descrição atual da interface e a documentação relevante.
2. Alterar — usar transações do editor, scripts do editor ou ferramentas de arquivo e shell.
3. Verificar — compilar, executar testes focados e coletar logs, relatórios, estados ou imagens.
4. Avaliar — comparar as evidências com os critérios de aceitação e, então, concluir ou tentar novamente.

![O loop de automação de inspecionar, alterar, verificar e avaliar](images/automation/automation_loop.png)

A verificação deve fornecer evidências do ambiente real. Evidências adequadas incluem:

* um resultado de build bem-sucedido;
* uma suíte de testes explicitamente concluída;
* o estado esperado do jogo em execução;
* um pacote ou relatório de build gerado;
* uma comparação de imagens determinística;
* uma captura de tela que atende a critérios visuais definidos.

Defina o resultado esperado antes de fazer alterações. Defina também um tempo limite e um número máximo de tentativas de correção. Um processo não assistido não deve continuar indefinidamente quando não conseguir atender aos critérios de aceitação.

## Próximas etapas {#next-steps}

Encontre mais detalhes sobre tópicos específicos relacionados a fluxos de trabalho de automação nos seguintes manuais:

* [Automação das tarefas do editor Defold com a API HTTP](/manuals/editor-http-api)
* [O serviço do engine e a API HTTP de tempo de execução](/manuals/engine-service)
* [Testes automatizados e verificação](/manuals/automated-testing)
* [Uso de agentes de programação com IA no Defold](/manuals/ai-agents)
