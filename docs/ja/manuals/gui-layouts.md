---
title: Defold の GUI レイアウト
brief: Defold は、モバイルデバイスの画面の向きの変更に自動的に対応する GUI をサポートしています。このドキュメントでは、この機能の仕組みを説明します。
---

# レイアウト {#layouts}

Defold は、モバイルデバイスの画面の向きの変更に自動的に対応する GUI をサポートしています。この機能を使うと、さまざまな画面サイズの向きやアスペクト比に対応する GUI を設計できます。また、特定のデバイスモデルに合うレイアウト（layout）を作成することもできます。

## ディスプレイプロファイルの作成 {#creating-display-profiles}

デフォルトでは、*game.project* の設定で、組み込みのディスプレイプロファイル（display profiles）設定ファイル（"builtins/render/default.display_profiles"）を使うように指定されています。デフォルトのプロファイルは「Landscape」（幅1280ピクセル、高さ720ピクセル）と「Portrait」（幅720ピクセル、高さ1280ピクセル）です。これらのプロファイルにはデバイスモデルが設定されていないため、どのデバイスにも一致します。

新しいプロファイル設定ファイルを作成するには、「builtins」フォルダーにあるファイルをコピーするか、*Assets* ビューの適切な場所を <kbd>右クリック</kbd> して <kbd>New... ▸ Display Profiles</kbd> を選択します。新しいファイルに適切な名前を付け、<kbd>Ok</kbd> をクリックします。

エディターで新しいファイルが開き、編集できるようになります。*Profiles* リストの <kbd>+</kbd> をクリックして、新しいプロファイルを追加します。各プロファイルに、一連の *条件（qualifier）* を追加します。

Width
: 条件の幅（ピクセル単位）です。

Height
: 条件の高さ（ピクセル単位）です。

