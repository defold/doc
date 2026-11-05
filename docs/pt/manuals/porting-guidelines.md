---
title: Diretrizes de porting e lançamento
brief: Este manual destaca alguns pontos a considerar ao portar um jogo para uma nova plataforma ou ao lançar seu jogo pela primeira vez.
---

# Diretrizes de porting e lançamento

Esta página contém um guia útil e uma checklist de itens a considerar ao lançar um jogo ou ao portar para uma nova plataforma.

Portar um jogo Defold para uma nova plataforma ou lançá-lo pela primeira vez costuma ser um processo direto. Em teoria, basta garantir que as seções relevantes estejam configuradas no arquivo *game.project*, mas, para aproveitar ao máximo cada plataforma, é recomendado adaptar o jogo às especificidades de cada uma.


## Entrada
Certifique-se de adaptar o jogo aos métodos de entrada da plataforma. Considere adicionar suporte a [gamepads](/manuals/input-gamepads) se a plataforma oferecer suporte a isso! E certifique-se de que o jogo tenha suporte a um menu de pausa; se um controle desconectar repentinamente, o jogo deve ser pausado!

## Localização
Traduza qualquer texto do jogo. Para lançamento na Europa e nas Américas, considere traduzir pelo menos para EFIGS (inglês, francês, italiano, alemão e espanhol). Certifique-se de que seja possível alternar facilmente entre diferentes idiomas dentro do jogo (por meio do menu de pausa).

