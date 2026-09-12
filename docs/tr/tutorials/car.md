---
title: Defold ile basit bir araba oluşturma.
brief: Defold kullanmaya yeni başladıysanız bu kılavuz düzenleyiciyi tanımanıza yardımcı olacaktır. Ayrıca temel fikirleri ve Defold'un en yaygın yapı taşlarını açıklar - oyun nesneleri, koleksiyonlar, betikler ve sprite bileşenleri.
---

# Araba oluşturma

Defold kullanmaya yeni başladıysanız bu kılavuz düzenleyiciyi tanımanıza yardımcı olacaktır. Ayrıca temel fikirleri ve Defold'un en yaygın yapı taşlarını açıklar: oyun nesneleri, koleksiyonlar, betikler ve sprite bileşenleri.

Boş bir projeyle başlayıp adım adım çok küçük, oynanabilir bir uygulama oluşturacağız. Sonunda Defold'un nasıl çalıştığı hakkında bir fikir edinmiş ve daha kapsamlı bir öğreticiyi izlemeye ya da doğrudan kılavuzlara geçmeye hazır olacağınızı umuyoruz.

::: sidenote
Öğretici boyunca kavramlara ve belirli işlemlerin nasıl yapıldığına ilişkin ayrıntılı açıklamalar, bu paragraf gibi işaretlenmiştir. Bu bölümlerin fazla ayrıntıya girdiğini düşünüyorsanız onları atlayabilirsiniz.
:::

## Yeni proje oluşturma

![Yeni proje](images/new_empty.png)

1. Defold'u başlatın.
2. Soldaki *New Project* seçeneğini seçin.
3. *From Template* sekmesini seçin.
4. *Empty Project* seçeneğini seçin
5. Proje için yerel sürücünüzde bir konum seçin.
6. *Create New Project* düğmesine tıklayın.

## Düzenleyici

[Yeni bir proje](/manuals/project-setup/) oluşturup düzenleyicide açarak başlayın. *main/main.collection* dosyasına çift tıklarsanız dosya açılır:

![Düzenleyiciye genel bakış](../manuals/images/editor/editor2_overview.png)

Düzenleyici şu ana alanlardan oluşur:

Assets bölmesi
: Bu görünüm projenizdeki tüm dosyaları gösterir. Farklı dosya türlerinin farklı simgeleri vardır. Bir dosyayı türüne uygun düzenleyicide açmak için çift tıklayın. Salt okunur özel *builtins* klasörü tüm projelerde ortaktır ve varsayılan bir işleme betiği (render script), bir yazı tipi, çeşitli bileşenlerin işlenmesi (rendering) için materyaller ve başka yararlı öğeler içerir.

Ana düzenleyici görünümü
: Düzenlediğiniz dosyanın türüne bağlı olarak bu görünümde o türe uygun bir düzenleyici gösterilir. En yaygın kullanılanı, burada gördüğünüz Scene düzenleyicisidir. Açık olan her dosya ayrı bir sekmede gösterilir.

Changed Files
: Geçerli Git commit'ine göre yerel olarak eklenen, değiştirilen, yeniden adlandırılan veya silinen dosyaları içerir. Burada metin farklarını görüntüleyebilir ve yerel değişiklikleri geri alabilirsiniz. Uzak bir depoyla eşitlemek için harici bir Git istemcisi veya komut satırı kullanın.

Outline
: O anda düzenlenen dosyanın içeriğini hiyerarşik bir görünümde gösterir. Bu görünüm aracılığıyla nesneleri ve bileşenleri ekleyebilir, silebilir, değiştirebilir ve seçebilirsiniz.

Properties
: O anda seçili nesne veya bileşen için ayarlanmış özellikler.

