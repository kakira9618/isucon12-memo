## ファイルディスクリプタ(fd)のチューニング
前提：Ubuntu 20.04
OS全体とプロセス（デーモン以外）とプロセス（デーモン）で分けて設定する。設定が終わったらマシン再起動して確認したほうが良い。

### OS全体
```
$ sudo vim /etc/sysctl.conf
fs.file-max = 1048576

$ sudo sysctl -p   # 適用して表示する
fs.file-max = 1048576
```

### プロセス(デーモン以外)

- プロセス(デーモン以外) が使えるファイルディスクリプタ数を確認
```
$ ps auxfww | grep nginx
root      337500  0.0  0.1  10772  4536 ?        S     7月19   0:00          \_ nginx: master process nginx -g daemon off;
www-data  337501  0.0  0.0  11152  2672 ?        S     7月19   0:00              \_ nginx: worker process
www-data  337502  0.0  0.0  11152  2672 ?        S     7月19   0:00              \_ nginx: worker process
www-data  337503  0.0  0.0  11152  2672 ?        S     7月19   0:00              \_ nginx: worker process
www-data  337504  0.0  0.0  11152  2672 ?        S     7月19   0:00              \_ nginx: worker process

$ cat /proc/337501/limits
Limit                     Soft Limit           Hard Limit           Units     
Max cpu time              unlimited            unlimited            seconds   
Max file size             unlimited            unlimited            bytes     
Max data size             unlimited            unlimited            bytes     
Max stack size            8388608              unlimited            bytes     
Max core file size        unlimited            unlimited            bytes     
Max resident set          unlimited            unlimited            bytes     
Max processes             unlimited            unlimited            processes 
Max open files            1048576              1048576              files     
Max locked memory         65536                65536                bytes     
Max address space         unlimited            unlimited            bytes     
Max file locks            unlimited            unlimited            locks     
Max pending signals       15607                15607                signals   
Max msgqueue size         819200               819200               bytes     
Max nice priority         0                    0                    
Max realtime priority     0                    0                    
Max realtime timeout      unlimited            unlimited            us     
```
- Max open files の値の読み方：
    - Soft Limit: 一般ユーザが設定した上限値。
    - Hard Limit: rootが設定した上限値
    - 実際に適用されるのは min(Soft Limit, Hard Limit, OS Setting)

- プロセスが使えるファイルディスクリプタ数の設定
```
$ sudo vim /etc/pam.d/common-session
session required pam_limits.so

$ sudo vim /etc/security/limits.conf
*   soft   nofile   1048576
*   hard  nofile   1048576
```
*は全ユーザを意味する。

### プロセス(デーモン) nginx
- nginx の worker process のfdの設定は /etc/nginx/nginx.conf で行う
  - https://www.1x1.jp/blog/2013/02/nginx_too_many_open_files_error.html
  - https://qiita.com/mikene_koko/items/85fbe6a342f89bf53e89
```
worker_processes  auto; # 4-Core CPU では 4プロセス
worker_rlimit_nofile 260000; # 1048576(OS全体fdリミット)/worker_processes

events {
    worker_connections  86666; # worker_rlimit_nofile / 3
}
```
  - `$ sudo systemctl restart nginx` で master process に反映
  - `$ sudo systemctl reload nginx` で worker process に反映

### プロセス(デーモン) docker
docker は https://docs.docker.jp/engine/articles/systemd.html を参考にする
### プロセス(デーモン) MySQL
mysql は https://sys-guard.com/post-15323/ を参考にする

### プロセス(デーモン) それ以外
- これら以外は /etc/systemd/system/<serviceName>.service.d/00-limits.conf に
```
[Service]
LimitNOFILE=1048576:1048576
```
みたいに書く。 

### 参考文献
- https://www.1x1.jp/blog/2013/02/nginx_too_many_open_files_error.html
- https://qiita.com/mikene_koko/items/85fbe6a342f89bf53e89
- https://stackoverflow.com/questions/17483723/command-not-found-when-using-sudo-ulimit
- https://qiita.com/KEINOS/items/f3e6b3064b0cbe35fd03
- https://oji-cloud.net/2022/03/16/post-6951/
- https://docs.docker.jp/engine/articles/systemd.htm
