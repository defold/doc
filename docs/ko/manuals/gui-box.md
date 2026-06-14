---
title: Defold의 GUI box 노드
brief: 이 매뉴얼은 GUI box 노드를 사용하는 방법을 설명합니다.
---

# GUI box 노드

box 노드는 색상, 텍스쳐 또는 애니메이션으로 채워진 사각형입니다.

## box 노드 추가하기

새 box 노드는 *Outline*에서 <kbd>오른쪽 클릭</kbd>한 뒤 <kbd>Add ▸ Box</kbd>를 선택하거나, <kbd>A</kbd>를 누른 뒤 <kbd>Box</kbd>를 선택하여 추가합니다.

GUI에 추가된 아틀라스 또는 타일 소스의 이미지와 애니메이션을 사용할 수 있습니다. 텍스쳐는 *Outline*의 *Textures* 폴더 아이콘을 <kbd>오른쪽 클릭</kbd>하고 <kbd>Add ▸ Textures...</kbd>를 선택하여 추가합니다. 그런 다음 box 노드의 *Texture* 프로퍼티를 설정합니다.

![Textures](images/gui-box/create.png)

box 노드의 색상이 그래픽에 틴트된다는 점에 유의하세요. 틴트 색상은 이미지 데이터에 곱해지므로, 색상을 흰색(기본값)으로 설정하면 틴트가 적용되지 않습니다.

![Tinted texture](images/gui-box/tinted.png)

box 노드는 텍스쳐가 할당되지 않았거나, 알파가 `0`으로 설정되었거나, 크기가 `0, 0, 0`으로 설정되어도 항상 렌더링됩니다. 렌더러가 box 노드를 올바르게 배치로 묶고 드로우콜 수를 줄일 수 있도록 box 노드에는 항상 텍스쳐를 할당해야 합니다.

## 애니메이션 재생하기

box 노드는 아틀라스 또는 타일 소스의 애니메이션을 재생할 수 있습니다. 자세한 내용은 [플립북 애니메이션 매뉴얼](/manuals/flipbook-animation)을 참고하세요.

:[Slice-9](../shared/slice-9-texturing.md)
