## コンテナに入りたい
### docker 単体
```
$ sudo docker ps
CONTAINER ID   IMAGE                       COMMAND                  CREATED          STATUS          PORTS                                                  NAMES
1e1ee481a121   docker-compose_nginx        "dockerize -timeout …"   48 seconds ago   Up 46 seconds   0.0.0.0:8080->80/tcp, :::8080->80/tcp                  docker-compose_nginx_1
b089e20992d7   docker-compose_api-server   "dockerize -timeout …"   48 seconds ago   Up 46 seconds   0.0.0.0:1323->1323/tcp, :::1323->1323/tcp              docker-compose_api-server_1
5b451fc26095   mysql:5.7                   "docker-entrypoint.s…"   49 seconds ago   Up 48 seconds   0.0.0.0:3306->3306/tcp, :::3306->3306/tcp, 33060/tcp   docker-compose_mysql_1
```

```
$ sudo docker container exec -it 1e1e bash
root@1e1ee481a121:/#
```

### docker-compose
1. 入りたいコンテナに対応する service 名を確認（docker-compose.yml や go.yaml など）
2. yaml があるディレクトリで `sudo docker-compose exec <service> bash`
  a. docker-compose.yml ではない場合は、 `sudo docker-compose -f go.yaml exec <service> bash` とする


### 参考文献
https://qiita.com/Keitaroooo/items/a30bf4eb9310d7b3f7cd
