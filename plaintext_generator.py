import scipy.io as spio
import os
import time
import datetime
import random


num_plaintext = 50000

cwd = os.getcwd()
PATH = os.path.join(cwd,"plaintext_folder")
if not os.path.exists(PATH):
    os.makedirs(PATH)
os.chdir(PATH) #make the folder directory to PATH.

#Converting int to a list. 
def splitting_plaintext(plaintext):
    lst = []
    for i in range(16):
        byte_val = (plaintext>>8*i)&0xff
        #print(hex(byte_val))
        lst.append(byte_val)
    return lst

plaintexts = []
for i in range(num_plaintext):
    text = random.randint(0, 2**128)
    print("num_text:" + str(i))
    #print(plaintext)
    #print(hex(plaintext))
    text = splitting_plaintext(text)
    plaintexts.append(text)

spio.savemat("plaintexts0.mat", {"plaintext": plaintexts}, do_compression=True, oned_as='row')



cwd2 = os.getcwd()
mat_fname = os.path.join(cwd2, "plaintexts0.mat")
#print(mat_fname)
mat_contents = spio.loadmat(mat_fname)
p = mat_contents["plaintext"]
print(list(p[0]))
p = list(p[0])
    


os.chdir("..") ##move back by one folder
### Functions to help check current directory ####
# cwd = os.getcwd()
# print(cwd)
