---
title: O design do Defold
brief: A filosofia por trás do design do Defold
---

# O design do Defold

O Defold foi criado com os seguintes objetivos:

- Ser uma plataforma profissional completa e pronta para produção para equipes de jogos.
- Ser simples e claro, oferecendo soluções explícitas para problemas comuns de arquitetura e fluxo de trabalho no desenvolvimento de jogos.
- Ser uma plataforma de desenvolvimento extremamente rápida, ideal para o desenvolvimento iterativo de jogos.
- Ter alto desempenho em tempo de execução.
- Ser verdadeiramente multiplataforma.

O design do editor e da engine foi cuidadosamente criado para atingir esses objetivos. Algumas das nossas decisões de design são diferentes do que você talvez conheça de outras plataformas, por exemplo:

- Exigimos a declaração estática da árvore de recursos e de todos os nomes. Isso exige algum esforço inicial, mas ajuda muito o processo de desenvolvimento no longo prazo.
- Incentivamos a passagem de mensagens entre entidades simples e encapsuladas.
- Não há herança por orientação a objetos.
- Nossas APIs são assíncronas.
- O pipeline de renderização é controlado por código e totalmente personalizável.
- Todos os nossos arquivos de recursos usam formatos simples de texto puro, estruturados de forma ideal para merges no Git e também para importação e processamento com ferramentas externas.
- Os recursos podem ser alterados e carregados por hot reload em um jogo em execução, permitindo iteração e experimentação extremamente rápidas.
