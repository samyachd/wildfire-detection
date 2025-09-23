
#<-------------------- fonctions  ------------------------>


import pandas as pd

def total_images(df: pd.DataFrame) -> int:
    # Nombre d'images différentes présentes dans ce DataFrame d'annotations
    return df['image_id'].nunique()

def total_annotations(df: pd.DataFrame) -> int:
    # Nombre total d'annotations contenues dans le DataFrame
    return len(df)

def categories(df: pd.DataFrame) -> list:
    # Extraction des catégories uniques
    return df['category'].unique().tolist()

def images_per_category(df: pd.DataFrame) -> pd.Series:
    # Compte des images uniques qui contiennent au moins une annotation dans cette catégorie
    return df.groupby('category')['image_id'].nunique()

def annotations_per_image(df: pd.DataFrame) -> pd.Series:
    # Nombre d'annotations par image
    return df.groupby('image_id').size()

def annotation_stats(df: pd.DataFrame) -> pd.Series:
    # Statistiques descriptives du nombre d'annotations par image
    return annotations_per_image(df).describe()
