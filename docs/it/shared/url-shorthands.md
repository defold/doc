  `.`
  : Forma abbreviata che fa riferimento all'oggetto di gioco corrente.

  `#`
  : Forma abbreviata che fa riferimento al componente corrente.

  Per esempio:

  ```lua
   -- Let this game object acquire input focus
   msg.post(".", "acquire_input_focus")
  ```

  ```lua
   -- Post "reset" to the current script
   msg.post("#", "reset")
  ```
