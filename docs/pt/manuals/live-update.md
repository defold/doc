---
title: Conteúdo Live Update no Defold
brief: A funcionalidade Live Update fornece um mecanismo que permite ao runtime buscar e armazenar no pacote da aplicação recursos que foram intencionalmente deixados fora do pacote durante a build. Este manual explica como ela funciona.
---

# Live Update

Ao empacotar um jogo, o Defold empacota todos os recursos do jogo no pacote específico da plataforma resultante. Na maioria dos casos, isso é preferível, pois a engine em execução tem acesso instantâneo a todos os recursos e pode carregá-los rapidamente do armazenamento. No entanto, há situações em que você pode querer adiar o carregamento de recursos para um estágio posterior. Por exemplo:

- Seu jogo tem uma série de episódios e você deseja incluir apenas o primeiro para os jogadores experimentarem antes de decidirem se querem continuar com o restante do jogo.
- Seu jogo é voltado para HTML5. No navegador, carregar uma aplicação do armazenamento significa que todo o pacote da aplicação precisa ser baixado antes da inicialização. Em uma plataforma assim, talvez você queira enviar um pacote inicial mínimo e colocar o app em execução rapidamente antes de baixar o restante dos recursos do jogo.
- Seu jogo contém recursos muito grandes (imagens, vídeos etc.) que você deseja baixar apenas quando estiverem prestes a aparecer no jogo. Isso mantém o tamanho de instalação menor.

A funcionalidade Live Update expande o conceito de proxy de coleção com um mecanismo que permite ao runtime buscar e armazenar no pacote da aplicação recursos que foram intencionalmente deixados fora do pacote durante a build.

Ela permite dividir seu conteúdo em vários arquivos:

* _Base Archive_
* Level Common Files
* Level Pack 1
* Level Pack 2
* ...

## Preparando conteúdo para Live Update

Suponha que estamos criando um jogo que contém recursos de imagem grandes e em alta resolução. O jogo mantém essas imagens em coleções com um objeto de jogo e um sprite com a imagem:

![Mona Lisa collection](images/live-update/mona-lisa.png)

Para fazer a engine carregar essa coleção dinamicamente, podemos simplesmente adicionar um componente de proxy de coleção e apontá-lo para *`monalisa.collection`*. Agora o jogo pode escolher quando carregar o conteúdo da coleção do armazenamento para a memória enviando uma mensagem `load` ao proxy de coleção. No entanto, queremos ir além e controlar nós mesmos o carregamento dos recursos contidos na coleção.

Isso é feito simplesmente marcando a caixa *Exclude* nas propriedades do proxy de coleção, instruindo o Defold a deixar qualquer conteúdo em *`monalisa.collection`* fora ao criar um pacote de aplicação.

::: important
Qualquer recurso referenciado pelo pacote base do jogo não será excluído.
:::

![Collection proxy excluded](images/live-update/proxy-excluded.png)

## Configurações de Live Update

Quando o Defold cria um pacote de aplicação, ele precisa armazenar em algum lugar quaisquer recursos excluídos. As configurações do projeto para Live Update controlam o local desses recursos. As configurações são encontradas em <kbd>Projeto ▸ Live update Settings...</kbd>. Isso criará um arquivo de configurações se nenhum existir. Em *game.project*, selecione qual arquivo de configurações live-update usar ao empacotar. Isso permite usar configurações live-update diferentes para ambientes diferentes, por exemplo live, QA, desenvolvimento etc.

![Live update settings](images/live-update/05-liveupdate-settings-zip.png)

Atualmente, há três formas pelas quais o Defold pode armazenar os recursos. Escolha o método no menu suspenso *Mode* na janela de configurações:

`Zip`
: Esta opção informa ao Defold para criar um arquivo Zip com quaisquer recursos excluídos. O arquivo é salvo no local especificado na configuração *Export path*.

`Folder`  
: Esta opção informa ao Defold para criar uma pasta com todos os recursos excluídos. Ela funciona exatamente da mesma forma que Zip, mas usa um diretório em vez de um arquivo compactado. Isso pode ser útil em casos em que você precisa pós-processar arquivos antes do upload e planeja compactá-los em um arquivo por conta própria.

`Amazon`
: Esta opção informa ao Defold para fazer upload automático dos recursos excluídos para um bucket Amazon Web Service (AWS) S3. Preencha o nome do seu *Credential profile* AWS, selecione o *Bucket* apropriado e forneça um nome de *Prefix*. Você pode ler mais sobre como configurar uma conta AWS neste [guia da aws](/manuals/live-update-aws)

