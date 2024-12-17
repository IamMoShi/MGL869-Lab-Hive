import os
import pandas as pd


def is_a_patch(file: str) -> bool:
    return not file.endswith(".0_static_metrics.csv")


def load_data(directory: str):
    data_dict = {}
    liste = ['CCViolDensityLine', 'CCViolDensityCode', 'RatioCommentToCode']

    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            if is_a_patch(filename):
                # Delete the file
                os.remove(os.path.join(directory, filename))
            else:
                file_path = os.path.join(directory, filename)
                data = pd.read_csv(file_path)
                for elm in liste:
                    data[elm] = data[elm].str.replace(',', '.').astype(float)
                data_dict[filename] = data

    return data_dict
