## ポート番号を利用しているプロセスを特定する

```
# TCPプロトコルを利用しているものを表示
$ sudo lsof -i TCP

# UDPプロトコルを利用しているものを表示
$ sudo lsof -i UDP

# 22ポートを使っているものを表示
$ sudo lsof -i :22
```

### 参考文献
https://qiita.com/toshihirock/items/c6a09575c2d88c210483
