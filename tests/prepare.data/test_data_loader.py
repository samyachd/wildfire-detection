from prepare_data.data_loader import load_json, load_dataframes
import pytest
import json
from pathlib import Path
import pandas as pd

# test le chargement de fichier json
def test_load_json():
    assert load_json("/home/nabil_simplon/wildfire-detection/data/_annotations.coco.json") 

def test_load_json_fichier_invalide():
    with pytest.raises(ValueError):
        df= load_json("/home/nabil_simplon/wildfire-detection/data/")

def test_load_json_fichier_inexistant():
    with pytest.raises(FileNotFoundError):
        df= load_json("/home/nabil_simplon/wildfire-detection/data/_annotations.coco")


# test entrée = dict, sortie= dataframe
def test_load_dataframe():
    file_dict= load_json("/home/nabil_simplon/wildfire-detection/data/_annotations.coco.json") 
    df= load_dataframes( file_dict)
    assert df

# Test load_dataframes sans name (tous les dfs)
def test_load_dataframe():
    dfs = load_json("/home/nabil_simplon/wildfire-detection/data/_annotations.coco.json")
    assert isinstance(dfs, dict)
    assert all(isinstance(df, (pd.DataFrame, list, dict)) for df in dfs.values())

# Test load_dataframes avec name valide
    df_images = load_dataframes(dfs, name="images")
    assert isinstance(df_images, pd.DataFrame)
    assert "file_name" in df_images.columns

   # Test load_dataframes avec name invalide
    with pytest.raises(ValueError):
        load_dataframes(dfs, name="invalide")
