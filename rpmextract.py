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


    def parse(self):
        self.archive.seek(0)
        self.parse_lead()


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
