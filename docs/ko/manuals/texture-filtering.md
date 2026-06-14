---
title: 텍스쳐 필터링
brief: 이 매뉴얼은 그래픽을 렌더링할 때 텍스쳐 필터링에 사용할 수 있는 옵션을 설명합니다.
---

# 텍스쳐 필터링과 샘플링

텍스쳐 필터링은 _텍셀_(텍스쳐 안의 픽셀)이 화면 픽셀과 완벽하게 정렬되지 않는 경우의 시각적 결과를 결정합니다. 텍스쳐를 포함한 그래픽 요소를 1픽셀보다 적게 이동할 때 이런 일이 발생합니다. 다음 필터 방식들을 사용할 수 있습니다.

Nearest
: 화면 픽셀에 색을 입히기 위해 가장 가까운 텍셀이 선택됩니다. 텍스쳐에서 화면에 보이는 결과까지 완전한 일대일 픽셀 매핑을 원한다면 이 샘플링 방식을 선택해야 합니다. nearest 필터링을 사용하면 이동할 때 모든 것이 픽셀 단위로 스냅됩니다. 스프라이트가 느리게 움직이면 움직임이 떨려 보일 수 있습니다.

Linear
: 화면 픽셀에 색을 입히기 전에 텍셀이 이웃 텍셀들과 평균화됩니다. 스프라이트가 픽셀을 완전히 색칠하기 전에 주변 픽셀로 번지므로, 느리고 연속적인 움직임에서 부드러운 모습을 만들며 스프라이트를 한 픽셀보다 적게 이동할 수 있습니다.

사용할 필터링 설정은 [프로젝트 설정](/manuals/project-settings/#graphics) 파일에 저장됩니다. 설정값은 두 가지입니다.

default_texture_min_filter
: 텍셀이 화면 픽셀보다 작을 때마다 축소 필터링이 적용됩니다.

default_texture_mag_filter
: 텍셀이 화면 픽셀보다 클 때마다 확대 필터링이 적용됩니다.

두 설정 모두 `linear`, `nearest`, `nearest_mipmap_nearest`, `nearest_mipmap_linear`, `linear_mipmap_nearest` 또는 `linear_mipmap_linear` 값을 받을 수 있습니다. 예:

```ini
[graphics]
default_texture_min_filter = nearest
default_texture_mag_filter = nearest
```

아무것도 지정하지 않으면 둘 다 기본값으로 `linear`가 설정됩니다.

*game.project*의 설정은 기본 샘플러에서 사용됩니다. 커스텀 메터리얼에서 샘플러를 지정하면 각 샘플러마다 필터 방식을 따로 설정할 수 있습니다. 자세한 내용은 [메터리얼 매뉴얼](/manuals/material/)을 참고하세요.
