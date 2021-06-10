import struct
import numpy as np
import serial
import os
import time
import datetime
import sys
import scipy.io as spio
#
# osc_en = sys.argv[1] ##Accept True or False from command prompt. True to save data. false to just run.
#
# if (osc_en == "True"):
#     en_oscilloscope = True
# else:
#     en_oscilloscope = False
#
# if en_oscilloscope == True:
#     import Oscilloscope as lecroy

no_combinations = 1
traces_per_file = 2 #make sure in sequence it is set to this number.
samples_per_trace = 10000 #Uses big knob under Horizontal to set it. 
num_traces = traces_per_file * no_combinations
cwd = os.getcwd()
PATH_Plaintext = cwd
#PATH_Plaintext = os.path.join(cwd,"plaintext_folder")

# if en_oscilloscope == True:
#     le = lecroy.Oscilloscope()
#     le.connect()
#     le.calibrate()
#     le.displayOn()
#     le.Samples = samples_per_trace
#     le.clearsweeps_all()
#
# if en_oscilloscope == False:
#     import Oscilloscope as lecroy
#     le = lecroy.Oscilloscope()
#     le.connect()
#     le.displayOn()
#     le.clearsweeps_all()
#
# if en_oscilloscope == True:
#  ts = time.time()
#  st = datetime.datetime.fromtimestamp(ts).strftime('AES_my_own_%Y-%m-%d_%H_%M_%S/')
#  if not os.path.exists(st):
#      os.makedirs(st)
#      os.chdir(st)

ser = serial.Serial(baudrate=115200, port="COM3", bytesize=8, timeout=1)
ser.reset_input_buffer()

##Read plaintext file.
plaintexts_fname = os.path.join(PATH_Plaintext, "plaintext_folder/plaintexts.mat")
plaintexts_contents = spio.loadmat(plaintexts_fname)
p = plaintexts_contents["plaintext"]
ciphertext_lst = []

time.sleep(2)
for i in range(num_traces):

    ser.write('S') ##This is to start the program.
    x = ser.read()  ##This is to check if the program has started.
    print("Give S: "+str(x) + "\nnum_traces: " + str(i))

    ##Create a random plaintext.
    # Example to test plaintext:
    # plaintext = [0x32,0x43,0xf6,0xa8,0x88,0x5a,0x30,0x8d,0x31,0x31,0x98,0xa2,0xe0,0x37,0x07,0x34]
    # plaintext = bytearray(plaintext)


    plaintext = p[i]
    plaintext = plaintext.tolist()
    print(plaintext)
    print('Give plaintext: ' + str(plaintext))

    ## 2. Send the plaintext into the MCU.
    ser.write(plaintext)


##    matrix1 = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
##    for k in range(4):
##        for j in range(4):
##            matrix1[j][k] = ser.read()
##            matrix1[j][k] = struct.unpack('>B',matrix1[j][k])[0]
##    print("Plaintext Matrix Initialised inside MC: ")
##    print(matrix1)
    
    ##3. save the plaintext.
    ##4. Process the ciphertext back to uint8_t[16], Recieve and save the ciphertext.
    ciphertext = ser.read(size=16)
    ciphertext = list(ciphertext)
    for k in range(len(ciphertext)):
        ciphertext[k] = struct.unpack('>B',ciphertext[k])[0]
    ciphertext_lst.append(ciphertext)
    print('Recieved ciphertext: '+str(ciphertext))
    #The test ciphertext obtain should be [0x39,0x25,0x84,0x1d,0x02,0xdc,0x09,0xfb,0xdc,0x11,0x85,0x97,0x19,0x6a,0x0b,0x32].
    # print('Actual ciphertext:')
    # print([0x39,0x25,0x84,0x1d,0x02,0xdc,0x09,0xfb,0xdc,0x11,0x85,0x97,0x19,0x6a,0x0b,0x32])
    # #
    # if(en_oscilloscope == True):
    #     value_no = (i / traces_per_file)
    #     if (i % traces_per_file == traces_per_file - 1):
    #         time.sleep(0.1)
    #         seqtrace = le.getWaveform_16_1()[0:samples_per_trace * traces_per_file]
    #         print((seqtrace))
    #         #seqtrace = list(os.urandom(16))
    #
    #         seqtrace = seqtrace + 32768 ##This is because the traces are -32768 to 32768. this transform it.
    #         tmp_traces = np.split(seqtrace, seqtrace.shape[0] / samples_per_trace)
    #         spio.savemat("traces_" + str(value_no)+".mat", {'traces': tmp_traces[0:(traces_per_file):1], 'ciphertexts': ciphertext_lst}, do_compression=True, oned_as='row')
    #         print("Saving file " + str(time.time() - ts) + " seconds")
    #         print("Collected traces: " + str(i + 1))
    #         print(os.getcwd())

os.chdir("..")



    
