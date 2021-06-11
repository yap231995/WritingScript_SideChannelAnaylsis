import random
import numpy as np
import os
import scipy.io as spio
import matplotlib.pyplot as plt


sbox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
  0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
  0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
  0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
  0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
  0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
  0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
  0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
  0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
  0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
  0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
  0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
  0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
  0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
  0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
  0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]




def HW(val):
    h = bin(int(val)).count("1")
    return h

def generate_simulated_trace(plaintext,master_key):
    #XOR key
    text = np.bitwise_xor(plaintext, master_key)
    trace = []
    for i in range(text.shape[0]):
        trace.append(HW(sbox[text[i]]))
    return trace
def generate_multiple_traces_and_plaintexts(num_plaintext,master_key):
    traces = []
    plaintexts = []
    def splitting_plaintext(plaintext):
        lst = []
        for i in range(16):
            byte_val = (plaintext >> 8 * i) & 0xff
            # print(hex(byte_val))
            lst.append(byte_val)
        return lst
    seed = 0
    random.seed(seed)
    for i in range(num_plaintext):
        plaintext = random.randint(0, 2 ** 128)
        plaintext = splitting_plaintext(plaintext)
        plaintext = np.array(plaintext)
        plaintexts.append(plaintext)
        traces.append(generate_simulated_trace(plaintext,master_key))
    plaintexts= np.array(plaintexts)
    traces = np.array(traces)
    return (traces,plaintexts)


def cpa(h,traces):
    #Input: h is the column guess matrix of HW(S(plaintext xor key)), traces is a num_traces x num_sample point
    #Return c: array of correlation for each time samples
    c = np.zeros(traces.shape[1])
    for i in range(0, traces.shape[1]):
         c[i] = abs(np.corrcoef(h, traces[:, i])[0, 1]) #traces here is the column i. corrcoef is a Correlation matrix,
                                                        # Roh = ((C_hh, C_ht),(C_th,C_tt)) So we take C_ht
    return c



#Create a matrix h the guess matrix: HW(S(plaintext xor key)) for each key.
#target_byte = 1  #This can be change. (This is going to the sample point for the trace.)
def CPA_traces(pt, traces):
    n_traces = traces.shape[0]
    print(n_traces)
    hypothesis_key = []
    for target_byte in range(16):
        key_corr = np.zeros(256)
        for i in range(256): #key
            H_matrix = np.zeros(n_traces) ## This is the column of H
            for j in range(n_traces):
                H_matrix[j] = HW(sbox[pt[j, target_byte] ^ i])
            key_corr[i] = np.max(cpa(H_matrix, traces))
        max_key = np.argmax(key_corr)
        hypothesis_key.append(max_key)
    return hypothesis_key

def CPA_traces_per_target_byte(pt, traces, target_byte):
    n_traces = traces.shape[0]
    #print(n_traces)

    key_corr = np.zeros(256)
    for i in range(256): #key
        print("Target_byte:" + str(target_byte) + " guess key:"+str(i))
        H_matrix = np.zeros(n_traces) ## This is the column of H
        for j in range(n_traces):
            H_matrix[j] = HW(sbox[pt[j, target_byte] ^ i])
        key_corr[i] = np.max(cpa(H_matrix, traces))
    max_key = np.argmax(key_corr)
    max_val = np.max(key_corr)
    return key_corr, max_key, max_val


def Corr_with_correct_key(pt,traces,master_key, target_byte):
    n_traces = traces.shape[0]
    H_matrix = np.zeros(n_traces)
    for j in range(n_traces):
        H_matrix[j] = HW(sbox[pt[j, target_byte] ^ master_key[target_byte]])
    key_corr = np.max(cpa(H_matrix, traces))
    return key_corr



cwd = os.getcwd()
PATH = os.path.join(cwd,"plaintext_folder")
num_traces = 10000

##Read traces
cwd = os.getcwd()
PATH_traces = os.path.join(cwd,"AES_my_own_2021-06-10_11_48_13") ## Need to change this accordingly
PATH_image = os.path.join(PATH_traces,"images")
if not os.path.exists(PATH_traces):
    raise("Traces Path does not exist here.")
if not os.path.exists(PATH_image):
    os.makedirs(PATH_image)

traces_fname = os.path.join(PATH_traces, "traces_0.mat")
traces_contents = spio.loadmat(traces_fname)
traces = traces_contents["traces"]

traces = traces[:, 5000:17500] #Truncate the traces according to the trigger:



##Read the plaintext
PATH_plaintext = os.path.join(cwd,"plaintext_folder")
plaintexts_fname = os.path.join(PATH_plaintext, "plaintexts.mat")
plaintexts_contents = spio.loadmat(plaintexts_fname)
pt = plaintexts_contents["plaintext"]
pt = pt[:num_traces]
print("Finished loading Plaintext")

master_key = np.array([0x2b,0x7e,0x15,0x16,0x28,0xae,0xd2,0xa6,0xab,0xf7,0x15,0x88,0x09,0xcf,0x4f,0x3c])
####Experiment1: Do CPA for each byte find the max abs correlation for every key candidate using all the traces
# max_index_lst = []
# key_corr_lst = []
# for target_byte in range(16):
#     key_corr, max_index, max_val = CPA_traces_per_target_byte(pt, traces, target_byte)
#     key_corr_lst.append(key_corr)
#     max_index_lst.append(max_index)
# spio.savemat("corr_key.mat", {'key_corr_lst': key_corr_lst, 'max_index_lst': max_index_lst}, do_compression=True, oned_as='row')
# load it and use corr_key_to_image.py in Experiment 1 for all graph and obtain the graph.



###Experiment2: Do CPA over number of sample
target_byte = 4
x_axis_value = []
key_corr_over_trunc_traces_lst = []
for no_trace in range(100,traces.shape[0], 100):
    x_axis_value.append(no_trace)
    trunc_trace = traces[:no_trace,:]
    #key_corr = list(os.urandom(256))
    key_corr, _,_ = CPA_traces_per_target_byte(pt, trunc_trace, target_byte) #key_corr = max correlation of each candidate key->key_corr.shape = (256,)
    key_corr_over_trunc_traces_lst.append(key_corr)
key_corr_over_trunc_traces_lst = np.array(key_corr_over_trunc_traces_lst)
PATH_Results = os.path.join(cwd,"Results")
PATH_Results_specific = os.path.join(PATH_Results,"AES_my_own_2021-06-09_17_51_39")
os.chdir(PATH_Results_specific)
spio.savemat("key_corr_over_trunc_traces_lst.mat", {'key_corr_over_trunc_traces_lst': key_corr_over_trunc_traces_lst}, do_compression=True, oned_as='row')
os.chdir('../..')













##Check for sitmulated traces
##master_key = np.array([0x2b,0x7e,0x15,0x16,0x28,0xae,0xd2,0xa6,0xab,0xf7,0x15,0x88,0x09,0xcf,0x4f,0x3c])
##num_plaintext = 100 # = num_traces
##traces, pt = generate_multiple_traces_and_plaintexts(num_plaintext,master_key)
# hypothesis_key = CPA_traces(pt, traces)
# for target_byte in range(len(hypothesis_key)):
#     if (master_key[target_byte] != hypothesis_key[target_byte]):
#         print("Wrong " + str(target_byte))
#     else:
#         print("Correct " + str(target_byte))