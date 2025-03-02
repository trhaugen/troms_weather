#usr/bin/python

import pandas as pd
import requests
import sys

class ReadingData:
    def __init__(self, station_name, client_id, client_secret):
        self.station_name = station_name
        with open (client_id) as f: self.client_id = f.read().strip()
        with open (client_secret) as f: self.client_secret = f.read().strip()

    def read_csv(self):
        return pd.read_csv(self.file_path)
    
    def status_code(self, r):
        if r.status_code == 200:
            print('Success!')
        else:
            print('Error! Returned status code %s' % r.status_code)
            print('Message: %s' % r.json()['error']['message'])
            print('Reason: %s' % r.json()['error']['reason'])
            sys.exit()     

    def get_station_datatypes(self):
        endpoint = 'https://frost.met.no/observations/availableTimeSeries/v0.jsonld'
        parameters = {
            'sources': self.station_name,
        }
        req = requests.get(endpoint, parameters, auth=(self.client_id, ''))
        self.status_code(req)
        jreq = req.json()
        all_datatypes = set([jreq['data'][i]['elementId'] for i in range(len(jreq['data']))])
        return all_datatypes
    

if __name__ == '__main__':
    station_name = 'SN18700'
    client_id = '../ignore_me/client_id.txt'
    client_secret = '../ignore_me/client_secret.txt'
    rd = ReadingData(station_name, client_id, client_secret)
    print(rd.get_station_datatypes())

        

