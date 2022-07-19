## nginxのパラメータチューニング
https://qiita.com/cubicdaiya/items/235777dc401ec419b14e

```
worker_processes 16;

events {
    worker_connections  10240;
    accept_mutex_delay 100ms;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    access_log off;

    sendfile on;
    open_file_cache max=100 inactive=20s;
    tcp_nopush on;

    keepalive_timeout  65;

    server {
        listen       80;
        server_name  localhost;
        location / {
            root   html;
            index  index.html index.htm;
        }
    }
}
```

[ファイルディスクリプタの設定](../linux/fd-tuning.md)も参考にしてください。

## 参考文献
- https://qiita.com/cubicdaiya/items/235777dc401ec419b14e
- https://github.com/kakira9618/isucon10-qual-webapp/pull/7