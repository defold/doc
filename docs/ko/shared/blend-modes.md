*Blend Mode* 프로퍼티는 컴포넌트 그래픽을 그 뒤에 있는 그래픽과 어떻게 블렌딩할지 정의합니다. 사용 가능한 블렌드 모드와 계산 방식은 다음과 같습니다:

Alpha
: 일반 블렌딩: `src.a * src.rgb + (1 - src.a) * dst.rgb`

Add
: 컴포넌트의 대응하는 픽셀 색상 값으로 배경을 밝게 합니다: `src.rgb + dst.rgb`

Multiply
: 컴포넌트의 대응하는 픽셀 값으로 배경을 어둡게 합니다: `src.rgb * dst.rgb`

Screen
: Multiply의 반대입니다. 컴포넌트의 대응하는 픽셀 값과 배경을 밝게 합니다: `src.rgb - dst.rgb * dst.rgb`
