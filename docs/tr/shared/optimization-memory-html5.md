## Öbek boyutu (HTML5)
Bir Defold HTML5 oyununun öbek boyutu (heap size), *game.project* dosyasındaki [`heap_size` alanından](/manuals/project-settings/#heap-size) yapılandırılabilir. Oyununuzun bellek kullanımını optimize ettiğinizden ve öbek boyutunu mümkün olan en küçük değere ayarladığınızdan emin olun.

Küçük oyunlarda 32 MB öbek boyutuna ulaşmak mümkündür. Daha büyük oyunlarda 64–128 MB hedefleyin. Örneğin, kullanımınız 58 MB ise ve daha fazla optimizasyon yapmak mümkün değilse, üzerinde fazla düşünmeden 64 MB değerini seçebilirsiniz. Kesin bir hedef boyut yoktur; bu, oyuna bağlıdır. Yalnızca daha küçük boyutları hedefleyin; ideal olarak ikinin kuvvetlerine karşılık gelen değerlerle ilerleyin. 

Geçerli öbek kullanımını kontrol etmek için oyununuzu başlatıp en fazla "kaynak tüketen" seviyeyi veya bölümü oynayarak bellek kullanımını izleyebilirsiniz:

```lua
if html5 then
    local mem = tonumber(html5.run("HEAP8.length") / 1024 / 1024)
    print(mem)
end
```

Tarayıcınızın geliştirici araçlarını açıp konsola şunu da yazabilirsiniz:

```js
HEAP8.length / 1024 / 1024
```

Bellek kullanımı 32 MB düzeyinde kalıyorsa harika! Kalmıyorsa, [motorun kendisinin ve sesler ile dokular gibi büyük varlıkların boyutunu optimize etmek](/manuals/optimization-size) için belirtilen adımları izleyin.