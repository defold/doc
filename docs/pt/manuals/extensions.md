---
title: Escrevendo extensões nativas para o Defold
brief: Este manual explica como escrever uma extensão nativa para a game engine Defold e como compilá-la pelos builders em nuvem sem configuração.
---

# Extensões nativas

Se você precisa de interação personalizada com software ou hardware externo em baixo nível, onde Lua não é suficiente, o SDK do Defold permite escrever extensões para a engine em C, C++, Objective C, Java ou Javascript, dependendo da plataforma-alvo. Casos de uso típicos para extensões nativas são:

- Interação com hardware específico, por exemplo a câmera em celulares.
- Interação com APIs externas de baixo nível, por exemplo APIs de redes de anúncios que não permitem interação por APIs de rede em que Luasocket poderia ser usado.
- Cálculos e processamento de dados de alto desempenho.

## O servidor de build

O Defold oferece um ponto de entrada sem configuração para extensões nativas com uma solução de build baseada em nuvem. Qualquer extensão nativa desenvolvida e adicionada a um projeto de jogo, diretamente ou por meio de um [projeto de biblioteca](/manuals/libraries/), passa a fazer parte do conteúdo comum do projeto. Não é necessário compilar versões especiais da engine e distribuí-las aos membros da equipe; isso é feito automaticamente: qualquer membro da equipe que compilar e executar o projeto receberá um executável da engine específico do projeto, com todas as extensões nativas incorporadas.

![Build em nuvem](images/extensions/cloud_build.png)

