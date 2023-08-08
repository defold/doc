---
title: Release checklist
brief: This manual contains a helpful guide and checklist of things to consider when releasing your game.
---

# Release checklist

This page contains a helpful guide and checklist of things to consider when releasing a game. You should also pay attention to the [Porting Guidelines document](/manuals/porting-guidelines/) for additional helpful tips, especially when releasing your game on a new platform.

## General advice

* **Display sizes** - Is everything looking good on a larger or smaller screen than the default width and height set in game project?
  * The projection used in the render script and the layouts used in the gui will play a role here.
* **Aspect ratios** - Is everything looking good on a screen with a different aspect ratio than the default aspect ratio from the width and height set in game project?
  * The projection used in the render script and the layouts used in the gui will play a role here.
* **Refresh rate** - Is the game running well on a screen with a higher refresh rate than 60 Hz?
  * The vsync and swap interval in the Display section of game.project 


## Text presented to your users

* **Localization** - Translate any text in the game as well as the text in the store page as this will have a positive impact on sales! For the localization, make sure it is possible to easily swap between different languages in-game (via the pause menu).


## Store materials

* **App icon** - Make sure your game stands out from the competition. The icon is often your first point of contact with potential players. It should be easy to find on a page full of game icons.

* **Store banners and images** - Make sure to use impactful and exciting art for your game. It is probably worth spending some money to work with an artist to create art that attracts players.



MORE HERE: https://forum.defold.com/t/checklist-for-release/72516/17?u=britzl


## Build artifacts

* Make sure to [generate debug symbols](/manuals/debugging-native-code/#symbolicate-a-callstack) for each released version so that you can debug crashes.
* Make sure to store the `manifest.private.der` and `manifest.public.der` files which are generated in the project root during the first bundle. These are the public and private signing keys for the game archive and archive manifest. You need these files in order to recreate a previous build of your game.


## Android

* Make sure to store your [keystore](/manuals/android/#creating-a-keystore) somewhere safe so that you can update your game.


## Consoles

* Store the complete bundle for each version. You will need these files if you want to patch the game.