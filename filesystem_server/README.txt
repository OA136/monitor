# filesystem_server




主要通过qemu-ndb将虚拟机的文件系统挂在到本地目录下，从而进行信息采集监控：
	vm-windows：主要监控注册表的变化，将变化存入到数据库表registry_change中
	vm-ubuntu:  根据表monitor_file_list中定义的文件，对其进行监控，并将变化的记录存入到表monitor_file_change中
文件：
	filesystem_monitor_settings.py：数据库等配置信息
	filesystem_monitor_server.py：  核心代码
	hash.py：						计算一个字符串或者一个文件的MD5值
	log.py：						日志格式化代码
	start-monitor.sh:				开始监控
	stop-monitor.sh:				结束监控
文件夹：
	registry：暂存windows的注册表
	files：	  暂存ubuntu的文件
	log：	  存日志

mount_thread()-->file_count()-->file_mount_change()
					|
					|
				q.put(registrypath)

q.get(registrypath)
	|
	|
registry()-->registry_analyze()-->rec()
		\
		 \
		 compare()

	
==============================命令说明===================================================
#1、加载ndb驱动
	modprobe nbd max_part=16
#2、查看信息
	modinfo nbd
#3、连接qemu-ndb
		qemu-nbd -c /dev/nbd0 /var/lib/libvirt/images/master.img
	##查看
		fdisk -l /dev/nbd0
		##linux逻辑分区挂载
			##查看逻辑组
				lvdisplay
			##激活vg0
				vgchange -ay vg0
			##挂载
				挂载vg0的逻辑分区lg1
					mount /dev/vg0/lg1 /mnt/master/lg1
	#linux挂载：
		mount /dev/nbd0p1 /mnt/master
	#umount 关闭连接：
		umount /dev/nbd0p1
		qemu-nbd -d /dev/nbd0p1
	
	#windows挂载：
		qemu-nbd -c /dev/nbd1 /var/lib/libvirt/images/win.img
		mount /dev/nbd1p2 /mnt/win
	#windows卸载：
		umount /mnt/win
		qemu-nbd -d /dev/nbd1
==============================qemu-ndb===================================================