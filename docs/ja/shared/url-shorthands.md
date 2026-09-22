  `.`
  : 現在のゲームオブジェクト（game object）に解決される省略形です。

  `#`
  : 現在のコンポーネント（component）に解決される省略形です。

  たとえば、次のように使います。

  ```lua
   -- Let this game object acquire input focus
   msg.post(".", "acquire_input_focus")
  ```

  ```lua
   -- Post "reset" to the current script
   msg.post("#", "reset")
  ```
