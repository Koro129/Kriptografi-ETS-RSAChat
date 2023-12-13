import socket
import threading
import random
import math

# Fungsi untuk menghasilkan bilangan prima secara acak
def generate_prime_number():
    while True:
        # Pilih bilangan prima secara acak dari 1000 hingga 10000
        p = random.randint(1000, 10000)
        if is_prime(p):
            return p

# Fungsi untuk memeriksa apakah sebuah bilangan prima
def is_prime(n):
    if n == 2 or n == 3:
        return True
    if n == 1 or n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n))+1, 2):
        if n % i == 0:
            return False
    return True

# Fungsi untuk menghasilkan bilangan coprime
def generate_coprime(p):
    while True:
        # Pilih bilangan acak dari 2 hingga p-1
        e = random.randint(2, p-1)
        if math.gcd(e, p-1) == 1:
            return e

# Fungsi untuk menghitung inversi modular menggunakan Algoritma Extended Euclidean
def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

# Inisialisasi socket client
s = socket.socket()
host = '192.168.1.138'
port = 1234

# Terhubung ke server
s.connect((host, port))

# Menghasilkan bilangan prima secara acak
p = generate_prime_number()

# Menghasilkan bilangan coprime
e = generate_coprime(p)

# Menghitung bilangan d sebagai inversi modular dari e modulo p-1
d = modinv(e, p-1)

# Mengirimkan kunci publik ke server
pubkey = (p, e)
s.send(str(pubkey).encode())

# Menerima kunci publik client lain dari server
client_pubkey = eval(s.recv(1024).decode())

# Fungsi untuk mengenkripsi pesan menggunakan kunci publik
def encrypt(message, pubkey):
    p, e = pubkey
    # Konversi pesan menjadi bilangan menggunakan ASCII
    m = [ord(char) for char in message]
    # Mengenkripsi setiap bilangan menggunakan Algoritma Exponentiation Modulo
    c = [pow(char, e, p) for char in m]
    return c

# Fungsi untuk mendekripsi pesan menggunakan kunci privat
def decrypt(c, privkey):
    p, d = privkey
    # Mendekripsi setiap bilangan menggunakan Algoritma Exponentiation Modulo
    m = [chr(pow(char, d, p)) for char in c]
    # Menggabungkan setiap karakter menjadi pesan
    message = ''.join(m)
    return message

# Fungsi untuk menerima pesan dari server
def receive_message():
    while True:
        try:
            # Terima pesan dari server
            sender = s.recv(1024).decode()
            message = s.recv(1024).decode()
            # Dekripsi pesan
            message = decrypt(eval(message), (p, d))
            print(f"({sender}): {message}")
            # print(message)
        except:
            # Jika ada kesalahan koneksi, keluar dari thread
            break

#Thread untuk menerima pesan
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

#Loop untuk mengirim pesan ke server
while True:
    message = input()
    # Enkripsi pesan dengan kunci publik client lain
    encrypted_message = encrypt(message, client_pubkey)
    # Kirim pesan ke server
    s.send(str(encrypted_message).encode())