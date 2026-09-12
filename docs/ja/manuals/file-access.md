---
title: ファイルの操作
brief: このマニュアルでは、ファイルの保存と読み込み、およびその他のファイル操作の方法を説明します。
---

# ファイルの操作 {#working-with-files}
ファイルの作成やアクセスにはさまざまな方法があります。ファイルパスとアクセス方法は、ファイルの種類と保存場所によって異なります。

## ファイルやフォルダーへのアクセスに使う関数 {#functions-for-file-and-folder-access}
Defold には、ファイルを操作するためのさまざまな関数があります。

* 標準の [`io.*` 関数](https://defold.com/ref/stable/io/) を使って、ファイルの読み取りと書き込みができます。これらの関数では、I/O 処理全体を非常に細かく制御できます。

```lua
-- open myfile.txt for writing in binary mode
-- returns nil plus error message on failure
local f, err = io.open("path/to/myfile.txt", "wb")
if not f then
	print("Something went wrong while opening the file", err)
	return
end

-- write to the file, flush it to disk and then close the file
f:write("Foobar")
f:flush()
f:close()

-- open myfile.txt for reading in binary mode
-- returns nil plus error message on failure
local f, err = io.open("path/to/myfile.txt", "rb")
if not f then
	print("Something went wrong while opening the file", err)
	return
end

-- read the entire file as a string
-- returns nil on failure
local s = f:read("*a")
if not s then
	print("Error while reading file")
	return
end

print(s) -- Foobar
```

* [`os.rename()`](https://defold.com/ref/stable/os/#os.rename:oldname-newname) と [`os.remove()`](https://defold.com/ref/stable/os/#os.remove:filename) を使って、ファイルの名前変更と削除ができます。

* [`sys.save()`](https://defold.com/ref/stable/sys/#sys.save:filename-table) と [`sys.load()`](https://defold.com/ref/stable/sys/#sys.load:filename) を使って、Lua テーブルの読み取りと書き込みができます。ほかにも、プラットフォームに依存しないファイルパスの解決に役立つ [`sys.*`](https://defold.com/ref/stable/sys/) 関数があります。

```lua
-- get a platform independent path to the file "highscore" for application "mygame"
local path = sys.get_save_file("mygame", "highscore")

-- save a Lua table with some data
local ok = sys.save(path, { highscore = 100 })
if not ok then
	print("Failed to save", path)
	return
end

-- load the data
local ok, data = pcall(sys.load, path)
if not ok then
	-- The file exists, but is corrupt, foreign, or uses an unsupported format.
	print("Failed to load save data:", data)
	data = {}
end
print(data.highscore) -- 100
```

`sys.load()` は、ファイルが存在しない場合、空のテーブルを返します。ファイルが存在していても、`sys.save()` で作成されていない、破損している、またはサポートされていないシリアライズ済みテーブルの形式を使用している場合、`sys.load()` は Lua エラーを発生させます。破損した保存データや外部で変更された保存データから復旧できるようにする必要がある場合は、上記のように `pcall()` を使います。


## ファイルとフォルダーの場所 {#file-and-folder-locations}
ファイルとフォルダーの場所は、次の3つに分類できます。

* アプリケーションが作成する、アプリケーション固有のファイル
* アプリケーションに同梱されるファイルとフォルダー
* アプリケーションがアクセスする、システム固有のファイル

### アプリケーション固有のファイルを保存、読み込みする方法 {#how-to-save-and-load-application-specific-files}
ハイスコア、ユーザー設定、ゲームの状態など、アプリケーション固有のファイルを保存、読み込みする際は、オペレーティングシステムがこの目的専用に提供する場所を使うことをお勧めします。[`sys.get_save_file()`](https://defold.com/ref/stable/sys/#sys.get_save_file:application_id-file_name) を使うと、ファイルへの OS 固有の絶対パスを取得できます。絶対パスを取得したら、`sys.*`、`io.*`、`os.*` 関数を使えます（上記参照）。

[`sys.save()` と `sys.load()` の使い方を示すサンプルを確認してください](/examples/file/sys_save_load/)。

### アプリケーションに同梱されたファイルにアクセスする方法 {#how-to-access-files-bundled-with-the-application}
バンドルリソース（bundle resources）とカスタムリソース（custom resources）を使って、アプリケーションにファイルを同梱できます。

#### カスタムリソース {#custom-resources}
:[Custom Resources](../shared/custom-resources.md)

拡張も `ext.properties` を通じてこれらのファイルを提供できます。エディターのビルドと Bob のアーカイブの両方で、そのパスはプロジェクトのカスタムリソースと統合されます。[拡張のカスタムリソース](/manuals/extensions/#custom-resources)を参照してください。

```lua
-- Load level data into a string
local data, error = sys.load_resource("/assets/level_data.json")
-- Decode json string to a Lua table
if data then
  local data_table = json.decode(data)
  pprint(data_table)
else
  print(error)
end
```

#### バンドルリソース {#bundle-resources}
:[Bundle Resources](../shared/bundle-resources.md)

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

::: sidenote
セキュリティ上の理由から、ブラウザー（およびその中で動作するすべての JavaScript）はシステムファイルへのアクセスを禁止されています。Defold の HTML5 ビルドでもファイル操作は機能しますが、ブラウザーの IndexedDB API を使う「仮想ファイルシステム」上でのみ行われます。つまり、`io.*` や `os.*` 関数を使ってバンドルリソースにアクセスすることはできません。ただし、`http.request()` を使えばバンドルリソースにアクセスできます。
:::


#### カスタムリソースとバンドルリソースの比較 {#custom-and-bundle-resources-comparison}

| 特性              | カスタムリソース                          | バンドルリソース                               |
|-----------------------------|-------------------------------------------|------------------------------------------------|
| 読み込み速度               | 速い - バイナリアーカイブからファイルを読み込みます | 遅い - ファイルシステムからファイルを読み込みます          |
| ファイルの一部の読み込み          | 不可 - ファイル全体のみ読み込めます                    | 可能 - ファイルから任意のバイトを読み取れます           |
| バンドル作成後のファイルの変更 | 不可 - ファイルはバイナリアーカイブ内に格納されます | 可能 - ファイルはローカルファイルシステム上に格納されます    |
| HTML5 対応               | 対応                                       | 対応 - ただし、ファイル I/O ではなく http 経由でアクセスします |


### システムファイルへのアクセス {#system-file-access}
セキュリティ上の理由から、オペレーティングシステムによってシステムファイルへのアクセスが制限されることがあります。[`extension-directories`](https://defold.com/assets/extensiondirectories/) ネイティブ拡張（native extension）を使うと、一般的なシステムディレクトリの一部（`documents`、`resource`、`temp` など）の絶対パスを取得できます。これらのファイルの絶対パスを取得したら、`io.*` 関数と `os.*` 関数を使ってファイルにアクセスできます（上記参照）。

::: sidenote
セキュリティ上の理由から、ブラウザー（およびその中で動作するすべての JavaScript）はシステムファイルへのアクセスを禁止されています。Defold の HTML5 ビルドでもファイル操作は機能しますが、ブラウザーの IndexedDB API を使う「仮想ファイルシステム」上でのみ行われます。つまり、HTML5 ビルドでシステムファイルにアクセスすることはできません。
:::

## 拡張機能 {#extensions}
[Asset Portal](https://defold.com/assets/) には、ファイルやフォルダーへのアクセスを簡単にするアセットがいくつかあります。次に例を示します。

* [Lua File System (LFS)](https://defold.com/assets/luafilesystemlfs/) - ディレクトリ、ファイルの権限などを操作する関数です。
* [DefSave](https://defold.com/assets/defsave/) - セッション間で設定やプレイヤーデータを保存、読み込みするためのモジュールです。
