1、libvirt_server使用说明：
	安装python所需要的libvirt库：
	wget https://libvirt.org/sources/python/libvirt-python-1.3.1.tar.gz
	tar zxvf libvirt-python-1.3.1.tar.gz && cd libvirt-python-1.3.1/
	python setup.py build && python setup.py install

2、运行setup.sh安装必要的库

3、必要步骤：
	需要将monitor目录放到和libvmi、volatility相同目录下
	因为需要用到libvmi（采集win）和volatility（采集linux）

4、具体详细的说明，见各个文件夹下的README


