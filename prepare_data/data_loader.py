import json
import pandas as pd
from pathlib import Path

def load_json(file_path: str | Path) -> dict:
    """
    Lit un fichier JSON et retourne son contenu sous forme de dictionnaire.

    Args:
        file_path (str | Path): Chemin vers le fichier JSON.

    Returns:
        dict: Contenu du fichier JSON.

    Raises:
        FileNotFoundError: Si le fichier n’existe pas.
        json.JSONDecodeError: Si le contenu n'est pas un JSON valide.
    """
    file_path = Path(file_path)
    

    if not file_path.exists():
        raise FileNotFoundError(f"Le fichier {file_path} n’existe pas.")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Le fichier {file_path} n'est pas un JSON valide : {e}")

    return data

def load_dataframes(dict, name=None):
    """Découpes le dictionnaire fourni en entrée en plusieurs dataframes

    Args:
        data (_type_): Dictionnaire
        name (_type_, optional): Nom du dataframe que l'on veut parmis info, licenses, categories, images et annotations.

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    dfs = {
        "info": pd.DataFrame(dict["info"], index=[0]),
        "licenses": pd.DataFrame(dict["licenses"], index=[0]),
        "categories": pd.DataFrame(dict["categories"]),
        "images": pd.DataFrame(dict["images"]),
        "annotations": pd.DataFrame(dict["annotations"])
    }

    if name:
        if name not in dfs:
            raise ValueError(f"Nom invalide : {name}. Choisis parmi {list(dfs.keys())}")
        return dfs[name]

    return dfs
