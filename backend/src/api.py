import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
import requests

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth, ADMIN_TOKEN

app = Flask(__name__)
setup_db(app)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PATCH,POST,DELETE,OPTIONS')
    return response


'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@ app.route('/drinks')
def retrieve_drinks():
    drinks = Drink.query.all()
    all_drinks = []
    for drink in drinks:
        all_drinks.append(drink.short())
    return jsonify({
        'success': True,
        'drinks': all_drinks
    })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@ app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def retrieve_drinks_detail(payload):
    drinks = Drink.query.all()
    all_drinks = []
    for drink in drinks:
        all_drinks.append(drink.long())
    return jsonify({
        'success': True,
        'drinks': all_drinks
    })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    try:
        body = request.get_json()
        new_title = body.get('title')
        new_recipe = json.dumps(body.get('recipe'))
        drink = Drink(title=new_title, recipe=new_recipe)
        drink.insert()
        new_drinks = [drink.long()]
        return jsonify({
            'success': True,
            'drinks': new_drinks
        })

    except:
        abort(422)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    try:
        drink = Drink.query.filter(
            Drink.id == id).first()
        body = request.get_json()
        new_title = body.get('title')
        new_recipe = json.dumps(body.get('recipe'))
        if new_title:
            drink.title = new_title
        if new_recipe:
            drink.recipe = new_recipe
        drink.update()
        updated_drink = [drink.long()]
        return jsonify({
            'success': True,
            'drinks': updated_drink
        })
    except:
        abort(422)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_question(payload, id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink is None:
        abort(404)
    try:
        drink.delete()
        return jsonify({
            'success': True,
            'delete': id
        })
    except:
        abort(422)

# Get Baristas only for Managers handler


@ app.route('/users/baristas')
@requires_auth('get:barista')
def retrive_baristas(payload):
    try:
        url = 'https://jimmy0.eu.auth0.com/api/v2/users'
        headers = {'Authorization': 'Bearer ' + ADMIN_TOKEN,
                   'Content-Type': 'application/json; charset=utf-8'}
        r = requests.get(url, headers=headers)
        files = r.json()
        users = []
        baristas = []
        for f in files:
            user = {'id': f['user_id'],
                    'nickname': f['nickname'], 'email': f['email'], 'picture': f['picture']}
            users.append(user)
        for user in users:
            url = 'https://jimmy0.eu.auth0.com/api/v2/users/' + \
                user['id']+'/roles'
            headers = {'Authorization': 'Bearer ' + ADMIN_TOKEN,
                       'Content-Type': 'application/json; charset=utf-8'}
            r = requests.get(url, headers=headers)
            files = r.json()

            for file in files:
                if file['name'] == 'Barista':
                    baristas.append(user)
        return jsonify({
            'success': True,
            'users': baristas
        })
    except:
        abort(422)

# Get All Users for Administrator handler


@ app.route('/users')
@requires_auth('get:manager')
def retrive_users(payload):
    try:
        url = 'https://jimmy0.eu.auth0.com/api/v2/users'
        headers = {'Authorization': 'Bearer ' + ADMIN_TOKEN,
                   'Content-Type': 'application/json; charset=utf-8'}
        r = requests.get(url, headers=headers)
        files = r.json()
        users = []
        baristas = []
        for f in files:
            user = {'id': f['user_id'],
                    'nickname': f['nickname'], 'email': f['email'], 'picture': f['picture']}
            users.append(user)
        for user in users:
            url = 'https://jimmy0.eu.auth0.com/api/v2/users/' + \
                user['id']+'/roles'
            headers = {'Authorization': 'Bearer ' + ADMIN_TOKEN,
                       'Content-Type': 'application/json; charset=utf-8'}
            r = requests.get(url, headers=headers)
            files = r.json()
            for file in files:
                if file['name'] == 'Barista' or file['name'] == 'Manager':
                    baristas.append(user)
        return jsonify({
            'success': True,
            'users': baristas
        })

    except:
        abort(422)


# Post New Barista handler

@app.route('/users/baristas', methods=['POST'])
@requires_auth('get:barista')
def create_barista(payload):
    try:
        body = request.get_json()
        nickname = body.get('nickname')
        email = body.get('email')
        password = body.get('password')
        connection = "Username-Password-Authentication"
        url = 'https://jimmy0.eu.auth0.com/api/v2/users'
        headers = {'Authorization': 'Bearer ' + ADMIN_TOKEN,
                   'Content-Type': 'application/json; charset=utf-8'}
        myjson = {"nickname": nickname, "email": email,
                  "connection": "Username-Password-Authentication", "password": password}
        r = requests.post(url, headers=headers, json=myjson)
        files = r.json()
        url2 = 'https://jimmy0.eu.auth0.com/api/v2/users/' + \
            files['user_id']+'/roles'
        rolejson = {"roles": ["rol_pMF8aXbnIy4QBqAT"]}
        r2 = requests.post(url2, headers=headers, json=rolejson)
        return jsonify({
            'success': True,
            'created': files
        })

    except:
        abort(422)


# Post New Manager handler

@app.route('/users', methods=['POST'])
@requires_auth('get:manager')
def create_manager(payload):
    try:
        body = request.get_json()
        nickname = body.get('nickname')
        email = body.get('email')
        password = body.get('password')
        connection = "Username-Password-Authentication"
        url = 'https://jimmy0.eu.auth0.com/api/v2/users'
        headers = {'Authorization': 'Bearer ' + ADMIN_TOKEN,
                   'Content-Type': 'application/json; charset=utf-8'}
        myjson = {"nickname": nickname, "email": email,
                  "connection": "Username-Password-Authentication", "password": password}
        r = requests.post(url, headers=headers, json=myjson)
        files = r.json()
        url2 = 'https://jimmy0.eu.auth0.com/api/v2/users/' + \
            files['user_id']+'/roles'
        rolejson = {"roles": ["rol_VZfz6NWdDLQ0Txhj"]}
        r2 = requests.post(url2, headers=headers, json=rolejson)
        return jsonify({
            'success': True,
            'created': files
        })

    except:
        abort(422)


# Delete User handler

@ app.route('/users/<user_id>', methods=['DELETE'])
@requires_auth('get:barista')
def delete_barista(payload, user_id):
    try:
        url = 'https://jimmy0.eu.auth0.com/api/v2/users/'+user_id
        headers = {'Authorization': 'Bearer ' + ADMIN_TOKEN,
                   'Content-Type': 'application/json; charset=utf-8'}
        r = requests.delete(url, headers=headers)
        return jsonify({
            'success': True,
            'deleted': user_id
        })

    except:
        abort(422)


# Update User handler

@app.route('/users/<user_id>', methods=['PATCH'])
@requires_auth('get:barista')
def update_barista(payload, user_id):
    try:
        body = request.get_json()
        nickname = body.get('nickname')
        email = body.get('email')
        password = body.get('password')
        if nickname:
            url = 'https://jimmy0.eu.auth0.com/api/v2/users/'+user_id
            headers = {'Authorization': 'Bearer ' + ADMIN_TOKEN,
                       'Content-Type': 'application/json; charset=utf-8'}
            myjson = {"nickname": nickname}
            r = requests.patch(url, headers=headers, json=myjson)
            files = r.json()
        if email:
            url = 'https://jimmy0.eu.auth0.com/api/v2/users/'+user_id
            headers = {'Authorization': 'Bearer ' + ADMIN_TOKEN,
                       'Content-Type': 'application/json; charset=utf-8'}
            myjson = {"email": email,
                      "connection": "Username-Password-Authentication"}
            r = requests.patch(url, headers=headers, json=myjson)
            files = r.json()
        if password:
            url = 'https://jimmy0.eu.auth0.com/api/v2/users/'+user_id
            headers = {'Authorization': 'Bearer ' + ADMIN_TOKEN,
                       'Content-Type': 'application/json; charset=utf-8'}
            myjson = {"password": password,
                      "connection": "Username-Password-Authentication"}
            r = requests.patch(url, headers=headers, json=myjson)
            files = r.json()
        return jsonify({
            'success': True,
            'updated': files
        })

    except:
        abort(422)


'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "forbidden"
    }), 403


if __name__ == "__main__":
    app.run(debug=True)
