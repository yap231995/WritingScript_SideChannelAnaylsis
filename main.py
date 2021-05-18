import numpy as np
import serial
import os

ser = serial.Serial()
ser.baudrate= 115200
ser.port= "COM3"
ser.bytesize = 8
ser.timeout = 1
ser.open()

##Generate plaintext
num_plaintext = 2
f = open("./plaintext_myownAES.txt", "wb")
c = open("./ciphertext_myownAES.txt", "wb")
for i in range(num_plaintext):

    ser.write(b'S') ##This is to start the program.
    x = ser.read()  ##This is to check if the program has started.
    print("Give S: "+str(x))


    ## 1. Create a random plaintext.
    plaintext = os.urandom(16)
    # Example to test plaintext:
    # plaintext = [0x32,0x43,0xf6,0xa8,0x88,0x5a,0x30,0x8d,0x31,0x31,0x98,0xa2,0xe0,0x37,0x07,0x34]
    # plaintext = bytearray(plaintext)
    print('Give plaintext: ' + str(plaintext))
    ## 2. Send the plaintext into the MCU.
    ser.write(plaintext)


    matrix1 = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for k in range(4):
        for j in range(4):
            matrix1[j][k] = ser.read()
    print("Outer Matrix: ")
    print(matrix1)
    plaintext_receive = ser.read(size=16)
    print('Recieved plaintext: '+str(plaintext_receive) +" \n")
    ##3. save the plaintext. (TODO: Need to change to spio.savemat)
    f.write(plaintext)

    ##4. Process the ciphertext back to uint8_t[16], Recieve and save the ciphertext.
    ciphertext = ser.read(size=16)
    c.write(ciphertext)


print("\nSAVE AND PRINT THE PLAINTEXT: ")
f.close()
c.close()
f = open("./plaintext_myownAES.txt", "rb")
contents = f.read(16)
print(contents)
contents = f.read(16)
print(contents)

f.close()

print("\nSAVE AND PRINT THE CIPHERTEXT: ")
c = open("./ciphertext_myownAES.txt", "rb")
ciph = c.read(16)
print(ciph)

ciph = c.read(16)
#ciph = list(ciph)
print(ciph)
# Example to check ciphertext
# ciphertext = np.array([0x39, 0x25, 0x84, 0x1d, 0x02, 0xdc, 0x09, 0xfb, 0xdc, 0x11, 0x85, 0x97, 0x19, 0x6a, 0x0b, 0x32])
# print('ciphertext_receive1:' + str(ciphertext))
c.close()