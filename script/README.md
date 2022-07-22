## 計測くん

### 設定

1. 必要なモジュールのインストール
```
$ cp -r script ~/
$ cd ~
$ python3 -m pip install -U "discord.py[voice]"
$ sudo apt install -y inkscape dstat
$ go get github.com/uber/go-torch
$ git clone https://github.com/brendangregg/FlameGraph
```

2. 設定
keisokukun.py の上部設定箇所をコメントに従って適切に設定してください。

### 使い方
```
$ vim ~/.bashrc
export DISCORD_BOT_TOKEN="token"
```
```
$ source ~/.bashrc
```
```
$ cd ~/script
$ python3 keisokukun.py
```

以下、Discord上でのコマンド

### ベンチマークを実行する
```
bench [opts]
```

ベンチマークを実行する。optsはベンチマーカーのオプションとして付加される。  
ベンチマークを実行中に、プロファイリングを行い、結果を保存する。  
ログIDと、ベンチマーカーの出力と、プロファイル結果と、アクセスログやスロークエリの解析結果をDiscordに投稿する。

### ログを見る
```
show_logs ログID
```
出力はbenchと同じだが、ベンチマークは実行しないで、ログIDものを解析対象とする

### オプションを変えてalpを実行する
```
alp ログID alpのオプション
```
ログIDを指定して、alpのオプションを変えて実行した場合の結果を投稿する

### 任意のコマンドを実行する
```
exec 絶対パスのカレントディレクトリ 実行するコマンド
```
`絶対パスカレントディレクトリ` にcdしてから、 `実行するコマンド` を実行する。  
ログIDが新しく発行され、結果はログに保存される。  
The Remote Code Execution!

