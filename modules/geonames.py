import requests
import pandas as pd
from unidecode import unidecode

from sqlalchemy import create_engine

def create_tables(engine, cities, timezones, countries):

	cities.to_sql('cities', engine)
	timezones.to_sql('timezones', engine)
	countries.to_sql('countries', engine)


def get_cities_df():

	#zip_file = '/home/jelle/Python/firstflaskapp/data/cities15000.zip'

	#r = requests.get('http://download.geonames.org/export/dump/cities15000.zip')
	#z = zipfile.ZipFile(io.BytesIO(zip_file))
	#z.extractall()

	filename = 'cities15000.txt'

	cities=pd.read_csv('../' + filename, sep='\t', header=None)

	cities.columns=['geonameid',
	'name',
	'asciiname',
	'alternatenames',
	'latitude',
	'longitude',
	'feature_class',
	'feature_code',
	'country_code',
	'cc2',
	'admin1_code',
	'admin2_code', 
	'admin3_code',
	'admin4_code',
	'population',
	'elevation',
	'dem',
	'timezone',
	'modification_date']

	cities['name_id'] = cities['asciiname'].str.lower().str.replace(r'[ |.|/|,]','-').str.replace(r'[-]+','-')
	return cities


def get_timezones_df():

	filename = 'timeZones.txt'

	r = requests.get('http://download.geonames.org/export/dump/'+filename)

	with open(filename, 'wb') as f:
	    f.write(r.content)

	timezones = pd.read_csv(filename, sep='\t')

	timezones.columns = ['country_code', 'timezone', 'gmt_offset',
	       'dst_offset', 'raw_offset']
	
	return timezones

def get_first_line(filename):
	with open(filename) as search:
		return max([index for index, line in enumerate(search) if line[0] == '#'])

def to_ascii(s):
    return unidecode(s)


def get_countries_df():
    r = requests.get('http://api.geonames.org/countryInfoJSON?lang=nl&username=tulipa')
    countries = pd.DataFrame.from_dict(r.json()['geonames'])   
    countries.columns = [col.lower().replace(' ','_').replace('-','_').replace('#','').replace('(','').replace(')','') for col in countries.columns]
    countries['country_id'] = countries['countryname'].str.lower().str.replace(r'[ |.|/|,]','-').str.replace(r'[-]+','-')
    countries['country_id'] = countries['country_id'].apply( lambda x: to_ascii(x) )

    countries['continent_id'] = countries['continentname'].str.lower()
    countries['continent_id'] = countries['continent_id'].apply( lambda x: to_ascii(x) )
    return countries

if __name__ == "__main__":
	engine = create_engine('sqlite:///../foo5.db')
	create_tables(engine, get_cities_df(), get_timezones_df(), get_countries_df())

