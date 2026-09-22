*Blend Mode* プロパティは、コンポーネント（component）のグラフィックスを、その背後のグラフィックスとどのようにブレンドするかを定義します。使用できるブレンドモード（blend mode）とその計算方法は次のとおりです:

Alpha
: 通常のブレンド: `src.a * src.rgb + (1 - src.a) * dst.rgb`

Add
: コンポーネントの対応するピクセルの色の値で、背景を明るくします: `src.rgb + dst.rgb`

Multiply
: コンポーネントの対応するピクセルの値で、背景を暗くします: `src.rgb * dst.rgb`

Screen
: Multiply とは逆の処理です。背景とコンポーネントの対応するピクセルの値を明るくします: `src.rgb - dst.rgb * dst.rgb`
