import os
import scipy.io as spio
import matplotlib.pyplot as plt
import numpy as np



## load key_corr
cwd = os.getcwd()
PATH_Results = os.path.join(cwd,"Results")
PATH = os.path.join(PATH_Results,"AES_my_own_2021-06-09_17_51_39")

traces_fname = os.path.join(PATH, "corr_key.mat")
corr_key_lst_contents = spio.loadmat(traces_fname)
key_corr_lst = corr_key_lst_contents["key_corr_lst"]
max_index_lst = corr_key_lst_contents["max_index_lst"]
print("Hyporthesis key:")
print(max_index_lst[0])

master_key = np.array([0x2b,0x7e,0x15,0x16,0x28,0xae,0xd2,0xa6,0xab,0xf7,0x15,0x88,0x09,0xcf,0x4f,0x3c])
print("Correct Key:")
print(master_key)

## Experiment 1
# for target_byte in range(16):
#     key_corr = key_corr_lst[target_byte]
    # plt.figure()
    # plt.plot(key_corr)
    # plt.plot(master_key[target_byte],key_corr[master_key[target_byte]],'k*')
    # plt.title("Max absolute correlation for every key candidate")
    # plt.xlabel("Key Candidates")
    # plt.ylabel("(Absolute) Correlation")
    # image_fname = os.path.join(PATH, 'Max absolute correlation for every key candidate with target_byte '+ str(target_byte) + '.png')
    # plt.savefig(image_fname)


##Experiment2