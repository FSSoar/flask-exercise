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
		


@app.route("/users/<id>", methods=["GET", "PUT"])
def returnUserByID(id):
	
	results = {"person": db.getById('users',int(id)) }

	if results['person'] is None:
		return abort(404, "ID not found")
		
		
		
	if request.method == 'PUT':
		print()
		data = request.get_json()
		keys = data.keys()
		print(data)
		print(db.updateById('users',int(id), data))
		return create_response({"status" : 201 })		
						
		
	else:
		

		return create_response(results);



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

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(debug=True)