O Defold fornece o servidor de build em nuvem gratuitamente, sem restrições de uso. O servidor é hospedado na Europa, e a URL para a qual o código nativo é enviado é configurada na [janela de Preferências do Editor](/manuals/editor-preferences/#extensions) ou pela opção de linha de comando `--build-server` do [bob](/manuals/bob/#usage). Se quiser configurar seu próprio servidor, [siga estas instruções](/manuals/extender-local-setup).

## Estrutura do projeto

Para criar uma nova extensão, crie uma pasta na raiz do projeto. Essa pasta conterá todas as configurações, código-fonte, bibliotecas e recursos associados à extensão. O builder de extensão reconhece a estrutura de pastas e coleta todos os arquivos-fonte e bibliotecas.

```
 myextension/
 │
 ├── ext.manifest
 │
 ├── src/
 │
 ├── include/
 │
 ├── lib/
 │   └──[platforms]
 │
 ├── manifests/
 │   └──[platforms]
 │
 └── res/
     └──[platforms]

```
*ext.manifest*
: A pasta da extensão _deve_ conter um arquivo *ext.manifest*. Esse arquivo é um arquivo de configuração com flags e definições usadas ao compilar uma única extensão. A definição do formato do arquivo pode ser encontrada no [manual de manifesto de extensão](https://defold.com/manuals/extensions-ext-manifests/).

*src*
: Esta pasta deve conter todos os arquivos de código-fonte.

*include*
: Esta pasta opcional contém quaisquer arquivos de inclusão.

*lib*
: Esta pasta opcional contém quaisquer bibliotecas compiladas das quais a extensão depende. Os arquivos de biblioteca devem ser colocados em subpastas nomeadas por `platform`, ou `architecture-platform`, dependendo de quais arquiteturas suas bibliotecas aceitam.

  :[platforms](../shared/platforms.md)

*manifests*
: Esta pasta opcional contém arquivos adicionais usados no processo de build ou empacotamento. Veja abaixo os detalhes.

*res*
: Esta pasta opcional contém quaisquer recursos extras dos quais a extensão depende. Os arquivos de recurso devem ser colocados em subpastas nomeadas por `platform`, ou `architecture-platform`, assim como as subpastas de "lib". Uma subpasta `common` também é permitida, contendo arquivos de recurso comuns a todas as plataformas.

### Arquivos de manifesto

A pasta opcional *manifests* de uma extensão contém arquivos adicionais usados no processo de build e empacotamento. Os arquivos devem ser colocados em subpastas nomeadas por `platform`:

* `android` - Esta pasta aceita um arquivo stub de manifesto a ser mesclado na aplicação principal ([conforme descrito aqui](/manuals/extensions-manifest-merge-tool)).
  * A pasta também pode conter um arquivo `build.gradle` com dependências a serem [resolvidas pelo Gradle](/manuals/extensions-gradle).
  * Por fim, a pasta também pode conter zero ou mais arquivos ProGuard (experimental).
* `ios` - Esta pasta aceita um arquivo stub de manifesto a ser mesclado na aplicação principal ([conforme descrito aqui](/manuals/extensions-manifest-merge-tool)).
  * A pasta também pode conter um arquivo `Podfile` com dependências a serem [resolvidas pelo Cocoapods](/manuals/extensions-cocoapods).
* `osx` - Esta pasta aceita um arquivo stub de manifesto a ser mesclado na aplicação principal ([conforme descrito aqui](/manuals/extensions-manifest-merge-tool)).
* `web` - Esta pasta aceita um arquivo stub de manifesto a ser mesclado na aplicação principal ([conforme descrito aqui](/manuals/extensions-manifest-merge-tool)).


## Compartilhando uma extensão

Extensões são tratadas como qualquer outro asset no seu projeto e podem ser compartilhadas da mesma forma. Se uma pasta de extensão nativa for adicionada como pasta de biblioteca, ela poderá ser compartilhada e usada por outras pessoas como uma dependência de projeto. Consulte o [manual de projeto de biblioteca](/manuals/libraries/) para mais informações.


## Um exemplo simples de extensão

Vamos criar uma extensão bem simples. Primeiro, criamos uma nova pasta raiz *`myextension`* e adicionamos um arquivo *`ext.manifest`* contendo o nome da extensão "`MyExtension`". Observe que o nome é um símbolo C++ e deve corresponder ao primeiro argumento de `DM_DECLARE_EXTENSION` (veja abaixo).

![Manifesto](images/extensions/manifest.png)

```yaml
# Símbolo C++ na sua extensão
name: "MyExtension"
```

A extensão consiste em um único arquivo C++, *`myextension.cpp`*, criado na pasta "`src`".

![Arquivo C++](images/extensions/cppfile.png)

O arquivo-fonte da extensão contém o seguinte código:

```cpp
// myextension.cpp
// Definições da lib da extensão
#define LIB_NAME "MyExtension"
#define MODULE_NAME "myextension"

// Inclui o SDK do Defold
#include <dmsdk/sdk.h>

static int Reverse(lua_State* L)
{
    // O número de itens esperados na pilha Lua
    // quando esta struct sair de escopo
    DM_LUA_STACK_CHECK(L, 1);

    // Verifica e obtém a string de parâmetro da pilha
    char* str = (char*)luaL_checkstring(L, 1);

    // Inverte a string
    int len = strlen(str);
    for(int i = 0; i < len / 2; i++) {
        const char a = str[i];
        const char b = str[len - i - 1];
        str[i] = b;
        str[len - i - 1] = a;
    }

    // Coloca a string invertida na pilha
    lua_pushstring(L, str);

    // Retorna 1 item
    return 1;
}

// Funções expostas para Lua
static const luaL_reg Module_methods[] =
{
    {"reverse", Reverse},
    {0, 0}
};

static void LuaInit(lua_State* L)
{
    int top = lua_gettop(L);

    // Registra nomes Lua
    luaL_register(L, MODULE_NAME, Module_methods);

    lua_pop(L, 1);
    assert(top == lua_gettop(L));
}

dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
    return dmExtension::RESULT_OK;
}

dmExtension::Result InitializeMyExtension(dmExtension::Params* params)
{
    // Inicializa Lua
    LuaInit(params->m_L);
    printf("Registered %s Extension\n", MODULE_NAME);
    return dmExtension::RESULT_OK;
}

dmExtension::Result AppFinalizeMyExtension(dmExtension::AppParams* params)
{
    return dmExtension::RESULT_OK;
}

dmExtension::Result FinalizeMyExtension(dmExtension::Params* params)
{
    return dmExtension::RESULT_OK;
}


// O SDK do Defold usa uma macro para configurar pontos de entrada da extensão:
//
// DM_DECLARE_EXTENSION(symbol, name, app_init, app_final, init, update, on_event, final)

// MyExtension é o símbolo C++ que contém todos os dados relevantes da extensão.
// Ele deve corresponder ao campo name em `ext.manifest`
DM_DECLARE_EXTENSION(MyExtension, LIB_NAME, AppInitializeMyExtension, AppFinalizeMyExtension, InitializeMyExtension, 0, 0, FinalizeMyExtension)
```

Observe a macro `DM_DECLARE_EXTENSION`, usada para declarar os vários pontos de entrada no código da extensão. O primeiro argumento `symbol` deve corresponder ao nome especificado em *ext.manifest*. Para este exemplo simples, não há necessidade de pontos de entrada "update" ou "on_event", então `0` é fornecido nessas posições da macro.

Agora basta compilar o projeto (<kbd>Projeto ▸ Compilar</kbd>). Isso enviará a extensão ao builder de extensões, que produzirá uma engine personalizada com a nova extensão incluída. Se o builder encontrar algum erro, uma caixa de diálogo com os erros de build será exibida.

Para testar a extensão, crie um objeto de jogo e adicione um componente de script com algum código de teste:

```lua
local s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
local reverse_s = myextension.reverse(s)
print(reverse_s) --> ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba
```

E pronto! Criamos uma extensão nativa totalmente funcional.


## Ciclo de vida da extensão

Como vimos acima, a macro `DM_DECLARE_EXTENSION` é usada para declarar os vários pontos de entrada no código da extensão:

`DM_DECLARE_EXTENSION(symbol, name, app_init, app_final, init, update, on_event, final)`

Os pontos de entrada permitem executar código em vários momentos do ciclo de vida de uma extensão:

* Início da engine
  * Os sistemas da engine estão iniciando
  * `app_init` da extensão
  * `init` da extensão - Todas as APIs do Defold foram inicializadas. Este é o ponto recomendado no ciclo de vida da extensão em que os bindings Lua para o código da extensão são criados.
  * Inicialização do script - A função `init()` dos arquivos de script é chamada.
* Loop da engine
  * Atualização da engine
    * `update` da extensão
    * Atualização do script - A função `update()` dos arquivos de script é chamada.
  * Eventos da engine (minimizar/maximizar janela etc.)
    * `on_event` da extensão
* Encerramento (ou reinicialização) da engine
  * Finalização do script - A função `final()` dos arquivos de script é chamada.
  * `final` da extensão
  * `app_final` da extensão

## Identificadores de plataforma definidos

Os seguintes identificadores são definidos pelo builder em cada plataforma respectiva:

* `DM_PLATFORM_WINDOWS`
* `DM_PLATFORM_OSX`
* `DM_PLATFORM_IOS`
* `DM_PLATFORM_ANDROID`
* `DM_PLATFORM_LINUX`
* `DM_PLATFORM_HTML5`

## Logs do servidor de build {#build-server-logs}

Os logs do servidor de build ficam disponíveis quando o projeto usa extensões nativas. O log do servidor de build (`log.txt`) é baixado junto com a engine personalizada quando o projeto é compilado e armazenado dentro do arquivo `.internal/%platform%/build.zip`, além de ser descompactado na pasta de build do seu projeto.

## Exemplos de extensões

* [Exemplo de extensão básica](https://github.com/defold/template-native-extension) (a extensão deste manual)
* [Exemplo de extensão Android](https://github.com/defold/extension-android)
* [Exemplo de extensão HTML5](https://github.com/defold/extension-html5)
* [Extensão de player de vídeo para macOS, iOS e Android](https://github.com/defold/extension-videoplayer)
* [Extensão de câmera para macOS e iOS](https://github.com/defold/extension-camera)
* [Extensão de compra dentro do aplicativo para iOS e Android](https://github.com/defold/extension-iap)
* [Extensão Firebase Analytics para iOS e Android](https://github.com/defold/extension-firebase-analytics)

O [portal de assets do Defold](https://www.defold.com/assets/) também contém várias extensões nativas.
