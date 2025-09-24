---
title: Buffer手册
brief: 本手册介绍了Defold中的Buffer资源的工作原理.
---

# Buffer

Buffer资源用于描述一个或多个值流，例如位置或颜色。每个流都有名称、数据类型、计数和数据本身。示例：

```
[
  {
    "name": "position",
    "type": "float32",
    "count": 3,
    "data": [
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      1.0,
      ...
    ]
  }
]
```

上面的示例描述了三维位置流，表示为32位浮点数。Buffer文件的格式为JSON，文件扩展名为`.buffer`。

Buffer资源通常使用外部工具或脚本创建，例如从Blender等建模工具导出时。 

Buffer资源可用作[Mesh组件](/manuals/mesh)的输入。也可以使用`buffer.create()`和[相关API函数](/ref/stable/buffer/#buffer.create:element_count-declaration)在运行时创建Buffer资源。