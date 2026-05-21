---
title: Objetos de colisão no Defold
brief: Um objeto de colisão é um componente usado para dar comportamento físico a um objeto de jogo. Um objeto de colisão tem propriedades físicas e uma forma espacial.
---

# Objetos de colisão

Um objeto de colisão é um componente usado para dar comportamento físico a um objeto de jogo. Um objeto de colisão tem propriedades físicas como peso, restituição e atrito, e sua extensão espacial é definida por uma ou mais _formas_ que você anexa ao componente. O Defold suporta os seguintes tipos de objetos de colisão:

Objetos estáticos
: Objetos estáticos nunca se movem, mas um objeto dinâmico que colide com um objeto estático reagirá quicando e/ou deslizando. Objetos estáticos são muito úteis para criar geometria de fase (isto é, chão e paredes) que não se move. Eles também são mais baratos em termos de desempenho do que objetos dinâmicos. Você não pode mover nem alterar objetos estáticos.

Objetos dinâmicos
: Objetos dinâmicos são simulados pela engine de física. A engine resolve todas as colisões e aplica as forças resultantes. Objetos dinâmicos são bons para objetos que devem se comportar de forma realista. A forma mais comum de afetá-los é indiretamente, [aplicando forças](/ref/physics/#apply_force) ou alterando o [amortecimento](/ref/stable/physics/#angular_damping) e a [velocidade](/ref/stable/physics/#linear_velocity) angular, além do [amortecimento](/ref/stable/physics/#linear_damping) e da [velocidade](/ref/stable/physics/#angular_velocity) linear. Também é possível manipular diretamente a posição e a orientação de um objeto dinâmico quando a [configuração Allow Dynamic Transforms](/manuals/project-settings/#allow-dynamic-transforms) está habilitada em *game.project*.

Objetos cinemáticos
: Objetos cinemáticos registram colisões com outros objetos de física, mas a engine de física não executa nenhuma simulação automática. O trabalho de resolver colisões, ou ignorá-las, fica por sua conta ([saiba mais](/manuals/physics-resolving-collisions)). Objetos cinemáticos são muito bons para objetos controlados pelo jogador ou por script que exigem controle fino das reações físicas, como um personagem do jogador.

Gatilhos
: Gatilhos são objetos que registram colisões simples. Gatilhos são objetos de colisão leves. Eles são semelhantes a [ray casts](/manuals/physics-ray-casts), no sentido de que leem o mundo de física em vez de interagir com ele. Eles são bons para objetos que só precisam registrar um acerto (como uma bala) ou como parte da lógica do jogo quando você quer disparar determinadas ações quando um objeto atinge um ponto específico. Gatilhos são computacionalmente mais baratos do que objetos cinemáticos e devem ser usados no lugar deles quando possível.


## Adicionando um componente de objeto de colisão

Um componente de objeto de colisão tem um conjunto de *Properties* que define seu tipo e propriedades físicas. Ele também contém uma ou mais *Shapes* que definem a forma completa do objeto de física.

Para adicionar um componente de objeto de colisão a um objeto de jogo:

1. Na visualização *Outline*, clique com o botão direito no objeto de jogo e selecione <kbd>Add Component ▸ Collision Object</kbd> no menu de contexto. Isso cria um novo componente sem formas.
2. Clique com o botão direito no novo componente e selecione <kbd>Add Shape ▸ Box / Capsule / Sphere</kbd>. Isso adiciona uma nova forma ao componente de objeto de colisão. Você pode adicionar qualquer número de formas ao componente. Também pode usar um tilemap ou um casco convexo para definir a forma do objeto de física.
3. Use as ferramentas de mover, rotacionar e escalar para editar as formas.
4. Selecione o componente no *Outline* e edite as *Properties* do objeto de colisão.

![Physics collision object](images/physics/collision_object.png)


## Adicionando uma forma de colisão

Um componente de colisão pode usar várias formas primitivas ou uma única forma complexa. Saiba mais sobre as várias formas e como adicioná-las a um componente de colisão no [manual de Formas de Colisão](/manuals/physics-shapes).


## Propriedades do objeto de colisão

Id
: A identidade do componente.

Collision Shape
: Esta propriedade é usada para geometria de tile map ou formas convexas que não usam formas primitivas. Veja [Formas de Colisão para mais informações](/manuals/physics-shapes).

Type
: O tipo de objeto de colisão: `Dynamic`, `Kinematic`, `Static` ou `Trigger`. Se você definir o objeto como dinâmico, _deve_ definir a propriedade *Mass* para um valor diferente de zero. Para objetos dinâmicos ou estáticos, você também deve verificar se os valores de *Friction* e *Restitution* são adequados ao seu caso de uso.

Friction
: Atrito torna possível que objetos deslizem realisticamente uns contra os outros. O valor de atrito normalmente fica entre `0` (sem atrito algum, um objeto muito escorregadio) e `1` (atrito forte, um objeto abrasivo). No entanto, qualquer valor positivo é válido.

  A força de atrito é proporcional à força normal (isso é chamado de atrito de Coulomb). Quando a força de atrito é calculada entre duas formas (`A` e `B`), os valores de atrito de ambos os objetos são combinados pela média geométrica:

```math
F = sqrt( F_A * F_B )
```

  Isso significa que, se um dos objetos tiver atrito zero, o contato entre eles terá atrito zero.

Restitution
: O valor de restituição define o "quique" do objeto. O valor normalmente fica entre 0 (colisão inelástica, o objeto não quica) e 1 (colisão perfeitamente elástica, a velocidade do objeto será refletida exatamente no quique)

  Valores de restituição entre duas formas (`A` e `B`) são combinados usando a seguinte fórmula:

```math
R = max( R_A, R_B )
```

  Quando uma forma desenvolve múltiplos contatos, a restituição é simulada aproximadamente porque o Box2D usa um solver iterativo. O Box2D também usa colisões inelásticas quando a velocidade de colisão é pequena para evitar tremulação de quique.

Linear damping
: O amortecimento linear reduz a velocidade linear do corpo. Ele é diferente do atrito, que só ocorre durante o contato, e pode ser usado para dar aos objetos uma aparência flutuante, como se estivessem se movendo por algo mais espesso que o ar. Valores válidos ficam entre 0 e 1.

  O Box2D aproxima o amortecimento para estabilidade e desempenho. Em valores pequenos, o efeito de amortecimento é independente do passo de tempo; em valores maiores de amortecimento, o efeito varia com o passo de tempo. Se você executar seu jogo com um passo de tempo fixo, isso nunca se torna um problema.

Angular damping
: O amortecimento angular funciona como o amortecimento linear, mas reduz a velocidade angular do corpo. Valores válidos ficam entre 0 e 1.

Locked rotation
: Definir esta propriedade desabilita totalmente a rotação no objeto de colisão, independentemente das forças aplicadas a ele.

Bullet
: Definir esta propriedade habilita detecção contínua de colisão (CCD) entre o objeto de colisão e outros objetos de colisão dinâmicos. A propriedade Bullet é ignorada se Type não estiver definido como `Dynamic`.

Group
: O nome do grupo de colisão ao qual o objeto deve pertencer. Você pode ter 16 grupos diferentes e nomeá-los como achar adequado para o seu jogo. Por exemplo, "players", "bullets", "enemies" e "world". Se *Collision Shape* estiver definido como um tile map, este campo não é usado; os nomes dos grupos são obtidos do tile source. [Saiba mais sobre grupos de colisão](/manuals/physics-groups).

Mask
: Os outros _grupos_ com os quais este objeto deve colidir. Você pode nomear um grupo ou especificar vários grupos em uma lista separada por vírgulas. Se deixar o campo Mask vazio, o objeto não colidirá com nada. [Saiba mais sobre grupos de colisão](/manuals/physics-groups).

Generate Collision Events
: Se habilitado, permitirá que este objeto envie eventos de colisão

Generate Contact Events
: Se habilitado, permitirá que este objeto envie eventos de contato

Generate Trigger Events
: Se habilitado, permitirá que este objeto envie eventos de gatilho


## Propriedades em tempo de execução

Um objeto de física tem várias propriedades diferentes que podem ser lidas e alteradas usando `go.get()` e `go.set()`:

`angular_damping`
: O valor de amortecimento angular do componente de objeto de colisão (`number`). [Referência da API](/ref/physics/#angular_damping).

`angular_velocity`
: A velocidade angular atual do componente de objeto de colisão (`vector3`). [Referência da API](/ref/physics/#angular_velocity).

`linear_damping`
: O valor de amortecimento linear do objeto de colisão (`number`). [Referência da API](/ref/physics/#linear_damping).

`linear_velocity`
: A velocidade linear atual do componente de objeto de colisão (`vector3`). [Referência da API](/ref/physics/#linear_velocity).

`mass`
: A massa física definida do componente de objeto de colisão. SOMENTE LEITURA. (`number`). [Referência da API](/ref/physics/#mass).
