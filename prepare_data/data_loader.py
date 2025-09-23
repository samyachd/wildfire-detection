import json
from pathlib import Path
import pandas as pd
from typing import Union


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



# def load_json_as_dataframe(data: Union[dict, list]) -> pd.DataFrame:
#     """
#     Convertit un objet JSON (dict ou list de dicts) en DataFrame pandas.

#     Args:
#         data (dict ou list): Données JSON déjà chargées.

#     Returns:
#         pd.DataFrame: Contenu du JSON sous forme de DataFrame.

#     Raises:
#         ValueError: Si le contenu JSON n'est pas compatible avec DataFrame.
#     """
#     if isinstance(data, list):
#         df = pd.DataFrame(data)
#     elif isinstance(data, dict):
#         df = pd.DataFrame([data])
#     else:
#         raise ValueError("Le contenu JSON n'est pas un format compatible avec DataFrame")

#     return df

