  `.`
  : Скорочення, що вказує на поточний ігровий об’єкт.

  `#`
  : Скорочення, що вказує на поточний компонент.

  Наприклад:

  ```lua
   -- Let this game object acquire input focus
   msg.post(".", "acquire_input_focus")
  ```

  ```lua
   -- Post "reset" to the current script
   msg.post("#", "reset")
  ```
