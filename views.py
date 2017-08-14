from flask import render_template, send_from_directory
from app import app, db
from models import Country, City

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
	
	poptext = population_text(city.name, city.population)
	
	return render_template('city.html', city=city, country=country, poptext=poptext)

def population_text(city_name, population):
	population = "{:,}".format(population).replace(',','.') 			
		
	texts = ['Het aantal inwoners van '+city_name+ ' bedraagt ' + population + '.',
'Met ' + population + ' inwoners is ' + city_name + ' een behoorlijke plaats.', city_name + ' heeft ' + population + ' inwoners.']
	
	rndnum = len(city_name) % len(texts)
	return texts[rndnum]






	
