## dstat
### 概要
OSのパフォーマンス指標をわかりやすく表示するコマンドラインツール

### インストール方法
```
$ sudo apt install dstat
```

### 使い方
1. 普通に表示
```
$ dstat
--total-cpu-usage-- -dsk/total- -net/total- ---paging-- ---system--
usr sys idl wai stl| read  writ| recv  send|  in   out | int   csw
  2   1  96   0   0| 580k  597k|   0     0 |   0     0 | 678  1178
  0   1  98   0   0|   0     0 | 612B  844B|   0     0 | 246   373
  2   1  97   0   0|   0   124k| 494B  342B|   0     0 | 410   583
  1   1  98   0   0|   0     0 |2344B 2588B|   0     0 | 293   489
```

2. メモリとかいろいろ
```
$ dstat -Tclmdrn
--epoch--- --total-cpu-usage-- ---load-avg--- ------memory-usage----- -dsk/total- --io/total- -net/total-
  epoch   |usr sys idl wai stl| 1m   5m  15m | used  free  buff  cach| read  writ| read  writ| recv  send
1657716533|  2   1  96   0   0|0.16 0.10 0.08| 697M  350M 92.5M 2667M| 572k  601k|15.5  4.56 |   0     0
1657716534|  1   1  98   0   0|0.16 0.10 0.08| 697M  349M 92.5M 2667M|   0     0 |   0     0 | 606B 1142B
1657716535|  1   1  99   0   0|0.16 0.10 0.08| 697M  349M 92.5M 2667M|   0     0 |   0     0 |2404B 2684B
1657716536|  1   0  98   0   0|0.16 0.10 0.08| 697M  349M 92.5M 2667M|   0     0 |   0     0 | 426B  446B
1657716537|  0   1  99   0   0|0.16 0.10 0.08| 697M  349M 92.5M 2667M|   0     0 |   0     0 | 486B  446B
```

3. その他は https://qiita.com/ryuichi1208/items/387fa1cba44690c3db9b

### 備考・注意点・躓いた点
- なし。指標の読み方は ![netdata.md](./netdata.md) を参照

### 参考文献
- https://qiita.com/ryuichi1208/items/387fa1cba44690c3db9b
