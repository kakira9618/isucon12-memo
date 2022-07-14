## docker-commands

### ISUCONで使うやつ
- docker ps
  - dockerコンテナの情報一覧
- docker exec -it <container-id> <command>
  - コンテナに入る
- docker logs <container-id>
  - 各コンテナのログを見る
- docker-compose logs
  - すべてのコンテナのログを見る

### チートシート
https://qiita.com/nimusukeroku/items/72bc48a8569a954c7aa2
https://qiita.com/wMETAw/items/34ba5c980e2a38e548db (ちょっと古いので注意)


### FAQ
- `ERROR: Couldn't connect to Docker daemon at http+docker://localhost - is it running?` と出る
  - sudo つけよう

