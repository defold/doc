---
title: Manual de compute do Defold
brief: Este manual explica como trabalhar com programas compute, constantes de shader e samplers.
---

# Programas compute

::: sidenote
O suporte a compute shaders no Defold está atualmente em *technical preview*.
Isso significa que alguns recursos ainda faltam e que a API pode mudar no futuro.
:::

Compute shaders são uma ferramenta poderosa para executar computações de uso geral na GPU. Eles permitem aproveitar o poder de processamento paralelo da GPU para tarefas como simulações de física, processamento de imagens e mais. Um compute shader opera sobre dados armazenados em buffers ou texturas, executando operações em paralelo em muitas threads da GPU. Esse paralelismo é o que torna compute shaders tão poderosos para computações intensivas.

* Para mais informações sobre o pipeline de renderização, veja a [documentação de Render](/manuals/render).
* Para uma explicação aprofundada de programas de shader, veja a [documentação de Shader](/manuals/shader).

## O que posso fazer com compute shaders?

Como compute shaders são destinados a computação genérica, realmente não há limite para o que você pode fazer com eles. Estes são alguns exemplos do que compute shaders normalmente são usados para fazer:

Processamento de imagens
  - Filtragem de imagem: aplicar blur, detecção de bordas, filtro de nitidez e assim por diante.
  - Gradação de cor: ajustar o espaço de cor de uma imagem.

Física
  - Sistemas de partículas: simular grandes quantidades de partículas para efeitos como fumaça, fogo e dinâmica de fluidos.
  - Física de corpos deformáveis: simular objetos deformáveis como tecido e gelatina.
  - Culling: occlusion culling, frustum culling.

Geração procedural
  - Geração de terreno: criar terreno detalhado usando funções de ruído.
  - Vegetação e folhagem: criar plantas e árvores geradas proceduralmente.

Efeitos de renderização
  - Iluminação global: simular iluminação realista aproximando a forma como a luz rebate em uma cena.
  - Voxelização: criar uma grade de voxels 3D a partir de dados de malha.

## Como compute shaders funcionam?

Em alto nível, compute shaders funcionam dividindo uma tarefa em muitas tarefas menores que podem ser executadas simultaneamente. Isso é alcançado por meio do conceito de `work groups` e `invocations`:

Work Groups
: O compute shader opera em uma grade de `work groups`. Cada work group contém um número fixo de invocações (ou threads). O tamanho dos work groups e o número de invocações são definidos no código do shader.

Invocations
: Cada invocação (ou thread) executa o programa compute shader. Invocações dentro de um work group podem compartilhar dados por meio de memória compartilhada, permitindo comunicação e sincronização eficientes entre elas.

A GPU executa o compute shader lançando muitas invocações em paralelo em vários work groups, oferecendo poder computacional significativo para tarefas adequadas.

## Criando um programa compute

Para criar um programa compute, use <kbd>right click</kbd> em uma pasta de destino no navegador *Assets* e selecione <kbd>New... ▸ Compute</kbd>. (Você também pode selecionar <kbd>File ▸ New...</kbd> no menu e então selecionar <kbd>Compute</kbd>). Dê um nome ao novo arquivo compute e pressione <kbd>Ok</kbd>.

![Arquivo compute](images/compute/compute_file.png)

O novo compute será aberto no *Compute Editor*.

![Editor compute](images/compute/compute.png)

O arquivo compute contém as seguintes informações:

Compute Program
: O arquivo de programa compute shader (*`.cp`*) a usar. O shader opera em "itens de trabalho abstratos", o que significa que não há uma definição fixa dos tipos de dados de entrada e saída. Cabe ao programador definir o que o compute shader deve produzir.

Constants
: Uniforms que serão passados ao programa compute shader. Veja abaixo uma lista de constantes disponíveis.

Samplers
: Você pode configurar samplers específicos opcionalmente no arquivo de materiais. Adicione um sampler, nomeie-o de acordo com o nome usado no programa shader e defina as configurações de wrap e filtro conforme preferir.


## Usando o programa compute no Defold

Ao contrário de materiais, programas compute não são atribuídos a nenhum componente e não fazem parte do fluxo normal de renderização. Um programa compute precisa ser `dispatched` em um script de renderização para fazer qualquer trabalho. Antes de despachar, no entanto, você precisa garantir que o script de renderização tenha uma referência ao programa compute. Atualmente, a única forma de um script de renderização conhecer o programa compute é adicioná-lo ao arquivo .render que mantém a referência ao seu script de renderização:

![Arquivo render compute](images/compute/compute_render_file.png)

Para usar o programa compute, primeiro ele precisa ser vinculado ao contexto de renderização. Isso é feito da mesma forma que com materiais:

```lua
render.set_compute("my_compute")
-- Faça o trabalho compute aqui, chame render.set_compute() para desvincular
render.set_compute()
```

Embora as constantes compute sejam aplicadas automaticamente quando o programa é despachado, não há como vincular entradas ou recursos de saída (texturas, buffers e assim por diante) a um programa compute pelo editor. Em vez disso, isso deve ser feito via scripts de renderização:

```lua
render.enable_texture("blur_render_target", "tex_blur")
render.enable_texture(self.storage_texture, "tex_storage")
```

Para executar o programa no espaço de trabalho que você decidiu, é preciso despachar o programa:

