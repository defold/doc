---
title: Defold kare dizisi animasyonları kılavuzu
brief: Bu kılavuz, Defold'da kare dizisi animasyonlarının nasıl kullanılacağını açıklar.
---

# Kare dizisi animasyonu

Kare dizisi animasyonu (flipbook animation), art arda gösterilen bir dizi durağan görüntüden oluşur. Bu teknik, geleneksel selüloit animasyonuna çok benzer (bkz. http://en.wikipedia.org/wiki/Traditional_animation). Her kare ayrı ayrı değiştirilebildiği için bu teknik sınırsız olanak sunar. Ancak her kare ayrı bir görüntüde saklandığından bellekte kaplanan alan yüksek olabilir. Animasyonun akıcılığı da saniyede gösterilen görüntü sayısına bağlıdır, ancak görüntü sayısını artırmak genellikle gereken iş miktarını da artırır. Defold kare dizisi animasyonları, bir [atlasa](/manuals/atlas) eklenen ayrı görüntüler olarak ya da tüm karelerin yatay bir sıra halinde yerleştirildiği bir [karo kaynağı](/manuals/tilesource) (tile source) olarak saklanır.

  ![Animasyon sayfası](images/animation/animsheet.png){.inline}
  ![Koşma döngüsü](images/animation/runloop.gif){.inline}

## Kare dizisi animasyonlarını oynatma

Sprite bileşenleri ve GUI kutu düğümleri (GUI box nodes) kare dizisi animasyonlarını oynatabilir ve çalışma sırasında bu animasyonlar üzerinde geniş bir denetiminiz vardır.

Sprite bileşenleri
: Çalışma sırasında bir animasyonu oynatmak için [`sprite.play_flipbook()`](/ref/sprite/?q=play_flipbook#sprite.play_flipbook:url-id-[complete_function]-[play_properties]) işlevini kullanın. Aşağıdaki örneğe bakın.

GUI kutu düğümleri
: Çalışma sırasında bir animasyonu oynatmak için [`gui.play_flipbook()`](/ref/gui/?q=play_flipbook#gui.play_flipbook:node-animation-[complete_function]-[play_properties]) işlevini kullanın. Aşağıdaki örneğe bakın.

::: sidenote
`Once Ping Pong` oynatma modu, animasyonu son kareye kadar oynatır, ardından sırayı tersine çevirerek ilk kareye değil, animasyonun **ikinci** karesine kadar geri oynatır. Bu davranış, animasyonları birbirine bağlamayı kolaylaştırır.
:::

### Sprite örneği

Oyununuzda, oyuncunun belirli bir düğmeye basarak kaçınmasını sağlayan bir "dodge" (kaçınma) özelliği olduğunu varsayalım. Bu özelliği görsel geri bildirimle desteklemek için dört animasyon oluşturdunuz:

"idle"
: Oyuncu karakterinin boşta durduğu, döngüde oynatılan bir animasyon.

"dodge_idle"
: Oyuncu karakterinin kaçınma duruşunda boşta durduğu, döngüde oynatılan bir animasyon.

"start_dodge"
: Oyuncu karakterini ayakta durma durumundan kaçınma duruşuna geçiren, bir kez oynatılan bir geçiş animasyonu.

"stop_dodge"
: Oyuncu karakterini kaçınma duruşundan tekrar ayakta durma durumuna geçiren, bir kez oynatılan bir geçiş animasyonu.

Aşağıdaki betik bu mantığı uygular:

```lua

local function play_idle_animation(self)
    if self.dodge then
        sprite.play_flipbook("#sprite", hash("dodge_idle"))
    else
        sprite.play_flipbook("#sprite", hash("idle"))
    end
end

function on_input(self, action_id, action)
    -- "dodge" is our input action
    if action_id == hash("dodge") then
        if action.pressed then
            sprite.play_flipbook("#sprite", hash("start_dodge"), play_idle_animation)
            -- remember that we are dodging
            self.dodge = true
        elseif action.released then
            sprite.play_flipbook("#sprite", hash("stop_dodge"), play_idle_animation)
            -- we are not dodging anymore
            self.dodge = false
        end
    end
end
```

### GUI kutu düğümü örneği

Bir düğüm için animasyon veya görüntü seçtiğinizde, aslında görüntü kaynağını (atlas veya karo kaynağı) ve varsayılan animasyonu tek seferde atarsınız. Görüntü kaynağı düğümde statik olarak belirlenir, ancak oynatılacak geçerli animasyon çalışma sırasında değiştirilebilir. Durağan görüntüler tek karelik animasyonlar olarak ele alındığından, çalışma sırasında bir görüntüyü değiştirmek, düğüm için farklı bir kare dizisi animasyonu oynatmakla eşdeğerdir:

```lua
function init(self)
    local character_node = gui.get_node("character")
    -- This requires that the node has a default animation in the same atlas or tile source as
    -- the new animation/image we're playing.
    gui.play_flipbook(character_node, "jump_left")
end
```


## Tamamlanma geri çağırımları

`sprite.play_flipbook()` ve `gui.play_flipbook()` işlevleri, son bağımsız değişken olarak isteğe bağlı bir Lua geri çağırım işlevini (callback function) destekler. Bu işlev, animasyon sonuna kadar oynatıldığında çağrılır. Döngüde oynatılan animasyonlar için bu işlev hiçbir zaman çağrılmaz. Geri çağırım, animasyon tamamlandığında olayları tetiklemek veya birden çok animasyonu birbirine bağlamak için kullanılabilir. Örnekler:

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    sprite.play_flipbook("#character", "jump_left", flipbook_done)
end
```

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    gui.play_flipbook(gui.get_node("character"), "jump_left", flipbook_done)
end
```
