  `.`
  : 指代当前游戏对象.

  `#`
  : 指代当前组件.

  举例:

  ```lua
   -- 使当前游戏对象获得输入焦点
   msg.post(".", "acquire_input_focus")
  ```

  ```lua
   -- 向当前脚本组件发出 "reset" 信息
   msg.post("#", "reset")
  ```
