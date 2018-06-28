import os

cmd = 'virsh dommemstat win1'
res = os.popen(cmd).read()
res=res.split('\n')
unused = 0
available = 0
for item in res:
	item = item.split(' ')
	print item
	if item[0] == 'unused':
		unused = float(item[1])
	if item[0] == 'available':
		available = float(item[1])
print unused,available
print (available-unused)/available
