#%%
import json
from tkinter import filedialog

from tomni.cytosmart_data_format import CytoSmartDataFormat
from tomni.transformers.json2contours import json2contours

#%%
json_fp = filedialog.askopenfilename(title="Select CDF JSONs.")

with open(json_fp, "rb") as f:
    dicts = json.load(f)
    print(f"Found {len(dicts)} dictionaries in json file.")
#%%
cdf = CytoSmartDataFormat.from_dicts(dicts=dicts)


#%%
contours = [json2contours(d) for d in dicts]
cdf = CytoSmartDataFormat.from_contours(contours=contours)

#%%
print(f"__len__: {len(cdf)}")
print(f"__len__: {len(cdf+cdf)}")

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
conts = cdf.to_contours()
print(conts)
