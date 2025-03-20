#usr/bin/python

import datetime
import pandas as pd
import requests
import sys

class ReadingData:
    """
    Reads data from the FROST API for a given station. 

    Args:
        station_name (str): The station name.
        client_id (str): The client id for the FROST API.
        client_secret (str): The client secret for the FROST API.
    """
    def __init__(self, station_name: str, client_id: str, client_secret: str):
        self.station_name = station_name
        with open (client_id) as f: self.client_id = f.read().strip()
        with open (client_secret) as f: self.client_secret = f.read().strip()
    
    def status_code(self, r) -> None:
        """
        Checks the status code for the requested data and exists the system if 
        something is wrong. 

        Args:
            r (requests.models.Response): The response object from the request.
        """
        if r.status_code == 200:
            pass
        else:
            print('Error! Returned status code %s' % r.status_code)
            print('Message: %s' % r.json()['error']['message'])
            print('Reason: %s' % r.json()['error']['reason'])
            sys.exit()     

    def get_station_info(self) -> tuple:
        """
        Fetches metadata information for a weather station from the Frost API.

        Returns:
            tuple: A tuple containing:
                - valid_from (str): The start date of the station's validity period (YYYY-MM-DD).
                - valid_to (str): The end date of the station's validity period, or 'Ongoing' if not specified.
                - coordinates (list): The station's geographic coordinates [longitude, latitude, altitude].
                - short_name (str): The short name of the weather station.
        """
        endpoint = 'https://frost.met.no/sources/v0.jsonld'
        parameters = {
            'ids': self.station_name,
        }
        req = requests.get(endpoint, parameters, auth=(self.client_id, ''))
        self.status_code(req)
        jreq = req.json()
        valid_from = jreq['data'][0]['validFrom'][:10]
        if 'ValidTo' in jreq['data'][0]:
            valid_to = jreq['data'][0]['ValidTo'][:10]
        else:
            valid_to = 'Ongoing'
        coordinates = jreq['data'][0]['geometry']['coordinates']
        short_name = jreq['data'][0]['shortName']
        return valid_from, valid_to, coordinates, short_name

    def get_station_datatypes(self, reference_time: str = '2025') -> set:
        """
        Fetches the available observation data types for a given weather station.

        This method queries the Frost API to retrieve all available data types 
        (e.g., temperature, precipitation) that have been recorded at the 
        specified weather station.

        Args:
        reference_time (str, optional): The year for which to check available 
        data types. Defaults to '2025'.

        Returns:
            set: A set containing all available data types (element IDs) for the
            given station.

        """
        endpoint = 'https://frost.met.no/observations/availableTimeSeries/v0.jsonld'
        parameters = {
            'sources': self.station_name,
            'referencetime': reference_time,
        }
        req = requests.get(endpoint, parameters, auth=(self.client_id, ''))
        self.status_code(req)
        jreq = req.json()
        all_datatypes = set([jreq['data'][i]['elementId'] for i in range(len(jreq['data']))])
        return all_datatypes
    
    def get_temperature_daily(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Gets the daily mean air temperature for a given time period from the FROST
        API. Returns a DataFrame with the date and temperature for the given station.

        Args:
        start_date (str): Start of time period for gathering data in the format 'YYYY-MM-DD'
        end_date (str): End of time period for gathering data in the format 'YYYY-MM-DD'

        Returns:
        pd.DataFrame: DataFrame with the date and daily temperature for given timeperiod
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
    
    def get_temperature_yearly(self, start_year:str, end_year:str) -> pd.DataFrame:
        """
        Gets the yearly mean air temperature anomaly for a given time period 
        with respect to the period 1961-1990 from the FROST API. Returns a
        DataFrame with the year and temperature anomaly for the given station.

        Args:
            start_year (str): Start of time period for gathering data in the format 'YYYY'
            end_year (str): End of time period for gathering data in the format 'YYYY'
        
        Returns:
            pd.DataFrame: DataFrame with the year, min, max and mean yearly temperature 
            for given timeperiod.
        """
        endpoint = 'https://frost.met.no/observations/v0.jsonld'
        parameters = {
            'sources': self.station_name,
            'elements': 'mean(air_temperature P1Y), min(air_temperature P1Y), max(air_temperature P1Y)',
            'referencetime': f'{start_year}-01-01/{end_year}-12-31',
        }
        req = requests.get(endpoint, parameters, auth=(self.client_id, ''))
        self.status_code(req)
        jreq = req.json()
        df = pd.DataFrame([{
            'year': datetime.datetime.strptime(entry['referenceTime'], "%Y-%m-%dT%H:%M:%S.%fZ").year,
            'min': next((obs.get('value') for obs in entry['observations'] if obs.get('elementId') == 'min(air_temperature P1Y)'), None),
            'max': next((obs.get('value') for obs in entry['observations'] if obs.get('elementId') == 'max(air_temperature P1Y)'), None),
            'mean': next((obs.get('value') for obs in entry['observations'] if obs.get('elementId') == 'mean(air_temperature P1Y)'), None)
        } for entry in jreq['data']])
        df = df.groupby('year', as_index=False).agg({
            'min': 'min',
            'max': 'max',
            'mean': 'mean'})
        return df
    
    def get_temperature_anomaly(self, start_year:str, end_year:str) -> pd.DataFrame:
        """
        Gets the monthly mean air temperature anomaly for a given time period
        with respect to the period 1961-1990 from the FROST API.
        Args:
            start_year (str): Start of time period for gathering data in the format 'YYYY'
            end_year (str): End of time period for gathering data in the format 'YYYY'
        Returns:
            pd.DataFrame: DataFrame with the year, month and temperature anomaly for given timeperiod.
        """
        endpoint = 'https://frost.met.no/observations/v0.jsonld'
        parameters = {
            'sources': self.station_name,
            'elements': 'mean(air_temperature_anomaly P3M 1961_1990)',
            'referencetime': f'{start_year}-01-01/{end_year}-12-31',
        }
        req = requests.get(endpoint, parameters, auth=(self.client_id, ''))
        self.status_code(req)
        jreq = req.json()
        df = pd.DataFrame([{
            'year': datetime.datetime.strptime(entry['referenceTime'], "%Y-%m-%dT%H:%M:%S.%fZ").year,
            'month': datetime.datetime.strptime(entry['referenceTime'], "%Y-%m-%dT%H:%M:%S.%fZ").month,
            'anomaly': next((obs.get('value') for obs in entry['observations'] 
                             if obs.get('elementId') == 'mean(air_temperature_anomaly P3M 1961_1990)'), None)
        } for entry in jreq['data']])
        df["year_month"] = df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2) 
        return df

