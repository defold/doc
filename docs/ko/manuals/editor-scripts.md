---
title: 에디터 스크립트
brief: 이 매뉴얼은 Lua를 사용해 에디터를 확장하는 방법을 설명합니다.
---

# 에디터 스크립트 {#editor-scripts}

특수 확장자인 `.editor_script`를 가진 Lua 파일을 사용해 커스텀 메뉴 항목과 에디터 라이프사이클 훅을 만들 수 있습니다. 이 시스템을 사용하면 개발 워크플로우를 개선하도록 에디터를 조정할 수 있습니다.

## 에디터 스크립트 런타임 {#editor-script-runtime}

에디터 스크립트는 Java VM이 에뮬레이션하는 Lua VM 안에서 에디터 내부에서 실행됩니다. 모든 스크립트는 하나의 동일한 환경을 공유하므로 서로 상호작용할 수 있습니다. `.script` 파일과 마찬가지로 Lua 모듈을 `require`할 수 있지만, 에디터 내부에서 실행되는 Lua 버전은 다르므로 공유 코드가 호환되는지 확인해야 합니다. 에디터는 Lua 버전 5.2.x, 더 구체적으로 현재 JVM에서 Lua를 실행할 수 있는 유일하게 실용적인 솔루션인 [luaj](https://github.com/luaj/luaj) 런타임을 사용합니다. 그 외에도 몇 가지 제한사항이 있습니다.
- `debug` 패키지가 없습니다.
- `os.execute`가 없지만, 비슷한 `editor.execute()`를 제공합니다.
- `os.tmpname`과 `io.tmpfile`이 없습니다. 현재 에디터 스크립트는 프로젝트 디렉토리 안의 파일에만 액세스할 수 있습니다.
- 현재 `os.rename`은 없지만, 추가하고 싶습니다.
- `os.exit`과 `os.setlocale`이 없습니다.
- 에디터가 스크립트에서 즉시 응답을 받아야 하는 컨텍스트에서는 일부 오래 실행되는 함수를 사용할 수 없습니다. 자세한 내용은 [실행 모드](#execution-modes)를 참고하세요.

에디터 스크립트에 정의된 모든 에디터 익스텐션은 프로젝트를 열 때 로드됩니다. 라이브러리를 가져오면, 의존하는 라이브러리에 새 에디터 스크립트가 있을 수 있으므로 익스텐션이 다시 로드됩니다. 이 다시 로드 중에는 사용자가 자신의 에디터 스크립트를 수정하는 중일 수 있으므로, 자신의 에디터 스크립트 변경사항은 반영되지 않습니다. 이 스크립트들도 다시 로드하려면 **Project → Reload Editor Scripts** 명령을 실행해야 합니다.

## `.editor_script`의 구조 {#anatomy-of-editor_script}

모든 에디터 스크립트는 다음과 같이 모듈을 반환해야 합니다.
```lua
local M = {}

function M.get_commands()
  -- TODO - 에디터 커맨드 정의
end

function M.get_language_servers()
  -- TODO - 언어 서버 정의
end

function M.get_prefs_schema()
  -- TODO - preferences 정의
end

return M
```
그런 다음 에디터는 프로젝트와 라이브러리에 정의된 모든 에디터 스크립트를 수집하고, 하나의 Lua VM에 로드한 뒤 필요할 때 호출합니다. 자세한 내용은 [커맨드](#commands)와 [라이프사이클 훅](#lifecycle-hooks) 섹션을 참고하세요.

## 에디터 API {#editor-api}

다음 API를 정의하는 `editor` 패키지를 사용해 에디터와 상호작용할 수 있습니다.
- `editor.platform` — 문자열입니다. Windows의 경우 `"x86_64-win32"`, macOS의 경우 `"x86_64-macos"`, Linux의 경우 `"x86_64-linux"` 중 하나입니다.
- `editor.version` — Defold 버전 이름 문자열입니다. 예: `"1.4.8"`
- `editor.engine_sha1` — Defold 엔진의 SHA1 문자열입니다.
- `editor.editor_sha1` — Defold 에디터의 SHA1 문자열입니다.
- `editor.get(node_id, property)` — 에디터 안의 어떤 노드 값을 가져옵니다. 에디터의 노드는 스크립트 또는 컬렉션 파일, 컬렉션 안의 게임 오브젝트, 리소스로 로드된 json 파일 등 다양한 엔티티입니다. `node_id`는 에디터가 에디터 스크립트에 전달하는 userdata입니다. 또는 노드 id 대신 리소스 경로를 전달할 수 있습니다. 예: `"/main/game.script"`. `property`는 문자열입니다. 현재 지원되는 프로퍼티는 다음과 같습니다.
  - `"path"` — *resources*, 즉 파일이나 디렉토리로 존재하는 엔티티의 프로젝트 폴더 기준 파일 경로입니다. 반환값 예: `"/main/game.script"`
  - `"children"` — 디렉토리 리소스의 자식 리소스 경로 목록입니다.
  - `"text"` — 스크립트 파일이나 json처럼 텍스트로 편집할 수 있는 리소스의 텍스트 컨텐츠입니다. 반환값 예: `"function init(self)\nend"`. 파일을 저장하지 않은 채 편집할 수 있고, 이 편집 내용은 `"text"` 프로퍼티에 액세스할 때만 사용할 수 있으므로, 이는 `io.open()`으로 파일을 읽는 것과 같지 않다는 점에 주의하세요.
  - 아틀라스: `images`(아틀라스 안 이미지의 에디터 노드 목록)와 `animations`(애니메이션 노드 목록)
  - 아틀라스 애니메이션: `images`(아틀라스의 `images`와 동일)
  - 타일맵: `layers`(타일맵 안 레이어의 에디터 노드 목록)
  - 타일맵 레이어: `tiles`(무제한 2D 타일 그리드). 자세한 내용은 `tilemap.tiles.*`를 참고하세요.
  - particlefx: `emitters`(emitter 에디터 노드 목록)와 `modifiers`(modifier 에디터 노드 목록)
  - particlefx emitter: `modifiers`(modifier 에디터 노드 목록)
  - 충돌 오브젝트: `shapes`(충돌 shape 에디터 노드 목록)
  - GUI 파일: `layers`(레이어 에디터 노드 목록)
  - Outline 창에서 무언가를 선택했을 때 Properties 창에 표시되는 일부 프로퍼티입니다. 지원되는 outline 프로퍼티 타입은 다음과 같습니다.
    - `strings`
    - `booleans`
    - `numbers`
    - `vec2`/`vec3`/`vec4`
    - `resources`
    - `curves`
    이 프로퍼티 중 일부는 읽기 전용일 수 있고, 일부는 다른 컨텍스트에서 사용할 수 없을 수 있습니다. 따라서 읽기 전에 `editor.can_get`을 사용하고, 에디터가 설정하도록 하기 전에 `editor.can_set`을 사용해야 합니다. Properties 창에서 프로퍼티 이름 위에 마우스를 올리면 에디터 스크립트에서 이 프로퍼티가 어떤 이름을 가지는지 알려주는 tooltip을 볼 수 있습니다. 리소스 프로퍼티에는 `""` 값을 제공해 `nil`로 설정할 수 있습니다.
- `editor.can_get(node_id, property)` — 이 프로퍼티를 가져올 수 있는지 확인하여 `editor.get()`이 오류를 던지지 않게 합니다.
- `editor.can_set(node_id, property)` — 이 프로퍼티를 사용하는 `editor.tx.set()` 트랜잭션 단계가 오류를 던지지 않을지 확인합니다.
- `editor.create_directory(resource_path)` — 디렉토리가 없으면 생성하고, 존재하지 않는 모든 부모 디렉토리도 생성합니다.
- `editor.create_resources(resources)` — 템플릿 또는 커스텀 컨텐츠로 리소스를 1개 이상 생성합니다.
- `editor.delete_directory(resource_path)` — 디렉토리가 있으면 삭제하고, 존재하는 모든 자식 디렉토리와 파일도 삭제합니다.
- `editor.execute(cmd, [...args], [options])` — 쉘 명령을 실행하고, 선택적으로 출력을 캡처합니다.
- `editor.save()` — 저장되지 않은 모든 변경사항을 디스크에 유지합니다.
- `editor.transact(txs)` — `editor.tx.*` 함수로 생성한 트랜잭션 단계 1개 이상을 사용해 에디터의 메모리 내 상태를 수정합니다.
- `editor.ui.*` — 다양한 UI 관련 함수입니다. [UI 매뉴얼](/manuals/editor-scripts-ui)을 참고하세요.
- `editor.prefs.*` — 에디터 preferences와 상호작용하는 함수입니다. [preferences](#preferences)를 참고하세요.

전체 에디터 API 레퍼런스는 [여기](https://defold.com/ref/alpha/editor/)에서 확인할 수 있습니다.

## 커맨드 {#commands}

에디터 스크립트 모듈이 `get_commands` 함수를 정의하면, 이 함수는 익스텐션 다시 로드 시 호출됩니다. 반환된 커맨드는 에디터 안의 메뉴 바 또는 Assets 및 Outline 창의 컨텍스트 메뉴에서 사용할 수 있습니다. 예:
```lua
local M = {}

function M.get_commands()
  return {
    {
      label = "Remove Comments",
      locations = {"Edit", "Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        local path = editor.get(opts.selection, "path")
        return ends_with(path, ".lua") or ends_with(path, ".script")
      end,
      run = function(opts)
        local text = editor.get(opts.selection, "text")
        editor.transact({
          editor.tx.set(opts.selection, "text", strip_comments(text))
        })
      end
    },
    {
      label = "Minify JSON",
      locations = {"Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        return ends_with(editor.get(opts.selection, "path"), ".json")
      end,
      run = function(opts)
        local path = editor.get(opts.selection, "path")
        editor.execute("./scripts/minify-json.sh", path:sub(2))
      end
    }
  }
end

return M
```
에디터는 `get_commands()`가 각각 별도의 커맨드를 설명하는 테이블 배열을 반환하기를 기대합니다. 커맨드 설명은 다음으로 구성됩니다.

- `label`(필수) — 사용자에게 표시될 메뉴 항목의 텍스트입니다.
- `locations`(필수) — `"Edit"`, `"View"`, `"Project"`, `"Debug"`, `"Assets"`, `"Bundle"`, `"Scene"` 또는 `"Outline"` 중 하나로 이루어진 배열입니다. 이 커맨드를 사용할 수 있어야 하는 위치를 설명합니다. `"Edit"`, `"View"`, `"Project"`, `"Debug"`는 상단의 메뉴 바를 의미하고, `"Assets"`는 Assets pane 창의 컨텍스트 메뉴, `"Outline"`은 Outline 창의 컨텍스트 메뉴, `"Bundle"`은 **Project → Bundle** 하위 메뉴를 의미합니다.
- `query` — 커맨드가 에디터에 관련 정보를 요청하고 어떤 데이터에 작동하는지 정의하는 방법입니다. `query` 테이블의 각 키마다 `active`와 `run` 콜백이 인자로 받는 `opts` 테이블에 대응하는 키가 생깁니다. 지원되는 키는 다음과 같습니다.
  - `selection`은 무언가가 선택되어 있을 때 이 커맨드가 유효하고, 이 선택 항목에 대해 동작한다는 뜻입니다.
    - `type`은 커맨드가 관심을 가지는 선택된 노드의 타입입니다. 현재 허용되는 타입은 다음과 같습니다.
      - `"resource"` — Assets와 Outline에서 resource는 대응하는 파일이 있는 선택 항목입니다. 메뉴 바(Edit 또는 View)에서 resource는 현재 열려 있는 파일입니다.
      - `"outline"` — Outline에 표시할 수 있는 무언가입니다. Outline에서는 선택된 항목이고, 메뉴 바에서는 현재 열려 있는 파일입니다.
      - `"scene"` — Scene에 렌더링할 수 있는 무언가입니다.
    - `cardinality`는 선택된 항목이 몇 개여야 하는지 정의합니다. `"one"`이면 커맨드 콜백에 전달되는 selection은 단일 노드 id입니다. `"many"`이면 커맨드 콜백에 전달되는 selection은 하나 이상의 노드 id 배열입니다.
  - `argument` — 커맨드 인자입니다. 현재는 `"Bundle"` 위치의 커맨드만 인자를 받으며, bundle 커맨드를 명시적으로 선택한 경우 `true`, rebundle인 경우 `false`입니다.
- `id` - 커맨드 식별자 문자열입니다. 예를 들어 마지막으로 사용한 bundle 커맨드를 `prefs`에 유지하는 데 사용됩니다.
- `active` - 커맨드가 활성 상태인지 확인하기 위해 실행되는 콜백이며, boolean을 반환해야 합니다. `locations`에 `"Assets"`, `"Scene"` 또는 `"Outline"`이 포함되어 있으면 컨텍스트 메뉴를 표시할 때 `active`가 호출됩니다. locations에 `"Edit"` 또는 `"View"`가 포함되어 있으면 키보드 입력이나 마우스 클릭 같은 모든 사용자 상호작용마다 active가 호출되므로, `active`는 비교적 빠르게 실행되도록 해야 합니다.
- `run` - 사용자가 메뉴 항목을 선택했을 때 실행되는 콜백입니다.

### 커맨드로 메모리 내 에디터 상태 변경하기 {#use-commands-to-change-the-in-memory-editor-state}

`run` 핸들러 안에서는 메모리 내 에디터 상태를 조회하고 변경할 수 있습니다. 조회는 `editor.get()` 함수를 사용해 수행하며, 이 함수로 에디터에 파일과 선택 항목의 현재 상태를 물어볼 수 있습니다(`query = {selection = ...}`를 사용하는 경우). 스크립트 파일의 `"text"` 프로퍼티를 가져올 수 있고, Properties 창에 표시되는 일부 프로퍼티도 가져올 수 있습니다. 프로퍼티 이름 위에 마우스를 올리면 에디터 스크립트에서 이 프로퍼티가 어떤 이름을 가지는지 알려주는 tooltip을 볼 수 있습니다. 에디터 상태 변경은 `editor.transact()`를 사용해 수행하며, 하나의 실행 취소 가능한 단계 안에 수정 1개 이상을 묶습니다. 예를 들어 게임 오브젝트의 transform을 reset할 수 있게 하고 싶다면 다음과 같은 커맨드를 작성할 수 있습니다.
```lua
{
  label = "Reset transform",
  locations = {"Outline"},
  query = {selection = {type = "outline", cardinality = "one"}},
  active = function(opts)
    local node = opts.selection
    return editor.can_set(node, "position")
       and editor.can_set(node, "rotation")
       and editor.can_set(node, "scale")
  end,
  run = function(opts)
    local node = opts.selection
    editor.transact({
      editor.tx.set(node, "position", {0, 0, 0}),
      editor.tx.set(node, "rotation", {0, 0, 0}),
      editor.tx.set(node, "scale", {1, 1, 1})
    })
  end
}
```

#### 아틀라스 편집 {#editing-atlases}

아틀라스의 프로퍼티를 읽고 쓰는 것 외에도, 아틀라스 이미지와 애니메이션을 읽고 수정할 수 있습니다. 아틀라스는 `images`와 `animations` node list 프로퍼티를 정의하고, 애니메이션은 `images` node list 프로퍼티를 정의합니다. 이 프로퍼티에는 `editor.tx.add`, `editor.tx.remove`, `editor.tx.clear` 트랜잭션 단계를 사용할 수 있습니다.

예를 들어 아틀라스에 이미지를 추가하려면 커맨드의 `run` 핸들러에서 다음 코드를 실행합니다.
```lua
editor.transact({
    editor.tx.add("/main.atlas", "images", {image="/assets/hero.png"})
})
```
아틀라스 안의 모든 이미지 집합을 찾으려면 다음 코드를 실행합니다.
```lua
local all_images = {} ---@type table<string, true>
-- 먼저 직접 등록된 이미지를 모두 수집합니다.
local image_nodes = editor.get("/main.atlas", "images")
for i = 1, #image_nodes do
    all_images[editor.get(image_nodes[i], "image")] = true
end
-- 두 번째로, 애니메이션에 사용된 이미지를 모두 수집합니다.
local animation_nodes = editor.get("/main.atlas", "animations")
for i = 1, #animation_nodes do
    local animation_image_nodes = editor.get(animation_nodes[i], "images")
    for j = 1, #animation_image_nodes do
        all_images[editor.get(animation_image_nodes[j], "image")] = true
    end
end
pprint(all_images)
-- {
--     ["/assets/hero.png"] = true,
--     ["/assets/enemy.png"] = true,
-- }}
```
아틀라스의 모든 애니메이션을 교체하려면 다음과 같이 합니다.
```lua
editor.transact({
    editor.tx.clear("/main.atlas", "animations"),
    editor.tx.add("/main.atlas", "animations", {
        id = "hero_run",
        images = {
            {image = "/assets/hero_run_1.png"},
            {image = "/assets/hero_run_2.png"},
            {image = "/assets/hero_run_3.png"},
            {image = "/assets/hero_run_4.png"}
        }
    })
})
```

#### tilesource 편집 {#editing-tilesources}

outline 프로퍼티 외에도 tilesource는 다음 프로퍼티를 정의합니다.
- `animations` - tilesource의 애니메이션 노드 목록입니다.
- `collision_groups` - tilesource의 충돌 그룹 노드 목록입니다.
- `tile_collision_groups` - tilesource 안 타일에 대한 충돌 그룹 할당 테이블입니다.

예를 들어 tilesource를 설정하는 방법은 다음과 같습니다.
```lua
local tilesource = "/game/world.tilesource"
editor.transact({
    editor.tx.add(tilesource, "animations", {id = "idle", start_tile = 1, end_tile = 1}),
    editor.tx.add(tilesource, "animations", {id = "walk", start_tile = 2, end_tile = 6, fps = 10}),
    editor.tx.add(tilesource, "collision_groups", {id = "player"}),
    editor.tx.add(tilesource, "collision_groups", {id = "obstacle"}),
    editor.tx.set(tilesource, "tile_collision_groups", {
        [1] = "player",
        [7] = "obstacle",
        [8] = "obstacle"
    })
})
```

#### 타일맵 편집 {#editing-tilemaps}

타일맵은 타일맵 레이어의 node list인 `layers` 프로퍼티를 정의합니다. 각 레이어도 이 레이어의 무제한 2D 타일 그리드를 담는 `tiles` 프로퍼티를 정의합니다. 이는 엔진과 다릅니다. 타일은 경계가 없고 음수 좌표를 포함해 어디든 추가될 수 있습니다. 타일을 편집하기 위해 에디터 스크립트 API는 다음 함수를 가진 `tilemap.tiles` 모듈을 정의합니다.
- `tilemap.tiles.new()`는 무제한 2D 타일 그리드를 담는 새 데이터 구조를 생성합니다. 에디터에서는 엔진과 달리 타일맵이 무제한이며 좌표가 음수일 수 있습니다.
- `tilemap.tiles.get_tile(tiles, x, y)`는 특정 좌표의 타일 인덱스를 가져옵니다.
- `tilemap.tiles.get_info(tiles, x, y)`는 특정 좌표의 전체 타일 정보를 가져옵니다. 데이터 형태는 엔진의 `tilemap.get_tile_info` 함수와 같습니다.
- `tilemap.tiles.iterator(tiles)`는 타일맵의 모든 타일을 순회하는 iterator를 생성합니다.
- `tilemap.tiles.clear(tiles)`는 타일맵에서 모든 타일을 제거합니다.
- `tilemap.tiles.set(tiles, x, y, tile_or_info)`는 특정 좌표에 타일을 설정합니다.
- `tilemap.tiles.remove(tiles, x, y)`는 특정 좌표에서 타일을 제거합니다.

예를 들어 전체 타일맵의 내용을 출력하는 방법은 다음과 같습니다.
```lua
local layers = editor.get("/level.tilemap", "layers")
for i = 1, #layers do
    local layer = layers[i]
    local id = editor.get(layer, "id")
    local tiles = editor.get(layer, "tiles")
    print("layer " .. id .. ": {")
    for x, y, tile in tilemap.tiles.iterator(tiles) do
        print("  [" .. x .. ", " .. y .. "] = " .. tile)
    end
    print("}")
end
```

타일맵에 타일이 있는 레이어를 추가하는 방법을 보여주는 예는 다음과 같습니다.
```lua
local tiles = tilemap.tiles.new()
tilemap.tiles.set(tiles, 1, 1, 2)
editor.transact({
    editor.tx.add("/level.tilemap", "layers", {
        id = "new_layer",
        tiles = tiles
    })
})
```

#### particlefx 편집 {#editing-particlefx}

`modifiers`와 `emitters` 프로퍼티를 사용해 particlefx를 편집할 수 있습니다. 예를 들어 acceleration modifier가 있는 circle emitter를 추가하는 작업은 다음과 같이 수행합니다.
```lua
editor.transact({
    editor.tx.add("/fire.particlefx", "emitters", {
        type = "emitter-type-circle",
        modifiers = {
          {type = "modifier-type-acceleration"}
        }
    })
})
```
많은 particlefx 프로퍼티는 커브 또는 커브 스프레드(즉 커브 + 어떤 randomizer 값)입니다. 커브는 비어 있지 않은 `points` 목록이 있는 테이블로 표현되며, 각 point는 다음 프로퍼티를 가진 테이블입니다.
- `x` - point의 x 좌표이며, 0에서 시작해 1에서 끝나야 합니다.
- `y` - point의 값입니다.
- `tx`(0에서 1)와 `ty`(-1에서 1) - point의 tangent입니다. 예를 들어 80도 각도의 경우 `tx`는 `math.cos(math.rad(80))`, `ty`는 `math.sin(math.rad(80))`여야 합니다.
커브 스프레드에는 추가로 `spread` 숫자형 프로퍼티가 있습니다.

예를 들어 이미 존재하는 emitter에 파티클 lifetime alpha 커브를 설정하는 코드는 다음과 같을 수 있습니다.
```lua
local emitter = editor.get("/fire.particlefx", "emitters")[1]
editor.transact({
    editor.tx.set(emitter, "particle_key_alpha", { points = {
        {x = 0,   y = 0, tx = 0.1, ty = 1}, -- 0에서 시작해 빠르게 올라갑니다.
        {x = 0.2, y = 1, tx = 1,   ty = 0}, -- lifetime의 20% 지점에서 1에 도달합니다.
        {x = 1,   y = 0, tx = 1,   ty = 0}  -- 천천히 0으로 내려갑니다.
    }})
})
```
물론 emitter를 생성할 때 테이블 안에서 `particle_key_alpha` 키를 사용할 수도 있습니다. 또한 "static" 커브를 표현하기 위해 단일 숫자를 대신 사용할 수도 있습니다.

#### 충돌 오브젝트 편집 {#editing-collision-objects}

기본 outline 프로퍼티 외에도, 충돌 오브젝트는 `shapes` node list 프로퍼티를 정의합니다. 새 충돌 shape 추가는 다음과 같이 수행합니다.
```lua
editor.transact({
    editor.tx.add("/hero.collisionobject", "shapes", {
        type = "shape-type-box" -- 또는 "shape-type-sphere", "shape-type-capsule"
    })
})
```
Shape의 `type` 프로퍼티는 생성 중에 필수이며, shape가 추가된 뒤에는 변경할 수 없습니다. shape 타입은 3가지입니다.
- `shape-type-box` - `dimensions` 프로퍼티가 있는 box shape
- `shape-type-sphere` - `diameter` 프로퍼티가 있는 sphere shape
- `shape-type-capsule` - `diameter`와 `height` 프로퍼티가 있는 capsule shape

#### GUI 파일 편집 {#editing-gui-files}

outline 프로퍼티 외에도, GUI 노드는 다음 프로퍼티를 정의합니다.
- `layers` — 레이어 에디터 노드 목록입니다(순서 변경 가능).
- `materials` — 메터리얼 에디터 노드 목록입니다.

에디터의 `layers` 프로퍼티를 사용해 GUI 레이어를 편집할 수 있습니다. 예:
```lua
editor.transact({
    editor.tx.add("/main.gui", "layers", {name = "foreground"}),
    editor.tx.add("/main.gui", "layers", {name = "background"})
})
```
추가로 레이어 순서를 변경할 수 있습니다.
```lua
local fg, bg = table.unpack(editor.get("/main.gui", "layers"))
editor.transact({
    editor.tx.reorder("/main.gui", "layers", {bg, fg})
})
```
마찬가지로 폰트, 메터리얼, 텍스쳐, particlefx는 `fonts`, `materials`, `textures`, `particlefxs` 프로퍼티를 사용해 편집합니다.
```lua
editor.transact({
    editor.tx.add("/main.gui", "fonts", {font = "/main.font"}),
    editor.tx.add("/main.gui", "materials", {name = "shine", material = "/shine.material"}),
    editor.tx.add("/main.gui", "particlefxs", {particlefx = "/confetti.material"}),
    editor.tx.add("/main.gui", "textures", {texture = "/ui.atlas"})
})
```
이 프로퍼티는 순서 변경을 지원하지 않습니다.

마지막으로 `nodes` list 프로퍼티를 사용해 GUI 노드를 편집할 수 있습니다. 예:
```lua
editor.transact({
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-box",
        position = {20, 20, 20}
    }),
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-template",
        template = "/button.gui"
    }),
})
```
내장 노드 타입은 다음과 같습니다.
- `gui-node-type-box`
- `gui-node-type-particlefx`
- `gui-node-type-pie`
- `gui-node-type-template`
- `gui-node-type-text`

spine extension을 사용하고 있다면 `gui-node-type-spine` 노드 타입도 사용할 수 있습니다.

GUI 파일이 레이아웃을 정의하면, `layout:property` 문법을 사용해 레이아웃에서 값을 가져오고 설정할 수 있습니다. 예:
```lua
local node = editor.get("/main.gui", "nodes")[1]

-- GET:
local position = editor.get(node, "position")
pprint(position) -- {20, 20, 20}
local landscape_position = editor.get(node, "Landscape:position")
pprint(landscape_position) -- {20, 20, 20}

-- SET:
editor.transact({
    editor.tx.set(node, "Landscape:position", {30, 30, 30})
})
pprint(editor.get(node, "Landscape:position")) -- {30, 30, 30}
```

설정된 layout 프로퍼티는 `editor.tx.reset`을 사용해 기본값으로 reset할 수 있습니다.
```lua
print(editor.can_reset(node, "Landscape:position")) -- true
editor.transact({
    editor.tx.reset(node, "Landscape:position")
})
```
Template 노드 트리는 읽을 수 있지만 편집할 수는 없습니다. template 노드 트리의 노드 프로퍼티만 설정할 수 있습니다.
```lua
local template = editor.get("/main.gui", "nodes")[2]
print(editor.can_add(template, "nodes")) -- false
local node_in_template = editor.get(template, "nodes")[1]
editor.transact({
    editor.tx.set(node_in_template, "text", "Button text")
})
print(editor.can_reset(node_in_template, "text")) -- true (template의 값을 오버라이드합니다.)
```

#### 게임 오브젝트 편집 {#editing-game-objects}

에디터 스크립트를 사용해 게임 오브젝트 파일의 컴포넌트를 편집할 수 있습니다. 컴포넌트는 referenced와 embedded라는 2가지 종류가 있습니다. Referenced 컴포넌트는 `component-reference` 타입을 사용하고 다른 리소스에 대한 참조처럼 동작하며, 스크립트에 정의된 go 프로퍼티의 오버라이드만 허용합니다. Embedded 컴포넌트는 `sprite`, `label` 같은 타입을 사용하고, 컴포넌트 타입에 정의된 모든 프로퍼티 편집뿐 아니라 충돌 오브젝트의 shape 같은 서브 컴포넌트 추가도 허용합니다. 예를 들어 다음 코드를 사용해 게임 오브젝트를 설정할 수 있습니다.
```lua
editor.transact({
    editor.tx.add("/npc.go", "components", {
        type = "sprite",
        id = "view"
    }),
    editor.tx.add("/npc.go", "components", {
        type = "collisionobject",
        id = "collision",
        shapes = {
            {
                type = "shape-type-box",
                dimensions = {32, 32, 32}
            }
        }
    }),
    editor.tx.add("/npc.go", "components", {
        type = "component-reference",
        path = "/npc.script"
        id = "controller",
        __hp = 100 -- 스크립트에 정의된 go 프로퍼티 설정
    })
})
```

#### 컬렉션 편집 {#editing-collections}
에디터 스크립트를 사용해 컬렉션을 편집할 수 있습니다. 게임 오브젝트(embedded 또는 referenced)와 컬렉션(referenced)을 추가할 수 있습니다. 예:
```lua
local coll = "/char.collection"
editor.transact({
    editor.tx.add(coll, "children", {
        -- embedded 게임 오브젝트
        type = "go",
        id = "root",
        children = {
            {
                -- referenced 게임 오브젝트
                type = "go-reference",
                path = "/char-view.go"
                id = "view"
            },
            {
                -- referenced 컬렉션
                type = "collection-reference",
                path = "/body-attachments.collection"
                id = "attachments"
            }
        },
        -- embedded go는 컴포넌트도 가질 수 있습니다.
        components = {
            {
                type = "collisionobject",
                id = "collision",
                shapes = {
                    {type = "shape-type-box", dimensions = {2.5, 2.5, 2.5}}
                }
            },
            {
                type = "component-reference",
                id = "controller",
                path = "/char.script",
                __hp = 100 -- 스크립트에 정의된 go 프로퍼티 설정
            }
        }
    })
})
```

에디터에서와 마찬가지로, referenced 컬렉션은 편집 중인 컬렉션의 루트에만 추가할 수 있고, 게임 오브젝트는 embedded 또는 referenced 게임 오브젝트에만 추가할 수 있으며, referenced 컬렉션이나 이 referenced 컬렉션 안의 게임 오브젝트에는 추가할 수 없습니다.

### 쉘 명령 사용 {#use-shell-commands}

`run` 핸들러 안에서는 파일에 쓸 수 있고(`io` 모듈 사용), 쉘 명령을 실행할 수 있습니다(`editor.execute()` 명령 사용). 쉘 명령을 실행할 때는 쉘 명령의 출력을 문자열로 캡처한 뒤 코드에서 사용할 수 있습니다. 예를 들어 전역으로 설치된 [`jq`](https://jqlang.github.io/jq/)에 shell out하는 JSON 포맷팅 커맨드를 만들고 싶다면 다음 커맨드를 작성할 수 있습니다.
```lua
{
  label = "Format JSON",
  locations = {"Assets"},
  query = {selection = {type = "resource", cardinality = "one"}},
  action = function(opts)
    local path = editor.get(opts.selection, "path")
    return path:match(".json$") ~= nil
  end,
  run = function(opts)
    local text = editor.get(opts.selection, "text")
    local new_text = editor.execute("jq", "-n", "--argjson", "data", text, "$data", {
      reload_resources = false, -- jq는 디스크를 건드리지 않으므로 리소스를 다시 로드하지 않습니다.
      out = "capture" -- 아무것도 반환하지 않는 대신 텍스트 출력을 반환합니다.
    })
    editor.transact({ editor.tx.set(opts.selection, "text", new_text) })
  end
}
```
이 커맨드는 쉘 프로그램을 읽기 전용 방식으로 호출하고(`reload_resources = false`를 사용해 이를 에디터에 알림), 따라서 이 작업을 실행 취소 가능하게 만들 수 있다는 이점이 있습니다.

::: sidenote
에디터 스크립트를 라이브러리로 배포하고 싶다면, 의존성 안에 에디터 플랫폼용 바이너리 프로그램을 번들로 포함하고 싶을 수 있습니다. 방법에 대한 자세한 내용은 [라이브러리의 에디터 스크립트](#editor-scripts-in-libraries)를 참고하세요.
:::

## 라이프사이클 훅 {#lifecycle-hooks}

특별하게 처리되는 에디터 스크립트 파일이 하나 있습니다. `hooks.editor_script`이며, 프로젝트 루트에서 *game.project*와 같은 디렉토리에 위치합니다. 오직 이 에디터 스크립트만 에디터에서 라이프사이클 이벤트를 받습니다. 이러한 파일의 예:
```lua
local M = {}

function M.on_build_started(opts)
  local file = io.open("assets/build.json", "w")
  file:write('{"build_time": "' .. os.date() .. '"}')
  file:close()
end

return M
```
라이프사이클 훅을 단일 에디터 스크립트 파일로 제한하기로 한 이유는, build hook이 발생하는 순서가 다른 build step을 추가하기 쉬운지보다 더 중요하기 때문입니다. 커맨드는 서로 독립적이므로 메뉴에 표시되는 순서는 실제로 중요하지 않습니다. 결국 사용자는 자신이 선택한 특정 커맨드를 실행합니다. 서로 다른 에디터 스크립트에서 build hook을 지정할 수 있다면 문제가 생깁니다. hook은 어떤 순서로 실행되어야 할까요? 아마 컨텐츠를 압축한 뒤 checksum을 만들고 싶을 것입니다... 그리고 각 step 함수를 명시적으로 호출해 build step의 순서를 정하는 단일 파일을 두는 것이 이 문제를 해결하는 방법입니다.

`/hooks.editor_script`가 지정할 수 있는 기존 라이프사이클 훅은 다음과 같습니다.
- `on_build_started(opts)` — Project Build 또는 Debug Start 옵션을 사용해 게임을 로컬 또는 어떤 원격 타겟에서 실행하도록 Built할 때 실행됩니다. 변경사항은 빌드된 게임에 나타납니다. 이 hook에서 오류를 발생시키면 빌드가 중단됩니다. `opts`는 다음 키를 포함하는 테이블입니다.
  - `platform` — 어떤 플랫폼용으로 빌드되는지를 설명하는 `%arch%-%os%` 형식의 문자열입니다. 현재는 항상 `editor.platform`과 같은 값입니다.
- `on_build_finished(opts)` — 빌드가 성공했든 실패했든 빌드가 끝나면 실행됩니다. `opts`는 다음 키를 가진 테이블입니다.
  - `platform` — `on_build_started`와 동일합니다.
  - `success` — 빌드가 성공했는지 여부이며, `true` 또는 `false`입니다.
- `on_bundle_started(opts)` — 번들을 만들거나 게임의 HTML5 버전을 Build할 때 실행됩니다. `on_build_started`와 마찬가지로, 이 hook이 트리거한 변경사항은 번들에 나타나고, 오류는 번들을 중단시킵니다. `opts`는 다음 키를 가집니다.
  - `output_directory` — bundle 출력이 있는 디렉토리를 가리키는 파일 경로입니다. 예: `"/path/to/project/build/default/__htmlLaunchDir"`
  - `platform` — 게임이 번들되는 플랫폼입니다. 가능한 플랫폼 값 목록은 [Bob 매뉴얼](/manuals/bob)을 참고하세요.
  - `variant` — bundle variant이며, `"debug"`, `"release"` 또는 `"headless"` 중 하나입니다.
- `on_bundle_finished(opts)` — 번들이 성공했든 아니든 번들이 끝나면 실행됩니다. `opts`는 `on_bundle_started`의 `opts`와 같은 데이터를 가진 테이블이며, 빌드가 성공했는지 나타내는 `success` 키가 추가됩니다.
- `on_target_launched(opts)` — 사용자가 게임을 실행하고 게임이 성공적으로 시작되면 실행됩니다. `opts`는 실행된 엔진 서비스를 가리키는 `url` 키를 포함합니다. 예: `"http://127.0.0.1:35405"`
- `on_target_terminated(opts)` — 실행된 게임이 닫히면 실행되며, `on_target_launched`와 같은 opts를 가집니다.

현재 라이프사이클 훅은 에디터 전용 기능이며, 커맨드 라인에서 번들링할 때 Bob이 실행하지 않는다는 점에 주의하세요.

## 언어 서버(Language server) {#language-servers}

에디터는 [Language Server Protocol](https://microsoft.github.io/language-server-protocol/)의 일부를 지원합니다. 향후 에디터의 LSP 기능 지원을 확장하는 것을 목표로 하지만, 현재는 편집 중인 파일에 diagnostics(즉 lint)를 표시하고 completions를 제공하는 것만 가능합니다.

언어 서버(language server)를 정의하려면 다음과 같이 에디터 스크립트의 `get_language_servers` 함수를 편집해야 합니다.

```lua
function M.get_language_servers()
  local command = 'build/plugins/my-ext/plugins/bin/' .. editor.platform .. '/lua-lsp'
  if editor.platform == 'x86_64-win32' then
    command = command .. '.exe'
  end
  return {
    {
      languages = {'lua'},
      watched_files = {
        { pattern = '**/.luacheckrc' }
      },
      command = {command, '--stdio'}
    }
  }
end
```
에디터는 지정된 `command`를 사용해 언어 서버를 시작하고, 서버 프로세스의 표준 입력과 출력을 통신에 사용합니다.

언어 서버 정의 테이블은 다음을 지정할 수 있습니다.
- `languages`(필수) — 서버가 관심을 가지는 언어 목록입니다. [여기](https://code.visualstudio.com/docs/languages/identifiers#_known-language-identifiers)에 정의되어 있습니다(파일 확장자도 동작합니다).
- `command`(필수) - 명령과 그 인자의 배열입니다.
- `watched_files` - `pattern` 키(glob)를 가진 테이블 배열입니다. 서버의 [watched files changed](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWatchedFiles) 알림을 트리거합니다.

## HTTP 서버 {#http-server}

실행 중인 에디터 인스턴스마다 HTTP 서버가 실행됩니다. 이 서버는 에디터 스크립트를 사용해 확장할 수 있습니다. 에디터 HTTP 서버를 확장하려면 `get_http_server_routes` 에디터 스크립트 함수를 추가해야 합니다. 이 함수는 추가 route를 반환해야 합니다.
```lua
print("My route: " .. http.server.url .. "/my-extension")

function M.get_http_server_routes()
  return {
    http.server.route("/my-extension", "GET", function(request)
      return http.server.response(200, "Hello world!")
    end)
  }
end
```
에디터 스크립트를 다시 로드하면 콘솔에 다음 출력이 표시됩니다. `My route: http://0.0.0.0:12345/my-extension`. 브라우저에서 이 링크를 열면 `"Hello world!"` 메세지가 표시됩니다.

입력 `request` 인자는 요청에 대한 정보를 담은 단순한 Lua 테이블입니다. `path`(`/`로 시작하는 URL path segment), 요청 `method`(예: `"GET"`), `headers`(소문자 헤더 이름을 가진 테이블), 그리고 선택적으로 `query`(query string)와 `body`(route가 body를 해석하는 방법을 정의한 경우) 같은 키를 포함합니다. 예를 들어 JSON body를 받는 route를 만들고 싶다면 `"json"` converter 파라미터로 정의합니다.
```lua
http.server.route("/my-extension/echo-request", "POST", "json", function(request)
  return http.server.json_response(request)
end)
```
커맨드 라인에서 `curl`과 `jq`를 사용해 이 endpoint를 테스트할 수 있습니다.
```sh
curl 'http://0.0.0.0:12345/my-extension/echo-request?q=1' -X POST --data '{"input": "json"}' | jq
{
  "path": "/my-extension/echo-request",
  "method": "POST",
  "query": "q=1",
  "headers": {
    "host": "0.0.0.0:12345",
    "content-type": "application/x-www-form-urlencoded",
    "accept": "*/*",
    "user-agent": "curl/8.7.1",
    "content-length": "17"
  },
  "body": {
    "input": "json"
  }
}
```
Route path는 요청 path에서 추출해 request의 일부로 handler 함수에 제공할 수 있는 패턴을 지원합니다. 예:
```lua
http.server.route("/my-extension/setting/{category}.{key}", function(request)
  return http.server.response(200, tostring(editor.get("/game.project", request.category .. "." .. request.key)))
end)
```
이제 예를 들어 `http://0.0.0.0:12345/my-extension/setting/project.title`을 열면 `/game.project` 파일에서 가져온 게임 title이 표시됩니다.

단일 segment path 패턴 외에도 `{*name}` 문법을 사용해 URL path의 나머지와 매칭할 수 있습니다. 예를 들어 프로젝트 루트에서 파일을 제공하는 간단한 파일 서버 endpoint는 다음과 같습니다.
```lua
http.server.route("/my-extension/files/{*file}", function(request)
  local attrs = editor.external_file_attributes(request.file)
  if attrs.is_file then
    return http.server.external_file_response(request.file)
  else
    return 404
  end
end)
```
이제 예를 들어 브라우저에서 `http://0.0.0.0:12345/my-extension/files/main/main.collection`을 열면 `main/main.collection` 파일의 내용이 표시됩니다.

## 라이브러리의 에디터 스크립트 {#editor-scripts-in-libraries}

다른 사람이 사용할 수 있도록 커맨드가 포함된 라이브러리를 publish할 수 있으며, 에디터가 자동으로 이를 선택합니다. 반면 hook은 자동으로 선택될 수 없습니다. hook은 프로젝트의 루트 폴더에 있는 파일에 정의되어야 하지만, 라이브러리는 하위 폴더만 노출하기 때문입니다. 이는 빌드 프로세스를 더 잘 제어할 수 있도록 의도된 동작입니다. 그래도 `.lua` 파일에 라이프사이클 훅을 단순 함수로 만들 수 있으므로, 라이브러리 사용자는 자신의 `/hooks.editor_script`에서 이를 require하고 사용할 수 있습니다.

또한 의존성이 Assets view에 표시되더라도 파일로 존재하지는 않는다는 점에 주의하세요(의존성은 zip 아카이브의 entry입니다). 에디터가 의존성에서 일부 파일을 추출해 `build/plugins/` 폴더에 넣도록 만들 수 있습니다. 이를 위해서는 라이브러리 폴더에 `ext.manifest` 파일을 만들고, `ext.manifest` 파일이 위치한 같은 폴더에 `plugins/bin/${platform}` 폴더를 만들어야 합니다. 해당 폴더의 파일은 `/build/plugins/${extension-path}/plugins/bin/${platform}` 폴더로 자동 추출되므로, 에디터 스크립트가 이를 참조할 수 있습니다.

## Preferences {#preferences}

에디터 스크립트는 preferences를 정의하고 사용할 수 있습니다. preferences는 사용자의 컴퓨터에 저장되는, 커밋되지 않는 영구 데이터 조각입니다. 이 preferences에는 세 가지 주요 특징이 있습니다.
- typed: 모든 preference에는 데이터 타입과 기본값 같은 기타 메타데이터를 포함하는 스키마 정의가 있습니다.
- scoped: preferences는 프로젝트별 또는 사용자별로 scope가 지정됩니다.
- nested: 모든 preference 키는 점으로 구분된 문자열이며, 첫 번째 path segment는 에디터 스크립트를 식별하고 나머지는

모든 preferences는 스키마를 정의해 등록해야 합니다.
```lua
function M.get_prefs_schema()
  return {
    ["my_json_formatter.jq_path"] = editor.prefs.schema.string(),
    ["my_json_formatter.indent.size"] = editor.prefs.schema.integer({default = 2, scope = editor.prefs.SCOPE.PROJECT}),
    ["my_json_formatter.indent.type"] = editor.prefs.schema.enum({values = {"spaces", "tabs"}, scope = editor.prefs.SCOPE.PROJECT}),
  }
end
```
이러한 에디터 스크립트가 다시 로드되면 에디터는 이 스키마를 등록합니다. 그 후 에디터 스크립트는 preferences를 가져오고 설정할 수 있습니다. 예:
```lua
-- 특정 preference 가져오기
editor.prefs.get("my_json_formatter.indent.type")
-- 반환값: "spaces"

-- 전체 preference 그룹 가져오기
editor.prefs.get("my_json_formatter")
-- 반환값:
-- {
--   jq_path = "",
--   indent = {
--     size = 2,
--     type = "spaces"
--   }
-- }

-- 중첩된 preferences 여러 개를 한 번에 설정
editor.prefs.set("my_json_formatter.indent", {
    type = "tabs",
    size = 1
})
```

## 실행 모드 {#execution-modes}

에디터 스크립트 런타임은 에디터 스크립트 입장에서는 대부분 투명한 2가지 실행 모드, 즉 **immediate**와 **long-running**을 사용합니다.

**Immediate** 모드는 에디터가 가능한 한 빠르게 스크립트에서 응답을 받아야 할 때 사용됩니다. 예를 들어 메뉴 커맨드의 `active` 콜백은 immediate 모드에서 실행됩니다. 이 확인 작업은 사용자가 에디터와 상호작용하는 것에 대한 응답으로 에디터 UI thread에서 수행되고, 같은 frame 안에서 UI를 업데이트해야 하기 때문입니다.

**Long-running** 모드는 에디터가 스크립트에서 즉각적인 응답을 받을 필요가 없을 때 사용됩니다. 예를 들어 메뉴 커맨드의 `run` 콜백은 **long-running** 모드에서 실행되므로, 스크립트가 작업을 완료하는 데 더 많은 시간을 사용할 수 있습니다.

에디터 스크립트에서 사용할 수 있는 일부 함수는 실행에 많은 시간이 걸릴 수 있습니다. 예를 들어 `editor.execute("git", "status", {reload_resources=false, out="capture"})`는 충분히 큰 프로젝트에서 최대 1초가 걸릴 수 있습니다. 에디터의 응답성과 성능을 유지하기 위해, 시간이 오래 걸릴 수 있는 함수는 에디터가 즉시 응답을 받아야 하는 컨텍스트에서 허용되지 않습니다. immediate 컨텍스트에서 이러한 함수를 사용하려고 하면 `Cannot use long-running editor function in immediate context` 오류가 발생합니다. 이 오류를 해결하려면 immediate 컨텍스트에서 이러한 함수를 사용하지 마세요.

다음 함수는 long-running으로 간주되어 immediate 모드에서 사용할 수 없습니다.
- `editor.create_directory()`, `editor.create_resources()`, `editor.delete_directory()`, `editor.save()`, `os.remove()`, `file:write()`: 이 함수들은 디스크의 파일을 수정하여 에디터가 메모리 내 리소스 트리를 디스크 상태와 동기화하게 만들며, 큰 프로젝트에서는 몇 초가 걸릴 수 있습니다.
- `editor.execute()`: 쉘 명령 실행에는 예측할 수 없는 시간이 걸릴 수 있습니다.
- `editor.transact()`: 널리 참조되는 노드에서 큰 트랜잭션을 수행하면 수백 밀리초가 걸릴 수 있으며, 이는 UI 응답성에는 너무 느립니다.

다음 코드 실행 컨텍스트는 immediate 모드를 사용합니다.
- 메뉴 커맨드의 `active` 콜백: 에디터는 같은 UI frame 안에서 스크립트의 응답을 받아야 합니다.
- 에디터 스크립트의 top-level: 에디터 스크립트를 다시 로드하는 행위가 어떤 부작용(side effect)도 가지지 않기를 기대합니다.

## Actions {#actions}

::: sidenote
이전에는 에디터가 Lua VM과 blocking 방식으로 상호작용했으므로 에디터 스크립트가 block하지 않아야 한다는 강한 요구사항이 있었습니다. 일부 상호작용은 에디터 UI thread에서 수행되어야 하기 때문입니다. 그 이유로 예를 들어 `editor.execute()`와 `editor.transact()`가 없었습니다. 대신 스크립트 실행과 에디터 상태 변경은 hook 및 커맨드 `run` 핸들러에서 "actions" 배열을 반환하는 방식으로 트리거되었습니다.

이제 에디터는 Lua VM과 non-blocking 방식으로 상호작용하므로 이러한 actions가 더 이상 필요하지 않습니다. `editor.execute()` 같은 함수를 사용하는 편이 더 편리하고 간결하며 강력합니다. actions는 이제 **DEPRECATED**되었지만, 제거할 계획은 없습니다.
:::

에디터 스크립트는 커맨드의 `run` 함수나 `/hooks.editor_script`의 hook 함수에서 actions 배열을 반환할 수 있습니다. 그러면 에디터가 이 actions를 수행합니다.

Action은 에디터가 무엇을 해야 하는지 설명하는 테이블입니다. 모든 action에는 `action` 키가 있습니다. Actions는 undoable과 non-undoable이라는 2가지 종류가 있습니다.

### 실행 취소 가능한 actions {#undoable-actions}

::: sidenote
`editor.transact()` 사용을 권장합니다.
:::

Undoable action은 실행된 뒤 실행 취소할 수 있습니다. 커맨드가 여러 undoable action을 반환하면 함께 수행되고 함께 실행 취소됩니다. 가능하다면 undoable action을 사용해야 합니다. 단점은 더 제한적이라는 점입니다.

기존 undoable actions:
- `"set"` — 에디터 안 노드의 프로퍼티를 어떤 값으로 설정합니다. 예:
  ```lua
  {
    action = "set",
    node_id = opts.selection,
    property = "text",
    value = "current time is " .. os.date()
  }
  ```
  `"set"` action에는 다음 키가 필요합니다.
  - `node_id` — 노드 id userdata입니다. 또는 여기에서 에디터에서 받은 노드 id 대신 리소스 경로를 사용할 수 있습니다. 예: `"/main/game.script"`
  - `property` — 설정할 노드의 프로퍼티입니다. 예: `"text"`
  - `value` — 프로퍼티의 새 값입니다. `"text"` 프로퍼티의 경우 문자열이어야 합니다.

### 실행 취소 불가능한 actions {#non-undoable-actions}

::: sidenote
`editor.execute()` 사용을 권장합니다.
:::

Non-undoable action은 실행 취소 기록(undo history)을 지우므로, 이러한 action을 실행 취소하고 싶다면 버전 관리 같은 다른 수단을 사용해야 합니다.

기존 non-undoable actions:
- `"shell"` — 쉘 스크립트를 실행합니다. 예:
  ```lua
  {
    action = "shell",
    command = {
      "./scripts/minify-json.sh",
      editor.get(opts.selection, "path"):sub(2) -- 앞의 "/" 제거
    }
  }
  ```
  `"shell"` action에는 command와 그 인자의 배열인 `command` 키가 필요합니다.

### Actions와 부작용(side effect) 섞기 {#mixing-actions-and-side-effects}

Undoable action과 non-undoable action을 섞을 수 있습니다. Actions는 순차적으로 실행되므로, actions의 순서에 따라 해당 커맨드의 일부를 실행 취소할 수 없게 될 수 있습니다.

Actions를 기대하는 함수에서 actions를 반환하는 대신, `io.open()`을 사용해 파일을 직접 읽고 쓸 수도 있습니다. 그러면 리소스 다시 로드가 트리거되어 실행 취소 기록(undo history)이 지워집니다.