```lua
render.dispatch_compute(128, 128, 1)
-- dispatch_compute também aceita uma tabela de opções como último argumento
-- você pode usar essa tabela de argumentos para passar constantes de renderização
-- para a chamada dispatch
local constants = render.constant_buffer()
constants.tint = vmath.vector4(1, 1, 1, 1)
render.dispatch_compute(32, 32, 32, {constants = constants})
```

### Gravando dados a partir de programas compute

Atualmente, gerar qualquer tipo de saída a partir de um programa compute só pode ser feito via `storage textures`. Uma storage texture é semelhante a uma "textura regular", exceto que oferece suporte a mais funcionalidades e configurabilidade. Storage textures, como o nome implica, podem ser usadas como um buffer genérico no qual você pode ler e gravar dados a partir de um programa compute. Depois, você pode vincular o mesmo buffer a um programa shader diferente para leitura.

Para criar uma storage texture no Defold, você precisa fazer isso a partir de um arquivo `.script` comum. Scripts de renderização não têm essa funcionalidade, pois texturas dinâmicas precisam ser criadas via API `resource`, que só está disponível em arquivos `.script` comuns.

```lua
-- Em um arquivo .script:
function init(self)
    -- Cria um recurso de textura como de costume, mas adiciona a flag "storage"
    -- para que ele possa ser usado como armazenamento de apoio para programas compute
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = graphics.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = graphics.TEXTURE_FORMAT_RGBA32F,
        flags  = graphics.TEXTURE_USAGE_FLAG_STORAGE + graphics.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    -- obtém o handle da textura a partir do recurso
    local t_backing_handle = resource.get_texture_info(t_backing).handle

    -- notifica o renderer sobre a textura de apoio, para que ela possa ser vinculada com render.enable_texture
    msg.post("@render:", "set_backing_texture", { handle = t_backing_handle })
end
```

## Juntando tudo

### Programa shader

```glsl
// compute.cp
#version 450

layout (local_size_x = 1, local_size_y = 1, local_size_z = 1) in;

// especifica os recursos de entrada
uniform vec4 color;
uniform sampler2D texture_in;

// especifica a imagem de saída
layout(rgba32f) uniform image2D texture_out;

void main()
{
    // Este não é um shader particularmente interessante, mas demonstra
    // como ler de uma textura e de um buffer de constantes e gravar em uma storage texture

    ivec2 tex_coord   = ivec2(gl_GlobalInvocationID.xy);
    vec4 output_value = vec4(0.0, 0.0, 0.0, 1.0);
    vec2 tex_coord_uv = vec2(float(tex_coord.x)/(gl_NumWorkGroups.x), float(tex_coord.y)/(gl_NumWorkGroups.y));
    vec4 input_value = texture(texture_in, tex_coord_uv);
    output_value.rgb = input_value.rgb * color.rgb;

    // Grava o valor de saída na storage texture
    imageStore(texture_out, tex_coord, output_value);
}
```

### Componente de script
```lua
-- Em um arquivo .script

-- Aqui especificamos a textura de entrada que depois vincularemos ao
-- programa compute. Podemos atribuir esta textura a um componente de modelo
-- ou habilitá-la no contexto de renderização no script de renderização.
go.property("texture_in", resource.texture())

function init(self)
    -- Cria um recurso de textura como de costume, mas adiciona a flag "storage"
    -- para que ele possa ser usado como armazenamento de apoio para programas compute
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = graphics.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = graphics.TEXTURE_FORMAT_RGBA32F,
        flags  = graphics.TEXTURE_USAGE_FLAG_STORAGE + graphics.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    local textures = {
        texture_in = resource.get_texture_info(self.texture_in).handle,
        texture_out = resource.get_texture_info(t_backing).handle
    }

    -- notifica o renderer sobre as texturas de entrada e saída
    msg.post("@render:", "set_backing_texture", textures)
end
```

### Script de renderização
```lua
-- responde à mensagem "set_backing_texture"
-- para definir a textura de apoio do programa compute
function on_message(self, message_id, message)
    if message_id == hash("set_backing_texture") then
        self.texture_in = message.texture_in
        self.texture_out = message.texture_out
    end
end

function update(self)
    render.set_compute("compute")
    -- Podemos vincular texturas a constantes nomeadas específicas
    render.enable_texture(self.texture_in, "texture_in")
    render.enable_texture(self.texture_out, "texture_out")
    render.set_constant("color", vmath.vector4(0.5, 0.5, 0.5, 1.0))
    -- Despacha o programa compute tantas vezes quanto temos pixels.
    -- Isto constitui nosso "working group". O shader será invocado
    -- 128 x 128 x 1 vezes, ou uma vez por pixel.
    render.dispatch_compute(128, 128, 1)
    -- quando terminamos com o programa compute, precisamos desvinculá-lo
    render.set_compute()
end
```

## Compatibilidade

Atualmente, o Defold oferece suporte a compute shaders nos seguintes adaptadores gráficos:

- Vulkan
- Metal (via MoltenVK)
- OpenGL 4.3+
- OpenGL ES 3.1+

::: sidenote
Atualmente não há como verificar se o cliente em execução oferece suporte a compute shaders.
Isso significa que não há garantia de que o cliente ofereça suporte à execução de compute shaders se o adaptador gráfico for baseado em OpenGL ou OpenGL ES.
Vulkan e Metal oferecem suporte a compute shaders desde a versão 1.0. Para usar Vulkan, você precisa criar um manifesto personalizado e selecionar Vulkan como backend.
:::

