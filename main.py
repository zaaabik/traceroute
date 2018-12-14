import sys

from trace_route import Traceroute


def main():
    address = sys.argv[1]
    if address is None:
        print('address not valid')
        exit(0)
    big_tr = Traceroute(address)
    big_tr.run()
    tr = Traceroute(address)
    tr.run(big_package=True)


if __name__ == '__main__':
    main()