::: important
Somente iOS - Certifique-se de especificar [Localizations](/manuals/project-settings/#localizations) em `game.project`, pois `sys.get_info()` nunca retornará um idioma que não esteja nessa lista.
:::

Traduza o texto da página da loja, pois isso terá um impacto positivo nas vendas! Algumas plataformas exigem que o texto da página da loja seja traduzido para o idioma de cada país onde o jogo está disponível.

## Materiais da loja

### Ícone do app
Certifique-se de que seu jogo se destaque da concorrência. O ícone costuma ser seu primeiro ponto de contato com jogadores em potencial. Ele deve ser fácil de encontrar em uma página cheia de ícones de jogos.

### Banners e imagens da loja
Certifique-se de usar arte impactante e empolgante para seu jogo. Provavelmente vale a pena gastar algum dinheiro para trabalhar com um artista e criar arte que atraia jogadores.


## Jogos salvos

### Jogos salvos em desktop, mobile e web
Jogos salvos e outros estados salvos podem ser armazenados usando a função da API Defold `sys.save(filename, data)` e carregados usando `sys.load(filename)`. Você pode usar `sys.get_save_file(application_id, name)` para obter um caminho para um local específico do sistema operacional onde arquivos podem ser salvos, normalmente na pasta home do usuário logado.

### Jogos salvos em console
Usar `sys.get_save_file()` e `sys.save()` funciona bem na maioria das plataformas, mas em consoles é recomendado usar uma abordagem diferente. Plataformas de console normalmente associam um usuário a cada controle conectado e, portanto, jogos salvos, conquistas e outros recursos devem ser associados ao respectivo usuário.

Os eventos de entrada de gamepad conterão um id de usuário que pode ser usado para associar as ações de um controle a um usuário no console.

As plataformas de console e suas extensões nativas expõem funções de API específicas da plataforma para salvar e carregar dados associados a um usuário específico. Use essas APIs ao salvar e carregar em console.

APIs de plataformas de console para operações de arquivo normalmente são assíncronas. Ao desenvolver um jogo multiplataforma voltado para console, é recomendado projetar seu jogo de modo que todas as operações de arquivo sejam assíncronas, independentemente da plataforma. Exemplo:

```lua
local function save_game(data, user_id, cb)
	if console then
		local filename = "savegame"
		consoleapi.save(user_id, filename, data, cb)
	else
		local filename = sys.get_save_file("mygame", "savegame" .. user_id)
		local success = sys.save(filename, data)
		cb(success)
	end
end
```


## Artefatos de build

Certifique-se de [gerar símbolos de depuração](/manuals/debugging-native-code/#symbolicate-a-callstack) para cada versão lançada, para que você possa depurar travamentos. Armazene-os junto com o pacote da aplicação.

## Otimizações da aplicação

Leia o [manual de Otimização](/manuals/optimization) sobre como otimizar sua aplicação em desempenho, tamanho, memória e uso de bateria.



## Desempenho
Sempre teste no hardware-alvo! Verifique o desempenho do jogo e otimize se necessário. Use o [perfilador](/manuals/profiling) para encontrar gargalos no código.


## Resolução de tela e taxa de atualização
Para plataformas com orientação e resolução de tela fixas: verifique se o jogo funciona na resolução de tela e proporção de tela da plataforma-alvo. Para plataformas com resolução e proporção de tela variáveis: verifique se o jogo funciona em uma variedade de resoluções e proporções de tela. Considere que tipo de [projeção de visualização](/manuals/render/#default-view-projection) é usada no script de renderização e na câmera.

Para plataformas mobile, bloqueie a orientação da tela em *game.project* ou certifique-se de que o jogo funcione nos modos paisagem e retrato.

* **Tamanhos de tela** - Tudo parece correto em uma tela maior ou menor do que a largura e altura padrão definidas em *game.project*?
  * A projeção usada no script de renderização e os layouts usados na GUI terão influência aqui.
* **Proporções de tela** - Tudo parece correto em uma tela com uma proporção diferente da proporção padrão derivada da largura e altura definidas em *game.project*?
  * A projeção usada no script de renderização e os layouts usados na GUI terão influência aqui.
* **Taxa de atualização** - O jogo roda bem em uma tela com taxa de atualização maior que 60 Hz?
  * O vsync e o intervalo de swap na seção Display de *game.project*


<a id="mobile-phones-and-notch-and-hole-punch-cameras"></a>

## Celulares, notch e câmeras hole punch
Tornou-se cada vez mais comum usar um pequeno recorte de lente na tela para acomodar a câmera frontal e sensores (também conhecido como notch ou câmera hole punch). Ao portar um jogo para mobile, mantenha as informações críticas dentro da área segura da plataforma.

O Defold tem suporte integrado a áreas seguras no Android e iOS. Defina `gui.safe_area_mode` em *game.project* para controlar quais insets opostos da área segura afetam o ajuste da GUI. `none` é o padrão e ignora os insets; `long` aplica esquerda/direita no modo paisagem e superior/inferior no modo retrato; `short` aplica o par oposto; e `both` aplica as quatro bordas. Um GUI script pode substituir o modo do projeto para sua cena com [`gui.set_safe_area_mode()`](/ref/gui/#gui.set_safe_area_mode). Para lógica personalizada de GUI ou renderização, [`window.get_safe_area()`](/ref/window/#window.get_safe_area) retorna o retângulo seguro e os insets individuais de cada borda. Plataformas sem insets de área segura integrados retornam a janela inteira e insets iguais a zero.

A [extensão Safe Area](/extension-safearea) continua sendo uma alternativa para projetos legados ou fluxos de trabalho que precisem de um comportamento além das APIs integradas; ela não é necessária para o tratamento padrão de áreas seguras no Android e iOS.

### Áreas reservadas da tela {#reserved-screen-areas}

[`window.get_reserved_areas()`](/ref/window/#window.get_reserved_areas) informa regiões individuais que obstruem a janela do jogo, como recortes de câmera e a Dynamic Island. Use esses retângulos ao posicionar conteúdo ao redor de obstruções individuais. Use `window.get_safe_area()` quando precisar de um único retângulo seguro para o layout e suas margens de borda.

O resultado é um array de tabelas com os campos `x`, `y`, `width` e `height`. Cada retângulo é recortado aos limites da janela do jogo. A origem fica no canto inferior esquerdo: `x` é a borda esquerda e `y` é a borda inferior, em pixels da janela correspondentes a [`window.get_size()`](/ref/window/#window.get_size). Essas coordenadas são independentes do ajuste de GUI e da resolução lógica em *game.project*; portanto, considere as transformações da GUI antes de usá-las como posições de nós.

O suporte por plataforma é:

- **iOS 27.1 e posteriores:** oclusões ativas informadas pelo UIKit, incluindo suas margens de interação.
- **Android 9 (API de nível 28) e posteriores:** retângulos de recorte da tela.

A função retorna uma tabela vazia em plataformas e versões de sistema operacional sem suporte ou quando nenhuma obstrução é informada para a janela. Uma tabela vazia não significa que a janela inteira seja segura para conteúdo importante: dobras, barras do sistema, teclados e regiões de gestos estão fora do escopo desta API. Use `window.get_safe_area()` para obter o retângulo seguro da plataforma.

### Atualizando áreas após eventos de janela {#refreshing-areas-after-window-events}

Consulte as áreas reservadas durante a inicialização e novamente em cada callback de [`window.WINDOW_EVENT_RESIZED`](/ref/window/#window.WINDOW_EVENT_RESIZED). Após a primeira consulta, alterações na geometria das áreas reservadas também disparam esse evento em plataformas compatíveis, mesmo quando o tamanho da janela permanece igual. Cada tabela retornada é um retrato daquele momento; tabelas salvas não são atualizadas automaticamente.

No iOS, esse evento também é enviado após transições de orientação e mudanças nas margens da área segura. Uma rotação de 180° em paisagem pode mover um recorte de câmera ou a Dynamic Island para o outro lado, enquanto as dimensões da janela e as margens da área segura permanecem iguais. Atualize a geometria ao receber o evento mesmo quando `data.width` e `data.height` forem iguais aos valores anteriores.

O script abaixo mantém ambos os conjuntos de geometria atualizados:

```lua
local function refresh_screen_areas(self)
    self.safe_area = window.get_safe_area()
    self.reserved_areas = window.get_reserved_areas()
    -- Atualize sua interface usando o novo retângulo seguro e as áreas reservadas.
end

local function on_window_event(self, event, data)
    if event == window.WINDOW_EVENT_RESIZED then
        -- Atualize mesmo quando a largura e a altura não tiverem mudado.
        refresh_screen_areas(self)
    end
end

function init(self)
    refresh_screen_areas(self)
    window.set_listener(on_window_event)
end

function final(self)
    window.set_listener(nil)
end
```

Apenas um listener de eventos de janela pode ser registrado por vez. Se seu jogo já tiver um, adicione essa lógica de atualização a ele. Substituir o array salvo a cada atualização também limpa retângulos obsoletos quando o resultado fica vazio.


## Diretrizes específicas de plataforma

### Android
Certifique-se de armazenar seu [keystore](/manuals/android/#creating-a-keystore) em um local seguro para poder atualizar seu jogo.


### Consoles
Armazene o pacote completo de cada versão. Você precisará desses arquivos se quiser aplicar patches ao jogo.


### Nintendo Switch
Integre código específico da plataforma - Para Nintendo Switch, há uma extensão separada com algumas funcionalidades auxiliares para seleção de usuário etc.

O Defold para Nintendo Switch usa Vulkan como backend gráfico - Certifique-se de testar o jogo usando o [backend gráfico Vulkan](https://github.com/defold/extension-vulkan).


### PlayStation®4
Integre código específico da plataforma - Para PlayStation®4, há uma extensão separada com algumas funcionalidades auxiliares para seleção de usuário etc.


### HTML5
Jogar jogos web em celulares está se tornando cada vez mais popular - Tente fazer o jogo rodar bem também em um navegador mobile! Também é importante lembrar que espera-se que jogos web carreguem rapidamente! Certifique-se de otimizar o jogo em tamanho. Considere também a experiência de carregamento em geral para não perder jogadores desnecessariamente.

Em 2018, os navegadores introduziram uma política de autoplay para sons que impede jogos e outros conteúdos web de reproduzir sons até que um evento de interação do usuário (toque, botão, gamepad etc.) tenha ocorrido. É importante levar isso em conta ao portar para HTML5 e só começar a tocar sons e música após a primeira interação do usuário. Tentativas de reproduzir sons antes de qualquer interação do usuário serão registradas como erro no console de desenvolvedor do navegador, mas não afetarão o jogo.

Certifique-se também de pausar quaisquer sons em reprodução se o jogo estiver exibindo anúncios.
