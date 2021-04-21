#%%
import numpy as np 
from time import time

from tomni.select_labels.main import select_labels_as_indices
import pickle

path = r"C:\Users\tomni\Downloads\labels.dump"
fileObject = open(path,'rb')
data = pickle.load(fileObject)

# #%% version 3
# start = time()
# result = select_labels_as_indices(data)
# print("0.3.3 timing", time() - start)

#%% version 2
import numpy as np 
from time import time

from main_0_4 import select_labels_as_indices as select_labels_as_indices_v2

start = time()
result = select_labels_as_indices_v2(data)
print("scipy timing", time() - start)