## Empacotando com Live Update

::: important
Compilar e executar a partir do editor (<kbd>Projeto ▸ Compilar</kbd>) não oferece suporte a Live Update. Para testar Live Update, você precisa empacotar o projeto.
:::

Empacotar com Live Update é fácil. Selecione <kbd>Projeto ▸ Empacotar ▸ ...</kbd> e então a plataforma para a qual deseja criar um pacote de aplicação. Isso abre o diálogo de empacotamento:

![Bundle Live application](images/live-update/bundle-app.png)

Ao empacotar, qualquer recurso excluído ficará fora do pacote de aplicação. Ao marcar a caixa *Publish Live update content*, você instrui o Defold a fazer upload dos recursos excluídos para a Amazon ou a criar um arquivo Zip, dependendo de como você configurou suas definições de Live Update (veja acima). O conteúdo Live Update publicado ainda inclui `liveupdate.game.dmanifest`, que contém a lista completa de recursos necessária para entrega remota.

Ao publicar conteúdo Live Update baseado em arquivos, *Strip Live Update Entries from Main Manifest* (`liveupdate.exclude_entries_from_main_manifest`) é habilitado por padrão. Com essa configuração habilitada, recursos exclusivos de Live Update são removidos do `game.dmanifest` empacotado, o que reduz o tamanho do pacote e o uso de memória em tempo de execução. Desabilite-a apenas se você precisar do comportamento descontinuado em que entradas excluídas permanecem no `game.dmanifest` empacotado.

Com a configuração padrão habilitada, `collectionproxy.get_resources()` retorna `{}` até que o arquivo relevante tenha sido montado. Após a montagem, ela retorna os hashes de recursos para esse proxy.

Clique em *Package* e selecione um local para o pacote de aplicação. Agora você pode iniciar a aplicação e verificar se tudo funciona conforme esperado.

## Os arquivos .zip

Um arquivo .zip live update contém arquivos que foram excluídos do pacote base do jogo.

Embora nosso pipeline atual ofereça suporte apenas à criação de um único arquivo .zip, na prática é possível dividir esse arquivo zip em arquivos .zip menores. Isso permite downloads menores para um jogo: pacotes de fases, conteúdo sazonal etc. Cada arquivo .zip também contém um arquivo de manifesto que descreve os metadados de cada recurso contido dentro do arquivo .zip.

## Dividindo arquivos .zip

Muitas vezes é desejável dividir o conteúdo excluído em vários arquivos menores para ter controle mais granular sobre o uso de recursos. Um exemplo é dividir um jogo baseado em fases em vários pacotes de fases. Outro é colocar decorações de UI com temas de feriados diferentes em arquivos separados e carregar e montar apenas o tema atualmente ativo no calendário.

O grafo de recursos é armazenado em `build/default/game.graph.json` e é gerado automaticamente sempre que o projeto é empacotado. O arquivo gerado contém uma lista de todos os recursos do projeto e as dependências de cada recurso. Exemplo de entrada:

```json
{
  "path" : "/game/player.goc",
  "hexDigest" : "caa342ec99794de45b63735b203e83ba60d7e5a1",
  "children" : [ "/game/ship.spritec", "/game/player.scriptc" ]
}
```

Cada entrada tem um `path`, que representa o caminho único do recurso dentro do projeto. O `hexDigest` representa a impressão digital criptográfica do recurso e será o nome do arquivo usado no arquivo .zip liveupdate. Por fim, o campo `children` é uma lista de outras dependências das quais esse recurso depende. No exemplo acima, `/game/player.goc` tem uma dependência de um componente sprite e de um componente script.

Você pode analisar o arquivo `game.graph.json` e usar essas informações para identificar grupos de entradas no grafo de recursos e armazenar seus recursos correspondentes em arquivos separados junto com o arquivo de manifesto original (o arquivo de manifesto será podado em tempo de execução para conter apenas os arquivos no arquivo montado).

## Live Update no Android

