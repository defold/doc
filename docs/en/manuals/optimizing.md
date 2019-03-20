---
title: Optimizing an application
brief: This manual explains various ways to identify areas to optimize.
---

# Introduction



## Storage and run-time size of graphics

It is important to always keep in mind the limitations of your target platform(s). On mobile devices it is especially important to keep an eye on the both application size and the size the images take up when loaded into memory. When you bundle your game you can also [generate a build report](/manuals/profiling/#_build_reports) containing a breakdown of content included in your application bundle. You can use this to inspect the size on disk and make decisions about reducing the size of certain images or applying image compression (and perhaps also compress audio which usually takes up quite a bit of space).

![](images/profiling/build_report_html.png)

For things such as background images it might for instance be ok to use a small image and scale it up to the desired size. This kind of image size optimization is done on the image before it is added to Defold in an atlas or a tilesource. Once the reduced size image is imported it can be scaled using the normal scale property of a game object or component depending on where it is supposed to be used.

It can also be acceptable to apply compression on images to reduce both storage size and run-time memory usage. Defold supports automatic texture processing and compression of image data using something called texture profiles. The texture profiles match groups of files or individual files to different texture compression algorithms with an option to apply different compression algorithms based on the target platform. You can also use the texture profiles system to disable mipmaps for content that isn't scaled to save further storage space. You can read more about how to use this system in the [Texture Profiles manual](/manuals/texture-profiles/).


## Reducing CPU usage

## Reducing GPU usage

## Reducing battery consumption
