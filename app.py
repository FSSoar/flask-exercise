from typing import Tuple

from flask import Flask, jsonify, request, Response, abort
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)





# TODO: Implement the rest of the API here!
""" GET and POST
    This function has the ability to insert new user data into the database as well as query for the data. 
	Querying can be done by getting all users or filtering by team. 
	
    :returns one or multiple users 
    """
@app.route("/users", methods=['GET', 'POST'])
def returnUsers():
	print("usersCalled")
	
	
	
	if request.method == 'POST':
		print("POST")
		data = request.get_json()
		keys = data.keys()
		print(keys)
		
		checkKeys(keys, ['name', 'age', 'team']) #throws an error if any criteria is missing 
		
		db.create('users', data)		
		status = {"status": 201 }
		return create_response(status)
		
	else:	
		team = request.args.get('team')
		print(team)
		list = []
		if (team is not None):
			print("readyToQuery")
			for i in db.get('users'):
				if i['team'] == team: 
					print("teamFound")
					list.append(i)


			info = {"users": list}
			return create_response(info)


		else:
			print("Do not query")
			info = {"users": db.get('users')}
			return create_response(info)
		


		
		
		
""" GET, PUT and DELETE
	Allows for access to one user in the database at a time based on id. 
	For all cases a 404 is thrown if ID is not found
	GET: returns one user based on the ID. 
	PUT: updates one user based on ID and returns if successful
	DELETE: deletes teh user from the database and returns a message if the data is successfully delted.
	
    :param id <int> 
    :returns a single user tuple 
    """
@app.route("/users/<id>", methods=["GET", "PUT", "DELETE"])
def returnUserByID(id):
	
	results = {"user": db.getById('users',int(id)) }

	if results['user'] is None:
		return abort(404, "ID not found")
		
		
	if request.method == 'PUT':
		data = request.get_json()
		keys = data.keys()
		print(data)
		db.updateById('users',int(id), data)
		return create_response({"status" : 201 })		
	elif request.method == 'DELETE': 
		db.deleteById('users',int(id))
		return create_response({"message" : "Deletion of Data Successful" })	
	else:
		return create_response(results);



	""" 
	This is a function that checks to see if all keys necessary are input by the user. 
	If all the expected keys are in the keys provided True is returned.
	If one or more keys is missing a 422 error is thrown and all the keys missing are returned as the error message.
    :param keys <string[]> 
	:param expectedValues <string[]> 
    :returns boolean
    """
def checkKeys(keys, expectedValues):
	
		
		
	areMissingKeys = False
	stringOfMissingKeys = ""
	missingKeys = 0
	for value in expectedValues:
		if value in keys:
			print('key found')
		else:
			print(value)
			areMissingKeys = True
			missingKeys += 1
			stringOfMissingKeys += "{}) ".format(missingKeys) + value + " "
			
	if areMissingKeys:
		abort(422, "You are missing the following keys " + stringOfMissingKeys)
		
	return True

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(debug=True)
