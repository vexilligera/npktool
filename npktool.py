import os
import sys
import shutil
import struct
import marshal

def search_bytes(src, dat):
	t = len(src) - len(dat) + 1
	for i in range(t):
		ret = True
		for j in range(len(dat)):
			if src[i + j] != dat[j]:
				ret = False
				break
		if ret:
			return i
	return -1

def i2bytes(integer):
	l = []
	_ = integer
	for i in range(4):
		l.append(_ & 0xFF)
		_ = _ >> 8
	return bytes(bytearray(l))

if len(sys.argv) == 1:
	print('usage:')
	print('python npktool.py d filename.apk - unpack the apk file.')
	print('python npktool.py c file.py 00ABCDEF - compile file.py and insert it at offset 00ABCDEF in script.npk and build the APK.')
	print('python npktool.py b path file.apk - build the APK file and sign.')
	sys.exit()
option = sys.argv[1]

if option == 'd':
	filename = ''.join(list(sys.argv[2])[:-4])
	if not os.path.exists(filename):
		os.system('apktool d ' + sys.argv[2])
	else:
		print('APK already disassembled.')
	shutil.copyfile(filename + '/assets/script.npk', 'original_script.npk')
elif option == 'c':
	filename = sys.argv[2]
	offset, = struct.unpack('>L', bytearray.fromhex(sys.argv[3]))
	offset_dat = i2bytes(offset)

	name = ''.join(list(filename)[:-3])
	os.system('python -m py_compile ' + filename)
	os.system('python pyc_encryptor.py ' + name + '.pyc ' + name + '.pycfix')
	os.system('python encode.py ' + name + '.pycfix ' + name + '.pyn')
	
	bin_size = os.path.getsize(name + '.pyn')
	new_bin = open(name + '.pyn', 'rb')
	original_script = open('original_script.npk', 'rb')
	original_script.seek(0x14)
	table_addr, = struct.unpack('<L', bytes(original_script.read(4)))
	original_script.seek(table_addr)
	offset_table = original_script.read()
	index_in_table = search_bytes(offset_table, offset_dat)
	size_addr = []
	size_addr.append(index_in_table + table_addr + 4)
	size_addr.append(size_addr[0] + 4)
	original_script.seek(size_addr[0])
	old_size = original_script.read(4)
	old_size, = struct.unpack('<L', old_size)
	print ('original size: ' + repr(old_size))
	print ('new size: ' + repr(bin_size))
	original_script.seek(0)
	new_script_body = original_script.read(offset)
	new_script_body = new_script_body + new_bin.read()
	original_script.seek(offset + bin_size)
	new_script_body = new_script_body + original_script.read(table_addr - offset - bin_size)

	new_bin_size_dat = i2bytes(bin_size)
	original_script.seek(table_addr)
	new_table = original_script.read(size_addr[0] - table_addr)
	new_table = new_table + new_bin_size_dat
	new_table = new_table + new_bin_size_dat
	original_script.seek(size_addr[1] + 4)
	new_table = new_table + original_script.read()

	new_script_dat = new_script_body + new_table
	new_bin.close()
	original_script.close()
	new_script_file = open('new_script.npk', 'wb')
	new_script_file.write(new_script_dat)
	new_script_file.close()
elif option == 'b':
	path = sys.argv[2]
	shutil.copyfile('new_script.npk', path + '/assets/script.npk')
	os.system('apktool b ' + path)
	os.system('java -jar signapk.jar testkey.x509.pem testkey.pk8 ' + path + '/dist/' + path + '.apk ' + sys.argv[3])