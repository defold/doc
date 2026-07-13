---
title: Física no Defold
brief: O Defold inclui engines de física para 2D e 3D. Elas permitem simular interações de física newtoniana entre diferentes tipos de objetos de colisão.
---

# Física

O Defold inclui o [Box2D](https://box2d.org/) para simulações de física 2D e o Bullet para física 3D. A [configuração Physics 2D do Manifesto do aplicativo](/manuals/app-manifest/#physics-2d) seleciona **Box2D Version 3**, **Box2D (Legacy Defold version)** ou **None**. A implementação legada é o padrão; o Box2D 3 é opt-in. Mudar de implementação pode alterar os resultados da simulação e exigir que você reajuste as [configurações de projeto do Box2D](/manuals/project-settings/#box2d), que são específicas de cada versão.

O fluxo de trabalho de objetos de colisão orientado a componentes e o módulo `physics` descritos nestes manuais funcionam com ambas as implementações do Box2D; selecionar **None** remove a física 2D. O Defold também expõe as APIs de nível mais baixo [`b2d`](/ref/stable/b2d/), `b2d.body`, `b2d.fixture`, `b2d.shape`, `b2d.joint`, `b2d.chain` e `b2d.world` para acesso direto a corpos, formas, joints, chains e worlds 2D. Nem todas as funções de nível mais baixo estão disponíveis em ambas as implementações do Box2D; confira a documentação de API gerada para cada função em relação à implementação selecionada no Manifesto do aplicativo.

Os principais conceitos das engines de física usadas no Defold são:

* **Objetos de colisão** - Um objeto de colisão é um componente usado para dar comportamento físico a um objeto de jogo. Um objeto de colisão tem propriedades físicas como peso, atrito e forma. [Aprenda como criar um objeto de colisão](/manuals/physics-objects).
* **Formas de colisão** - Um objeto de colisão pode usar várias formas primitivas ou uma única forma complexa para definir sua extensão espacial. [Aprenda como adicionar formas a um objeto de colisão](/manuals/physics-shapes).
* **Grupos de colisão** - Todos os objetos de colisão devem pertencer a um grupo predefinido, e cada objeto de colisão pode especificar uma lista de outros grupos com os quais pode colidir. [Aprenda como usar grupos de colisão](/manuals/physics-groups).
* **Mensagens de colisão** - Quando dois objetos de colisão colidem, a engine de física envia mensagens aos objetos de jogo aos quais os componentes pertencem. [Saiba mais sobre mensagens de colisão](/manuals/physics-messages)

Além dos próprios objetos de colisão, você também pode definir **restrições** de objetos de colisão, mais comumente conhecidas como **joints**, para conectar dois objetos de colisão e limitar, ou de outras formas aplicar força e influenciar como eles se comportam na simulação de física. [Saiba mais sobre joints](/manuals/physics-joints).

Você também pode sondar e ler o mundo de física ao longo de um raio linear conhecido como **ray cast**. [Saiba mais sobre ray casts](/manuals/physics-ray-casts).


## Unidades usadas pela simulação da engine de física

A engine de física simula física newtoniana e foi projetada para funcionar bem com unidades de metros, quilogramas e segundos (MKS). Além disso, a engine de física é ajustada para funcionar bem com objetos móveis de tamanho na faixa de 0,1 a 10 metros (objetos estáticos podem ser maiores) e, por padrão, a engine trata 1 unidade (pixel) como 1 metro. Essa conversão entre pixels e metros é conveniente em nível de simulação, mas do ponto de vista de criação de jogos não é muito útil. Com as configurações padrão, uma forma de colisão com tamanho de 200 pixels seria tratada como tendo 200 metros, o que está muito fora da faixa recomendada, pelo menos para um objeto móvel.

Em geral, é necessário escalar a simulação de física para que ela funcione bem com o tamanho típico dos objetos em um jogo. A escala da simulação de física pode ser alterada em *game.project* pela [configuração physics scale](/manuals/project-settings/#physics). Definir esse valor como, por exemplo, 0.02 significaria que 200 pixels seriam tratados como 4 metros. Observe que a gravidade (também alterada em *game.project*) precisa ser aumentada para acomodar a mudança de escala.


## Atualizações de física {#physics-updates}

É recomendado atualizar a engine de física em intervalos regulares para garantir uma simulação estável (em vez de atualizar em intervalos possivelmente irregulares dependentes da taxa de quadros). Você pode usar uma atualização fixa para física marcando a [configuração Use Fixed Timestep](/manuals/project-settings/#physics) da seção Physics no arquivo *game.project*. A frequência de atualização é controlada pela [configuração Fixed Update Frequency](/manuals/project-settings/#engine) da seção Engine no arquivo *game.project*. Ao usar um timestep fixo para física, também é recomendado usar a função de ciclo de vida `fixed_update(self, dt)` para interagir com os objetos de colisão do seu jogo, por exemplo ao aplicar forças a eles.


## Ressalvas e problemas comuns

Proxies de coleção
: Por meio de proxies de coleção, é possível carregar mais de uma coleção de nível superior, ou *mundo de jogo*, na engine. Ao fazer isso, é importante saber que cada coleção de nível superior é um mundo físico separado. Interações de física ([colisões, gatilhos](/manuals/physics-messages) e [ray-casts](/manuals/physics-ray-casts)) só acontecem entre objetos pertencentes ao mesmo mundo. Portanto, mesmo que os objetos de colisão de dois mundos estejam visualmente exatamente sobrepostos, não pode haver interação de física entre eles.

Colisões não detectadas
: Se você tiver problemas com colisões que não são tratadas ou detectadas corretamente, leia sobre [depuração de física no manual de Depuração](/manuals/debugging-game-logic/#debugging-problems-with-physics).
