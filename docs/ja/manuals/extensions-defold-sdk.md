---
title: ネイティブ拡張 - Defold SDK
brief: このマニュアルでは、ネイティブ拡張を作成する際の Defold SDK の使い方を説明します。
---

# Defold SDK {#the-defold-sdk}

Defold SDK には、ネイティブ拡張（native extension）を宣言し、アプリケーションが動作する低水準のネイティブプラットフォーム層や、ゲームロジックを記述する高水準の Lua 層と連携するために必要な機能が含まれています。

## 使い方 {#usage}

C++ の拡張では、集約ヘッダーファイル `dmsdk/sdk.h` をインクルードできます:

```cpp
#include <dmsdk/sdk.h>
```

集約ヘッダーには C++ の宣言が含まれているため、C ソースファイルからはインクルードできません。C ソースファイルでは、必要な C 互換の `.h` ヘッダーを個別にインクルードしてください。たとえば、次のようにします:

```c
#include <dmsdk/extension/extension.h>
#include <dmsdk/dlib/configfile.h>
#include <dmsdk/resource/resource.h>
```

現時点で純粋な C インターフェースを備えているのは dmSDK の一部だけであり、すべての C++ サブシステムに C 版が用意されているわけではありません。利用できる関数と型は、[C API の概要](/ref/overview_defoldc/)と [C++ API の概要](/ref/overview_defoldcpp/)に記載されています。Defold SDK のヘッダーは、[GitHub 上の Defold の各リリース](https://github.com/defold/defold/releases)に、独立した `defoldsdk_headers.zip` アーカイブとして含まれています。これらのヘッダーを使うと、好みのエディターでコード補完を利用できます。
