---
title: Controle de versão
brief: Este manual aborda como trabalhar com o sistema integrado de controle de versão.
---

# Controle de versão

O Defold é construído para pequenas equipes que trabalham em colaboração intensa para criar jogos. Integrantes da equipe podem trabalhar em paralelo no mesmo conteúdo com pouquíssimo atrito. O Defold tem suporte integrado a controle de versão usando [Git](https://git-scm.com). O Git foi projetado para trabalho colaborativo distribuído e é uma ferramenta extremamente poderosa que permite uma grande variedade de fluxos de trabalho.

## Arquivos alterados

Quando você salva alterações na sua cópia de trabalho local, o Defold rastreia todas as alterações no painel *Changed Files* do editor, listando cada arquivo que foi adicionado, excluído ou modificado.

![changed files](images/workflow/changed_files.png)

Selecione um arquivo na lista e clique em <kbd>Diff</kbd> para ver as alterações que você fez no arquivo, ou em <kbd>Revert</kbd> para desfazer todas as alterações e restaurar o arquivo ao estado que tinha após a última sincronização.

## Git

O Git foi criado principalmente para lidar com código-fonte e arquivos de texto, e armazena esses tipos de arquivos com um uso de espaço muito baixo. Apenas as alterações entre cada versão são armazenadas, o que significa que você pode manter um histórico extenso de alterações em todos os arquivos do projeto a um custo relativamente pequeno. Arquivos binários, como imagens ou sons, porém, não se beneficiam do esquema de armazenamento do Git. Cada nova versão que você registra e sincroniza ocupa aproximadamente o mesmo espaço. Isso normalmente não é um grande problema com assets finais do projeto (imagens JPEG ou PNG, arquivos de som OGG etc), mas pode rapidamente se tornar um problema com arquivos de trabalho do projeto (arquivos PSD, projetos Protools etc). Esses tipos de arquivo costumam crescer muito, já que geralmente são trabalhados em resolução muito maior que os assets finais. Em geral, considera-se melhor evitar colocar arquivos de trabalho grandes sob controle do Git e, em vez disso, usar uma solução separada de armazenamento e backup para eles.

Há muitas formas de usar Git em um fluxo de trabalho de equipe. A forma usada pelo Defold é a seguinte. Quando você sincroniza, acontece o seguinte:

1. Quaisquer alterações locais são guardadas em stash para que possam ser restauradas se algo falhar mais tarde no processo de sincronização.
2. Alterações do servidor são baixadas.
3. O stash é aplicado (as alterações locais são restauradas), o que pode resultar em conflitos de merge que precisam ser resolvidos.
4. O usuário recebe a opção de commitar quaisquer alterações locais de arquivos.
5. Se houver commits locais, o usuário pode optar por enviá-los ao servidor. Novamente, é possível que isso leve a conflitos que precisem ser resolvidos.

Se preferir um fluxo de trabalho diferente, você pode executar Git pela linha de comando ou por uma aplicação de terceiros para fazer pulls, pushes, commits e merges, trabalhar em vários branches e assim por diante.
