from prepare_data.data_explorer import files_extension, compare_files, inv_values, ids_check

def test_files_extension_nofolder():

    folder = ""

    result = files_extension(folder)
    assert len(result) == 0