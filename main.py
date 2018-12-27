import argparse

from trace_route import Traceroute

parser = argparse.ArgumentParser()
parser.add_argument('--address')
parser.add_argument('--port')
args = parser.parse_args()


def main():
    address = args.address
    port = int(args.port)
    big_tr = Traceroute(address, port)
    big_tr.run()


if __name__ == '__main__':
    main()
