---
title: Joints de física no Defold
brief: O Defold suporta joints para física 2D. Este manual explica como criar e trabalhar com joints.
---

# Joints

O Defold suporta joints para física 2D. Um joint conecta dois objetos de colisão usando algum tipo de restrição. Os tipos de joint suportados são:

* **Fixed (physics.JOINT_TYPE_FIXED)** - Um rope joint que restringe a distância máxima entre dois pontos. No Box2D, é chamado de Rope joint.
* **Hinge (physics.JOINT_TYPE_HINGE)** - Um hinge joint especifica um ponto de âncora em dois objetos de colisão e os move para que os dois objetos de colisão estejam sempre no mesmo lugar, sem restringir a rotação relativa dos objetos de colisão. O hinge joint pode habilitar um motor com torque máximo e velocidade definidos. No Box2D, é chamado de [Revolute joint](https://box2d.org/documentation/group__revolute__joint.html#details).
* **Weld (physics.JOINT_TYPE_WELD)** - Um weld joint tenta restringir todo movimento relativo entre dois objetos de colisão. O weld joint pode ser suavizado como uma mola, com frequência e fator de amortecimento. No Box2D, é chamado de [Weld joint](https://box2d.org/documentation/group__weld__joint.html#details).
* **Spring (physics.JOINT_TYPE_SPRING)** - Um spring joint mantém dois objetos de colisão a uma distância constante um do outro. O spring joint pode ser suavizado como uma mola, com frequência e fator de amortecimento. No Box2D, é chamado de [Distance joint](https://box2d.org/documentation/group__distance__joint.html#details).
* **Slider (physics.JOINT_TYPE_SLIDER)** - Um slider joint permite a translação relativa de dois objetos de colisão ao longo de um eixo especificado e impede rotação relativa. No Box2D, é chamado de [Prismatic joint](https://box2d.org/documentation/group__prismatic__joint.html#details).
* **Wheel (physics.JOINT_TYPE_WHEEL)** - Um wheel joint restringe um ponto em `bodyB` a uma linha em `bodyA`. O wheel joint também fornece uma mola de suspensão. No Box2D, é chamado de [Wheel joint](https://box2d.org/documentation/group__wheel__joint.html#details).

## Criando joints

Atualmente, joints só podem ser criados programaticamente usando [`physics.create_joint()`](/ref/physics/#physics.create_joint:joint_type-collisionobject_a-joint_id-position_a-collisionobject_b-position_b-[properties]):
::: sidenote
Suporte do editor para criar joints está planejado, mas nenhuma data de lançamento foi definida.
:::

```lua
-- conecta dois objetos de colisão com uma restrição de joint fixo (rope)
physics.create_joint(physics.JOINT_TYPE_FIXED, "obj_a#collisionobject", "my_test_joint", vmath.vector3(10, 0, 0), "obj_b#collisionobject", vmath.vector3(0, 20, 0), { max_length = 20 })
```

O código acima criará um fixed joint com id `my_test_joint` conectado entre os dois objetos de colisão `obj_a#collisionobject` e `obj_b#collisionobject`. O joint é conectado 10 pixels à esquerda do centro do objeto de colisão `obj_a#collisionobject` e 20 pixels acima do centro do objeto de colisão `obj_b#collisionobject`. O comprimento máximo do joint é de 20 pixels.

## Destruindo joints

Um joint pode ser destruído usando [`physics.destroy_joint()`](/ref/physics/#physics.destroy_joint:collisionobject-joint_id):

```lua
-- destrói um joint previamente conectado ao primeiro objeto de colisão
physics.destroy_joint("obj_a#collisionobject", "my_test_joint")
```

## Lendo e atualizando joints

As propriedades de um joint podem ser lidas usando [`physics.get_joint_properties()`](/ref/physics/#physics.get_joint_properties:collisionobject-joint_id) e definidas usando [`physics.set_joint_properties()`](/ref/physics/#physics.set_joint_properties:collisionobject-joint_id-properties):

```lua
function update(self, dt)
    if self.accelerating then
        local hinge_props = physics.get_joint_properties("obj_a#collisionobject", "my_hinge")
        -- aumenta a velocidade do motor em 100 revoluções por segundo
        hinge_props.motor_speed = hinge_props.motor_speed + 100 * 2 * math.pi * dt
        physics.set_joint_properties("obj_a#collisionobject", "my_hinge", hinge_props)
    end
end
```

## Obter força e torque de reação do joint

A força e o torque de reação aplicados a um joint podem ser lidos usando [`physics.get_joint_reaction_force()`](/ref/physics/#physics.get_joint_reaction_force:collisionobject-joint_id) e [`physics.get_joint_reaction_torque()`](/ref/physics/#physics.get_joint_reaction_torque:collisionobject-joint_id).
