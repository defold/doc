---
title: Trabalhando com projetos de biblioteca no Defold
brief: O recurso de Bibliotecas permite compartilhar assets entre projetos. Este manual explica como ele funciona.
---

# Bibliotecas

O recurso de Bibliotecas permite compartilhar assets entre projetos. É um mecanismo simples, mas muito poderoso, que você pode usar no seu fluxo de trabalho de várias maneiras.

Bibliotecas são úteis para os seguintes fins:

* Copiar assets de um projeto concluído para um novo. Se você está fazendo uma sequência de um jogo anterior, esta é uma forma fácil de começar.
* Criar uma biblioteca de modelos que você pode copiar para seus projetos e depois personalizar ou especializar.
* Criar uma ou mais bibliotecas de objetos prontos ou scripts que você pode referenciar diretamente. Isso é muito prático para armazenar módulos de script comuns ou criar uma biblioteca compartilhada de gráficos, sons e assets de animação.

## Configurando o compartilhamento de bibliotecas

Suponha que você queira criar uma biblioteca contendo sprites e tile sources compartilhados. Comece [configurando um novo projeto](/manuals/project-setup/). Decida quais pastas do projeto você quer compartilhar e adicione os nomes dessas pastas à propriedade *`include_dirs`* nas configurações do projeto. Se quiser listar mais de uma pasta, separe os nomes com espaços:

![Include directories](images/libraries/libraries_include_dirs.png)

Antes de adicionar essa biblioteca a outro projeto, precisamos de uma forma de localizar a biblioteca.

## URL da biblioteca

Bibliotecas são referenciadas por uma URL padrão. Para um projeto hospedado no GitHub, essa seria a URL de uma release do projeto:

![GitHub Library URL](images/libraries/libraries_library_url_github.png)

::: important
É recomendável sempre depender de uma release específica de um projeto de biblioteca, em vez da branch `master`. Assim, cabe a você, como desenvolvedor, decidir quando incorporar mudanças de um projeto de biblioteca, em vez de sempre receber as alterações mais recentes (e potencialmente incompatíveis) da branch `master` desse projeto.
:::

