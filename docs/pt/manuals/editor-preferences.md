---
title: Preferências do editor
brief: Você pode modificar as configurações do editor pela janela Preferences.
---

# Preferências do editor

Você pode modificar as configurações do editor pela janela Preferences. A janela de preferências é aberta pelo menu <kbd>File -> Preferences</kbd>.

## General

![](images/editor/preferences_general.png)

Load External Changes on App Focus
: Habilita a varredura de alterações externas quando o editor recebe foco.

Open Bundle Target Folder
: Habilita a abertura da pasta de destino do pacote depois que o processo de empacotamento termina.

Enable Texture Compression
: Habilita a [compressão de textura](/manuals/texture-profiles) para todos os builds feitos pelo editor.

Escape Quits Game
: Encerra um build em execução do seu jogo usando a tecla <kbd>Esc</kbd>.

Track Active Tab in Asset Browser
: O arquivo editado na aba selecionada no painel *Editor* será selecionado no Asset Browser (também conhecido como painel *Assets*).

Lint Code on Build
: Habilita [linting de código](/manuals/writing-code/#linting-configuration) quando o projeto é compilado. Esta opção é habilitada por padrão, mas pode ser desabilitada se o linting em um projeto grande levar tempo demais.

Engine Arguments
: Argumentos que serão passados ao executável dmengine quando o editor compilar e executar.
 Use um argumento por linha. Por exemplo:
 ```
--config=bootstrap.main_collection=/my dir/1.collectionc
--verbose
--graphics-adapter=vulkan
```


## Code

![](images/editor/preferences_code.png)

Custom Editor
: Caminho absoluto para um editor externo. No macOS, deve ser o caminho para o executável dentro do .app (por exemplo, `/Applications/Atom.app/Contents/MacOS/Atom`).

Open File
: O padrão usado pelo editor personalizado para especificar qual arquivo abrir. O padrão `{file}` será substituído pelo nome do arquivo a abrir.

Open File at Line
: O padrão usado pelo editor personalizado para especificar qual arquivo abrir e em qual número de linha. O padrão `{file}` será substituído pelo nome do arquivo a abrir, e `{line}` pelo número da linha.

Code editor font
: Nome de uma fonte instalada no sistema para usar no editor de código.

Zoom on Scroll
: Define se o tamanho da fonte deve mudar ao rolar no editor de código enquanto mantém o botão Cmd/Ctrl pressionado.

Auto-insert closing parens
: Insere automaticamente os caracteres de fechamento correspondentes durante a edição de código. Esta opção vem ativada por padrão.


### Abrir arquivos de script no Visual Studio Code

![](images/editor/preferences_vscode.png)

Para abrir arquivos de script do Defold Editor diretamente no Visual Studio Code, você deve definir as seguintes configurações especificando o caminho para o arquivo executável:

- MacOS: `/Applications/Visual Studio Code.app/Contents/MacOS/Electron`
- Linux: `/usr/bin/code`
- Windows: `C:\Program Files\Microsoft VS Code\Code.exe`

 Defina estes parâmetros para abrir arquivos e linhas específicas:

- Open File: `. {file}`
- Open File at Line: `. -g {file}:{line}`

O caractere `.` aqui é necessário para abrir o workspace inteiro, não um arquivo individual.


## Extensions

![](images/editor/preferences_extensions.png)

Build Server
: URL do servidor de build usado ao compilar um projeto que contém [extensões nativas](/manuals/extensions). É possível adicionar um nome de usuário e token de acesso à URL para acesso autenticado ao servidor de build. Use a seguinte notação para especificar o nome de usuário e o token de acesso: `username:token@build.defold.com`. Acesso autenticado é necessário para builds Nintendo Switch e ao executar sua própria instância de servidor de build com autenticação habilitada ([consulte a documentação do servidor de build](https://github.com/defold/extender/blob/dev/README_SECURITY.md) para mais informações). O nome de usuário e a senha também podem ser definidos como as variáveis de ambiente do sistema `DM_EXTENDER_USERNAME` e `DM_EXTENDER_PASSWORD`.

Build Server Username
: nome de usuário para autenticação.

Build Server Password
: senha para autenticação; será armazenada criptografada no arquivo de preferências.

Build Server Headers
: headers adicionais para o servidor de build ao compilar extensões nativas. Isso é importante para usar o serviço CloudFlare ou serviços semelhantes com o Extender.

## Tools

![](images/editor/preferences_tools.png)

ADB path
: Caminho para a ferramenta de linha de comando [ADB](https://developer.android.com/tools/adb) instalada neste sistema. Se você tiver o ADB instalado no seu sistema, o editor Defold o usará para instalar e executar APKs Android empacotados em um dispositivo Android conectado. Por padrão, o editor verifica se o ADB está instalado em locais conhecidos, então você só precisa especificar o caminho se tiver o ADB instalado em um local personalizado.

ios-deploy path
: Caminho para as ferramentas de linha de comando [ios-deploy](https://github.com/ios-control/ios-deploy) instaladas neste sistema (relevante apenas para macOS). De forma semelhante ao caminho do ADB, o editor Defold usará esta ferramenta para instalar e executar aplicações iOS empacotadas em um iPhone conectado. Por padrão, o editor verifica se ios-deploy está instalado em locais conhecidos, então você só precisa especificar o caminho se usar uma instalação personalizada do ios-deploy.

## Keymap

![](images/editor/preferences_keymap.png)

Você pode configurar os atalhos de teclado e controles de mouse do editor na aba Keymap. Para alterar um comando, dê um duplo clique nele, pressione <kbd>Enter</kbd> ou <kbd>Space</kbd>, ou use o menu de contexto da linha.

Atalhos de teclado aparecem como combinações de teclas na coluna *Shortcuts*. Controles de mouse aparecem na mesma lista com um marcador:

- <kbd>MB</kbd> significa uma vinculação de botão do mouse, opcionalmente combinada com <kbd>Shift</kbd>, <kbd>Ctrl</kbd>/<kbd>Control</kbd> ou <kbd>Alt</kbd>.
- <kbd>MM</kbd> significa uma tecla modificadora usada por uma ação de mouse.

Alguns controles de mouse reutilizam vinculações do Scene 2D Camera padrão, então uma linha pode mostrar uma vinculação antes de você personalizá-la. Elas geralmente são exibidas com uma cor mais escura. Se você definir uma vinculação personalizada para essa linha, o Defold usará a sua vinculação. Use *Reset to Defaults* para remover sua alteração e voltar ao comportamento integrado ou herdado.

Avisos são exibidos em laranja. Passe o mouse sobre um aviso para ver detalhes. Avisos geralmente significam:
- o atalho pode digitar texto e interferir em campos de texto.
- o mesmo atalho ou vinculação de mouse já está sendo usado por outro comando.