É possível usar Play Asset Delivery para baixar e montar conteúdo Live Update. Saiba mais [no manual oficial](https://defold.com/extension-pad/).

## Verificação de conteúdo

Uma das principais funcionalidades do sistema live update é que agora você pode usar muitos arquivos de conteúdo, potencialmente de muitas versões diferentes do Defold.

O comportamento padrão de `liveupdate.add_mount()` é adicionar uma verificação de versão da engine ao anexar um mount.
Isso significa que tanto o arquivo base do jogo quanto o(s) arquivo(s) live update precisam ser criados ao mesmo tempo com a mesma versão da engine, usando a opção de empacotamento. Isso invalidará quaisquer arquivos baixados anteriormente pelo cliente, forçando-o a baixar o conteúdo novamente.

Esse comportamento pode ser desativado com uma flag de opções.
Quando desativado, a responsabilidade pela verificação de conteúdo fica inteiramente com o desenvolvedor, para garantir que cada arquivo live update funcionará com a engine em execução.

Recomendamos armazenar alguns metadados para cada mount, para que _logo na inicialização_ o desenvolvedor possa decidir se o mount/arquivo deve ser removido.
Uma forma de fazer isso é adicionar um arquivo extra ao arquivo zip depois que o jogo tiver sido empacotado. Por exemplo, inserindo um `metadata.json` com qualquer informação relevante que o jogo exija. Então, na inicialização, o jogo pode recuperá-lo com `sys.load_resource("/metadata.json")`. _Observe que você precisará de um nome único para os dados personalizados de cada mount, ou os mounts fornecerão o arquivo com a maior prioridade_

Se você não fizer isso, pode acabar em uma situação em que o conteúdo não é compatível com a engine de forma alguma, forçando-a a encerrar.

## Mounts

O sistema live update pode usar vários arquivos de conteúdo ao mesmo tempo.
Cada arquivo é "montado" no sistema de recursos da engine, com um nome e prioridade.

Se dois arquivos tiverem o mesmo arquivo `sprite.texturec`, a engine carregará o arquivo do mount com a prioridade mais alta.

A engine não mantém referência a nenhum recurso em um mount. Depois que um recurso é carregado na memória, o arquivo pode ser desmontado. O recurso permanecerá na memória até ser descarregado.

Os mounts são readicionados automaticamente na reinicialização da engine.

::: sidenote
Montar um arquivo não copia nem move o arquivo. A engine armazena apenas o caminho para o arquivo. Portanto, o desenvolvedor pode remover o arquivo a qualquer momento, e o mount também será removido na próxima inicialização.
:::

## Programando com Live Update

Para realmente usar o conteúdo live update, você precisa baixar e montar os dados no seu jogo.
Leia mais sobre como [programar com live update aqui](/manuals/live-update-scripting).

::: important
O fluxo antigo de Live Update de recurso único foi descontinuado. Evite `collectionproxy.missing_resources()`, as APIs de manifesto descontinuadas (`liveupdate.get_current_manifest()`, `liveupdate.store_resource()`, `liveupdate.store_manifest()`, `liveupdate.store_archive()`, `liveupdate.is_using_liveupdate_data()`) e os antigos aliases auxiliares `resource.*` (`resource.get_current_manifest()`, `resource.store_resource()`, `resource.store_manifest()`, `resource.store_archive()`, `resource.is_using_liveupdate_data()`) em projetos novos.

Projetos atuais devem publicar arquivos, montá-los com `liveupdate.add_mount()`, gerenciá-los com `liveupdate.get_mounts()` e `liveupdate.remove_mount()`, e usar `collectionproxy.get_resources()` quando precisarem inspecionar conteúdo excluído de um proxy. Chaves antigas de assinatura de manifesto não fazem mais parte deste pipeline: `publickey` e `privatekey` de `liveupdate.settings` estão descontinuadas e não são usadas, e `game.public.der` não é mais gerado nem empacotado.
:::

## Observações de desenvolvimento

Depuração
: Ao executar uma versão empacotada do seu jogo, você não tem acesso direto a um console. Isso causa problemas para depuração. No entanto, você pode executar a aplicação pela linha de comando ou clicando duas vezes diretamente no executável no pacote:

  ![Running a bundle application](images/live-update/run-bundle.png)

  Agora o jogo inicia com uma janela de shell que exibirá quaisquer instruções `print()`:

  ![Console output](images/live-update/run-bundle-console.png)

Forçando novo download de recursos
: O desenvolvedor pode baixar o conteúdo para qualquer arquivo/pasta que desejar, mas frequentemente eles ficam sob o caminho da aplicação. O local da pasta de suporte da aplicação depende do sistema operacional. Ele pode ser encontrado com `print(sys.get_save_file("", ""))`.

  O arquivo liveupdate.mounts está localizado sob o "local storage", e seu caminho é exibido no console na inicialização: "INFO:LIVEUPDATE: Live update folder located at: ..."

  ![Local storage](images/live-update/local-storage.png)
