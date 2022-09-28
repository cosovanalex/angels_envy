from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Whiskey, whiskey_schema, whiskeys_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'pour one': 'for me'}


@api.route('/whiskey', methods = ['POST'])
@token_required
def add_whiskey(current_user_token):
    name = request.json['name']
    style = request.json['style']
    region = request.json['region']
    country = request.json['country']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    whiskey = Whiskey(name, style, region, country, user_token = user_token )

    db.session.add(whiskey)
    db.session.commit()

    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('/whiskey', methods = ['GET'])
@token_required
def get_whiskey(current_user_token):
    a_user = current_user_token.token
    whiskeys = Whiskey.query.filter_by(user_token = a_user).all()
    response = whiskeys_schema.dump(whiskeys)
    return jsonify(response)

@api.route('/whiskey/<id>', methods = ['GET'])
@token_required
def get_single_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('/whiskey/<id>', methods = ['POST','PUT'])
@token_required
def update_whiskey(current_user_token,id):
    whiskey = Whiskey.query.get(id) 
    whiskey.name = request.json['name']
    whiskey.style = request.json['style']
    whiskey.region = request.json['region']
    whiskey.country = request.json['country']
    whiskey.user_token = current_user_token.token

    db.session.commit()
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('/whiskey/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    db.session.delete(whiskey)
    db.session.commit()
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)
