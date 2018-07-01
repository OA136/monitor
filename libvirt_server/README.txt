# libvirt_monitor_server
vm status monitor base on libvirt

获取虚拟机的内存、CPU、网络传输信息
	
	cloud_monitor_server-result-in-row.py： 核心代码
	cloud_monitor_settings.py：				配置信息
	start-monitor.sh：						开始采集
	stop-monitor.sh：						结束采集

	#从宿主机获取虚拟机的信息并将其存入到cloud_vhost中
	class thread_read_host_list(threading.Thread) 

	#从数据库中获取宿主机IP，并将其放入队列queue_host_list中：host_dict: {host:[v1, v2, ...], ...}
	class thread_get_host_list_from_db(threading.Thread)

	#获取queue_host_list，并调用multi_host_libvirt_check
	class thread_do_check(threading.Thread)

	#获取queue_result，并存入数据库表cloud_result_in_row中
	class thread_update_db(threading.Thread)

	#获取虚拟机的mem、rx、cpu，并放入队列queue_result中：result： {uuid：{mem：40%，cpu：20%，rx：14567}，...}
	def multi_host_libvirt_check(host_dict)


需要配置宿主机ssh远程登录免密码
	对于客户机（即运行采集系统的主机）：
		a、在用户家目录下公私钥：ssh-keygen 文件在$HOME/.ssh/目录下
		b、将公钥传递到远程服务器：ssh-copy-id -i $HOME/.ssh/id_rsa.pub -p 22 user@host 
		c、输入密码即可添加成功，之后可以免密登录
	对于远程宿主机（虚拟机所在的主机）：
		需要重新配置ssh配置文件/etc/ssh/sshd_config，把配置文件中的
			"PermitRootLogin without-password" 修改为 "PermitRootLogin yes，
		去除	AuthorizedKeysFile     %h/.ssh/authorized_keys 这句的注释；
		之后重新启动ssh
			service ssh restart

#其他不足
	目前，在表cloud_vhost中还无法自动配置虚拟机的profile、 allocation（nbd0-15）、windows（win虚拟机为1，否则为0）
	等信息，暂时为手动写入需要另外的模块自动化写入数据库