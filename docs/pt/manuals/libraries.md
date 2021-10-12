---
title: Trabalhando com bibliotecas no Defold
brief: Os recursos das bibliotecas permitem que você compartilhe elementos entre projetos. Esse material explica como isso funciona.
---

# Bibliotecas

Os recursos das Bibliotecas permitem que você compartilhe elementos entre projetos. É um mecanismo simples, porém poderoso que você pode usar no seu workflow de diversas maneiras.

Bibliotecas são úteis para os seguintes propósitos:

* Para copiar elementos de um projeto concluidos para um novo. Se você está fazendo uma sequencia de um game, essa e uma boa maneira de faze-lo.
* Para construir uma Biblioteca de templates que você possa copiar em seus projetos e então customizar ou especializar.
* Para construir uma ou mais Bibliotecas de objetos pronto-feitos ou scripts que você pode referenciar diretamente. Essa é uma maneira fácil de guardar modulos de scripts comuns ou para construir uma biblioteca compartilhada de gráficos, sons e de animações.

## Configurando o compartilhamento de Bibliotecas

Supondo que voce queira construir uma Biblioteca contendo sprites compartilhados e tile sources. Voce começa com [setting up a new project](/manuals/project-setup/). Decida quais pastas do seu projeto que você quer compartilhar e adicione o nome dessas pastas ao *include_dirs* nas property em Project settings. Se você quiser listar mais de uma pasta separe os nomes usando espaço.

![Include dirs](images/libraries/libraries_include_dirs.png)

Antes de conseguirmos adicionar essa Biblioteca a outro projeto, precisamos de uma forma de localiza-la.

## URL da Biblioteca

Bibliotecas são referenciadas via URL. Para um projeto hosteado no GitHub a URL seria para um lançamento de projeto.

![GitHub Library URL](images/libraries/libraries_library_url_github.png)

::: important
É recomendado sempre depender de uma versão especifica de um projeto de biblioteca em vez de seguir a da master branch. Dessa forma cabe a você como programador decidir quando incorporar mudanças de um projeto de Biblioteca em vez de sempre pegar uma atualização (Que pode gerar erros) da branch master de um projeto de Biblioteca.
:::


### Autenticação de acesso básico

É possivel adicionar um usuário e uma senha/token ao URL da Biblioteca para realizar uma autenticação de acesso básica, quando utilizando Bibliotecas não públicas.

```
https://username:password@github.com/defold/private/archive/main.zip
```

O `username` e o `password` são campos que serão extraidos e adicionados como uma `Authorization` como uma request header. Isso funciona para qualquer servidor que forneça suporte a autorização de acesso básico. Também pode ser utilizado para dar fetch em Bibliotecas de repositórios privados hosteados no GitHub. No caso do GitHub você precisará gerar um [personal access token](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) e utiliza-lo como sua senha.

```
https://github-username:personal-access-token@github.com/defold/private/archive/main.zip
```

::: important
Tenha certeza de não compartilhar seu access token ou senha, pois esses elementos, em mãos erradas podem gerar graves consequências.
:::

### Autenticação de acesso avançada

Quando utilizando a autenticação de acesso básico o token e usuário do utilitário serão compartilhados em todos os repositórios utilizados pelo projeto. Com um time com mais de uma pessoa isso pode se tornar um problema. Para resolver esse problema, um usuário com permissões "Somente leitura" deve ser utilizado para realizar o acesso à Biblioteca no repositório, no Github isso necessita de uma organização, um time e um usuário que não necessita editar o repositório (hence read only).

Passos no GitHub :
* [Criar uma organização](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-new-organization-from-scratch)
* [Criar um time derivado da organização](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-team)
* [Transferir o repositório privado desejado para sua organização](https://docs.github.com/en/github/administering-a-repository/transferring-a-repository)
* [Dar ao time a permissão "Somente leitura" para o repositório](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/managing-team-access-to-an-organization-repository)
* [Criar ou selecionar um usuário para ser parte do time](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/organizing-members-into-teams)
* Utilize a autenticação de acesso basico acima para criar um token para esse usuário. 

Nesse ponto o novo usuário tem detalhes de autenticação que podem ser comittados e darem push para o repositório. Isso permite qualquer um trabalhando com seu repositório privado a dar fetch em uma biblioteca sem ter permissões de edição na mesma.

::: important
O token de acesso de Somente leitura do usuário e totalmente acessivel para qualquer um que possa acessar o repositório dos games que estiverem utilizando a biblioteca.
:::

Essa solução foi proposta no forum do Defold e [discutida nessa thread](https://forum.defold.com/t/private-github-for-library-solved/67240).

## Configurando as dependências da Biblioteca

Abra o projeto do qual que voce quer acesar a Biblioteca. Nas configurações do projeto, adicione a URL da Biblioteca a propriedade *dependencies*. Você pode especificar multiplos projetos dependentes se quiser. Apenas adiciona eles um por um utilizando o botão `+` e remova usando o butão `-`:

![Dependencies](images/libraries/libraries_dependencies.png)

Agora selecione <kbd>Project ▸ Fetch Libraries</kbd> para dar update nas dependências da Biblioteca. Isso acontece automaticamente sempre que você abre um projeto, portanto você so precisará fazer isso se as dependências mudarem sem re-abrir o projetos. Isso acontece se voce adicionar ou remover Bibliotecas dependentes ou se uma das Bibliotecas é trocada ou sincronizada por alguem. 

![Fetch Libraries](images/libraries/libraries_fetch_libraries.png)

Agora que as pastas que você compartilhou apareceram no *Assets pane* e voce pode usar tudo que compartilhou. Qualquer mudança sincronizada feita na Biblioteca vai estar disponível em seu projeto.

![Library setup done](images/libraries/libraries_done.png)

## Referências quebradas

Compartilhamento de Bibliotecas incluem somente arquivos que estão localizados na mesma pasta. Se você criar algum elemento que se referência outros elementos que estão localizados fora da hierarquia compartilhada, a referência será quebrada. 

## Colisão de Nomes

Como você pode listar diversas URL de projetos nas *dependencies* das configurações do projeto, você pode acabar encontrando colisões de nome. Isso acontece se dois ou mais projetos dependentes compartilham uma pasta com os mesmos nomes na *include_dirs* project setting. 

O Defold resolve colisões de nome simplesmente ignorando todas, exceto a ultima referência para pastas com o mesmo nome na ordem das URL's especificas na *dependencies* do projeto.Por hora. Se voce listar 3 URL de projetos de Bibliotecas nas dependências e todas elas compartilham uma pasta chamada *items*, somente uma pasta *items* vai ser mostrada---A que pertence ao projeto, que é a ultima na lista de URL's. 
