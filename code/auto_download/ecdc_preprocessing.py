import os
import glob
import pandas as pd

def preprocess_by_country(country_names=['Germany'], fips_codes=['GM']):
                                         
    # Get latest file
    list_of_files = glob.glob('../../data-truth/ECDC/raw/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    
    # contains data from all countries
    df_all = pd.read_csv(latest_file)

    df_all['date'] = pd.to_datetime(df_all.dateRep, dayfirst=True)
    
    
    for country, code in zip(country_names, fips_codes):
        print('Extracting data for {}.'.format(country))
        
        # select one country
        df = df_all[df_all.countriesAndTerritories == country].copy()
        
        # adjust data format and naming
        df.rename(columns={'countriesAndTerritories' : 'location_name', 'deaths' : 'value', }, inplace=True)
        df['location'] = code
        df = df[['date', 'location', 'location_name', 'value']].sort_values('date').reset_index(drop=True)
        
        # export incident deaths
        df.to_csv('../../data-truth/ECDC/truth_ECDC-Incident Deaths_{}.csv'.format(country), index=False)

        # compute cumulative deaths
        df.value = df.value.cumsum()
        
        # export cumulative deaths
        df.to_csv('../../data-truth/ECDC/truth_ECDC-Cumulative Deaths_{}.csv'.format(country), index=False)
        
preprocess_by_country(['Germany', 'Poland'], ['GM', 'PL'])
