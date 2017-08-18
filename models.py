from app import db

class Country(db.Model):
    __tablename__ = 'countries'
    #__table_args__ = {'extend_existing': True}

    iso = db.Column('countrycode',db.String, primary_key=True)
    geonameid = db.Column('geonameid',db.Integer)
    country = db.Column('countryname',db.String )
    continent = db.Column('continent',db.String )
    continent_name = db.Column('continentname', db.String )
    continent_id = db.Column('continent_id', db.String )
    country_id = db.Column('country_id', db.String )
    currencycode = db.Column('currencycode', db.String )
    languages = db.Column('languages', db.String )
    population = db.Column('population', db.String )
    areainsqkm = db.Column('areainsqkm', db.Float )
    capital = db.Column('capital', db.String )

    cities = db.relationship('City', backref='in_country')
    timezones = db.relationship('Timezone', backref='in_country')

    def __repr__(self):
        return "<Country(name='%s', id='%s')>" % (self.country, self.geonameid)


#child

class City(db.Model):
    __tablename__ = 'cities'
    #__table_args__ = {'extend_existing': True}


    geonameid = db.Column('geonameid',db.Integer, primary_key=True)
    population = db.Column('population',db.Integer)
    name = db.Column('name',db.String)
    asciiname = db.Column('asciiname',db.String)
    country_code = db.Column('country_code', db.String, db.ForeignKey('countries.countrycode'))
    timezone = db.Column('timezone', db.String, db.ForeignKey('timezones.timezone'))
    name_id = db.Column('name_id',db.String)
    alternatenames = db.Column('alternatenames',db.String)
    latitude = db.Column('latitude',db.Float)
    longitude = db.Column('longitude',db.Float)
    elevation = db.Column('elevation',db.Float)

    def __repr__(self):
        return "<City(name='%s', id='%s')>" % (self.name, self.geonameid)


#child

class Timezone(db.Model):
    __tablename__ = 'timezones'
    #__table_args__ = {'extend_existing': True}


    country_code = db.Column('country_code', db.String, db.ForeignKey('countries.countrycode'))
    timezone = db.Column('timezone', db.String, primary_key=True)
    cities = db.relationship("City", backref='in_timezone')
    gmt_offset = db.Column('gmt_offset', db.Float)
    dst_offset = db.Column('dst_offset', db.Float)
    raw_offset = db.Column('raw_offset', db.Float)

    def __repr__(self):
        return "<Timezone(timezone='%s', country_code='%s')>" % (self.timezone, self.country_code)
