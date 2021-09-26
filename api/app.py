import flask
from flask import request, jsonify, abort

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False # Prevent sorting keys to jsonify in current order

MISSING_PERSON_ID_MSG = 'The person you have requested does not exist, refer to README.md for examples'
FRIEND_FIELD_MISSING_MSG = 'Please provide friend field, refer to README.md for examples'
FRIEND_EXISTS_MSG = 'Friend already in network, refer to README.md for examples'
FRIEND_MISSING_MSG = 'Friend does not exist to remove, refer to README.md for examples'

# Initialise test data for my friend network
# Assume duplicate entries will not be in initial data 
relationships = ["Bob knows Alice", "Alice knows Fred", "Fred knows Ganesh"]

# Sample network structure.
#
#  "network": [
#    {
#      "id": 1,
#      "name": "Bob",
#      "friends": [
#        "Alice"
#      ]
#    },
#    {
#      "id": 2,
#      "name": "Alice",
#      "friends": [
#        "Bob",
#        "Fred"
#      ]
#    },
#  ]

# Main array of dictionarys holding person items, example above
network = [] 

# Seperate dictionary to track names we have seen and ids for quicker lookup
name_ids = {} 

# Function to get person record from network given the id
def get_person_item(id):
    return [person for person in network if person['id'] == id]

# Function to add person pair to network data structure
def add_relationship(person1,person2):

    # If person1 in name_ids dictionary append to friends array
    if person1 in name_ids:
        person_id = name_ids[person1]
        person_item = get_person_item(person_id)
        person_item[0]['friends'].append(person2)
    # Otherwise create person entry and add to network
    else:
        id = len(network) + 1
        name_ids[person1] = id
        entry = {'id': id, 'name': person1, 'friends': [person2]}
        network.append(entry)

# Function to create network data structure based on relationships array
def create_network(relationships):

    # Iterate through inital relationships array and parse
    for pair in relationships:
        pair_arr = pair.split(" knows ")

        # Create relationship both ways
        add_relationship(pair_arr[0],pair_arr[1])
        add_relationship(pair_arr[1],pair_arr[0])

@app.errorhandler(400)
def custom_400(error):
    response = jsonify({'status':400, 'message': error.description})
    response.status_code = 400
    return response

@app.errorhandler(404)
def custom_404(error):
    response = jsonify({'status':404, 'message': error.description})
    response.status_code = 404
    return response

@app.errorhandler(409)
def custom_409(error):
    response = jsonify({'status':409, 'message': error.description})
    response.status_code = 409
    return response

# Index route
@app.route('/', methods=['GET'])
def home():
    return "<h1>Friend network API</h1><p>This site is a prototype API for adding friends, removing friends and listing friends of friends. Refer to README.md for documentation.</p>"

# A route to return all of the available entries in our network.
@app.route('/api/v1/resources/network', methods=['GET'])
def api_all():
    return jsonify({'network': network}), 200

# A route to add a friend relationship to our network given an id and a friend.
@app.route('/api/v1/resources/network/<int:id>', methods=['PUT'])
def api_add(id):

    person = get_person_item(id)

    if len(person) == 0:
        abort(404, MISSING_PERSON_ID_MSG)
        
    # Validate JSON payload contains expected field
    if 'friend' in request.json:
        friend = request.json['friend']
    else:
        abort(400, FRIEND_FIELD_MISSING_MSG)
    
    # If friend to be added already in network
    if friend in person[0]['friends'] or person[0]['name'] == friend:
        abort(409, FRIEND_EXISTS_MSG)

    # Add relationship both ways to our network
    add_relationship(person[0]['name'],friend)
    add_relationship(friend,person[0]['name'])

    response = {
        'status':200,
        'message':'Requested friend added to person',
    }

    return jsonify(response), 200

# A route to remove a friend relationship from our network given an id and a friend.
@app.route('/api/v1/resources/network/<int:id>', methods=['DELETE'])
def api_remove(id):

    person = get_person_item(id)

    if len(person) == 0:
        abort(404, MISSING_PERSON_ID_MSG)
    
    # Validate JSON payload contains expected field
    if 'friend' in request.json:
        friend = request.json['friend']
    else:
        abort(400, FRIEND_FIELD_MISSING_MSG) 

    # Check if friend exists to remove both ways
    if friend in person[0]['friends']:
        person[0]['friends'].remove(friend) # Remove friend from person

        person2 = get_person_item(name_ids[friend]) # Get id of friend 
        person2[0]['friends'].remove(person[0]['name']) # Remove person from friend
    else:
        abort(404, FRIEND_MISSING_MSG)

    response = {
        'status':200,
        'message':'Requested friend removed from person',
    }

    return jsonify(response), 200

# A route to list friends of friends from our network given an id.
@app.route('/api/v1/resources/network/<int:id>', methods=['GET'])
def api_friendsof(id):
    
    result = [] # Array to hold friends of friends
    person = get_person_item(id)

    if len(person) == 0:
        abort(404, MISSING_PERSON_ID_MSG)

    # Loop through each of their friends then get their friends
    for friend in person[0]['friends']:
        mutual = get_person_item(name_ids[friend])
        # Loop through the mutuals friends and append to result
        for friend_of in mutual[0]['friends']:
            # Ensure we dont add original entry
            if friend_of != person[0]['name']:
                result.append(friend_of)

    friends_of = {person[0]['name']: result}
    
    return jsonify(friends_of), 200

# Create network from initial data
create_network(relationships)

if __name__ == '__main__':
    app.run()
