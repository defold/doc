---
title: Nodes GUI do tipo box no Defold
brief: Este manual explica como usar nodes GUI do tipo box.
---

# Nodes GUI do tipo box

Um node do tipo box é um retângulo preenchido com uma cor, textura ou animação.

## Adicionando nodes box

Adicione novos nodes box clicando com o botão direito no *Outline* e selecionando <kbd>Add ▸ Box</kbd>, ou pressione <kbd>A</kbd> e selecione <kbd>Box</kbd>.

Você pode usar imagens e animações de atlas ou tile sources que foram adicionados à GUI. Você adiciona texturas clicando com o botão direito no ícone da pasta *Textures* no *Outline* e selecionando <kbd>Add ▸ Textures...</kbd>. Em seguida, defina a propriedade *Texture* no node box:

![Texturas](images/gui-box/create.png)

Observe que a cor do node box tingirá os gráficos. A cor de tint é multiplicada nos dados da imagem, o que significa que, se você definir a cor como branca (o padrão), nenhum tint será aplicado.

![Textura tingida](images/gui-box/tinted.png)

Nodes box são sempre renderizados, mesmo que não tenham uma textura atribuída, tenham alpha definido como `0` ou tenham tamanho `0, 0, 0`. Nodes box devem sempre ter uma textura atribuída para que o renderizador consiga agrupá-los corretamente e reduzir o número de draw calls.

## Reproduzindo animações

Nodes box podem reproduzir animações de atlas ou tile sources. Consulte o [manual de animação flipbook](/manuals/flipbook-animation) para saber mais.

:[Slice-9](../shared/slice-9-texturing.md)
