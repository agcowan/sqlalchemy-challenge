import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

app = Flask(__name__)

#################################################
# Database setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect=True)

# References to tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Routes
#################################################
# Home
@app.route("/")
def Home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f'<a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a><br/>'
        f'<a href="/api/v1.0/stations">/api/v1.0/stations</a><br/>'
        f'<a href="/api/v1.0/tobs">/api/v1.0/tobs</a><br/>'
        f'<a href="/api/v1.0/&lt;start&gt;">/api/v1.0/&lt;start&gt;</a> Use date in YYYY-MM-DD format<br/>' # remind user to put date as YYYY-MM-DD
        f'<a href="/api/v1.0/&lt;start&gt;/&lt;end&gt;">/api/v1.0/&lt;start&gt;/&lt;end&gt;</a> Use date in YYYY-MM-DD format'
    )

# Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # create session
    session = Session(engine)
    results = session.query(Measurement.date,Measurement.prcp).all()
    # close session
    session.close()
    all_precip = []

    for date,prcp in results:
        date_dict = {}
        date_dict["date"] = date
        date_dict["prcp"] = prcp
        all_precip.append(date_dict)

    return jsonify(all_precip)

# Stations
@app.route("/api/v1.0/stations")
def stations():
     # create session
    session = Session(engine)
    locations = session.query(Station.station).all()
    # close session
    session.close()
    stations = list(np.ravel(locations))
    return jsonify(stations)

# Temperature observations
@app.route("/api/v1.0/tobs")
def tobs():
    # create session
    session = Session(engine)
    last_year = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.date>='2016-08-23').\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date).all()
    # close session
    session.close()
    temps = list(np.ravel(last_year))
    return jsonify(temps)

# Search all dates from input start date until end
@app.route("/api/v1.0/<start>")
def aggregate1(start):
    # create session
    session = Session(engine)
    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date>start).all()
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date>start).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date>start).all()
    # close session
    session.close()
    return jsonify(f'Min: {min_temp[0][0]}, Max: {max_temp[0][0]}, Average: {round(avg_temp[0][0],2)}')

# Search all dates from input start date until input end date
@app.route("/api/v1.0/<start>/<end>")
def aggregate2(start,end):
    # create session
    session = Session(engine)
    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date>start).filter(Measurement.date<end).all()
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date>start).filter(Measurement.date<end).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date>start).filter(Measurement.date<end).all()
    # close session
    session.close()
    return jsonify(f'Min: {min_temp[0][0]}, Max: {max_temp[0][0]}, Average: {round(avg_temp[0][0],2)}')

# Boilerplate
if __name__ == '__main__':
    app.run(debug=True)