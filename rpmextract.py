#!/usr/bin/python3

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

def main():
    settings = parse_arguments()


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
    except Exception as e:
        import traceback
        traceback.print_exc()
        print (str(e))

        exit(-1)

    exit(0)
