from prepare_data.data_loader import load_dataframes, load_json
from prepare_data.data_explorer import files_extension, compare_files, inv_values, ids_check
from prepare_data.data_cleaner import  rm_no_annots, duplicate_and_rm_files, save_json, locate_files, combine_dataframes
from prepare_data.data_preparation import test_split, create_targets
import pandas as pd

path = "/home/achar/test_bash/wildfire-detection/data/_annotations.coco.json"
folder = "data"
json_filename = "_annotations.coco.json"
target_dir = "datasets"
origin_dir = "data_filtered"
subdir = ["test", "train", "val"]

def data_pipeline():
    
    print("Data loading started ... ")

    data = load_json(path) # On lit le fichier JSON

    df_images = load_dataframes(data,"images")
    df_annotations = load_dataframes(data,"annotations")
    df_info = load_dataframes(data,"info")
    df_licenses = load_dataframes(data,"licenses")
    df_categories = load_dataframes(data,"categories")

    print("Data loading finished")
    print("Data exploration started ...")

    files_extension(folder) # On affiche les extensions de fichier dans le dossier
    compare_files(folder, df_images["file_name"], json_filename) # On compare les noms de fichier avec ceux du dataframe images
    inv_values(df_annotations) # On check les valeurs de bbox et area
    ids_check(df_annotations["image_id"], df_images["id"]) # On check s'il y a des id de annotations qui n'existent pas dans images
    ids_check(df_images["id"], df_annotations["image_id"]) # Et l'inverse

    print("Data exploration finished")
    print("Data cleaning started ...")

    df_filtered = rm_no_annots(df_images, df_annotations) # On supprime les images sans annotations dans le df
    files_list = locate_files(df_annotations, df_images)
    duplicate_and_rm_files(folder, files_list)
    dfs = {
        "info" : df_info,
        "licenses": df_licenses,
        "categories": df_categories,
        "images" : df_filtered,
        "annotations":df_annotations
    }
    json_filtered = combine_dataframes(dfs)
    save_json(json_filtered, "data_filtered/_annotations_filtered.coco.json")

    print("Data cleaning finished, completed succesfully")
    print("Data preparation started ...")

    create_targets(origin_dir, target_dir)
    test_split(origin_dir, target_dir)

    content = """\
    test: test/images
    train: train/images
    val: val/images
    names:
     0: wildfire
     1: fire
    nc: 2
    """

    with open(target_dir+"/data.yaml", "w", encoding="utf-8") as f:
        f.write(content)

    print("Data preparation finished, all done!")




