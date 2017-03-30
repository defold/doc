Texture profiles
=================
:location: documentation manuals project
:type: manual

Defold supports automatic texture processing and compression of image data (in *Atlas*, *Tile sources*, *Cubemaps* and stand-alone textures used for models, GUI etc). This manual describes the available functionality.

There are two types of compression, hardware texture compression and software image compression. Hardware texture compression reduce memory footprint and graphics hardware is able to manage compressed textures. Both hardware texture compression and software image compression reduces the size of image resources and the final bundle size. It should be noted that for example PNG file compression can sometimes yield smaller files, but PNG files need to be uncompressed when read into memory.

The processing of textures is configured through a specific texture profile. In this file you create _profiles_ that express what compressed format(s) and type should be used when creating bundles for a specific platform. _Profiles_ are then tied to matching file _paths patterns_, allowing fine tuned control over what files in your project should be compressed and exactly how.

Since all available hardware texture compression is lossy, you will get artifacts in your texture data. These artifacts are highly dependant on how your source material looks and what compression method is used. You should test your source material and experiment to get the best results. Google is your friend here.

You can select what software image compression is applied on the final texture data (compressed or raw) in the bundle archives. Defold supports WebP or ZLib (default). WebP supports both lossy and lossless compression and usually results in significantly better compression than ZLib, which is a general data compression algorithm.

::: sidenote
Compression is a resource intense and time consuming operation that can cause _very_ long build times depending on the amount of texture images to compress and also the chosen texture formats and type of software compression.
:::

## Texture profiles

Each project contain a specific *.texture_profiles* file that contain the configuration used when compressing textures. By default, this file is "builtins/graphics/default.texture_profiles" and is has a configuration matching every texture resource to a profile using RGBA with no hardware texture compression and using the default ZLib file compression.

To add texture compression:

- Select *File > New > Other...* and choose "Texture Profiles File" to create a new texture profiles file. (Alternatively copy "default.texture_profiles" to a location outside of "builtins")
- Change the *texture_profiles* entry on "game.project" to point to the new file.
- Open the *.texture_profiles* file and configure it according to your requirements.

![New profiles file](images/texture_profiles/texture_profiles_new_file.png)

![Setting the texture profile](images/texture_profiles/texture_profiles_game_project.png)

You can turn on and off the use of texture profiles in the editor preferences. Select *File > Preferences*. The *Defold* pane contains a checkbox item *Enable texture profiles*.

![Texture profiles preferences](images/texture_profiles/texture_profiles_preferences.png)

## Paths

