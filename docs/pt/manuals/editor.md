---
title: Visão geral do editor
brief: Este manual oferece uma visão geral de como o editor Defold se parece, como funciona e como navegar nele.
---

# Visão geral do editor

O editor permite navegar e manipular todos os arquivos e pastas do seu projeto de jogo de forma eficiente. Editar arquivos abre um editor adequado e mostra todas as informações relevantes sobre o arquivo em visualizações separadas.

## Iniciando o editor

Quando você executa o Defold Editor, uma tela de seleção e criação de projetos é exibida. Clique para selecionar o que deseja fazer:

MY PROJECTS
: Aqui ficam seus projetos abertos recentemente, para que você possa acessá-los rapidamente. Esta é a visualização padrão da tela inicial.

  Se você não abriu nenhum projeto antes (ou removeu todos), ela mostrará dois botões: você pode clicar em `Open From Disk…` para encontrar e abrir um usando o navegador de arquivos do sistema, ou clicar no botão `Create New Project`, e ela mudará para a aba `TEMPLATES`.

  ![meus projetos](images/editor/start_no_projects.png)


  Se você já abriu projetos antes, ela mostrará uma lista dos seus projetos, como na imagem abaixo:

  ![meus projetos](images/editor/start_my_projects.png)

TEMPLATES
: Contém projetos básicos vazios ou quase vazios, feitos para iniciar rapidamente um novo projeto Defold para certas plataformas ou usando certas extensões.


TUTORIALS
: Contém projetos com tutoriais guiados para aprender, jogar e modificar, caso você queira seguir um tutorial.


SAMPLES
: Contém projetos preparados para demonstrar certos casos de uso.

  ![Novo projeto](images/editor/start_templates.png)

Quando você cria um novo projeto, ele é armazenado no seu disco local, e todas as edições feitas são salvas localmente.

