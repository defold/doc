---
title: Manual de segurança de aplicações
brief: Este manual aborda várias áreas relacionadas a práticas de desenvolvimento seguro.
---

# Segurança de aplicações

Segurança de aplicações é um tema amplo que cobre desde práticas de desenvolvimento seguro até a proteção do conteúdo do seu jogo depois que ele foi lançado. Este manual aborda várias áreas e as coloca no contexto da segurança de aplicações ao usar a engine, as ferramentas e os serviços do Defold:

* Proteção de propriedade intelectual
* Soluções anti-cheat
* Comunicação de rede segura
* Uso de software de terceiros
* Uso de servidores de build na nuvem
* Conteúdo baixável


## Protegendo sua propriedade intelectual contra roubo
Uma preocupação comum entre desenvolvedores é como proteger suas criações contra roubo. Do ponto de vista jurídico, direitos autorais, patentes e marcas registradas podem ser usados para proteger diferentes aspectos da propriedade intelectual de videogames. Direitos autorais dão ao proprietário o direito exclusivo de distribuir a obra criativa, patentes protegem invenções, e marcas registradas protegem nomes, símbolos e logotipos.

Também pode ser desejável tomar precauções técnicas para proteger a obra criativa de um jogo. No entanto, é importante lembrar que, depois que o jogo está nas mãos do jogador, é possível encontrar formas de extrair os assets. Isso pode ser feito por engenharia reversa da aplicação e dos arquivos do jogo, mas também usando ferramentas para extrair texturas e modelos enquanto eles são enviados para a GPU ou quando outros assets são carregados na memória.

Por esse motivo, nossa posição geral é que, se os usuários estiverem determinados a extrair os assets de um jogo, eles conseguirão fazer isso.

Desenvolvedores podem adicionar suas próprias proteções para dificultar, __mas não impossibilitar__, a extração dos assets. Isso normalmente inclui vários meios de criptografia e ofuscação para proteger e ocultar assets do jogo.

### Ofuscação de código-fonte
Aplicar ofuscação de código-fonte é um processo automatizado no qual o código-fonte é deliberadamente tornado difícil para humanos entenderem, sem afetar a saída do programa. O objetivo costuma ser proteger contra roubo, mas também dificultar trapaças.

É possível aplicar ofuscação de código-fonte no Defold como uma etapa de pré-build ou como uma parte integrada do processo de build do Defold. Com ofuscação antes do build, o código-fonte é ofuscado usando uma ferramenta de ofuscação antes que o processo de build do Defold seja iniciado.

