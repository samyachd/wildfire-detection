import json
import pandas as pd
import os
from data_loader import load_data

filename = "_annotations.coco.json"
path = "/data/"

df_images = load_data(filename,"images")
df_annotations= load_data(filename,"annotations")

def remove_no_annotations():
        
    list_annot_id = df_annotations["image_id"].tolist()
    list_image_id = df_images["id"].tolist()

    list_diff = [z for z in list_image_id if z not in list_annot_id]
    df_annotations["image_id"].drop(index=list_diff)

def files_extension(folder):

    files = os.listdir(str(os.getcwd()) + folder)
    files = [f for f in files if os.path.isfile(os.path.join(str(os.getcwd()) + folder, f))]
    list_ext = [os.path.splitext(f)[1] for f in files]

    return set(list_ext)