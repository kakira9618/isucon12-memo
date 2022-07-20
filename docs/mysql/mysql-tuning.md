## mysqlをチューニングする
前提：mysql 5.7

### mysqltunerを使ってチューニングしたほうが良い箇所を洗い出す
https://github.com/major/MySQLTuner-perl

1. 準備
my.cnf に performance_schema を有効化する設定を足す。 performance_schema はmysqlのいろいろなパフォーマンスに関する統計情報を取るやつ
```
[mysqld]
performance_schema=ON
```

2. インストール
mysqltuner をダウンロードするだけ。実行に必要なリソースも同時にダウンロードする
```
$ wget http://mysqltuner.pl/ -O mysqltuner.pl
$ wget https://raw.githubusercontent.com/major/MySQLTuner-perl/master/basic_passwords.txt -O basic_passwords.txt
$ wget https://raw.githubusercontent.com/major/MySQLTuner-perl/master/vulnerabilities.csv -O vulnerabilities.csv
```

3. 使い方
```
$ perl mysqltuner.pl --host 127.0.0.1 --user root --pass root
 >>  MySQLTuner 2.0.4
         * Jean-Marie Renouard <jmrenouard@gmail.com>
         * Major Hayden <major@mhtx.net>
 >>  Bug reports, feature requests, and downloads at http://mysqltuner.pl/
 >>  Run with '--help' for additional options and output filtering

[--] Skipped version check for MySQLTuner script
[--] Performing tests on 127.0.0.1:3306
[OK] Logged in using credentials passed on the command line
[OK] Currently running supported MySQL version 5.7.38-log
[OK] Operating on 64-bit architecture
 
-------- Log file Recommendations ------------------------------------------------------------------
[!!] log_error is set to stderr, but this script can't read stderr
 
-------- Storage Engine Statistics -----------------------------------------------------------------
[--] Status: +ARCHIVE +BLACKHOLE +CSV -FEDERATED +InnoDB +MEMORY +MRG_MYISAM +MyISAM +PERFORMANCE_SCHEMA 
[--] Data in InnoDB tables: 28.0M (Tables: 3)
[OK] Total fragmented tables: 0
 
-------- Analysis Performance Metrics --------------------------------------------------------------
[--] innodb_stats_on_metadata: OFF
[OK] No stat updates during querying INFORMATION_SCHEMA.
 
-------- Views Metrics -----------------------------------------------------------------------------
 
-------- Triggers Metrics --------------------------------------------------------------------------
 
-------- Routines Metrics --------------------------------------------------------------------------
 
-------- Security Recommendations ------------------------------------------------------------------
[OK] No Role user detected
[OK] There are no anonymous accounts for any database users
[OK] All database users have passwords assigned
[!!] User 'isucon'@'%' has user name as password.
[!!] User 'root'@'%' has user name as password.
[!!] User 'root'@'localhost' has user name as password.
[!!] User 'isucon'@% does not specify hostname restrictions.
[!!] User 'root'@% does not specify hostname restrictions.
[--] There are 620 basic passwords in the list.
[!!] User 'root@localhost' is using weak password: root in a lower, upper or capitalize derivative version.
[!!] User 'root@%' is using weak password: root in a lower, upper or capitalize derivative version.
 
-------- CVE Security Recommendations --------------------------------------------------------------
[OK] NO SECURITY CVE FOUND FOR YOUR VERSION
 
-------- Performance Metrics -----------------------------------------------------------------------
[--] Up for: 8m 12s (94K q [192.632 qps], 1K conn, TX: 235M, RX: 52M)
[--] Reads / Writes: 91% / 9%
[--] Binary logging is disabled
[--] Physical Memory     : 3.8G
[--] Max MySQL memory    : 942.9M
[--] Other process memory: 0B
[--] Total buffers: 169.0M global + 5.1M per thread (151 max threads)
[--] P_S Max memory usage: 72B
[--] Galera GCache Max memory usage: 0B
[OK] Maximum reached memory usage: 230.5M (5.86% of installed RAM)
[OK] Maximum possible memory usage: 942.9M (23.96% of installed RAM)
[OK] Overall possible memory usage with other process is compatible with memory available
[OK] Slow queries: 0% (0/94K)
[OK] Highest usage of available connections: 7% (12/151)
[OK] Aborted connections: 0.07%  (1/1381)
[OK] Query cache is disabled by default due to mutex contention on multiprocessor machines.
[OK] Sorts requiring temporary tables: 0% (12 temp sorts / 8K sorts)
[OK] No joins without indexes
[OK] Temporary tables created on disk: 0% (0 on disk / 6 total)
[OK] Thread cache hit rate: 99% (12 created / 1K connections)
[OK] Table cache hit rate: 99% (185K hits / 185K requests)
[OK] table_definition_cache (1400) is greater than number of tables (282)
[OK] Open file limit used: 0% (17/1M)
[OK] Table locks acquired immediately: 100% (105 immediate / 105 locks)
 
-------- Performance schema ------------------------------------------------------------------------
[--] Performance_schema is activated.
[--] Memory used by P_S: 72B
[--] Sys schema is installed.
 
-------- ThreadPool Metrics ------------------------------------------------------------------------
[--] ThreadPool stat is disabled.
 
-------- MyISAM Metrics ----------------------------------------------------------------------------
[!!] Key buffer used: 18.3% (1.5M used / 8.0M cache)
[OK] Key buffer size / total MyISAM indexes: 8.0M/43.0K
[!!] Read Key buffer hit rate: 50.0% (10 cached / 5 reads)
 
-------- InnoDB Metrics ----------------------------------------------------------------------------
[--] InnoDB is enabled.
[--] InnoDB Thread Concurrency: 0
[OK] InnoDB File per table is activated
[OK] InnoDB buffer pool / data size: 128.0M / 28.0M
[!!] Ratio InnoDB log file size / InnoDB Buffer pool size (75%): 48.0M * 2 / 128.0M should be equal to 25%
[OK] InnoDB buffer pool instances: 1
[--] Number of InnoDB Buffer Pool Chunk: 1 for 1 Buffer Pool Instance(s)
[OK] Innodb_buffer_pool_size aligned with Innodb_buffer_pool_chunk_size & Innodb_buffer_pool_instances
[OK] InnoDB Read buffer efficiency: 100.00% (59780132 hits/ 59780452 total)
[OK] InnoDB Write log efficiency: 99.40% (82292 hits/ 82792 total)
[OK] InnoDB log waits: 0.00% (0 waits / 500 writes)
 
-------- Aria Metrics ------------------------------------------------------------------------------
[--] Aria Storage Engine not available.
 
-------- TokuDB Metrics ----------------------------------------------------------------------------
[--] TokuDB is disabled.
 
-------- XtraDB Metrics ----------------------------------------------------------------------------
[--] XtraDB is disabled.
 
-------- Galera Metrics ----------------------------------------------------------------------------
[--] Galera is disabled.
 
-------- Replication Metrics -----------------------------------------------------------------------
[--] Galera Synchronous replication: NO
[--] No replication slave(s) for this server.
[--] Binlog format: ROW
[--] XA support enabled: ON
[--] Semi synchronous replication Master: Not Activated
[--] Semi synchronous replication Slave: Not Activated
[--] This is a standalone server
 
-------- Recommendations ---------------------------------------------------------------------------
General recommendations:
    Set up a Secure Password for 'isucon'@'%' user: SET PASSWORD FOR 'isucon'@'%' = PASSWORD('secure_password');
    Set up a Secure Password for 'root'@'%' user: SET PASSWORD FOR 'root'@'%' = PASSWORD('secure_password');
    Set up a Secure Password for 'root'@'localhost' user: SET PASSWORD FOR 'root'@'localhost' = PASSWORD('secure_password');
    Restrict Host for 'isucon'@'%' to 'isucon'@LimitedIPRangeOrLocalhost
    RENAME USER 'isucon'@'%' TO 'isucon'@LimitedIPRangeOrLocalhost;
    Restrict Host for 'root'@'%' to 'root'@LimitedIPRangeOrLocalhost
    RENAME USER 'root'@'%' TO 'root'@LimitedIPRangeOrLocalhost;
    Set up a Secure Password for root@localhost user: SET PASSWORD FOR 'root'@'localhost' = PASSWORD('secure_password');
    Set up a Secure Password for root@% user: SET PASSWORD FOR 'root'@'%' = PASSWORD('secure_password');
    2 user(s) used basic or weak password from basic dictionary.
    MySQL was started within the last 24 hours - recommendations may be inaccurate
    Before changing innodb_log_file_size and/or innodb_log_files_in_group read this: https://bit.ly/2TcGgtU
Variables to adjust:
    key_buffer_size (~ 1M)
    innodb_log_file_size should be (=16M) if possible, so InnoDB total log files size equals 25% of buffer pool size.
```
ISUCONではセキュリティ系の箇所は基本読み飛ばしても良い。Recomendations と Variables to adjust を見ていく。

