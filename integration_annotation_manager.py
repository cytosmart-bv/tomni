#%%
import json
from tkinter import filedialog

from tomni.annotation_manager import AnnotationManager
from tomni.transformers.json2contours import json2contours

#%%
json_fp = filedialog.askopenfilename(title="Select CDF JSONs.")

with open(json_fp, "rb") as f:
    dicts = json.load(f)
    print(f"Found {len(dicts)} dictionaries in json file.")
#%%
manager = AnnotationManager.from_dicts(dicts=dicts)
print(f"__len__: {len(manager)}")


#%%
contours = [json2contours(d) for d in dicts]
manager = AnnotationManager.from_contours(contours=contours)

#%%
print(f"__len__: {len(manager)}")
print(f"__len__: {len(manager + manager)}")


#%%
# manager creates a generator.
count = 0
for annotation in manager:
    count += 1
print(f"Count: {count}")


#%%
dicts_ = manager.to_dict()
with open("temp.json", "w") as f:
    json.dump(dicts_, f)

# %%
conts = manager.to_contours()
print(conts)


#%%
annotations = manager.filter(feature="roundness", min_val=0.5, max_val=1.0)
print(annotations)

# %%
# Filter with inplace=True: manager object is updated internally. Returns manager object to allow chaining.
updated_manager = manager.filter(
    # The return does not have to be used. This is merely to show difference between inplace.
    feature="roundness",
    min_val=0.5,
    max_val=1.0,
    inplace=True,
).filter(feature="area", min_val=0, max_val=1000, inplace=True)
print(type(updated_manager))


#%%
# Filter: inplace=False returns a new list of annotations.
annotations = manager.filter(
    feature="roundness", min_val=0.5, max_val=1.0, inplace=False
)
print(type(annotations))

# %%