Device Models
: デバイスモデルのコンマ区切りのリストです。デバイスモデルはモデル名の先頭部分と照合されます。たとえば、`iPhone10` は「iPhone10,\*」モデルに一致します。コンマを含むモデル名は引用符で囲む必要があります。たとえば、`"iPhone10,3", "iPhone10,6"` は iPhone X モデルに一致します（[iPhone ウィキ](https://www.theiphonewiki.com/wiki/Models)を参照）。`sys.get_sys_info()` を呼び出したときにデバイスモデルを返すプラットフォームは、Android と iOS だけである点に注意してください。ほかのプラットフォームは空文字列を返すため、デバイスモデルの条件があるディスプレイプロファイルが選択されることはありません。

![新しいディスプレイプロファイル](images/gui-layouts/new_profiles.png)

エンジンで新しいプロファイルを使うように指定する必要もあります。*game.project* を開き、*display* の *Display Profiles* 設定でディスプレイプロファイルファイルを選択します。

![設定](images/gui-layouts/settings.png)

デバイスの回転時に、エンジンが縦向きと横向きのレイアウトを自動的に切り替えるようにするには、*Dynamic Orientation* チェックボックスをオンにします。エンジンは一致するレイアウトを動的に選択し、デバイスの向きが変わると選択を変更します。

### Auto Layout Selection (Display Profiles)

Display Profiles リソースには「Auto Layout Selection」オプションがあります（デフォルトは ON）。ON の場合、エンジンはシーン（scene）の作成時とウィンドウやディスプレイのサイズ変更時の両方で、最もよく一致する GUI レイアウトを自動的に選択します。OFF の場合、エンジンはレイアウトを自動的に変更しません。GUI スクリプト（GUI script）から `gui.set_layout()` を使って、手動でレイアウトを切り替えます。この設定は Display Profiles ファイルに保存され、すべての GUI シーンに影響します。

## GUI レイアウト {#gui-layouts}

現在のディスプレイプロファイルのセットを使って、GUI ノード（GUI node）の構成に対するレイアウトのバリエーションを作成できます。GUI シーンに新しいレイアウトを追加するには、*Outline* ビューの *Layouts* アイコンを右クリックし、<kbd>Add ▸ Layout ▸ ...</kbd> を選択します。

![シーンへのレイアウトの追加](images/gui-layouts/add_layout.png)

GUI シーンの編集中は、すべてのノードが特定のレイアウト上で編集されます。現在選択されているレイアウトは、ツールバーの GUI シーンのレイアウトドロップダウンに表示されます。レイアウトが選択されていない場合、ノードは *Default* レイアウトで編集されます。

![レイアウトのツールバー](images/gui-layouts/toolbar.png)

![縦向きのレイアウトの編集](images/gui-layouts/portrait.png)

レイアウトが選択された状態でノードのプロパティを変更すると、そのプロパティを *Default* レイアウトに対して _上書き_ します。上書きされたプロパティは青色で表示されます。プロパティが上書きされたノードも青色で表示されます。上書きされたプロパティの横にあるリセットボタンをクリックすると、元の値に戻せます。

![横向きのレイアウトの編集](images/gui-layouts/landscape.png)

レイアウトではノードの削除や新しいノードの作成はできず、プロパティの上書きだけができます。レイアウトからノードを取り除く必要がある場合は、ノードを画面外に移動するか、スクリプトのロジックで削除します。また、現在選択されているレイアウトにも注意してください。プロジェクトにレイアウトを追加すると、新しいレイアウトは現在選択されているレイアウトに従って設定されます。ノードのコピーと貼り付けでも、コピー時 *と* 貼り付け時のどちらでも、現在選択されているレイアウトが考慮されます。

## プロファイルの動的な選択 {#dynamic-profile-selection}

Auto Layout Selection が有効な場合、エンジンは最もよく一致するレイアウトを自動的に選択します。動的なレイアウトの照合では、次の規則に従って各ディスプレイプロファイルの条件のスコアを求めます。

1. デバイスモデルが設定されていない場合、またはデバイスモデルが一致する場合、その条件のスコア（S）を計算します。

2. スコア（S）は、ディスプレイの面積（A）、条件の面積（A_Q）、ディスプレイのアスペクト比（R）、条件のアスペクト比（R_Q）を使って計算します。

<img src="https://latex.codecogs.com/svg.latex?\inline&space;S=\left|1&space;-&space;\frac{A}{A_Q}\right|&space;&plus;&space;\left|1&space;-&space;\frac{R}{R_Q}\right|" title="S=\left|1 - \frac{A}{A_Q}\right| + \left|1 - \frac{R}{R_Q}\right|" />

3. スコアが最も低い条件を持つプロファイルを、その条件の向き（横向きまたは縦向き）がディスプレイと一致する場合に選択します。

4. 同じ向きの条件を持つプロファイルが見つからない場合、もう一方の向きで最もスコアのよい条件を持つプロファイルを選択します。

5. プロファイルを選択できない場合は、フォールバックとして *Default* プロファイルを使います。

実行時に、よりよく一致するレイアウトがない場合は、*Default* レイアウトがフォールバックとして使われます。そのため、「Landscape」レイアウトを追加すると、「Portrait」レイアウトも追加するまでは、それが *すべて* の向きに最もよく一致するレイアウトになります。

## レイアウト変更メッセージ {#layout-change-messages}

レイアウトが変更されると、GUI コンポーネント（GUI component）のスクリプトに `layout_changed` メッセージが送信されます。これは、エンジンが自動的にレイアウトを変更した場合（Auto Layout Selection が ON）、またはスクリプトが `gui.set_layout()` を呼び出し、実際にレイアウトが変更された場合に発生します。メッセージにはレイアウトのハッシュ化された ID が含まれるため、スクリプトで選択されたレイアウトに応じた処理を実行できます。

```lua
function on_message(self, message_id, message, sender)
  if message_id == hash("layout_changed") and message.id == hash("My Landscape") then
    -- switching layout to landscape
  elseif message_id == hash("layout_changed") and message.id == hash("My Portrait") then
    -- switching layout to portrait
  end
end
```

また、現在のレンダースクリプト（render script）は、ウィンドウ（ゲームビュー）が変わるたびにメッセージを受信します。これには向きの変更も含まれます。

```lua
function on_message(self, message_id, message)
  if message_id == hash("window_resized") then
    -- The window was resized. message.width and message.height contain the
    -- new dimensions of the window.
  end
end
```

向きが切り替わると、GUI レイアウトマネージャーはレイアウトとノードのプロパティに従って、GUI ノードの拡大縮小と再配置を自動的に行います。一方、ゲーム内のコンテンツは、デフォルトでは別のレンダーパスで、現在のウィンドウに合わせて引き伸ばす投影を使って描画されます。この動作を変更するには、独自に変更したレンダースクリプトを用意するか、カメラの[ライブラリ](/assets/)を使います。

## 手動でのレイアウト選択（Lua） {#manual-layout-selection-lua}

使用中の Display Profiles で Auto Layout Selection が OFF の場合、エンジンはレイアウトを自動的に切り替えません。GUI スクリプトから次の関数を使って、手動でレイアウトを管理します。

### gui.set_layout(layout)

- 文字列またはハッシュ値（レイアウト ID）を受け取ります。
- 真偽値を返します。シーン内にレイアウトが存在し、適用された場合は `true`、それ以外の場合は `false` です。
- レイアウトが Display Profiles に存在する場合、シーンの解像度をプロファイルの幅と高さに更新します。
- 実際にレイアウトが変更された場合に `layout_changed` を送信します。

例:

```lua
function init(self)
    -- Manually apply the "Portrait" layout
    local ok = gui.set_layout("Portrait")
    if not ok then
        print("Portrait layout not found in this scene")
    end
end
```

### gui.get_layouts()

- 各レイアウト ID のハッシュ値を `vmath.vector3(width, height, 0)` に対応付けるテーブルを返します。
- デフォルトのレイアウトについては、現在のシーンの解像度を返します。

例:

```lua
local layouts = gui.get_layouts()
for id, size in pairs(layouts) do
    print(id, size.x, size.y)
end
```

注意: GUI レイアウトがシーン内に存在しても Display Profiles に存在しない場合、`gui.set_layout()` はレイアウトごとのノードの上書き設定を適用しますが、シーンの解像度は変更しません。
