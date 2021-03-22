#!/usr/bin/env python
from server import run

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8080,
                        help="Set port for server;")
    parser.add_argument('-ha', '--host-address', type=str, default='',
                        help="Set host for server;")
    args = parser.parse_args()
    run(host=args.host_address, port=args.port, )
