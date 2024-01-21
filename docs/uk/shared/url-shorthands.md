  `.`
  : Скорочення для поточного ігрового обʼєкта.

  `#`
  : Скорочення для поточного компонента.

  Наприклад:

  ```lua
   -- Let this game object acquire input focus
   msg.post(".", "acquire_input_focus")
  ```

  ```lua
   -- Post "reset" to the current script
   msg.post("#", "reset")
  ```
