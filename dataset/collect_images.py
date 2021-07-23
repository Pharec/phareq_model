'''
    Collect images of websites from a URL list
'''

import argparse
import pandas as pd
from webscreenshot.webscreenshot import take_screenshot

class CI():
    def __init__(self,
                 data_path="online-valid.csv"
                 ):
        self.data_path = data_path
        self._load_urls()

    def _load_urls(self):
        self.urls_df = pd.read_csv(self.data_path)['url']

    def take_screenshots(self, limit=100):
        parser = argparse.ArgumentParser()
        options = parser.parse_args()
        options.workers = 1
        options.single_output_file = False
        options.output_directory = "images"
        options.renderer = "firefox"
        options.renderer_binary = "firefox"
        options.no_xserver = False
        options.no_error_file = True
        options.label = False
        options.timeout = 30
        options.log_level = 1
        options.window_size = "1200,800"

        return take_screenshot(list(self.urls_df[:limit]), options)

if __name__ == "__main__":
    ci = CI()
    limit = int(input("how many of the urls you want screenshots of?"))
    ci.take_screenshots(limit)
