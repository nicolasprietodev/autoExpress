import pandas as pd 
def load_files(file_paths):
    dataframes = [pd.read_excel(file) for file in file_paths]
    combinedata = pd.concat(dataframes, ignore_index=True) 
    return combinedata