---
title: Defold'da Lua modülleri
brief: Lua modülleri, projenizi yapılandırmanıza ve yeniden kullanılabilir kütüphane kodu oluşturmanıza olanak tanır. Bu kılavuz, Defold'da bunun nasıl yapılacağını açıklar.
---

# Lua modülleri

Lua modülleri (Lua modules), projenizi yapılandırmanıza ve yeniden kullanılabilir kütüphane kodu oluşturmanıza olanak tanır. Projelerinizde kod tekrarından kaçınmak genellikle iyi bir fikirdir. Defold, Lua'nın modül özelliğini kullanarak betik (script) dosyalarını başka betik dosyalarına dahil etmenizi sağlar. Böylece işlevselliği (ve verileri) harici bir betik dosyasında kapsülleyerek oyun nesnesi (game object) ve GUI betik dosyalarında yeniden kullanabilirsiniz.

## Lua dosyalarını yükleme

Oyun projenizin dizin yapısında herhangi bir yerde bulunan `.lua` uzantılı dosyalarda saklanan Lua kodu, `require` ile betik ve GUI betik dosyalarına yüklenebilir. Yeni bir Lua modülü dosyası oluşturmak için *Assets* görünümünde dosyayı oluşturmak istediğiniz klasöre sağ tıklayın, ardından <kbd>New... ▸ Lua Module</kbd> seçeneğini seçin. Dosyaya benzersiz bir ad verin ve <kbd>Ok</kbd> düğmesine basın:

![yeni dosya](images/modules/new_name.png)

Aşağıdaki kodun "`main/anim.lua`" dosyasına eklendiğini varsayalım:

```lua
function direction_animation(direction, char)
    local d = ""
    if direction.x > 0 then
        d = "right"
    elseif direction.x < 0 then
        d = "left"
    elseif direction.y > 0 then
        d = "up"
    elseif direction.y < 0 then
        d = "down"
    end
    return hash(char .. "-" .. d)
end
```

Ardından herhangi bir betik bu dosyayı `require` ile yükleyip işlevi kullanabilir:

```lua
require "main.anim"

function update(self, dt)
    -- update position, set direction etc
    ...

    -- set animation
    local anim = direction_animation(self.dir, "player")
    if anim ~= self.current_anim then
        sprite.play_flipbook("#sprite", anim)
        self.current_anim = anim
    end
end
```

`require` işlevi, belirtilen modülü yükler. Önce modülün zaten yüklenmiş olup olmadığını belirlemek için `package.loaded` tablosuna bakar. Modül yüklenmişse `require`, `package.loaded[module_name]` konumunda saklanan değeri döndürür. Aksi takdirde dosyayı bir yükleyici aracılığıyla yükler ve değerlendirir.

`require` işlevine verilen dosya adı dizesinin sözdizimi biraz özeldir. Lua, dosya adı dizesindeki `.` karakterlerini yol ayırıcılarıyla değiştirir: macOS ve Linux'ta `/`, Windows'ta ise `\\` kullanılır.

Yukarıda yaptığımız gibi durum saklamak ve işlev tanımlamak için genel kapsamı (global scope) kullanmanın genellikle iyi bir fikir olmadığını unutmayın. Ad çakışmalarına yol açma, modülün durumunu dışarıya açma veya modülü kullanan kodlar arasında bağımlılık oluşturma riski vardır.

## Modüller

Lua, verileri ve işlevleri kapsüllemek için _modülleri_ kullanır. Lua modülü, işlevleri ve verileri içermek için kullanılan sıradan bir Lua tablosudur. Genel kapsamı kirletmemek için tablo yerel olarak tanımlanır:

```lua
local M = {}

-- private
local message = "Hello world!"

function M.hello()
    print(message)
end

return M
```

Ardından modül kullanılabilir. Burada da modülü yerel bir değişkene atamak tercih edilir:

```lua
local m = require "mymodule"
m.hello() --> "Hello world!"
```

## Modülleri çalışma sırasında yeniden yükleme

Basit bir modülü ele alalım:

```lua
-- module.lua
local M = {} -- creates a new table in the local scope
M.value = 4711
return M
```

Modülü kullanan kod ise şöyle olsun: 

```lua
local m = require "module"
print(m.value) --> "4711" (even if "module.lua" is changed and hot reloaded)
```

Modül dosyasını çalışma sırasında yeniden yüklerseniz (hot reload) kod yeniden çalıştırılır, ancak `m.value` değişmez. Bunun nedeni nedir?

İlk olarak, `module.lua` içindeki tablo yerel kapsamda (local scope) oluşturulur ve bu tabloya bir _başvuru_ modülü kullanan koda döndürülür. `module.lua` dosyasını yeniden yüklemek modül kodunu yeniden değerlendirir, ancak bu işlem `m` değişkeninin başvurduğu tabloyu güncellemek yerine yerel kapsamda yeni bir tablo oluşturur.

