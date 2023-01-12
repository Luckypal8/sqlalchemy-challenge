# Import Dependencies
import datetime as datetime
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#Create Engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(autoload_with=engine)
#assign to tables
measurement = Base.classes.measurement
station = Base.classes.station
#create session
session = Session(engine)
#import Flask
app = Flask(__name__)


#1 /
@app.route("/")
def welcome():
    """List of all available api routes."""
    return (
    f"<h2>Welcome!</h2><br/>"
    f"Available routes are:<br/>"
    f"<ul><li>Precipitation -/api/v1.0/precipitation</li></ul>"
    f"<ul><li>Stations - /api/v1.0/stations</li></ul>"
    f"<ul><li>Temperature Observations - /api/v1.0/tobs</li></ul>"
    f"<ul><li>Calculated Temperatures (Single Date) - /api/v1.0/start</li></ul>"
    f"<ul><li>Calculated Temperatures (Dual Dates) - /api/v1.0/start/end</li></ul>"
    )

#2 /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all daily precipitation totals for the last year"""
    # Query and summarize daily precipitation across all stations for the last year of available data
    
    start_date = '2016-08-23'
    sel = [measurement.date, 
        func.sum(measurement.prcp)]
    precipitation = session.query(*sel).\
            filter(measurement.date >= start_date).\
            group_by(measurement.date).\
            order_by(measurement.date).all()
   
    session.close()


#3.  /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    results = session.query(station.station).all()
# convert to a list
    stations = list(np.ravel(results))
    return jsonify(stations)


#4. /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Return the temperature observations (tobs) for previous year."""
    # Calculate the date 1 year ago 
    prev_year = datetime.date(2017, 8, 23) - datetime.timedelta(days=365)

    # Query the primary station for all tobs from the last year
    results = session.query(measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= prev_year).all()

    # convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps)

#5 /api/v1.0/temp/<start>
@app.route("/api/v1.0/temp/<start>")

def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

    # Select statement
    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]

   
        # calculate TMIN, TAVG, TMAX for dates greater than start
results = session.query(*sel).\
    filter(measurement.date >= start).all()
    if not end:
    temps = list(np.ravel(results))
    return jsonify(temps)


#6 
@app.route("/api/v1.0/temp/<start>/<end>")
    # calculate TMIN, TAVG, TMAX with start and end

results = session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()
    
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)
