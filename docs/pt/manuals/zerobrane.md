---
title: Depuração com ZeroBrane Studio
brief: Este manual explica como usar o ZeroBrane Studio para depurar código Lua no Defold.
---

# Depurando scripts Lua com ZeroBrane Studio

O Defold contém um depurador integrado, mas também é possível executar a IDE Lua gratuita e de código aberto _ZeroBrane Studio_ como depurador externo. O ZeroBrane Studio precisa estar instalado para usar os recursos de depuração. O programa é multiplataforma e roda tanto no macOS quanto no Windows.

Baixe o "ZeroBrane Studio" em http://studio.zerobrane.com

## Configuração do ZeroBrane

Para que o ZeroBrane encontre os arquivos no seu projeto, você precisa apontá-lo para o local do diretório do seu projeto Defold. Uma forma conveniente de descobrir isso é usar a opção <kbd>Show in Desktop</kbd> em um arquivo na raiz do seu projeto Defold.

1. Clique com o botão direito em *game.project*
2. Escolha <kbd>Show in Desktop</kbd>

![Show in Finder](images/zerobrane/show_in_desktop.png)

## Configurando o ZeroBrane

Para configurar o ZeroBrane, selecione <kbd>Project ▸ Project Directory ▸ Choose...</kbd>:

![Set up](images/zerobrane/setup.png)

Depois que isso for configurado para corresponder ao diretório atual do projeto Defold, deve ser possível ver a árvore de diretórios do projeto Defold no ZeroBrane, além de navegar e abrir os arquivos.

Outras alterações de configuração recomendadas, mas não obrigatórias, podem ser encontradas mais adiante neste documento.

## Iniciando o servidor de depuração

Antes de iniciar uma sessão de depuração, o servidor de depuração integrado do ZeroBrane precisa ser iniciado. A opção de menu para iniciá-lo fica no menu <kbd>Project</kbd>. Basta selecionar <kbd>Project ▸ Start Debugger Server</kbd>:

![Start debugger](images/zerobrane/startdebug.png)

## Conectando sua aplicação ao depurador

A depuração pode ser iniciada em qualquer ponto da vida da aplicação Defold, mas precisa ser iniciada ativamente por um script Lua. O código Lua para iniciar uma sessão de depuração é assim:

::: sidenote
Se o seu jogo sair quando `dbg.start()` for chamado, talvez seja porque o ZeroBrane detectou um problema e enviou o comando de saída para o jogo. Por algum motivo, o ZeroBrane precisa de um arquivo aberto para iniciar a sessão de depuração; caso contrário, ele exibirá:
"Can't start debugging without an opened file or with the current file not being saved 'untitled.lua')."
No ZeroBrane, abra o arquivo ao qual você adicionou `dbg.start()` para corrigir esse erro.
:::

```lua
dbg = require "builtins.scripts.mobdebug"
dbg.start()
```

Ao inserir o código acima na aplicação, ela se conectará ao servidor de depuração do ZeroBrane (por "localhost", por padrão) e pausará na próxima instrução a ser executada.

```txt
Debugger server started at localhost:8172.
Mapped remote request for '/' to '/Users/my_user/Documents/Projects/Defold_project/'.
Debugging session started in '/Users/my_user/Documents/Projects/Defold_project'.
```

Agora é possível usar os recursos de depuração disponíveis no ZeroBrane; você pode avançar passo a passo, inspecionar, adicionar e remover breakpoints etc.

::: sidenote
A depuração só será ativada para o contexto lua de onde a depuração foi iniciada. Ativar "shared_state" em *game.project* significa que você pode depurar toda a aplicação, independentemente de onde começou.
:::

![Stepping](images/zerobrane/code.png)

Se a tentativa de conexão falhar (possivelmente porque o servidor de depuração não está em execução), sua aplicação continuará a rodar normalmente depois que a tentativa de conexão for feita.

## Depuração remota

Como a depuração acontece por conexões de rede comuns (TCP), isso permite depuração remota. Isso significa que é possível depurar sua aplicação enquanto ela está rodando em um dispositivo móvel.

A única alteração necessária é no comando que inicia a depuração. Por padrão, `start()` tentará se conectar ao localhost, mas para depuração remota precisamos especificar manualmente o endereço do servidor de depuração do ZeroBrane, assim:

```lua
dbg = require "builtins.scripts.mobdebug"
dbg.start("192.168.5.101")
```

Isso também significa que é importante garantir conectividade de rede a partir do dispositivo remoto e que firewalls ou softwares similares permitam conexões TCP pela porta 8172. Caso contrário, a aplicação pode travar ao iniciar enquanto tenta estabelecer a conexão com seu servidor de depuração.

## Outra configuração recomendada do ZeroBrane

É possível fazer o ZeroBrane abrir automaticamente arquivos de script Lua durante a depuração. Isso permite entrar em funções de outros arquivos de origem sem precisar abri-los manualmente.

O primeiro passo é acessar o arquivo de configuração do editor. Recomenda-se alterar a versão de usuário do arquivo.

- Selecione <kbd>Edit ▸ Preferences ▸ Settings: User</kbd>
- Adicione o seguinte ao arquivo de configuração:

  ```txt
  - to automatically open files requested during debugging
  editor.autoactivate = true
  ```

- Reinicie o ZeroBrane

![Other recommended settings](images/zerobrane/otherrecommended.png)