Console
: Oyun çalışırken bu görünüm, oyun motorundan gelen çıktıları (günlük kayıtları, hatalar, hata ayıklama bilgileri vb.) ve betiklerinizdeki özel `print()` ve `pprint()` hata ayıklama iletilerini gösterir. Uygulamanız veya oyununuz başlamıyorsa ilk kontrol etmeniz gereken yer konsoldur. Konsolun arkasında hata bilgilerini gösteren bir dizi sekme ve parçacık efektleri oluşturulurken kullanılan bir eğri düzenleyicisi bulunur.

## Oyunu çalıştırma

"Empty" proje şablonu gerçekten de tamamen boştur. Yine de projeyi derleyip oyunu başlatmak için <kbd>Project ▸ Build</kbd> seçeneğini seçin.

![Proje derleme](images/car/start_build_and_launch.png)

Siyah bir ekran pek heyecan verici olmayabilir, ancak bu, çalışan bir Defold oyun uygulamasıdır ve onu kolayca daha ilginç bir şeye dönüştürebiliriz. Öyleyse bunu yapalım.

::: sidenote
Defold düzenleyicisi dosyalar üzerinde çalışır. *Assets bölmesinde* bir dosyaya çift tıklayarak onu uygun bir düzenleyicide açarsınız. Ardından dosyanın içeriği üzerinde çalışabilirsiniz.

Bir dosyayı düzenlemeyi bitirdiğinizde onu kaydetmeniz gerekir. Ana menüden <kbd>File ▸ Save</kbd> seçeneğini seçin. Düzenleyici, kaydedilmemiş değişiklikler içeren dosyaların sekmelerindeki dosya adına bir yıldız işareti '\*' ekleyerek bunu belirtir.

![Kaydedilmemiş değişiklikler içeren dosya](images/car/file_changed.png)
:::

## Arabayı birleştirme

İlk yapacağımız şey yeni bir koleksiyon (collection) oluşturmak. Koleksiyon, yerleştirdiğiniz ve konumlandırdığınız oyun nesnelerini barındıran bir kapsayıcıdır. Koleksiyonlar en yaygın olarak oyun bölümleri oluşturmak için kullanılır, ancak bir arada bulunması gereken oyun nesnesi gruplarını ve/veya hiyerarşilerini yeniden kullanmanız gerektiğinde de çok yararlıdır. Koleksiyonları bir tür yeniden kullanılabilir nesne tanımı, yani prefab olarak düşünmek faydalı olabilir.

*Assets bölmesindeki* *main* klasörüne tıklayın, ardından sağ tıklayıp <kbd>New ▸ Collection File</kbd> seçeneğini seçin. Ana menüden <kbd>File ▸ New ▸ Collection File</kbd> seçeneğini de seçebilirsiniz.

![Yeni koleksiyon dosyası](images/car/start_new_collection.png)

Yeni koleksiyon dosyasına *car.collection* adını verin ve dosyayı açın. Bu yeni, boş koleksiyonu kullanarak birkaç oyun nesnesinden küçük bir araba oluşturacağız. Oyun nesnesi (game object), oyununuzu oluşturmak için kullandığınız bileşenleri (component; sprite bileşenleri, sesler, oyun mantığı betikleri vb.) barındıran bir kapsayıcıdır. Her oyun nesnesi, oyunda id değeriyle benzersiz olarak tanımlanır. Oyun nesneleri ileti aktarımı (message passing) yoluyla birbirleriyle iletişim kurabilir; buna daha sonra değineceğiz.

Ayrıca burada yaptığımız gibi bir koleksiyonun içinde yerinde bir oyun nesnesi oluşturmak da mümkündür. Bunun sonucunda kendine özgü bir nesne oluşur. Bu nesneyi kopyalayabilirsiniz, ancak her kopya ayrıdır---birini değiştirmek diğerlerini etkilemez. Yani bir oyun nesnesinin 10 kopyasını oluşturup hepsini değiştirmek istediğinizi fark ederseniz nesnenin 10 örneğinin tamamını düzenlemeniz gerekir. Bu nedenle, yerinde oluşturulan oyun nesneleri çok sayıda kopyasını oluşturmayı düşünmediğiniz nesneler için kullanılmalıdır.

