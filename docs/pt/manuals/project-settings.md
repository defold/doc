---
title: Configurações de projeto do Defold
brief: Este manual descreve como as configurações específicas de projeto funcionam no Defold.
---

# Configurações de projeto {#project-settings}

O arquivo *game.project* contém todas as configurações globais do projeto. Ele deve permanecer na pasta raiz do projeto e deve se chamar *game.project*. A primeira coisa que a engine faz ao iniciar e lançar seu jogo é procurar esse arquivo.

Toda configuração no arquivo pertence a uma categoria. Quando você abre o arquivo, o Defold apresenta todas as configurações agrupadas por categoria.

![Project settings](images/project-settings/settings.jpg)


## Formato do arquivo {#file-format}

As configurações em *game.project* geralmente são alteradas dentro do Defold, mas o arquivo também pode ser editado em qualquer editor de texto padrão. O arquivo segue o padrão de formato de arquivo INI e se parece com isto:

```ini
[category1]
setting1 = value
setting2 = value
[category2]
...
```

Um exemplo real é:

```ini
[bootstrap]
main_collection = /main/main.collectionc
```

o que significa que a configuração *main_collection* pertence à categoria *bootstrap*. Sempre que uma referência de arquivo é usada, como no exemplo acima, o caminho precisa receber um caractere 'c' no final, o que significa que você está referenciando a versão compilada do arquivo. Observe também que a pasta que contém *game.project* será a raiz do projeto, por isso há uma '/' inicial no caminho da configuração.


## Acesso em tempo de execução {#runtime-access}

