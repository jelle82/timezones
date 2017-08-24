from flask import render_template, send_from_directory
from app import app, db
from models import Country, City, Timezone
from datetime import datetime, timedelta

@app.route('/')
def index():
    countries = db.session.query(Country).all()

    continents = set([(country.continent_name, country.continent_id) for country in countries])
    #continent_ids = set([ for country in countries])

    return render_template('base.html', continents=continents)

@app.route('/<continent_id>/')
def continent(continent_id):
	countries = db.session.query(Country).filter(Country.continent_id==continent_id).all()

	return render_template('continent.html', countries=countries, continent_id=continent_id)

@app.route('/<continent_id>/<country_id>/')
def country(continent_id,country_id):
	country = db.session.query(Country).filter(Country.country_id==country_id,Country.continent_id==continent_id).one()

	cities = country.cities
	timezones = country.timezones

	return render_template('country.html', country=country, cities=cities, timezones=timezones)

@app.route('/<continent_id>/<country_id>/<city_id>/')
def city(continent_id,country_id,city_id):
    city = db.session.query(City).filter(City.name_id==city_id).first()
    country = city.in_country
    timezone = city.in_timezone
    texts = city_text(city.name, city.population, city.timezone)
    city_tzs = get_featured_cities()

    altnames = city.alternatenames.split(',')

    #print(feat_cities)

    return render_template('city.html', city=city, country=country, timezone=timezone, texts=texts, city_tzs=city_tzs, altnames=altnames)

def city_text(city_name, population, timezone):
    population = "{:,}".format(population).replace(',','.')

    poptxt = ['Het aantal inwoners van '+city_name+ ' bedraagt ' + population + '.','Er wonen en leven ' + population + ' mensen in ' + city_name + '.', city_name + ' heeft ' + population + ' inwoners.', ]
    tztext = ['De tijdzone bepaalt de tijd in '+city_name+'. De tijdzone heet '+timezone+'.','De tijdzone van '+city_name+' is '+timezone+'. Deze zone is bepalend voor de tijd in de plaats.', ]

    poprnd = len(city_name) % len(poptxt)
    tzrnd = len(timezone) % len(tztext)
    return [poptxt[poprnd], tztext[tzrnd]]

def get_featured_cities():
    cities = db.session.query(City).filter(((City.name_id=='paris')&(City.country_code=='FR'))|((City.name_id=='london')&(City.country_code=='GB'))|((City.name_id=='sydney')&(City.country_code=='AU'))|((City.name_id=='new-york-city')&(City.country_code=='US'))|((City.name_id=='buenos-aires')&(City.country_code=='AR'))).all()

    timezones = [ city.in_timezone for city in cities ]
    countries = [ city.in_country for city in cities ]

    city_tzs = zip(cities, timezones, countries)

    return city_tzs

@app.template_filter('local_time')
def local_time_filter(offset):
    return (datetime.utcnow() + timedelta(hours=offset)).strftime('%X')

@app.template_filter('offsets')
def format_offset(fl_num):
    if fl_num.is_integer():
        if fl_num > 0:
            return '+' + str(int(fl_num)) + ' uur'
        else:
            return str(int(fl_num)) + ' uur'
    return str(fl_num) + ' uur'

@app.template_filter('diff_offset')
def diff_offset(fl_num, cc='NL'):
    tz = db.session.query(Timezone).filter(Timezone.country_code==cc).first()
    return fl_num - tz.dst_offset