class FindingStations:
    def __init__(self, client_id: str, client_secret: str):
        with open (client_id) as f: self.client_id = f.read().strip()
        with open (client_secret) as f: self.client_secret = f.read().strip()

    def status_code(self, r):
        """ 
        Checks the status code for the requested data and exists the system if
        something is wrong.

        Args:
            r (requests.models.Response): The response object from the request.
        """
        if r.status_code == 200:
            pass
        else:
            print('Error! Returned status code %s' % r.status_code)
            print('Message: %s' % r.json()['error']['message'])
            print('Reason: %s' % r.json()['error']['reason'])
            sys.exit()     

    def get_sensors(self, lat: float, lon: float, max_count: int, municipality: str = None) -> list:
        """
        Fetches sensors from the FROST API based on the given latitude and longitude. 
        If municipality is specified, only sensors from that municipality are returned.
        
        Args:
            lat (float): The latitude of the location.
            lon (float): The longitude of the location.
            max_count (int): The maximum number of sensors to return.
            municipality (str): The municipality to filter the sensors by.
            
        Returns:
            list: A list of sensors with the sensor ID and name.
        """
        endpoint = 'https://frost.met.no/sources/v0.jsonld'
        parameters = {
            'ids': 'SN*',
            'types': 'SensorSystem',
            'geometry': f'nearest(POINT({lon} {lat}))',
            'nearestmaxcount': f'{max_count}',
        }
        req = requests.get(endpoint, params=parameters, auth=(self.client_id, ''))
        self.status_code(req)
        jreq = req.json()
        sensors = [
            [sensor['id'], sensor['name']] for sensor in jreq['data']
            if municipality is None or sensor.get('municipality') == municipality
        ]
        return sensors


if __name__ == '__main__':
    station_name = 'SN90560'
    client_id = '../ignore_me/client_id.txt'
    client_secret = '../ignore_me/client_secret.txt'
    rd = ReadingData(station_name, client_id, client_secret)
    print(rd.get_station_info())
    print(rd.get_temperature_anomaly('1920', '2020'))
    #print(rd.get_station_datatypes())

        

