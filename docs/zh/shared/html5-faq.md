#### Q: 我的HTML5游戏在Chrome里一到溅射屏幕就卡死了?

A: 很多浏览器不允许从本地磁盘文件来启动程序. 从编辑器里运行就能自动生成临时本地服务器. 另外, 你也可以使用 Python 之类的程序快速搭建本地服务器 SimpleHTTPServer:

```sh
$ python -m SimpleHTTPServer [port]
```


#### Q: 游戏加载时报 "Unexpected data size" 错误然后崩溃?

A: 这种情况可能发生在使用 Windows 编译并且提交到 Git 上的时候. 如果 Git 配置文件里含有不正确的行尾符上传的时候就会被自动改正造成数据大小变化. 解决方案详见: https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings
