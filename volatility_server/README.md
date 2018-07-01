# volatility_server
vm status monitor base on volatility



此采集系统主要采集虚拟机的进程信息，分别存入相应的数据库表中
	linux：
		ifconfig、arp表、pslist、lsmod
	windows：
		lsmod、plist

必要步骤：
	需要将安装编译好的libvmi拷贝到monitor目录下，即当前目录的父目录下
	将volatility考入到当前文件夹下
	因为需要用到libvmi（采集win）和volatility（采集linux）