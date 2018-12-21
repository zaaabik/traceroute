import argparse

from trace_route import Traceroute

parser = argparse.ArgumentParser()
parser.add_argument('--address')
parser.add_argument('--b', action='store_true')
args = parser.parse_args()


def main():
    address = args.address
    big_tr = Traceroute(address)
    big_tr.run()
    print(args.b)
    if args.b:
        tr = Traceroute(address)
        tr.run(big_package=True)


if __name__ == '__main__':
    main()
