## SSHの設定 (client)

ISUCON 用に VSCode を使ってリモートに接続しつつ、github 認証のための秘密鍵もついでに持っていく設定。  
[予めサーバーサイドで、作業ユーザで直接ssh接続できるように設定しておく必要がある。](./ssh-server-setting.md)  
 (デフォルトの接続userからsuして作業ユーザに変えると、ssh-agentが鍵を持っていってくれなくなるため)

1. (WSL のみ) `~/.bashrc` 末尾に以下を追加 (VS Code でも ssh-agent が使えるように追加)
```
eval `ssh-agent`
ssh-add ~/.ssh/id_rsa
```
今回は、ssh-add の引数として、 **github に登録した鍵に対応する秘密鍵**を指定する。

2. 設定ファイルを編集  
例:
```
Host isucon10-01
    HostName 153.120.166.47
    User isucon
    Port 22
    IdentityFile ~/.ssh/id_rsa
    ForwardAgent yes # 追加
```
こちらの IdentityFile には、**isucon10-01 サーバーにログインするのに必要な秘密鍵**を指定する。  
`1.` で指定したものと異なることがあるので注意。（ログイン鍵もgithub鍵も同一のものであれば同一のものを指定して良い）

3. 接続。VSCode の Remote SSH でも開けるはず
```
$ ssh isucon10-01
```

4. github 確認。 VSCode のターミナルでも動くはず
```
$ ssh -T git@github.com
Hi <github-username>! You've successfully authenticated, but GitHub does not provide shell access.
```

## 参考文献
- https://qiita.com/sshojiro/items/60982f06c1a0ba88c160
- https://qiita.com/murata-tomohide/items/43a343a3ad0157423f04
- https://qiita.com/yuki153/items/0ad5cb02faf3ecdcf903
