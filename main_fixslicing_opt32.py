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


ser = serial.Serial(baudrate= 115200, port= "COM53", bytesize = 8, timeout = 1)
#ser.open()
ser.reset_input_buffer()

for i in range(num_traces):

    ser.write(b'S') ##This is to start the program.
    x = ser.read()  ##This is to check if the program has started.
    print("Give S: "+str(x) + "num_traces: " + str(i))


    ## 1. Create a random plaintext.
    plaintext0 = os.urandom(16)
    plaintext1 = os.urandom(16)

##    print('Give plaintext0: ' + str(plaintext0))
##    print('Give plaintext1: ' + str(plaintext1))
    ## 2. Send the plaintext into the MCU.
    ser.write(plaintext0)
    ser.write(plaintext1)

    plaintext_receive0 = ser.read(size=16)
    plaintext_receive1 = ser.read(size=16)
##    print('plaintext_receive0:' + str(plaintext_receive0))
##    print('plaintext_receive1:' + str(plaintext_receive1))

    ciphertext_receive0 = ser.read(size=16)
    ciphertext_receive1 = ser.read(size=16)
    ciphertext_receive0 = list(ciphertext_receive0)
    ciphertext_receive1 = list(ciphertext_receive1)
    
##    print('ciphertext_receive0:' + str(ciphertext_receive0))
##    print('ciphertext_receive1:' + str(ciphertext_receive1))

    if en_oscilloscope == True:
        value_no = (i / traces_per_file)
        if (i % traces_per_file == traces_per_file - 1):
            time.sleep(0.1)
            seqtrace = le.getWaveform_16_1()[0:samples_per_trace * traces_per_file]
            #seqtrace = list(os.urandom(16))
            #seqtrace = seqtrace + 32768 ##This is because the traces are -32768 to 32768. this transform it.  
            tmp_traces = np.split(seqtrace, seqtrace.shape[0] / samples_per_trace)
            spio.savemat("traces_" + str(value_no), {'traces': tmp_traces[0:(traces_per_file):1], 'plaintext0': plaintext0, 'plaintext1': plaintext1,\
                                                     'ciphertext0': ciphertext_receive0, 'ciphertext1': ciphertext_receive1}, do_compression=True, oned_as='row')
            print("Saving file " + str(time.time() - ts) + " seconds")
            print("Collected traces: " + str(i + 1))

