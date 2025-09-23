import pandas as pd
import os

def data_infos(dataframe):
    
    """Renvoies des informations basique sur les données

    Args:
        dataframe (_type_): Dataframe

    Returns:
        _type_: Dataframes
    """
    try:
        infos = dataframe.info()
        describe = dataframe.describe()
    except TypeError as e:
        raise TypeError(f"Attendu un pd.DataFrame, mais reçu {type(dataframe).__name__}")
    except ValueError as e:
        raise AttributeError(f"Le fichier {dataframe} n'est pas un dataframe valide : {e}")
    return infos, describe

    # if dataframe.empty:
    #     raise ValueError("Le DataFrame ne doit pas être vide")
    # if not isinstance(dataframe, pd.DataFrame):
    #     raise TypeError(f"Attendu un pd.DataFrame, mais reçu {type(dataframe).__name__}")
    # else:
    #     infos = dataframe.info()
    #     describe = dataframe.describe()
    # return infos, describe


def files_extension(folder):
    
    """Renvoie les extensions de fichier contenus dans un dossier

    Args:
        folder (_type_): Dossier

    Returns:
        _type_: Un set qui contient les extensions uniques contenues dans le dossier
    """

    files = os.listdir(str(os.getcwd()) + folder)
    files = [f for f in files if os.path.isfile(os.path.join(str(os.getcwd()) + folder, f))]
    list_ext = [os.path.splitext(f)[1] for f in files]

    return print(set(list_ext), "extensions de fichiers repérées dans le dossier")


def compare_files(file1, file2, exception):

    """Compares les fichiers contenus dans le dossier en argument avec ceux du dataframe en 2nd argument.

    Args:
        _file1_: Dossier relatif où sont contenus les data ("/data/" dans ce cas précis)
        _file2_: Colonne du dataframe où sont contenus les noms des fichiers (df_images["file_name"] dans ce cas précis)

    Returns:
        _type_: Un boolean. True si les noms de fichier et extensions sont les même, false s'il y a une différence.
    """
    path = str(os.getcwd()) + file1

    files = os.listdir(path)
    files = [f for f in files if os.path.isfile(os.path.join(path, f))]
    list_files=[]
    for f in files:
        list_files.append(f)
    list_files.remove(exception) # Si besoin de remove des fichiers de la liste
    df_files = pd.DataFrame(list_files, columns=["file_name"])
    set1 = set(df_files['file_name'])
    set2 = set(file2)

    if set1 == set2:
        return print(f"Les noms de fichier dans {file1} correspondent à la colonne du dataframe {file2.name}")
    else:
        return print("Erreur : Les noms de fichier ne correspondent pas à la colonne du dataframe")
    
    
def inv_values(df):

    """Vérifies les champs des valeurs du df_annotations pour les colonnes bbox et area.

    Args:
        df : Dataframe

    Returns:
        _type_: Booleans et prints
    """
    testmax_x, testmax_y, testmax_w, testmax_h = zip(*[(i[0] <= 1200, i[1] <= 860, i[2] <= 1200, i[3] <= 860) for i in df["bbox"].apply(lambda x: x[0:4])])
    
    testmin_x, testmin_y, testmin_w, testmin_h = zip(*[(i[0] >= 0, i[1] >= 0, i[2] > 0, i[3] > 0) for i in df["bbox"].apply(lambda x: x[0:4])])

    testmax_area = df.loc[(df["area"] >= 1032000)]

    testmin_area = df.loc[(df["area"] <= 0)]

    if zip(testmax_x, testmax_y, testmax_w, testmax_h, testmin_x, testmin_y, testmin_w, testmin_h, testmax_area, testmin_area):
        return print ("Toutes les valeurs de bbox et area sont dans les champs de valeurs possibles")
    else:
        return print("Une valeur de bbox et area n'est pas dans le champ des valeurs possibles")


def ids_check(df_serie1, df_serie2):
    
    """Renvoies une liste des éléments de df1 qui n'existent pas dans df2

    Returns:
        _type_: Liste
    """

    list_serie1 = df_serie1.tolist()
    list_serie2 = df_serie2.tolist()

    list_diff = [z for z in list_serie2 if z not in list_serie1]
    if list_diff:
        return print(f"{list_diff} : ces éléments n'existent pas dans {df_serie1.name}")
    else:
        return print(f"Tout les éléments de {df_serie1.name} existent dans {df_serie2.name}")
    


