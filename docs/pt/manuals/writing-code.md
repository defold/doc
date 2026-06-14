---
title: Escrevendo código
brief: Este manual aborda brevemente como trabalhar com código no Defold.
---

# Escrevendo código

Embora o Defold permita criar muito conteúdo do seu jogo usando ferramentas visuais, como os editores de tilemap e efeitos de partículas, você ainda cria a lógica do jogo usando um editor de código. A lógica do jogo é escrita usando a [linguagem de programação Lua](https://www.lua.org/), enquanto extensões para a própria engine são escritas usando a(s) linguagem(ns) nativa(s) da plataforma-alvo.

## Escrevendo código Lua

O Defold usa Lua 5.1 e LuaJIT (dependendo da plataforma-alvo), e você precisa seguir a especificação da linguagem para essas versões específicas de Lua ao escrever a lógica do jogo. Para mais detalhes sobre como trabalhar com Lua no Defold, veja nosso [manual Lua no Defold](/manuals/lua).

## Usando outras linguagens que transpilem para Lua

O Defold suporta o uso de transpilers que emitem código Lua. Com a extensão de transpiler instalada, você pode usar linguagens alternativas - como [Teal](https://github.com/defold/extension-teal) - para escrever Lua com verificação estática. É um recurso em preview que tem limitações: o suporte atual a transpiler não expõe as informações sobre módulos e funções definidas no runtime Lua do Defold. Isso significa que usar APIs do Defold como `go.animate` exigirá que você escreva definições externas por conta própria.

## Escrevendo código nativo

O Defold permite estender a engine de jogos com código nativo para acessar funcionalidades específicas de plataforma não fornecidas pela própria engine. Você também pode usar código nativo quando o desempenho de Lua não for suficiente (cálculos intensivos, processamento de imagens etc). Consulte nossos [manuais sobre Native Extensions](/manuals/extensions/) para saber mais.

## Usando o editor de código integrado

O Defold tem um editor de código integrado que permite abrir e editar arquivos Lua (.lua), arquivos de script do Defold (.script, .gui_script e .render_script), assim como qualquer outro arquivo com uma extensão não tratada nativamente pelo editor. Além disso, o editor fornece destaque de sintaxe para arquivos Lua e scripts.

![](/images/editor/code-editor.png)


### Autocompletar código

O editor de código integrado mostrará autocompletar de funções enquanto você escreve código:

![](/images/editor/codecompletion.png)

Pressionar <kbd>CTRL</kbd> + <kbd>Space</kbd> mostrará informações adicionais sobre funções, argumentos e valores de retorno:

![](/images/editor/apireference.png)

### Configuração de linting {#linting-configuration}

O editor de código integrado realiza linting de código usando [Luacheck](https://luacheck.readthedocs.io/en/stable/index.html) e [Lua language server](https://luals.github.io/wiki/diagnostics/). Para configurar o Luacheck, crie um arquivo `.luacheckrc` na raiz do projeto. Você pode ler a [página de configuração do Luacheck](https://luacheck.readthedocs.io/en/stable/config.html) para ver a lista de opções disponíveis. O Defold usa os seguintes padrões para a configuração do Luacheck:

```lua
unused_args = false      -- não avisa sobre argumentos não usados (comum em arquivos .script)
max_line_length = false  -- não avisa sobre linhas longas
ignore = {
    "611",               -- linha contém apenas whitespace
    "612",               -- linha contém whitespace no fim
    "614"                -- whitespace no fim de um comentário
},
```

## Usando um editor de código externo

O editor de código do Defold fornece a funcionalidade básica necessária para escrever código, mas para casos de uso mais avançados ou para usuários experientes com um editor de código favorito, é possível fazer o Defold abrir arquivos usando um editor externo. Na [janela Preferences na aba Code](/manuals/editor-preferences/#code), é possível definir um editor externo que deve ser usado ao editar código.

### Visual Studio Code - Defold Kit

Defold Kit é um plugin do Visual Studio Code com os seguintes recursos:

* Instalação de extensões recomendadas
* Destaque de Lua, autocompletar e linting
* Aplicação de configurações relevantes ao workspace
* Anotações Lua para a API do Defold
* Anotações Lua para dependências
* Build e execução
* Depuração com breakpoints
* Empacotamento para todas as plataformas
* Implantação em dispositivos móveis conectados

Saiba mais e instale o Defold Kit pelo [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=astronachos.defold).


## Software de documentação

Pacotes de referência de API criados pela comunidade estão disponíveis para [Dash e Zeal](https://forum.defold.com/t/defold-docset-for-dash/2417).