Já a ofuscação em tempo de build é integrada ao processo de build usando um plugin Lua builder. Um plugin Lua builder recebe o código-fonte bruto como entrada e retorna uma versão ofuscada do código-fonte como saída. Um exemplo de ofuscação em tempo de build é mostrado na [extensão Prometheus](https://github.com/defold/extension-prometheus), baseada no ofuscador Lua Prometheus disponível no GitHub. Abaixo você encontra um exemplo de uso do Prometheus para ofuscar agressivamente um trecho de código. Observe que esse tipo de ofuscação pesada afeta o desempenho em runtime do código Lua:

Exemplo:

```
function init(self)
 print("hello")
 test.greet("Bob")
end
```

Saída ofuscada:

```
local v={"+qdW","ZK0tEKf=";"XP/IX3+="}for o,J in ipairs({{1;3};{1,1},{2,3}})do while J[1]<J[2]do v[J[1]],v[J[2]],J[1],J[2]=v[J[2]],v[J[1]],J[1]+1,J[2]-1 end end local function J(o)return v[o+45816]end do local o={["/"]=9;["8"]=48;["9"]=1;q=38,o=62;V=33;y=43,d=61,B=50,L=54;v=2;["0"]=21,n=31;p=63;R=5;N=3;i=10;e=35;C=7;l=56;a=47,J=58;m=59;["2"]=36;z=11;M=12;Z=26;O=18;["5"]=20;s=8,["4"]=30,P=55;w=4;U=29;Q=28;r=24,h=41;G=45;c=19;W=34,k=57;T=14,t=44,S=0;f=60;F=42,E=27;u=40;X=25,j=17;["3"]=23,b=13;["1"]=53;Y=32,A=22,K=6,["+"]=16,["6"]=46;["7"]=51;I=37;D=52;H=15,x=49,g=39}local J=type local x=string.sub local d=v local l=string.len local W=string.char local L=table.insert local w=table.concat local h=math.floor for v=1,#d,1 do local X=d[v]if J(X)=="string"then local J=l(X)local H={}local S=1 local k=0 local K=0 while S<=J do local v=x(X,S,S)local d=o[v]if d then k=k+d*64^(3-K)K=K+1 if K==4 then K=0 local o=h(k/65536)local v=h((k%65536)/256)local J=k%256 L(H,W(o,v,J))k=0 end elseif v=="="then L(H,W(h(k/65536)))if S>=J or x(X,S+1,S+1)~="="then L(H,W(h((k%65536)/256)))end break end S=S+1 end d[v]=w(H)end end end local function o(o)test[J(-45815)](o)end function init(v)print(J(-45813))o(J(-45814))end
```

### Criptografia de recursos
Durante o processo de build do Defold, os recursos do jogo são processados e transformados em formatos adequados para consumo em runtime pela engine Defold. Texturas são compiladas no formato Basis Universal, coleções, objetos de jogo e componentes são convertidos de uma representação textual legível por humanos para equivalentes binários, e o código-fonte Lua é processado e compilado em bytecode. Outros assets, como arquivos de som, são usados como estão.

Quando esse processo é concluído, os assets são adicionados ao arquivo do jogo, um por um. O arquivo do jogo é um arquivo binário grande, e a localização de cada recurso dentro dele é armazenada em um arquivo de índice do arquivo. O formato está documentado [aqui](https://github.com/defold/defold/blob/dev/engine/docs/ARCHIVE_FORMAT.md).

Antes que os arquivos-fonte Lua sejam adicionados ao arquivo, eles também podem ser criptografados opcionalmente. A criptografia padrão fornecida no Defold é uma cifra de bloco simples usada para impedir que strings no código fiquem imediatamente visíveis caso o arquivo do jogo seja inspecionado com uma ferramenta de visualização de arquivos binários. Ela não deve ser considerada criptograficamente segura, já que o código-fonte do Defold está disponível no GitHub com a chave da cifra visível no código-fonte.

É possível adicionar criptografia personalizada a arquivos-fonte Lua implementando um plugin de criptografia de recursos. Um plugin de criptografia de recursos consiste em uma parte em tempo de build, para criptografar recursos como parte do processo de build, e uma parte em runtime, para descriptografar recursos quando eles são lidos do arquivo do jogo. Um plugin básico de Resource Encryption, que pode ser usado como ponto de partida para sua própria criptografia, está [disponível no GitHub](https://github.com/defold/extension-resource-encryption).


### Codificando valores de configuração do projeto
O arquivo *game.project* será incluído como está no pacote da sua aplicação. Às vezes você pode querer armazenar chaves públicas de acesso a APIs ou valores semelhantes, que são sensíveis, mas talvez não privados. Para reforçar a segurança desses valores, eles podem ser incluídos no binário da aplicação em vez de armazenados em *game.project*, e ainda assim ficarem acessíveis a funções da API do Defold como `sys.get_config_string()` e funções semelhantes. Você pode fazer isso adicionando uma extensão nativa em seu *game.project* e usando a macro `DM_DECLARE_CONFIGFILE_EXTENSION` para fornecer suas próprias substituições para obter valores de configuração usando as funções da API do Defold. Um projeto de exemplo que pode ser usado como ponto de partida está [disponível no GitHub](https://github.com/defold/example-configfile-extension/tree/master).


## Protegendo seu jogo contra trapaceiros
Trapaças em videogames existem há tanto tempo quanto a própria indústria de jogos. Códigos de trapaça costumavam ser compartilhados em revistas populares de videogame, e cartuchos especiais de trapaça eram vendidos para os primeiros computadores domésticos. À medida que a indústria e os jogos evoluíram, também evoluíram os trapaceiros e seus métodos. Alguns dos mecanismos de trapaça mais populares em jogos são:

* Reempacotamento do conteúdo do jogo para injetar lógica personalizada
* Speed hacks para fazer um jogo rodar mais rápido ou mais devagar que o normal
* Automação e análise visual para mira automática e bots
* Injeção de código e memória para modificar pontuações, vidas, munição etc.

Proteger contra trapaceiros é difícil, beirando o impossível. Mesmo jogos na nuvem, nos quais os jogos rodam em servidores remotos e são transmitidos diretamente para o dispositivo de um usuário, não estão totalmente imunes a trapaceiros.

O Defold não fornece soluções anti-cheat na engine nem nas ferramentas e, em vez disso, deixa esse trabalho a cargo de uma das muitas empresas especializadas em fornecer soluções anti-cheat para jogos.


## Protegendo sua comunicação de rede
A comunicação por socket e HTTP do Defold oferece suporte a conexões de socket seguras. Recomenda-se usar conexões seguras em qualquer comunicação com servidor para autenticar o servidor e proteger a privacidade e a integridade de quaisquer dados trocados enquanto estão em trânsito do cliente para o servidor e vice-versa. O Defold usa a popular e amplamente adotada implementação de código aberto [Mbed TLS](https://github.com/Mbed-TLS/mbedtls) dos protocolos TLS e SSL. O Mbed TLS é desenvolvido pela ARM e por seus parceiros de tecnologia.

### Validação de certificado SSL
Para evitar ataques man-in-the-middle na sua comunicação de rede, é possível validar a cadeia de certificados durante o handshake SSL ao negociar uma conexão com um servidor. Isso pode ser feito fornecendo uma lista de chaves públicas ao cliente de rede no Defold. Para mais informações sobre como proteger sua comunicação de rede, leia a seção sobre verificação SSL no [manual de rede](https://defold.com/manuals/networking/#secure-connections).


## Protegendo seu uso de software de terceiros
Embora não seja necessário usar bibliotecas de terceiros nem extensões nativas para criar um jogo, tornou-se uma prática muito comum entre desenvolvedores usar assets do [Portal de Assets](https://defold.com/assets/) oficial para acelerar o desenvolvimento. O Portal de Assets contém uma grande seleção de assets, desde integrações com SDKs de terceiros até gerenciadores de telas, bibliotecas de UI, câmeras e muito mais.

Nenhum dos assets do Portal de Assets foi revisado pela Defold Foundation, e nós não nos responsabilizamos por qualquer dano ao seu sistema de computador ou outro dispositivo, nem por perda de dados resultante do uso de qualquer asset obtido pelo Portal de Assets. Você pode ler os detalhes nos nossos [Termos e Condições](https://defold.com/terms-and-conditions/#3-no-warranties).

Recomendamos que você revise qualquer asset antes de usá-lo e, depois de considerar que ele é adequado para uso no seu projeto, crie um fork ou uma cópia do asset para garantir que ele não mude sem que você perceba.


## Protegendo seu uso de servidores de build na nuvem
Os servidores de build na nuvem do Defold (também chamados de servidores Extender) foram criados para ajudar desenvolvedores a adicionar novas funcionalidades à engine Defold sem exigir uma recompilação da própria engine. Quando um projeto Defold contendo código nativo é compilado pela primeira vez, o código nativo e quaisquer recursos associados são enviados aos servidores de build na nuvem, onde uma versão personalizada da engine Defold é criada e enviada de volta ao desenvolvedor. O mesmo processo é aplicado quando um projeto é compilado usando um manifesto de aplicação personalizado para remover componentes não usados da engine.

Os servidores de build na nuvem são hospedados na AWS e criados de acordo com as melhores práticas de segurança. A Defold Foundation, no entanto, não garante que os servidores de build na nuvem atenderão aos seus requisitos, estarão livres de defeitos, vírus, problemas de segurança ou erros, nem que seu uso dos servidores será ininterrupto ou seguro. Você pode ler os detalhes nos nossos [Termos e Condições](https://defold.com/terms-and-conditions/#3-no-warranties).

Se a segurança e a disponibilidade dos servidores de build forem uma preocupação para você, recomendamos configurar seus próprios servidores de build privados. Instruções sobre como configurar seu próprio servidor podem ser encontradas no [arquivo readme principal](https://github.com/defold/extender) do repositório Extender no GitHub.


## Protegendo seu conteúdo baixável
O sistema Live Update do Defold permite que desenvolvedores excluam conteúdo do pacote principal do jogo para baixá-lo e usá-lo mais tarde. Um caso de uso típico é baixar fases, mapas ou mundos adicionais conforme o jogador avança pelo jogo.

Quando o conteúdo excluído é baixado e preparado para uso em um jogo, ele é verificado criptograficamente pela engine antes do uso para garantir que não tenha sido adulterado. A verificação consiste em várias checagens:

* O formato binário está correto?
* O conteúdo baixado é compatível com a versão da engine que está em execução?
* O conteúdo baixado está assinado com o par correto de chaves pública e privada?
* O conteúdo baixado está completo e sem arquivos ausentes?

Você pode ler mais sobre esse processo no [manual do Live Update](https://defold.com/manuals/live-update/#manifest-verification).
