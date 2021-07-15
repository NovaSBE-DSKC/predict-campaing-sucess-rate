import pycountry
import numpy as np
import pandas as pd
import json
import settings

from dskc import dskc_clean

def reduce_cardinality(data, colname, percentile):
    series = pd.value_counts(data[colname])
    mask = (series/series.sum() * 100).lt(percentile)

    return np.where(data[colname].isin(series[mask].index), 'Others', data[colname])


def get_countries(location):
    location = location.lower().strip()

    if 'moçambique' in location:
        return 'Mozambique'
    elif 'são tomé e príncipe' in location or 'são tomé e principe' in location:
        return 'Sao tome and principe'
    elif 'lisboa' in location:
        return 'Portugal'
    else:
        if ',' in location:
            city = location.split(',')[0].strip()
            location = location.split(',')[1].strip()

        try:
            country = pycountry.countries.lookup(location).name
        except:
            country = 'Others'

        if country == 'Others':
            try:
                country = pycountry.countries.search_fuzzy(location)[0].name
            except:
                try:
                    country = pycountry.countries.search_fuzzy(city)[0].name
                except:
                    country = 'Others'

        return country.capitalize()


def set_countries(df):
  df['COUNTRY'] = None
  df['COUNTRY'] = df.apply(lambda x: get_countries(x['LOCATION']), axis=1)
  df['COUNTRY_REDUCED'] = reduce_cardinality(df, colname='COUNTRY', percentile=0.5)

  countries_list = list(df["COUNTRY_REDUCED"].unique())

  with open(settings.COUNTRIES_LIST_PATH, 'w') as f:
    json.dump(countries_list, f)

  df.drop('COUNTRY', axis=1, inplace=True)
  df = dskc_clean.one_hot_encode(df, "COUNTRY_REDUCED")

  return df
