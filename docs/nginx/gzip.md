## nginxのgzip有効化

ベンチマーカーが静的ファイルも受け取る場合、これらの設定を入れると通信量が下がり、CPU使用率が上がる

https://qiita.com/RyoMa_0923/items/55078f6fb57e9d70a37f

```
gzip on;
gzip_types text/css application/javascript application/json application/font-woff application/font-tff image/gif image/png image/jpeg application/octet-stream;
```

### 参考文献
- https://qiita.com/RyoMa_0923/items/55078f6fb57e9d70a37f
- https://github.com/kakira9618/isucon10-qual-webapp/pull/8