Buna karşılık, bir _dosyada_ saklanan oyun nesnesi bir prototip (prototype; diğer motorlarda "prefab" veya "taslak", yani "blueprint" olarak da bilinir) işlevi görür. Dosyada saklanan bir oyun nesnesinin örneklerini koleksiyona yerleştirdiğinizde her nesne _başvuru yoluyla_ yerleştirilir---yani prototipe dayalı bir klondur. Prototipi değiştirmeniz gerektiğine karar verirseniz o prototipe dayalı olarak yerleştirilen her oyun nesnesi anında güncellenir.

![Araba oyun nesnesi ekleme](images/car/start_add_car_gameobject.png)

*Outline* görünümünde kök "Collection" düğümünü seçin, sağ tıklayıp <kbd>Add Game Object</kbd> seçeneğini seçin. Koleksiyonda id değeri "go" olan yeni bir oyun nesnesi görünür. Bu nesneyi seçin ve *Properties* görünümünde id değerini "car" olarak ayarlayın. "car" şu ana kadar pek ilgi çekici değil. Boş; ne görsel bir temsili ne de herhangi bir mantığı var. Görsel bir temsil eklemek için bir sprite _bileşeni_ eklememiz gerekir.

Bileşenler, oyun nesnelerine görsel ve işitsel varlık (grafikler, ses) ve işlevsellik (fabrikalarla (factory) çalışma sırasında nesne oluşturma, çarpışmalar, betiklerle tanımlanan davranışlar) eklemek için kullanılır. Bir bileşen kendi başına var olamaz; bir oyun nesnesinin içinde bulunmalıdır. Bileşenler genellikle oyun nesnesiyle aynı dosyada yerinde tanımlanır. Ancak bir bileşeni yeniden kullanmak istiyorsanız onu ayrı bir dosyada saklayabilir (oyun nesnelerinde olduğu gibi) ve herhangi bir oyun nesnesi dosyasına başvuru olarak ekleyebilirsiniz. Bazı bileşen türlerinin (örneğin Lua betiklerinin) ayrı bir bileşen dosyasına yerleştirilmesi ve ardından nesnelerinize başvuru olarak eklenmesi gerekir.

Bileşenleri doğrudan değiştirmediğinizi unutmayın---bileşenleri barındıran oyun nesnelerini taşıyabilir, döndürebilir, ölçekleyebilir ve özelliklerine animasyon uygulayabilirsiniz.

![Araba bileşeni ekleme](images/car/start_add_car_component.png)

"car" oyun nesnesini seçin, sağ tıklayıp <kbd>Add Component</kbd> seçeneğini seçin; ardından *Sprite* seçeneğini seçip *Ok* düğmesine tıklayın. *Outline* görünümünde sprite bileşenini seçerseniz bazı özelliklerinin ayarlanması gerektiğini görürsünüz:

Image
: Burada sprite bileşeni için bir görüntü kaynağı gerekir. *Assets bölmesinde* "main" klasörünü seçin, sağ tıklayıp <kbd>New ▸ Atlas File</kbd> seçeneğini seçerek bir atlas görüntü dosyası oluşturun. Yeni atlas dosyasına *sprites.atlas* adını verin ve atlas düzenleyicisinde açmak için çift tıklayın. Aşağıdaki iki görüntü dosyasını bilgisayarınıza kaydedin ve *Assets bölmesindeki* *main* klasörüne sürükleyin. Artık atlas düzenleyicisinde Atlas kök düğümünü seçip sağ tıklayarak <kbd>Add Images</kbd> seçeneğini seçebilirsiniz. Araba ve lastik görüntülerini atlasa ekleyip kaydedin. Artık "car" koleksiyonundaki "car" oyun nesnesinde bulunan sprite bileşeninin görüntü kaynağı olarak *sprites.atlas* dosyasını seçebilirsiniz.

