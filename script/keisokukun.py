# python3 -m pip install -U "discord.py[voice]"
# sudo apt install -y inkscape dstat
# go get github.com/uber/go-torch
# git clone https://github.com/brendangregg/FlameGraph
# https://qiita.com/1ntegrale9/items/cb285053f2fa5d0cccdf
import discord
import asyncio
import subprocess
import os
import time
import datetime
from multiprocessing import Process

script_dir = os.getcwd()

client = discord.Client()

# Discord bot のアクセストークン。秘密だよ。
token = os.environ['DISCORD_BOT_TOKEN']

# 反応するチャンネル。インスタンスに沿ったものを指定してね
channel_name = "bot-01"

# ホームディレクトリのパス。最後に/は入れないこと
home = "/home/isucon"

# nginxのアクセスログと、mysqlのスローログのパス
# ベンチを実行すると内容が削除されるので注意。（ベンチ後にscript/logsディレクトリに格納されます）
nginx_access_logfile = "/var/log/nginx/access.log"
mysql_slow_logfile = "/var/log/mysql/slow.log"

# ベンチ実行前に内容削除を行うシステムログのパスの配列
system_logfiles = [nginx_access_logfile, mysql_slow_logfile]

# ベンチマーカー実行ファイルのあるディレクトリのパス。ここに cd してから下のベンチマーカーのコマンドを実行するよ。
bench_dir = "/bin/"

# ベンチマーカー本体の実行コマンド
bench_command = "echo test"

# この文字列がベンチマーカーから出力されると、プロファイルを開始します
#bench_pprof_triger_string = "=== validation ==="

# プロファイルを開始する、となってから待つ時間
bench_pprof_before_sleep_time = 15

# プロファイル実行時間
bench_pprof_exec_time = 30

# プロファイルコマンド（アプリ）。go-torchはPATHにFlameGraphディレクトリへのパスが含まれている必要があるため、指定している。
profile_command = "PATH=$PATH:" + home + "/FlameGraph go-torch --time " + str(bench_pprof_exec_time) + " --url https://isuports-2.t.isucon.dev/debug/pprof/profile"

# プロファイルコマンド（OS）。dstatを使用している。
dstat_command = "timeout " + str(bench_pprof_exec_time) + " dstat -tTcdn --top-cpu"

def clear_logfile(logfile_path):
    command = "sudo cp /dev/null " + logfile_path
    subprocess.run(command, shell=True)
    print("clear log file:", logfile_path)

def clear_logfiles():
    for logfile_path in system_logfiles:
        clear_logfile(logfile_path)

def get_log_dir_name():
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    return now.strftime('%Y%m%d%H%M%S')

def get_frame_graph():
    time.sleep(bench_pprof_before_sleep_time)
    subprocess.run(profile_command, shell=True)

def get_dstat(log_dir):
    time.sleep(bench_pprof_before_sleep_time)
    dstat_result = subprocess.run(dstat_command, shell=True, capture_output=True, text=True)
    dstat_path = get_dstat_path(log_dir)
    f = open(dstat_path, 'w', encoding='UTF-8')
    f.write(dstat_result.stdout)
    f.close()

def get_lines(cmd, log_dir):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=bench_dir)
    executed = False
    while True:
        line = proc.stdout.readline()
        if line:
            yield line
        if not line and proc.poll() is not None:
            break

def bench(log_dir, opts, do_bench):
    bench_logfile_path = log_dir + "/bench_log.txt"
    png = home + "/pprof/torch.png"
    svg = home + "/pprof/torch.svg"

    if do_bench:
        clear_logfiles()

        p = Process(target=get_frame_graph, args=())
        p.start()
        p2 = Process(target=get_dstat, args=(log_dir, ))
        p2.start()

        command = bench_dir + "/" + bench_command + " " + opts
        print("command:", command)

        f = open(bench_logfile_path, 'w', encoding='UTF-8')
        for line in get_lines(cmd=command, log_dir=log_dir):
            f.write(line)
        f.close()

        print("wait...")
        time.sleep(70) # 計測待ち
        print("wait completed.")

        subprocess.run("cp /home/isucon/script/torch.svg /home/isucon/pprof", shell=True)

        convert_command = "inkscape -z /home/isucon/script/torch.svg -w 1600 /home/isucon/script/torch.png"
        subprocess.run("cp /home/isucon/script/torch.png /home/isucon/pprof", shell=True)

        subprocess.run(convert_command, shell=True)
        subprocess.run("cp " + png + " " + log_dir, shell=True)
        subprocess.run("cp " + svg + " " + log_dir, shell=True)

    return (bench_logfile_path, png, svg)

def alp(log_dir, opts="--sort=count -r"):
    now = get_log_dir_name()
    alp_result_path = log_dir + "/alp_" + now + ".txt"
    alp_result = subprocess.run("sudo cat " + nginx_access_logfile + " | alp ltsv --limit 100000 " + opts, shell=True, capture_output=True, text=True)
    subprocess.run("sudo cp " + nginx_access_logfile + " " + log_dir, shell=True)
    f = open(alp_result_path, 'w', encoding='UTF-8')
    f.write(alp_result.stdout)
    f.close()
    return alp_result_path

