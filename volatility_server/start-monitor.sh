echo "" > ./log/monitor.log
cat /dev/null > nohup.out
(nohup python volatility_monitor_server.py &)
