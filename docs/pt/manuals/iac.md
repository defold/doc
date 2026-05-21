---
title: Comunicação entre aplicativos no Defold
brief: A comunicação entre aplicativos permite capturar os argumentos de inicialização usados ao iniciar sua aplicação. Este manual explica a API do Defold disponível para essa funcionalidade.
---

# Comunicação entre aplicativos

Na maioria dos sistemas operacionais, aplicações podem ser iniciadas de várias formas:

* A partir da lista de aplicações instaladas
* A partir de um link específico da aplicação
* A partir de uma notificação push
* Como etapa final de um processo de instalação.

Quando a aplicação é iniciada por um link, notificação ou quando instalada, é possível passar argumentos adicionais, como um install referrer durante a instalação ou um deep link ao iniciar por um link específico da aplicação ou por uma notificação. O Defold fornece uma forma unificada de obter as informações sobre como a aplicação foi invocada usando uma extensão nativa.

## Instalando a extensão

Para começar a usar a extensão Inter-app communication, você precisa adicioná-la como dependência ao arquivo *game.project*. A versão estável mais recente está disponível com a URL de dependência:
```
https://github.com/defold/extension-iac/archive/master.zip
```

Recomendamos usar um link para um arquivo zip de uma [release específica](https://github.com/defold/extension-iac/releases).

## Usando a extensão

A API é muito fácil de usar. Você fornece à extensão uma função listener e reage aos callbacks do listener.

```
local function iac_listener(self, payload, type)
     if type == iac.TYPE_INVOCATION then
         -- Esta foi uma invocação
         print(payload.origin) -- origin pode ser uma string vazia se não puder ser resolvido
         print(payload.url)
     end
end

function init(self)
     iac.set_listener(iac_listener)
end
```

A documentação completa da API está disponível na [página da extensão no GitHub](https://defold.github.io/extension-iac/).
