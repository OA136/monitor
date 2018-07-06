# coding: utf-8
import os
import sys
import web
import time,datetime
import logging
import threading

from filesystem_monitor_settings import *
from Registry import Registry
from log import getlogger
from hash import *
import Queue

logger = getlogger("monitor")

web.config.debug = False

# 数据库连接
db = web.database(dbn=db_engine, host=db_server, db=db_database, 
                               user=db_username, pw=db_password)
# 全局变量存储虚拟机元数据
ret = db.select('cloud_vhost',what='uuid,name,allocation,windows,profile')
profiles = {}
for line in ret:
    profiles[line['uuid']] = (line['windows'], line['name'], line['profile'], line['allocation'])


files_list = []         # 暂存单个虚拟机的文件：             [fn1,fn2,...]
files_dict = {}         # 所有虚拟机的文件，键为虚拟机id：    {uuid：[fn1,fn2,...], ...}

registry_dict = {}      # 暂存单个虚拟机注册表：             {path: [(name,type,value), ..], ...}
registries_dict = {}    # 存储所有虚拟机注册表，键为虚拟机id：{uuid: {path:[(name,type,value), ..], ...}，...}

# 读取监控linux的文件列表
for (uuid,(win,name,profile,allocation)) in profiles.items():
    files_list = [] 
    ret = db.select('monitor_file_list',where="`uuid`='%s'" % uuid)
    for line in ret:
        files_list.append(line['filename'])
    files_dict[line['uuid']] = files_list



# 队列存放windows虚拟机某时刻的注册表文件名
q = Queue.Queue(maxsize = 5)

#挂载虚拟机文件到本地，并区分linux和windows作不同处理；
#win：都将注册表复制到registry文件夹，并以uid_time_SYSTEM命名
#linux：获取文件的内容
class file_mount(threading.Thread):
    def __init__(self, uuid, allocation, win, name):
        super(file_mount, self).__init__()
        self.daemon = True
        self.uuid = uuid
        self.allocation = allocation
        self.win = win
        self.name = name

    def run(self):
        global files_dict
        global q
        cmd = 'qemu-nbd -c /dev/%s /var/lib/libvirt/images/%s.img' % (self.allocation,self.name)
        os.popen(cmd)
        #将虚拟机文件挂载到本地
        if self.win == 0:
            try:
                cmd = 'mount /dev/%sp1 /tmp/%s' % (self.allocation, self.uuid)
                os.popen(cmd)
	        monitor_file_list = files_dict[self.uuid]
                for monitor_file in monitor_file_list:
		    if (os.access('/tmp/%s%s' % (self.uuid, monitor_file), os.R_OK)):
                        cmd = 'cat /tmp/%s%s' % (self.uuid, monitor_file)
                        try:
                            res = os.popen(cmd).read()
   		            #比较文件内容是否变化
                            file_mount_change(self.uuid, monitor_file, res)
                            logger.debug(cmd+' '+res)
                        except:
                            continue
	    except:
		logger.debug("mount linux error!")
        else:
	    try:
                cmd = 'mount /dev/%sp2 /tmp/%s' % (self.allocation, self.uuid)
                os.popen(cmd)

                # 注册表打印
                if q.qsize() < 5 and self.win == 1:
                    ctime = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime())
                    registrypath = '%s_%s_SYSTEM' % (self.uuid, ctime)
                    try:
		        cmd_cp = 'cp /tmp/%s/Windows/System32/config/SYSTEM registry/' % (self.uuid)
                        os.popen(cmd_cp)
                        cmd_mv = 'mv registry/SYSTEM registry/%s' % (registrypath)
                        os.popen(cmd_mv)

                        #放入队列，registry线程取出
                        q.put(registrypath)
                        logger.debug(registrypath)
		    except:
                        logger.debug(cmd_cp + "== or ==" + cmd_mv + "is error")
	    except:
                logger.debug("mount windows error!")
        cmd = 'umount /tmp/%s' % (self.uuid)
        os.popen(cmd)
        cmd = 'qemu-nbd -d /dev/%s' % (self.allocation)
        os.popen(cmd)

#比较注册表变化，从队列q中取出注册表名：uid_time_SYSTEM
class registry(threading.Thread):
    def __init__(self):
        super(registry, self).__init__()
        self.daemon = True

    def run(self):
        global q
        global registry_dict
        global registries_dict
        table = 'registry_list'
        if q.empty():
            time.sleep(2)
        else:
            registry_name = q.get()
            uuid = registry_name.split('_')[0]
            ctime = registry_name.split('_')[1]
            registry = registry_name.split('_')[2]
            md5_new = GetFileMd5('registry/%s' % registry_name)

            ret = db.select(table, where="`uuid`='%s' and `registry`='%s'" % (uuid, registry))
            #没有此虚拟机的注册表记录，直接存入
            if len(ret) == 0:
                registry_dict = {}
                #
                registry_analyze('registry/%s' % registry_name)
                db.insert(table,uuid = uuid,
                        registry= registry,
                        time = ctime,
                        md5 = md5_new
                        )
                registries_dict[uuid] = registry_dict
            #有则比较MD5值是否变化
            else:
                registry_dict = {}
                md5_old = list(ret)[0]['md5']
                if md5_old != md5_new:
                    #先获取当前的注册表信息，存入字典registry_dict
                    registry_analyze('registry/%s' % registry_name)
                    #再与之前的注册表registries_dict[uuid]信息比较
		    try:
                    	compare(uuid, registry, registry_dict, registries_dict[uuid])
		    except:
			logger.debug('compare is error!')
                    # 更新数据库hash值
                    db.update(table,where="`uuid`='%s' and `registry`='%s'" % (uuid, registry),
                        md5 = md5_new,
                        time = ctime
                        )


                    registries_dict[uuid] = registry_dict
            
            cmd = 'rm registry/%s' % (registry_name)
            os.popen(cmd)
            logger.debug('rm success')


