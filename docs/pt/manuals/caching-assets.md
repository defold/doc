---
title: Caching de recursos
brief: Esse manual irá explicar como utilizar o cache de recursos para acelerar suas builds.
---

# Caching de recursos

Jogos criados com Defold geralmente são contruindos em questão de segundos, mas com o crescimento de um projeto também há um crescimento no numero de recursos(assets). Compilando fontes e comprimindo texturas pode demorar em um grande projeto, assim existe o cache de recurso ou(asset cache), que serve para acelerar as builds somente recosntruindo recursos que foram alterados enquanto recursos ja compilados estavão sendo utilizados do cache para recursos que não foram mudados. 

O Defold utiliza um cache de três camadas

1. Projeto de cache
2. Cache Local
3. Cache Remoto


## Projeto de cache

O Defold por padrão ira dar cache nos recursos já compilados na pasta `build/default` de um projeto Defold. O projeto cache vai acelerar builds subsequentes sendo que elas so modifica recursos que precisam ser re-compilados, enquanto recursos sem mudanças serão usados do cache do projeto. Esse cache sempre está ativado e é utilizado tanto pelo editor como pelas ferramentas da linha de comando.

O projeto de cache pode ser deletado manualmente simplesmente deletandos os arquivos em `build/default` ou insinuando o comando `clean` da [Ferramenta de construção da linha de comando Bob](/manuals/bob).


## Cache Local

Adicionado no Defold 1.2.187

O cache local é um cache secundário opcional onde recursos compilados estarão guardados em uma localização externa de arquivos na mesma maquina ou em um network drive. Graças ao seu local externo os conteudos do cache sobrevivem a limpeza do cache do projeto. Ele pode ser compartilhado por multiplos desenvolvedores trabalhando no mesmo projeto. O cache é atualmente so está disponivel quando construindo a partir das ferramentas da linha de comando. Ele é ativado pela opção `resource-cache-local`:

```sh
java -jar bob.jar --resource-cache-local /Users/john.doe/defold_local_cache
```

Recursos compilados são acessados do cache local baseado em um chcksum computado que leva em conta a versão da engine Defold, o nome e os conteudos dos recursos fonte assim como as opções de construção. Isso irá garantir que os recursos em cache sejam únicos e que o cache possa ser compartilhado entre multiplas versões do Defold.

::: sidenote
Arquivos guardados no cache local são armazenados de forma indefinida. Está sob comando do desenvolvedor a ação de remover arquivos antigos/sem-uso.
:::


## Cache Remoto

Adicionado no Defold 1.2.187

O cache remoto é uma opção terciária de cache em que recursos compilados são armazenados em um servidor que é acessado via requisições HTTP. O cache é atualmente somente disponível quando construindo a partir das ferramentas da linha de comando. Isso pode ser ativado a partir da opção `resource-cache-remote`:

```sh
java -jar bob.jar --resource-cache-remote http://192.168.0.100/
```

Assim como o cache local todos os recursos são acessados de um cache remoto baseado em um checksum computado. Recursos em cache são acessados por uma requisição HTTP pelos metodos GET, PUT e HEAD. Defold não provê o servidor de cache remoto. Cada desenvolvedor está responsavel por settar esse recurso. Um exemplo de [um servidor básico em Python pode ser visto aqui](https://github.com/britzl/httpserver-python).
