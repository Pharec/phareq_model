'''
    Collect images of websites from a URL list
'''

import pandas as pd

class CI():
    def __init__(self,
                 data_path="online-valid.csv"
                 ):
        self.data_path = data_path

    def _load_urls(self):
        self.urls_df = pd.read_csv(self.data_path)