İkinci olarak Lua, `require` ile yüklenen dosyaları önbelleğe alır. Bir dosya ilk kez yüklendiğinde [`package.loaded`](/ref/package/#package.loaded) tablosuna yerleştirilir; böylece sonraki `require` çağrılarında daha hızlı okunabilir. Dosyanın tablodaki girdisini `nil` olarak ayarlayarak dosyanın diskten yeniden okunmasını zorlayabilirsiniz: `package.loaded["my_module"] = nil`.

Bir modülü çalışma sırasında doğru şekilde yeniden yüklemek için modülü yeniden yüklemeniz, önbelleği sıfırlamanız ve ardından modülü kullanan tüm dosyaları yeniden yüklemeniz gerekir. Bu, ideal bir çözüm olmaktan uzaktır.

Bunun yerine, _geliştirme sırasında_ kullanabileceğiniz bir geçici çözümü düşünebilirsiniz: modül tablosunu genel kapsama yerleştirin ve dosya her değerlendirildiğinde yeni bir tablo oluşturmak yerine `M` değişkeninin genel kapsamdaki tabloya başvurmasını sağlayın. Böylece modülü yeniden yüklemek genel kapsamdaki tablonun içeriğini değiştirir:

```lua
--- module.lua

-- Replace with local M = {} when done
uniquevariable12345 = uniquevariable12345 or {}
local M = uniquevariable12345

M.value = 4711
return M
```

## Modüller ve durum

Durum tutan (stateful) modüller, modülü kullanan tüm kodlar arasında paylaşılan bir iç durum saklar ve tek örnekli yapılara (singleton) benzetilebilir:

```lua
local M = {}

-- all users of the module will share this table
local state = {}

function M.do_something(foobar)
    table.insert(state, foobar)
end

return M
```

Durum tutmayan (stateless) bir modül ise herhangi bir iç durum saklamaz. Bunun yerine, durumu, modülü kullanan kodun yerel kapsamında bulunan ayrı bir tabloya taşıyan bir mekanizma sağlar. Bunu uygulamanın birkaç farklı yolu vardır:

Durum tablosu kullanma
: Belki de en kolay yaklaşım, yalnızca durum içeren yeni bir tablo döndüren bir yapıcı işlev kullanmaktır. Durum, durum tablosunu değiştiren her işlevin ilk parametresi olarak modüle açıkça aktarılır.

  ```lua
  local M = {}
  
  function M.alter_state(the_state, v)
      the_state.value = the_state.value + v
  end
  
  function M.get_state(the_state)
      return the_state.value
  end
  
  function M.new(v)
      local state = {
          value = v
      }
      return state
  end
  
  return M
  ```
  
  Modülü şu şekilde kullanın:
  
  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  m.alter_state(my_state, 1)
  print(m.get_state(my_state)) --> 43
  ```

Meta tablolar kullanma
: Bir diğer yaklaşım, meta tablolar (metatables) kullanarak her çağrıldığında durumu ve modülün dışarıya açık işlevlerini içeren yeni bir tablo döndüren bir yapıcı işlev kullanmaktır:

  ```lua
  local M = {}
  
  function M:alter_state(v)
      -- self is added as first argument when using : notation
      self.value = self.value + v
  end
  
  function M:get_state()
      return self.value
  end
  
  function M.new(v)
      local state = {
          value = v
      }
      return setmetatable(state, { __index = M })
  end
  
  return M
  ```

  Modülü şu şekilde kullanın:

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state:alter_state(1) -- "my_state" is added as first argument when using : notation
  print(my_state:get_state()) --> 43
  ```

Kapanışlar kullanma
:  Üçüncü bir yol, tüm durumu ve işlevleri içeren bir kapanış (closure) döndürmektir. Meta tablolar kullanılırken olduğu gibi örneği bir bağımsız değişken olarak (açıkça veya iki nokta üst üste işleciyle örtük olarak) aktarmak gerekmez. İşlev çağrılarının `__index` meta yöntemlerinden geçmesi gerekmediği için bu yöntem meta tablo kullanımından biraz daha hızlıdır; ancak her kapanış yöntemlerin kendi kopyasını içerdiğinden bellek tüketimi daha yüksektir.

  ```lua
  local M = {}
  
  function M.new(v)
      local state = {
          value = v
      }
  
      state.alter_state = function(v)
          state.value = state.value + v
      end
  
      state.get_state = function()
          return state.value
      end
  
      return state
  end
  
  return M
  ```

  Modülü şu şekilde kullanın:

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state.alter_state(1)
  print(my_state.get_state()) 
  ```
