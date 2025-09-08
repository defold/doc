`.`
  : 简写形式，解析为当前游戏对象。

  `#`
  : 简写形式，解析为当前组件。

  例如：

  ```lua
   -- 让当前游戏对象获取输入焦点
   msg.post(".", "acquire_input_focus")
  ```

  ```lua
   -- 向当前脚本发送 "reset" 消息
   msg.post("#", "reset")
  ```
