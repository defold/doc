---
title: Como obter ajuda
brief: Este manual descreve como obter ajuda se você encontrar um problema ao usar o Defold.
---

# Obtendo ajuda {#getting-help}

Se você encontrar um problema ao usar o Defold, queremos saber para que possamos corrigir a questão e/ou ajudar você a contornar o problema. Há várias formas de discutir e também relatar problemas. Escolha a opção que funciona melhor para você:

## Relatar um problema no fórum

Uma boa forma de discutir e obter ajuda com um problema é publicar uma pergunta no nosso [fórum](https://forum.defold.com). Publique na categoria [Questions](https://forum.defold.com/c/questions) ou [Bugs](https://forum.defold.com/c/bugs), dependendo do tipo de problema. Lembre-se de [buscar](https://forum.defold.com/search) sua pergunta/problema antes de perguntar, pois talvez já exista uma solução.

Se você tiver várias perguntas, crie várias publicações. Não faça perguntas sem relação entre si na mesma publicação.

### Informações necessárias
Não poderemos oferecer suporte a menos que você forneça as informações necessárias:

**Título**
Use um título curto e descritivo. Um bom título seria "Como movo um objeto de jogo na direção em que ele está rotacionado?" ou "Como faço um sprite desaparecer gradualmente?". Um título ruim seria "Preciso de ajuda para usar o Defold!" ou "Meu jogo não está funcionando!".

**Descreva o bug (OBRIGATÓRIO)**
Uma descrição clara e concisa do bug.

**Como reproduzir (OBRIGATÓRIO)**
Passos para reproduzir o comportamento:
1. Vá para '...'
2. Clique em '....'
3. Role para baixo até '....'
4. Veja o erro

**Comportamento esperado (OBRIGATÓRIO)**
Uma descrição clara e concisa do que você esperava que acontecesse.

**Versão do Defold (OBRIGATÓRIO):**
  - Versão [por exemplo, 1.2.155]

**Plataformas (OBRIGATÓRIO):**
 - Plataformas: [por exemplo, iOS, Android, Windows, macOS, Linux, HTML5]
 - SO: [por exemplo, iOS8.1, Windows 10, High Sierra]
 - Dispositivo: [por exemplo, iPhone6]

**Projeto mínimo de reprodução (OPCIONAL):**
Anexe um projeto mínimo em que o bug seja reproduzido. Isso ajudará muito a pessoa que tentará investigar e corrigir o bug.

**Logs (OPCIONAL):**
Forneça logs relevantes da engine, do editor ou do servidor de build. Saiba onde os logs são armazenados [aqui](#log-files).

**Solução alternativa (OPCIONAL):**
Se houver uma solução alternativa, descreva-a aqui.

**Capturas de tela (OPCIONAL):**
Se aplicável, adicione capturas de tela para ajudar a explicar o problema.

**Contexto adicional (OPCIONAL):**
Adicione aqui qualquer outro contexto sobre o problema.


### Compartilhando código
Ao compartilhar código, recomenda-se compartilhá-lo como texto, não como capturas de tela. Compartilhar como texto facilita buscar, destacar erros, sugerir e fazer modificações. Compartilhe código envolvendo-o em três \`\`\` ou recuando com 4 espaços.

Exemplo:

\`\`\`
print("Hello code!")
\`\`\`

Resultado:

```
print("Hello code!")
```


## Relatar um problema pelo editor {#report-a-problem-from-the-editor}

O editor oferece uma forma conveniente de relatar problemas. Selecione a opção de menu <kbd>Help->Report Issue</kbd> dentro do editor para relatar um problema.

![](images/getting_help/report_issue.png)

Selecionar essa opção de menu levará você a um rastreador de issues no GitHub. Forneça [arquivos de log](#log-files), informações sobre seu sistema operacional, passos para reproduzir o problema, possíveis soluções alternativas etc.

::: sidenote
Você precisa de uma conta do GitHub para enviar um relatório de bug dessa forma.
:::


## Discutir um problema no Discord

Se você encontrar um problema ao usar o Defold, pode tentar fazer a pergunta no [Discord](https://www.defold.com/discord/). No entanto, recomendamos que perguntas complexas e discussões aprofundadas sejam publicadas no fórum. Observe também que não aceitamos relatórios de bug enviados pelo Discord.


# Arquivos de log {#log-files}

A engine, o editor e o servidor de build geram informações de log que podem ser muito valiosas ao pedir ajuda e depurar um problema. Sempre forneça arquivos de log ao relatar um problema:

* [Logs da engine](/manuals/debugging-game-and-system-logs)
* [Logs do editor](/manuals/editor#editor-logs)
* [Logs do servidor de build](/manuals/extensions#build-server-logs)
