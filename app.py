import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


#Precipitation Path

@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)   

    date = dt.datetime(2016, 8, 23)

    last_year = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date>date).\
        order_by(Measurement.date.asc()).all()

    for date, prcp in last_year:
        last_year_dict = {}
        last_year_dict ={date: prcp}
        return jsonify(last_year_dict)
    

#Change list of tuples (date, perceip) to list of dictionaries where the key = date. Value = precip
# Do in jupyter notebook first

#Stations Path

@app.route("/api/v1.0/stations")
def stat():
    session = Session(engine)
#TOBS path
    station_group = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()

    return jsonify(station_group)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    date = dt.datetime(2016, 8, 23)

    top_station_year = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date>date).\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.tobs.asc()).all()
    
    return jsonify(top_station_year)

@app.route("/api/v1.0/start")
def calc_temps(start_date, end_date):

    session = Session(engine)

    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()


if __name__ == '__main__':
    app.run(debug=True)