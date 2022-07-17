## SSHの設定
1. 設定ファイルを編集  
設定例
```
Host isucon10-01
  HostName 153.120.166.47
  User isucon
  Port 22
  IdentityFile ~/.ssh/id_rsa
  ForwardAgent yes # 追加
```

2. 秘密鍵をエージェントに登録  
```
//windows の場合
$ eval `ssh-agent`
$ ssh-add -k ~/.ssh/id_rsa
```


## 参考文献
- https://qiita.com/sshojiro/items/60982f06c1a0ba88c160