Oyunumuz için görüntüler:

![Araba görüntüsü](images/car/start_car.png)
![Lastik görüntüsü](images/car/start_tire.png)

Bu görüntüleri atlasa ekleyin:

![Sprite atlası](images/car/start_sprites_atlas.png)

![Sprite özellikleri](images/car/start_sprite_properties.png)

Default Animation
: Bunu "car" olarak (veya araba görüntüsüne verdiğiniz ad neyse o adla) ayarlayın. Her sprite bileşeni, oyunda gösterildiğinde oynatılacak bir varsayılan animasyona ihtiyaç duyar. Bir atlasa görüntü eklediğinizde Defold, her görüntü dosyası için tek karelik (durağan) animasyonlar oluşturarak işinizi kolaylaştırır.

## Arabayı tamamlama

Koleksiyona iki oyun nesnesi daha ekleyerek devam edin. Bunlara "left_wheel" ve "right_wheel" adlarını verin ve her birine, *sprites.atlas* dosyasına eklediğimiz lastik görüntüsünü gösteren bir sprite bileşeni koyun. Ardından tekerlek oyun nesnelerini tutup "car" üzerine bırakarak onları "car" nesnesinin alt nesneleri yapın. Başka oyun nesnelerinin alt nesnesi olan oyun nesneleri, üst nesneleri hareket ettiğinde ona bağlı kalır. Ayrı ayrı da hareket ettirilebilirler, ancak tüm hareketler üst nesneye göredir. Bu, lastikler için tam istediğimiz davranıştır; çünkü onların arabaya bağlı kalmasını isteriz ve arabayı yönlendirirken onları hafifçe sola ve sağa döndürmemiz yeterlidir. Bir koleksiyon, yan yana duran, karmaşık üst-alt nesne ağaçları biçiminde düzenlenmiş veya bu iki biçimi bir arada kullanan istenen sayıda oyun nesnesi içerebilir.

Lastik oyun nesnelerini seçip <kbd>Scene ▸ Move Tool</kbd> seçeneğini seçerek yerlerine taşıyın. Nesneyi uygun bir noktaya taşımak için ok tutamaçlarını veya ortadaki yeşil kareyi tutun. Son olarak lastiklerin arabanın altında çizildiğinden emin olmamız gerekir. Bunu, konumun Z bileşenini -0.5 olarak ayarlayarak yaparız. Oyundaki her görsel öğe, Z değerine göre sıralanarak arkadan öne doğru çizilir. Z değeri 0 olan bir nesne, Z değeri -0.5 olan bir nesnenin üzerine çizilir. Araba oyun nesnesinin varsayılan Z değeri 0 olduğundan lastik nesnelerinin yeni değeri onları araba görüntüsünün altına yerleştirir.

![Tamamlanmış araba koleksiyonu](images/car/start_car_collection_complete.png)

## Araba betiği

Bulmacanın son parçası, arabayı kontrol edecek bir _betiktir_ (script). Betik, oyun nesnelerinin davranışlarını tanımlayan bir program içeren bileşendir. Betiklerle oyununuzun kurallarını ve nesnelerin çeşitli etkileşimlere (hem oyuncuyla hem de diğer nesnelerle) nasıl tepki vermesi gerektiğini belirleyebilirsiniz. Tüm betikler Lua programlama dilinde yazılır. Defold ile çalışabilmek için sizin veya ekibinizden birinin Lua ile programlamayı öğrenmesi gerekir.

*Assets bölmesinde* "main" klasörünü seçin, sağ tıklayıp <kbd>New ▸ Script File</kbd> seçeneğini seçin. Yeni dosyaya *car.script* adını verin; ardından *Outline* görünümünde "car" nesnesini seçip sağ tıklayın ve <kbd>Add Component File</kbd> seçeneğini seçerek dosyayı "car" oyun nesnesine ekleyin. *car.script* dosyasını seçin ve *OK* düğmesine tıklayın. Koleksiyon dosyasını kaydedin.

