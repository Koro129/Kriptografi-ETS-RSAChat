import socket
import threading

# Inisialisasi socket server
s = socket.socket()
host = '192.168.1.138'
port = 1234

# Binding socket ke alamat dan port yang ditentukan
s.bind((host, port))

# Menunggu koneksi dari client
s.listen(2)
print('Waiting for incoming connections...')

# Menerima koneksi dari client 1
c1, addr1 = s.accept()
print('Client 1 connected from: ', addr1)

# Menerima kunci publik dari client 1
c1_pubkey = c1.recv(1024)

# Menerima koneksi dari client 2
c2, addr2 = s.accept()
print('Client 2 connected from: ', addr2)

# Menerima kunci publik dari client 2
c2_pubkey = c2.recv(1024)

c1.send(c2_pubkey)
c2.send(c1_pubkey)

# Fungsi untuk menerima pesan dari client dan mengirimkan ke client lain
def forward_message(client, other_client, client_name):
    while True:
        try:
            # Terima pesan dari client
            message = client.recv(1024)
            sender = client.getpeername()[0]
            other_client.send(f"{sender}".encode())
            print(f"({client.getpeername()[0]}): {message.hex()}")
            # Kirim pesan ke client lain
            other_client.send(message)
        except:
            # Jika ada kesalahan koneksi, keluar dari thread
            print(f'{client_name} disconnected')
            client.close()
            other_client.close()
            break

# Thread untuk menerima dan mengirimkan pesan dari client 1 ke client 2
c1_to_c2_thread = threading.Thread(target=forward_message, args=(c1, c2, 'Client 1'))
c1_to_c2_thread.start()

# Thread untuk menerima dan mengirimkan pesan dari client 2 ke client 1
c2_to_c1_thread = threading.Thread(target=forward_message, args=(c2, c1, 'Client 2'))
c2_to_c1_thread.start()
