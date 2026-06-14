---
title: Layouts de GUI no Defold
brief: O Defold oferece suporte a GUIs que se adaptam automaticamente a mudanças de orientação de tela em dispositivos móveis. Este documento explica como o recurso funciona.
---

# Layouts

O Defold oferece suporte a GUIs que se adaptam automaticamente a mudanças de orientação de tela em dispositivos móveis. Usando esse recurso, você pode criar GUIs que se adaptam à orientação e à proporção de tela de vários tamanhos de tela. Também é possível criar layouts que correspondem a modelos específicos de dispositivo.

## Criando perfis de exibição {#creating-display-profiles}

Por padrão, as configurações de *game.project* especificam que um arquivo integrado de configurações de perfis de exibição ("builtins/render/default.display_profiles") é usado. Os perfis padrão são "Landscape" (1280 pixels de largura e 720 pixels de altura) e "Portrait" (720 pixels de largura e 1280 pixels de altura). Nenhum modelo de dispositivo é definido nos perfis, então eles corresponderão a qualquer dispositivo.

Para criar um novo arquivo de configurações de perfis, copie o arquivo da pasta "builtins" ou clique com o botão direito em um local adequado na visualização *Assets* e selecione <kbd>New... ▸ Display Profiles</kbd>. Dê ao novo arquivo um nome adequado e clique em <kbd>Ok</kbd>.

O editor agora abre o novo arquivo para edição. Adicione novos perfis clicando no <kbd>+</kbd> na lista *Profiles*. Para cada perfil, adicione um conjunto de *qualifiers*:

Width
: A largura em pixels do qualificador.

Height
: A altura em pixels do qualificador.

