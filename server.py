from flask import Flask, request
app = Flask(__name__)
import mysql.connector
import json

# # https://flask-cors.corydolphin.com/en/latest/index.html
# from flask_cors import CORS
# cors = CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="test123*",
    database="pokemonDB"
)

# https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursordict.html
cursor = mydb.cursor(dictionary=True)

@app.route('/api/pokemon', methods=['GET'])
def selectAll():
    select_query = "SELECT * FROM pokemon;"
    cursor.execute(select_query)
    results = cursor.fetchall()
    return json.dumps(results)

@app.route('/api/pokemon/<string:id>', methods=['GET'])
def selectOne(id):
    select_query = "SELECT * FROM pokemon WHERE id = %s;"
    cursor.execute(select_query, (id, ))
    results = cursor.fetchall()
    return json.dumps(results)

@app.route('/api/pokemon', methods=['POST'])
def insertOne():
    data = request.json
    params = {}
    for k in data.keys():
        params[k] = str(data[k])
    cols = list(params.keys())
    vals = tuple(params.values())
    filler = ["%s"] * len(cols)
    insert_query = "INSERT INTO pokemon (" + ", ".join(cols) + ") VALUES (" + ", ".join(filler) + ");"
    cursor.execute(insert_query, vals)
    mydb.commit()
    return json.dumps(params)

@app.route('/api/pokemon/<string:id>', methods=['PUT'])
def updateOne(id):
    data = request.json
    params = {}
    for k in data.keys():
        params[k] = str(data[k])
    cols = list(params.keys())
    vals = tuple(params.values())
    sets = map(lambda c: c + " = %s", cols)
    update_query = "UPDATE pokemon"
    update_query += " SET " + ", ".join(sets)
    update_query += " WHERE id = %s;"
    vals = vals + (id, )
    print(vals)
    cursor.execute(update_query, vals)
    mydb.commit()
    return json.dumps(params)

if __name__ == '__main__':
    app.run()