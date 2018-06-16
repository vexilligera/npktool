import rotor
import marshal
import zlib
from sys import argv

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

def decrypt(data):
    rot = init_rotor()
    #print 'original data:'
    #print repr(data)
    data = rot.decrypt(data)
    #print 'rot decrypt data:'
    #print repr(data)
    data = zlib.decompress(data)
    #print 'zlib decompressed data:'
    #print repr(data)
    data = _reverse_string(data)
    #print '_reverse string data:'
    #print repr(data)
    data = marshal.loads(data)
    #print 'marshaled data:'
    #print repr(data)
    return data