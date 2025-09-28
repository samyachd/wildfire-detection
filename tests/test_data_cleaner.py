from prepare_data.data_cleaner import  rm_no_annots, rm_files, save_json, locate_files, combine_dataframes

def test_rm_files_nofiles():

    file = ""

    result = rm_files(file)
    assert len(result) == 0