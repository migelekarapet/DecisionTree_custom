import pandas as pd
import numpy as np
import os
import math
import subprocess

def import_dataset(path = "heart.data", index_col = 13):
    if os.path.exists("titanic\train.csv"):
        print("Dataset: {}\nFound: Locally".format(path))
        try:
            df = pd.read_csv(path, header=0, engine='python', index_col=index_col)
        except IndexError as ind:
            print(ind)
            print("Index provided: {}".format(index_col))
            exit()
        except:
            print("couldn't parse data set...")
            raise
    else:
        print("ds not found.\nyou can download it...")
        try:
            df = pd.read_csv(path)
        except:
            exit("invalid dataset address")

        with open(path, 'w') as ffile:
            print("save ds")
            df.to_csv(ffile)
    return df