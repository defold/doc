---
brief: In this tutorial you will convert a shader from shadertoy.com to Defold.
layout: tutorial
locale: en
title: Shadertoy to Defold tutorial
---

# Shadertoy tutorial

[Shadertoy.com](https://www.shadertoy.com/) is a site that gathers user contributed GL shaders. It is a great resource for finding shader code and inspiration. In this tutorial we will take a shader from Shadertoy and make it run in Defold. Some basic understanding of shaders is assumed. If you need to read up, [the Shader manual](/manuals/shader/) is a good place to start.

The shader we will use is [Star Nest](https://www.shadertoy.com/view/XlfGRj) by Pablo Andrioli (user "Kali" on Shadertoy). It is a purely procedural mathematical black magic fragment shader that renders a really cool star field effect.

![Star Nest](../images/shadertoy/starnest.png)

The shader is just 65 lines of quite complicated GLSL code, but don't worry. We're gonna treat it as a black box that does its thing based on a few simple inputs. Our job here is to modify the shader so it interfaces with Defold instead of Shadertoy.

## Something to texture

The Star Nest shader is a pure fragment shader, so we only need something for the shader to texture. There are a number of options: a sprite, a tilemap, a GUI or a model. For this tutorial we are going to use a simple 3D model. The reason is that we can easily make the model rendering into a full screen effect---something we need to do if we want to do visual post processing, for example.

We can start from an empty project.

1. Open Defold and select Create From *Templates*.
2. Select *Empty Project*.
3. Set the *Title* and selection *Location* on your disk.
4. Click <kbd>Create New Project</kbd>.

![start](../images/shadertoy/empty_project.png)

You can use a built-in built-in `quad.gltf` mesh from `builtins/assets/meshes`.

Optionally, you can also create a quadratic plane mesh in Blender, or any other 3D modelling program --- for convenience the 4 vertex coordinates are at -1 and 1 on the X-axis and -1 and 1 on the Y axis. Blender has the Z-axis up by default so you need to rotate the mesh 90° around the X-axis. You should also make sure that you generate correct UV-coordinates for the mesh. In Blender, enter *Edit Mode* with the mesh selected, then select <kbd>Mesh ▸ UV unwrap... ▸ Unwrap</kbd>.

<div class='sidenote' markdown='1'>
Blender is a free, open-source 3D software which can be downloaded from [blender.org](https://www.blender.org).
</div>

![quad in Blender](../images/shadertoy/quad_blender.png)

1. Open your "main.collection" file in Defold and create a new game object "star-nest".
2. Add a *Model* component to the "star-nest" game object.
3. Set the *Mesh* property to our `quad.gltf`.
4. We need to set the material for the model, so for now select the built-in `model.material`.

The model should appear in the scene editor, but it is rendered all black. That is because it has no texture set yet:

![quad in Defold](../images/shadertoy/quad_default_material.png)

## Creating the material

1. Create a new material file *`star-nest.material`* by clicking <kbd>Right Mouse Button</kbd> on the `main` folder in the `Assets` pane and selecting <kbd>New</kbd>-><kbd>Material</kbd> and naming it `star-nest`.

 ![material](../images/shadertoy/new_material.png)

2. In the same way create a vertex shader program `star-nest.vp` and a fragment shader program `star-nest.fp`:
3. Open the *star-nest.material*.
4. Set the *Vertex Program* to `star-nest.vp`.
5. Set the *Fragment Program* to `star-nest.fp`.
6. Add a *Vertex Constant* and name it "`view_proj`" of type `Viewproj` (for "view projection").
8. Add a tag "tile" to the *Tags*. This is so that the quad is included in the render pass when sprites and tiles are drawn.

 ![material](../images/shadertoy/material.png)

### Vertex program

1. Open the vertex shader program file `star-nest.vp`. It should contain the following code:

    ```glsl
    #version 140

    // positions are in world space
    in vec4 position;
    in vec2 texcoord0;

    out vec2 var_texcoord0;

    uniform vertex_inputs
    {
        mat4 view_proj;
    };

    void main()
    {
        gl_Position = view_proj * vec4(position.xyz, 1.0);
        var_texcoord0 = texcoord0;
    }
    ```

### Fragment program

1. Open the fragment shader program file `star-nest.fp` and modify the code so the fragment color is set based on the X and Y coordinates of the UV coordinates (`var_texcoord0`). We do this to make sure we have the model set up correctly:

    ```glsl
    #version 140

    in vec2 var_texcoord0;

    out vec4 out_fragColor;

    void main()
    {
        out_fragColor = vec4(var_texcoord0.xy, 0.0, 1.0);
    }
    ```

2. Set the `Material` property to our newly created `star-nest` material on the model component in the `star-nest` game object in the `main.collection`.

Now the editor should render the model with the new shader and we can clearly see if the UV coordinates are correct; the bottom left corner should have black color (0, 0, 0), the top left corner green color (0, 1, 0), the top right corner yellow color (1, 1, 0) and the bottom right corner should have red color (1, 0, 0):

![quad in Defold](../images/shadertoy/quad_material.png)

## Camera

We can now run our project (<kbd>Project</kbd>-><kbd>Build</kbd> or shortcut <kbd>Ctrl</kbd>/<kbd>Cmd</kbd> + <kbd>B</kbd>), but we will see a black screen (well, almost, except maybe one tiny pixel in the bottom left corner). This is because there is no camera, and default render script uses a simple fallback, that is showing a huge 2D space, while our model is in (0,0,0) position with only 1 width.

Let's add a game object with a camera component to define what we'll see in the game.

1. Add a game object named `camera` with position (0,0,1). (It's important to set Z coordinate to 1, so that this game object is in front of our model, as Z axis is pointing now, in the default 2D setup, towards us).
2. Add a `Camera` component and you'll see a camera preview with our quad inside. With the default properties we are fortunate enough in such a setting to not need to change anything and we should already see the correct result, except only one thing - we don't need such a huge camera view frustum, so we can reduce the `Far Z` to `2`.

![camera](../images/shadertoy/camera.png)

Optionally, we can change the camera type by setting `Orthographic Projection` to `true`, and then also adjust the `Orthographic Zoom` to something like 600, but in this case we won't have an automatic aspect ratio, so our model won't fill our screen.

## The star nest shader

Now everything is in place let's start working on the actual shader code. Let's first take a look at the original code. It consists of a few sections:

![Star Nest shader code](../images/shadertoy/starnest_code.png)

We will use a modern pipeline with GLSL in version 140 - to do so, we'll declare the version on top of the file with `#version 140`.

1. Lines 5--18 defines a bunch of constants. We can leave these as is. They are plain GLSL constants and do not depend on Shadertoy or Defold specifically.

2. Lines 21 and 63 contains the input fragment X and Y screen space texture coordinates (`in vec2 fragCoord`), and output fragment color (`out vec4 fragColor`).

    Defold passes texture coordinates from the vertex shader to the fragment shader through an interpolated variable as UV coordinates (in the range 0--1). In our vertex shader this is declared with an `out` qualifier:

    ```glsl
    // in star-nest.vp
    out vec2 var_texcoord0;
    ```

     In the fragment shader the same value is received with an `in` qualifier:

    ```glsl
    // in star-nest.fp
    in vec2 var_texcoord0;
    ```

    Then, in GLSL 140, we declare an explicit fragment output with `out` qualifier:

    ```glsl
    // in star-nest.fp
    out vec4 out_fragColor;
    ```

    So where the original Shadertoy code writes to `fragColor`, our Defold shader writes to `out_fragColor`.

3. Lines 23--27 sets up the dimensions of the texture as well as movement direction and scaled time. In Shadertoy, the shader receives the pixel position through `fragCoord` and the viewport resolution of the viewport/texture is passed to the shader as `uniform vec3 iResolution`. The shader calculates UV style coordinates with the right aspect ratio from the fragment coordinates and the resolution. Some resolution offsetting is also done to get a nicer framing.

    In Defold, we do not start from pixel coordinates. Instead, we already receive normalized UV coordinates from the vertex shader through `var_texcoord0`. These coordinates are in the `0.0` to `1.0` range across the rendered quad.

    The Defold version needs to alter these calculations to use the UV coordinates from `var_texcoord0`.
    A typical conversion looks like this:

    ```glsl
    vec2 uv = var_texcoord0.xy;
    uv = uv * 2.0 - 1.0;
    uv.x *= aspect;
    ```
    The exact aspect value depends on how the example is set up. If the effect is rendered on a full-screen quad with a known display size, the aspect ratio can be hardcoded for the tutorial. If the effect needs to support arbitrary window sizes, pass the resolution as a fragment constant and place it inside a GLSL 140 uniform block.

    Time is also set up here. It is passed to the shader as `uniform float iGlobalTime`. Defold (since 1.12.3) provides time to shaders via a special `Time` constant that we'll use.

    In modern Defold, non-opaque uniforms are declared inside uniform blocks.
    In the fragment shader we declare it like this:

    ```glsl
    uniform fragment_inputs
    {
        vec4 time;
    };
    ```

    Then, in the `star-nest.material`, we will add a Fragment Constant named `time` and set its type to `Time`.

    The value can then be used like this:

    ```glsl
    float iGlobalTime = time.x;
    float dt = time.y;
    ```
    where `time.x` is the time since engine start, and `time.y` is the delta time from the previous frame.

4. Lines 29--39 sets up the rotation of the volumetric rendering, with mouse position affecting the rotation. The mouse coordinates are passed to the shader as `uniform vec4 iMouse`.

    For this tutorial we are going to skip mouse input.

5. Lines 41--62 is the core of the shader. We can leave this code as is.

## The modified star nest shader

Going through the sections above and doing the necessary changes results in the following shader code. It has been cleaned up a little for better readability. The differences between the Defold and Shadertoy versions are noted:

```glsl
#version 140 // <1>

// Star Nest by Pablo Román Andrioli
// This content is under the MIT License.

#define iterations 17
#define formuparam 0.53

#define volsteps 20
#define stepsize 0.1

#define zoom   0.800
#define tile   0.850
#define speed  0.010

#define brightness 0.0015
#define darkmatter 0.300
#define distfading 0.730
#define saturation 0.850

in vec2 var_texcoord0; // <2>

out vec4 out_fragColor; // <3>

uniform fragment_inputs // <4>
{
	vec4 time;
};

void main() // <5>
{
	// get coords and direction
	vec2 res = vec2(1.0, 1.0); // <6>
	vec2 uv = var_texcoord0.xy * res.xy - 0.5;
	vec3 dir = vec3(uv * zoom, 1.0);

	float iGlobalTime = time.x; // <7>
	float shader_time = iGlobalTime * speed;

	float a1 = 0.5; // <8>
	float a2 = 0.8;
	mat2 rot1 = mat2(cos(a1), sin(a1), -sin(a1), cos(a1));
	mat2 rot2 = mat2(cos(a2), sin(a2), -sin(a2), cos(a2));

	dir.xz *= rot1;
	dir.xy *= rot2;

	vec3 from = vec3(1.0, 0.5, 0.5);
	from += vec3(shader_time * 2.0, shader_time, -2.0);
	from.xz *= rot1;
	from.xy *= rot2;

	// volumetric rendering
	float s = 0.1;
	float fade = 1.0;
	vec3 v = vec3(0.0);

	for (int r = 0; r < volsteps; r++) {
		vec3 p = from + s * dir * 0.5;

		// tiling fold
		p = abs(vec3(tile) - mod(p, vec3(tile * 2.0)));

		float pa = 0.0;
		float a = 0.0;

		for (int i = 0; i < iterations; i++) {
			// the magic formula
			p = abs(p) / dot(p, p) - formuparam;

			// absolute sum of average change
			a += abs(length(p) - pa);
			pa = length(p);
		}

		// dark matter
		float dm = max(0.0, darkmatter - a * a * 0.001);

		a *= a * a;

		// dark matter, don't render near
		if (r > 6) {
			fade *= 1.0 - dm;
		}

		v += fade;

		// coloring based on distance
		v += vec3(s, s * s, s * s * s * s) * a * brightness * fade;

		fade *= distfading;
		s += stepsize;
	}

	// color adjust
	v = mix(vec3(length(v)), v, saturation);

	out_fragColor = vec4(v * 0.01, 1.0); // <9>
}
```

1. We declare #version 140 at the top of the file to use Defold's modern GLSL pipeline. Then we leave the defines as is.
2. The vertex shader passes UV coordinates to the fragment shader through var_texcoord0. In GLSL 140, the fragment shader receives this interpolated value with the in qualifier.
3. In GLSL 140, the fragment shader should declare an explicit output variable instead of writing to gl_FragColor. Here we use out vec4 out_fragColor.
4. Defold's Time material constant is exposed to the shader through a uniform block. In star-nest.material, add a Fragment Constant named time and set its type to Time.
5. Shadertoy uses mainImage(out vec4 fragColor, in vec2 fragCoord). In Defold we use the normal void main() entry point, read the interpolated UV coordinates from var_texcoord0, and write the final color to out_fragColor.
6. For this tutorial we define a static resolution/aspect value for the rendering. Currently the model is square, so we can use vec2 res = vec2(1.0, 1.0);. With a rectangular model of size 1280×720, we could instead use vec2 res = vec2(1.78, 1.0); and multiply the UV coordinates with that to preserve the correct aspect ratio.
7. The original Shadertoy shader uses iGlobalTime. In this Defold version, time.x contains the time since engine start, so we assign it to a local iGlobalTime variable and use it to animate the camera movement through the star field.
8. We keep this tutorial simple by removing the iMouse values altogether. The rotation itself is still kept, because it reduces visual symmetry in the volumetric rendering.
9. Finally, the shader writes the resulting fragment color to out_fragColor.

Save the fragment shader program. The model should now be nicely textured with a star field in the Scene editor and in runtime:

![quad with starnest](../images/shadertoy/quad_starnest.png)


## Animation

The final piece of the puzzle is the introduction of time to make the stars move. Defold (since 1.12.3) provides this automatically through a fragment constant of type `Time`.

1. Open *star-nest.material*.
2. Add a *Fragment Constant* and name it "time".
3. Set its *Type* to `Time`.

![time constant](../images/shadertoy/time_constant.png)

And that's it! We already handle this `time` in the fragment shader. We are done!

## Exercises

A fun continuation exercise is to add the original mouse movement input to the shader. You will need to create a new Fragment Constant, this time of type `User` and update it in `on_input` in some script that is detecting mouse movement using the `go.set()` function and setting the input coordinates to the new constant.

Happy Defolding!
