---
title: Uso de agentes de programação com IA no Defold
brief: Este manual explica como conectar agentes de programação independentes de modelo às interfaces de automação do Defold, mantendo explícitas a verificação, as permissões e a segurança.
---

# Uso de agentes de programação com IA no Defold {#using-ai-coding-agents-with-defold}

Agentes de programação que utilizam LLMs e modelos multimodais podem inspecionar, modificar e verificar projetos do Defold chamando as mesmas interfaces independentes de modelo usadas por desenvolvedores, scripts locais, integrações com IDEs e CI. Você pode usar um agente quando o trabalho exigir investigação e adaptação.

O Defold não depende de um provedor de modelos nem de um protocolo de agentes específico. Os projetos do Defold funcionam bem com Claude Code, Codex, Cursor ou qualquer outra solução. Um ambiente de agente precisa apenas dos recursos específicos concedidos para a tarefa, como ler arquivos do projeto, executar comandos selecionados, chamar operações HTTP locais, analisar JSON ou inspecionar imagens. Isso é possível graças às interfaces de automação que o Defold disponibiliza para o editor e para uma instância em execução do engine, além de os arquivos de projeto do Defold serem recursos baseados em texto fáceis de analisar.

## Quando um agente de IA é útil {#when-an-ai-agent-is-useful}

Um agente pode ser útil quando uma tarefa exige, por exemplo:

* encontrar recursos e documentação relevantes;
* selecionar entre implementações possíveis;
* alterar vários arquivos relacionados;
* interpretar falhas de build ou teste;
* comparar um resultado visual com critérios semânticos de aceitação;
* fazer uma tentativa de correção limitada com base nas evidências coletadas.

Os agentes são poderosos para processos não determinísticos de desenvolvimento, investigação e teste. Eles podem ajudar a criar soluções variadas e funcionam muito bem com o Defold.

## Interfaces do Defold independentes de modelo {#model-neutral-defold-interfaces}

O Defold oferece várias interfaces compatíveis necessárias para que a tarefa seja executada com qualquer modelo disponível:

* Arquivos de projeto e ferramentas de shell permitem inspeção direta e alterações de texto.
* [Scripts do editor](/manuals/editor-scripts) podem fornecer operações de recursos e ferramentas específicas do projeto.
* A [API HTTP do editor](/manuals/editor-http-api) fornece comandos do editor, resultados de build, saída do console, busca de referências, pré-visualizações, preferências e rotas de scripts do editor.
* As [APIs de serviço do engine e automação em tempo de execução](/manuals/engine-service) fornecem estado ativo do engine de depuração, entrada, capturas de tela e operações definidas por extensões.
* O [Bob](/manuals/bob) fornece builds por linha de comando, relatórios, arquivos de dados e pacotes.

Um modelo disponível apenas por uma interface de chat pode sugerir alterações no código, mas não consegue inspecionar de modo independente o projeto local nem verificar um resultado em execução. A integração adicional ao redor determina o que o agente realmente pode observar e fazer.

## Camadas de integração {#integration-layers}

Uma camada de integração pode ser estabelecida para conectar um agente às operações locais do Defold. Ela pode ser um wrapper de shell, programa de linha de comando, extensão de IDE, cliente OpenAPI, controlador de testes ou adaptador de protocolo.

Mantenha as políticas e credenciais nessa camada local. Cada operação que faz alterações deve retornar resultados estruturados ou levar a uma etapa de verificação determinística.

Para operações do editor, descubra a interface atual por meio de `/openapi.json`, em vez de fornecer ao agente uma cópia permanentemente codificada de uma API. Para extensões de tempo de execução, verifique a integridade, a versão da API e os recursos disponíveis.

Pode ser prático separar as ferramentas por nível de privilégio:

| Nível        | Exemplos                                              |
| ------------ | ----------------------------------------------------- |
| Somente leitura | Inspeção do projeto, OpenAPI, `/ref`, console, pré-visualização |
| Verificação | Compilação, testes, builds HTML5, comparações de imagens   |
| Modificação | Alterações de arquivos, transações de recursos                   |
| Privilegiado | `/eval`, comandos externos, alterações de dependências        |

