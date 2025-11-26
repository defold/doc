---
title: Editor overview
brief: This manual gives an overview on how the Defold editor look and works, and how to navigate in it.
---

# Editor overview

The editor allows you to browse and manipulate all files and folders in your game project in an efficient manner. Editing files brings up a suitable editor and shows all relevant information about the file in separate views.

## Starting the Editor

When you run the Defold Editor, you are presented with a project selection and creation screen. Click to select what you want to do:

#### MY PROJECTS
Click to show your recently opened projects so you can quickly access them. This is the default view.

If you didn't open any projects earlier, it will show a view like on the left  - you can click `Open From Disk…` to open one using system file browser or click `Create New Project` button and it will switch to a tab `TEMPLATES`, otherwise it will show a list of your projects, like on the right on the below picture:

  ![my projects](images/editor/my_projects.png)

#### TEMPLATES
Contains empty or almost empty basic projects made for quick start of a new Defold project for certain platforms or using certain extensions.

#### TUTORIALS
Contains projects with guided tutorials to learn, play and modify, if you would like to follow a tutorial.

#### SAMPLES
Contains projects prepared to showcase certain use cases.

  ![new project](images/editor/new_project.png)

When you create a new project it is stored on your local drive and any edits you do are saved locally.

You can learn more about the different options in the [Project Setup manual](https://www.defold.com/manuals/project-setup/).

## The Editor panes

The Defold Editor is separated into a set of panes, or views, that display specific information.

![Editor 2](images/editor/editor_overview.png)

### 1. Assets pane
Lists all the files and folders that are part of your project in a tree structure, corresponding to the same structure on your disk. Click and scroll to navigate the list. All file oriented operations can be made in this view:

   - <kbd>Left Mouse Click</kbd> to select any file or folder, and while holding <kbd>⇧ Shift</kbd> you can expand selection or while holding <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> you can (un)select clicked.
   - <kbd>Double Mouse Click</kbd> a file to open it in a specific editor for that file type.
   - <kbd>Drag and Drop</kbd> to add files from elsewhere on your disk to the project or move files and folders to new locations in the project.
   - <kbd>Right Mouse Click</kbd> to open a _Context Menu_ from where you can create new files or folders, rename, delete, track file dependencies and more.

### 2. Editor pane
The center view shows the currently open file in a specific editor for that file type, for example script files are opened in the built-in Code Editor, while visual components - in 3D Visual Editor. All Visual Editors allows you to change the camera view:

- Pan: <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Left Mouse Button</kbd> or <kbd>Right Mouse Button</kbd>
- Zoom: <kbd>Scroll Mouse Wheel</kbd> or <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Right Mouse Button</kbd>.
- Rotate in 3D around selection: <kbd>Ctrl</kbd>/<kbd>^ Control</kbd> + <kbd>Left Mouse Button</kbd>.

#### Toolbar
There is a toolbar in the top right corner of the scene view where you can find object manipulation tools (from left):

*Move* (<kbd>W</kbd>), *Rotate* (<kbd>E</kbd>), *Scale* (<kbd>R</kbd>), *Grid Settings* `▦`, *Align Camera 2D/3D* `2D`, *Camera Perspective/Orthographic Toggle* and *Visibility Filters* `👁`.

![toolbar](images/editor/toolbar.png)

### 3. Outline pane

This view shows the content of the file currently being edited, but in a hierarchical tree structure. The Outline reflects the editor view and allows you to perform operations on your items:

   - <kbd>Left Mouse Click</kbd> to select an item, and while holding <kbd>⇧ Shift</kbd> you can expand selection or while holding <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> you can (un)select clicked.
   - <kbd>Drag and drop</kbd> to move items. Drop a game object on another game object in a collection to create a parent-child relationship.
   - <kbd>Right Mouse Click</kbd> to open a _Context Menu_ from where you can add items, delete selected items etc.

It is possible to toggle the visibility of game objects and visual components by clicking on the little `👁` Eye Icon to the right of an element in the list (Defold 1.9.8 and newer).

![toolbar](images/editor/outline.png)

### 4. Properties pane

This view shows properties associated with the currently selected item, like Id, URL, Position, Rotation, Scale, and/or other component specific properties and also custom properties for scripts.

You can also <kbd>Drag</kbd> the `↕` Up-Down Arrow and move mouse to change value of the given numerical property (1.10.2+).

![toolbar](images/editor/properties.png)

### 5. Tools pane

This view has several tabs.

*Console* tab : shows any error, warning and info engine output or purposeful printing that you do while your game is running,

*Build Errors* : shows errors from the building process,

*Search Results* : shows results of searching (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd> + <kbd>F</kbd>) the whole project, if you click `Keep Results`

*Curve Editor* : used when editing curves in the [Particle Editor](/manuals/particlefx/).

The Tools pane is also used for interacting with the integrated debugger. Read more about it in the [Debugging Manual](/manuals/debugging/).

### 6. Changed Files pane

If your project uses the distributed version-control system Git this view lists any files that has been changed, added or deleted in your project. By synchronizing the project regularly you can bring your local copy in sync with what is stored in the project Git repository, that way you can collaborate within a team, and you won’t lose your work if disaster strikes. You can learn more about Git in our [Version Control manual](/manuals/version-control/). Some file oriented operations can be performed in this view:

   - <kbd>Left Mouse Click</kbd> - to select a given file, and while holding <kbd>⇧ Shift</kbd> you can expand selection or while holding <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> you can (un)select clicked. If a single changed file is selected you can click `Diff` to show the differences. You can click `Revert` to undo changes in all selected files.
   - <kbd>Double Left Mouse Click</kbd> a file to open a view of the file. The editor opens the file in a suitable editor, just like in the assets view.
   - <kbd>Right Mouse Click</kbd> a file to open a pop up menu from where you can open a diff view, revert all changes done to the file, find the file on the filesystem and more.

### Menu Bar

On the top of the Editor view or in System Bar on Mac you can find Menu Bar with 6 menus: `File`, `Edit`, `View`, `Project`, `Debug`, `Help`. Their functions will be explained in the manuals.

### Status Bar

On the bottom bar of the Editor you can find a narrow space in which the Status is displayed, e.g.:
- when a new update is available a clickable button `Update Available` will be visible - check section Updating the Editor in this manual below.
- when building or bundling a progress of it will be presented there.

## Panes Size and Visibility

Panes size can be adjusted inside the Editor by <kbd>Dragging</kbd> the section borders between all described above 6 Panes.

Panes visibility can be toggled in the Editor by using options in `View` menu or using given shortcuts:
- `Toggle Assets Pane` (<kbd>F6</kbd>) to toggle Assets and Changed Files Panes visibility
- `Toggle Changed Files` to toggle visibility of the Changed Files Pane alone
- `Toggle Tools Pane` (<kbd>F7</kbd>) to toggle Tools Pane visibility
- `Toggle Properties Pane` (<kbd>F8</kbd>) to toggle Outline and Properties Panes visibility

![Panes Visibility](images/editor/editor_panes.png)

In the `View` menu you can also toggle or change other visibility related settings, like Grid, Guides, Camera or fit the view to selection (`Frame Selection` or <kbd>F</kbd> key) and toggle between default 2D and 3D view (`Realign Camera` or <kbd>.</kbd> key), many of them accessible from the Toolbar or via shortcuts too.

## Tabs

If you have multiple files open, a separate tab for each file is shown at the top of the Editor view.  Tabs in a single pane can be moved around - <kbd>Drag and Drop</kbd> them to swap their positions inside the tabs bar. You can also:

- <kbd>Right Mouse Click</kbd> on a tab to open a _Context Menu_,
- Click `Close` (<<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>W</kbd>) a single tab,
- Click `Close Others` to close all tabs except the selected one,
- Click `Close All` (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd>+<kbd>W</kbd>) to close all tabs in the active pane,
- Select `➝| Open As` - to use other than default editor or associated external tool set in `Preferences ▸ Code ▸ Custom Editor`. Check more in [Preferences manual](/manuals/editor-preferences).

![Tabs](images/editor/tabs.png){.inline} ![Tabs](images/editor/tabs_custom.png){.inline}

## Side-by-side editing

It is possible to open 2 editor views side by side.

- <kbd>Right Mouse Click</kbd> the tab for the editor you want to move and select `Move to Other Tab Pane`.

![2 panes](images/editor/2-panes.png)

You can also use the tab menu to `Swap with Other Tab Pane` to move given tab between panes or `Join Tab Panes` to a single pane.

## The Scene Editor

Double clicking a collection or game object or visual component file brings up the *Scene Editor*. By default, all visual scenes open with a 2D orthographic perspective:

![Scene Editor](images/editor/2d_scene.png)

If you are working with a 3D project it is worth to check the Toolbar and adjust the *Grid Settings* `▦` e.g. realign camera to toggle 2D/3D `2D` (or <kbd>.</kbd> key), set grid to be displayed on Plane `Y` or any other that looks more intuitively to you and change the camera to perspective - using a toggle on the Toolbar or `View` &rarr; `Perspective Camera`:

![Scene Editor 3D](images/editor/3d_scene.png)

### Selecting objects

<kbd>Left Mouse Click</kbd> on objects in the main window to select them. The rectangle (or cuboid) surrounding the object in the editor view will highlight with cyan to indicate what item is selected. The selected object is also highlighted in the `Outline` view as in the picture above.

  You can also select objects by:

  - <kbd>Left Mouse Click</kbd> and <kbd>Drag</kbd> to select all objects inside the selection region.
  - <kbd>Left Mouse Click</kbd> objects in the `Outline`, and while holding <kbd>⇧ Shift</kbd> you can expand selection or while holding <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> you can (un)select clicked.

### Move tool <kbd>W</kbd>

![Move tool](images/editor/icon_move.png){.left}
To move objects, use the *Move Tool*. You can find it in the Toolbar in the top right corner of the scene editor, or by pressing the <kbd>W</kbd> key.

![Move object](images/editor/move.png){.inline}![Move object 3D](images/editor/move_3d.png){.inline}

The gizmo changes and shows a set of manipulators - squares and arrows (selected manipulator will turn to orange color) that you can <kbd>Drag</kbd> to move:

- one cyan center square handle to move the object only in the screen space,
- 3 red, green and blue arrows along each axis to move the object only along the given X, Y or Z axis.
- 3 red, green and blue square handles to move the object only on the given plane, e.g. X-Y (blue) and (visible if rotating the camera in 3D) X-Z (green) and Y-Z (red) planes.

### Rotate tool <kbd>E</kbd>

![Rotate tool](images/editor/icon_rotate.png) : 
To rotate objects, use the *Rotate Tool* by selecting it in the Toolbar, or by pressing the <kbd>E</kbd> key.

![Rotate object](images/editor/rotate.png){.inline}![Rotate object 3D](images/editor/rotate_3d.png){.inline}

This tool consists of four circular manipulators (selected manipulator will turn to orange color) that you can <kbd>Drag</kbd> to rotate:

- one cyan (outer, biggest circle) manipulator that rotates the object in the screen space
- 3 smaller red, green and blue circle manipulators allowing rotation around each of the X, Y and Z axes separately. For 2D orthographic view, the 2 of them are perpendicular to the X- and Y-axis, so the circles only appear as two lines crossing the object.


### Scale tool <kbd>R</kbd>

![Scale tool](images/editor/icon_scale.png){.left}
To scale objects, use the *Scale Tool* by selecting it in the toolbar, or by pressing the <kbd>R</kbd> key.

![Scale object](images/editor/scale.png){.inline}![Scale object 3D](images/editor/scale_3d.png){.inline}

This tool consists of a set of square/cube manipulators (selected manipulator will turn to orange color) that you can <kbd>Drag</kbd> to scale:

- one cyan cube in the center scales the object uniformly in all axes (including Z).
- 3 red, blue and green cube manipulators scale the object along each of the X, Y and Z axes separately.
- 3 red, blue and green cube manipulators scale the object in the X-Y plane, the X-Z plane or the Y-Z plane separately.


### Visibility filters

Click on the Visibility Eye Icon (`👁`) in the Toolbar to toggle visibility of various component types as well as bounding boxes and guide lines (`Component Guides` or shortcut <kbd>Ctrl</kbd> + <kbd>H</kbd> (Win/Linux) or <kbd>^ Ctrl</kbd> + <kbd>⌘ Cmd</kbd> + <kbd>H</kbd>(Mac)).

![Visibility filters](images/editor/visibilityfilters.png)


## Creating new project files

To create new resource files, either select `File ▸ New...` and then choose the file type from the menu, or use the context menu:

<kbd>Right Mouse Click</kbd> the target location in the `Assets` browser, then select `New... ▸ [file type]`:

![create file](images/editor/create_file.png)

Type a suitable *Name* for the new file and eventually change *Location*. The full file name including the file type suffix is shown under *Preview* in the dialog:

![create file name](images/editor/create_file_name.png)


## Templates

It is possible to specify custom templates for each project. To do so, create a new folder named `templates` in the project’s root directory, and add new files named `default.*` with the desired extensions, such as `/templates/default.gui` or `/templates/default.script`. Additionally, if the `{{NAME}}` token is used in these files, it will be replaced with the filename specified in the file creation window.

If a template is available for a given file type, whenever a new file of this type is created, it will be initialized with the content of the file from `templates`.


![Templates](images/editor/templates.png)

## Importing files to your project

To add asset files (images, sounds, models etc) to your project, simply drag and drop them to the correct position in the *Assets* browser. This will make _copies_ of the files at the selected location in the project file structure. Read more about [how to import assets in our manual](/manuals/importing-assets/).

![Import files](images/editor/import.png)

## Updating the Editor

The Editor will automatically check for updates when connected to internet. When an update is detected a blue clickable link `Update Available` will be shown in the lower left corner of the project selection screen or in the lower right corner of the Editor window.

![Update from project selection](images/editor/update_available.png)

Press the `Update Available` clickable link to download and update. A confirmation window with information will pop up - click `Download Update` to proceed.

![Update Editor popup](images/editor/update.png)

You will see the download progress in the bottom status bar:

![Download progress](images/editor/download_status.png)

After update is downloaded the blue link will change to `Restart to Update`. Click it to restart and open the updated Editor.

![Restart to update](images/editor/restart_to_update.png)

## Preferences

You can modify the settings of the Editor in the `Preferences` window. To open it click `File ▸ Preferences...` or shortcut <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>,</kbd>

Read more details in the [Preferences manual](/manuals/editor-preferences)

![Preferences](images/editor/preferences.png)

## Editor logs
If you run into a problem with the Editor and need to report issue (`Help  ▸ Report Issue`)  it is a good idea to provide log files from the editor itself. To open location of the logs in your system browser click on `Help ▸ Show Logs`.

Read more in [Getting Help manual](/manuals/getting-help/#getting-help).

![Show Logs](images/editor/show_logs.png)

The editor logs files can be found here:

  * Windows: `C:\Users\ **Your Username** \AppData\Local\Defold`
  * macOS: `/Users/ **Your Username** /Library/Application Support/` or `~/Library/Application Support/Defold`
  * Linux: `$XDG_STATE_HOME/Defold` or `~/.local/state/Defold`

You can also get access to editor logs while the Editor is running if it is started from a terminal/command prompt. To launch the Editor use command:

```shell
# Linux:
$ ./path/to/Defold/Defold

# macOS:
$ > ./path/to/Defold.app/Contents/MacOS/Defold
```

## Editor Server

When the Editor opens a project, it will start a web server on a random port. The server may be used to interact with the editor from other applications. Since 1.11.0, the port is written to the `.internal/editor.port` file.

Additionally, since 1.11.0 the editor executable has a command line option `--port` (or `-p`), which allows specifying the port during launch, e.g.::
```shell
# Windows
.\path\to\Defold\Defold.exe --port 8181

# Linux:
./path/to/Defold/Defold --port 8181

# macOS:
./path/to/Defold/Defold.app/Contents/MacOS/Defold --port 8181
```

## Editor Styling

Editor appearance can be changed with custom styling. Read more in the [Editor Styling manual](/manuals/editor-styling.md).

## FAQ
:[Editor FAQ](../shared/editor-faq.md)
