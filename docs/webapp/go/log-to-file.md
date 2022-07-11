## ログを標準出力ではなくファイルに移したい
echo を使っている場合、ファイルを開き、log.SetOutput(file)をすれば良い。
また、middlewareを使ってリクエストのログを表示している場合は、
e.Use(middleware.Logger()) の代わりに、e.Use(middleware.LoggerWithConfig(middleware.LoggerConfig{ Output: file })) とすれば良い

https://github.com/kysnm/echo_log_practice/blob/master/main.go