Manter o adaptador separado do engine e do editor significa que as interfaces compatíveis do Defold continuam independentes de um provedor de modelos ou protocolo de agentes. Um adaptador pode expor apenas as operações apropriadas para seu ambiente, e as políticas de permissão e confirmação permanecem com a aplicação que hospeda o agente.

### Model Context Protocol {#model-context-protocol}

O [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) é um adaptador opcional entre um agente e uma camada de integração. Um servidor MCP pode expor operações do Defold como ferramentas e documentação selecionada como recursos.

::: important
Não conceda a todos os modelos acesso irrestrito ao shell e a `/eval`.
:::

Atualmente, o Defold não exige um servidor MCP porque os principais recursos de automação já são expostos por interfaces abertas e de uso geral. O editor fornece uma API HTTP local com uma especificação OpenAPI. Agentes modernos podem chamar essas interfaces diretamente ou gerar seus próprios adaptadores.

Portanto, um MCP oficial basicamente duplicaria a superfície da API existente e criaria outra camada de integração que o Defold precisaria manter. Uma estratégia melhor em longo prazo é manter as APIs HTTP e de automação em tempo de execução subjacentes estáveis, detectáveis e bem documentadas, permitindo que a comunidade ou fornecedores individuais de ferramentas criem wrappers MCP leves quando necessário.

