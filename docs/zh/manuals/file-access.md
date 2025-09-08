---
title: 处理文件
brief: 本手册解释了如何保存和加载文件以及执行其他类型的文件操作。
---

# 处理文件
创建和/或访问文件有许多不同的方式。文件路径和访问这些文件的方式根据文件类型和文件位置而有所不同。

## 文件和文件夹访问函数
Defold 提供了几种不同的函数来处理文件：

* 您可以使用标准的 [`io.*` 函数](https://defold.com/ref/stable/io/)来读写文件。这些函数为您提供了对整个 I/O 过程的非常精细的控制。

```lua
-- 以二进制模式打开 myfile.txt 进行写入
-- 失败时返回 nil 和错误消息
local f, err = io.open("path/to/myfile.txt", "wb")
if not f then
	print("打开文件时出错了", err)
	return
end

-- 写入文件，刷新到磁盘然后关闭文件
f:write("Foobar")
f:flush()
f:close()

-- 以二进制模式打开 myfile.txt 进行读取
-- 失败时返回 nil 和错误消息
local f, err = io.open("path/to/myfile.txt", "rb")
if not f then
	print("打开文件时出错了", err)
	return
end

-- 将整个文件作为字符串读取
-- 失败时返回 nil
local s = f:read("*a")
if not s then
	print("读取文件时出错")
	return
end

print(s) -- Foobar
```

* 您可以使用 [`os.rename()`](https://defold.com/ref/stable/os/#os.rename:oldname-newname) 和 [`os.remove()`](https://defold.com/ref/stable/os/#os.remove:filename) 来重命名和删除文件。

* 您可以使用 [`sys.save()`](https://defold.com/ref/stable/sys/#sys.save:filename-table) 和 [`sys.load()`](https://defold.com/ref/stable/sys/#sys.load:filename) 来读写 Lua 表。还有其他 [`sys.*`](https://defold.com/ref/stable/sys/) 函数可以帮助实现平台无关的文件路径解析。

```lua
-- 获取应用程序"mygame"的文件"highscore"的平台无关路径
local path = sys.get_save_file("mygame", "highscore")

-- 保存包含一些数据的 Lua 表
local ok = sys.save(path, { highscore = 100 })
if not ok then
	print("保存失败", path)
	return
end

-- 加载数据
local data = sys.load(path)
print(data.highscore) -- 100
```

## 文件和文件夹位置
文件和文件夹位置可以分为三类：

* 由您的应用程序创建的应用程序特定文件
* 与您的应用程序捆绑在一起的文件和文件夹
* 由您的应用程序访问的系统特定文件

### 如何保存和加载应用程序特定文件
当保存和加载应用程序特定文件（如高分、用户设置和游戏状态）时，建议在操作系统提供的专门用于此目的的位置中进行。您可以使用 [`sys.get_save_file()`](https://defold.com/ref/stable/sys/#sys.get_save_file:application_id-file_name) 获取文件的操作系统特定绝对路径。一旦获得绝对路径，您就可以使用 `sys.*`、`io.*` 和 `os.*` 函数（见上文）。

[查看展示如何使用 `sys.save()` 和 `sys.load()` 的示例](/examples/file/sys_save_load/)。

### 如何访问与应用程序捆绑的文件
您可以使用捆绑资源和自定义资源将文件包含在您的应用程序中。

#### 自定义资源
:[自定义资源](../shared/custom-resources.md)

```lua
-- 将关卡数据加载到字符串中
local data, error = sys.load_resource("/assets/level_data.json")
-- 将 json 字符串解码为 Lua 表
if data then
  local data_table = json.decode(data)
  pprint(data_table)
else
  print(error)
end
```

#### 捆绑资源
:[捆绑资源](../shared/bundle-resources.md)

```lua
local path = sys.get_application_path()
local f = io.open(path .. "/mycommonfile.txt", "rb")
local txt, err = f:read("*a")
if not txt then
	print(err)
	return
end
print(txt)
```

::: important
出于安全原因，浏览器（以及扩展来说，在浏览器中运行的任何 JavaScript）被阻止访问系统文件。在 Defold 的 HTML5 构建中，文件操作仍然有效，但仅在浏览器中使用 IndexedDB API 的"虚拟文件系统"上有效。这意味着无法使用 `io.*` 或 `os.*` 函数访问捆绑资源。但是，您可以使用 `http.request()` 访问捆绑资源。
:::


#### 自定义和捆绑资源 - 比较

| 特性              | 自定义资源                          | 捆绑资源                               |
|-----------------------------|-------------------------------------------|------------------------------------------------|
| 加载速度               | 更快 - 从二进制存档加载文件 | 更慢 - 从文件系统加载文件          |
| 加载部分文件          | 否 - 只能加载整个文件                    | 是 - 从文件读取任意字节           |
| 捆绑后修改文件 | 否 - 文件存储在二进制存档内 | 是 - 文件存储在本地文件系统上    |
| HTML5 支持               | 是                                       | 是 - 但通过 http 访问而不是文件 I/O |


### 系统文件访问
出于安全原因，操作系统可能会限制对系统文件的访问。您可以使用 [`extension-directories`](https://defold.com/assets/extensiondirectories/) 原生扩展来获取一些常见系统目录（即文档、资源、临时文件）的绝对路径。一旦获得这些文件的绝对路径，您就可以使用 `io.*` 和 `os.*` 函数来访问文件（见上文）。

::: important
出于安全原因，浏览器（以及扩展来说，在浏览器中运行的任何 JavaScript）被阻止访问系统文件。在 Defold 的 HTML5 构建中，文件操作仍然有效，但仅在浏览器中使用 IndexedDB API 的"虚拟文件系统"上有效。这意味着在 HTML5 构建中无法访问系统文件。
:::

## 扩展
[资源门户](https://defold.com/assets/) 包含几个简化文件和文件夹访问的资源。一些示例：

* [Lua 文件系统 (LFS)](https://defold.com/assets/luafilesystemlfs/) - 用于处理目录、文件权限等的函数
* [DefSave](https://defold.com/assets/defsave/) - 一个帮助您在会话之间保存/加载配置和玩家数据的模块
