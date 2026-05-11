---
title: Refatoração
brief: Este manual aborda como você pode alterar facilmente a estrutura do seu projeto com a ajuda de uma refatoração poderosa.
---

# Refatoração

Refatoração se refere ao processo de reestruturar código e assets existentes. Durante o desenvolvimento de um projeto, a necessidade de alterar ou mover coisas frequentemente aparece: nomes precisam mudar para seguir convenções de nomenclatura ou melhorar a clareza, e arquivos de código ou assets precisam ser movidos para um lugar mais lógico na hierarquia do projeto.

O Defold ajuda você a refatorar com eficiência mantendo controle de como os assets são usados. Ele atualiza automaticamente referências a assets que são renomeados e/ou movidos. Como desenvolvedor, você deve se sentir livre no seu trabalho. Seu projeto é uma estrutura flexível que você pode alterar à vontade sem temer que tudo quebre.

::: important
A refatoração automática só funcionará se as mudanças forem feitas dentro do editor. Se você renomear ou mover um arquivo fora do editor, quaisquer referências a esse arquivo não serão alteradas automaticamente.
:::

No entanto, se você quebrar uma referência, por exemplo excluindo um asset, o editor não conseguirá resolver o problema, mas fornecerá sinais de erro úteis. Por exemplo, se você excluir uma animação de um atlas e essa animação estiver em uso em algum lugar, o Defold sinalizará um erro quando você tentar iniciar o jogo. O editor também marcará onde os erros ocorrem para ajudar você a localizar rapidamente o problema:

![Refactoring error](images/workflow/delete_error.png)

Erros de build aparecem no painel *Build Errors* na parte inferior do editor. <kbd>Clicar duas vezes</kbd> em um erro leva você ao local do problema.
