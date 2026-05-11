#### P: Quais são os requisitos de sistema para o editor?
R: O editor usará até 75% da memória disponível do sistema. Em um computador com 4 GB de RAM, isso deve ser suficiente para projetos Defold menores. Para projetos médios ou grandes, recomenda-se usar 6 GB ou mais de RAM.


#### P: As versões beta do Defold são atualizadas automaticamente?
R: Sim. O editor beta do Defold verifica se há uma atualização na inicialização, assim como a versão estável do Defold.


#### P: Por que recebo um erro dizendo `java.awt.AWTError: Assistive Technology not found` ao iniciar o editor?
R: Esse erro está relacionado a problemas com tecnologia assistiva Java, como o [leitor de tela NVDA](https://www.nvaccess.org/download/). Você provavelmente tem um arquivo `.accessibility.properties` na sua pasta home. Remova o arquivo e tente iniciar o editor novamente. (Observação: se você usa alguma tecnologia assistiva e precisa que esse arquivo esteja presente, entre em contato conosco pelo endereço info@defold.se para discutir soluções alternativas).

Discutido [aqui no fórum do Defold](https://forum.defold.com/t/editor-endless-loading-windows-10-1-2-169-solved/65481/3).


#### P: Por que recebo um erro dizendo `sun.security.validator.ValidatorException: PKIX path building failed` ao iniciar o editor?
R: Essa exceção ocorre quando o editor tenta fazer uma conexão https, mas a cadeia de certificados fornecida pelo servidor não pode ser verificada.

Veja [este link](https://github.com/defold/defold/blob/master/editor/README_TROUBLESHOOTING_PKIX.md) para detalhes sobre esse erro.


#### P: Por que recebo um `java.lang.OutOfMemoryError: Java heap space` ao executar certas operações?
R: O editor Defold é criado com Java e, em alguns casos, a configuração padrão de memória do Java pode não ser suficiente. Se isso acontecer, você pode configurar manualmente o editor para alocar mais memória editando o arquivo de configuração do editor. O arquivo de configuração, chamado `config`, fica na pasta `Defold.app/Contents/Resources/` no macOS. No Windows, ele fica ao lado do executável `Defold.exe`; no Linux, ao lado do executável `Defold`. Abra o arquivo `config` e adicione `-Xmx6gb` à linha que começa com `vmargs`. Adicionar `-Xmx6gb` definirá o tamanho máximo da heap para 6 gigabytes (o padrão geralmente é 4Gb). Ele deve ficar parecido com isto:

```
vmargs = -Xmx6gb,-Dfile.encoding=UTF-8,-Djna.nosys=true,-Ddefold.launcherpath=${bootstrap.launcherpath},-Ddefold.resourcespath=${bootstrap.resourcespath},-Ddefold.version=${build.version},-Ddefold.editor.sha1=${build.editor_sha1},-Ddefold.engine.sha1=${build.engine_sha1},-Ddefold.buildtime=${build.time},-Ddefold.channel=${build.channel},-Ddefold.archive.domain=${build.archive_domain},-Djava.net.preferIPv4Stack=true,-Dsun.net.client.defaultConnectTimeout=30000,-Dsun.net.client.defaultReadTimeout=30000,-Djogl.texture.notexrect=true,-Dglass.accessible.force=false,--illegal-access=warn,--add-opens=java.base/java.lang=ALL-UNNAMED,--add-opens=java.desktop/sun.awt=ALL-UNNAMED,--add-opens=java.desktop/sun.java2d.opengl=ALL-UNNAMED,--add-opens=java.xml/com.sun.org.apache.xerces.internal.jaxp=ALL-UNNAMED
```
