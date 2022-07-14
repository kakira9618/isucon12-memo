## mysql の初期化について
mysql は datadir (デフォルトでは `/var/lib/mysql/`) 内の `mysql` ディレクトリが無い場合、`/docker-entrypoint-initdb.d/` 内にある `.sql` ファイル及び `.sh` ファイルを名前の昇順に実行する。  
これを使ってスキーマの定義や初期データの埋め込みが可能。

docker や docker-compose などを使って mysql が管理されている場合、datadir がボリュームとしてマウントされていないかを確認しよう。
マウントされている場合、datadir の内容はコンテナ終了後も残るので、中にあるファイルすべてを削除（`sudo rm -rf ./<datadir>`）しない限り、コンテナを立ち上げ直しても、初期化スクリプト群は動かない（データもスキーマもそのままということになる）。

## 参考文献
- https://qiita.com/moaikids/items/f7c0db2c98425094ef10
- https://github.com/docker-library/mysql/blob/master/5.7/docker-entrypoint.sh