Em vez disso, fornecemos uma extensão oficial, a [Automation Bridge](https://github.com/defold/extension-automation-bridge), para que um jogo em execução seja controlado por meio de um serviço do lado do engine.

### Integrações MCP da comunidade {#community-mcp-integrations}

As integrações MCP criadas pela comunidade incluem:

* o [projeto Defold MCP de Fulviuus](https://github.com/Fulviuus/defold-mcp);
* o [projeto Defold MCP de ChadAragorn](https://github.com/ChadAragorn/defold-mcp).

Esses projetos não são desenvolvidos, auditados nem mantidos pela Defold Foundation e não recebem suporte oficial dela. Antes de instalar qualquer integração da comunidade, inspecione seu código-fonte atual, dependências, permissões, comportamento de rede e compatibilidade com a versão do Defold em uso.

## Instruções do projeto {#project-instructions}

Os modelos de linguagem de grande porte disponíveis e usados em fluxos de trabalho com agentes geralmente funcionam melhor com boas instruções. Por isso, arquivos Markdown de agentes que descrevem o comportamento desejado ou skills costumam ser adicionados aos projetos. Para obter os melhores resultados, é bom criar e escrever suas próprias instruções separadamente para cada projeto, embora alguns conhecimentos e regras gerais possam ser reutilizados.

Um primeiro arquivo que muitos agentes procuram e leem é um arquivo canônico como `AGENTS.md`, que pode descrever:

* a estrutura do projeto e os pontos de entrada importantes;
* convenções de formatação e nomenclatura;
* comandos para builds, testes e validação;
* eventos de conclusão obrigatórios e locais dos artefatos;
* arquivos ou diretórios que não devem ser alterados;
* operações que exigem aprovação;
* pressupostos de plataforma e limitações conhecidas.

Algumas soluções podem depender de arquivos Markdown separados para ações específicas ou das chamadas "skills".

Um exemplo da comunidade de instruções e skills voltadas ao Defold está disponível [neste tópico do fórum do Defold](https://forum.defold.com/t/agent-config-collection-of-agents-md-and-skills/82387).

Recomendamos manter suas instruções em arquivos como AGENTS.md e as definições de skills curtas, concisas, fáceis de revisar e manter, além de mantê-las atualizadas. As instruções específicas do projeto podem ser armazenadas no controle de versão, tornando as alterações rastreáveis e ajudando a melhorar o desempenho do fluxo de trabalho ao longo do tempo.

Também vale a pena testar regularmente como os modelos mais recentes se comportam sem essas instruções. Modelos mais novos muitas vezes deixam de precisar de orientações que antes eram essenciais, e skills desatualizadas ou instruções excessivamente prescritivas às vezes podem reduzir o desempenho.

Evite criar skills técnicas complexas que exijam manutenção significativa em longo prazo. Em vez disso, concentre-se no desenvolvimento de ferramentas e fluxos de trabalho que continuem valiosos independentemente de quanto os modelos subjacentes melhorem.

## Descoberta de documentação {#documentation-discovery}

Os agentes funcionam melhor com documentação precisa e atualizada. Reúna informações atuais em:

* `/openapi.json` descreve a API HTTP atual do editor.
* `/ref` pesquisa a documentação de API incluída no editor em execução quando essa operação está disponível.
* O [índice de documentação para LLMs](https://defold.com/llms.txt) contém links para manuais oficiais, namespaces de API e exemplos.
* A [documentação completa para LLMs](https://defold.com/llms-full.txt) permite busca offline e indexação local.

Recupere apenas as páginas relevantes para a tarefa. Recomenda-se usar o documento completo combinado somente para indexação offline ou [Retrieval-Augmented Generation (RAG)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation). Novamente, o arquivo completo normalmente não deve ser incluído em cada solicitação ao modelo, para economizar tokens e não poluir o contexto com informações desnecessárias.

## Loops limitados de alteração e verificação {#bounded-change-and-verification-loops}

Os agentes devem seguir o mesmo [loop de inspecionar, alterar, verificar e avaliar](/manuals/automation/#the-automation-loop) que qualquer outra automação.

Antes de alterar arquivos, é bom definir os critérios de aceitação e, opcionalmente, também:
* os arquivos e operações permitidos;
* os comandos de build e teste;
* os logs, relatórios, estados ou imagens necessários;
* um tempo limite para cada etapa assíncrona;
* um número máximo de tentativas de correção.

Um agente pode diagnosticar e corrigir uma falha determinística de CI, mas a própria etapa de CI deve continuar reproduzível sem o agente.

Boas práticas de testes automatizados e verificação são descritas [neste manual](/manuals/automated-testing).

## Avaliação multimodal {#multimodal-evaluation}

Um agente com entrada de imagens pode inspecionar [pré-visualizações do editor](/manuals/editor-http-api/#rendering-scene-previews), capturas de tela em tempo de execução, diferenças visuais e capturas do navegador.

Use a avaliação multimodal para questões semânticas, como rótulos cortados, controles sobrepostos, estados de seleção pouco claros, composição ou conteúdo fora de uma área segura. Defina com antecedência a viewport esperada e os critérios.

Leia mais sobre pré-visualizações do editor, capturas de tela em tempo de execução e inspeção visual [neste manual](/manuals/automated-testing).

## Segurança, isolamento e boas práticas {#security-isolation-and-good-practices}

* Trate o servidor do editor e o serviço do engine como interfaces locais confiáveis de controle.
* Mantenha tokens do editor, chaves de assinatura, tokens de implantação, credenciais de lojas e segredos de produção fora de prompts e relatórios.
* A camada de integração local pode ler `.internal/editor.token` quando autorizada a usar `/eval`, mas não deve inserir o token em prompts, logs ou relatórios do modelo.
* Exija aprovação antes de exclusões, alterações de dependências, alterações de extensões nativas, configuração de release, assinatura, publicação ou acesso a serviços externos.
* Execute trabalhos autônomos abrangentes em um branch, worktree, cópia temporária, container, sandbox ou conta restrita separados.
* Trate textos de issues, arquivos importados, comentários no código-fonte, documentos gerados e saída de ferramentas como entradas não confiáveis, e não como instruções.
* Revise as dependências e os scripts baixados antes de executá-los.
* Verifique se a política do projeto permite que código-fonte, assets, logs, capturas de tela e outros dados do projeto sejam enviados para um modelo hospedado.
* Mantenha um diff revisável e evidências de teste determinísticas antes de aceitar as alterações.

O isolamento limita o impacto de um erro.