*car.script* dosyasını açmak için çift tıklayın.

::: sidenote
Defold, oyun mantığını kodlamak için çeşitli yaşam döngüsü işlevleri sağlar. Bunlar hakkında daha fazla bilgiyi [Betik kılavuzunda](/manuals/script) bulabilirsiniz.
:::

Bu öğreticide ihtiyaç duymayacağımız için önce `final`, `on_message` ve `on_reload` işlevlerini
kaldırın.

Ardından `init` işlevinin başlangıcından önce aşağıdaki kod satırlarını ekleyin.

```lua
-- Constants
local turn_speed = 0.1                           									  -- Slerp factor
local max_steer_angle_left = vmath.quat_rotation_z(math.pi / 6)     -- 30 degrees
local max_steer_angle_right = vmath.quat_rotation_z(-math.pi / 6)   -- -30 degrees
local steer_angle_zero = vmath.quat_rotation_z(0)									  -- Zero degrees
local wheels_vector = vmath.vector3(0, 72, 0)         		        	-- Vector from center of back and front wheel pairs

local acceleration = 100 																						-- The acceleration of the car

-- prehash the inputs
local left = hash("left")
local right = hash("right")
local accelerate = hash("accelerate")
local brake = hash("brake")
```

Burada yapılan değişiklikler oldukça basit; betiğimize, daha sonra arabamızın kodunu yazarken kullanacağımız bir dizi sabit (`constants`) ekledik.

::: sidenote
Karma değerlerini (hash) önceden değişkenlerde nasıl sakladığımıza dikkat edin. Bunu yapmak iyi bir uygulamadır; çünkü kodunuzu daha okunabilir ve performanslı hâle getirir.
:::

Ardından `init` işlevini aşağıdakileri içerecek şekilde düzenleyin:

```lua
function init(self)
	-- Send a message to the render script (see builtins/render/default.render_script) to set the clear color.
	-- This changes the background color of the game. The vector4 contains color information
	-- by channel from 0-1: Red = 0.2. Green = 0.2, Blue = 0.2 and Alpha = 1.0
	msg.post("@render:", "clear_color", { color = vmath.vector4(0.2, 0.2, 0.2, 1.0) } )		--<1>

	-- Acquire input focus so we can react to input
	msg.post(".", "acquire_input_focus")		-- <2>

	-- Some variables
	self.steer_angle = vmath.quat()				 -- <3>
	self.direction = vmath.quat()

	-- Velocity and acceleration are car relative (not rotated)
	self.velocity = vmath.vector3()
	self.acceleration = vmath.vector3()

	-- Input vector. This is modified later in the on_input function
	-- to store the input.
	self.input = vmath.vector3()
end
```

Az önce neleri değiştirdiğimizi merak ediyorsanız aşağıdaki açıklamaya bakın.

1. İşleme betiğimize, arka plan rengini gri olarak ayarlamasını isteyen bir ileti gönderiyoruz. İşleme betikleri, nesnelerin ekranda nasıl gösterileceğini kontrol eden özel Defold betikleridir.
2. Bir betik bileşeninde veya GUI betiğinde girdi eylemlerini dinlemek için bileşeni barındıran oyun nesnesine `acquire_input_focus` iletisinin gönderilmesi gerekir. Bu örnekte iletiyi araba betiğini barındıran oyun nesnesine gönderiyoruz.
3. Ardından arabamızın geçerli durumunu takip etmek için kullanacağımız bazı değişkenler tanımlıyoruz.

Kolaydı, değil mi? Şimdi `update` işlevini aşağıdakileri içerecek şekilde düzenleyerek devam edeceğiz:

