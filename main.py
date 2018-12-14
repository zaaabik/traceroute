import sys

from trace_route import Traceroute


def main():
    address = sys.argv[1]
    if address is None:
        print('address not valid')
        exit(0)
    tr = Traceroute(address)
    tr.run()


if __name__ == '__main__':
    main()