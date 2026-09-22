#### Q: HTML5 uygulamam Chrome'da neden açılış ekranında donuyor?

A: Bazı durumlarda bir oyunu tarayıcıda yerel dosya sisteminden çalıştırmak mümkün değildir. Oyunu düzenleyiciden çalıştırdığınızda oyun yerel bir web sunucusundan sunulur. Örneğin, Python'daki `SimpleHTTPServer` modülünü kullanabilirsiniz:

```sh
$ python -m SimpleHTTPServer [port]
```


#### Q: Oyunum yüklenirken neden "Unexpected data size" hatasıyla çöküyor?

A: Bu durum genellikle Windows kullanırken bir derleme çıktısı oluşturup bunu Git'e kaydettiğinizde (commit) ortaya çıkar. Git'teki satır sonu yapılandırmanız yanlışsa Git satır sonlarını ve dolayısıyla veri boyutunu da değiştirir. Sorunu çözmek için şu yönergeleri izleyin: [https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings](https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings)
