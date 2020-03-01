The *Blend Mode* property defines how the component graphics should be blended with the graphics behind it. These are the available blend modes and how they are calculated:

Alpha
: Normal blending: a~0~ * rgb~0~ + (1 - a~0~) * rgb~1~

Add
: Brighten the background with the color values of the corresponding pixels of the component: rgb~0~ + rgb~1~

Multiply
: Darken the background with values of the the corresponding pixels of the component: rgb~0~ * rgb~1~
