import re
from pathlib import Path
import pandas as pd

demo = pd.read_excel("data/IXI.xls", engine="xlrd")
ages = dict(zip(demo["IXI_ID"], demo["AGE"]))

rows = []
for f in sorted(Path("data/IXI-T1").glob("*-T1.nii.gz")):
    sid = int(re.search(r"IXI0*(\d+)", f.name).group(1))
    rows.append({"subject": f"IXI{sid:03d}", "age": ages.get(sid), "file": f.name})

subs = pd.DataFrame(rows)
subs.to_csv("subjects.csv", index=False)
print("saved subjects.csv:", subs.shape)
