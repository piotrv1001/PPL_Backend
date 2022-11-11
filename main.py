import mysql.connector
from flask import Flask
from flask_restful import Api, Resource
from flask import request
from flask import abort
# from flask import jsonify
from user import User
from category import Category
import jsonpickle

def getConnection():
    return mysql.connector.connect(
        user = 'ppl-admin',
        password = 'PPL-password-123',
        host = '127.0.0.1',
        database = 'ppl-project',
        auth_plugin = 'mysql_native_password'
    )

app = Flask(__name__)
api = Api(app)

@app.route('/user', methods = ['GET'])
def getUsers():
    users = []
    connection = getConnection()
    cursor = connection.cursor(dictionary = True)
    query = 'SELECT * FROM User;'
    cursor.execute(query)

    for row in cursor:
        currentUser = User(
            userId = row['userId'],
            email = row['email'],
            password = row['password'],
            address = row['address'],
            name = row['name'],
            phoneNumber = row['phoneNumber'],
            isAdmin = row['isAdmin']
        )
        users.append(currentUser)

    connection.close()

    return jsonpickle.encode(users, unpicklable = False)


@app.route('/register', methods = ['POST'])
def register():
    requestData = request.get_json()
    connection = getConnection()
    cursor = connection.cursor()
    query = 'INSERT INTO User(email, password, name, address, phoneNumber, isAdmin) VALUES (%(email)s, %(password)s, %(name)s, %(address)s, %(phoneNumber)s, %(isAdmin)s);'
    cursor.execute(query, requestData)
    connection.commit()
    connection.close()

    return requestData, 201


@app.route('/login', methods = ['POST'])
def login():
    email = request.args.get('email', '')
    password = request.args.get('password', '')
    if email == '' or password == '':
        # 400 - Bad Request
        abort(400)
    
    connection = getConnection()
    cursor = connection.cursor()
    query = 'SELECT * FROM User WHERE email=%s AND password=%s;'
    cursor.execute(query, (email, password))
    result = cursor.fetchall()
    if len(result) == 0:
        connection.close()
        # 404 - Not Found
        abort(404)

    connection.close()
    return ('', 200)


@app.route('/user/<int:userId>', methods = ['GET'])
def getUserById(userId):
    connection = getConnection()
    cursor = connection.cursor(dictionary = True)
    query = "SELECT * FROM User WHERE userId=%s;"
    cursor.execute(query, (userId,))
    result = cursor.fetchall()
    if len(result) == 0:
        connection.close()
        # 404 - Not Found
        abort(404)
    
    user = None
    row = result[0]
    user = User(
        userId = row['userId'],
        email = row['email'],
        password = row['password'],
        address = row['address'],
        name = row['name'],
        phoneNumber = row['phoneNumber'],
        isAdmin = row['isAdmin']
    )

    return jsonpickle.encode(user, unpicklable = False)


@app.route('/category', methods = ['GET'])
def getCategories():
    categories = []
    connection = getConnection()
    cursor = connection.cursor(dictionary = True)
    query = 'SELECT * FROM Category;'
    cursor.execute(query)

    for row in cursor:
        currentCategory = Category(
            name = row['name']
        )
        categories.append(currentCategory)

    connection.close()

    return jsonpickle.encode(categories, unpicklable = False)


@app.route('/category', methods = 'POST')
def addCategory():
    requestData = request.get_json()
    connection = getConnection()
    cursor = connection.cursor()
    query = 'INSERT INTO Category(name) VALUES (%(name)s)'
    cursor.execute(query, requestData)
    connection.commit()
    connection.close()

    return requestData, 201


@app.route('/category/<int:categoryId>', methods = 'DELETE')
def deleteCategoryById(categoryId):
    connection = getConnection()
    cursor = connection.cursor()
    query = 'DELETE FROM Category WHERE categoryId=%s;'
    cursor.execute(query, (categoryId,))
    connection.commit()
    connection.close()

    return '', 200


if __name__ == '__main__':
    app.run(debug = True, port = 5000)