Você pode saber mais sobre as diferentes opções no [manual de configuração de projeto](https://www.defold.com/manuals/project-setup/).

## Idioma do editor

No canto inferior esquerdo da tela inicial, você pode ver uma seleção de Language; selecione uma das localizações atualmente disponíveis. Isso também está disponível no editor em `File ▸ Preferences ▸ General ▸ Editor Language`.

![Idiomas](images/editor/languages.png)

## Os painéis do editor {#the-editor-views}

O Defold Editor é separado em um conjunto de painéis, ou visualizações, que exibem informações específicas.

![Editor 2](images/editor/editor_overview.png)

### 1. Painel Assets
Lista todos os arquivos e pastas que fazem parte do seu projeto em uma estrutura de árvore, correspondente à mesma estrutura no seu disco. Clique e role para navegar pela lista. Todas as operações orientadas a arquivos podem ser feitas nesta visualização:

   - <kbd>Left Mouse Click</kbd> para selecionar qualquer arquivo ou pasta; mantendo <kbd>⇧ Shift</kbd> pressionado você pode expandir a seleção, ou mantendo <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> pressionado você pode selecionar/desselecionar o item clicado.
   - <kbd>Double Mouse Click</kbd> em um arquivo para abri-lo em um editor específico para aquele tipo de arquivo.
   - <kbd>Drag and Drop</kbd> para adicionar ao projeto arquivos de outro lugar do seu disco ou mover arquivos e pastas para novos locais no projeto.
   - <kbd>Right Mouse Click</kbd> para abrir um _Context Menu_ de onde você pode criar novos arquivos ou pastas, renomear, excluir, rastrear dependências de arquivo e mais.

### 2. Painel Scene Editor {#the-scene-editor}

Dar duplo clique em uma coleção, objeto de jogo ou arquivo de componente visual abre o *Scene Editor*, o editor visual para construir e editar cenas. Arquivos de script e outros recursos não visuais são abertos em seus próprios editores dedicados.

![Scene Editor](images/editor/2d_scene.png)

Alguns dos recursos principais oferecidos pelo Scene Editor:

- [Navegação de cena 2D e 3D](/manuals/scene-editing/#2d-and-3d-scene-orientation) com modos de câmera ortográfica e perspectiva
- [Ferramentas de transformação](/manuals/scene-editing/#manipulating-objects) para mover, rotacionar e escalar objetos
- [Free Camera Mode](/manuals/scene-editing/#free-camera-mode) para navegação 3D em primeira pessoa
- [Configurações de grid](/manuals/scene-editing/#grid-settings) com tamanho, plano e aparência configuráveis
- [Filtros de visibilidade](/manuals/scene-editing/#visibility-filters) para alternar tipos de componentes e guias

Leia mais no [manual do Scene Editor](/manuals/scene-editing/).

### 3. Painel Outline

Esta visualização mostra o conteúdo do arquivo atualmente sendo editado, mas em uma estrutura de árvore hierárquica. O Outline reflete a visualização do editor e permite realizar operações nos seus itens:

   - <kbd>Left Mouse Click</kbd> para selecionar um item; mantendo <kbd>⇧ Shift</kbd> pressionado você pode expandir a seleção, ou mantendo <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> pressionado você pode selecionar/desselecionar o item clicado.
   - <kbd>Drag and drop</kbd> para mover itens. Solte um objeto de jogo sobre outro objeto de jogo em uma coleção para criar uma relação pai-filho.
   - <kbd>Right Mouse Click</kbd> para abrir um _Context Menu_ de onde você pode adicionar itens, excluir itens selecionados etc.

É possível alternar a visibilidade de objetos de jogo e componentes visuais clicando no pequeno ícone de olho `👁` à direita de um elemento na lista.

![Outline](images/editor/outline.png)

### 4. Painel Properties

Esta visualização mostra propriedades associadas ao item selecionado no momento, como Id, URL, Position, Rotation, Scale e/ou outras propriedades específicas de componente, além de propriedades personalizadas para scripts.

Você também pode <kbd>Drag</kbd> a seta vertical `↕` e mover o mouse para alterar o valor da propriedade numérica fornecida.

![Properties](images/editor/properties.png)

### 5. Painel Tools

Esta visualização tem várias abas.

A aba *Console*: mostra qualquer saída de erro, aviso e informação da engine, ou impressão proposital que você faz enquanto seu jogo está em execução,

*Build Errors*: mostra erros do processo de build,

*Search Results*: mostra resultados de busca (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd> + <kbd>F</kbd>) no projeto inteiro, se você clicar em `Keep Results`

*Curve Editor*: usada ao editar curvas no [Particle Editor](/manuals/particlefx/).

O painel Tools também é usado para interagir com o depurador integrado. Leia mais sobre isso no [manual de depuração](/manuals/debugging/).

### 6. Painel Changed Files

Se seu projeto usa o sistema de controle de versão distribuído Git, esta visualização lista quaisquer arquivos que foram alterados, adicionados ou excluídos no seu projeto. Ao sincronizar o projeto regularmente, você pode alinhar sua cópia local com o que está armazenado no repositório Git do projeto; dessa forma, pode colaborar em uma equipe e não perderá seu trabalho se algo der errado. Você pode aprender mais sobre Git no nosso [manual de controle de versão](/manuals/version-control/). Algumas operações orientadas a arquivos podem ser executadas nesta visualização:

   - <kbd>Left Mouse Click</kbd> - para selecionar um arquivo específico; mantendo <kbd>⇧ Shift</kbd> pressionado você pode expandir a seleção, ou mantendo <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> pressionado você pode selecionar/desselecionar o item clicado. Se um único arquivo alterado estiver selecionado, você pode clicar em `Diff` para mostrar as diferenças. Você pode clicar em `Revert` para desfazer alterações em todos os arquivos selecionados.
   - <kbd>Double Left Mouse Click</kbd> em um arquivo para abrir uma visualização do arquivo. O editor abre o arquivo em um editor adequado, assim como na visualização de assets.
   - <kbd>Right Mouse Click</kbd> em um arquivo para abrir um menu popup de onde você pode abrir uma visualização de diff, reverter todas as alterações feitas no arquivo, encontrar o arquivo no sistema de arquivos e mais.

### Barra de menu

No topo da visualização do editor, ou na barra do sistema no Mac, você encontra a barra de menu com 6 menus: `File`, `Edit`, `View`, `Project`, `Debug`, `Help`. Suas funções serão explicadas nos manuais.

### Barra de status

Na barra inferior do editor, há um espaço estreito em que o status é exibido, por exemplo:
- quando uma nova atualização está disponível, um botão clicável `Update Available` ficará visível; veja a seção Atualizando o editor neste manual abaixo.
- quando um build ou empacotamento está em andamento, o progresso será apresentado ali.

## Tamanho e visibilidade dos painéis

O tamanho dos painéis pode ser ajustado dentro do editor usando <kbd>Dragging</kbd> nas bordas das seções entre todos os 6 painéis descritos acima.

A visibilidade dos painéis pode ser alternada no editor usando opções no menu `View` ou usando os atalhos fornecidos:
- `Toggle Assets Pane` (<kbd>F6</kbd>) para alternar a visibilidade dos painéis Assets e Changed Files
- `Toggle Changed Files` para alternar a visibilidade apenas do painel Changed Files
- `Toggle Tools Pane` (<kbd>F7</kbd>) para alternar a visibilidade do painel Tools
- `Toggle Properties Pane` (<kbd>F8</kbd>) para alternar a visibilidade dos painéis Outline e Properties

![Visibilidade dos painéis](images/editor/editor_panes.png)

No menu `View`, você também pode alternar ou alterar outras configurações relacionadas à visibilidade, como Grid, Guides, Camera, ajustar a visualização à seleção (`Frame Selection` ou tecla <kbd>F</kbd>) e alternar entre a visualização 2D e 3D padrão (`Realign Camera` ou tecla <kbd>.</kbd>), muitas delas também acessíveis pela barra de ferramentas ou por atalhos.

## Abas

Se você tiver vários arquivos abertos, uma aba separada para cada arquivo será mostrada no topo da visualização do editor. Abas em um único painel podem ser movidas: use <kbd>Drag and Drop</kbd> para trocar suas posições dentro da barra de abas. Você também pode:

- Usar <kbd>Right Mouse Click</kbd> em uma aba para abrir um _Context Menu_,
- Clicar em `Close` (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>W</kbd>) para fechar uma única aba,
- Clicar em `Close Others` para fechar todas as abas exceto a selecionada,
- Clicar em `Close All` (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd>+<kbd>W</kbd>) para fechar todas as abas no painel ativo,
- Selecionar `➝| Open As` para usar um editor diferente do padrão ou uma ferramenta externa associada definida em `File ▸ Preferences ▸ Code ▸ Custom Editor`. Veja mais no [manual de Preferences](/manuals/editor-preferences).

![Abas](images/editor/tabs_custom.png)

## Edição lado a lado

É possível abrir 2 visualizações de editor lado a lado.

- Use <kbd>Right Mouse Click</kbd> na aba do editor que deseja mover e selecione `Move to Other Tab Pane`.

![2 painéis](images/editor/2-panes.png)

Você também pode usar o menu da aba para `Swap with Other Tab Pane`, movendo a aba entre painéis, ou `Join Tab Panes`, unindo em um único painel.

## Criando novos arquivos de projeto {#creating-new-project-files}

Para criar novos arquivos de recurso, selecione `File ▸ New…` e então escolha o tipo de arquivo no menu, ou use o menu de contexto:

Use <kbd>Right Mouse Click</kbd> no local de destino no navegador `Assets` e selecione `New… ▸ [file type]`:

![criar arquivo](images/editor/create_file.png)

Digite um *Name* adequado para o novo arquivo e, se necessário, altere *Location*. O nome completo do arquivo, incluindo o sufixo do tipo de arquivo, é mostrado em *Preview* na caixa de diálogo:

![nome do arquivo a criar](images/editor/create_file_name.png)

## Templates

É possível especificar templates personalizados para cada projeto. Para isso, crie uma nova pasta chamada `templates` no diretório raiz do projeto e adicione novos arquivos chamados `default.*` com as extensões desejadas, como `/templates/default.gui` ou `/templates/default.script`. Além disso, se o token `{{NAME}}` for usado nesses arquivos, ele será substituído pelo nome de arquivo especificado na janela de criação de arquivo.

Se um template estiver disponível para um determinado tipo de arquivo, sempre que um novo arquivo desse tipo for criado ele será inicializado com o conteúdo do arquivo em `templates`.


![Templates](images/editor/templates.png)

## Importando arquivos para seu projeto

Para adicionar arquivos de asset (imagens, sons, modelos etc.) ao seu projeto, basta arrastá-los e soltá-los na posição correta no navegador *Assets*. Isso fará _cópias_ dos arquivos no local selecionado na estrutura de arquivos do projeto. Leia mais sobre [como importar assets no nosso manual](/manuals/importing-assets/).

![Importar arquivos](images/editor/import.png)

## Atualizando o editor

O editor verificará atualizações automaticamente quando estiver conectado à internet. Quando uma atualização for detectada, um link azul clicável `Update Available` será mostrado no canto inferior esquerdo da tela de seleção de projeto ou no canto inferior direito da janela do editor.

![Atualização na seleção de projeto](images/editor/update_start.png)
![Atualização no editor](images/editor/update_available.png)

Pressione o link clicável `Update Available` para baixar e atualizar. Uma janela de confirmação com informações aparecerá; clique em `Download Update` para prosseguir.

![Popup de atualização do editor](images/editor/update.png)

Você verá o progresso do download na barra de status inferior:

![Progresso do download](images/editor/download_status.png)

Depois que a atualização for baixada, o link azul mudará para `Restart to Update`. Clique nele para reiniciar e abrir o editor atualizado.

![Reiniciar para atualizar](images/editor/restart_to_update.png)

## Preferences

Você pode modificar as configurações do editor na janela `Preferences`. Para abri-la, clique em `File ▸ Preferences…` ou use o atalho <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>,</kbd>

Leia mais detalhes no [manual de Preferences](/manuals/editor-preferences)

![Preferences](images/editor/preferences.png)

## Logs do editor {#editor-logs}
Se você encontrar um problema com o editor e precisar reportar uma issue (`Help  ▸ Report Issue`), é uma boa ideia fornecer arquivos de log do próprio editor. Para abrir o local dos logs no navegador do sistema, clique em `Help ▸ Show Logs`.

Leia mais no [manual Getting Help](/manuals/getting-help/#getting-help).

![Mostrar logs](images/editor/show_logs.png)

Os arquivos de logs do editor podem ser encontrados aqui:

  * Windows: `C:\Users\ **Your Username** \AppData\Local\Defold`
  * macOS: `/Users/ **Your Username** /Library/Application Support/` ou `~/Library/Application Support/Defold`
  * Linux: `$XDG_STATE_HOME/Defold` ou `~/.local/state/Defold`

Você também pode acessar os logs do editor enquanto o editor está em execução se ele tiver sido iniciado por um terminal/prompt de comando. Para iniciar o editor, use o comando:

```shell
# Linux:
$ ./path/to/Defold/Defold

# macOS:
$ > ./path/to/Defold.app/Contents/MacOS/Defold
```

## Servidor do editor

Quando o editor abre um projeto, ele inicia um servidor web em uma porta aleatória. O servidor pode ser usado para interagir com o editor a partir de outras aplicações. A porta é escrita no arquivo `.internal/editor.port`.

Além disso, o executável do editor tem a opção de linha de comando `--port` (ou `-p`), que permite especificar a porta durante a inicialização, por exemplo::
```shell
# Windows
.\path\to\Defold\Defold.exe --port 8181

# Linux:
./path/to/Defold/Defold --port 8181

# macOS:
./path/to/Defold/Defold.app/Contents/MacOS/Defold --port 8181
```

## Estilização do editor

A aparência do editor pode ser alterada com estilização personalizada. Leia mais no [manual de estilização do editor](/manuals/editor-styling).

## FAQ
:[Editor FAQ](../shared/editor-faq.md)
