import socket
import struct


class Traceroute:
    port = 33434

    def __init__(self, address, max_hops=25):
        self.address = address
        self.max_hops = max_hops

    def __create_sockets(self):
        icmp = socket.getprotobyname('icmp')
        udp = socket.getprotobyname('udp')
        receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        timeout = struct.pack("ll", 5, 0)
        receiver.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)
        sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        return receiver, sender

    def run(self, big_package=False):
        ttl = 1
        if big_package:
            port = 33434
        else:
            port = 33437
        receiver, sender = self.__create_sockets()
        dest_addr = socket.gethostbyname(self.address)
        results = []
        while 1:
            sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
            receiver.bind(('', port))

            pkg = b''
            if big_package:
                pkg = bytes([0x13] * 1000)
            sender.sendto(pkg, (dest_addr, port))

            curr_addr = None
            curr_name = None

            try:
                _, curr_addr = receiver.recvfrom(512)
                curr_addr = curr_addr[0]
                try:
                    curr_name = socket.gethostbyaddr(curr_addr)[0]
                except socket.error:
                    curr_name = curr_addr
            except socket.error:
                pass

            if curr_addr is not None:
                curr_host = "%s (%s)" % (curr_name, curr_addr)
            else:
                curr_host = "*"
            results.append(f'{ttl}, {curr_host}')

            if curr_addr == dest_addr or ttl > self.max_hops:
                break

            ttl += 1
        if big_package:
            print('big')
        else:
            print('small')
        for r in results:
            print(r)
