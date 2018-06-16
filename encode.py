import rotor
import marshal
import zlib
import sys

def init_rotor():
    asdf_dn = 'j2h56ogodh3se'
    asdf_dt = '=dziaq.'
    asdf_df = '|os=5v7!"-234'
    asdf_tm = asdf_dn * 4 + (asdf_dt + asdf_dn + asdf_df) * 5 + '!' + '#' + asdf_dt * 7 + asdf_df * 2 + '*' + '&' + "'"
    rot = rotor.newrotor(asdf_tm)
    return rot

def _reverse_string(s):
    l = list(s)
    l = map(lambda x: chr(ord(x) ^ 154), l[0:128]) + l[128:]
    l.reverse()
    return ''.join(l)

def reverse_string(s):
	l = list(s)
	l.reverse()
	sub_l = l[0:128]
	sub_l = map(lambda x: chr(ord(x) ^ 154), l[0:128])
	l = sub_l + l[128:]
	return ''.join(l)

def encode(data):
	rot = init_rotor()
	#print 'original data:'
	#print repr(data)
	data = reverse_string(data)
	#print '_reverse string data:'
	#print repr(data)
	data = zlib.compress(data, 9)
	#print 'zlib compressed data:'
	#print repr(data)
	data = rot.encrypt(data)
	#print 'rot encrypt data:'
	#print repr(data)
	return data

file = open(sys.argv[1], 'rb')
save = open(sys.argv[2], 'wb')
data = file.read()
save.write(encode(data))
file.close()
save.close()