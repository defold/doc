  `.`
  : Atalho que resolve para o objeto de jogo atual.

  `#`
  : Atalho que resolve para o componente atual.

  Por exemplo:

  ```lua
   -- Permite que este objeto de jogo adquira foco de entrada
   msg.post(".", "acquire_input_focus")
  ```

  ```lua
   -- Envia "reset" ao script atual
   msg.post("#", "reset")
  ```
