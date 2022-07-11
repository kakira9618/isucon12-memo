## pt-query-digest
### 概要
特定の形式のログファイル（mysqlのslow-logやtcpdumpなど）を解析・集計してわかりやすく表示してくれるコマンド

### インストール方法
1. まず、対象のmysqldの設定を変更し、スローログが出力されるようにする
```
$ vim /etc/my.cnf # サーバー本体ではなく、docker containerの中のmy.cnfを変更しなければならない場合に注意する
```
```
[mysqld]
character-set-server=utf8mb4
slow_query_log=1
slow_query_log_file='/tmp/slow.log'
long_query_time=0.01
```

2. （最悪飛ばしてもOK) スロークエリ設定ができているかどうか確認する

mysqld にログインする。`mysql` でログインできなかったら、接続情報は環境変数 (.env, env.sh) や設定ファイル (.yaml) などにあるはずなので調べる
```
$ mysql -u ユーザ名 -p データベース名
Enter password:（パスワードを入力）
```
```
mysql> show variables like 'slow_query%';
+---------------------+---------------+
| Variable_name       | Value         |
+---------------------+---------------+
| slow_query_log      | ON            |
| slow_query_log_file | /tmp/slow.log |
+---------------------+---------------+
2 rows in set (0.01 sec)

mysql> show variables like 'long%';
+-----------------+----------+
| Variable_name   | Value    |
+-----------------+----------+
| long_query_time | 0.010000 |
+-----------------+----------+
1 row in set (0.00 sec)
```

3. percona-toolkit をインストールする（と自動的にpt-query-digestも入る）
```
$ cd ~
$ git clone https://github.com/percona/percona-toolkit
$ cd percona-toolkit
$ perl Makefile.PL
$ make
$ make test
$ make install
```
```
$ pt-query-digest --version
pt-query-digest 3.4.0
```

### 使い方

1. 負荷テスト実行
2. 集計
```
$ sudo cat /tmp/slow.log | pt-query-digest
```

[実行結果](./resources/pt-query-digest-result.txt)はこんな感じ


### 備考・注意点・躓いた点
- 巷の解説サイトを参考にすると古いバージョンのをインストールすることになりがちなので注意
- `pt-query-digest filename` で直接ファイル名を指定することもできるが、パーミッション関連がしっかり設定されていないとうまく行かないので注意
  - pt-query-digest がうまくファイルを読めなかった場合、`# No events processed.` と出力される
  - ログファイルの中身が確かにあるのにコレが出たら、パーミッション関連の問題であることが多い
- 基本的にデフォルトの設定で十分使えそうだが、集計方法をカスタマイズしたい場合は [こちら](https://www.percona.com/doc/percona-toolkit/LATEST/pt-query-digest.html) を参照。

### 参考文献
- https://github.com/percona/percona-toolkit
- https://www.percona.com/doc/percona-toolkit/LATEST/pt-query-digest.html
