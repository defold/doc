---
title: 파일 작업하기
brief: 이 매뉴얼은 파일을 저장하고 로드하는 방법과 기타 파일 작업을 수행하는 방법을 설명합니다.
---

# 파일 작업하기
파일을 생성하거나 액세스하는 방법은 다양합니다. 파일 경로와 파일에 액세스하는 방식은 파일의 종류와 파일 위치에 따라 달라집니다.

## 파일 및 폴더 액세스 함수
Defold는 파일을 다루기 위한 여러 함수를 제공합니다:

* 표준 [`io.*` 함수](https://defold.com/ref/stable/io/)를 사용해 파일을 읽고 쓸 수 있습니다. 이 함수들은 전체 I/O 과정에 대해 매우 세밀한 제어를 제공합니다.

```lua
-- myfile.txt를 바이너리 모드로 쓰기 위해 엽니다
-- 실패하면 nil과 오류 메세지를 반환합니다
local f, err = io.open("path/to/myfile.txt", "wb")
if not f then
	print("Something went wrong while opening the file", err)
	return
end

-- 파일에 쓰고, 디스크로 flush한 다음 파일을 닫습니다
f:write("Foobar")
f:flush()
f:close()

-- myfile.txt를 바이너리 모드로 읽기 위해 엽니다
-- 실패하면 nil과 오류 메세지를 반환합니다
local f, err = io.open("path/to/myfile.txt", "rb")
if not f then
	print("Something went wrong while opening the file", err)
	return
end

-- 전체 파일을 문자열로 읽습니다
-- 실패하면 nil을 반환합니다
local s = f:read("*a")
if not s then
	print("Error while reading file")
	return
end

print(s) -- Foobar
```

* [`os.rename()`](https://defold.com/ref/stable/os/#os.rename:oldname-newname)과 [`os.remove()`](https://defold.com/ref/stable/os/#os.remove:filename)를 사용해 파일 이름을 변경하고 파일을 삭제할 수 있습니다.

* [`sys.save()`](https://defold.com/ref/stable/sys/#sys.save:filename-table)와 [`sys.load()`](https://defold.com/ref/stable/sys/#sys.load:filename)를 사용해 Lua 테이블을 읽고 쓸 수 있습니다. 플랫폼과 무관한 파일 경로 해석을 돕기 위한 추가 [`sys.*`](https://defold.com/ref/stable/sys/) 함수들도 있습니다.

```lua
-- 어플리케이션 "mygame"의 파일 "highscore"에 대한 플랫폼 독립적인 경로를 얻습니다
local path = sys.get_save_file("mygame", "highscore")

-- 데이터가 담긴 Lua 테이블을 저장합니다
local ok = sys.save(path, { highscore = 100 })
if not ok then
	print("Failed to save", path)
	return
end

-- 데이터를 로드합니다
local data = sys.load(path)
print(data.highscore) -- 100
```


## 파일 및 폴더 위치
파일 및 폴더 위치는 세 가지 범주로 나눌 수 있습니다:

* 어플리케이션이 생성한 어플리케이션별 파일
* 어플리케이션과 함께 번들된 파일 및 폴더
* 어플리케이션이 액세스하는 시스템별 파일

### 어플리케이션별 파일을 저장하고 로드하는 방법
하이스코어, 사용자 설정, 게임 상태 같은 어플리케이션별 파일을 저장하고 로드할 때는 운영체제가 이 목적을 위해 제공하는 위치를 사용하는 것이 좋습니다. [`sys.get_save_file()`](https://defold.com/ref/stable/sys/#sys.get_save_file:application_id-file_name)을 사용하면 파일에 대한 OS별 절대 경로를 얻을 수 있습니다. 절대 경로를 얻은 뒤에는 `sys.*`, `io.*`, `os.*` 함수를 사용할 수 있습니다(위 내용 참고).

[`sys.save()`와 `sys.load()` 사용 방법을 보여주는 예제를 확인하세요](/examples/file/sys_save_load/).

### 어플리케이션에 번들된 파일에 액세스하는 방법 {#how-to-access-files-bundled-with-the-application}
번들 리소스와 커스텀 리소스를 사용해 파일을 어플리케이션에 포함할 수 있습니다.

#### 커스텀 리소스
:[Custom Resources](../shared/custom-resources.md)

```lua
-- 레벨 데이터를 문자열로 로드합니다
local data, error = sys.load_resource("/assets/level_data.json")
-- JSON 문자열을 Lua 테이블로 디코드합니다
if data then
  local data_table = json.decode(data)
  pprint(data_table)
else
  print(error)
end
```

#### 번들 리소스
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
보안상의 이유로 브라우저(그리고 확장하면 브라우저에서 실행되는 모든 JavaScript)는 시스템 파일에 액세스할 수 없습니다. Defold의 HTML5 빌드에서도 파일 작업은 동작하지만, 브라우저의 IndexedDB API를 사용하는 "가상 파일 시스템"에서만 동작합니다. 따라서 `io.*` 또는 `os.*` 함수로 번들 리소스에 액세스할 방법은 없습니다. 하지만 `http.request()`를 사용하면 번들 리소스에 액세스할 수 있습니다.
:::


#### 커스텀 리소스와 번들 리소스 비교

| 특성                        | 커스텀 리소스                             | 번들 리소스                                    |
|-----------------------------|-------------------------------------------|------------------------------------------------|
| 로딩 속도                   | 더 빠름 - 바이너리 아카이브에서 파일 로드 | 더 느림 - 파일 시스템에서 파일 로드            |
| 파일 일부 로드              | 아니요 - 전체 파일만 가능                 | 예 - 파일에서 임의 바이트 읽기                 |
| 번들링 후 파일 수정         | 아니요 - 파일이 바이너리 아카이브 안에 저장됨 | 예 - 파일이 로컬 파일 시스템에 저장됨      |
| HTML5 지원                  | 예                                        | 예 - 하지만 파일 I/O가 아닌 http를 통해 액세스 |


### 시스템 파일 액세스
시스템 파일 액세스는 보안상의 이유로 운영체제에 의해 제한될 수 있습니다. [`extension-directories`](https://defold.com/assets/extensiondirectories/) 네이티브 익스텐션을 사용하면 일반적인 일부 시스템 디렉토리(예: `documents`, `resource`, `temp`)의 절대 경로를 얻을 수 있습니다. 이 파일들의 절대 경로를 얻은 뒤에는 `io.*`와 `os.*` 함수를 사용해 파일에 액세스할 수 있습니다(위 내용 참고).

::: sidenote
보안상의 이유로 브라우저(그리고 확장하면 브라우저에서 실행되는 모든 JavaScript)는 시스템 파일에 액세스할 수 없습니다. Defold의 HTML5 빌드에서도 파일 작업은 동작하지만, 브라우저의 IndexedDB API를 사용하는 "가상 파일 시스템"에서만 동작합니다. 즉, HTML5 빌드에서는 시스템 파일에 액세스할 방법이 없습니다.
:::

## 익스텐션
[Asset Portal](https://defold.com/assets/)에는 파일 및 폴더 액세스를 단순화하는 여러 에셋이 있습니다. 예:

* [Lua File System (LFS)](https://defold.com/assets/luafilesystemlfs/) - 디렉토리, 파일 권한 등을 다루는 함수
* [DefSave](https://defold.com/assets/defsave/) - 세션 간 config와 플레이어 데이터를 저장/로드하는 데 도움을 주는 모듈.