```lua
function update(self, dt)
	-- Set acceleration to the y input
	self.acceleration.y = self.input.y * acceleration				-- <1>

	-- Calculate the new positions of front and back wheels
	local front_vel = vmath.rotate(self.steer_angle, self.velocity)
	local new_front_pos = vmath.rotate(self.direction, wheels_vector + front_vel)
	local new_back_pos = vmath.rotate(self.direction, self.velocity)								-- <2>

	-- Calculate the car's new direction
	local new_dir = vmath.normalize(new_front_pos - new_back_pos)
	self.direction = vmath.quat_rotation_z(math.atan2(new_dir.y, new_dir.x) - math.pi / 2)			-- <3>

	-- Calculate new velocity based on current acceleration
	self.velocity = self.velocity + self.acceleration * dt			-- <4>

	-- Update position based on current velocity and direction
	local pos = go.get_position()
	pos = pos + vmath.rotate(self.direction, self.velocity)
	go.set_position(pos)																			-- <5>

	-- Interpolate the wheels using vmath.slerp
	if self.input.x > 0 then																		-- <6>
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_right)
	elseif self.input.x < 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_left)
	else
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, steer_angle_zero)
	end

	-- Update the wheel rotation
	go.set_rotation(self.steer_angle, "left_wheel")					-- <7>
	go.set_rotation(self.steer_angle, "right_wheel")

	-- Set the game object's rotation to the direction
	go.set_rotation(self.direction)

	-- reset acceleration and input
	self.acceleration = vmath.vector3()								-- <8>
	self.input = vmath.vector3()
end
```

Bu oldukça büyük bir işlevdi! Ama endişelenmeyin; işte tüm bunların nasıl çalıştığı:

1. Önce ivme vektörümüzü girdi vektörümüze göre ayarlarız. Bu, arabanın ivmesinin girdi yönünde olmasını sağlar.
2. Ardından her iki tekerleğin yer değiştirmesi hesaplanır. Bunun dayandığı basit mantık şudur: arabanın arka tekerlekleri her zaman ileri doğru hareket ederken ön tekerlekler döndürüldükleri yönde hareket eder.
3. Her iki tekerleğin yer değiştirmesine göre arabamızın yeni hareket yönü hesaplanır.
4. Burada hesaplanan ivmeyi hıza ekleriz.
5. Son olarak arabanın konumunu geçerli hızımıza göre güncelleriz.
6. Sol/sağ girdimize göre direksiyon açısına küresel doğrusal ara değerleme (slerp) uygularız. Böylece girdi değiştiğinde tekerlekler aniden yeni açıya geçmez.
7. Ardından tekerleklerin dönmesi, arabanın geçerli direksiyon açısına göre ayarlanır. Benzer şekilde arabanın dönmesi de o anda hareket ettiği yöne göre ayarlanır.
8. Son olarak ivme ve girdi vektörlerini sıfırlarız.

Sonunda arabamızın girdiye tepki vermesini sağlamanın zamanı geldi. `on_input` işlevini şu şekilde güncelleyin:

```lua
function on_input(self, action_id, action)
	-- set the input vector to correspond to the key press
	if action_id == left then
		self.input.x = -1
	elseif action_id == right then
		self.input.x = 1
	elseif action_id == accelerate then
		self.input.y = 1
	elseif action_id == brake then
		self.input.y = -1
	end
end
```

Bu işlev aslında oldukça basit; yalnızca girdiyi alıp girdi vektörümüzü ayarlarız.

Düzenlemelerinizi kaydetmeyi unutmayın.

## Girdi

Henüz hiçbir girdi eylemi ayarlanmadı; şimdi bunu yapalım. */input/game.input_bindings* dosyasını açın ve "accelerate", "brake", "left" ve "right" için *key_trigger* girdi eşlemeleri (input binding) ekleyin. Bunları ok tuşlarına (KEY_LEFT, KEY_RIGHT, KEY_UP ve KEY_DOWN) eşliyoruz:

![Girdi eşlemeleri](images/car/start_input_bindings.png)

