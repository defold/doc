Bileşenler (component), oyun nesnelerine (game object) belirli bir görünüm ve/veya işlev kazandırmak için kullanılır. Bileşenlerin oyun nesnelerinin içinde bulunması gerekir ve bileşeni içeren oyun nesnesinin konumundan, dönmesinden ve ölçeğinden etkilenirler:

![Bileşenler](../shared/images/components.png)

Birçok bileşenin, türüne özgü ve değiştirilebilen özellikleri vardır. Ayrıca, çalışma sırasında bileşenlerle etkileşim kurmak için bileşen türüne özgü işlevler bulunur:

```lua
-- disable the can "body" sprite
msg.post("can#body", "disable")

-- play "hoohoo" sound on "bean" in 1 second
sound.play("bean#hoohoo", { delay = 1, gain = 0.5 } )
```

Bileşenler bir oyun nesnesine ya yerinde (in-place) ya da bir bileşen dosyasına başvuru olarak eklenir:

*Outline* görünümünde oyun nesnesine <kbd>sağ tıklayın</kbd> ve <kbd>Add Component</kbd> (yerinde ekleme) veya <kbd>Add Component File</kbd> (dosya başvurusu olarak ekleme) seçeneğini seçin.

Çoğu durumda bileşenleri yerinde oluşturmak en mantıklısıdır, ancak aşağıdaki bileşen türlerinin, bir oyun nesnesine başvuru yoluyla eklenmeden önce ayrı kaynak dosyalarında oluşturulması gerekir:

* Betik (Script)
* GUI
* Parçacık efekti (Particle FX)
* Karo haritası (Tile Map)
