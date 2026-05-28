---
title: Cache de assets
brief: Este manual explica como usar o cache de assets para acelerar builds.
---

# Cache de assets

Jogos criados com o Defold geralmente são compilados em questão de segundos, mas a quantidade de assets cresce junto com o projeto. Compilar fontes e comprimir texturas pode levar bastante tempo em um projeto grande, e o cache de assets existe para acelerar builds recompilando apenas os assets que mudaram e reutilizando do cache os assets já compilados que não mudaram.

O Defold usa um cache em três camadas:

1. Cache do projeto
2. Cache local
3. Cache remoto


## Cache do projeto

Por padrão, o Defold armazena assets compilados na pasta `build/default` de um projeto Defold. O cache do projeto acelera builds subsequentes, já que somente assets modificados precisam ser recompilados, enquanto assets sem alterações são usados a partir do cache do projeto. Esse cache está sempre ativado e é usado tanto pelo editor quanto pelas ferramentas de linha de comando.

O cache do projeto pode ser excluído manualmente apagando os arquivos em `build/default` ou executando o comando `clean` da [ferramenta de build de linha de comando Bob](/manuals/bob).


## Cache local

O cache local é um segundo cache opcional em que assets compilados são armazenados em um local externo no mesmo computador ou em uma unidade de rede. Por ficar fora do projeto, o conteúdo do cache sobrevive à limpeza do cache do projeto. Ele também pode ser compartilhado por vários desenvolvedores trabalhando no mesmo projeto. No momento, o cache está disponível apenas ao compilar usando as ferramentas de linha de comando. Ele é ativado pela opção `resource-cache-local`:

```sh
java -jar bob.jar --resource-cache-local /Users/john.doe/defold_local_cache
```

Assets compilados são acessados do cache local com base em um checksum calculado que leva em conta a versão da engine Defold, os nomes e conteúdos dos assets de origem, bem como as opções de build do projeto. Isso garante que os assets em cache sejam únicos e que o cache possa ser compartilhado entre várias versões do Defold.

::: sidenote
Arquivos armazenados no cache local são mantidos indefinidamente. Cabe ao desenvolvedor remover manualmente arquivos antigos ou sem uso.
:::


## Cache remoto

O cache remoto é um terceiro cache opcional em que assets compilados são armazenados em um servidor e acessados por requisições HTTP. No momento, o cache está disponível apenas ao compilar usando as ferramentas de linha de comando. Ele é ativado pela opção `resource-cache-remote`:

```sh
java -jar bob.jar --resource-cache-remote http://192.168.0.100/
```

Assim como no cache local, todos os assets são acessados do cache remoto com base em um checksum calculado. Assets em cache são acessados pelos métodos de requisição HTTP GET, PUT e HEAD. O Defold não fornece o servidor de cache remoto. Cabe a cada desenvolvedor configurar esse servidor. Um exemplo de [servidor básico em Python pode ser visto aqui](https://github.com/britzl/httpserver-python).
