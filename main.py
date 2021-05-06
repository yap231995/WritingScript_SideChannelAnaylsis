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
f = open("./plaintext.txt", "wb")
c = open("./ciphertext.txt", "wb")
for i in range(num_plaintext):
    ser.write(b'S') ##This is to start the program.
    x = ser.read()
    print("Give S: "+str(x))
    plaintext = os.urandom(16)
    print('Give plaintext: '+ str(plaintext))
    ser.write(plaintext)
    matrix1 = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for k in range(4):
        for j in range(4):
            matrix1[j][k] = ser.read()
    print("Outer Matrix: ")
    print(matrix1)
    plaintext_receive = ser.read(size=16)
    print('Recieved plaintext: '+str(plaintext_receive) +" \n")
    ##1. save the plaintext. (Need to change to spio.savemat)
    f.write(plaintext)
    ##2. convert the recieved plaintext on the MCU to be processed.

    ##TODO: 3. Process the ciphertext back to uint8_t[16], Recieve and save the ciphertext. (Need to check.)
    ciphertext = ser.read(size=16)
    c.write(ciphertext)


print("\nSAVE AND PRINT THE PLAINTEXT: ")
f.close()
c.close()
f = open("./plaintext.txt", "rb")
contents = f.read(16)
print(contents)
contents = f.read(16)
print(contents)

f.close()

print("\nSAVE AND PRINT THE CIPHERTEXT: ")
c = open("./ciphertext.txt", "rb")
ciph = c.read(16)
print(ciph)

ciph = c.read(16)
print(ciph)
c.close()