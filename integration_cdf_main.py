import glob
import json
from tkinter import filedialog

from tomni.cytosmart_data_format import CytoSmartDataFormat

# json_filepaths = filedialog.askopenfilenames(title="Select CDF JSONs.")

json_fp = r"C:\Users\janni\Data\julia_thp_exp4\6eccfc85-b5b6-4eae-93dd-1af4690dc8bc_brightfield_1644225105198.json"


with open(json_fp, "rb") as f:
    dicts = json.load(f)

cdf = CytoSmartDataFormat.from_dicts(dicts=dicts)
print(cdf)
