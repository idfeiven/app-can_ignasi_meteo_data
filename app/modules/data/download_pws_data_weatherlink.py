'''
This program connects and downloads 
weather station data from Weatherlink
API v2 
'''

import requests
import pandas as pd
from datetime import datetime

# -------------------------------------CONFIG-----------------------------------

URL_BASE = "https://api.weatherlink.com/v2"

cols = ['ts', 'bar_absolute', 'bar_sea_level', 'bar_trend',
       'wind_speed_hi_last_2_min', 'hum', 'wind_dir_at_hi_speed_last_10_min', 'wind_chill',
       'wind_dir_scalar_avg_last_10_min', 'rain_size', 'uv_index',
       'wind_speed_last', 'wet_bulb', 'wind_speed_avg_last_10_min',
       'wind_dir_at_hi_speed_last_2_min', 'wind_dir_last', 'rainfall_daily_mm', 'dew_point',
       'rainfall_last_15_min_mm', 'rain_rate_hi_mm', 'rain_storm_last_end_at', 'rain_storm_mm',
       'wind_dir_scalar_avg_last_2_min', 'heat_index', 'rainfall_last_60_min_mm',
       'rain_storm_start_time', 'rainfall_last_24_hr_mm', 'wind_speed_hi_last_10_min',
       'rainfall_year_mm', 'wind_dir_scalar_avg_last_1_min', 'temp',
       'wind_speed_avg_last_2_min', 'solar_rad', 'rainfall_monthly_mm',
       'rain_storm_last_mm', 'wind_speed_avg_last_1_min', 'rain_rate_last_mm', 'rain_rate_hi_last_15_min_mm']

cols_hist = ['bar_absolute', 'bar_hi_at', 'bar_sea_level', 'bar_lo', 'bar_hi',
       'bar_lo_at', 'wind_speed_avg', 'dew_point_hi_at', 'dew_point_lo_at', 'dew_point_last',       
       'heat_index_hi', 'rain_rate_hi_at', 'temp_hi', 'temp_lo',
       'wind_dir_of_prevail', 'rainfall_mm', 'hum_lo',
       'heat_index_last', 'hum_hi', 'heat_index_hi_at', 'rain_rate_hi_mm',
       'wind_speed_hi', 'temp_last', 'temp_avg', 'hum_last', 
       'wind_speed_hi_at', 'wind_speed_hi_dir', 'temp_lo_at', 'dew_point_hi',
       'dew_point_lo', 'temp_hi_at', 'hum_lo_at', 'hum_hi_at', 'ts']

# ------------------------------------FUNCTIONS---------------------------------

def read_api_keys():
    '''
    Read API v2 keys from the local system
    '''
    api_key = "vy636qzdr3v4n9uospitzgpgcuuqzwi2"
    api_secret = "mublr5cz9rw8tbhym0jzykzwv7w0i5c5"

    return api_key, api_secret


def get_station_ids(api_key, api_secret):
    '''
    Get the station indo IDs shared
    with the user
    '''

    endpoint = "stations"
    url = f"{URL_BASE}/{endpoint}?api-key={api_key}"
    headers = {"X-Api-Secret": api_secret}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print("Successful request")
            json_response = response.json()
            df_stn_ids = pd.DataFrame(json_response["stations"])
            return df_stn_ids

        else:
            print(response.status_code)
            print(response.reason)
            return None
        
    except Exception:
        print("Could not retrieve information")
        return None


def get_current_data(station_name,
                     df_stn_ids,
                     api_key,
                     api_secret):
    '''
    Get current conditions for the selected station
    ID
    '''
    station_id = df_stn_ids[df_stn_ids["station_name"] == station_name]["station_id"].values.flatten()[0]
    endpoint = "current"
    headers = {"X-Api-Secret": api_secret}
    url = f"{URL_BASE}/{endpoint}/{station_id}?api-key={api_key}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Successful request")
            json_response = response.json()
            df_sensors = pd.DataFrame(json_response["sensors"])

            df_data = pd.DataFrame()
            for data in df_sensors["data"]:
                df_sensor = pd.DataFrame(data)
                df_data = pd.concat([df_data, df_sensor], axis = 1)

            # df_data = df_data[cols]
            print(f"Retrieved current data from {station_name}")
            return df_data
        else:
            print(response.status_code)
            print(response.reason)
            return None
        
    except Exception:
        print("Could not retrieve information")
        return None


def _datetime_str_to_unix(datetime_str):
    '''
    Return a UNIX timestamp in seconds
    as an integer. Date must be in format
    YYYY-MM-DD
    '''

    date_format = datetime.strptime(datetime_str,
                                         "%Y-%m-%d")
    unix_time = datetime.timestamp(date_format)

    return int(unix_time)


