---
title: Extensões nativas - SDK do Defold
brief: Este manual descreve como trabalhar com o SDK do Defold ao criar extensões nativas.
---

# O SDK do Defold

O SDK do Defold contém a funcionalidade necessária para declarar uma extensão nativa, além de fazer a interface com a camada nativa de baixo nível da plataforma em que a aplicação é executada e com a camada Lua de alto nível em que a lógica do jogo é criada.

## Uso

Extensões C++ podem incluir o arquivo de cabeçalho agregador `dmsdk/sdk.h`:

```cpp
#include <dmsdk/sdk.h>
```

O cabeçalho agregador inclui declarações C++ e não pode ser incluído em um arquivo-fonte C. Arquivos-fonte C devem incluir individualmente os cabeçalhos `.h` compatíveis com C de que precisam, por exemplo:

```c
#include <dmsdk/extension/extension.h>
#include <dmsdk/dlib/configfile.h>
#include <dmsdk/resource/resource.h>
```

Apenas parte do dmSDK possui atualmente uma interface C pura; nem todo subsistema C++ tem um equivalente em C. As funções e os tipos disponíveis estão documentados na [visão geral da API C](/ref/overview_defoldc/) e na [visão geral da API C++](/ref/overview_defoldcpp/). Os cabeçalhos do SDK do Defold são incluídos como um arquivo separado `defoldsdk_headers.zip` para cada [release do Defold no GitHub](https://github.com/defold/defold/releases). Você pode usar esses cabeçalhos para autocompletar código no editor de sua escolha.
