#### Q: 4k または HiDPI モニターで実行すると、Defold エディターが極端に小さく表示されるのはなぜですか？ {#q-why-is-the-defold-editor-super-small-when-run-on-a-4k-or-hidpi-monitor}

A: GNOME を使用している場合は、Defold を実行する前に表示倍率を変更できます。[出典](https://unix.stackexchange.com/a/552411)

```bash
$ gsettings set org.gnome.desktop.interface scaling-factor 2
$ ./Defold
```

A: 別の解決方法として、特に小数を含む倍率で拡大したい場合は、`Defold/config` ファイルの `vmargs` 行に `glass.gtk.uiScale` を追加します。[出典](https://forum.defold.com/t/4k-hidpi-monitor-support-solved/64108/12?u=britzl)

```
vmargs = -Dglass.gtk.uiScale=1.5,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=175%,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=192dpi,-Dfile.encoding=UTF-8,...
```

この値の詳細は、[Arch Linux wiki の HiDPI の記事](https://wiki.archlinux.org/title/HiDPI#JavaFX)を参照してください。

A: KDE を使用している場合は、`GDK_SCALE` を設定できます。

```bash
$ GDK_SCALE=2 ./Defold
```

#### Q: Elementary OS でマウスのクリックがエディターを通り抜けて、背後にあるものに届くのはなぜですか？ {#q-why-does-mouse-clicks-on-elementary-os-go-through-the-editor-onto-whatever-is-below}

A: 次のようにエディターを起動します。

```bash
$ GTK_CSD=0 ./Defold
```


#### Q: コレクション（collection）やゲームオブジェクト（game object）を開くと Defold エディターがクラッシュし、クラッシュ時の情報に `com.jogamp.opengl` が含まれます {#q-the-defold-editor-crashes-when-opening-a-collection-or-game-object-and-the-crash-refers-to-comjogampopengl}

A: 一部のディストリビューション（Ubuntu 18 など）では、Defold が使用する `jogamp`/`jogl` と、システム上の [Mesa](https://docs.mesa3d.org/) のバージョンの組み合わせに問題があります。`MESA_GL_VERSION_OVERRIDE` を 2.1 以上、かつドライバーが対応するバージョン以下の値に設定すると、`glGetString(GL_VERSION)` の呼び出し時に報告される GL バージョンを上書きできます。ドライバーが対応する OpenGL の最大バージョンは、`glxinfo` で確認できます。

```bash
glxinfo | grep version
```

出力例（「OpenGL version string: x.y」を探してください）：

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

バージョン 2.1 またはグラフィックスドライバーに対応するバージョンを使用します。

```bash
$ MESA_GL_VERSION_OVERRIDE=2.1 ./Defold
```

```bash
$ MESA_GL_VERSION_OVERRIDE=4.6 ./Defold
```


#### Q: Defold の起動時に「`com.jogamp.opengl.GLException: Graphics configuration failed`」と表示されるのはなぜですか？ {#q-why-am-i-getting-comjogampopenglglexception-graphics-configuration-failed-when-launching-defold}

A: 一部のディストリビューション（Ubuntu 20.04 など）では、Defold の実行時に新しい [Mesa](https://docs.mesa3d.org/) ドライバー（Iris）で問題が発生します。Defold の実行時に古いバージョンのドライバーを使用してみてください。

```bash
$ MESA_LOADER_DRIVER_OVERRIDE=i965 ./Defold
```


#### Q: コレクションやゲームオブジェクトを開くと Defold エディターがクラッシュし、クラッシュ時の情報に `libffi.so` が含まれます {#q-the-defold-editor-crashes-when-opening-a-collection-or-game-object-and-the-crash-refers-to-libffiso}

A: ディストリビューションの [libffi](https://sourceware.org/libffi/) のバージョンと、Defold が必要とするバージョン（6 または 7）が一致していません。`libffi.so.6` または `libffi.so.7` が `/usr/lib/x86_64-linux-gnu` にインストールされていることを確認してください。`libffi.so.7` は次のようにダウンロードできます。  

```bash
$ wget http://ftp.br.debian.org/debian/pool/main/libf/libffi/libffi7_3.3-6_amd64.deb
$ sudo dpkg -i libffi7_3.3-6_amd64.deb
```

次に、Defold の実行時に、このバージョンへのパスを環境変数 `LD_PRELOAD` で指定します。

```bash
$ LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libffi.so.7 ./Defold
```


#### Q: OpenGL ドライバーが古いのですが、Defold を使用できますか？ {#q-my-opengl-drivers-are-outdated-can-i-still-use-defold}

A: はい、ソフトウェアレンダリングを有効にすると Defold を使用できる可能性があります。環境変数 `LIBGL_ALWAYS_SOFTWARE` を 1 に設定すると、ソフトウェアレンダリングを有効にできます。

```bash
$ LIBGL_ALWAYS_SOFTWARE=1 ./Defold
```


#### Q: Linux で実行しようとすると、Defold のゲームが起動しないのはなぜですか？ {#q-why-doesnt-my-defold-game-start-when-i-try-to-run-it-on-linux}

A: エディターのコンソール出力を確認してください。次のメッセージが表示される場合は、

```
dmengine: error while loading shared libraries: libopenal.so.1: cannot open shared object file: No such file or directory
```

*`libopenal1`* をインストールする必要があります。パッケージ名はディストリビューションによって異なり、場合によっては *`openal`* と、*`openal-dev`* または *`openal-devel`* のパッケージをインストールする必要があります。

```bash
$ apt-get install libopenal-dev
```

#### Q: 項目を選択する前に上部のメニューが閉じてしまうのはなぜですか？ {#q-why-does-the-top-menu-close-before-i-can-select-something}

A: 使用しているウィンドウマネージャー（`Qtile` や i3 など）が原因と考えられます。これは [JavaFX の既知の問題](https://bugs.openjdk.org/browse/JDK-8251240?focusedCommentId=14362084&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-14362084)で、環境変数 `GDK_DISPLAY` を 1 に設定すると解決できます。

```bash
$ GDK_DISPLAY=1 ./Defold

D=2

```

または、`Defold/config` ファイルの `vmargs` 行に `-Djdk.gtk.version=2` を追加することでも解決できます。

```
vmargs = -Djdk.gtk.version=2,-Dfile.encoding=UTF-8,...
```


#### Q: Open From Disk を選択したときに、利用可能なファイルの場所をすべて参照できないのはなぜですか？ {#q-why-am-i-not-able-to-browse-all-available-file-locations-when-i-select-open-from-disk}

A: [Flatpak を使用した Steam](https://flathub.org/apps/com.valvesoftware.Steam) から Defold を実行している場合は、他のドライブにアクセスする権限を Steam に付与する必要があります。Flatpak アプリケーションの権限は、[Flatseal](https://flathub.org/apps/com.github.tchx84.Flatseal) などのツールで変更できます。


#### Q: Web プロファイラーや、ブラウザーを必要とする他のメニュー項目を開けないのはなぜですか？ {#q-why-am-i-not-able-to-open-the-web-profiler-or-any-other-menu-option-which-requires-a-browser}

A: Gnome 以外のシステムではブラウザーが検出されないため、内部での `Desktop.getDesktop().browse(new URI(url));` の呼び出しが失敗していると考えられます。`libgnome` をインストールしてみてください。

```bash
$ apt-get install libgnome
```