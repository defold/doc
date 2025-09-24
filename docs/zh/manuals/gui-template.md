---
title: GUI模板手册
brief: 本手册解释了Defold GUI模板系统，该系统用于创建基于共享模板或'prefabs'的可重用可视化GUI组件。
---

# GUI模板节点

GUI模板节点提供了一种强大的机制，用于基于共享模板或"prefabs"创建可重用的GUI组件。本手册解释了这一功能及其使用方法。

GUI模板是在另一个GUI场景中逐个节点实例化的GUI场景。然后可以覆盖原始模板节点中的任何属性值。

## 创建模板

GUI模板是一个普通的GUI场景，因此它的创建方式与任何其他GUI场景相同。在 *Assets* 面板中<kbd>右键点击</kbd>一个位置并选择 <kbd>New... ▸ Gui</kbd>。

![Create template](images/gui-templates/create.png)

创建模板并保存。注意，实例的节点将相对于原点放置，因此在 0, 0, 0 位置创建模板是一个好主意。

## 从模板创建实例

您可以根据模板创建任意数量的实例。创建或打开要放置模板的GUI场景，然后在*Outline*视图中<kbd>右键点击</kbd>*Nodes*部分，并选择<kbd>Add ▸ Template</kbd>。

![Create instance](images/gui-templates/create_instance.png)

将*Template*属性设置为模板GUI场景文件。

您可以添加任意数量的模板实例，并且对于每个实例，您可以覆盖每个节点的属性，并更改实例节点的位置、颜色、大小、纹理等。

![Instances](images/gui-templates/instances.png)

任何已更改的属性在编辑器中会标记为蓝色。单击属性旁边的重置按钮可将其值设置为模板值：

![Properties](images/gui-templates/properties.png)

任何具有覆盖属性的节点在*Outline*视图中也会以蓝色显示：

![Outline](images/gui-templates/outline.png)

模板实例在*Outline*视图中列为可折叠条目。但是，需要注意的是，大纲中的此项*不是一个节点*。模板实例在运行时也不存在，但属于实例的所有节点都存在。

属于模板实例的节点会自动在其*Id*前附加前缀和斜杠（`"/"`）。前缀是在模板实例中设置的*Id*。

## 运行时修改模板

操作或查询通过模板机制添加的节点的脚本只需要考虑实例节点的命名，并将模板实例*Id*作为节点名称前缀包含在内：

```lua
if gui.pick_node(gui.get_node("button_1/button"), x, y) then
    -- 做些什么...
end
```

没有与模板实例本身对应的节点。如果需要实例的根节点，请将其添加到模板中。

如果脚本与模板GUI场景相关联，则该脚本不属于实例节点树的一部分。您可以将单个脚本附加到每个GUI场景，因此您的脚本逻辑需要位于已实例化模板的GUI场景上。
