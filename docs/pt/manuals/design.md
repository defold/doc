---
title: The design of Defold
brief: The philosophy behind Defold's design
---
# The design of Defold

 Deflod foi criado para os seguintes objetivos:

 - Para ser uma plataforma profissional completa e facil, para equipes de jogos.

 - Para ser simples e intuitiva ,fornecendo  explícitas  soluções, para problemas comuns de arquitetura é  fluxo de trabalho no desenvolvimento de jogos.

 - Para ser uam plataforma ideal e extemamente rápida no desenvolvimento iterativo de jogos.

 - Para ter um alto desempenho no tempo de execução.

 - Sendo realmente  uma multiplataforma

  O design do editor e do mecanismo é cuidadosamente criado para atingir os objetivos.Algumas de nossas decisões de design diferem  das  experiência em outras plataformas que você já está 
  acostumado, pelos exemplos:

 - Nos exigimos estática declaração da   árvore  de recusoso e todos os nomes. Com isso requer algum  esforço inicial
 do usuario , mas ajuda muito o processo de desenvolvimento ao longo prazo. 
 
 - Nos encorajamos a simples troca de mensagens entre entidades encapsuladas.

 -Não há herança de orientação de objeto.

 - Nossas APIS são assíncronas.

 - A renderização do pipelibe  é orientado por código e é totalmente personalizável.  
 
 - Todos os recursos de nossos arquivos estão em formatos de texto simples sendo estruturados de forma otimizada para  Git , como importação e processamento com ferramentas externas. 
 
 - Recursos podem ser alterados e recarregados na execução de um jogo , permitindo extremamente rápidas a iteração e experimentação . 
