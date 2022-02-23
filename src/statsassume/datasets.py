# ==========================
# Module: Datasets
# Author: Kenneth Leung
# Last Modified: 12 Jan 2022
# ==========================
import pandas as pd


def load_data(dataset_name: str,
              processed: bool = False,
              save_copy: bool = False,
              raw_url: str = 'https://raw.githubusercontent.com/kennethleungty/statsassume/main/datasets/',
              file_ext: str = '.csv'):
    """Loads toy dataset for assumption checks

    Args:
        dataset_name (str): Name of dataset (selected from list of available datasets)
        processed (bool, optional): If True, retrieves the processed data version instead of raw one. Defaults to False.
        save_copy (bool, optional): Save a copy of dataset locally. Defaults to False.
        raw_url (str, optional): URL where datasets are stored. Defaults to 'https://raw.githubusercontent.com/kennethleungty/Logistic-Regression-Assumptions/main/datasets/'.
        file_ext (str, optional): Extension of data file. Defaults to '.csv'.

    Returns:
        pd.DataFrame: Dataframe of the retrieved toy dataset
    """

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
