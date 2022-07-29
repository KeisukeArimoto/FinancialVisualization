import pandas as pd
import os


def make_element_ids_csv(egg_file_name, work_dir=None):
    work_path = f'{ os.getcwd() if work_dir==None else work_dir }'
    result_file_name = f'element_ids ( { egg_file_name } ).csv'
    df_egg = pd.read_csv(os.path.join(
        work_path, egg_file_name)).drop_duplicates()
    df_egg.loc[:, 'element_id'].drop_duplicates().to_csv(
        os.path.join(work_path, result_file_name))


def make_sample_data_csv(egg_file_name, edinet_code, work_dir=None):
    work_path = f'{ os.getcwd() if work_dir==None else work_dir }'
    result_file_name = f'sample_data ( { egg_file_name } { edinet_code } ).csv'
    df_egg = pd.read_csv(os.path.join(
        work_path, egg_file_name)).drop_duplicates()
    check1 = df_egg[(df_egg['file_nm'].str.contains(edinet_code))]
    if len(check1) > 0:
        check1.to_csv(os.path.join(work_path, result_file_name))
    else:
        print(f'{ edinet_code }のデータはありませんでした')
