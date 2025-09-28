import pandas as pd
from pathlib import Path
import os

def data_infos(df: pd.DataFrame):
    """
    Affiche et retourne les infos et stats descriptives d'un DataFrame pandas.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("L'argument doit être un pandas.DataFrame")

    print(df.info())
    print(df.describe(include="all"))
    return df.info(), df.describe(include="all")


def files_extension(folder: str) -> set[str]:
    """
    Renvoie les extensions de fichiers contenues dans un dossier.

    Args:
        folder (str): Chemin du dossier (relatif ou absolu)

    Returns:
        set[str]: Ensemble des extensions uniques trouvées dans le dossier
    """
    path = Path(folder)

    if not path.is_dir():
        raise NotADirectoryError(f"{path} n'est pas un dossier valide")

    extensions = {f.suffix for f in path.iterdir() if f.is_file()}
    print(f"{extensions} extensions de fichiers repérées dans le dossier {path}")
    return extensions

def compare_files(folder: str, file_series: pd.Series, exception: str | None = None) -> bool:
    """
    Compare les fichiers contenus dans un dossier avec ceux d'une série pandas.

    Args:
        folder (str): Dossier (relatif ou absolu) contenant les fichiers.
        file_series (pd.Series): Série ou colonne pandas contenant les noms de fichiers à comparer.
        exception (str, optionnel): Nom de fichier à exclure du dossier.

    Returns:
        bool: True si les noms de fichier (après exclusion éventuelle) sont identiques,
              False sinon.
    """
    path = Path(folder)


    if not path.is_dir():
        raise NotADirectoryError(f"{path} n'est pas un dossier valide")

    if not isinstance(file_series, pd.Series):
        raise TypeError("file_series doit être une pandas.Series")


    list_files = [f.name for f in path.iterdir() if f.is_file()]

    if exception and exception in list_files:
        list_files.remove(exception)

    set_folder = set(list_files)
    set_df = set(file_series)

    if set_folder == set_df:
        print("Tous les fichiers correspondent entre le dossier et la série.")
        return True
    else:
        missing_in_df = set_folder - set_df
        missing_in_folder = set_df - set_folder
        print(f"Différences détectées :\n- Dans le dossier mais pas dans df: {missing_in_df}\n- Dans df mais pas dans le dossier: {missing_in_folder}")
        return False
    
def inv_values(df: pd.DataFrame) -> bool:
    """
    Vérifie les champs des valeurs du DataFrame pour les colonnes bbox et area.

    Args:
        df (pd.DataFrame): DataFrame contenant au moins les colonnes 'bbox' et 'area'

    Returns:
        bool: True si toutes les valeurs sont dans les champs possibles, False sinon.
    """

    if "bbox" not in df.columns or "area" not in df.columns:
        raise KeyError("Le DataFrame doit contenir les colonnes 'bbox' et 'area'")

    test_bbox = df["bbox"].apply(lambda x: x[0:4])

    max_x = all(i[0] <= 1200 for i in test_bbox)
    max_y = all(i[1] <= 860 for i in test_bbox)
    max_w = all(i[2] <= 1200 for i in test_bbox)
    max_h = all(i[3] <= 860 for i in test_bbox)

    min_x = all(i[0] >= 0 for i in test_bbox)
    min_y = all(i[1] >= 0 for i in test_bbox)
    min_w = all(i[2] > 0 for i in test_bbox)
    min_h = all(i[3] > 0 for i in test_bbox)

    max_area = df["area"].le(1032000).all()
    min_area = df["area"].gt(0).all()

    all_ok = all([max_x, max_y, max_w, max_h,
                  min_x, min_y, min_w, min_h,
                  max_area, min_area])

    if all_ok:
        print("Toutes les valeurs de bbox et area sont dans les champs de valeurs possibles")
    else:
        print("Au moins une valeur de bbox ou area n'est pas dans le champ des valeurs possibles")

    return all_ok


def ids_check(df_serie1: pd.Series, df_serie2: pd.Series) -> list:
    """
    Renvoie une liste des éléments de df_serie1 qui n'existent pas dans df_serie2.

    Args:
        df_serie1 (pd.Series): Série de référence (éléments à vérifier)
        df_serie2 (pd.Series): Série contenant les éléments existants

    Returns:
        list: Liste des éléments de df_serie1 absents de df_serie2
    """
    if not isinstance(df_serie1, pd.Series):
        raise TypeError("df_serie1 doit être une pandas.Series")
    if not isinstance(df_serie2, pd.Series):
        raise TypeError("df_serie2 doit être une pandas.Series")

    list_serie1 = df_serie1.tolist()
    list_serie2 = df_serie2.tolist()

    list_diff = [z for z in list_serie1 if z not in list_serie2]

    if list_diff:
        print(f"{list_diff} : ces éléments n'existent pas dans {df_serie2.name}")
    else:
        print(f"Tous les éléments de {df_serie1.name} existent dans {df_serie2.name}")

    return list_diff
    
