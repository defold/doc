---
title: Defold 컴퓨트 매뉴얼
brief: 이 매뉴얼은 컴퓨트 프로그램, 쉐이더 상수, 샘플러를 다루는 방법을 설명합니다.
---

# 컴퓨트 프로그램

::: sidenote
Defold의 컴퓨트 쉐이더 지원은 현재 *기술 프리뷰* 상태입니다.
이는 아직 부족한 기능이 일부 있으며, API가 앞으로 변경될 가능성이 있다는 뜻입니다.
:::

컴퓨트 쉐이더는 GPU에서 범용 계산을 수행하기 위한 강력한 도구입니다. 물리 시뮬레이션, 이미지 처리 등 다양한 작업에서 GPU의 병렬 처리 성능을 활용할 수 있습니다. 컴퓨트 쉐이더는 버퍼나 텍스쳐에 저장된 데이터에 대해 동작하며, 많은 GPU 스레드에서 병렬로 작업을 수행합니다. 이러한 병렬성이 컴퓨트 쉐이더를 집약적인 계산에 매우 강력하게 만들어 줍니다.

* 렌더 파이프라인에 대한 자세한 내용은 [Render 문서](/manuals/render)를 참고하세요.
* 쉐이더 프로그램에 대한 자세한 설명은 [쉐이더 문서](/manuals/shader)를 참고하세요.

## 컴퓨트 쉐이더로 무엇을 할 수 있나요?

컴퓨트 쉐이더는 일반적인 계산에 사용하도록 만들어졌기 때문에 실제로 할 수 있는 일에는 제한이 없습니다. 다음은 컴퓨트 쉐이더가 일반적으로 사용되는 몇 가지 예입니다.

이미지 처리
  - 이미지 필터링: 블러, 엣지 감지, 선명화 필터 등을 적용합니다.
  - 컬러 그레이딩: 이미지의 색상 공간을 조정합니다.

물리
  - 파티클 시스템: 연기, 불, 유체 역학 같은 효과를 위해 많은 수의 파티클을 시뮬레이션합니다.
  - 소프트 바디 물리: 천이나 젤리처럼 변형 가능한 오브젝트를 시뮬레이션합니다.
  - 컬링: 오클루전 컬링(occlusion culling), 절두체 컬링(frustum culling)

절차적 생성
  - 지형 생성: 노이즈 함수를 사용해 세밀한 지형을 만듭니다.
  - 식생과 잎: 절차적으로 생성된 식물과 나무를 만듭니다.

렌더링 효과
  - 전역 조명: 빛이 씬 안에서 반사되는 방식을 근사해 사실적인 조명을 시뮬레이션합니다.
  - 복셀화: 메시 데이터에서 3D 복셀(voxel) 그리드를 만듭니다.

## 컴퓨트 쉐이더는 어떻게 동작하나요?

높은 수준에서 보면 컴퓨트 쉐이더는 하나의 작업을 동시에 실행할 수 있는 많은 작은 작업으로 나누어 동작합니다. 이는 `work groups`와 `invocations`라는 개념을 통해 이루어집니다.

Work Groups
: 컴퓨트 쉐이더는 `work groups`의 그리드에서 동작합니다. 각 work group에는 고정된 수의 invocation(또는 스레드)이 들어 있습니다. work group의 크기와 invocation의 수는 쉐이더 코드에서 정의됩니다.

Invocations
: 각 invocation(또는 스레드)은 컴퓨트 쉐이더 프로그램을 실행합니다. 같은 work group 안의 invocation들은 공유 메모리를 통해 데이터를 공유할 수 있으므로, 서로 효율적으로 통신하고 동기화할 수 있습니다.

GPU는 여러 work group에 걸쳐 많은 invocation을 병렬로 실행하여 컴퓨트 쉐이더를 실행하며, 적합한 작업에 상당한 계산 성능을 제공합니다.

## 컴퓨트 프로그램 생성하기

컴퓨트 프로그램을 만들려면 *Assets* 브라우저에서 대상 폴더를 <kbd>right click</kbd>하고 <kbd>New... ▸ Compute</kbd>를 선택합니다. 메뉴에서 <kbd>File ▸ New...</kbd>를 선택한 다음 <kbd>Compute</kbd>를 선택할 수도 있습니다. 새 컴퓨트 파일의 이름을 지정하고 <kbd>Ok</kbd>를 누릅니다.

![컴퓨트 파일](images/compute/compute_file.png)

새 컴퓨트 파일이 *Compute Editor*에서 열립니다.

![컴퓨트 에디터](images/compute/compute.png)

컴퓨트 파일에는 다음 정보가 포함됩니다.

