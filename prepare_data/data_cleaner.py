def rm_no_annots(df1, df2):
    
    """Supprime les éléments non existants de df_series2 dans df_series1

    Returns:
        _type_: Series
    """
    
    list_serie1 = df1["id"].tolist()
    list_serie2 = df2["image_id"].tolist()

    list_diff = [z for z in list_serie1 if z not in list_serie2]
    df1 = df1.drop(index=list_diff)
    df1 = df1.dropna()
    print(f"{list_diff} éléments ont été supprimés")
    return print(df1)


def locate_files(df1, df2):

    list_serie1 = df1["image_id"].tolist()
    list_serie2 = df2["id"].tolist()

    list_diff = [z for z in list_serie2 if z not in list_serie1]

    files_name = df2["file_name"].loc[df2["id"].isin(list_diff)].tolist()

    return files_name