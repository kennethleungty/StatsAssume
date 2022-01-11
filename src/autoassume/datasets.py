# ==========================
# Module: Datasets
# Author: Kenneth Leung
# Last Modified: 07 Jan 2022
# ==========================
import pandas as pd


def load_data(dataset_name: str,
              processed: bool = False,
              save_copy: bool = False,
              raw_url: str = 'https://raw.githubusercontent.com/kennethleungty/Logistic-Regression-Assumptions/main/datasets/',
              file_ext: str = '.csv'):

    if processed:
        try:
            filename = dataset_name + '_processed'
            data = pd.read_csv(raw_url + filename + file_ext)
        except Exception:
            pass
        else:
            filename = dataset_name
            data = pd.read_csv(raw_url + dataset_name + file_ext)
    else:
        filename = dataset_name
        data = pd.read_csv(raw_url + filename + file_ext)

    if save_copy:
        data.to_csv(filename, index=False)

    return data
