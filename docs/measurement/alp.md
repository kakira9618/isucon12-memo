## alp
### 概要
アクセスログ解析ツール

### インストール方法
1. alpのインストール
```
wget https://github.com/tkuchiki/alp/releases/download/v0.4.0/alp_linux_amd64.zip
sudo apt install unzip
unzip alp_linux_amd64.zip
sudo mv alp_linux_amd64 alp
sudo mv alp /usr/local/bin/alp
```

alp が使えるようになっていればOK

2. nginx用の拡張設定ファイル（log_format.conf）を作る
```
sudo touch /etc/nginx/conf.d/log_format.conf
sudo chmod 777 /etc/nginx/conf.d/log_format.conf
```

3. log_format.conf に設定を追記
```
log_format ltsv "time:$time_local"
                "\thost:$remote_addr"
                "\tforwardedfor:$http_x_forwarded_for"
                "\treq:$request"
                "\tstatus:$status"
                "\tmethod:$request_method"
                "\turi:$request_uri"
                "\tsize:$body_bytes_sent"
                "\treferer:$http_referer"
                "\tua:$http_user_agent"
                "\treqtime:$request_time"
                "\tcache:$upstream_http_x_cache"
                "\truntime:$upstream_http_x_runtime"
                "\tapptime:$upstream_response_time"
                "\tvhost:$host";

access_log /var/log/nginx/access.log ltsv;
```

### 使い方
```
sudo cat /var/log/nginx/access.log | alp

+-------+--------+-------------------------------------------------------------+-----+------+-----+-----+-----+-------+-------+---------+-------+-------+-------+-------+--------+-----------+-----------+--------------+-----------+
| COUNT | METHOD |                             URI                             | 1XX | 2XX  | 3XX | 4XX | 5XX |  MIN  |  MAX  |   SUM   |  AVG  |  P1   |  P50  |  P99  | STDDEV | MIN(BODY) | MAX(BODY) |  SUM(BODY)   | AVG(BODY) |
+-------+--------+-------------------------------------------------------------+-----+------+-----+-----+-----+-------+-------+---------+-------+-------+-------+-------+--------+-----------+-----------+--------------+-----------+
|     1 | GET    | /api/estate/28817                                           |   0 |    1 |   0 |   0 |   0 | 0.000 | 0.000 |   0.000 | 0.000 | 0.000 | 0.000 | 0.000 |  0.000 |   620.000 |   620.000 |      620.000 |   620.000 |
|     1 | GET    | /api/estate/14721                                           |   0 |    1 |   0 |   0 |   0 | 0.000 | 0.000 |   0.000 | 0.000 | 0.000 | 0.000 | 0.000 |  0.000 |   631.000 |   631.000 |      631.000 |   631.000 |
|     1 | POST   | /api/estate/req_doc/24565                                   |   0 |    1 |   0 |   0 |   0 | 0.000 | 0.000 |   0.000 | 0.000 | 0.000 | 0.000 | 0.000 |  0.000 |     0.000 |     0.000 |        0.000 |     0.000 |
|     1 | GET    | /config/getuser                                             |   0 |    0 |   0 |   1 |   0 | 0.000 | 0.000 |   0.000 | 0.000 | 0.000 | 0.000 | 0.000 |  0.000 |   154.000 |   154.000 |      154.000 |   154.000 |
（略）
```

### 注意点・躓いた点
- nginxのアクセスログ（access.log）が生成されないとき
  - sudo systemctl restart nginx しましたか
  - sudo systemctl reload nginx しましたか
  - そのnginxに本当にアクセスが通っていますか？
    - 生のnginxとdockerで立ち上げたコンテナ内で走るnginxは別物です
  - ファイルのアクセス権限は適切ですか？
    - https://www.bit-hive.com/articles/20220414
    - ディレクトリの所有者、パーミッション、ログファイルの所有者パーミッションをチェック
- コンテナ内ログファイルに対してalpしたい
  - 共有ボリュームを設定してデータを外に出すと吉
  - あるいはnginx自体で配信してしまうとか。

### 参考文献
- https://nasaemon.hateblo.jp/entry/isucon_joban
- https://www.bit-hive.com/articles/20220414
