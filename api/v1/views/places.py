#!/usr/bin/python3
"""handles place route requests"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, request, abort


@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=[
    'POST', 'GET'])
@app_views.route('/places/<place_id>', strict_slashes=False, methods=[
    'PUT', 'GET', 'DELETE'])
def places(city_id=None, place_id=None, user_id=None):
    """handles HTTP requests related to cities"""
    if city_id is not None:
        # /cities/<city_id>/places GET method
        if request.method == 'GET':
            city_list = storage.all('City')
            places_list = []
            if city_list is not {}:
                for city in city_list.values():
                    if city.id == city_id:
                        for place in city.places:
                            places_list.append(place.to_dict())
                        return jsonify(places_list)
            abort(404)

        # /cities/<city_id>/places POST method
        if request.method == 'POST':
            new_json = request.get_json(silent=True)
            city = storage.get(City, city_id)
            user = storage.get(User, user_id)
            if city or user is None:
                abort(404)
            if user_id not in new_json:
                abort(400, 'Missing user_id')
            if new_json is None:
                abort(400, 'Not a JSON')
            if 'name' not in new_json:
                abort(400, 'Missing name')
            new_place = Place(**new_json)
            new_place.city_id = city_id
            new_place.save()
            return jsonify(new_place.to_dict()), 201

    else:
        # places/<place_id> GET method
        if request.method == 'GET':
            place = storage.get(Place, place_id)
            if place is not None:
                return jsonify(place.to_dict())
            abort(404)

        # places/<place_id> DELETE method
        if request.method == 'DELETE':
            place = storage.get(Place, place_id)
            if Place is not None:
                place.delete()
                storage.save()
                return jsonify({}), 200
            abort(404)

        # places/<place_id> PUT method
        if request.method == 'PUT':
            place = storage.get(Place, place_id)
            if place is None:
                abort(404)
            new_json = request.get_json(silent=True)
            if new_json is None:
                abort(400, 'Not a JSON')
            for k, v in new_json.items():
                if k not in ['id', 'user_id', 'city_id',
                             'created_at', 'updated_at']:
                    setattr(place, k, v)
            place.save()
            return jsonify(place.to_dict()), 200