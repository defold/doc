---
title: Defold'da tuş ve metin girdisi
brief: Bu kılavuz, tuş ve metin girdisinin nasıl çalıştığını açıklar.
---

::: sidenote
Defold'da girdinin genel olarak nasıl çalıştığını, girdiyi nasıl alacağınızı ve betik dosyalarınızın girdiyi hangi sırayla aldığını öğrenmeniz önerilir. Girdi sistemi hakkında daha fazla bilgi için [Girdiye genel bakış kılavuzuna](/manuals/input) bakın.
:::

# Tuş tetikleyicileri
Tuş tetikleyicileri (key triggers), klavyedeki tek bir tuştan gelen girdiyi oyun eylemlerine bağlamanızı sağlar. Her tuş, karşılık gelen eylemle ayrı ayrı eşlenir. Tuş tetikleyicileri, yön veya WASD tuşlarıyla karakter hareketi gibi belirli işlevleri belirli tuşlara bağlamak için kullanılır. Serbest klavye girdisini okumanız gerekiyorsa metin tetikleyicilerini kullanın (aşağıya bakın).

![](images/input/key_bindings.png)

```lua
function on_input(self, action_id, action)
    if action_id == hash("left") then
        if action.pressed then
            -- start moving left
        elseif action.released then
            -- stop moving left
        end
    end
end
```

# Metin tetikleyicileri
Metin tetikleyicileri (text triggers), serbest metin girdisini okumak için kullanılır. İki tür metin tetikleyicisi vardır: `text` ve `marked-text`.

![](images/input/text_bindings.png)

## Metin
`text` tetikleyicisi normal metin girdisini yakalar. Eylem tablosunun `text` alanını, yazılan karakteri içeren bir dizeye ayarlar. Eylem yalnızca tuşa basıldığında tetiklenir; `release` veya `repeated` eylemi gönderilmez.

```lua
function on_input(self, action_id, action)
    if action_id == hash("text") then
        -- Concatenate the typed character to the "user" node...
        local node = gui.get_node("user")
        local name = gui.get_text(node)
        name = name .. action.text
        gui.set_text(node, name)
    end
end
```

## İşaretli metin
İşaretli metin (marked text) tetikleyicisi `marked-text`, esas olarak birden fazla tuşa basmanın tek bir girdiye karşılık gelebildiği Asya dillerine ait klavyelerde kullanılır. Örneğin, iOS "Japanese-Kana" klavyesinde kullanıcı tuş birleşimleri yazabilir; klavyenin üst kısmında girilebilecek simgeler veya simge dizileri görüntülenir.

![İşaretli metin girdisi](images/input/marked_text.png)

- Bir tuşa her basıldığında ayrı bir eylem oluşturulur ve eylemin `text` alanı o ana kadar girilen simge dizisine ("işaretli metin") ayarlanır.
- Kullanıcı bir simge veya simge birleşimi seçtiğinde, girdi eşlemesi (input binding) listesinde tanımlanmış olması koşuluyla ayrı bir `text` türü tetikleyici eylemi gönderilir. Bu ayrı eylemde `text` alanı kesinleşen simge dizisine ayarlanır.
