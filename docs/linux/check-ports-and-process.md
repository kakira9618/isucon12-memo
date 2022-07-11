## ポート番号を利用しているプロセスを特定する

```
# TCPプロトコルを利用しているものを表示
$ sudo lsof -i TCP

# UDPプロトコルを利用しているものを表示
$ sudo lsof -i UDP

# 22ポートを使っているものを表示
$ sudo lsof -i :22
```

```
$ sudo lsof -i :8080
COMMAND    PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
docker-pr 4507 root    4u  IPv4 105476      0t0  TCP *:http-alt (LISTEN)
docker-pr 4522 root    4u  IPv6 101283      0t0  TCP *:http-alt (LISTEN)
```
### 参考文献
https://qiita.com/toshihirock/items/c6a09575c2d88c210483
