#### P: Por que o editor Defold fica muito pequeno quando executado em um monitor 4K ou HiDPI?

R: Se você estiver usando GNOME, é possível alterar o fator de escala antes de rodar o Defold. [fonte](https://unix.stackexchange.com/a/552411)

```bash
$ gsettings set org.gnome.desktop.interface scaling-factor 2
$ ./Defold
```

R: Uma solução alternativa, especialmente quando você deseja aumentar a escala por uma fração, é modificar o arquivo `Defold/config` e, na linha `vmargs`, adicionar `glass.gtk.uiScale`: [fonte](https://forum.defold.com/t/4k-hidpi-monitor-support-solved/64108/12?u=britzl)

```
vmargs = -Dglass.gtk.uiScale=1.5,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=175%,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=192dpi,-Dfile.encoding=UTF-8,...
```

Mais sobre esse valor no [artigo da wiki do Arch Linux sobre HiDPI](https://wiki.archlinux.org/title/HiDPI#JavaFX).

R: Se você estiver usando KDE, é possível definir `GDK_SCALE`:

```bash
$ GDK_SCALE=2 ./Defold
```

#### P: Por que cliques do mouse no Elementary OS atravessam o editor e atingem o que está abaixo?

R: Inicie o editor assim:

```bash
$ GTK_CSD=0 ./Defold
```


#### P: O editor Defold trava ao abrir uma coleção ou objeto de jogo e o crash se refere a `com.jogamp.opengl`

R: Em certas distribuições (como Ubuntu 18), há um problema entre a versão de `jogamp`/`jogl` que o Defold usa e a versão do [Mesa](https://docs.mesa3d.org/) no sistema. Você pode sobrescrever qual versão de GL é relatada ao chamar `glGetString(GL_VERSION)` definindo `MESA_GL_VERSION_OVERRIDE` como 2.1 ou um valor maior, mas menor ou igual à versão do seu driver. Você pode verificar qual é a versão máxima do OpenGL compatível com seu driver usando `glxinfo`:

```bash
glxinfo | grep version
```

Exemplo de saída (procure por "OpenGL version string: x.y"):

```
server glx version string: 1.4
client glx version string: 1.4
GLX version: 1.4
Max core profile version: 4.6
Max compat profile version: 4.6
Max GLES1 profile version: 1.1
Max GLES[23] profile version: 3.2
OpenGL core profile version string: 4.6 (Core Profile) Mesa 20.2.6
OpenGL core profile shading language version string: 4.60
OpenGL version string: 4.6 (Compatibility Profile) Mesa 20.2.6
OpenGL shading language version string: 4.60
OpenGL ES profile version string: OpenGL ES 3.2 Mesa 20.2.6
OpenGL ES profile shading language version string: OpenGL ES GLSL ES 3.20
GL_EXT_shader_implicit_conversions, GL_EXT_shader_integer_mix,
```

Use a versão 2.1 ou a versão correspondente ao seu driver gráfico:

```bash
$ MESA_GL_VERSION_OVERRIDE=2.1 ./Defold
```

```bash
$ MESA_GL_VERSION_OVERRIDE=4.6 ./Defold
```


#### P: Por que recebo "`com.jogamp.opengl.GLException: Graphics configuration failed`" ao iniciar o Defold?

R: Em certas distribuições (por exemplo, Ubuntu 20.04), há um problema com os novos drivers [Mesa](https://docs.mesa3d.org/) (Iris) ao rodar o Defold. Você pode tentar usar uma versão de driver mais antiga ao rodar o Defold:

```bash
$ MESA_LOADER_DRIVER_OVERRIDE=i965 ./Defold
```


#### P: O editor Defold trava ao abrir uma coleção ou objeto de jogo e o crash se refere a `libffi.so`

R: A versão da [libffi](https://sourceware.org/libffi/) da sua distribuição e a exigida pelo Defold (versão 6 ou 7) não correspondem. Certifique-se de que `libffi.so.6` ou `libffi.so.7` esteja instalado em `/usr/lib/x86_64-linux-gnu`. Você pode baixar `libffi.so.7` assim:

```bash
$ wget http://ftp.br.debian.org/debian/pool/main/libf/libffi/libffi7_3.3-6_amd64.deb
$ sudo dpkg -i libffi7_3.3-6_amd64.deb
```

Em seguida, especifique o caminho para essa versão na variável de ambiente `LD_PRELOAD` ao rodar o Defold:

```bash
$ LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libffi.so.7 ./Defold
```


#### P: Meus drivers OpenGL estão desatualizados. Ainda posso usar o Defold?

R: Sim, talvez seja possível usar o Defold se você habilitar a renderização por software. Você pode habilitar a renderização por software definindo a variável de ambiente `LIBGL_ALWAYS_SOFTWARE` como 1:

```bash
$ LIBGL_ALWAYS_SOFTWARE=1 ./Defold
```


#### P: Por que meu jogo Defold não inicia quando tento rodá-lo no Linux?

R: Verifique a saída do console no editor. Se você receber a seguinte mensagem:

```
dmengine: error while loading shared libraries: libopenal.so.1: cannot open shared object file: No such file or directory
```

Então você precisa instalar *`libopenal1`*. O nome do pacote varia entre distribuições e, em alguns casos, talvez você precise instalar os pacotes *`openal`* e *`openal-dev`* ou *`openal-devel`*.

```bash
$ apt-get install libopenal-dev
```

#### P: Por que o menu superior fecha antes que eu consiga selecionar algo?

R: Isso provavelmente é causado pelo gerenciador de janelas usado (por exemplo, `Qtile` ou i3). Este é um [problema conhecido no JavaFX](https://bugs.openjdk.org/browse/JDK-8251240?focusedCommentId=14362084&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-14362084) e pode ser resolvido definindo a variável de ambiente `GDK_DISPLAY` como 1:

```bash
$ GDK_DISPLAY=1 ./Defold

D=2

```

Ou modificando o arquivo `Defold/config` e adicionando `-Djdk.gtk.version=2` à linha `vmargs`:

```
vmargs = -Djdk.gtk.version=2,-Dfile.encoding=UTF-8,...
```


#### P: Por que não consigo navegar por todos os locais de arquivo disponíveis ao selecionar Open From Disk?

R: Se você estiver executando o Defold pela [Steam usando Flatpak](https://flathub.org/apps/com.valvesoftware.Steam), precisa dar permissão à Steam para acessar seus outros discos. Você pode modificar as permissões dos seus aplicativos Flatpak usando o [Flatseal](https://flathub.org/apps/com.github.tchx84.Flatseal) ou uma ferramenta similar.


#### P: Por que não consigo abrir o perfilador web ou qualquer outra opção de menu que exige um navegador?

R: É provável que uma chamada interna para `Desktop.getDesktop().browse(new URI(url));` falhe porque nenhum navegador é detectado em sistemas não GNOME. Tente instalar `libgnome`.

```bash
$ apt-get install libgnome
```
