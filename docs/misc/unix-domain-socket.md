# Unix Domain Socket

## Unix Domain Socket とは

普通、プロセスたちは TCP を通じて通信を行う。  
TCP はリモート相手でも通信できるので、違うインスタンス内のプロセスとも通信できるのがメリットだが、オーバーヘッドが大きく、細かい通信をたくさん行うのに向いていない。

最初から同じインスタンス内で動くプロセスたちの通信には、ファイル（に見せかけたメモリ内の領域）を使って直接情報をやり取りするのが早い。

Unixにおけるそのようなファイルを Unix Domain Socket (UDS) という。

nginx - app 間の通信を TCP ではなく UDS で行うのは、ISUCONでは頻出のテクニックである。  
(他には app - memcached / redis などの通信にもUDSが有効。app - db 間は後でインスタンスを分けて運用したくなることが多いのでUDSは使わないほうが無難。)

## 設定方法

### docker-compose を使っている場合
docker-composeを使っていない（そのままsystemd上で動いているなど）場合はスキップ。  
コンテナ間共有ボリュームを作り、共通ボリュームとそれぞれのコンテナ内パスを結びつける。  
このとき dockerize などの疎通確認用のコマンド内容も変更する必要がある。  
環境変数にパスを入れておくと管理が docker-compose.yml だけになって楽。

例：docker-compose.yml（/var/run/app/app.sock を使うと決めた場合）
```yaml
  api-server:
    build: ../go
    entrypoint:
      - dockerize
      - -timeout
      - 60s
      - -wait
      - tcp://mysql:3306
    volumes:
      - ../mysql/db:/go/src/mysql/db
      - ../fixture:/go/src/fixture
      - appsocket:/var/run/app # 追加
    environment:
      SOCK_PATH: /var/run/app/app.sock # 追加(オプション)
      MYSQL_DBNAME: isuumo
      MYSQL_USER: isucon
      MYSQL_PASS: isucon
      MYSQL_HOST: mysql
      SERVER_PORT: 1323
    ports:
      - "1323:1323"
      - "6060:6060"
    depends_on:
      - mysql
    command: /go/src/isuumo/isuumo

  frontend:
    build: ../frontend
    volumes:
      - ../nginx/out:/frontend/out

  nginx:
    build: ../nginx
    volumes:
        - ../../provisioning/ansible/roles/web-bootstrap/files/nginx.conf.template:/etc/nginx/nginx.conf.template
        - ../logs/nginx:/var/log/nginx
        - ../nginx/conf.d:/etc/nginx/conf.d
        - ../nginx/out:/www/data
        - appsocket:/var/run/app #追加
    ports:
      - "8080:80"
    entrypoint:
      - dockerize
      - -timeout
      - 60s
      - -wait
      - unix:/var/run/app/app.sock # 変更 dockerizeの疎通確認でこの.sockが存在するかを確認する
    environment:
      API_SERVER: api-server
      SOCK_PATH: /var/run/app/app.sock # 追加(オプション)
    depends_on:
      - frontend
    command: >
      /bin/sh -c
      "envsubst '
      $$API_SERVER
      '< /etc/nginx/nginx.conf.template
      > /etc/nginx/nginx.conf
      && nginx -g 'daemon off;'"

# 追加
volumes:
  appsocket: # この docker-compose.yml 内での共通ボリュームの名前
    driver_opts:
      type: none
      device: /var/run/app # ホスト側のディレクトリのパス (予め mkdir -p /var/run/app などでディレクトリを作っておく)
      o: bind
```

### 各コンテナ内で Unix Domain Socket を使うように設定する

実際に各コンテナ内で動くサービスの設定を変えて、tcp ではなく unix domain socket を見てもらうようにする

- nginx の場合

例：nginx.conf
```nginx
    upstream appuds {
        server unix:/var/run/app/app.sock; # 通信に使うソケットファイルのパス (環境変数から取ってくるべきだがハマったので直値)
    }

    server {
        listen 80 default_server;
        listen [::]:80 default_server;

        location /api {
            #proxy_pass http://${API_SERVER}:1323;
		    proxy_pass http://appuds; # upstream 名を記入
        }

        location /initialize {
            #proxy_pass http://${API_SERVER}:1323;
		    proxy_pass http://appuds; # upstream 名を記入
        }

        location / {
                root /www/data;
        }
    }
```

- Go (echo) アプリケーションの場合

例: main.go
```go
import (
    …
    "net"  // 追加
    "net/http" // 追加
    "github.com/labstack/echo"
	"github.com/labstack/echo/middleware"
    …
)
func main() {
    …
    e := echo.New()
    …
    // Start server (TCP でのスタート処理)
	// serverPort := fmt.Sprintf(":%v", getEnv("SERVER_PORT", "1323"))
	// e.Logger.Fatal(e.Start(serverPort))

	// ここからソケット接続設定 ---
	socket_file := getEnv("SOCK_PATH", "/var/run/app/app.sock")
	os.Remove(socket_file)

	l, err := net.Listen("unix", socket_file)
	if err != nil {
		e.Logger.Fatal(err)
	}

	// go runユーザとnginxのユーザ（グループ）を同じにすれば777じゃなくてok
	err = os.Chmod(socket_file, 0777)
	if err != nil {
		e.Logger.Fatal(err)
	}

	e.Listener = l
	// ここまで ---

	e.Logger.Fatal(e.Start(""))
    …
}
```

## 備考・躓いた点・注意点
- TCP接続でも接続可能にしたい。
  - 調査中
  - ワークアラウンドとして、下みたいにするのはアリ。
  ```go
    if getEnv("MY_SERVER_ON_UDS", "undef") != "undef" {
        e.Logger.Fatal(e.Start(""))
    } else {
        e.Logger.Fatal(e.Start(serverPort))
    }
  ```
- pprof と両立させたい。
  - nginx 経由でアクセスすれば外側からはTCPに見えるのを使って、appサーバーの実装に pprof を同居させておいて、nginxからpass_proxyすれば良い
- なんか接続できない
  - ログを確認しよう。nginx なら `/var/log/error.log` とか。
- いつのまにホスト側のソケットファイルが消えてる
  - /tmp/ 以下とかに作ると消えたりする。/var 以下にディレクトリを作ろう

## 参考文献
- https://qiita.com/jungissei/items/62aceb4f8962e6f38266
- https://belhb.hateblo.jp/entry/2019/01/08/192010
