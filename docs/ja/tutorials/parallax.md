---
title: パララックスのコードサンプル
brief: このサンプルでは、パララックス効果を使ってゲームワールドに奥行きを表現する方法を学びます。
---
# パララックス - サンプルプロジェクト {#parallax-sample-project}

<iframe width="560" height="315" src="https://www.youtube.com/embed/UdNA7kanRQE" frameborder="0" allowfullscreen></iframe>


[エディターから開く](/manuals/project-setup/)、または [GitHub からダウンロードする](https://github.com/defold/sample-parallax)ことができるこのサンプルプロジェクトでは、パララックス（parallax）効果を使ってゲームワールド（game world）に奥行きを表現する方法を紹介します。
雲のレイヤーは2つあり、一方のレイヤーがもう一方よりも奥にあるように見えます。さらに、彩りを添えるために、アニメーションする空飛ぶ円盤もあります。

雲のレイヤーは、それぞれ *タイルマップ（Tile Map）* と *スクリプト（Script）* を持つ、2つの独立したゲームオブジェクト（game object）として構成されています。
レイヤーを異なる速度で動かすことで、パララックス効果を生み出します。この処理は、以下の *background1.script* と *background2.script* の `update()` で行います。

```lua
-- file: background1.script

function init(self)
    msg.post("@render:", "clear_color", { color = vmath.vector4(0.52, 0.80, 1, 0) } )
end

-- the background is a tilemap in a gameobject
-- we move the gameobject for the parallax effect

function update(self, dt)
    -- decrease x-position by 1 units per frame for parallax effect
    local p = go.get_position()
    p.x = p.x + 1
    go.set_position(p)
end
```

```lua
-- file: background2.script

-- the background is a tilemap in a gameobject
-- we move the gameobject for the parallax effect

function update(self, dt)
    -- decrease x-position by 0.5 units per frame for parallax effect
    local p = go.get_position()
    p.x = p.x + 0.5
    go.set_position(p)
end
```

円盤は、*スプライト（Sprite）* と *スクリプト* を持つ独立したゲームオブジェクトです。
一定の速度で左に移動します。上下の動きは、Lua の正弦関数（`math.sin()`）を使い、位置の y 成分を固定値の周りで変化させることで実現しています。この処理は、*spaceship.script* の `update()` で行います。


```lua
-- file: spaceship.script

function init(self)
    -- remeber initial y position such that we
    -- can move the spaceship without changing the script
    self.start_y = go.get_position().y
    -- set counter to zero. use for sin-movement below
    self.counter = 0
end

function update(self, dt)
    -- decrease x-position by 2 units per frame
    local p = go.get_position()
    p.x = p.x - 2

    -- move the y position around initial y
    p.y = self.start_y + 8 * math.sin(self.counter * 0.08)

    -- update position
    go.set_position(p)

    -- remove shaceship when outside of screen
    if p.x < - 32 then
        go.delete()
    end

    -- increase the counter
    self.counter = self.counter + 1
end
```