Compute Program
: 사용할 컴퓨트 쉐이더 프로그램 파일(*`.cp`*)입니다. 쉐이더는 "abstract work items"에 대해 동작합니다. 즉 입력과 출력 데이터 타입에 대한 고정된 정의가 없습니다. 컴퓨트 쉐이더가 무엇을 생성해야 하는지는 프로그래머가 직접 정의해야 합니다.

Constants
: 컴퓨트 쉐이더 프로그램에 전달될 uniform입니다. 사용할 수 있는 상수 목록은 아래를 참고하세요.

Samplers
: 메터리얼 파일에서 특정 샘플러를 선택적으로 설정할 수 있습니다. 샘플러를 추가하고, 쉐이더 프로그램에서 사용하는 이름과 같게 이름을 지정한 다음, 원하는 wrap 및 filter 설정을 지정합니다.


## Defold에서 컴퓨트 프로그램 사용하기

메터리얼과 달리 컴퓨트 프로그램은 어떤 컴포넌트에도 할당되지 않으며, 일반 렌더 흐름의 일부도 아닙니다. 컴퓨트 프로그램이 작업을 수행하려면 렌더 스크립트에서 `dispatched`되어야 합니다. 하지만 디스패치하기 전에 렌더 스크립트가 컴퓨트 프로그램에 대한 참조를 가지고 있는지 확인해야 합니다. 현재 렌더 스크립트가 컴퓨트 프로그램을 알 수 있는 유일한 방법은 렌더 스크립트에 대한 참조를 가진 .render 파일에 컴퓨트 프로그램을 추가하는 것입니다.

![컴퓨트 렌더 파일](images/compute/compute_render_file.png)

컴퓨트 프로그램을 사용하려면 먼저 렌더 컨텍스트에 바인딩해야 합니다. 이는 메터리얼과 같은 방식으로 수행됩니다.

```lua
render.set_compute("my_compute")
-- 여기에서 컴퓨트 작업을 수행하고, render.set_compute()를 호출해 바인딩을 해제합니다
render.set_compute()
```

프로그램이 디스패치될 때 컴퓨트 상수는 자동으로 적용되지만, 에디터에서 컴퓨트 프로그램에 입력 또는 출력 리소스(텍스쳐, 버퍼 등)를 바인딩할 방법은 없습니다. 대신 렌더 스크립트를 통해 수행해야 합니다.

```lua
render.enable_texture("blur_render_target", "tex_blur")
render.enable_texture(self.storage_texture, "tex_storage")
```

정한 작업 공간에서 프로그램을 실행하려면 프로그램을 디스패치해야 합니다.

```lua
render.dispatch_compute(128, 128, 1)
-- dispatch_compute는 마지막 인자로 options 테이블도 받을 수 있습니다
-- 이 인자 테이블을 사용해 render 상수를 dispatch 호출에 전달할 수 있습니다
local constants = render.constant_buffer()
constants.tint = vmath.vector4(1, 1, 1, 1)
render.dispatch_compute(32, 32, 32, {constants = constants})
```

### 컴퓨트 프로그램에서 데이터 쓰기

현재 컴퓨트 프로그램에서 어떤 종류의 출력이든 생성하려면 `storage textures`를 통해서만 가능합니다. storage texture는 더 많은 기능과 설정 가능성을 지원한다는 점을 제외하면 "일반 텍스쳐"와 비슷합니다. 이름에서 알 수 있듯이 storage texture는 컴퓨트 프로그램에서 데이터를 읽고 쓸 수 있는 범용 버퍼로 사용할 수 있습니다. 그런 다음 같은 버퍼를 다른 쉐이더 프로그램에 읽기용으로 바인딩할 수 있습니다.

Defold에서 storage texture를 만들려면 일반 `.script` 파일에서 작업해야 합니다. 렌더 스크립트에는 이 기능이 없습니다. 동적 텍스쳐는 일반 `.script` 파일에서만 사용할 수 있는 `resource` API를 통해 생성해야 하기 때문입니다.

```lua
-- .script 파일에서:
function init(self)
    -- 평소처럼 텍스쳐 리소스를 만들되, "storage" 플래그를 추가합니다.
    -- 그러면 컴퓨트 프로그램의 backing storage로 사용할 수 있습니다.
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = graphics.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = graphics.TEXTURE_FORMAT_RGBA32F,
        flags  = graphics.TEXTURE_USAGE_FLAG_STORAGE + graphics.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    -- 리소스에서 텍스쳐 핸들을 가져옵니다.
    local t_backing_handle = resource.get_texture_info(t_backing).handle

    -- backing texture를 렌더러에 알려 render.enable_texture()로 바인딩할 수 있게 합니다.
    msg.post("@render:", "set_backing_texture", { handle = t_backing_handle })
end
```

## 전체 구성하기

### 쉐이더 프로그램

