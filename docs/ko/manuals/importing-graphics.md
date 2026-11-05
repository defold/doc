---
title: 2D 그래픽 임포트 및 사용하기
brief: 이 매뉴얼은 2D 그래픽을 임포트하고 사용하는 방법을 설명합니다.
---

# 2D 그래픽 임포트하기

Defold는 2D 게임에서 자주 사용되는 여러 종류의 시각 컴포넌트를 지원합니다. Defold로 정적 및 애니메이션 스프라이트, UI 컴포넌트, 파티클 효과, 타일 맵, 비트맵 폰트를 만들 수 있습니다. 이러한 시각 컴포넌트를 만들려면 먼저 사용하려는 그래픽이 들어 있는 이미지 파일을 임포트해야 합니다. 이미지 파일을 임포트하려면 컴퓨터 파일 시스템에서 파일을 드래그해 Defold 에디터의 *Assets pane* 안의 적절한 위치에 놓으면 됩니다.

![파일 임포트](images/graphics/import.png)

::: sidenote
아틀라스와 타일 소스에는 PNG 또는 JPEG 이미지를 사용하세요. 모델 텍스쳐용 KTX2 원본 텍스쳐도 임포트할 수 있습니다. 아래를 참고하세요.
:::

## KTX2 텍스쳐 {#ktx2-textures}

독립적인 *.ktx2* 파일을 *Assets* 창으로 드래그해 임포트한 다음 Model 컴포넌트의 메터리얼 텍스쳐 필드에 지정합니다. [glTF와 GLB 모델](/manuals/importing-models/#ktx2-textures)도 외부 KTX2 파일을 참조하거나 KTX2 이미지를 내장할 수 있습니다. 아틀라스, 타일 소스, 큐브맵 면 입력은 기존 이미지 포멧을 계속 사용합니다.

지원되는 KTX2 입력은 ETC1S/BasisLZ, UASTC, BC7 또는 8비트 R/RG/RGB/RGBA UNORM이나 sRGB 데이터를 사용하는 2D 텍스쳐입니다. KTX2 배열, 큐브맵, 볼륨, HDR 텍스쳐는 지원하지 않습니다. KTX2는 빌드 시 Defold의 *.texturec* 리소스로 처리되며 런타임은 KTX2 컨테이너를 읽지 않습니다.

KTX2 에셋을 열면 원본 포멧, 크기, 색 공간, 알파 메타데이터, 밉 레벨을 검사할 수 있습니다. *Outline*에서 개별 원본 밉 레벨을 선택할 수 있습니다. 텍스쳐 프로파일이 컴파일된 텍스쳐 크기를 바꾸거나 밉맵을 비활성화하더라도 여기에는 원본 이미지가 표시됩니다.

[텍스쳐 프로파일](/manuals/texture-profiles/#ktx2-source-textures)로 원본 포멧을 유지할지 다른 포멧으로 변환할지 선택합니다. 타겟 기기가 지원하는 출력 포멧을 선택하세요. 이미 손실 압축된 소스를 다시 압축하면 화질이 더 낮아질 수 있습니다. 이미지 처리 후 **Keep KTX2 Format**에서 다시 인코딩해야 하는 경우도 마찬가지입니다.

## Defold 에셋 만들기

이미지를 Defold에 임포트하면 Defold 전용 에셋을 만드는 데 사용할 수 있습니다:

![아틀라스](images/icons/atlas.png){.icon} Atlas
: 아틀라스는 서로 분리된 이미지 파일 목록을 포함하며, 이 파일들은 자동으로 더 큰 텍스쳐 이미지 하나로 결합됩니다. 아틀라스는 정지 이미지와 *Animation Groups*를 포함할 수 있으며, Animation Groups는 함께 플립북 애니메이션을 이루는 이미지 집합입니다.

  ![아틀라스](images/graphics/atlas.png)

[아틀라스 매뉴얼](/manuals/atlas)에서 아틀라스 리소스에 대해 자세히 알아보세요.

![타일 소스](images/icons/tilesource.png){.icon} Tile Source
: 타일 소스는 균일한 그리드에 배치된 작은 하위 이미지들로 구성되도록 이미 만들어진 이미지 파일을 참조합니다. 이런 복합 이미지를 흔히 _sprite sheet_라고도 합니다. 타일 소스는 애니메이션의 첫 번째 타일과 마지막 타일로 정의되는 플립북 애니메이션을 포함할 수 있습니다. 이미지를 사용해 타일에 충돌 모형을 자동으로 붙이는 것도 가능합니다.

  ![타일 소스](images/graphics/tilesource.png)

[타일 소스 매뉴얼](/manuals/tilesource)에서 타일 소스 리소스에 대해 자세히 알아보세요.

![비트맵 폰트](images/icons/font.png){.icon} Bitmap Font
: 비트맵 폰트는 PNG 폰트 시트에 글리프를 담고 있습니다. 이런 타입의 폰트는 TrueType 또는 OpenType 폰트 파일에서 생성된 비트맵 폰트에 비해 성능 향상을 제공하지는 않지만, 임의의 그래픽, 색상, 그림자를 이미지에 직접 포함할 수 있습니다.

[폰트 매뉴얼](/manuals/font/#bitmap-bmfonts)에서 비트맵 폰트에 대해 자세히 알아보세요.

  ![BMfont](images/font/bm_font.png)


## Defold 에셋 사용하기

이미지를 Atlas 및 Tile Source 파일로 변환한 후에는 이를 사용해 여러 종류의 시각 컴포넌트를 만들 수 있습니다:

![스프라이트](images/icons/sprite.png){.icon}
: 스프라이트는 화면에 표시되는 정지 이미지 또는 플립북 애니메이션입니다.

  ![스프라이트](images/graphics/sprite.png)

[스프라이트 매뉴얼](/manuals/sprite)에서 스프라이트에 대해 자세히 알아보세요.

![타일 맵](images/icons/tilemap.png){.icon} 타일 맵
: 타일맵 컴포넌트는 타일 소스에서 가져온 타일(이미지 및 충돌 모형)을 조합해 맵을 구성합니다. 타일 맵은 아틀라스 소스를 사용할 수 없습니다.

  ![타일맵](images/graphics/tilemap.png)

[타일 맵 매뉴얼](/manuals/tilemap)에서 타일맵에 대해 자세히 알아보세요.

![파티클 효과](images/icons/particlefx.png){.icon} Particle fx
: 파티클 emitter에서 스폰되는 파티클은 아틀라스 또는 타일 소스의 정지 이미지나 플립북 애니메이션을 사용합니다.

  ![파티클](images/graphics/particles.png)

[Particle FX 매뉴얼](/manuals/particlefx)에서 파티클 효과에 대해 자세히 알아보세요.

![GUI](images/icons/gui.png){.icon} GUI
: GUI box 노드와 파이 노드는 아틀라스 및 타일 소스의 정지 이미지와 플립북 애니메이션을 사용할 수 있습니다.

  ![GUI](images/graphics/gui.png)

[GUI 매뉴얼](/manuals/gui)에서 GUI에 대해 자세히 알아보세요.
