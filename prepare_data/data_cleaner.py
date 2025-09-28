import json
import shutil
from pathlib import Path
from typing import List
import pandas as pd

def rm_no_annots(df1: pd.DataFrame, df2: pd.DataFrame,
                 id_col_df1: str = "id", id_col_df2: str = "image_id") -> pd.DataFrame:
    """
    Supprime dans df1 les lignes dont l'ID n'existe pas dans df2.

    Args:
        df1 (pd.DataFrame): DataFrame source
        df2 (pd.DataFrame): DataFrame de référence
        id_col_df1 (str): Nom de la colonne ID dans df1
        id_col_df2 (str): Nom de la colonne ID dans df2

    Returns:
        pd.DataFrame: DataFrame df1 filtré
    """

    if id_col_df1 not in df1.columns:
        raise KeyError(f"La colonne {id_col_df1} est absente de df1")
    if id_col_df2 not in df2.columns:
        raise KeyError(f"La colonne {id_col_df2} est absente de df2")

    list_serie1 = df1[id_col_df1].tolist()
    list_serie2 = df2[id_col_df2].tolist()

    list_diff = [z for z in list_serie1 if z not in list_serie2]

    df1_filtered = df1[~df1[id_col_df1].isin(list_diff)].copy()

    print(f"{len(list_diff)} éléments ont été supprimés")
    return df1_filtered

import pandas as pd

def combine_dataframes(dfs: dict) -> dict:
    """
    Reconstitue un dictionnaire JSON COCO à partir d'un dictionnaire de DataFrames.

    Args:
        dfs (dict): dictionnaire de DataFrames avec les clés 'info', 'licenses', 'categories', 'images', 'annotations'

    Returns:
        dict: dictionnaire au format COCO
    """
    required_keys = ["info", "licenses", "categories", "images", "annotations"]
    for key in required_keys:
        if key not in dfs:
            raise ValueError(f"Clé manquante dans dfs : {key}")

    data = {
        "info": dfs["info"].iloc[0].to_dict(),
        "licenses": dfs["licenses"].to_dict(orient="records"),
        "categories": dfs["categories"].to_dict(orient="records"),
        "images": dfs["images"].to_dict(orient="records"),
        "annotations": dfs["annotations"].to_dict(orient="records")
    }

    if len(data["licenses"]) == 1:
        data["licenses"] = data["licenses"]

    return data

def locate_files(df1: pd.DataFrame, df2: pd.DataFrame,
                 col_df1: str = "image_id", col_df2: str = "id", file_col: str = "file_name") -> list:
    """
    Retourne la liste des noms de fichiers de df2 dont l'ID n'existe pas dans df1.

    Args:
        df1 (pd.DataFrame): Premier DataFrame contenant la colonne col_df1
        df2 (pd.DataFrame): Second DataFrame contenant les colonnes col_df2 et file_col
        col_df1 (str): Nom de la colonne dans df1 qui contient les IDs de référence
        col_df2 (str): Nom de la colonne dans df2 à comparer
        file_col (str): Nom de la colonne fichier dans df2

    Returns:
        list: Liste des fichiers de df2 dont l'ID n’est pas dans df1
    """
    for col, df in [(col_df1, df1), (col_df2, df2), (file_col, df2)]:
        if col not in df.columns:
            raise KeyError(f"La colonne '{col}' est absente du DataFrame")

    list_serie1 = df1[col_df1].tolist()
    list_serie2 = df2[col_df2].tolist()

    list_diff = [z for z in list_serie2 if z not in list_serie1]

    files_name = df2.loc[df2[col_df2].isin(list_diff), file_col].tolist()

    return files_name


def duplicate_and_rm_files(folder: str, files_to_remove: List[str], new_folder: str = "data_filtered"):
    """
    Copie uniquement les fichiers .jpg d'un dossier dans un nouveau dossier,
    en excluant une liste de fichiers.

    Args:
        folder (str): Chemin relatif ou absolu du dossier source.
        files_to_remove (list): Liste des noms de fichiers .jpg à exclure.
        new_folder (str): Nom du dossier dupliqué. Par défaut "data_filtered" dans le même répertoire.

    Returns:
        Path: Chemin du nouveau dossier créé.
    """
    source = Path(folder).resolve()

    if not source.is_dir():
        print(f"Le dossier {source} n'existe pas.")
        return None

    new_folder = Path(new_folder)
    if not new_folder.is_absolute():
        new_folder = source.parent / new_folder

    if new_folder.exists():
        print(f"Le dossier {new_folder} existe déjà.")
        return None
    new_folder.mkdir(parents=True)

    jpg_files = [f for f in source.iterdir() if f.is_file() and f.suffix.lower() == ".jpg"]

    for file_path in jpg_files:
        if file_path.name not in files_to_remove:
            shutil.copy2(file_path, new_folder / file_path.name)
        else:
            print(f"{file_path.name} ignoré (présent dans files_to_remove)")

    print(f"Nouveau dossier créé : {new_folder}")
    return new_folder

def save_json(data, chemin_fichier_sortie):
    """
    Sauvegarde le dataframe dans un dictionnaire JSON COCO après supression des images sans annotations dans un nouveau fichier.

    Args:
        data (dict): dictionnaire JSON COCO à sauvegarder.
        chemin_fichier_sortie (str): chemin complet du fichier de sortie.
    """
    with open(chemin_fichier_sortie, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Fichier sauvegardé sous : {chemin_fichier_sortie}")