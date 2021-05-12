import numpy as np
import serial
import os

ser = serial.Serial()
ser.baudrate= 115200
ser.port= "COM3"
ser.bytesize = 8
ser.timeout = 1
ser.open()

num_plaintext = 2
for i in range(num_plaintext):

    ser.write(b'S') ##This is to start the program.
    x = ser.read()  ##This is to check if the program has started.
    print("Give S: "+str(x))


    ## 1. Create a random plaintext.
    plaintext0 = os.urandom(16)
    plaintext1 = os.urandom(16)

    print('Give plaintext0: ' + str(plaintext0))
    print('Give plaintext1: ' + str(plaintext1))
    ## 2. Send the plaintext into the MCU.
    ser.write(plaintext0)
    ser.write(plaintext1)

    plaintext_receive0 = ser.read(size=16)
    plaintext_receive1 = ser.read(size=16)
    print('plaintext_receive0:' + str(plaintext_receive0))
    print('plaintext_receive1:' + str(plaintext_receive1))

    ciphertext_receive0 = ser.read(size=16)
    ciphertext_receive1 = ser.read(size=16)
    ciphertext_receive0 = list(ciphertext_receive0)
    ciphertext_receive1 = list(ciphertext_receive1)

    print('ciphertext_receive0:' + str(ciphertext_receive0))
    print('ciphertext_receive1:' + str(ciphertext_receive1))

