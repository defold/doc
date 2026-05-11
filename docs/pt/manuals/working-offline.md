---
title: Trabalhando offline
brief: Este manual descreve como trabalhar offline em projetos que contêm dependências e, em especial, extensões nativas
---

# Trabalhando offline

Na maioria dos casos, o Defold não exige conexão com a internet para funcionar. Porém, há algumas situações em que uma conexão com a internet é necessária:

* Atualizações automáticas
* Relatar problemas
* Buscar dependências
* Compilar extensões nativas


## Atualizações automáticas

O Defold verificará periodicamente se existem novas atualizações. As verificações de atualização do Defold são feitas no [site oficial de download](https://d.defold.com). Se uma atualização for detectada, ela será baixada automaticamente.

Se você só tem conexão com a internet por períodos limitados e não quer esperar a atualização automática ser acionada, pode baixar manualmente novas versões do Defold pelo [site oficial de download](https://d.defold.com).


## Relatando problemas

Se um problema for detectado no editor, você terá a opção de relatar o problema ao rastreador de issues do Defold. O rastreador de issues é [hospedado no GitHub](https://www.github.com/defold/editor2-issues), o que significa que você precisa de uma conexão com a internet para relatar o problema.

Se encontrar um problema enquanto estiver offline, você pode relatá-lo manualmente mais tarde usando a [opção Report Issue no menu Help](/manuals/getting-help/#report-a-problem-from-the-editor) do editor.


## Buscando dependências

O Defold suporta um sistema em que desenvolvedores podem compartilhar código e assets por meio de algo chamado [Library Projects](/manuals/libraries/). Bibliotecas são arquivos zip que podem ser hospedados em qualquer lugar online. Normalmente você encontra projetos de biblioteca do Defold no GitHub e em outros repositórios de código-fonte online.

Um projeto pode adicionar uma biblioteca como uma [dependência de projeto nas configurações do projeto](/manuals/project-settings/#dependencies). Dependências são baixadas/atualizadas quando o projeto é aberto ou sempre que a opção *Fetch Libraries* é selecionada no menu *Project*.

Se você precisa trabalhar offline e em vários projetos, pode baixar dependências com antecedência e então compartilhá-las usando um servidor local. Dependências no GitHub normalmente estão disponíveis na aba Releases do repositório do projeto:

![GitHub Library URL](images/libraries/libraries_library_url_github.png)

Você pode usar Python para criar facilmente um servidor local:

    python -m SimpleHTTPServer

Isso criará um servidor no diretório atual servindo arquivos em `localhost:8000`. Se o diretório atual contiver dependências baixadas, você poderá adicioná-las ao seu arquivo *game.project*:

    http://localhost:8000/extension-fbinstant-4.1.1.zip


## Compilando extensões nativas

O Defold suporta um sistema em que desenvolvedores podem adicionar código nativo para estender a funcionalidade da engine por meio de um sistema chamado [Native Extensions](/manuals/extensions/). O Defold fornece um ponto de entrada sem configuração para extensões nativas com uma solução de build baseada em nuvem.

Na primeira vez que você compila um projeto e o projeto contém uma extensão nativa, o código nativo será compilado em uma engine de jogo Defold personalizada nos servidores de build do Defold e enviado de volta ao seu PC. A engine personalizada será armazenada em cache no seu projeto e reutilizada em builds posteriores, desde que você não adicione, remova ou altere extensões nativas e desde que não atualize o editor.

Se você precisa trabalhar offline e seu projeto contém extensões nativas, certifique-se de compilar com sucesso pelo menos uma vez para garantir que seu projeto contenha uma cópia em cache da engine personalizada.
