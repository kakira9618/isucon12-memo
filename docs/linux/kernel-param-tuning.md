## カーネルパラメータ設定
設定パラメータ名と値、設定すべき状況等は https://matsukaz.hatenablog.com/entry/2018/09/20/081855 を参考にしよう

### カーネルパラメータの確認
```
$ sudo sysctl -a
abi.vsyscall32 = 1
debug.exception-trace = 1
debug.kprobes-optimization = 1
dev.cdrom.autoclose = 1
dev.cdrom.autoeject = 0
dev.cdrom.check_media = 0
dev.cdrom.debug = 0
dev.cdrom.info = CD-ROM information, Id: cdrom.c 3.20 2003/12/17
dev.cdrom.info = 
dev.cdrom.info = drive name:            sr0
…
```

net.ipv4.tcp_rmem だけ確認する場合
```
$ sudo sysctl net.ipv4.tcp_rmem
net.ipv4.tcp_rmem = 4096        131072  6291456
```

### カーネルパラメータの書き換え
net.ipv4.tcp_rmem を書き換える場合

- 一時的に書き換え
```
$ sudo sysctl -w net.ipv4.tcp_rmem="8192 131072 6291456"
```

- 恒久的に書き換え
```
$ sudo vim /etc/sysctl.conf

fs.file-max = 1048576
net.ipv4.tcp_rmem = 8192 131072 6291456
```

### ISUCONで使いそうなやつ（デフォルト設定）
```bash
$ sudo sysctl fs.file-max
fs.file-max = 1048576
$ sudo sysctl fs.aio-max-nr
fs.aio-max-nr = 65536
$ sudo sysctl kernel.threads-max
kernel.threads-max = 31177
$ sudo sysctl kernel.pid_max
kernel.pid_max = 4194304
$ sudo sysctl vm.max_map_count
vm.max_map_count = 65530
$ sudo sysctl vm.swappiness
vm.swappiness = 60
$ sudo sysctl net.core.somaxconn
net.core.somaxconn = 4096
$ sudo sysctl net.ipv4.tcp_max_syn_backlog
net.ipv4.tcp_max_syn_backlog = 256
$ sudo sysctl net.core.netdev_max_backlog
net.core.netdev_max_backlog = 1000
$ sudo sysctl net.ipv4.tcp_tw_reuse
net.ipv4.tcp_tw_reuse = 2
$ sudo sysctl net.ipv4.ip_local_port_range
net.ipv4.ip_local_port_range = 32768    60999
$ sudo sysctl net.ipv4.tcp_fin_timeout
net.ipv4.tcp_fin_timeout = 60
```

### ISUCONで使いそうなやつをいくつか変更
`sudo sysctl -a` でバックアップを取得してからが吉

リスクが低そうなものだけ。`/etc/sysctl.conf` に書いてリブートしよう
```
$ sudo sh -c 'cat <<EOS >> /etc/sysctl.conf
fs.file-max = 1048576
vm.swappiness = 15
net.ipv4.tcp_tw_reuse = 1
net.ipv4.ip_local_port_range = 1024 65535
net.ipv4.tcp_fin_timeout = 10
EOS
'
```