É possível ler qualquer valor de *game.project* em tempo de execução usando [`sys.get_config_string(key)`](/ref/sys/#sys.get_config_string), [`sys.get_config_number(key)`](/ref/sys/#sys.get_config_number) e [`sys.get_config_int(key)`](/ref/sys/#sys.get_config_int). Exemplos:

```lua
local title = sys.get_config_string("project.title")
local gravity_y = sys.get_config_number("physics.gravity_y")
```

::: sidenote
A chave é uma combinação da categoria e do nome da configuração, separados por ponto, escrita em letras minúsculas com quaisquer espaços substituídos por underscores. Exemplos: o campo "Title" da categoria "Project" se torna `project.title` e o campo "Gravity Y" da categoria "Physics" se torna `physics.gravity_y`.
:::


## Seções e configurações {#sections-and-settings}

Abaixo estão todas as configurações disponíveis, organizadas por categoria.

### Project

#### Title
O título da aplicação.

#### Version
A versão da aplicação.

#### Publisher
Nome do publisher.

#### Developer
Nome do desenvolvedor.

#### Write Log File
Controla quando a engine grava um arquivo de log. Opções:

- "Never": Não grava um arquivo de log.
- "Debug": Grava um arquivo de log apenas para builds Debug.
- "Always": Grava um arquivo de log para builds Debug e Release.

Se mais de uma instância estiver sendo executada a partir do editor, o arquivo será chamado *instance_2_log.txt*, com `2` sendo o índice da instância. Se uma única instância estiver sendo executada, ou se estiver sendo executada a partir de um pacote, o arquivo será chamado *log.txt*. O local do arquivo de log será um dos seguintes caminhos (tentados em ordem):

1. O caminho especificado em *project.log_dir* (configuração oculta)
2. O caminho de log do sistema:
  * macOS/iOS: `NSDocumentDirectory`
  * Android: `Context.getExternalFilesDir()`
  * Outros: raiz da aplicação
3. O caminho de suporte da aplicação
  * macOS/iOS: `NSApplicationSupportDirectory`
  * Windows: `CSIDL_APPDATA` (por exemplo, `C:\Users\<username>\AppData\Roaming`)
  * Android: `Context.getFilesDir()`
  * Linux: variável de ambiente `HOME`

#### Minimum Log Level
Especifica o nível mínimo de log para o sistema de logging. Somente logs nesse nível ou acima dele serão mostrados.

#### Compress Archive
Habilita compressão de arquivos ao empacotar. Observe que isso atualmente se aplica a todas as plataformas exceto Android, onde o apk já contém todos os dados comprimidos.

#### Dependencies
Uma lista de URLs para os *Library URL*s do projeto. Consulte o [manual de Bibliotecas](/manuals/libraries/) para mais informações.

#### Custom Resources
`custom_resources`
:[Custom Resources](../shared/custom-resources.md)

O carregamento de recursos personalizados é abordado em mais detalhes no [manual de Acesso a Arquivos](/manuals/file-access/#how-to-access-files-bundled-with-the-application).

#### Bundle Resources
`bundle_resources`
:[Bundle Resources](../shared/bundle-resources.md)

O carregamento de recursos de pacote é abordado em mais detalhes no [manual de Acesso a Arquivos](/manuals/file-access/#how-to-access-files-bundled-with-the-application).

#### Bundle Exclude Resources
`bundle_exclude_resources`
Uma lista separada por vírgulas de recursos que não devem ser incluídos no pacote. Ou seja, eles são removidos do resultado da coleta da etapa `bundle_resources`.

---

### Bootstrap

#### Main Collection
Referência de arquivo da coleção a usar para iniciar a aplicação, `/logic/main.collection` por padrão.

#### Render
Qual arquivo de configuração de renderização usar, que define o pipeline de renderização, `/builtins/render/default.render` por padrão.

---

### Library

#### Include Dirs
Uma lista de diretórios separados por espaço que devem ser compartilhados a partir do seu projeto via compartilhamento de biblioteca. Consulte o [manual de Bibliotecas](/manuals/libraries/) para mais informações.

---

### Script

#### Shared State
Marque para compartilhar um único estado Lua entre todos os tipos de script.

---

### Engine

#### Run While Iconified
Permite que a engine continue em execução enquanto a janela da aplicação está iconificada (somente plataformas desktop).

#### Fixed Update Frequency
A frequência de atualização da função de ciclo de vida `fixed_update(self, dt)`. Em Hertz.

#### Max Time Step
Se o passo de tempo ficar grande demais durante um único frame, ele será limitado a este valor máximo. Em segundos.

---

### Display

#### Width
A largura em pixels da janela da aplicação.

#### Height
A altura em pixels da janela da aplicação.

#### High Dpi
Cria um back buffer high dpi em displays que oferecem suporte a isso. Normalmente o jogo será renderizado no dobro da resolução definida nas configurações *Width* e *Height*, que ainda serão a resolução lógica usada em scripts e propriedades.

#### Samples
Quantas amostras usar para anti-aliasing por superamostragem. Isso define a hint de janela GLFW_FSAA_SAMPLES. Um valor de `0` significa que anti-aliasing está desativado.

#### Fullscreen
Marque se a aplicação deve iniciar em tela cheia. Se desmarcado, a aplicação roda em janela.

#### Update Frequency
A taxa de quadros desejada em Hertz. Defina como 0 para taxa de quadros variável. Um valor maior que 0 resultará em uma taxa de quadros fixa, limitada em tempo de execução em relação à taxa de quadros real (o que significa que você não pode atualizar o loop do jogo duas vezes em um frame da engine). Use [`sys.set_update_frequency(hz)`](https://defold.com/ref/stable/sys/?q=set_update_frequency#sys.set_update_frequency:frequency) para alterar esse valor em tempo de execução. Essa configuração também funciona em builds headless.

#### Swap interval
Este valor inteiro controla como a aplicação lida com vsync. 0 desabilita vsync, e o valor padrão é 1. Ao usar um adaptador OpenGL, esse valor define o número de frames entre [trocas de buffer](https://www.khronos.org/opengl/wiki/Swap_Interval) da janela. Para Vulkan, não há conceito integrado de swap interval; em vez disso, o valor controla se vsync deve ser habilitado ou não.

#### Vsync
Depende do vsync de hardware para o timing dos frames. Pode ser sobrescrito dependendo do driver gráfico e das especificidades da plataforma. Para o comportamento obsoleto de 'variable_dt', desmarque esta configuração e defina o limite de frames como 0.

#### Display Profiles
Especifica qual arquivo de perfis de exibição usar, `/builtins/render/default.display_profilesc` por padrão. Saiba mais no [manual de Layouts de GUI](/manuals/gui-layouts/#creating-display-profiles).

#### Dynamic Orientation
Marque se o app deve alternar dinamicamente entre retrato e paisagem na rotação do dispositivo. Observe que o aplicativo de desenvolvimento atualmente não respeita essa configuração.

#### Display Device Info
Emite informações da GPU no console durante a inicialização.

---

### Render

#### Clear Color Red
Canal vermelho da cor de limpeza, usado pelo script de renderização e quando a janela é criada.

#### Clear Color Green
Canal verde da cor de limpeza, usado pelo script de renderização e quando a janela é criada.

#### Clear Color Blue
Canal azul da cor de limpeza, usado pelo script de renderização e quando a janela é criada.

#### Clear Color Alpha
Canal alfa da cor de limpeza, usado pelo script de renderização e quando a janela é criada.

---

### Font

#### Runtime Generation
Usa geração de fonte em tempo de execução.

---

### Physics

#### Max Collision Object Count
Número máximo de objetos de colisão.

#### Type
Qual tipo de física usar, `2D` ou `3D`.

#### Gravity X
Gravidade do mundo ao longo do eixo x. Em metros por segundo.

#### Gravity Y
Gravidade do mundo ao longo do eixo y. Em metros por segundo.

#### Gravity Z
Gravidade do mundo ao longo do eixo z. Em metros por segundo.

#### Debug
Marque se a física deve ser visualizada para depuração.

#### Debug Alpha
Valor do componente alfa para física visualizada, `0`--`1`.

#### World Count
Número máximo de mundos de física simultâneos, `4` por padrão. Se você carregar mais de 4 mundos simultaneamente por meio de proxies de coleção, precisa aumentar esse valor. Esteja ciente de que cada mundo de física aloca uma quantidade considerável de memória.

#### Scale
Diz à engine de física como escalar os mundos de física em relação ao mundo do jogo para precisão numérica, `0.01`--`1.0`. Se o valor for definido como `0.02`, isso significa que a engine de física verá 50 unidades como 1 metro ($1 / 0.02$).

#### Allow Dynamic Transforms
Marque se a engine de física deve aplicar a transformação de um objeto de jogo a quaisquer componentes de objeto de colisão anexados. Isso pode ser usado para mover, escalar e rotacionar formas de colisão, mesmo as dinâmicas.

#### Use Fixed Timestep
Marque se a engine de física deve usar atualizações fixas e independentes da taxa de quadros. Use esta configuração em combinação com a função de ciclo de vida `fixed_update(self, dt)` e a configuração de projeto `engine.fixed_update_frequency` para interagir com a engine de física em intervalos regulares. Para novos projetos, a configuração recomendada é `true`.

#### Debug Scale
O tamanho para desenhar objetos unitários em física, como tríades e normais.

#### Max Collisions
Quantas colisões serão relatadas de volta aos scripts.

#### Max Contacts
Quantos pontos de contato serão relatados de volta aos scripts.

#### Contact Impulse Limit
Ignora impulsos de contato com valores menores que esta configuração.

#### Ray Cast Limit 2d
O número máximo de requisições de ray cast 2d por frame.

#### Ray Cast Limit 3d
O número máximo de requisições de ray cast 3d por frame.

#### Trigger Overlap Capacity
O número máximo de gatilhos de física sobrepostos.

#### Velocity Threshold
Velocidade mínima que resultará em colisões elásticas.

#### Max Fixed Timesteps
Número máximo de passos na simulação ao usar timestep fixo (somente 3D).

---

### Graphics

#### Default Texture Min Filter
Especifica qual filtragem usar para filtragem de minificação.

#### Default Texture Mag Filter
Especifica qual filtragem usar para filtragem de magnificação.

#### Max Draw Calls
O número máximo de chamadas de renderização.

#### Max Characters:
O número de caracteres pré-alocados no buffer de renderização de texto, isto é, o número de caracteres que podem ser exibidos a cada frame.

#### Max Font Batches
O número máximo de batches de texto que podem ser exibidos a cada frame.

#### Max Debug Vertices
O número máximo de vértices de depuração. Usado para renderização de formas de física, entre outras coisas.

#### Texture Profiles
O arquivo de perfis de textura a usar para este projeto, `/builtins/graphics/default.texture_profiles` por padrão.

#### Verify Graphics Calls
Verifica o valor de retorno após cada chamada gráfica e relata quaisquer erros no log.

#### OpenGL Version Hint
Hint de versão de contexto OpenGL. Se uma versão específica for selecionada, ela será usada como a versão mínima exigida (não se aplica ao OpenGL ES).

#### OpenGL Core Profile Hint
Define a hint de perfil OpenGL 'core' ao criar o contexto. O core profile remove todos os recursos obsoletos do OpenGL, como renderização em modo imediato. Não se aplica ao OpenGL ES.

---

### Shader

#### Exclude GLES 2.0
Não compila shaders para dispositivos executando OpenGLES 2.0 / WebGL 1.0.

---

### Input

#### Repeat Delay
Segundos a aguardar antes que uma entrada mantida pressionada comece a se repetir.

#### Repeat Interval
Segundos a aguardar entre cada repetição de uma entrada mantida pressionada.

#### Gamepads
Referência de arquivo do arquivo de configuração de gamepads, que mapeia sinais de gamepad para o SO, `/builtins/input/default.gamepads` por padrão.

#### Game Binding
Referência de arquivo do arquivo de configuração de entrada, que mapeia entradas de hardware para ações, `/input/game.input_binding` por padrão.

#### Use Accelerometer
Marque para fazer a engine receber eventos de entrada do acelerômetro a cada frame. Desabilitar a entrada do acelerômetro pode trazer algum ganho de desempenho.

---

### Resource

#### Http Cache
Se marcado, um cache HTTP é habilitado para carregar recursos mais rapidamente pela rede na engine em execução no dispositivo.

#### Uri
Onde encontrar os dados de build do projeto, em formato URI.

#### Max Resources
O número máximo de recursos que podem ser carregados ao mesmo tempo.

---

### Network

#### Http Timeout
O timeout HTTP em segundos. Defina como `0` para desabilitar timeout.

#### Http Thread Count
O número de worker threads para o serviço HTTP.

#### Http Cache Enabled
Marque para habilitar o cache HTTP para requisições de rede (usando `http.request()`). O cache HTTP armazenará a resposta associada a uma requisição e reutilizará a resposta armazenada em requisições posteriores. O cache HTTP oferece suporte aos cabeçalhos de resposta HTTP `ETag` e `Cache-Control: max-age`.

#### SSL Certificates
Arquivo contendo certificados raiz SSL a usar ao verificar a cadeia de certificados durante handshakes SSL.

---

### Collection

#### Max Instances
Número máximo de instâncias de objetos de jogo em uma coleção, `1024` por padrão. [(Veja informações sobre otimizações de contagem máxima de componentes)](#component-max-count-optimizations).

#### Max Input Stack Entries
Número máximo de objetos de jogo na pilha de entrada.

---

### Sound

#### Gain
Ganho global (volume), `0`--`1`.

#### Use Linear Gain
Se habilitado, o ganho é linear. Se desabilitado, usa uma curva exponencial.

#### Max Sound Data
Número máximo de recursos de som, isto é, o número de arquivos de som únicos em tempo de execução.

#### Max Sound Buffers
(Atualmente não usado) Número máximo de buffers de som simultâneos.

#### Max Sound Sources
(Atualmente não usado) Número máximo de sons tocando simultaneamente.

#### Max Sound Instances
Número máximo de instâncias de som simultâneas, isto é, sons reais reproduzidos ao mesmo tempo.

#### Max Component Count
Número máximo de componentes de som por coleção.

#### Sample Frame Count
Número de amostras usadas para cada atualização de áudio. 0 significa automático (1024 para 48 kHz, 768 para 44,1 kHz).

#### Use Thread
Se marcado, o sistema de som usará threads para reprodução de som para reduzir o risco de engasgos quando a thread principal estiver sob carga elevada.

#### Stream Enabled
Se marcado, o sistema de som usará streaming para carregar arquivos-fonte.

#### Stream Cache Size
O tamanho máximo do cache de chunks de som contendo _todos_ os chunks. `2097152` bytes por padrão.
Esse número deve ser maior que o número de arquivos de som carregados multiplicado pelo tamanho do chunk de stream.
Caso contrário, você corre o risco de expulsar novos chunks a cada frame.

#### Stream Chunk Size
O tamanho em bytes de cada chunk transmitido por streaming.

#### Stream Preload Size
Determina o tamanho em bytes do chunk inicial para arquivos de som lidos do archive.

---

### Sprite

#### Max Count
Número máximo de sprites por coleção. [(Veja informações sobre otimizações de contagem máxima de componentes)](#component-max-count-optimizations).

#### Subpixels
Marque para permitir que sprites apareçam desalinhados em relação aos pixels.

---

### Tilemap

#### Max Count
Número máximo de tile maps por coleção. [(Veja informações sobre otimizações de contagem máxima de componentes)](#component-max-count-optimizations).

#### Max Tile Count
Número máximo de tiles visíveis simultâneos por coleção.

---

### Spine

#### Max Count
Número máximo de componentes de modelo spine. [(Veja informações sobre otimizações de contagem máxima de componentes)](#component-max-count-optimizations).

---

### Mesh

#### Max Count
Número máximo de componentes de mesh por coleção. [(Veja informações sobre otimizações de contagem máxima de componentes)](#component-max-count-optimizations).

---

### Model

#### Max Count
Número máximo de componentes de modelo por coleção. [(Veja informações sobre otimizações de contagem máxima de componentes)](#component-max-count-optimizations).

#### Split Meshes
Divide meshes com mais de 65536 vértices em novas meshes.

#### Max Bone Matrix Texture Width
Largura máxima da textura de matriz de ossos. Apenas o tamanho necessário para animações é usado, arredondado para a potência de dois mais próxima.

#### Max Bone Matrix Texture Height
Altura máxima da textura de matriz de ossos. Apenas o tamanho necessário para animações é usado, arredondado para a potência de dois mais próxima.

---

### GUI

#### Max Count
Número máximo de componentes GUI. [(Veja informações sobre otimizações de contagem máxima de componentes)](#component-max-count-optimizations).

#### Max Particle Count
O número máximo de partículas simultâneas na GUI.

#### Max Animation Count
O número máximo de animações ativas na gui.

---

### Label

#### Max Count
Número máximo de rótulos. [(Veja informações sobre otimizações de contagem máxima de componentes)](#component-max-count-optimizations).

#### Subpixels
Marque para permitir que rótulos apareçam desalinhados em relação aos pixels.

---

### Particle FX

#### Max Count
O número máximo de emissores simultâneos. [(Veja informações sobre otimizações de contagem máxima de componentes)](#component-max-count-optimizations).

#### Max Particle Count
O número máximo de partículas simultâneas.

---

### Box2D

#### Velocity Iterations
Número de iterações de velocidade para o solver de física Box2D 2.2.

#### Position Iterations
Número de iterações de posição para o solver de física Box2D 2.2.

#### Sub Step Count
Número de subpassos para o solver de física Box2D 3.x.

---

### Collection proxy

#### Max Count
Número máximo de proxies de coleção. [(Veja informações sobre otimizações de contagem máxima de componentes)](#component-max-count-optimizations).

---

### Collection factory

#### Max Count
Número máximo de fábricas de coleção. [(Veja informações sobre otimizações de contagem máxima de componentes)](#component-max-count-optimizations).

---

### Factory

#### Max Count
Número máximo de fábricas de objetos de jogo. [(Veja informações sobre otimizações de contagem máxima de componentes)](#component-max-count-optimizations).

---

### iOS

#### App Icon 57x57--180x180
Arquivo de imagem (.png) a usar como ícone da aplicação nas dimensões de largura e altura fornecidas `W` &times; `H`.

#### Launch Screen
Arquivo Storyboard (.storyboard). Saiba mais sobre como criar um no [manual de iOS](/manuals/ios/#creating-a-storyboard).

#### Icons Asset
O arquivo de asset de ícones (.car) contendo ícones do app.

#### Prerendered Icons
(iOS 6 e anteriores) Marque se seus ícones são pré-renderizados. Se isso estiver desmarcado, os ícones receberão automaticamente um destaque brilhante.

#### Bundle Identifier
O bundle identifier permite que o iOS reconheça quaisquer atualizações do seu app. Seu bundle ID deve ser registrado na Apple e ser único para seu app. Você não pode usar o mesmo identificador para apps iOS e macOS. Deve consistir em dois ou mais segmentos separados por ponto. Cada segmento deve começar com uma letra. Cada segmento deve consistir apenas em letras alfanuméricas, underscore ou hífen (-) (veja [`CFBundleIdentifier`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430))

#### Bundle Name
O nome curto do bundle (15 caracteres) (veja [`CFBundleName`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)).

#### Bundle Version
A versão do bundle, seja um número ou x.y.z. (veja [`CFBundleVersion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430))

#### Info.plist
Se especificado, usa este arquivo *`info.plist`* ao empacotar seu app.

#### Privacy Manifest
O Apple Privacy Manifest da aplicação. O campo usará `/builtins/manifests/ios/PrivacyInfo.xcprivacy` como padrão.

#### Custom Entitlements
Se especificado, os entitlements no provisioning profile fornecido (`.entitlements`, `.xcent`, `.plist`) serão mesclados com os entitlements do provisioning profile fornecido ao empacotar a aplicação.

#### Default Language
O idioma usado se a aplicação não tiver o idioma preferido do usuário na lista `Localizations` (veja [`CFBundleDevelopmentRegion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)). Use o padrão ISO 639-1 de duas letras se o idioma preferido estiver disponível ali, ou o ISO 639-2 de três letras.

#### Localizations
Este campo contém strings separadas por vírgula que identificam o nome do idioma ou designador ISO de idioma das localizações suportadas (veja [`CFBundleLocalizations`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552)).

---

### Android

#### App Icon 36x36--192x192
Arquivo de imagem (.png) a usar como ícone da aplicação nas dimensões de largura e altura fornecidas `W` &times; `H`.

#### Push Icon Small--LargeXxxhdpi
Arquivos de imagem (.png) a serem usados como ícone personalizado de notificação push no Android. Os ícones serão usados automaticamente para notificações push locais e remotas. Se não definido, o ícone da aplicação será usado por padrão.

#### Push Field Title
Especifica qual campo JSON do payload deve ser usado como título da notificação. Deixar esta configuração vazia faz com que os pushes usem o nome da aplicação como título por padrão.

#### Push Field Text
Especifica qual campo JSON do payload deve ser usado como texto da notificação. Se deixado vazio, o texto no campo `alert` é usado, assim como no iOS.

#### Version Code
Um valor inteiro que indica a versão do app. Aumente o valor a cada atualização subsequente.

#### Minimum SDK Version
O API Level mínimo necessário para a aplicação executar (`android:minSdkVersion`).

#### Target SDK Version
O API Level que a aplicação tem como alvo (`android:targetSdkVersion`).

#### Package
Identificador do pacote. Deve consistir em dois ou mais segmentos separados por ponto. Cada segmento deve começar com uma letra. Cada segmento deve consistir apenas em letras alfanuméricas ou no caractere underscore.

#### GCM Sender Id
Google Cloud Messaging Sender Id. Defina isto como a string atribuída pelo Google para habilitar notificações push.

#### FCM Application Id
Firebase Cloud Messaging Application Id.

#### Manifest
Se definido, usa o arquivo XML de manifesto Android especificado ao empacotar.

#### Iap Provider
Especifica qual loja usar. As opções válidas são `Amazon` e `GooglePlay`. Consulte [extension-iap](/extension-iap/) para mais informações.

#### Input Method
Especifica qual método usar para obter entrada de teclado em dispositivos Android. As opções válidas são `KeyEvent` (método antigo) e `HiddenInputField` (novo).

#### Immersive Mode
Se definido, oculta as barras de navegação e status e permite que seu app capture todos os eventos de toque na tela.

#### Display Cutout
Estende até o recorte da tela.

#### Debuggable
Se a aplicação pode ou não ser depurada usando ferramentas como [GAPID](https://github.com/google/gapid) ou [Android Studio](https://developer.android.com/studio/profile/android-profiler). Isso definirá a flag `android:debuggable` no manifesto Android ([documentação oficial](https://developer.android.com/guide/topics/manifest/application-element#debug)).

#### ProGuard config
Arquivo ProGuard personalizado para ajudar a remover classes Java redundantes do APK final.

#### Extract Native Libraries
Especifica se o instalador do pacote extrai bibliotecas nativas do APK para o sistema de arquivos. Se definido como `false`, suas bibliotecas nativas são armazenadas sem compressão no APK. Embora seu APK possa ficar maior, sua aplicação carrega mais rápido porque as bibliotecas são carregadas diretamente do APK em tempo de execução. Isso definirá a flag `android:extractNativeLibs` no Android Manifest ([documentação oficial](https://developer.android.com/guide/topics/manifest/application-element#extractNativeLibs)).

---

### macOS

#### App Icon
Arquivo de ícone do bundle (.icns) a usar como ícone da aplicação no macOS.

#### Info.plist
Se definido, usa o arquivo info.plist especificado ao empacotar.

#### Privacy Manifest
O Apple Privacy Manifest da aplicação. O campo usará `/builtins/manifests/osx/PrivacyInfo.xcprivacy` como padrão.

#### Bundle Identifier
O bundle identifier permite que o macOS reconheça atualizações do seu app. Seu bundle ID deve ser registrado na Apple e ser único para seu app. Você não pode usar o mesmo identificador para apps iOS e macOS. Deve consistir em dois ou mais segmentos separados por ponto. Cada segmento deve começar com uma letra. Cada segmento deve consistir apenas em letras alfanuméricas, underscore ou hífen (-).

#### Default Language
O idioma usado se a aplicação não tiver o idioma preferido do usuário na lista `Localizations` (veja [`CFBundleDevelopmentRegion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)). Use o padrão ISO 639-1 de duas letras se o idioma preferido estiver disponível ali, ou o ISO 639-2 de três letras.

#### Localizations
Este campo contém strings separadas por vírgula que identificam o nome do idioma ou designador ISO de idioma das localizações suportadas (veja [`CFBundleLocalizations`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552)).

---

### Windows

#### App Icon
Arquivo de imagem (.ico) a usar como ícone da aplicação no Windows. Leia mais sobre como criar um arquivo .ico no [manual de Windows](/manuals/windows).

---

### HTML5

Consulte o [manual da plataforma HTML5](/manuals/html5/) para mais informações sobre muitas dessas opções.

#### Heap Size
Tamanho do heap em megabytes para o Emscripten usar.

#### .html Shell
Usa o arquivo HTML de template especificado ao empacotar. Por padrão, `/builtins/manifests/web/engine_template.html`.

#### Custom .css
Usa o arquivo CSS de tema especificado ao empacotar. Por padrão, `/builtins/manifests/web/light_theme.css`.

#### Splash Image
Se definido, usa a imagem splash especificada na inicialização ao empacotar, em vez do logo Defold.

#### Archive Location Prefix
Ao empacotar para HTML5, os dados do jogo são divididos em um ou mais arquivos de dados de archive. Quando a engine inicia o jogo, esses arquivos de archive são lidos para a memória. Use esta configuração para especificar a localização dos dados.

#### Archive Location Suffix
Sufixo a ser anexado aos arquivos de archive. Útil, por exemplo, para forçar conteúdo sem cache de uma CDN (`?version2`, por exemplo).

#### Engine Arguments
Lista de argumentos que serão passados à engine.

#### Wasm Streaming
Habilita streaming do arquivo wasm (mais rápido e usa menos memória, mas exige o tipo MIME `application/wasm`).

#### Show Fullscreen Button
Habilita Fullscreen Button no arquivo `index.html`.

#### Show Made With Defold
Habilita o link Made With Defold no arquivo `index.html`.

#### Show Console Banner
Quando habilitada, esta opção imprimirá informações sobre a engine e a versão da engine no console do navegador (usando `console.log()`) quando a engine iniciar.

#### Scale Mode
Especifica qual método usar para escalar o canvas do jogo.

#### Retry Count
O número de tentativas de baixar um arquivo quando a engine inicia (veja `Retry Time`).

#### Retry Time
O número de segundos a aguardar entre tentativas de baixar um arquivo quando o download falha (veja `Retry Count`).

#### Transparent Graphics Context
Marque se você quer que o contexto gráfico tenha um fundo transparente.

---

### IAP

#### Auto Finish Transactions
Marque para finalizar automaticamente transações IAP. Se desmarcado, você precisa chamar explicitamente `iap.finish()` após uma transação bem-sucedida.

---

### Live update

#### Settings
Arquivo de recurso de configurações Liveupdate a usar durante o empacotamento.

#### Mount On Start
Habilita montagem automática de recursos montados anteriormente quando a aplicação inicia.

---

### Native extension

#### _App Manifest_
Se definido, usa o app manifest para personalizar a build da engine. Isso permite remover partes não usadas da engine para diminuir o tamanho final do binário. Aprenda como excluir recursos não usados [no manual de manifesto da aplicação](/manuals/app-manifest).

---

### Profiler

#### Enabled
Habilita o perfilador dentro do jogo.

#### Track Cpu
Se marcado, habilita profiling de CPU em versões release das builds. Normalmente, você só pode acessar informações de profiling em builds de depuração.

#### Sleep Between Server Updates
Número de milissegundos a dormir entre atualizações do servidor.

#### Performance Timeline Enabled
Habilita a timeline de desempenho no navegador (somente HTML5).

---

## Definindo valores de configuração na inicialização da engine {#setting-config-values-on-engine-startup}

Quando a engine inicia, é possível fornecer valores de configuração pela linha de comando que sobrescrevem as configurações de *game.project*:

```bash
# Especifica uma coleção bootstrap
$ dmengine --config=bootstrap.main_collection=/my.collectionc

# Define dois valores de configuração personalizados
$ dmengine --config=test.my_value=4711 --config=test2.my_value2=foobar
```

Valores personalizados podem, assim como qualquer outro valor de configuração, ser lidos com [`sys.get_config_string()`](/ref/sys/#sys.get_config_string) ou [`sys.get_config_number()`](/ref/sys/#sys.get_config_number):

```lua
local my_value = sys.get_config_number("test.my_value")
local my_value2 = sys.get_config_string("test.my_value2")
```


:[Component max count optimizations](../shared/component-max-count-optimizations.md)


## Configurações personalizadas de projeto {#custom-project-settings}

É possível definir configurações personalizadas para o projeto principal ou para uma [extensão nativa](/manuals/extensions/). Configurações personalizadas para o projeto principal devem ser definidas em um arquivo `game.properties` na raiz do projeto. Para uma extensão nativa, elas devem ser definidas em um arquivo `ext.properties` ao lado do arquivo `ext.manifest`.

O arquivo de configurações usa o mesmo formato INI de *game.project*, e atributos de propriedade são definidos usando notação com ponto e um sufixo:

```
[my_category]
my_property.private = 1
...
```

O meta arquivo padrão que é sempre aplicado está disponível [aqui](https://github.com/defold/defold/blob/dev/com.dynamo.cr/com.dynamo.cr.bob/src/com/dynamo/bob/meta.properties)

Os seguintes atributos estão disponíveis atualmente:

```
[my_extension]
// `type` - usado para analisar a string de valor
my_property.type = string // um dos seguintes valores: bool, string, number, integer, string_array, resource

// `help` - usado como dica de ajuda no editor (não usado por enquanto)
my_property.help = string

// `default` - valor usado como padrão se o usuário não definiu valor manualmente
my_property.default = string

// `private` - valor privado usado durante o processo de empacotamento, mas removido do próprio pacote
my_property.private = 1 // valor booleano 1 ou 0

// `label` - rótulo de entrada no editor
my_property.label = My Awesome Property

// `minimum` e/ou `maximum` - faixa válida para propriedades numéricas, validada na UI do editor
my_property.minimum = 0
my_property.maximum = 255

// `options` - opções de menu suspenso para a UI do editor, pares valor[:rótulo] separados por vírgula
my_property.options = android: Android, ios: iOS

// apenas tipo `resource`:
my_property.filter = jpg,png // extensões de arquivo permitidas para o diálogo seletor de recursos
my_property.preserve-extension = 1 // usa a extensão original do recurso em vez de uma gerada

// depreciação
my_property.deprecated = 1 // marca a propriedade como obsoleta
my_property.severity-default = warning // se a propriedade obsoleta for especificada, mas definida para um valor padrão
my_property.severity-override = error  // se a propriedade obsoleta for especificada e definida para um valor não padrão

```
Além disso, você pode definir os seguintes atributos em uma categoria de configuração:
```
[my_extension]
// `group` - grupo de categoria de game.project, por exemplo, Main, Platforms, Components, Runtime, Distribution
group = Runtime
// `title` - título exibido da categoria
title = My Awesome Extension
// `help` - ajuda exibida da categoria
help = Settings for My Awesome Extension
```


No momento, meta properties são usadas apenas em `bob.jar` ao empacotar a aplicação, mas futuramente serão analisadas pelo editor e representadas no visualizador de *game.project*.
