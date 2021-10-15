The *Blend Mode* property defines how the component graphics should be blended with the graphics behind it. These are the available blend modes and how they are calculated:

Alpha
: Normal blending: `src.a * src.rgb + (1 - src.a) * dst.rgb`

Add
: Brighten the background with the color values of the corresponding pixels of the component: `src.rgb + dst.rgb`

Multiply
: Darken the background with values of the corresponding pixels of the component: `src.rgb * dst.rgb`

Screen
: Opposite of Multiply. Brighten background and values of the corresponding pixels of the component: `src.rgb - dst.rgb * dst.rgb`