::: important
É recomendável sempre revisar bibliotecas de terceiros antes de usá-las. Saiba mais sobre [como proteger o uso de software de terceiros](https://defold.com/manuals/application-security/#securing-your-use-of-third-party-software).
:::

### Autenticação de acesso básico

É possível adicionar um nome de usuário e senha/token à URL da biblioteca para realizar autenticação de acesso básico ao usar bibliotecas que não estão disponíveis publicamente:

```
https://username:password@github.com/defold/private/archive/main.zip
```

Os campos `username` e `password` serão extraídos e adicionados como um cabeçalho de requisição `Authorization`. Isso funciona para qualquer servidor com suporte a autorização de acesso básico.

::: important
Certifique-se de não compartilhar nem vazar acidentalmente seu personal access token ou senha gerados, pois isso pode ter consequências graves se caírem em mãos erradas.
:::

Para evitar o vazamento acidental de credenciais em texto claro na URL da biblioteca, também é possível usar um padrão de substituição de strings e armazenar as credenciais como variáveis de ambiente:

```
https://__PRIVATE_USERNAME__:__PRIVATE_TOKEN__@github.com/defold/private/archive/main.zip
```

No exemplo acima, o nome de usuário e o token serão lidos das variáveis de ambiente do sistema `PRIVATE_USERNAME` e `PRIVATE_TOKEN`.

#### Autenticação no GitHub

Para buscar de um repositório privado no GitHub, você precisa [gerar um personal access token](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) e usá-lo como senha.

```
https://github-username:personal-access-token@github.com/defold/private/archive/main.zip
```

#### Autenticação no GitLab

Para buscar de um repositório privado no GitLab, você precisa [gerar um personal access token](https://docs.gitlab.com/ee/security/token_overview.html) e enviá-lo como parâmetro de URL.

```
https://gitlab.com/defold/private/-/archive/main/test-main.zip?private_token=personal-access-token
```

### Autenticação de acesso avançada

Ao usar autenticação de acesso básico, o token de acesso e o nome de usuário de um usuário serão compartilhados em qualquer repositório usado pelo projeto. Em uma equipe com mais de uma pessoa, isso pode ser um problema. Para resolver isso, um usuário "somente leitura" deve ser usado para acesso da biblioteca ao repositório. No GitHub, isso exige uma organização, uma equipe e um usuário que não precise editar o repositório (portanto, somente leitura).

Etapas no GitHub:
* [Criar uma organização](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-new-organization-from-scratch)
* [Criar uma equipe dentro da organização](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-team)
* [Transferir o repositório privado desejado para sua organização](https://docs.github.com/en/github/administering-a-repository/transferring-a-repository)
* [Dar à equipe acesso "somente leitura" ao repositório](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/managing-team-access-to-an-organization-repository)
* [Criar ou selecionar um usuário para fazer parte dessa equipe](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/organizing-members-into-teams)
* Usar a "autenticação de acesso básico" acima para criar um personal access token para esse usuário.

Nesse ponto, os dados de autenticação do novo usuário podem ser commitados e enviados ao repositório. Isso permite que qualquer pessoa trabalhando com seu repositório privado busque-o como biblioteca sem ter permissão para editar a própria biblioteca.

::: important
O token do usuário somente leitura fica totalmente acessível a qualquer pessoa que tenha acesso aos repositórios de jogos que usam a biblioteca.
:::

Essa solução foi proposta no fórum do Defold e [discutida nesta thread](https://forum.defold.com/t/private-github-for-library-solved/67240).

## Configurando dependências de biblioteca {#setting-up-library-dependencies}

Abra o projeto a partir do qual você quer acessar a biblioteca. Nas configurações do projeto, adicione a URL da biblioteca à propriedade *dependencies*. Você pode especificar vários projetos dependentes se quiser. Basta adicioná-los um por um usando o botão `+` e removê-los usando o botão `-`:

![Dependencies](images/libraries/libraries_dependencies.png)

Agora selecione <kbd>Project ▸ Fetch Libraries</kbd> para atualizar as dependências de biblioteca. Isso acontece automaticamente sempre que você abre um projeto, então você só precisa fazer isso se as dependências mudarem sem reabrir o projeto. Isso acontece se você adicionar ou remover bibliotecas dependentes, ou se um dos projetos de biblioteca dependentes for alterado e sincronizado por alguém.

![Fetch Libraries](images/libraries/libraries_fetch_libraries.png)

Agora as pastas que você compartilhou aparecem no *Assets pane*, e você pode usar tudo o que compartilhou. Qualquer alteração sincronizada feita no projeto de biblioteca ficará disponível no seu projeto.

![Library setup done](images/libraries/libraries_done.png)

## Editando arquivos em dependências de biblioteca

Arquivos em bibliotecas não podem ser salvos. Você pode fazer alterações, e o editor conseguirá compilar com essas alterações, o que é útil para testes. No entanto, o arquivo em si permanece inalterado, e todas as modificações serão descartadas quando o arquivo for fechado.

Se quiser alterar arquivos de biblioteca, crie seu próprio fork da biblioteca e faça as alterações nele. Outra opção é copiar e colar a pasta inteira da biblioteca para o diretório do seu projeto e usar a cópia local. Nesse caso, sua pasta local vai sobrepor a dependência original, e o link da dependência deve ser removido de `game.project` (não se esqueça de escolher <kbd>Project ▸ Fetch Libraries</kbd> depois).

`builtins` também é uma biblioteca fornecida pela engine. Se quiser editar arquivos nela, copie-os para o seu projeto e use essas cópias no lugar dos arquivos `builtins` originais. Por exemplo, para modificar `default.render_script`, copie tanto `/builtins/render/default.render` quanto `/builtins/render/default.render_script` para a pasta do seu projeto como `my_custom.render` e `my_custom.render_script`. Depois, atualize o arquivo local `my_custom.render` para referenciar `my_custom.render_script` em vez do script embutido, e defina seu `my_custom.render` personalizado em `game.project`, na configuração Render.

Se você copiar e colar um material e quiser usá-lo em todos os componentes de um certo tipo, pode ser útil usar [modelos por projeto](/manuals/editor/#creating-new-project-files).

## Referências quebradas

O compartilhamento de bibliotecas inclui apenas arquivos localizados dentro das pastas compartilhadas. Se você criar algo que referencia assets localizados fora da hierarquia compartilhada, os caminhos de referência ficarão quebrados.

## Colisões de nomes

Como você pode listar várias URLs de projetos na configuração *dependencies* do projeto, pode encontrar uma colisão de nomes. Isso acontece se dois ou mais projetos dependentes compartilham uma pasta com o mesmo nome na configuração *`include_dirs`* do projeto.

O Defold resolve colisões de nomes simplesmente ignorando todas as referências a pastas de mesmo nome, exceto a última, na ordem em que as URLs dos projetos são especificadas na lista *dependencies*. Por exemplo, se você listar 3 URLs de projetos de biblioteca nas dependências e todos eles compartilharem uma pasta chamada *items*, apenas uma pasta *items* aparecerá: a que pertence ao projeto que está por último na lista de URLs.
