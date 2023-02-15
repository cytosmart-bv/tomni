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

#%%
# cdf creates a generator.
count = 0
for annotation in cdf:
    count += 1
print(f"Count: {count}")


#%%
dicts_ = cdf.to_dict(
    do_compress=True, n_iter=3, n_points_limit=100, do_rdp_compresion=True
)
with open(json_fp.replace(".json", "_dict.json"), "w") as f:
    json.dump(dicts_, f)


# %%
conts = cdf.to_contours()
print(conts)


#%%
annotations = cdf.filter(feature="roundness", min_val=0.5, max_val=1.0)
print(annotations)

# %%
# Filter with inplace=True: CDF object is updated internally. Returns CDF object to allow chaining.
updated_cdf = cdf.filter(
    # The return does not have to be used. This is merely to show difference between inplace.
    feature="roundness",
    min_val=0.5,
    max_val=1.0,
    inplace=True,
).filter(feature="area", min_val=0, max_val=1000, inplace=True)
print(type(updated_cdf))


#%%
# Filter: inplace=False returns a new list of annotations.
annotations = cdf.filter(feature="roundness", min_val=0.5, max_val=1.0, inplace=False)
print(type(annotations))

# %%
