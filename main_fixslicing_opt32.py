import numpy as np
import serial
import os
import time
import datetime
import sys
import numpy as np
import scipy.io as spio
import struct

osc_en = sys.argv[1] ##Accept True or False from command prompt. True to save data. false to just run.

if (osc_en == "True"):
    en_oscilloscope = True
else:
    en_oscilloscope = False
    
if en_oscilloscope == True:
    import Oscilloscope as lecroy


no_combinations = 1
traces_per_file = 10 #make sure in sequence it is set to this number. 
samples_per_trace = 10000 #Uses big knob under Horizontal to set it.
num_traces = traces_per_file * no_combinations
cwd = os.getcwd()
PATH_Plaintext = os.path.join(cwd,"plaintext_folder")

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
    st = datetime.datetime.fromtimestamp(ts).strftime('AES_Fixslicing_opt32_%Y-%m-%d_%H_%M_%S/') #Remember to change the name accordingingly. 
    if not os.path.exists(st):
        os.makedirs(st)
        os.chdir(st)


ser = serial.Serial(baudrate= 115200, port= "COM53", bytesize = 8, timeout = 1)
#ser.open()
ser.reset_input_buffer()
time.sleep(2)

ciphertext_lst =[]
for i in range(num_traces):

    ser.write(b'S') ##This is to start the program.
    x = ser.read()  ##This is to check if the program has started.
    print("Give S: "+str(x) + "\nnum_traces: " + str(i))


    ## 1. Create a random plaintext.
    # plaintext0 = os.urandom(16)
    # plaintext1 = os.urandom(16)

    ## Test PlainText
    # plaintext0 = [0x32,0x43,0xf6,0xa8,0x88,0x5a,0x30,0x8d,0x31,0x31,0x98,0xa2,0xe0,0x37,0x07,0x34]
    # plaintext0 = bytearray(plaintext0)
    # plaintext1 = [0x32,0x43,0xf6,0xa8,0x88,0x5a,0x30,0x8d,0x31,0x31,0x98,0xa2,0xe0,0x37,0x07,0x34]
    # plaintext1 = bytearray(plaintext1)
    # print('Give plaintext0: ' + str(plaintext0))
    # print('Give plaintext1: ' + str(plaintext1))

    mat_fname = os.path.join(PATH_Plaintext, "plaintexts"+ str(i)+".mat")
    mat_contents = spio.loadmat(mat_fname)
    p = mat_contents["plaintext"] ## Same plaintext. 
    plaintext0 = p[0].tolist()
    #plaintext0 = bytearray(plaintext0)
    plaintext1 = p[0].tolist()
    #plaintext1 = bytearray(plaintext1)
##    print('Give plaintext0: ' + str(plaintext0))
##    print('Give plaintext1: ' + str(plaintext1))


    ## 2. Send the plaintext into the MCU.
    ser.write(plaintext0)
    ser.write(plaintext1)

    plaintext_receive0 = ser.read(size=16)
    plaintext_receive1 = ser.read(size=16)
    plaintext_receive0 = list(plaintext_receive0)
## Check plaintext
##    for k in range(len(plaintext_receive0)):
##        plaintext_receive0[k] = struct.unpack('>B',plaintext_receive0[k])[0]
##    plaintext_receive1 = list(plaintext_receive1)
##    for k in range(len(plaintext_receive1)):
##        plaintext_receive1[k] = struct.unpack('>B',plaintext_receive1[k])[0]
##    print('plaintext_receive0:' + str(plaintext_receive0))
##    print('plaintext_receive1:' + str(plaintext_receive1))
    
    ciphertext_receive0 = ser.read(size=16)
    ciphertext_receive1 = ser.read(size=16)
    ciphertext_receive0 = list(ciphertext_receive0)
    ciphertext_receive1 = list(ciphertext_receive1)
    

##Convert ciphertext into int list and store it.
    
    for k in range(len(ciphertext_receive0)):
        ciphertext_receive0[k] = struct.unpack('>B',ciphertext_receive0[k])[0]
    ciphertext_lst.append(ciphertext_receive0)
##   
##    for k in range(len(ciphertext_receive1)):
##        ciphertext_receive1[k] = struct.unpack('>B',ciphertext_receive1[k])[0]
##

    #Test Ciphertext: [0x39,0x25,0x84,0x1d,0x02,0xdc,0x09,0xfb,0xdc,0x11,0x85,0x97,0x19,0x6a,0x0b,0x32]
##    print('ciphertext_receive0:' + str(ciphertext_receive0))
##    print('ciphertext_receive1:' + str(ciphertext_receive1))
    # print('Actual ciphertext:')
    # print([0x39,0x25,0x84,0x1d,0x02,0xdc,0x09,0xfb,0xdc,0x11,0x85,0x97,0x19,0x6a,0x0b,0x32])


    if(en_oscilloscope == True):
        value_no = (i / traces_per_file)
        if (i % traces_per_file == traces_per_file - 1):
            time.sleep(0.1)
            seqtrace = le.getWaveform_16_1()[0:samples_per_trace * traces_per_file]
            print((seqtrace))
            #seqtrace = list(os.urandom(16))
            
            seqtrace = seqtrace + 32768 ##This is because the traces are -32768 to 32768. this transform it.
            tmp_traces = np.split(seqtrace, seqtrace.shape[0] / samples_per_trace)
            print(len(tmp_traces))
            #Remember to change the ciphertext if they are different.
            spio.savemat("traces_" + str(value_no)+".mat", {'traces': tmp_traces[0:(traces_per_file):1], 'ciphertexts': ciphertext_lst}, do_compression=True, oned_as='row')
            print("Saving file " + str(time.time() - ts) + " seconds")
            print("Collected traces: " + str(i + 1))
    

os.chdir("..")

