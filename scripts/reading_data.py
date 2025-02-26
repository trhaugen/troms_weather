#usr/bin/python

import pandas as pd


class ReadingData:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path, parse_dates=['datetime'])

    def read_csv(self):
        return pd.read_csv(self.file_path)
    
    def station(self, station_name):
        self.station_name = station_name


        
    
    def temperature(self):

