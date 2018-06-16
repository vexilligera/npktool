import struct
import os
import redirect
import marshal
import pyc_decryptor

print('Usage: unpack the apk file using npktool and execute this script. Scripts stored in decompile/python_file/pyc')

path = 'python_file'
if not os.path.exists(path):
    os.makedirs(path)
    os.makedirs(path + '/pyc')

file = open('original_script.npk', 'rb')
file_size = os.path.getsize('original_script.npk')
file.seek(0x14)
base, = struct.unpack('<L', bytes(file.read(4)))
encryptor = pyc_decryptor.PYCEncryptor()
while base < file_size:
	base += 0x4
	file.seek(base)
	py_addr, = struct.unpack('<L', bytes(file.read(4)))
	py_size_ptr = base + 0x8
	file.seek(py_size_ptr)
	py_size, = struct.unpack('<I', bytes(file.read(4)))
	file.seek(py_addr)
	
	py_encrypted = file.read(py_size)
	try:
		pyc_original = redirect.decrypt(py_encrypted)
	except:
		print 'File at 0x%x failed to decrypt.' % py_addr

	file_name = path + '/' + hex(py_addr)
	save_file = open(file_name, 'wb')
	marshal.dump(pyc_original, save_file)
	save_file.close()
	encryptor.decrypt_file(file_name, path + '/pyc/' + hex(py_addr) + '.pyc')
	base += 0x18

file.close()