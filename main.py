import numpy as np
import serial
import os
import time
import datetime
import sys
import numpy as np
import scipy.io as spio
osc_en = sys.argv[1] ##Accept True or False from command prompt. True to save data. false to just run.

if (osc_en == "True"):
    en_oscilloscope = True
else:
    en_oscilloscope = False

if en_oscilloscope == True:
    import Oscilloscope as lecroy

no_combinations = 1
traces_per_file = 100000
samples_per_trace = 25000
num_traces = traces_per_file * no_combinations

if en_oscilloscope == True:
    le = lecroy.Oscilloscope()
    le.connect()
    le.calibrate()
    le.displayOn()
    le.Samples = samples_per_trace
    le.clearsweeps_all()

if en_oscilloscope == False:
    import Oscilloscope as lecroy
    le = lecroy.Oscilloscope()
    le.connect()
    le.displayOn()
    le.clearsweeps_all()

if en_oscilloscope == True:
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('AES_Fixslicing_opt32_%Y-%m-%d_%H_%M_%S/')
    if not os.path.exists(st):
        os.makedirs(st)
        os.chdir(st)

ser = serial.Serial(baudrate=115200, port="COM53", bytesize=8, timeout=1)
# ser.open()
ser.reset_input_buffer()

##Generate plaintext
# f = open("./plaintext_myownAES.txt", "wb")
# c = open("./ciphertext_myownAES.txt", "wb")
for i in range(num_traces):

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
    ##3. save the plaintext.
    ##4. Process the ciphertext back to uint8_t[16], Recieve and save the ciphertext.
    ciphertext = ser.read(size=16)

    if(en_oscilloscope == True):
            value_no = (i / traces_per_file)
            if (i % traces_per_file == traces_per_file - 1):
                time.sleep(0.1)
                seqtrace = le.getWaveform_16_1()[0:samples_per_trace * traces_per_file]
                #seqtrace = list(os.urandom(16))
                #seqtrace = seqtrace + 32768 ##This is because the traces are -32768 to 32768. this transform it.
                tmp_traces = np.split(seqtrace, seqtrace.shape[0] / samples_per_trace)
                spio.savemat("traces_" + str(value_no), {'traces': tmp_traces[0:(traces_per_file):1], 'plaintext': plaintext,\
                                                         'ciphertext': ciphertext}, do_compression=True, oned_as='row')
                print("Saving file " + str(time.time() - ts) + " seconds")
                print("Collected traces: " + str(i + 1))



