## Redis
### 概要
インメモリDB。基本的に key-value store で管理するが、言語付属の HashMap 等と異なり、情報は不揮発的に保存する。
つまり、再起動してもデータは保持されたままとなる。
普段はメモリ内にデータを管理しておき（速い）、随時タイミングを見つけてHDDに書き出しておく、みたいなことが簡単にできる。

### インストール方法
1. redis-server のインストール
    - (A) system 直下に直接入れる方法  
    [ここを参照](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04-ja)

    - (B) docker-compose を使う場合  
    docker-compose.yml を編集する。データディレクトリのパスは環境に合わせて変更すること。  
    変更したら `docker-compose up` すればできるはず（redisが立ち上がらない場合は、`--build` オプションが正しいかどうか確認しよう）
```
  redis:
    image: "redis:latest"
    ports:
      - "6379:6379"
    volumes:
      - "../logs/redis:/data"  # データディレクトリのパス。ホスト側:コンテナ側
```

2. （飛ばしてもOK）動作確認
```
$ sudo docker-compose -f docker-compose/go.yaml exec redis bash
# redis-cli
127.0.0.1:6379> ping
PONG
127.0.0.1:6379> set test "It's working!"
OK
127.0.0.1:6379> get test
"It's working!"
127.0.0.1:6379> exit
```
コンテナを再起動してもデータを保持しているはず
```
$ sudo docker-compose -f docker-compose/go.yaml down
$ sudo docker-compose -f docker-compose/go.yaml exec redis bash
# redis-cli
127.0.0.1:6379> get test
"It's working!"
127.0.0.1:6379> exit
```

### 使い方
Goアプリケーションに組み込む場合。細かい使い方は [コミットを参照](https://github.com/kakira9618/isucon10-qual-webapp/pull/4/commits/7a738ae4ab3bb1bfa6b0286309e5905881cabc2b) してください。

使い方抜粋

```
    rdb = redis.NewClient(&redis.Options{
        Addr:     "redis:6379",
        Password: "", // no password set
        DB:       0,  // use default DB
    })
```
接続してクライアントオブジェクトを作成している。  
このオブジェクトはグローバルに定義しておき、アプリの起動時に一回だけ初期化すれば良い（リクエストごとに作っていると遅くなる、はず）

```
ret, err := rdb.Get(ctx, "count").Result()
```
`count` というキーを指定して、データを取得している。まだデータが定義されていないときは err が設定される。
返り値は `string` 型。
```
err = rdb.Set(ctx, "count", fmt.Sprintf("%d", val), 0).Err()
```
`count` キーにデータを設定している。int型は直接設定できないので注意（string型に変換が必要）。

他にも sharding, go-redis/cache が結構使えそう（未検証）

### 備考・注意点・躓いた点
- データ型に注意。基本的に string. 任意の型を使いたい場合は go-redis/cache が使えそう
    - https://redis.uptrace.dev/guide/go-redis-cache.html#go-redis-cache

### 参考文献
- https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04-ja
- https://github.com/kakira9618/isucon10-qual-webapp/pull/4/commits/7a738ae4ab3bb1bfa6b0286309e5905881cabc2b
- https://redis.uptrace.dev/

