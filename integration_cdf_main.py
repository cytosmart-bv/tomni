#%%
import json
from tkinter import filedialog

from tomni.cytosmart_data_format import CytoSmartDataFormat

#%%
json_fp = filedialog.askopenfilename(title="Select CDF JSONs.")

with open(json_fp, "rb") as f:
    dicts = json.load(f)
cdf = CytoSmartDataFormat.from_dicts(dicts=dicts)

#%%
print(f"__len__: {len(cdf)}")

#%%
# cdf creates a generator.
count = 0
for annotation in cdf:
    count += 1
print(f"Count: {count}")


#%%
dicts_ = cdf.to_dict()
with open("temp.json", "w") as f:
    json.dump(dicts_, f)

# %%
