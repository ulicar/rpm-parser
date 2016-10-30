#!/usr/bin/python3

import struct
import sys

DEBUG = False

__all__ = [
    'c2i', 's2i', 'i2i',
    'str_from_bytes',
    'read_string',
    'set_debug', 'log', 'die'
]

def c2i(char):
    return struct.unpack('>b', char)[0]

def s2i(short):
    return struct.unpack('>h', short)[0]

def i2i(unsigned_int):
    return struct.unpack('>I', unsigned_int)[0]

def str_from_bytes(bytes, count):
    strings = bytes.split(b'\x00')

    return strings[0:count]


def read_string(binary_stream):
    string = ''
    while True:
        c = binary_stream.read(1)
        c = c.decode('utf-8')

        if c == '\0':
            break

        string += c

    return string

def set_debug(debug):
    global DEBUG
    DEBUG = debug


def log(statement):
    if not DEBUG:
        return

    if isinstance(statement, list):
        print (*statement)
        return

    print (statement)


def die(message):
    print (message, file=sys.stderr)
    exit(-1)