Device Models
: Uma lista separada por vírgulas de modelos de dispositivo. O modelo do dispositivo corresponde ao início do nome do modelo, por exemplo, `iPhone10` corresponderá aos modelos "iPhone10,\*". Nomes de modelo com vírgulas devem ficar entre aspas, isto é, `"iPhone10,3", "iPhone10,6"` corresponde aos modelos iPhone X (veja a [wiki do iPhone](https://www.theiphonewiki.com/wiki/Models)). Observe que as únicas plataformas que informam um modelo de dispositivo ao chamar `sys.get_sys_info()` são Android e iOS. Outras plataformas retornam uma string vazia e, portanto, nunca escolherão um perfil de exibição que tenha um qualificador de modelo de dispositivo.

![Novos perfis de exibição](images/gui-layouts/new_profiles.png)

Você também precisa especificar que a engine deve usar seus novos perfis. Abra *game.project* e selecione o arquivo de perfis de exibição na configuração *Display Profiles* em *display*:

![Configurações](images/gui-layouts/settings.png)

Se quiser que a engine alterne automaticamente entre layouts retrato e paisagem ao girar o dispositivo, marque a caixa *Dynamic Orientation*. A engine selecionará dinamicamente um layout correspondente e também mudará a seleção se o dispositivo alterar a orientação.

### Seleção automática de layout (Display Profiles)

O recurso Display Profiles tem uma opção “Auto Layout Selection” (ativada por padrão). Quando ativada, a engine seleciona automaticamente o layout de GUI com melhor correspondência tanto quando a cena é criada quanto quando o tamanho da janela/tela muda. Quando desativada, a engine não muda layouts automaticamente; use `gui.set_layout()` no seu script de GUI para alternar layouts manualmente. Essa configuração é armazenada no arquivo Display Profiles e afeta todas as cenas GUI.

## Layouts de GUI

O conjunto atual de perfis de exibição pode ser usado para criar variantes de layout da sua configuração de nodes GUI. Para adicionar um novo layout a uma cena GUI, clique com o botão direito no ícone *Layouts* na visualização *Outline* e selecione <kbd>Add ▸ Layout ▸ ...</kbd>:

![Adicionar layout à cena](images/gui-layouts/add_layout.png)

Ao editar uma cena GUI, todos os nodes são editados em um layout específico. O layout selecionado atualmente é indicado no menu suspenso de layout da cena GUI na barra de ferramentas. Se nenhum layout for escolhido, os nodes são editados no layout *Default*.

![Barra de ferramentas de layouts](images/gui-layouts/toolbar.png)

![edição em retrato](images/gui-layouts/portrait.png)

Cada alteração em uma propriedade de node feita com um layout selecionado _sobrescreve_ a propriedade em relação ao layout *Default*. Propriedades sobrescritas são marcadas em azul. Nodes com propriedades sobrescritas também são marcados em azul. Você pode clicar no botão de reset ao lado de qualquer propriedade sobrescrita para restaurá-la ao valor original.

![edição em paisagem](images/gui-layouts/landscape.png)

Um layout não pode apagar nem criar novos nodes, apenas sobrescrever propriedades. Se precisar remover um node de um layout, você pode movê-lo para fora da tela ou apagá-lo com lógica de script. Você também deve prestar atenção ao layout selecionado atualmente. Se você adicionar um layout ao seu projeto, o novo layout será configurado de acordo com o layout selecionado no momento. Além disso, copiar e colar nodes considera o layout selecionado atualmente, ao copiar *e* ao colar.

## Seleção dinâmica de perfil

Quando Auto Layout Selection está habilitado, a engine seleciona automaticamente o layout com melhor correspondência. A correspondência dinâmica de layouts pontua cada qualificador de perfil de exibição de acordo com as seguintes regras:

1. Se não houver modelo de dispositivo definido, ou se o modelo de dispositivo corresponder, uma pontuação (S) é calculada para o qualificador.

2. A pontuação (S) é calculada com a área da tela (A), a área do qualificador (A_Q), a proporção de tela (R) e a proporção do qualificador (R_Q):

<img src="https://latex.codecogs.com/svg.latex?\inline&space;S=\left|1&space;-&space;\frac{A}{A_Q}\right|&space;&plus;&space;\left|1&space;-&space;\frac{R}{R_Q}\right|" title="S=\left|1 - \frac{A}{A_Q}\right| + \left|1 - \frac{R}{R_Q}\right|" />

3. O perfil com o qualificador de menor pontuação é selecionado, se a orientação (paisagem ou retrato) do qualificador corresponder à tela.

4. Se nenhum perfil com um qualificador da mesma orientação for encontrado, o perfil com o qualificador de melhor pontuação da outra orientação será selecionado.

5. Se nenhum perfil puder ser selecionado, o perfil fallback *Default* será usado.

Como o layout *Default* é usado como fallback em runtime quando não há layout com melhor correspondência, isso significa que, se você adicionar um layout "Landscape", ele será a melhor correspondência para *todas* as orientações até que você também adicione um layout "Portrait".

## Mensagens de mudança de layout

Quando o layout muda, uma mensagem `layout_changed` é enviada ao script do componente GUI. Isso acontece quando a engine muda o layout automaticamente (Auto Layout Selection ON) ou quando seu script chama `gui.set_layout()` e o layout realmente muda. A mensagem contém o id com hash do layout, para que o script possa executar lógica dependendo de qual layout está selecionado:

```lua
function on_message(self, message_id, message, sender)
  if message_id == hash("layout_changed") and message.id == hash("My Landscape") then
    -- alternando layout para paisagem
  elseif message_id == hash("layout_changed") and message.id == hash("My Portrait") then
    -- alternando layout para retrato
  end
end
```

Além disso, o script de renderização atual recebe uma mensagem sempre que a janela (visualização do jogo) muda, e isso inclui mudanças de orientação.

```lua
function on_message(self, message_id, message)
  if message_id == hash("window_resized") then
    -- A janela foi redimensionada. message.width e message.height contêm as
    -- novas dimensões da janela.
  end
end
```

Quando a orientação é alterada, o gerenciador de layout da GUI escala e reposiciona automaticamente os nodes GUI de acordo com seu layout e propriedades de node. O conteúdo dentro do jogo, porém, é renderizado em uma passagem separada (por padrão) com uma projeção stretch-fit na janela atual. Para mudar esse comportamento, forneça seu próprio script de renderização modificado ou use uma [biblioteca](/assets/) de câmera.

## Seleção manual de layout (Lua)

Quando Auto Layout Selection está desativado para os Display Profiles em uso, a engine não alterna layouts automaticamente. Use estas funções a partir de um script de GUI para gerenciar layouts manualmente:

### gui.set_layout(layout)

- Aceita uma string ou hash (id do layout).
- Retorna boolean: `true` se o layout existir na cena e tiver sido aplicado; `false` caso contrário.
- Se o layout existir em Display Profiles, atualiza a resolução da cena para a largura/altura do perfil.
- Emite `layout_changed` quando o layout realmente muda.

Exemplo:

```lua
function init(self)
    -- Aplica manualmente o layout "Portrait"
    local ok = gui.set_layout("Portrait")
    if not ok then
        print("Portrait layout not found in this scene")
    end
end
```

### gui.get_layouts()

- Retorna uma tabela que mapeia cada hash de id de layout para `vmath.vector3(width, height, 0)`.
- Para o layout padrão, retorna a resolução atual da cena.

Exemplo:

```lua
local layouts = gui.get_layouts()
for id, size in pairs(layouts) do
    print(id, size.x, size.y)
end
```

Observação: se um layout de GUI existir na cena, mas não estiver presente em Display Profiles, `gui.set_layout()` ainda aplicará as sobrescritas de node por layout, mas não mudará a resolução da cena.
