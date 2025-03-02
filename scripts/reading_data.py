#usr/bin/python

import datetime
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

    def get_station_age(self):
        endpoint = 'https://frost.met.no/observations/availableTimeSeries/v0.jsonld'
        parameters = {
            'sources': self.station_name,
        }
        req = requests.get(endpoint, parameters, auth=(self.client_id, ''))
        self.status_code(req)
        jreq = req.json()
        valid_from = jreq['data'][0]['validFrom'][:10]
        if 'ValidTo' in jreq['data'][0]:
            valid_to = jreq['data'][0]['ValidTo'][:10]
        else:
            valid_to = 'Ongoing'
        print(f'The station {self.station_name} has data from {valid_from} to {valid_to}')

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
    
    def get_temperature_daily(self, start_date: str, end_date: str):
        """
        Parameters:
        start_date (str): Start of time period for gathering data in the format 'YYYY-MM-DD'
        end_date (str): End of time period for gathering data in the format 'YYYY-MM-DD'
        """
        endpoint ='https://frost.met.no/observations/v0.jsonld'
        parameters = {
            'sources': self.station_name,
            'elements': 'mean(air_temperature P1D)',
            'referencetime': f'{start_date}/{end_date}',
        }
        req = requests.get(endpoint, parameters, auth=(self.client_id, ''))
        self.status_code(req)
        jreq = req.json()
        temperature = [jreq['data'][i]['observations'][0]['value'] for i in range(len(jreq['data']))]
        dates = [jreq['data'][i]['referenceTime'] for i in range(len(jreq['data']))]
        c_dates = [datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ") for date in dates]
        df = pd.DataFrame({'date': c_dates, 'temperature': temperature})
        return df

if __name__ == '__main__':
    station_name = 'SN90610'
    station_name = 'SN90560'
    client_id = '../ignore_me/client_id.txt'
    client_secret = '../ignore_me/client_secret.txt'
    rd = ReadingData(station_name, client_id, client_secret)
    rd.get_station_age()
    #print(rd.get_station_datatypes())

        

