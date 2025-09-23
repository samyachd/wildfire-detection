import json
import pandas as pd
from pathlib import Path
from typing import Dict, Union, Optional

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
    except IsADirectoryError as e :
        raise ValueError(f"Le fichier {file_path} n'est pas un fichier valide : {e}")
    return data


def load_dataframes(data: dict, name: Optional[str] = None) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Découpe le dictionnaire COCO fourni en plusieurs DataFrames (info, licenses, categories, images, annotations).

    Args:
        data (dict): Dictionnaire issu du JSON COCO.
        name (str, optional): Nom du DataFrame à extraire. 
            Doit être l'une des clés suivantes : "info", "licenses", "categories", "images", "annotations".
            Si None, renvoie un dictionnaire contenant tous les DataFrames.

    Raises:
        ValueError: Si `name` n'est pas une des clés valides.

    Returns:
        Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
            - Si `name` est fourni → le DataFrame correspondant.
            - Sinon → un dictionnaire {nom: DataFrame}.
    """
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


dict = load_json("/home/nabil_simplon/wildfire-detection/data/_annotations.coco.json")
print(type(dict))

data= load_dataframes(dict, 'info')
print(type(data))