#获取注册表内容
def registry_analyze(filename):
    if not os.path.isfile(filename):
        return
    reg = Registry.Registry(filename)
    rec(reg.root())

#递归获取注册表树型结构，并将其以字典键值对的方式存储:{path:[(name,type,value), ..], ...}
def rec(key):
    global registry_dict
    element_list = []
    if key.values() == []:
      registry_dict[key.path()] = []
    for element in key.values():
        element_tuple = (element.name(), element.value_type_str(), element.value())
        element_list.append(element_tuple)
    registry_dict[key.path()] = element_list
    for subkey in key.subkeys():
        rec(subkey)

#比较注册表变化，并将变化写入数据库
def compare(uuid, registry, old_dict, new_dict):
    table = 'registry_change'
    for k,v in new_dict.items():
      if k in old_dict:
        if v != old_dict[k]:
            for element_tuple in v:
                if element_tuple not in old_dict[k]:
                    name = element_tuple[0]
                    value_type = element_tuple[1]
                    ctime = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime())
                    db.insert(table,uuid = uuid,
                            registry = registry,
                            path = k,
                            key_name = name,
                            key_type = value_type,
                            time = ctime,
                            )

#通过计算MD5值比较文件内容是否变化，monitor_file为文件名，res为文件现在的内容
def file_mount_change(uuid, monitor_file, res):
    logger.debug("file_mount_change start!")
    table = 'monitor_file_change'
    ret = db.select(table, where="`uuid`='%s' and `filename`='%s' order by time desc" % (uuid, monitor_file))

    size = len(res)
    md5_new = GetMd5(res)
    ctime = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime())

    filepath = monitor_file.split('/')[-1]
    filepath = 'files/%s_%s_%s' % (uuid, ctime, filepath)
    #之前没记录，直接存入数据库
    if len(ret) == 0:
        db.insert(table, uuid = uuid,
                        filename = monitor_file,
                        size = size,
                        md5 = md5_new,
                        time = ctime)

        file_object = open(filepath, 'w')
        file_object.write(res)
        file_object.close( )
    	logger.debug('no record:\tsize:'+size+'filepath:'+filepath+'\tres:'+res)
    #否则，比较md5值，不同则存入数据库
    else:
        md5_old = list(ret)[0]['md5']
        if md5_old != md5_new:
            db.insert(table, uuid = uuid,
                            filename = monitor_file,
                            size = size,
                            md5 = md5_new,
                            time = ctime)

            file_object = open(filepath, 'w')
            file_object.write(res)
            file_object.close( )
	#logger.debug('update:'+list(ret)[0]['time']+'\tsize:'+size+'filepath:'+filepath+'\tres:'+res)
    logger.debug(ctime + ' ' + uuid+ ' ' + filepath + ' '+res)

#启动file_mount线程
class mount_thread(threading.Thread):
    def __init__(self, uuid, allocation, win, name):
        super(mount_thread, self).__init__()
        self.daemon = True
        self.uuid = uuid
        self.allocation = allocation
        self.win = win
        self.name = name
        
    def run(self):
        while True:
            t = file_mount(self.uuid, self.allocation, self.win, self.name)
            t.setDaemon(True)
            t.start()
            t.join()
            time.sleep(5)

#启动registry线程
class registry_thread(threading.Thread):
    def __init__(self):
        super(registry_thread, self).__init__()
        self.daemon = True
        
    def run(self):
        while True:
            t = registry()
            t.setDaemon(True)
            t.start()
            t.join()
            time.sleep(5)


def main():
    logger.debug("============[OK] server start up!=============")
    # 加载nbd模块
    cmd = 'modprobe nbd max_part=16'
    os.popen(cmd)
    while True:
        threads = []
        for (uuid,(win,name,profile,allocation)) in profiles.items():
            # 创建挂载目录
            mount_dir = '/tmp/%s' % (uuid)
            if not os.path.exists(mount_dir):
                cmd = 'mkdir /tmp/%s' % (uuid)
                os.popen(cmd)
            t = mount_thread(uuid, allocation, win, name)
            threads.append(t)
            if win == 1:
                t = registry_thread()
                threads.append(t)

        for t in threads:
            t.setDaemon(True)
            t.start()

        for t in threads:
            t.join()


if __name__ == '__main__':
    main()
