---
title: Empacotando uma aplicação
brief: Este manual aborda como criar um pacote de aplicação.
---

# Empacotando uma aplicação

Enquanto desenvolve sua aplicação, crie o hábito de testar o jogo nas plataformas-alvo com a maior frequência possível. Faça isso para detectar problemas de desempenho cedo no processo de desenvolvimento, quando essas coisas são muito mais fáceis de corrigir. Também é recomendável testar em todas as plataformas-alvo para encontrar discrepâncias em coisas como shaders. Ao desenvolver para mobile, você tem a opção de usar o [aplicativo de desenvolvimento mobile](/manuals/dev-app/) para enviar conteúdo ao app, em vez de precisar fazer um ciclo completo de empacotar, desinstalar e instalar.

Você pode criar um pacote de aplicação para todas as plataformas compatíveis com o Defold a partir do próprio editor Defold, sem precisar de ferramentas externas. Também é possível empacotar pela linha de comando usando nossas ferramentas de linha de comando. O empacotamento de aplicações exige uma conexão de rede se seu projeto contiver uma ou mais [extensões nativas](/manuals/extensions).

## Empacotando pelo editor

Você cria um pacote de aplicação pelo menu Project e pela opção Bundle:

![](images/bundling/bundle_menu.png)

Selecionar qualquer uma das opções de menu abrirá a caixa de diálogo Bundle para aquela plataforma específica.

### Relatórios de build

Ao empacotar seu jogo, há uma opção para criar um relatório de build. Isso é muito útil para entender o tamanho de todos os assets que fazem parte do pacote do seu jogo. Basta marcar a caixa *Generate build report* ao empacotar o jogo.

![relatório de build](images/profiling/build_report.png)

Para saber mais sobre relatórios de build, consulte o [manual de profiling](/manuals/profiling/#build-reports).

### Android

A criação de um pacote de aplicação Android (arquivo .apk) está documentada no [manual do Android](/manuals/android/#creating-an-android-application-bundle).

### iOS

A criação de um pacote de aplicação iOS (arquivo .ipa) está documentada no [manual do iOS](/manuals/ios/#creating-an-ios-application-bundle).

### macOS

A criação de um pacote de aplicação macOS (arquivo .app) está documentada no [manual do macOS](/manuals/macos).

### Linux

A criação de um pacote de aplicação Linux não exige configuração específica nem configuração opcional específica da plataforma no [arquivo de configurações do projeto](/manuals/project-settings/#linux) *game.project*.

### Windows

A criação de um pacote de aplicação Windows (arquivo .exe) está documentada no [manual do Windows](/manuals/windows).

### HTML5

A criação de um pacote de aplicação HTML5, bem como a configuração opcional, está documentada no [manual de HTML5](/manuals/html5/#creating-html5-bundle).

#### Facebook Instant Games

É possível criar uma versão especial de um pacote de aplicação HTML5 especificamente para Facebook Instant Games. Esse processo está documentado no [manual de Facebook Instant Games](/manuals/instant-games/).

## Empacotando pela linha de comando

O editor usa nossa ferramenta de linha de comando [Bob](/manuals/bob/) para empacotar a aplicação.

Durante o desenvolvimento diário da sua aplicação, é provável que você compile e empacote pelo editor Defold. Em outras circunstâncias, você talvez queira gerar pacotes de aplicação automaticamente, por exemplo fazendo builds em lote para todos os alvos ao lançar uma nova versão ou criando builds noturnos da versão mais recente do jogo, talvez em um ambiente de CI. A compilação e o empacotamento de uma aplicação podem ser feitos fora do fluxo normal de trabalho do editor usando a [ferramenta de linha de comando Bob](/manuals/bob/).

## Layout do pacote

O layout lógico do pacote é estruturado assim:

![](images/bundling/bundle_schematic_01.png)

Um pacote é gerado em uma pasta. Dependendo da plataforma, essa pasta também pode ser compactada em um arquivo `.apk` ou `.ipa`.
O conteúdo da pasta depende da plataforma.

Além dos arquivos executáveis, nosso processo de empacotamento também coleta os assets necessários para a plataforma (por exemplo, os arquivos de recurso .xml para Android).

Usando a configuração [bundle_resources](https://defold.com/manuals/project-settings/#bundle-resources), você pode configurar assets que devem ser colocados dentro do pacote como estão.
Você pode controlar isso por plataforma.

Os assets do jogo ficam no arquivo `game.arcd`, e são compactados individualmente usando compressão LZ4.
Usando a configuração [custom_resources](https://defold.com/manuals/project-settings/#custom-resources), você pode configurar assets que devem ser colocados (com compressão) dentro de `game.arcd`.
Esses assets podem ser acessados pela função [`sys.load_resource()`](https://defold.com/ref/sys/#sys.load_resource).

## Release vs Debug

Ao criar um pacote de aplicação, você tem a opção de criar um pacote debug ou release. As diferenças entre os dois pacotes são pequenas, mas importantes:

* Builds Release não incluem o [profiler](/manuals/profiling)
* Builds Release não incluem o [gravador de tela](/ref/stable/sys/#start_record)
* Builds Release não mostram a saída de chamadas a `print()` nem a saída de extensões nativas
* Builds Release têm o valor `is_debug` em `sys.get_engine_info()` definido como `false`
* Builds Release não fazem consultas reversas de valores `hash` ao chamar `tostring()`. Na prática, isso significa que um `tostring()` para um valor do tipo `url` ou `hash` retornará sua representação numérica, e não a string original (`'hash: [/camera_001]'` vs `'hash: [11844936738040519888 (unknown)]'`)
* Builds Release não oferecem suporte a direcionamento a partir do editor para [hot reload](/manuals/hot-reload) e funcionalidades semelhantes


