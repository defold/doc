---
title: Defold development for the Windows platform
brief: This manual describes how to build and run Defold applications on Windows
---

# Windows development

Developing Defold applications for the Windows platform is a straight forward process with very few considerations to make.

## Project settings

Windows specific application configuration is done from the [Windows section](/manuals/project-settings/#windows) of the *game.project* settings file.

## Application icon

The application icon used for a Windows game must be in the .ico format. You can easily create a .ico file from a .png file using an online tool such as [ICOConvert](https://icoconvert.com/). Upload an image and use the following icon sizes:

![Windows icon sizes](images/windows/windows-icon.png)

## Facebook Gameroom

Facebook Gameroom for PC gaming is a Windows-native client available as a free download for players worldwide. Within Facebook Gameroom, players can experience both web games and also native games built exclusively for the platform. When bundling for Windows there is an option in the *game.project* settings file to select Gameroom as an IAP provider. Learn more about Facebook Gameroom in the [Gameroom manual](/manuals/gameroom).
