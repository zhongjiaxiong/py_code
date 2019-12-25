import socket


ip_addr = 'localhost'  # 写你本机ip
port = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(client)
client.connect((ip_addr, port))

while True:
    data = input('input >>>')
    if not data:  # 如果数据为空，继续输入
        continue
    client.send(data.encode())  # 发送数据
    data = client.recv(1024)  # 接收数据
    print('接收数据 =', data.decode())

client.close()  # 关闭