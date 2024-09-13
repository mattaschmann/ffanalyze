import json
import pandas as pd

with open('data/QBs.json') as f:
    d = json.load(f)
    df = pd.json_normalize(d)
    print(df)

