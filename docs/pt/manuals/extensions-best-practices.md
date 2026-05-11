---
title: Extensões nativas - boas práticas
brief: Este manual descreve boas práticas ao desenvolver extensões nativas.
---

# Boas práticas

Escrever código multiplataforma pode ser difícil, mas há algumas formas de facilitar tanto o desenvolvimento quanto a manutenção desse código.


## Estrutura do projeto

Ao criar uma extensão, há algumas coisas que ajudam no desenvolvimento e também na manutenção dela.

### API Lua

Deve haver apenas uma API Lua e uma implementação dela. Isso torna muito mais fácil ter o mesmo comportamento em todas as plataformas.

Se a plataforma em questão não deve oferecer suporte à extensão, recomenda-se simplesmente não registrar nenhum módulo Lua. Dessa forma, você pode detectar suporte verificando `nil`:

```lua
    if myextension ~= nil then
        myextension.do_something()
    end
```

### Estrutura de pastas

A seguinte estrutura de pastas é usada com frequência para extensões:

```
    /root
        /input
        /main                            -- Todos os arquivos do projeto de exemplo real
            /...
        /myextension                     -- A pasta raiz real da extensão
            ext.manifest
            /include                     -- Includes externos, usados por outras extensões
            /libs
                /<platform>              -- Bibliotecas externas para todas as plataformas suportadas
            /src
                myextension.cpp          -- A API Lua da extensão e as funções de ciclo de vida da extensão
                                            Também contém implementações genéricas das funções da sua API Lua.
                myextension_private.h    -- Sua API interna que cada plataforma implementará (isto é, `myextension_Init` etc)
                myextension.mm           -- Se chamadas nativas forem necessárias para iOS/macOS. Implementa `myextension_Init` etc para iOS/macOS
                myextension_android.cpp  -- Se chamadas JNI forem necessárias para Android. Implementa `myextension_Init` etc para Android
                /java
                    /<platform>          -- Quaisquer arquivos Java necessários para Android
            /res                         -- Quaisquer recursos necessários para uma plataforma
            /external
                README.md                -- Notas/scripts sobre como compilar ou empacotar bibliotecas externas
        /bundleres                       -- Recursos que devem ser incluídos no pacote (veja game.project e a [configuração bundle_resources]([physics scale setting](/manuals/project-settings/#project))
            /<platform>
        game.project
        game.appmanifest                 -- Informações extras de configuração do app
```

Observe que `myextension.mm` e `myextension_android.cpp` só são necessários se você estiver fazendo chamadas nativas específicas para aquela plataforma.

#### Pastas de plataforma

Em certos lugares, a arquitetura da plataforma é usada como nome de pasta, para saber quais arquivos usar ao compilar/empacotar a aplicação. Elas têm a forma:

    <architecture>-<platform>

A lista atual é:

    arm64-ios, armv7-ios, x86_64-ios, arm64-android, armv7-android, x86_64-linux, x86_64-osx, x86_64-win32, x86-win32

Então, por exemplo, coloque bibliotecas específicas de plataforma em:

    /libs
        /arm64-ios
                            /libFoo.a
        /arm64-android
                            /libFoo.a


## Escrevendo código nativo

No código-fonte do Defold, C++ é usado de forma muito moderada, e a maior parte do código é bem parecida com C. Quase não há templates, exceto por algumas classes de contêiner, já que templates têm custo em tempo de compilação e no tamanho do executável.

### Versão de C++

O código-fonte do Defold é compilado com a versão padrão de C++ de cada compilador. O próprio código-fonte do Defold não usa versão de C++ superior a C++98. Embora seja possível usar uma versão mais alta para compilar uma extensão, uma versão mais alta pode trazer mudanças de ABI. Isso pode tornar impossível usar uma extensão em conjunto com extensões na engine ou do [Portal de Assets](/assets).

O código-fonte do Defold evita usar os recursos ou versões mais recentes de C++. Principalmente porque não há necessidade de novos recursos ao construir uma engine de jogos, mas também porque acompanhar os recursos mais recentes de C++ é uma tarefa demorada, e dominar esses recursos de fato exige muito tempo precioso.

Isso também traz o benefício adicional para desenvolvedores de extensão de que o Defold mantém uma ABI estável. Também vale apontar que usar os recursos mais recentes de C++ pode impedir que o código compile em diferentes plataformas devido ao suporte variável.

### Sem exceções C++

O Defold não usa exceções na engine. Exceções geralmente são evitadas em engines de jogos, já que os dados são (em grande parte) conhecidos antecipadamente durante o desenvolvimento. Remover o suporte a exceções C++ diminui o tamanho do executável e melhora o desempenho em tempo de execução.

### Standard Template Libraries - STL

Como a engine Defold não usa código STL, exceto por alguns algoritmos e matemática (`std::sort`, `std::upper_bound` etc.), pode funcionar para você usar STL na sua extensão.

Novamente, tenha em mente que incompatibilidades de ABI podem atrapalhar ao usar sua extensão em conjunto com outras extensões ou bibliotecas de terceiros.

Evitar as bibliotecas STL (fortemente baseadas em templates) também melhora nossos tempos de build e, mais importante, reduz o tamanho do executável.

#### Strings

Na engine Defold, `const char*` é usado em vez de `std::string`. O uso de `std::string` é uma armadilha comum ao misturar diferentes versões de C++ ou versões de compilador, pois pode resultar em incompatibilidade de ABI. Usar `const char*` e algumas funções auxiliares evita isso.

### Tornar funções ocultas

Use a palavra-chave `static` em funções locais à sua unidade de compilação, se possível. Isso permite ao compilador fazer algumas otimizações, podendo melhorar o desempenho e reduzir o tamanho do executável.

## Bibliotecas de terceiros

Ao escolher uma biblioteca de terceiros para usar (independentemente da linguagem), considere o seguinte:

* Funcionalidade - Ela resolve o problema específico que você tem?
* Desempenho - Ela implica um custo de desempenho em tempo de execução?
* Tamanho da biblioteca - Quanto maior o executável final ficará? Isso é aceitável?
* Dependências - Ela exige bibliotecas extras?
* Suporte - Qual é o estado da biblioteca? Ela tem muitas issues abertas? Ainda é mantida?
* Licença - Ela pode ser usada neste projeto?


## Dependências de código aberto

Sempre certifique-se de que você tem acesso às suas dependências. Por exemplo, se você depende de algo no GitHub, nada impede que esse repositório seja removido ou mude repentinamente de direção ou propriedade. Você pode mitigar esse risco criando um fork do repositório e usando seu fork em vez do projeto upstream.

Lembre-se de que o código da biblioteca será injetado no seu jogo, então certifique-se de que a biblioteca faz o que deve fazer, e nada mais!
