#!/usr/bin/python3
"""handles review route requests"""
from api.v1.views import app_views
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity
from models.user import User
from flask import jsonify, request, abort


@app_views.route('/places/<place_id>/amenities', strict_slashes=False, methods=['GET'])
@app_views.route('/places/<place_id>/amenities/<amenity_id>', strict_slashes=False, methods=['DELETE', 'POST'])
def amenities(place_id=None, amenity_id=None):
    if amenity_id is None:
        place = storage.get(Place, place_id)
        if place is not None:
            return jsonify([amenity.to_dict() for amenity in place.amenities])
        else:
            abort(404)
    else:
        if request.method == 'DELETE':
            place = storage.get(Place, place_id)
            amenity = storage.get(Amenity, amenity_id)
            if place is not None and amenity is not None:
                place.
