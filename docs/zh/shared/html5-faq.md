#### Q: 我的HTML5游戏在Chrome里一到溅射屏幕就卡死了?

A: 很多浏览器不允许从本地磁盘文件来启动程序. 从编辑器里运行就能自动生成临时本地服务器. 另外, 你也可以使用 Python 之类的程序快速搭建本地服务器 SimpleHTTPServer:

```sh
$ python -m SimpleHTTPServer [port]
```
