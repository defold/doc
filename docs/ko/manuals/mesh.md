---
title: Defold의 3D mesh
brief: 이 매뉴얼은 게임에서 런타임에 3D mesh를 생성하는 방법을 설명합니다.
---

# Mesh 컴포넌트 {#mesh-component}

Defold는 근본적으로 3D 엔진입니다. 2D 컨텐츠만으로 작업할 때도 모든 렌더링은 3D로 수행되며, 화면에는 직교 투영되어 표시됩니다. Defold에서는 컬렉션 안에서 런타임에 3D mesh를 추가하고 생성하여 완전한 3D 컨텐츠를 활용할 수 있습니다. 3D 에셋만으로 순수한 3D 게임을 만들 수도 있고, 원하는 대로 3D와 2D 컨텐츠를 섞을 수도 있습니다.

## Mesh 컴포넌트 만들기 {#creating-a-mesh-component}

Mesh 컴포넌트는 다른 게임 오브젝트 컴포넌트와 같은 방식으로 생성합니다. 방법은 두 가지입니다:

- *Assets* 브라우저에서 위치를 <kbd>오른쪽 클릭</kbd>하고 <kbd>New... ▸ Mesh</kbd>를 선택하여 *Mesh file*을 생성합니다.
- *Outline* 뷰에서 게임 오브젝트를 <kbd>오른쪽 클릭</kbd>하고 <kbd>Add Component ▸ Mesh</kbd>를 선택하여 게임 오브젝트 안에 직접 내장된 컴포넌트를 생성합니다.

![게임 오브젝트의 Mesh](images/mesh/mesh.png)

mesh를 생성한 뒤에는 여러 프로퍼티를 지정해야 합니다:

### Mesh 프로퍼티 {#mesh-properties}

프로퍼티 *Id*, *Position*, *Rotation* 외에 다음 컴포넌트 전용 프로퍼티가 있습니다:

*Material*
: mesh 렌더링에 사용할 메터리얼입니다.

*Vertices*
: 스트림별 mesh 데이터를 설명하는 Buffer 파일입니다.

*Primitive Type*
: Lines, Triangles 또는 Triangle Strip입니다.

*Position Stream*
: 이 프로퍼티는 *position* 스트림의 이름이어야 합니다. 이 스트림은 자동으로 버텍스 쉐이더의 입력으로 제공됩니다.

*Normal Stream*
: 이 프로퍼티는 *normal* 스트림의 이름이어야 합니다. 이 스트림은 자동으로 버텍스 쉐이더의 입력으로 제공됩니다.

*tex0*
: mesh에 사용할 텍스쳐로 설정합니다.

## 에디터 조작 {#editor-manipulation}

Mesh 컴포넌트가 배치되면 일반적인 *Scene Editor* 도구로 컴포넌트 및/또는 해당 컴포넌트를 포함하는 게임 오브젝트를 자유롭게 편집하고 조작하여 원하는 대로 mesh를 이동, 회전, 스케일 조정할 수 있습니다.

## 런타임 조작 {#runtime-manipulation}

Defold buffer를 사용해 런타임에 mesh를 조작할 수 있습니다. 다음은 triangle strip으로 큐브를 만드는 예제입니다:

```Lua

-- 큐브
local vertices = {
	0, 0, 0,
	0, 1, 0,
	1, 0, 0,
	1, 1, 0,
	1, 1, 1,
	0, 1, 0,
	0, 1, 1,
	0, 0, 1,
	1, 1, 1,
	1, 0, 1,
	1, 0, 0,
	0, 0, 1,
	0, 0, 0,
	0, 1, 0
}

-- position 스트림이 있는 buffer를 생성합니다
local buf = buffer.create(#vertices / 3, {
	{ name = hash("position"), type=buffer.VALUE_TYPE_FLOAT32, count = 3 }
})

-- position 스트림을 가져와 버텍스를 씁니다
local positions = buffer.get_stream(buf, "position")
for i, value in ipairs(vertices) do
	positions[i] = vertices[i]
end

-- 버텍스가 들어 있는 buffer를 mesh에 설정합니다
local res = go.get("#mesh", "vertices")
resource.set_buffer(res, buf)
```

샘플 프로젝트와 코드 스니펫을 포함한 Mesh 컴포넌트 사용 방법에 대한 자세한 내용은 [포럼 공지 게시글](https://forum.defold.com/t/mesh-component-in-defold-1-2-169-beta/65137)을 참고하세요.

## 절두체 컬링 {#frustum-culling}

Mesh 컴포넌트는 동적인 특성과 위치 데이터가 어떻게 인코딩되어 있는지 확실히 알 수 없다는 점 때문에 자동으로 컬링되지 않습니다. mesh를 컬링하려면 6개의 부동 소수점 숫자(AABB min/max)를 사용해 mesh의 축 정렬 바운딩 박스(axis-aligned bounding box)를 buffer의 메타 데이터로 설정해야 합니다:

```lua
buffer.set_metadata(buf, hash("AABB"), { 0, 0, 0, 1, 1, 1 }, buffer.VALUE_TYPE_FLOAT32)
```

## 메터리얼 상수 {#material-constants}

{% include shared/material-constants.md component='mesh' variable='tint' %}

`tint`
: mesh의 색조(tint)입니다(`vector4`). `vector4`는 x, y, z, w가 각각 빨강, 초록, 파랑, 알파 색조에 대응하는 tint를 표현하는 데 사용됩니다.

## 버텍스 로컬 공간과 월드 공간 {#vertex-local-vs-world-space}
mesh 메터리얼의 Vertex Space 설정이 Local Space로 설정되어 있으면 데이터는 쉐이더에 있는 그대로 제공되며, 일반적으로 GPU에서 하듯이 버텍스/노멀을 변환해야 합니다.

mesh 메터리얼의 Vertex Space 설정이 World Space로 설정되어 있으면 기본 `position` 및 `normal` 스트림을 제공하거나 mesh를 편집할 때 드롭다운에서 선택해야 합니다. 이렇게 해야 엔진이 다른 오브젝트와 배치 처리할 수 있도록 데이터를 월드 공간으로 변환할 수 있습니다.