```glsl
// compute.cp
#version 450

layout (local_size_x = 1, local_size_y = 1, local_size_z = 1) in;

// 입력 리소스를 지정합니다.
uniform vec4 color;
uniform sampler2D texture_in;

// 출력 이미지를 지정합니다.
layout(rgba32f) uniform image2D texture_out;

void main()
{
    // 특별히 흥미로운 쉐이더는 아니지만, 텍스쳐와 상수 버퍼에서
    // 읽고 storage texture에 쓰는 방법을 보여줍니다.

    ivec2 tex_coord   = ivec2(gl_GlobalInvocationID.xy);
    vec4 output_value = vec4(0.0, 0.0, 0.0, 1.0);
    vec2 tex_coord_uv = vec2(float(tex_coord.x)/(gl_NumWorkGroups.x), float(tex_coord.y)/(gl_NumWorkGroups.y));
    vec4 input_value = texture(texture_in, tex_coord_uv);
    output_value.rgb = input_value.rgb * color.rgb;

    // 출력 값을 storage texture에 씁니다.
    imageStore(texture_out, tex_coord, output_value);
}
```

### 스크립트 컴포넌트
```lua
-- .script 파일에서

-- 여기에서는 나중에 컴퓨트 프로그램에 바인딩할 입력 텍스쳐를 지정합니다.
-- 이 텍스쳐를 모델 컴포넌트에 할당하거나, 렌더 스크립트에서
-- 렌더 컨텍스트에 활성화할 수 있습니다.
go.property("texture_in", resource.texture())

function init(self)
    -- 평소처럼 텍스쳐 리소스를 만들되, "storage" 플래그를 추가합니다.
    -- 그러면 컴퓨트 프로그램의 backing storage로 사용할 수 있습니다.
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

    -- 입력 및 출력 텍스쳐를 렌더러에 알립니다.
    msg.post("@render:", "set_backing_texture", textures)
end
```

### 렌더 스크립트
```lua
-- "set_backing_texture" 메세지에 응답하여
-- 컴퓨트 프로그램의 backing texture를 설정합니다.
function on_message(self, message_id, message)
    if message_id == hash("set_backing_texture") then
        self.texture_in = message.texture_in
        self.texture_out = message.texture_out
    end
end

function update(self)
    render.set_compute("compute")
    -- 텍스쳐를 특정 이름의 상수에 바인딩할 수 있습니다.
    render.enable_texture(self.texture_in, "texture_in")
    render.enable_texture(self.texture_out, "texture_out")
    render.set_constant("color", vmath.vector4(0.5, 0.5, 0.5, 1.0))
    -- 픽셀 수만큼 컴퓨트 프로그램을 디스패치합니다.
    -- 이것이 우리의 "working group"을 구성합니다. 쉐이더는
    -- 128 x 128 x 1번, 즉 픽셀당 한 번 호출됩니다.
    render.dispatch_compute(128, 128, 1)
    -- 컴퓨트 프로그램 사용이 끝나면 바인딩을 해제해야 합니다.
    render.set_compute()
end
```

## 호환성

Defold는 현재 다음 그래픽 어댑터에서 컴퓨트 쉐이더를 지원합니다.

- Vulkan
- Metal (via MoltenVK)
- OpenGL 4.3+
- OpenGL ES 3.1+

활성 그래픽 어댑터가 컴퓨트 쉐이더를 지원하는지 확인하려면 `graphics.get_adapter_info()`를 사용합니다. `features` 필드에는 어댑터가 지원하는 컨텍스트 기능 상수의 배열이 포함됩니다.

```lua
local function has_context_feature(feature)
    local adapter_info = graphics.get_adapter_info()
    for _, supported_feature in ipairs(adapter_info.features) do
        if supported_feature == feature then
            return true
        end
    end
    return false
end

local compute_shaders_supported = has_context_feature(
    graphics.CONTEXT_FEATURE_COMPUTE_SHADER
)
```

배열에는 지원되는 기능만 포함되며 기능 상수를 키로 사용하는 테이블이 아닙니다. 게임을 여러 그래픽 어댑터에서 실행할 수 있거나 드라이버 지원이 서로 다른 기기에서 실행할 수 있다면 컴퓨트 쉐이더를 사용하기 전에 항상 이 검사를 수행하십시오. OpenGL 및 OpenGL ES 지원 여부는 API 버전과 드라이버에 따라 달라집니다. Vulkan과 MoltenVK를 통한 Metal은 버전 1.0부터 컴퓨트 쉐이더를 지원합니다. Vulkan이 아직 기본 그래픽 백엔드가 아닌 플랫폼에서 Vulkan을 선택하려면 [애플리케이션 매니페스트](/manuals/app-manifest)를 사용하십시오.