## Arabayı oyuna ekleme

Araba artık sürüşe hazır. Onu "car.collection" içinde oluşturduk, ancak henüz oyunda mevcut değil. Bunun nedeni, motorun şu anda başlatılırken "main.collection" dosyasını yüklemesidir. Bunu düzeltmek için *car.collection* dosyasını *main.collection* dosyasına eklememiz yeterlidir. *main.collection* dosyasını açın, *Outline* görünümünde kök "Collection" düğümünü seçin, sağ tıklayıp <kbd>Add Collection From File</kbd> seçeneğini seçin; ardından *car.collection* dosyasını seçip *OK* düğmesine tıklayın. Artık *car.collection* dosyasının içeriği, yeni örnekler olarak *main.collection* içine yerleştirilir. *car.collection* dosyasının içeriğini değiştirirseniz koleksiyonun her örneği oyun derlendiğinde otomatik olarak güncellenir.

![Araba koleksiyonunu ekleme](images/car/start_adding_car_collection.png)

Şimdi <kbd>Project ▸ Build</kbd> seçeneğini seçin ve yeni arabanızla bir tur atın!
Artık arabayı istediğiniz gibi hareket ettirebildiğinizi göreceksiniz. Ancak hâlâ yolunda gitmeyen bir şey var. Kontrolleri bıraktığınızda araba, durması gerektiği hâlde durmuyor. Şimdi bunu ekleme zamanı!

## Sürükleme kuvveti imdada yetişiyor

Gerçek dünyada bir nesne hareket ettiğinde sürükleme kuvveti (drag), nesnenin hareketine karşı koyarak yavaşlamasına neden olur. Bu kuvvet, hareketli nesnenin hızının karesiyle yaklaşık olarak orantılıdır ve dolayısıyla `D = k * |V| * V` olarak ifade edilebilir. Burada `k` bir sabit, `V` hız ve `|V|` hızın büyüklüğüdür (sürat). Bunu ekleyelim.

Betiğin başındaki sabitler bölümüne aşağıdaki sabiti ekleyin

```lua
local drag = 1.1	        --the drag constant <1>
```

Ardından `update` işlevinde bu satırın hemen üstüne aşağıdaki satırları ekleyin ve dosyayı kaydedin.

```lua
function update(self, dt)
	...
  -- Calculate new velocity based on current acceleration
	self.velocity = self.velocity + self.acceleration * dt
	...
end
```

```lua
function update(self, dt)
	...
	-- Speed is the magnitude of the velocity
	local speed = vmath.length_sqr(self.velocity)

	-- Apply drag
	self.acceleration = self.acceleration - speed * self.velocity * drag

	-- Stop if we are already slow enough
	if speed < 0.5 then self.velocity = vmath.vector3(0) end
	...
end
```

1. Sürükleme değerini sabit olarak tanımlayın.
2. Hareket ettiğimiz sürati hesaplayın.
3. Formüle göre geçerli ivmeye sürükleme kuvvetini uygulayın
4. Araba zaten yeterince yavaşsa durdurun.

## Araba betiğinin tamamı

Yukarıdaki adımları tamamladıktan sonra *car.script* dosyanız şöyle görünmelidir:

