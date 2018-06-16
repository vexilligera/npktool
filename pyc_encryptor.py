import os  
import zlib  
import rotor  
import marshal  
import binascii  
import argparse  
import pymarshal  
class PYCEncryptor(object):  
    def __init__(self):
        self.opcode_encrypt_map = {
            38: 1, 46: 2, 37: 3, 66: 4, 12: 5, 35: 10, 67: 11, 81: 12, 32: 13,
            9: 15, 63: 19, 70: 20, 44: 21, 36: 22, 39: 23, 57: 24, 10: 25,
            52: 26, 49: 28, 86: 30, 87: 31, 88: 32, 89: 33, 24: 40, 25: 41,
            26: 42, 27: 43, 14: 50, 15: 51, 16: 52, 17: 53, 8: 54, 21: 55,
            55: 56, 82: 57, 34: 58, 22: 59, 65: 60, 6: 61, 58: 62, 71: 63,
            43: 64, 30: 65, 19: 66, 5: 67, 60: 68, 53: 71, 42: 72, 3: 73,
            48: 74, 84: 75, 77: 76, 78: 77, 85: 78, 47: 79, 51: 80, 54: 81,
            50: 82, 83: 83, 74: 84, 64: 85, 31: 86, 72: 87, 45: 88, 33: 89,
            145: 90, 159: 91, 125: 92, 149: 93, 157: 94, 132: 95, 95: 96, 113: 97,
            111: 98, 138: 99, 153: 100, 101: 101, 135: 102, 90: 103, 99: 104, 151: 105,
            96: 106, 114: 107, 134: 108, 116: 109, 156: 110, 105: 111, 130: 112, 137: 113,
            148: 114, 172: 115, 155: 116, 103: 119, 158: 120, 128: 121, 110: 122, 97: 124,
            104: 125, 118: 126, 93: 130, 131: 131, 136: 132, 115: 133, 100: 134, 120: 135,
            129: 136, 102: 137, 140: 140, 141: 141, 142: 142, 94: 143, 109: 146, 123: 147
        }
        self.opcode_decrypt_map = {self.opcode_encrypt_map[key]: key for key in self.opcode_encrypt_map}
    def _decrypt_file(self, filename):
        os.path.splitext(filename)
        file = open(filename)
        file.seek(8)
        content = file.read()
        try:
            m = pymarshal.loads(content)
        except:
            try:
                m = marshal.loads(content)
            except Exception as e:
                print("[!] error: %s" % str(e))
                return None
        return m.co_filename.replace('\\', '/'), pymarshal.dumps(m, self.opcode_decrypt_map)
    def decrypt_file(self, input_file, output_file=None):
        result = self._decrypt_file(input_file)
        if not result:
            return
        pyc_filename, pyc_content = result
        if not output_file:
            output_file = os.path.basename(pyc_filename) + '.pyc'
        with open(output_file, 'wb') as fd:
            fd.write(pyc_content)
def main():  
    parser = argparse.ArgumentParser(description='onmyoji py decrypt tool')
    parser.add_argument("INPUT_NAME", help='input file')
    parser.add_argument("OUTPUT_NAME", help='output file')
    args = parser.parse_args()
    encryptor = PYCEncryptor()
    encryptor.decrypt_file(args.INPUT_NAME, args.OUTPUT_NAME)
if __name__ == '__main__':  
    main()