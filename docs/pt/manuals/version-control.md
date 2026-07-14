---
title: Controle de versão
brief: Este manual aborda como usar Git com projetos Defold e inspecionar alterações locais no editor.
---

# Controle de versão

Projetos Defold funcionam bem com [Git](https://git-scm.com), mas a sincronização é feita fora do editor. Use seu cliente Git preferido ou a linha de comando para clonar, buscar, baixar, commitar e enviar alterações, criar branches e resolver conflitos.

## Arquivos alterados

Quando o diretório do projeto é a raiz de uma árvore de trabalho Git com pelo menos um commit, o Defold lista no painel *Changed Files* do editor os arquivos não ignorados detectados como adicionados, modificados, excluídos ou renomeados. Essas entradas são obtidas comparando diretamente os arquivos no disco com o commit atual (`HEAD`); portanto, preparar uma alteração para commit não modifica a lista. Resolva conflitos de merge em um cliente Git externo.

![changed files](images/workflow/changed_files.png)

Selecione exatamente um arquivo modificado ou renomeado e clique em <kbd>Diff</kbd> para ver seu diff de texto. Clique em <kbd>Revert</kbd> para descartar as alterações selecionadas na árvore de trabalho e no índice. Arquivos rastreados são restaurados para `HEAD`; arquivos ausentes de `HEAD` são excluídos, estejam ou não preparados como adições; e renomeações excluem o novo caminho e restauram o antigo. Isso não pode ser desfeito no editor; portanto, faça commit ou backup do trabalho de que talvez precise.

## Git

O Git armazena com eficiência os arquivos de projeto baseados em texto do Defold. Assets binários grandes que mudam com frequência, como arquivos PSD ou arquivos de produção de áudio, ainda podem fazer o histórico do repositório crescer rapidamente. Considere usar Git LFS ou uma solução separada de armazenamento e backup para arquivos de trabalho grandes.

O painel *Changed Files* fornece apenas operações locais de status, diff e reversão. Ele não sabe se os commits foram enviados a um repositório remoto e não busca, baixa, commita nem envia alterações. Execute essas operações em um cliente Git externo ou pela linha de comando. Por padrão, o Defold recarrega alterações externas e atualiza o painel quando volta a receber foco. Se *Load External Changes on App Focus* estiver desabilitada, selecione *File ▸ Load External Changes*.
