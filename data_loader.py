import json
import pandas as pd


def load_data(filename, name=None):
        with open('data/' + filename, 'r') as f:
            data = json.load(f)
        
        dfs = {
            "info": pd.DataFrame(data["info"], index=[0]),
            "licenses": pd.DataFrame(data["licenses"], index=[0]),
            "categories": pd.DataFrame(data["categories"]),
            "images": pd.DataFrame(data["images"]),
            "annotations": pd.DataFrame(data["annotations"])
        }

       
        if name:
            if name not in dfs:
                raise ValueError(f"Nom invalide : {name}. Choisis parmi {list(dfs.keys())}")
            return dfs[name]

        return dfs