The *path_settings* section of the texture profiles file contains a list of path regular expressions and the name of which *profile* to use when processing resources that match the path expression. The path regular expressions are expressed with "Ant Glob" patterns (see http://ant.apache.org/manual/dirtasks.html#patterns for details). Patterns can be expressed using the following wildcards:

'*'
: Matches zero or more characters. For instance "sprite*.png" matches the files "sprite1.png", "sprite.png" and "sprite_with_a_long_name.png".

'?'
: Matches exactly one character. For instance: "sprite?.png" matches the files "sprite1.png", "spriteA.png" but not "sprite.png" or "sprite_with_a_long_name.png".

\'**'
: Matches a complete directory tree, or--when used as the name of a directory--zero or more directories. For instance: "/gui/\\**" matches all files in the directory "/gui" and all its subdirectories.


![Paths](images/texture_profiles/texture_profiles_paths.png)

This example contains two path patterns and corresponding profile.

"/gui/\**/*.atlas"
: All *.atlas* files in directory "/gui" or any of its subdirectories will be processed according to profile "gui_atlas".

"/\**/*.atlas"
: All *.atlas* files anywhere in the project will be process according to the profile "atlas".


Note that the more generic path is put last. The matcher works top down. The first occurence that matches the resource path will be used. A matching path expression further down the list never overrides the first match. Had the paths been put in the opposite order every atlas would have been processed with profile "atlas", even the ones in directory "/gui".

Texture resources that _do not_ match any path in the profiles file will be compiled and rescaled to the closest power of 2, but will otherwise be left intact.

## Profiles

The *profiles* section of the texture profiles file contains a list of named profiles. Each profile contains one or more *plaforms*, each platform being described by a list of properties.

![Profiles](images/texture_profiles/texture_profiles_profiles.png)

*os*
: Specifies a matching OS platform. "OS\_ID\_GENERIC" matches all platforms including dev-app builds on device, "OS\_ID\_WINDOWS" matches Windows target bundles, "OS\_ID\_IOS" matches iOS bundles and so on. Note that if "OS\_ID\_GENERIC" is specified, it will be included for all platforms.

*formats*
: One or more texture formats to generate. If several formats are specified, textures for each format is generated and included in the bundle. The engine selects textures of a format that is supported by the runtime platform.

*mipmaps*
: For each platform, specify whether mipmaps should be generated. The property can be either "true" or "false".

*max_texture_size*
: If set to a non-zero value, textures are limited in pixel size to the specified number. Any texture that has a width or height larger than the specified value will be scaled down.


The *formats* added to a profile each has the following properties:

*format*
: The format to use when encoding the texture. See below for all available texture formats.

*compression_level*
: Selects the quality level for the resulting compressed image. The values range from "FAST" (low quality, fast compression) to "NORMAL", "HIGH" and "BEST" (highest quality, slowest compression).

*compression_type*
: Selects the type of compression used for the resulting compressed image, "COMPRESSION\_TYPE\_DEFAULT", "COMPRESSION\_TYPE\_WEBP" or "COMPRESSION\_TYPE\_WEBP\_LOSSY". see Compression type section for more details.

## Texture formats

Textures can be processed into uncompressed or *lossy* compressed data with various number of channels and bit depths. Compression that is fixed means that the resulting image will be of a fixed size, regardless of the image content. This means that the quality loss during compression depends on the content of the original texture.

The following lossy compression formats are currently supported.

//////////////////////////////////////////
DXT
: Also called S3 Texture Compression. It can be generated on Windows platform only, but OS X supports reading it and it's possible to install support for it on Linux. The format divides the image into 4x4 pixel blocks with 4 colors set to the pixels within each block.

//////////////////////////////////////////

PVRTC
: Textures are compressed in blocks. In 4 bit mode (4BPP) one block has 4×4 pixels. In 2 bit mode (2BPP) one block are 8×4 pixels. One block always occupies 64 bits (8 bytes) of memory space.  The format is used in all generations of the iPhone, iPod Touch, and iPad. (certain Android devices, that use PowerVR GPUs also support the format). Defold supports PVRTC1, as indicated by the suffix "V1" in the format identifiers.


ETC
: Ericsson Texture Compression. Blocks of 4x4 pixels are compressed into a single 64-bit word. The 4x4 block is divided in half and each half is assigned a base color. Each pixel is then encoded as one of four offset values from the base color of its half. Android supports ETC1 since version 2.2 (Froyo). Defold compresses ETC1 textures.


[.table-striped]
|===========================
| Format | Compression | Color | Note

| TEXTURE\_FORMAT\_LUMINANCE
| none
| One channel gray-scale, no alpha
| RGB channels multiplied into one. Alpha is discarded.

| TEXTURE\_FORMAT\_RGB
| none
| 3 channel color
| Alpha is discarded

| TEXTURE\_FORMAT\_RGBA
| none
| 3 channel color and full alpha
|

| TEXTURE\_FORMAT\_RGB\_PVRTC2BPPV1
| 1:16 fixed
| No alpha
| Requires square images. Non square images will be resized.

| TEXTURE\_FORMAT\_RGB\_PVRTC4BPPV1
| 1:8 fixed
| No alpha
| Requires square images. Non square images will be resized.

| TEXTURE\_FORMAT\_RGBA\_PVRTC2BPPV1
| 1:16 fixed
| Pre-multiplied alpha
| Requires square images. Non square images will be resized.

| TEXTURE\_FORMAT\_RGBA\_PVRTC4BPPV1
| 1:8 fixed
| Pre-multiplied alpha
| Requires square images. Non square images will be resized.

| TEXTURE\_FORMAT\_RGB\_ETC1
| 1:6 fixed
| No alpha
|

|===========================

//////////////////////////////////////////
| TEXTURE\_FORMAT\_RGB\_DTX1
| 1:8 fixed
| No alpha
| Can be compressed on Windows only

| TEXTURE\_FORMAT\_RGBA\_DTX1
| 1:8 fixed
| 1 bit alpha
| Can be compressed on Windows only

| TEXTURE\_FORMAT\_RGBA\_DXT3
| 1:4 fixed
| 4 bit fixed alpha
| Can be compressed on Windows only

| TEXTURE\_FORMAT\_RGBA\_DXT5
| 1:4 fixed
| Interpolated smooth alpha
| Can be compressed on Windows only
//////////////////////////////////////////

## Compression types

COMPRESSION\_TYPE\_DEFAULT
: Default ZLib generic lossless data compression.

COMPRESSION\_TYPE\_WEBP
: WebP lossless compression. Higher quality level results in smaller size.<br>For hardware compressed texture formats PVRTC or ETC, the compression process transforms the compressed hardware texture format data into data more suitable for WebP image compression using an internal intermediate format. This is then transformed back into the compressed hardware texture format when loaded by the run-time.

COMPRESSION\_TYPE\_WEBP\_LOSSY
: WebP lossy compression. Lower quality level results in smaller size.<br>WebP lossy type is currently not supported for hardware compressed texture formats.

