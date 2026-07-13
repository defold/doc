---
title: Configuração de projeto
brief: Este manual aborda como criar ou abrir um projeto no Defold.
---

# Configuração de projeto

Você pode criar facilmente um novo projeto dentro do editor Defold. Também tem a opção de abrir um projeto existente já localizado no seu computador.

## Criando um novo projeto local {#creating-a-new-project}

Clique na opção <kbd>New Project</kbd> e selecione que tipo de projeto você deseja criar. Especifique um local no seu disco rígido onde os arquivos do projeto serão armazenados. Clique em <kbd>Create New Project</kbd> para criar o projeto no local escolhido. Você pode criar um novo projeto a partir de um Template:

![open project](images/workflow/open_project.png)

Ou a partir de um Tutorial com instruções passo a passo:

![create project from tutorial](images/workflow/create_from_tutorial.png)

Ou a partir de um jogo Sample concluído:

![create project from sample](images/workflow/create_from_sample.png)

### Adicionando o projeto ao GitHub

Um projeto local não tem integração com nenhum sistema de controle de versão, o que significa que os arquivos residem apenas no seu disco rígido e não há um histórico que permita reverter alterações. Arquivos excluídos pelo painel Assets do editor são movidos para a Lixeira do sistema quando há suporte, mas podem ser excluídos permanentemente se essa operação não estiver disponível ou falhar. A Lixeira não protege edições arbitrárias nem fornece um histórico de versões; portanto, recomenda-se usar um sistema de controle de versão como Git para acompanhar alterações nos seus arquivos. Isso também torna muito fácil colaborar em um projeto com outras pessoas. Enviar um projeto local para o GitHub pode ser feito em poucos passos:

1. Crie ou faça login em uma conta no [GitHub](https://github.com/)
2. Crie um repositório usando a opção [New Repository](https://help.github.com/en/articles/creating-a-new-repository)
3. Envie todos os arquivos do projeto pela opção [Upload Files](https://help.github.com/en/articles/adding-a-file-to-a-repository)

O projeto agora está sob controle de versão e você deve [clonar o projeto](https://help.github.com/en/articles/cloning-a-repository) para seu disco rígido local e trabalhar a partir desse novo local.

## Abrir um projeto existente

Clique na opção <kbd>Open From Disk</kbd> para abrir um projeto já localizado no seu computador.

![import project](images/workflow/open_from_disk.png)

## Abrir um projeto recente

Depois que um projeto foi aberto uma vez, ele aparecerá na lista de projetos recentes. A lista mostrará os projetos em que você trabalhou mais recentemente e permitirá abrir rapidamente qualquer um deles clicando duas vezes no projeto na lista.