def pt_query_digest(log_dir):
    pt_query_digest_result_path = log_dir + "/pt-query-digest.txt"
    pt_query_digest_result = subprocess.run("sudo cat " + mysql_slow_logfile + " | pt-query-digest", shell=True, capture_output=True, text=True)
    
    subprocess.run("sudo cp " + mysql_slow_logfile + " " + log_dir, shell=True)
    f = open(pt_query_digest_result_path, 'w', encoding='UTF-8')
    f.write(pt_query_digest_result.stdout)
    f.close()
    return pt_query_digest_result_path

def exec_command(cur_dir, command):
    (log_id, log_dir) = init_log_dir()
    result_path = log_dir + "/command_result_" + log_id + ".txt"
    result = subprocess.run(command, cwd=cur_dir, shell=True, capture_output=True, text=True, timeout=10)
    f = open(result_path, 'w', encoding='UTF-8')
    f.write("[" + cur_dir + "]$ " + command + "\n")
    f.write(result.stdout)
    f.close()
    return (result_path, log_id)

def get_log_dir_path(log_id):
    return script_dir + "/logs/" + log_id

def get_dstat_path(log_dir):
    return log_dir + "/dstat.txt"

def init_log_dir():
    log_id = get_log_dir_name()
    log_dir = get_log_dir_path(log_id)
    os.makedirs(log_dir)
    print("log_id:", log_id)
    print("log_dir:", log_dir)
    return (log_id, log_dir)

async def show_logs(message, log_id, log_dir, opts):
    (bench_logfile_path, png, svg) = bench(log_dir, opts, False)

    if os.path.exists(bench_logfile_path):
        await message.channel.send("ログID: " + log_id, file=discord.File(bench_logfile_path))

    if os.path.exists(png):
        await message.channel.send("pprof(png):", file=discord.File(png))

    if os.path.exists(svg):
        await message.channel.send("pprof(svg):", file=discord.File(svg))

    dstat_path = get_dstat_path(log_dir)
    if os.path.exists(dstat_path):
        await message.channel.send("dstat:", file=discord.File(dstat_path))

    alp_result_path = alp(log_dir)
    if os.path.exists(alp_result_path):
        await message.channel.send("alp:", file=discord.File(alp_result_path))

    pt_query_digest_result_path = pt_query_digest(log_dir)
    if os.path.exists(pt_query_digest_result_path):
        await message.channel.send("pt-query-digest:", file=discord.File(pt_query_digest_result_path))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.name != channel_name:
        return

    if message.content.startswith("help"):
        m = """**ベンチマークを実行する**
```
bench [opts]
``````
bench --workload 10
```
実計測する。optsはベンチマーカーのオプションとして付加される。
ベンチマークを実行中に、プロファイリングを行い、結果を保存する。
ログIDと、ベンチマーカーの出力と、プロファイル結果と、アクセスログやスロークエリの解析結果をDiscordに投稿する。


**ログを見る**
```
show_logs ログID
``````
show_logs 20220723073158
```
出力はbenchと同じだが、ベンチマークは実行しないで、ログIDものを解析対象とする


**オプションを変えてalpを実行する**
```
alp ログID alpのオプション
``````
alp 20220723005047 --filters "Uri matches '^/api/estate'" --sort=count -r
```
ログIDを指定して、alpのオプションを変えて実行した場合の結果を投稿する


**任意のコマンドを実行する**
```
exec 絶対パスのカレントディレクトリ 実行するコマンド
``````
exec /home/isucon ./script/test.sh
```
絶対パスカレントディレクトリ にcdしてから、 実行するコマンド を実行する
ログIDが新しく発行され、結果はログに保存される。
コマンドの時間制限は10秒。それ以上かかると強制終了する。
The Remote Code Execution!
"""
        await message.channel.send(m)
        
    if message.content.startswith("はろー"):
        m = "こんにちは、" + message.author.name + "さん"
        await message.channel.send(m)

    if message.content.startswith("bench"):
        opts = message.content[5:]

        (log_id, log_dir) = init_log_dir()
        await message.channel.send("15秒後から計測を開始するよ！ すぐにベンチを走らせてね")

        bench(log_dir, opts, True)

        await show_logs(message, log_id, log_dir, opts)
        await message.channel.send("ベンチ & 計測終わり！")

    if message.content.startswith("show_logs"):
        log_id = message.content[10:]
        if (log_id == ""):
            await message.channel.send("ログID(数字)を指定してね。`show_logs log_ID`")
            return

        log_dir = get_log_dir_path(log_id)
        await message.channel.send("ログ解析を開始するよ！")
        await show_logs(message, log_id, log_dir, "")
        await message.channel.send("ログ解析終わり！")

    if message.content.startswith("alp"):
        sp = message.content.split()
        (log_id, opts) = (sp[1], " ".join(sp[2:]))
        print(opts)
        if (log_id == ""):
            await message.channel.send("ログID(数字)を指定してね。`show_logs log_ID`")
            return

        log_dir = get_log_dir_path(log_id)

        alp_result_path = alp(log_dir, opts)
        if os.path.exists(alp_result_path):
            await message.channel.send("alp:", file=discord.File(alp_result_path))

    if message.content.startswith("exec"):
        sp = message.content.split()
        (cur_dir, command) = (sp[1], " ".join(sp[2:]))
        if (cur_dir == "" or command == ""):
            await message.channel.send("`exec カレントディレクトリ(絶対パス) 実行コマンド`")
        
        (result_path, log_id) = exec_command(cur_dir, command)
        if os.path.exists(result_path):
            await message.channel.send("exec result (ログID:" + log_id + "):", file=discord.File(result_path))

client.run(token)