def get_historic_data(station_name,
                     start_datetime,
                     end_datetime, 
                     df_stn_ids,
                     api_key,
                     api_secret):
    '''
    Get current conditions for the selected station
    ID
    '''
    station_id = df_stn_ids[df_stn_ids["station_name"] == station_name]["station_id"].values.flatten()[0]
    endpoint = "historic"
    headers = {"X-Api-Secret": api_secret}

    start_datetime_unix = _datetime_str_to_unix(start_datetime)
    end_datetime_unix = _datetime_str_to_unix(end_datetime)

    if end_datetime_unix - start_datetime_unix > 86400:
        print("Data requests cannot exceed 1 day!")

    elif end_datetime_unix < start_datetime_unix:
        print("Initial datetime is older than end datetime!")
    
    else:
        # make the request
        url = f"{URL_BASE}/{endpoint}/{station_id}?api-key={api_key}&start-timestamp={start_datetime_unix}&end-timestamp={end_datetime_unix}"

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print("Successful request")
                json_response = response.json()
                df_sensors = pd.DataFrame(json_response["sensors"])

                df_data = pd.DataFrame()
                for data in df_sensors["data"]:
                    df_sensor = pd.DataFrame(data)
                    df_data = pd.concat([df_data, df_sensor], axis = 1)

                # df_data = df_data[cols]
                print(f"Retrieved current data from {station_name}")
                return df_data
            else:
                print(response.status_code)
                print(response.reason)
                return None
            
        except Exception:
            print("Could not retrieve information")
            return None


def _filter_cols_current_data(df_data):
    df_data = df_data.loc[:,~df_data.columns.duplicated(keep = "last")].copy()
    df_data = df_data[cols]

    return df_data


def _filter_cols_historic_data(df_data):
    df_nowind_data = df_data.loc[:,~df_data.columns.duplicated(keep = "last")].copy()
    df_wind_data = df_data.loc[:,~df_data.columns.duplicated(keep = "first")].copy()
    df_data = pd.concat([df_wind_data, df_nowind_data], axis = 1)
    df_data = df_data.dropna(axis = 1, how = "all")
    df_data = df_data.loc[:,~df_data.columns.duplicated(keep = "first")].copy()
    df_data = df_data[cols_hist]

    return df_data


def _unix_to_datetime(df_data):

    df_data = df_data.copy()
    df_data["ts"] = pd.to_datetime(df_data["ts"], unit = "s", origin = "unix")

    return df_data


def _in_to_hPa(pressure_in):
    return pressure_in * 33.863889532611


def _fahrenheit_to_celsius(temp_fahr):
    return (temp_fahr - 32.) * 5/9


def _mph_to_kmh(speed_mph):
    return speed_mph * 1.60934


def parse_current_data(df_data):
    df_data = _filter_cols_current_data(df_data)
    df_data = _unix_to_datetime(df_data)

    # convert pressure from inches to hPa
    cols_pres = [column for column in df_data.columns if column.startswith('bar')]
    df_data[cols_pres] = df_data[cols_pres].apply(_in_to_hPa).round(1)

    # convert temperature fahrenheit to celsius
    cols_temp = ["temp", "wind_chill", "wet_bulb", "dew_point", "heat_index"]
    df_data[cols_temp] = df_data[cols_temp].apply(_fahrenheit_to_celsius).round(1)

    # convert wind speed data from mph to kmh
    cols_wind = [column for column in df_data.columns if column.startswith('wind_speed')]
    df_data[cols_wind] = df_data[cols_wind].apply(_mph_to_kmh).round(1)

    return df_data


def parse_historic_data(df_data):
    df_data = _filter_cols_historic_data(df_data)
    df_data = _unix_to_datetime(df_data)

    # convert times at maximum and minimum values to datetime
    df_times = df_data.loc[:, df_data.columns.str.contains("_at")].apply(pd.to_datetime, unit = "s", origin = "unix")
    df_data[df_times.columns] = df_times

    # convert pressure from inches to hPa
    cols_pres = ['bar_absolute', 'bar_sea_level', 'bar_lo', 'bar_hi']
    df_data[cols_pres] = df_data[cols_pres].apply(_in_to_hPa).round(1)

    # convert temperature fahrenheit to celsius
    cols_temp = ['dew_point_last', 'heat_index_hi', 
                 'temp_hi', 'temp_lo', 'heat_index_last', 'temp_last',
                 'temp_avg', 'dew_point_hi', 'dew_point_lo']
    df_data[cols_temp] = df_data[cols_temp].apply(_fahrenheit_to_celsius).round(1)

    # convert wind speed data from mph to kmh
    cols_wind = ['wind_speed_avg', 'wind_speed_hi']
    df_data[cols_wind] = df_data[cols_wind].apply(_mph_to_kmh).round(1)

    return df_data


# -----------------------------------MAIN PROGRAM----------------------------------------

def download_data(station_name, start_datetime, end_datetime, historic = False):
    '''
    Main method for download_pws_data_weatherlink.py
    '''
    api_key, api_secret = read_api_keys()

    df_stn_ids = get_station_ids(api_key, api_secret)

    if historic == False:
        # download current data
        df_data = get_current_data(station_name,
                                df_stn_ids,
                                api_key,
                                api_secret)

        if df_data.empty:
            print("No data to parse!")
            return None
        else:    
            data_parsed = parse_current_data(df_data) 
            return data_parsed
        
    else:
        # download historic data
        df_data = get_historic_data(station_name,
                                    start_datetime,
                                    end_datetime,
                                    df_stn_ids,
                                    api_key,
                                    api_secret)

        if df_data.empty:
            print("No data to parse!")
            return None
        else:    
            data_parsed = parse_historic_data(df_data) 
            return data_parsed
