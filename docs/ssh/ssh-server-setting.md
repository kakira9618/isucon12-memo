## SSHの設定 (server)

ssh の公開鍵認証でサーバーにログインできるようにするための設定。インスタンスごとに設定が必要。  
**注意点：接続確認できるまで、設定に用いたssh接続は切断しないこと。切断すると設定失敗時に面倒なことになる可能性が高い。**

### 設定の確認
ISUCONの場合はほとんど大丈夫だと思うが、念の為、設定値を確認しておく。ついでに `2.` で使う `authorized_keys` のパスも確認する

大丈夫な例：
```
$ cat /etc/ssh/sshd_config | grep Authentication
# Authentication:
#PubkeyAuthentication yes    # コメントアウトされているが、デフォルトで有効なので問題なし。noだったらyesにする
#HostbasedAuthentication no
# HostbasedAuthentication
PasswordAuthentication no    # パスワード認証はsshの設定中はyesにしておいたほうが良いかも。公開鍵設定後はnoにする
ChallengeResponseAuthentication no
#KerberosAuthentication no
#GSSAPIAuthentication no
# be allowed through the ChallengeResponseAuthentication and
# PasswordAuthentication.  Depending on your PAM configuration,
# PAM authentication via ChallengeResponseAuthentication may bypass
# PAM authentication, then enable this but set PasswordAuthentication
# and ChallengeResponseAuthentication to 'no'.
```

```
$ cat /etc/ssh/sshd_config | grep AuthorizedKeysFile
#AuthorizedKeysFile	.ssh/authorized_keys .ssh/authorized_keys2  # コメントアウトされているのでデフォルトのパス `~/.ssh/authorized_keys` となる
```

設定を変更したら、必ずsshdを再起動してください（再起動しないと設定が反映されません）
```
$ sudo systemctl restart sshd
```

### 公開鍵の登録
接続したいユーザのホームディレクトリ内の `.ssh/authorized_keys` (先程調べたパス) に、ssh ログインで使う公開鍵を登録する。  
複数登録したい場合は改行区切りで入力する。  
必ず一つの公開鍵が一行に対応するようにすること（途中で変な改行が入ることがよくあります）。
```
$ vim ~/.ssh/authorized_keys  # 先程調べたパス
```

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDJ+eR0wngEWeQlL4NaH0GPyy/Nn4vkrlWv92PURJm/xqUU6Hj6Cn5Gv10CcWlYOVPLpi0Hs+2jPd7u/i4kSv7weikSL4DH2E7fMsTVIG0i5G8JVHy40IPe04Ba1B97v4R0xowaTItnVGfEmT48KV1upOqRT1OKBn1FEHlQmhIFgZCXWUGphPhnl/tx7I0IGwjTDENj6afMobnZApzBrYjWl27OBBX8iIRnRa1hSHNGTjDcMjSIiiU81/qUpumgKOr78aBsqMaLkpFMJJA17CFguaoxGC4MLlWgFk8QOaNjzjXDdLT6wWEV92JE1u/7dQweFuCfPI3ikJxKE/SaY7FL+Wi1SC9uDG5t0Q+huJI6bK/e06aou5WMvxRH+p0bo9oQmAlfJCMml7CkL+pxqaUYhKpI362bdZwUqXiMLMCo5k6dwO1sziYEHEj5LssXd9F8AYvYBd5Cs9LlF1i3ftXdswnjIskDAvd444XsiJcH2Itykdb5preGKhxvsMH/1qs=
```

### パーミッションの確認
忘れがち。  
`~/.ssh` ディレクトリはパーミッション**700**に、`~/.ssh/authorized_keys` はパーミッション**600**にしないと接続できない。  
余分な権限がついてる場合が多いのでちゃんと厳密に設定しよう（新しいユーザーでログインできるように設定する場合は`~.ssh`ディレクトリを作るところから始まる場合があるので注意する）
```
$ ls -la ~/.ssh
total 16
drwx------  2 isucon isucon 4096  7月 18 07:23 .　　　　　　　　　 # パーミッションは700
drwxr-xr-x 18 isucon isucon 4096  7月 18 07:23 ..
-rw-------  1 isucon isucon 2366  7月 17 15:55 authorized_keys  # パーミッションは600
-rw-r--r--  1 isucon isucon  888  7月 17 16:46 known_hosts
```

### 接続確認
[クライアント側接続設定を行い](./ssh-client-setting.md)、sshで接続できればOK。  
接続に失敗した場合は、
```
$ ssh hogehoge -v
$ ssh hogehoge -vv
$ ssh hogehoge -vvv
```
とするとクライアント側の詳細情報が見れる。

サーバー側のログは、`/var/log/auth.log` (Ubuntu系) や `/var/log/secure` (CentOS系) を見る。