## mysqlをチューニングする
https://qiita.com/mamy1326/items/9c5eaee3c986cff65a55 を見ながらチューニングしていく。  
(記事は mysql 5.5 についての情報で、mysql 5.7 ではパラメータ名や動作に変更が加えられているので注意: https://www.slideshare.net/yoku0825/mysql-57-51945745)

チューニング結果は以下の通り  
https://github.com/kakira9618/isucon10-qual-webapp/pull/6

/etc/my.cnf
```ini
# #################
# innodb
# #################

# InnoDBのデータとインデックスをキャッシュするバッファのサイズ(推奨は物理メモリの8割)
innodb_buffer_pool_size=3G

# InnoDBのデータ・ディクショナリーや内部データ構造情報を持つバッファのサイズ
# innodb_additional_mem_pool_size=20M  # mysql 5.7 ではコメントアウト

# コミットされていないトランザクションのためのバッファのサイズ
innodb_log_buffer_size=64M

# InnoDBの更新ログを記録するディスク上のファイルサイズ(innodb_buffer_pool_sizeの4分の1程度)
innodb_log_file_size=750M

# データやインデックスを共有ではなくテーブル個別に保存する
innodb_file_per_table=1

# #################
# query cache
# #################

# クエリキャッシュ最大サイズ
query_cache_limit=16M

# クエリキャッシュで使用するメモリサイズ
query_cache_size=512M

# クエリキャッシュのタイプ(0:off, 1:ON SELECT SQL_NO_CACHE以外, 2:DEMAND SELECT SQL_CACHEのみ)
query_cache_type=1

# #################
# etc
# #################

# インデックス未使用でのJOIN時に使用するバッファ
join_buffer_size=256K

# クライアントからサーバーに送信できるパケットの最大長
max_allowed_packet=8M

# フルスキャンのレコードバッファ
read_buffer_size=1M

# キーを使用したソートで読み込まれた行がキャッシュされるバッファ
read_rnd_buffer_size=2M

# ソート時に使用されるバッファ
sort_buffer_size=4M

# MEMORYテーブルの最大サイズ。このサイズを超えたMEMORYテーブルはディスク上に作成
max_heap_table_size=16M

# スレッド毎に作成される一時的なテーブルの最大サイズ。スレッドバッファ
tmp_table_size=16M

# スレッドキャッシュ保持最大数
thread_cache_size=100

# コネクションタイムアウト時間
wait_timeout=30
```

最悪意味がわからなくてもコピペでスコア1.5倍とかになったりするのでやりましょう。

### 参考文献
- https://github.com/major/MySQLTuner-perl
- https://qiita.com/mamy1326/items/9c5eaee3c986cff65a55
- https://www.slideshare.net/yoku0825/mysql-57-51945745
- https://github.com/kakira9618/isucon10-qual-webapp/pull/6
