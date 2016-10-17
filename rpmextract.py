#!/usr/bin/python3

import argparse


def main():
    settings = parse_arguments()


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
