import scipy.io as spio
import os


num_traces = 10

cwd = os.getcwd()
PATH = os.path.join(cwd,"AES_my_own_2021-06-07_12_26_54")
if not os.path.exists(PATH):
    raise("Traces Path does not exist here.")
os.chdir(PATH) #make the folder directory to PATH.


cwd2 = os.getcwd()
mat_fname = os.path.join(cwd2, "traces_0.mat")
mat_contents = spio.loadmat(mat_fname)
traces = mat_contents["traces"]
cip = mat_contents["ciphertexts"]

print('traces:')
print(traces)
print(len(traces))
print(len(traces[0]))
print('ciphertexts:')
print(cip)
print(len(cip))
print(len(cip[0]))

os.chdir("..") ##move back by one folder
### Functions to help check current directory ####
# cwd = os.getcwd()
# print(cwd)
