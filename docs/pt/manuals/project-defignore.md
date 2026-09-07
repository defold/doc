---
title: Arquivos ignorados em projetos Defold
brief: Este manual descreve como ignorar arquivos e pastas no Defold.
---

# Ignorando arquivos

É possível configurar o editor Defold e as ferramentas para ignorar arquivos e pastas em um projeto. Isso pode ser útil se o projeto contiver arquivos com extensões que entram em conflito com extensões usadas pelo Defold. Um exemplo são arquivos da linguagem Go com a extensão `.go`, que é a mesma que o editor usa para arquivos de objeto de jogo.

## O arquivo `.defignore`
Os arquivos e pastas a excluir são definidos em um arquivo chamado `.defignore` na raiz do projeto. O arquivo deve listar arquivos e pastas a excluir, um por linha. Exemplo:

```
/path/to/file.png
/otherpath
```

Isso excluirá o arquivo `/path/to/file.png` e qualquer coisa no caminho `/otherpath`.
Cada linha deve começar com `/` e é comparada com os caminhos do projeto relativos à raiz do projeto. Um padrão corresponde a um caminho se for igual a ele ou se for uma de suas pastas superiores. A comparação diferencia maiúsculas de minúsculas.

### Curingas

Os padrões podem conter curingas:

* `*` corresponde a qualquer número de caracteres, exceto `/`
* `?` corresponde a exatamente um caractere, exceto `/`
* `**` corresponde a qualquer número de caracteres, incluindo `/`

Todos os outros caracteres são comparados literalmente. Exemplo:

```
/levels/*/tiled
/**/generated
/assets/temp_??.png
```

Isso excluirá a pasta `tiled` em cada subpasta direta de `/levels` (como `/levels/01/tiled`), todas as pastas chamadas `generated` dentro de qualquer subpasta e arquivos como `/assets/temp_01.png`.

Observe que `**` não corresponde às barras ao seu redor, portanto `/levels/**` corresponde a tudo dentro de `/levels`, mas não à própria pasta `/levels`, e `/**/generated` não corresponde a `/generated` na raiz do projeto.

## O arquivo `.defunload`

Para certos projetos grandes que contêm vários módulos independentes, talvez você queira excluir partes dele do carregamento para reduzir o uso de memória e os tempos de carregamento no editor. Para isso, você pode listar caminhos a excluir do carregamento em um arquivo `.defunload` abaixo do diretório do projeto.

Simplificando, o arquivo `.defunload` permite ocultar partes do projeto do editor sem transformar referências aos recursos ocultos em erro de build.

Os padrões em `.defunload` usam as mesmas regras do arquivo `.defignore`. Collections e Game Objects descarregados se comportarão como se estivessem vazios quando referenciados por recursos carregados. Outros recursos que correspondem aos padrões de `.defunload` ficarão em estado descarregado e não poderão ser visualizados no editor. No entanto, se um recurso carregado depender deles, os recursos descarregados e suas dependências serão carregados automaticamente.

Por exemplo, se um Sprite depende de imagens em um Atlas, precisamos carregar o Atlas, ou a imagem ausente será relatada como erro. Se isso acontecer, uma notificação avisará o usuário sobre a situação e fornecerá informações sobre qual recurso descarregado foi referenciado e de onde.

O editor impedirá que o usuário adicione referências a recursos `.defunloaded` a partir de recursos carregados, então essa situação só ocorre quando recursos são lidos do disco.

Ao contrário do arquivo `.defignore`, você precisa reiniciar o editor depois de editar o arquivo `.defunload` para ver as alterações entrarem em vigor.
