---
title: 모델 임포트하기
brief: 이 매뉴얼은 모델 컴포넌트에서 사용하는 3D 모델을 임포트하는 방법을 설명합니다.
---

# 3D 모델 임포트하기
Defold는 glTF 2.0 (GL Transmission Format) 포멧의 모델, 스켈레톤, 애니메이션을 지원합니다. 3D 모델에는 *.gltf* 또는 *.glb* 파일을 사용하세요. glTF는 게임엔진과 실시간 어플리케이션에서 3D 데이터를 전송하고 로드하도록 설계된 최신 포멧입니다.

Maya, 3ds Max, SketchUp, Blender 같은 도구를 사용해 3D 모델을 만들거나 glTF로 변환할 수 있습니다.

Blender는 강력하고 인기 있는 3D 모델링, 애니메이션, 렌더링 프로그램입니다. Windows, macOS, Linux에서 실행되며 [https://www.blender.org](https://www.blender.org)에서 무료로 받을 수 있습니다.

![Blender의 모델](images/model/blender_gltf.png)

## Defold로 임포트하기
모델을 임포트하려면 *.gltf* 또는 *.glb* 파일을 Defold 에디터의 *Assets pane*으로 드래그-앤-드롭합니다.

glTF는 보통 두 가지 방식으로 저장할 수 있습니다:

* *.glb*는 단일 바이너리 파일입니다. 모델 데이터를 포함하며, 패킹된 텍스쳐 이미지를 포함할 수도 있습니다. 모델을 하나의 파일로 옮기거나 저장하려는 경우 편리합니다.
* *.gltf*는 텍스트 기반 JSON 파일입니다. 보통 메쉬 데이터용 별도 *.bin* 파일과 *.png*, *.jpg*, *.ktx2* 등의 별도 텍스쳐 이미지를 참조합니다. 이 형식을 사용할 때는 참조하는 모든 파일을 프로젝트에 추가하고 상대 경로를 유지하세요.

내장 이미지는 별도 에셋으로 추출하지 않고 glTF나 GLB 파일에서 직접 사용할 수 있습니다. 외부 이미지 및 버퍼 파일은 여전히 상대 경로를 유지하여 모델과 함께 임포트해야 합니다.

::: sidenote
Defold는 임포트한 glTF 파일의 위치와 트랜스폼을 유지하며 모델 중심을 자동으로 다시 맞추지 않습니다. 에디터 미리보기와 런타임은 임포트된 트랜스폼을 일관되게 사용합니다. 스킨드 메쉬나 본을 부모로 갖는 메쉬는 스켈레톤 기준의 로컬 트랜스폼을 유지하고, 강체 메쉬는 계층구조를 평탄화한 월드 배치를 유지합니다.

[Model 컴포넌트](/manuals/model/#model-properties)에서 임포트된 씬의 이름 있는 메쉬 하나를 선택할 수 있습니다. *Mesh* 필드를 비워 두면 전체 씬을 사용하고 위에서 설명한 트랜스폼을 유지합니다. 메쉬를 선택하면 glTF 노드 트랜스폼 없이 로컬 지오메트리를 사용하므로 모델 컴포넌트나 게임 오브젝트의 트랜스폼으로 배치하세요.

이전 버전의 Defold로 만든 모델을 다시 임포트한 후 위치나 방향이 달라졌다면 Blender 또는 다른 저작 도구에서 트랜스폼을 수정하고 *.gltf* 또는 *.glb* 파일을 다시 익스포트하세요.
:::

### 압축된 지오메트리 {#compressed-geometry}

*.gltf*와 *.glb* 소스에는 Draco 또는 Meshopt로 압축된 지오메트리가 포함될 수 있습니다. 지원하는 glTF 압축 익스텐션은 다음과 같습니다:

| 압축 | glTF 익스텐션 |
| --- | --- |
| Draco | `KHR_draco_mesh_compression` |
| Meshopt | `EXT_meshopt_compression` 및 `KHR_meshopt_compression` |

이 익스텐션 중 하나로 glTF 2.0 에셋을 익스포트하거나 최적화한 다음 압축하지 않은 모델과 같은 절차로 임포트합니다. 외부 버퍼와 텍스쳐를 포함하고 상대 경로를 유지하세요. 평소처럼 임포트된 파일을 Model 컴포넌트의 *Scene* 프로퍼티에 지정합니다.

Defold는 임포트와 빌드 시 압축된 지오메트리를 디코딩합니다. 결과 모델은 Defold의 일반 런타임 지오메트리 표현을 사용합니다. 이 지원이 실행 중인 엔진에서 Draco나 Meshopt 압축을 활성화하는 것은 아니며, 원본 파일이 작다고 게임 번들도 반드시 작아지는 것은 아닙니다.

### 임포트한 씬 살펴보기 {#browsing-the-imported-scene}

*Assets* 창에서 *.gltf* 또는 *.glb* 파일을 펼쳐 메쉬, 생성된 메터리얼, 내장 이미지를 살펴봅니다. 씬을 열면 정의된 메터리얼과 텍스쳐로 미리보기를 표시합니다. 개별 메쉬를 열어 미리볼 수도 있습니다.

파일 내부에 노출된 리소스는 읽기 전용입니다. 메쉬의 편집 가능한 Model 리소스를 만들려면 메쉬를 복사하여 프로젝트 폴더에 붙여넣습니다. 생성된 *.model* 파일은 계속 임포트된 glTF나 GLB 파일을 참조합니다. 원본 지오메트리나 내장 이미지를 변경하려면 제작 도구에서 에셋을 수정하고 다시 익스포트하세요.

에디터 스크립트는 `editor.resource_children(path)`로 이 리소스들을 나열할 수 있습니다. 폴더와 glTF/GLB 파일 내부 리소스를 재귀적으로 방문하는 예제는 [프로젝트 리소스 순회](/manuals/editor-scripts/#traversing-project-resources)를 참고하세요.

### KTX2 텍스쳐 {#ktx2-textures}

모델 텍스쳐는 외부 파일 또는 *.gltf*, *.glb* 파일 내부 이미지로 *.ktx2* 소스를 사용할 수 있습니다. 외부 파일은 모델과 함께 임포트합니다. 내장 KTX2 이미지는 *Assets* 창의 씬 아래에 표시되며 메터리얼 텍스쳐 필드에 직접 또는 <kbd>Auto Fill</kbd>로 지정할 수 있습니다.

[텍스쳐 프로파일](/manuals/texture-profiles/#ktx2-source-textures)은 KTX2 원본 포멧을 유지할지 설정된 출력 포멧으로 변환할지 결정합니다. **Keep KTX2 Format**은 텍스쳐 압축이 활성화되어 있으면 원본 인코딩 포멧을 유지하지만, 이미지 처리에 따라 재인코딩이 필요할 수 있습니다. 타겟 기기의 포멧 지원을 확인하고 이미 압축된 텍스쳐를 다시 압축할 때 추가 화질 손실이 발생할 수 있음을 고려하세요. [KTX2 입력 포멧과 미리보기](/manuals/importing-graphics/#ktx2-textures)를 참고하세요.

## 모델 사용하기 {#using-a-model}
모델을 임포트한 뒤에는 [모델 컴포넌트](/manuals/model)에서 사용합니다:

1. *Assets* pane에서 <kbd>New... ▸ Model</kbd>로 Model 파일을 만들거나, <kbd>Add Component ▸ Model</kbd>로 게임 오브젝트에 Model 컴포넌트를 직접 추가합니다.
2. *Scene* 프로퍼티를 임포트한 *.gltf* 또는 *.glb* 파일로 설정합니다.
3. *Auto Fill Model Fields?* 대화 상자가 나타나면 <kbd>Auto Fill</kbd>을 선택하여 씬에서 생성된 메터리얼과 참조 텍스쳐를 지정합니다. 기존 메터리얼과 텍스쳐 바인딩이 교체됩니다. 바인딩을 유지하려면 <kbd>Keep Current</kbd>를 선택하세요. 새 씬 선택은 그대로 적용됩니다.
4. 전체 씬을 사용하려면 *Mesh*를 비워 두고, 로컬 지오메트리만 사용하려면 이름 있는 메쉬를 선택합니다. 메쉬 선택을 바꿀 때도 같은 대화 상자가 나타날 수 있습니다. 메쉬를 선택하면 해당 메터리얼을, 선택을 지우면 씬의 모든 메터리얼을 제안합니다. <kbd>Keep Current</kbd>는 새 메쉬 선택을 적용하면서 바인딩을 유지합니다.
5. 애니메이션되는 모델의 경우 *Skeleton* 프로퍼티를 스켈레톤이 들어 있는 *.gltf* 또는 *.glb* 파일로 설정합니다. 메쉬, 스켈레톤, 애니메이션을 함께 익스포트했다면 *Scene*에 사용한 파일과 같은 경우가 많습니다.
6. 애니메이션용 *Animation Set* 파일을 만들고 *Animations* 프로퍼티에 할당합니다. 애니메이션을 자동으로 시작하려면 *Default Animation*을 설정합니다.

선택한 glTF나 GLB 소스가 메터리얼을 노출하면 에디터가 바인딩 채우기를 제안합니다. 내장 이미지와 외부 이미지 참조를 모두 해결합니다. 생성된 메터리얼은 내장 glTF 쉐이더를 사용합니다. 조명과 지원하는 메터리얼 효과는 [PBR 매뉴얼](/manuals/physically-based-rendering/#built-in-pbr-materials)을 참고하세요.

### 메터리얼과 텍스쳐 수동 지정 {#assigning-materials-and-textures-manually}

<kbd>Keep Current</kbd>를 선택했거나 커스텀 셰이딩이 필요하면 각 *Material* 프로퍼티를 적절한 메터리얼로 설정합니다. 내장 `gltf` 메터리얼은 PBR 셰이딩을 제공하며, 내장 `model` 메터리얼이나 직접 만든 메터리얼도 사용할 수 있습니다. 정적, 스킨드, 인스턴싱 변형과 요구 사항은 [Model 매뉴얼](/manuals/model/#material)을 참고하세요.

각 텍스쳐를 해당 메터리얼 텍스쳐 필드에 지정합니다. *Assets* 창의 glTF 또는 GLB 파일 아래에 노출된 내장 이미지나 프로젝트의 별도 이미지 에셋을 사용할 수 있습니다. 샘플러가 여러 개인 메터리얼에서는 각 텍스쳐를 의도한 샘플러에 맞추세요. [PBR 매뉴얼에 내장 glTF 샘플러 이름](/manuals/physically-based-rendering/#built-in-pbr-materials)이 나와 있습니다.

## glTF로 익스포트하기
익스포트된 *.gltf* 또는 *.glb* 파일에는 모델을 구성하는 모든 버텍스, 엣지, 페이스뿐 아니라, 정의한 경우 _UV 좌표_ (텍스쳐 이미지의 어느 부분이 메쉬의 특정 부분에 매핑되는지), 스켈레톤의 본, 애니메이션 데이터가 들어 있습니다.

* 폴리곤 메쉬에 대한 자세한 설명은 http://en.wikipedia.org/wiki/Polygon_mesh 에서 확인할 수 있습니다.

* UV 좌표와 UV 매핑은 http://en.wikipedia.org/wiki/UV_mapping 에 설명되어 있습니다.

Defold는 익스포트된 애니메이션 데이터에 몇 가지 제한을 둡니다:

* 현재 Defold는 베이크된 애니메이션만 지원합니다. 애니메이션은 포지션, 회전, 스케일을 별도 키로 갖는 것이 아니라, 애니메이션되는 각 본마다 각 키프레임에 대한 메트릭스를 가져야 합니다.

* 애니메이션은 또한 선형으로 보간됩니다. 더 고급 곡선 보간을 사용한다면 익스포터에서 애니메이션을 미리 베이크해야 합니다.

### 요구사항

모델을 익스포트할 때는 도구와 엔진마다 glTF 지원이 다를 수 있음을 고려하세요. glTF 2.0을 사용하고 텍스쳐를 사용하는 모델의 UV 좌표가 올바른지 확인합니다. 이미지는 glTF나 GLB 파일에 내장하거나 씬이 참조하는 별도 파일로 저장할 수 있습니다. Defold로 임포트할 때 모든 외부 이미지와 버퍼 파일을 포함하세요.

glTF 포멧을 완전히 지원하는 것이 목표이지만, 아직 완전한 상태는 아닙니다.
빠진 기능이 있다면 [Defold 저장소](https://github.com/defold/defold/issues)에 기능 요청을 올려 주세요.

### 텍스쳐 익스포트하기

텍스쳐 이미지를 직접 만들려면 Blender에서 UV 레이아웃을 템플릿으로 익스포트할 수 있습니다. 먼저 메쉬와 모든 버텍스를 선택합니다:

![모두 선택](images/model/blender_select_all_vertices.png)

모든 버텍스를 선택한 뒤에는 메쉬를 언랩하여 UV 레이아웃을 얻습니다:

![메쉬 언랩](images/model/blender_unwrap_mesh.png)

그런 다음 UV 레이아웃을 텍스쳐로 사용할 수 있는 이미지로 익스포트합니다:

![UV 레이아웃 익스포트](images/model/blender_export_uv_layout.png)

![UV 레이아웃 익스포트 결과](images/model/blender_export_uv_layout_result.png)

### Blender로 익스포트하기
<kbd>File ▸ Export ▸ glTF 2.0 (.glb/.gltf)</kbd>를 사용해 Blender에서 모델을 익스포트합니다.

![Blender로 익스포트하기](images/model/export_gltf.png)

익스포트하기 전에 오브젝트를 하나 이상 선택하고, 선택 항목만 익스포트하려면 *Selected Objects*를 활성화합니다.

*Format* 옵션 중 하나를 선택합니다:

* *glTF Binary (.glb)*는 파일 하나를 생성합니다. 모델을 하나의 에셋으로 쉽게 옮기거나 저장하려는 경우 사용하세요.
* *glTF Separate (.gltf + .bin + textures)*는 모델 설명, 바이너리 데이터, 텍스쳐에 대해 별도 파일을 생성합니다. 텍스쳐 이미지를 편집하거나 Defold에서 별도로 할당하려는 경우 사용하세요.

모델에 애니메이션이 포함되어 있다면 애니메이션 익스포트를 활성화하고 애니메이션이 베이크되었는지 확인합니다. 모델이 텍스쳐를 사용한다면 메쉬에 UV 언랩이 있고 텍스쳐 이미지가 PNG 또는 JPEG처럼 Defold에서 임포트할 수 있는 포멧으로 익스포트되는지 확인합니다.

![Blender로 익스포트하기](images/model/export_settings.png)
