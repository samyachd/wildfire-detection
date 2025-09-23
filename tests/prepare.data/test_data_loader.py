from prepare_data.data_loader import load_json

import json
from pathlib import Path

def test_load_json():
    assert load_json("/home/nabil_simplon/wildfire-detection/data/_annotations.coco.json") 
