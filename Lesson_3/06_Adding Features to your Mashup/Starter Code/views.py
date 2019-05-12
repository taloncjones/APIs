from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

import mysecrets
google_api_key = mysecrets.google_api_key
foursquare_client_id = mysecrets.foursquare_client_id
foursquare_client_secret = mysecrets.foursquare_client_secret


engine = create_engine('sqlite:///restaurants.db', connect_args={'check_same_thread': False})

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
  #YOUR CODE HERE
    if request.method == 'GET':
        restaurants = session.query(Restaurant).all()
        return jsonify(restaurants = [i.serialize for i in restaurants])
    elif request.method == 'POST':
        location = request.args.get('location', '')
        mealType = request.args.get('mealType', '')
        restaurant_info = findARestaurant(mealType, location)
        if restaurant_info != "No Restaurants Found":
            restaurant = Restaurant(restaurant_name = unicode(restaurant_info['name']), restaurant_address = unicode(restaurant_info['address']), restaurant_image = restaurant_info['image'])
            session.add(restaurant)
            session.commit()
            return jsonify(restaurant = restaurant.serialize)
        else:
            return jsonify({"error":"No Restaurants Found for %s in %s" % (mealType, location)})

@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
  #YOUR CODE HERE
    restaurant = session.query(Restaurant).filter_by(id = id).one()
    if request.method == 'GET':
        return jsonify(restaurant = restaurant.serialize)
    elif request.method == 'PUT':
        name = request.args.get('name')
        address = request.args.get('address')
        image = request.args.get('image')
        if name:
            restaurant.restaurant_name = name
        if address:
            restaurant.restaurant_address = address
        if image:
            restaurant.restaurant_image = image
        session.commit()
        return jsonify(restaurant = restaurant.serialize)
    else:
        return

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


  
