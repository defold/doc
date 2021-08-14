  `.`
  : Dirección del objeto actual.

  `#`
  : Dirección del componente actual.

  Ejemplo:

  ```lua
   -- Let this game object acquire input focus
   msg.post(".", "acquire_input_focus")
  ```

  ```lua
   -- Post "reset" to the current script
   msg.post("#", "reset")
  ```
