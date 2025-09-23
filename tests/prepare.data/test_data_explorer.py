from prepare_data.data_explorer import data_infos
from prepare_data.data_loader import load_json, load_dataframes
import pytest
import pandas as pd

def test_data_infos():
    file_dict= load_json("/home/nabil_simplon/wildfire-detection/data/_annotations.coco.json") 
    df= load_dataframes( file_dict, "images")
    assert data_infos(df)


def test_data_infos_no_dataframe():
    file_dict= load_json("/home/nabil_simplon/wildfire-detection/data/_annotations.coco.json") 
    df= load_dataframes( file_dict)
    with pytest.raises(AttributeError):
        data_infos(df)



def test_data_infos_dataframe_empty():
    data_vide = []
    df=pd.DataFrame(data_vide)
    with pytest.raises(AttributeError): 
         data_infos(df)