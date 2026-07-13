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
* *.gltf*는 텍스트 기반 JSON 파일입니다. 일반적으로 메쉬 데이터용 별도 *.bin* 파일과 *.png* 또는 *.jpg* 같은 별도 텍스쳐 이미지를 참조합니다. 이 방식을 사용할 때는 참조된 모든 파일을 프로젝트에 추가하고 상대 경로를 그대로 유지하세요.

모델이 Defold에서 텍스쳐를 사용해야 한다면 텍스쳐 이미지를 별도 에셋으로 임포트하세요. 소스 glTF/GLB 파일에 내장 이미지가 포함되어 있더라도 텍스쳐는 컴포넌트 메터리얼 텍스쳐 프로퍼티를 통해 Model 컴포넌트에 할당해야 합니다.

![임포트된 모델 에셋](images/model/assets_gltf.png)

::: sidenote
Defold 1.13.0부터 임포트된 glTF 파일의 위치와 트랜스폼이 보존되며 임포트 과정에서 모델의 중심을 자동으로 다시 맞추지 않습니다. 에디터 프리뷰와 런타임은 임포트된 트랜스폼을 일관되게 사용합니다. 스키닝되었거나 본에 부모로 연결된 메쉬는 로컬 스켈레톤 기준 트랜스폼을 보존하고, 리지드 메쉬는 플래튼된 월드 배치를 유지합니다.

이전 버전의 Defold로 만든 모델을 다시 임포트한 후 위치나 방향이 달라졌다면 Blender 또는 다른 저작 도구에서 트랜스폼을 수정하고 *.gltf* 또는 *.glb* 파일을 다시 익스포트하세요.
:::

## 모델 사용하기
모델을 임포트한 뒤에는 [모델 컴포넌트](/manuals/model)에서 사용합니다:

1. *Assets* pane에서 <kbd>New... ▸ Model</kbd>로 Model 파일을 만들거나, <kbd>Add Component ▸ Model</kbd>로 게임 오브젝트에 Model 컴포넌트를 직접 추가합니다.
2. *Mesh* 프로퍼티를 메쉬가 들어 있는 임포트된 *.gltf* 또는 *.glb* 파일로 설정합니다.
3. 애니메이션되는 모델의 경우 *Skeleton* 프로퍼티를 스켈레톤이 들어 있는 *.gltf* 또는 *.glb* 파일로 설정합니다. 메쉬, 스켈레톤, 애니메이션을 함께 익스포트했다면 *Mesh*에 사용한 파일과 같은 경우가 많습니다.
4. 애니메이션용 *Animation Set* 파일을 만들고 *Animations* 프로퍼티에 할당합니다. 애니메이션을 자동으로 시작하려면 *Default Animation*을 설정합니다.
5. *Material* 프로퍼티를 모델에 적합한 메터리얼로 설정합니다. 내장 *model.material*, *model_instanced.material*, *model_skinned.material*, *model_skinned_instanced.material* 파일은 유용한 시작점입니다. 스킨드 메터리얼은 GPU에서 스키닝을 실행할 수 있도록 로컬 버텍스 공간을 사용합니다. GPU 스키닝 또는 인스턴싱 모델용 커스텀 메터리얼도 로컬 버텍스 공간을 사용해야 합니다. 그래픽 어댑터 요구 사항은 [모델 매뉴얼](/manuals/model/#material)을 참고하세요.
6. *Texture* 같은 메터리얼 텍스쳐 프로퍼티를 임포트한 텍스쳐 이미지 파일로 설정합니다. 메터리얼이 여러 텍스쳐를 사용한다면 각 텍스쳐를 해당 메터리얼 텍스쳐 필드에 할당합니다.


## glTF로 익스포트하기
익스포트된 *.gltf* 또는 *.glb* 파일에는 모델을 구성하는 모든 버텍스, 엣지, 페이스뿐 아니라, 정의한 경우 _UV 좌표_ (텍스쳐 이미지의 어느 부분이 메쉬의 특정 부분에 매핑되는지), 스켈레톤의 본, 애니메이션 데이터가 들어 있습니다.

* 폴리곤 메쉬에 대한 자세한 설명은 http://en.wikipedia.org/wiki/Polygon_mesh 에서 확인할 수 있습니다.

* UV 좌표와 UV 매핑은 http://en.wikipedia.org/wiki/UV_mapping 에 설명되어 있습니다.

Defold는 익스포트된 애니메이션 데이터에 몇 가지 제한을 둡니다:

* 현재 Defold는 베이크된 애니메이션만 지원합니다. 애니메이션은 포지션, 회전, 스케일을 별도 키로 갖는 것이 아니라, 애니메이션되는 각 본마다 각 키프레임에 대한 메트릭스를 가져야 합니다.

* 애니메이션은 또한 선형으로 보간됩니다. 더 고급 곡선 보간을 사용한다면 익스포터에서 애니메이션을 미리 베이크해야 합니다.

### 요구사항
모델을 익스포트할 때는 도구와 엔진마다 glTF 지원이 다를 수 있다는 점을 염두에 두세요. glTF 2.0을 사용하고, 모델이 텍스쳐를 사용한다면 올바른 UV 좌표가 있는지 확인하고, Model 컴포넌트에 할당해야 하는 텍스쳐 이미지는 별도로 임포트하세요.

glTF 포멧을 완전히 지원하는 것이 목표이지만, 아직 완전한 상태는 아닙니다.
빠진 기능이 있다면 [Defold 저장소](https://github.com/defold/defold/issues)에 기능 요청을 올려 주세요.

### 텍스쳐 익스포트하기
모델에 사용할 텍스쳐가 아직 없다면 Blender를 사용해 텍스쳐를 생성할 수 있습니다. 모델에서 추가 메터리얼을 제거하기 전에 이 작업을 해야 합니다. 먼저 메쉬와 그 모든 버텍스를 선택합니다:

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
