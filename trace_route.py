import socket


class Traceroute:
    port = 33434

    def __init__(self, address, max_hops=25):
        self.address = socket.gethostbyaddr(address)
        self.max_hoops = max_hops

    def __create_sockets(self):
        receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.SOCK_DGRAM)
        return receiver, sender

    def run(self):
        ttl = 1
        port = 33434
        receiver, sender = self.__create_sockets()
        while 1:
            sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
            receiver.bind(('', port))

            sender.sendto(b'', (self.address, port))

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
            print(f'{ttl}, {curr_host}')

            if curr_addr == self.address or ttl > self.max_hops:
                break

            ttl += 1