```lua
local turn_speed = 0.1                           				          	-- Slerp factor
local max_steer_angle_left = vmath.quat_rotation_z(math.pi / 6)	    -- 30 degrees
local max_steer_angle_right = vmath.quat_rotation_z(-math.pi / 6)   -- -30 degrees
local steer_angle_zero = vmath.quat_rotation_z(0)				          	-- Zero degrees
local wheels_vector = vmath.vector3(0, 72, 0)         				      -- Vector from center of back and front wheel pairs

local acceleration = 100 		                      									-- The acceleration of the car
local drag = 1.1                                                  	-- the drag constant

function init(self)
	-- Send a message to the render script (see builtins/render/default.render_script) to set the clear color.
	-- This changes the background color of the game. The vector4 contains color information
	-- by channel from 0-1: Red = 0.2. Green = 0.2, Blue = 0.2 and Alpha = 1.0
	msg.post("@render:", "clear_color", { color = vmath.vector4(0.2, 0.2, 0.2, 1.0) } )

	-- Acquire input focus so we can react to input
	msg.post(".", "acquire_input_focus")

	-- Some variables
	self.steer_angle = vmath.quat()
	self.direction = vmath.quat()

	-- Velocity and acceleration are car relative (not rotated)
	self.velocity = vmath.vector3()
	self.acceleration = vmath.vector3()

	-- Input vector. This is modified later in the on_input function
	-- to store the input.
	self.input = vmath.vector3()
end

function update(self, dt)
	-- Set acceleration to the y input
	self.acceleration.y = self.input.y * acceleration

	-- Calculate the new positions of front and back wheels
	local front_vel = vmath.rotate(self.steer_angle, self.velocity)
	local new_front_pos = vmath.rotate(self.direction, wheels_vector + front_vel)
	local new_back_pos = vmath.rotate(self.direction, self.velocity)

	-- Calculate the car's new direction
	local new_dir = vmath.normalize(new_front_pos - new_back_pos)
	self.direction = vmath.quat_rotation_z(math.atan2(new_dir.y, new_dir.x) - math.pi / 2)

	-- Speed is the magnitude of the velocity
	local speed = vmath.length(self.velocity)

	-- Apply drag
	self.acceleration = self.acceleration - speed * self.velocity * drag

	-- Stop if we are already slow enough
	if speed < 0.5 then self.velocity = vmath.vector3() end

	-- Calculate new velocity based on current acceleration
	self.velocity = self.velocity + self.acceleration * dt

	-- Update position based on current velocity and direction
	local pos = go.get_position()
	pos = pos + vmath.rotate(self.direction, self.velocity)
	go.set_position(pos)

	-- Interpolate the wheels using vmath.slerp
	if self.input.x > 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_right)
	elseif self.input.x < 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_left)
	else
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, steer_angle_zero)
	end

	-- Update the wheel rotation
	go.set_rotation(self.steer_angle, "left_wheel")
	go.set_rotation(self.steer_angle, "right_wheel")

	-- Set the game object's rotation to the direction
	go.set_rotation(self.direction)

	-- reset acceleration and input
	self.acceleration = vmath.vector3()
	self.input = vmath.vector3()
end

function on_input(self, action_id, action)
	-- set the input vector to correspond to the key press
	if action_id == hash("left") then
		self.input.x = -1
	elseif action_id == hash("right") then
		self.input.x = 1
	elseif action_id == hash("accelerate") then
		self.input.y = 1
	elseif action_id == hash("brake") then
		self.input.y = -1
	end
end
```

## Son hâliyle oyunu deneme

Şimdi ana menüden <kbd>Project ▸ Build</kbd> seçeneğini seçin ve yeni arabanızla bir tur atın!

Bu giriş öğreticisini tamamladık. İşte kendi başınıza çözmeyi deneyebileceğiniz bazı görevler:

1. Araba şu anda hem ileri hem de geri yönde aynı ivmeyle hareket ediyor. Bunu, araba geri giderken daha yavaş hareket edecek şekilde değiştirmek isteyebilirsiniz.
2. Bazı sabitleri (örneğin ivmeyi) özelliklere (`properties`) dönüştürerek arabanın farklı örnekleri için değiştirilebilmelerini sağlayın.
3. Arabanıza sesler ekleyin ve vınlasın! ([İpucu](/manuals/sound/))

Şimdi Defold'u keşfetmeye devam edin. Size yol göstermek için hazırladığımız pek çok [kılavuz ve öğretici](/learn) var; takıldığınızda sizi [forumda](//forum.defold.com) görmekten memnuniyet duyarız.

Defold ile keyifli çalışmalar!
