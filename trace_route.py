import socket


class Traceroute:
    def __init__(self, address, port, max_hops=25):
        self.address = address  # инициализируем конечный адрес
        self.port = port  # порт конечного адреса
        self.max_hops = max_hops  # макисмальное количество узлов

    @staticmethod
    def __create_sockets():
        icmp = socket.getprotobyname('icmp')
        udp = socket.getprotobyname('udp')
        receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)  # сокет для прием ICMP пакетов
        sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)  # сокет для отправки UDP пакетов
        return receiver, sender

    def run(self):
        ttl = 1
        port = self.port # выбираем порт неиспользуемый udp
        receiver, sender = self.__create_sockets()
        dest_addr = socket.gethostbyname(self.address)
        while 1:
            sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)  # устанавливем ttl
            receiver.bind(('', port))  # слушаем localhost и нужный нам порт

            pkg = b''
            sender.sendto(pkg, (dest_addr, port))  # отправляем пустой UDP пакет

            curr_addr = None
            curr_name = None

            try:
                _, curr_addr = receiver.recvfrom(512)  # получаем ICMP ответ
                curr_addr = curr_addr[0]  # извлекаем адрес получателся
                try:
                    curr_name = socket.gethostbyaddr(curr_addr)[0]  # получаем хост имя получателя
                except socket.error:
                    curr_name = curr_addr
            except socket.error:
                pass

            if curr_addr is not None:
                curr_host = "%s (%s)" % (curr_name, curr_addr)  # выводим хост имя если его удалось поулчить
            else:
                curr_host = "*"
            print(f'{ttl} {curr_host}')

            if curr_addr == dest_addr or ttl > self.max_hops:  # проверяем достигли ли мы конечного узла, либо превысили порог
                break

            ttl += 1  # увеличиваем ttl
