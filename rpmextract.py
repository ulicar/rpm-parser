#!/usr/bin/python3
# -*- coding: utf8 -*-

import argparse
import copy
import gzip
import io
import struct
import sys


def c2i(char):
    return struct.unpack('>b', char)[0]

def s2i(short):
    return struct.unpack('>h', short)[0]

def i2i(unsigned_int):
    return struct.unpack('>I', unsigned_int)[0]

def str_from_bytes(bytes, count):
    strings = bytes.split(b'\x00')

    return strings[0:count]


class RPM(object):
    MAGIC = b'\xed\xab\xee\xdb'
    HEADER = b'\x8e\xad\xe8'
    LEAD_SIZE = 96

    def __init__(self, archive):
        self.archive = archive
        self.__version = None                       # 4
        self.__type = {                             # 2
                b'\x00\x00': 'Binary',
                b'\x00\x01': 'Source'
        }
        self.__arhitecture = {                      # 2
                b'\x00\x01': 'i386',
                b'\x00\x02': 'Alpha',
                b'\x00\x03': 'Sparc',
                b'\x00\x04': 'MIPS',
                b'\x00\x05': 'PowerPC',
                b'\x00\x06': '68000',
                b'\x00\x07': 'SGI'
        }
        self.__package_name = None                  # 66
        self.__operating_system = {                 # 2
                b'\x00\x01': 'Linux'
        }
        self.__signature = None                     # 2
        self.__header_version = None                # 1
        self.__reserved = None                      # 4
        self.__index_entries_count = None           # 4
        self.__signature_size = None                # 4
        self.__index = {
                'tag': None,                        # 4
                'type': None,                       # 4
                'offset': None,                     # 4
                'count': None                       # 4
        }
        self.__index_type = {
                0: ('NULL',         0, ()),
                1: ('CHAR',         1, lambda d: c2i(d[0:1])),
                2: ('INT8',         1, lambda d: c2i(d[0:1])),
                3: ('INT16',        2, lambda d: s2i(d[0:2])),
                4: ('INT32',        4, lambda d: i2i(d[0:4])), 
                5: ('INT64',        0, ()),
                6: ('STRING',       0, lambda d: d.hex()),
                7: ('BIN',          1, lambda d: d.hex()),
                8: ('STRING_ARRAY', 0, ()),
                9: ('I18STRING',    0, ())
        }
        self.__signature_type = {
                  62: 'TAG_HEADERSIGNATURES',
                  63: 'TAG_HEADERIMMUTABLE',
                  64: 'TAG_HEADER18NTABLE',
                 267: 'SIGTAG_DSA',
                 268: 'SIGTAG_RSA',
                 269: 'SIGTAG_SHA1',
                1000: 'SIGTAG_SIZE',
                1002: 'SIGTAG_PGP',
                1004: 'SIGTAG_MD5',
                1005: 'SIGTAG_GPG',
                1007: 'SIGTAG_PAYLOADSIZE',
                1010: 'SIGTAG_SHA1HEADER',
                1011: 'SIGTAG_DSAHEADER',
                1012: 'SIGTAG_RSAHEADER'
        }

        self.__store = None                         # Unlimited


    def parse(self):
        self.archive.seek(0)
        self.parse_lead()

        self.archive.seek(RPM.LEAD_SIZE)
        self.parse_signature()

        self.archive.seek(self.signature_size())
        print (self.archive.tell())
        self.parse_header()


    def parse_lead(self):
        magic = self.archive.read(4)

        assert magic == RPM.MAGIC, 'File {f} is not a RPM self.archive'.format(f=self.__archive)

        rpm_version = self.archive.read(2)
        self.__version = '{major}.{minor}'.format(major=c2i(rpm_version[0:1]), minor=c2i(rpm_version[1:2]))
        print (self.__version)

        self.__type = self.__type[self.archive.read(2)]
        print (self.__type)

        self.__arhitecture = self.__arhitecture[self.archive.read(2)]
        print (self.__arhitecture)

        self.__package_name = self.archive.read(66).decode('utf-8').strip('\0')
        print (self.__package_name)
         
        self.__operating_system = self.__operating_system[self.archive.read(2)]
        print (self.__operating_system)

        self.__signature = '{sig}'.format(sig=s2i(self.archive.read(2)))
        print (self.__signature)

        reserved = self.archive.read(16)

    def parse_header(self):
        header = self.archive.read(3)

        assert header == RPM.HEADER, 'Wrong header in RPM self.archive'

        self.__header_version = c2i(self.archive.read(1))
        print (self.__header_version)

        reserved = self.archive.read(4)

        self.__index_entries_count = i2i(self.archive.read(4))
        print (self.__index_entries_count)

        self.__header_size = i2i(self.archive.read(4))
        print (self.__header_size)

        self.__index_entries = []
        for _ in range(0, self.__index_entries_count):
            index = dict()
            index['tag'] = self.__signature_type[i2i(self.archive.read(4))]
            index['type'] = i2i(self.archive.read(4))
            index['offset'] = i2i(self.archive.read(4))
            index['count'] = i2i(self.archive.read(4))
            
            self.__index_entries.append(index)

        size = sum(index['count'] for index in self.__index_entries)
        self.__store_position = RPM.LEAD_SIZE + size 

        self.__index_entries.sort(key=lambda index: index['offset'])

        self.__store = {}
        for index in self.__index_entries:
            name, size, callback = self.__index_type[index['type']]

            self.archive.seek(self.__store_position + index['offset'])

            #print (self.__index_type[index['type']], index['count'], index['tag'])
            

            if index['type'] <= 5 or index['type'] == 7:
                data = self.archive.read(size * index['count'])
                
                self.__store[index['tag']] = callback(data)

                print (index['tag'], self.__store[index['tag']])

                continue

            elif index['type'] == 6 or index['type'] == 9:
                data = self.archive.read()
                strings = str_from_bytes(data, index['count'])

                converted = list(map(callback, strings))

                if index['count'] == 1:
                    converted = converted[0]

                self.__store[index['tag']] = converted

                print (index['tag'], self.__store[index['tag']])

                continue

    def parse_signature(self):
        signature = self.parse_header()

    def signature_size(self):
        start = self.__store_position + self.__header_size
        self.archive.seek(start)
        data = self.archive.read()

        return data.index(RPM.HEADER) + start


def main():
    settings = parse_arguments()

    with open(settings.rpm, 'rb') as archive:
        rpm = RPM(archive)
        rpm.parse()


def die(message):
    print (message, file=sys.stderr)
    exit(-1)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Extract files from RPM package')
    parser.add_argument(
        'rpm',
        metavar='RPM',
        help='RPM file'
    )

    return parser.parse_args()


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        import traceback
        traceback.print_exc()
        die(str(error))

    exit(0)
