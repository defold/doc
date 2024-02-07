---
title: 缓存教程
brief: 本教程介绍了 Defold 的缓存资源.
---

# Buffer

缓存资源用来描述一个或多个数据流, 比如位置或颜色. 每种流有名字, 数据类型, 数目及数据自身. 例如:

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

上例描述了三维位置数据流, 用 32-bit 浮点数表示. 缓存类型是 JSON, 文件扩展名是 `.buffer`.

缓存资源一般由扩展工具或脚本创建, 比如用 Blender 导出模型时创建. 

缓存资源可以用作 [模型资源](/manuals/mesh) 的数据. 缓存资源还可以使用 `buffer.create()` 和 [相关 API 函数](/ref/stable/buffer/#buffer.create:element_count-declaration) 在运行时创建. 