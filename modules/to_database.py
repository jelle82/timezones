# DATABASE

from sqlalchemy import create_engine, text
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

#engine = create_engine('postgresql://testing:testing@localhost/testing', echo=True)
engine = create_engine('sqlite:///foo.db')

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

session = Session()

sql = text('DROP TABLE IF EXISTS cities;')
result = engine.execute(sql)
sql = text('DROP TABLE IF EXISTS timezones;')
result = engine.execute(sql)
sql = text('DROP TABLE IF EXISTS countries;')
result = engine.execute(sql)

cities.to_sql('cities', engine)
timezones.to_sql('timezones', engine)
countries.to_sql('countries', engine)



Base = declarative_base(engine)

#parent

class Country(Base):
    __tablename__ = 'countries'
    #__table_args__ = {'extend_existing': True}
        
    iso = Column('iso',String, primary_key=True)
    geonameid = Column('geonameid',Integer)   
    cities = relationship('City', backref='in_country')
    timezones = relationship('Timezone', backref='in_country')
    country = Column('country',String )
    
    def __repr__(self):
        return "<Country(name='%s', id='%s')>" % (self.country, self.geonameid)


#child

class City(Base):
    __tablename__ = 'cities'
    #__table_args__ = {'extend_existing': True}
    
    
    geonameid = Column('geonameid',Integer, primary_key=True)
    name = Column('name',String)
    country_code = Column('country_code', String, ForeignKey('countries.iso'))
    timezone = Column('timezone', String, ForeignKey('timezones.timezone'))
    
    
    def __repr__(self):
        return "<City(name='%s', id='%s')>" % (self.name, self.geonameid)


#child

class Timezone(Base):
    __tablename__ = 'timezones'
    #__table_args__ = {'extend_existing': True}
    
    
    country_code = Column('country_code', String, ForeignKey('countries.iso'))
    timezone = Column('timezone', String, primary_key=True)
    cities = relationship("City", backref='in_timezone')
    
                      
    #'gmt_offset',  'dst_offset', 'raw_offset'
    
    def __repr__(self):
        return "<Timezone(timezone='%s', country_code='%s')>" % (self.timezone, self.country_code)

