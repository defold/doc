---
title: Extensões nativas - SDK do Defold
brief: Este manual descreve como trabalhar com o SDK do Defold ao criar extensões nativas.
---

# O SDK do Defold

O SDK do Defold contém a funcionalidade necessária para declarar uma extensão nativa, além de fazer a interface com a camada nativa de baixo nível da plataforma em que a aplicação é executada e com a camada Lua de alto nível em que a lógica do jogo é criada.

## Uso

Você usa o SDK do Defold incluindo o arquivo de cabeçalho `dmsdk/sdk.h`:

    #include <dmsdk/sdk.h>

As funções e namespaces disponíveis do SDK estão documentados na nossa [referência da API](/ref/overview_cpp). Os cabeçalhos do SDK do Defold são incluídos como um arquivo separado `defoldsdk_headers.zip` para cada [release do Defold no GitHub](https://github.com/defold/defold/releases). Você pode usar esses cabeçalhos para autocompletar código no editor de sua escolha.
