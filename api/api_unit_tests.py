import unittest, json, app
from copy import deepcopy

BASE_URL = 'http://127.0.0.1:5000/api/v1/resources/network'
MISSING_ITEM_URL = '{}/5'.format(BASE_URL) # N/A
EXISTING_ITEM_URL = '{}/3'.format(BASE_URL) # Fred 

# All tests are based on the following initial relationships list
# relationships = ["Bob knows Alice", "Alice knows Fred", "Fred knows Ganesh"]

class test_network_api(unittest.TestCase):

    # Function to setup new test data, occurs at the beginning of each test
    def setUp(self):
        self.backup_network = deepcopy(app.network)  # Create a deepcopy
        self.app = app.app.test_client()
        self.app.testing = True

    # Function to test returning all items in the network
    def test_get_all(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['network']), 4)

    # Function to test adding a friend to the network
    def test_add(self):
        payload = {"friend": "Josh"}
        response = self.app.put(EXISTING_ITEM_URL,
                                data=json.dumps(payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())

        # Test friend was added to first person item
        self.assertEqual(data['network'][2]['friends'], ['Alice', 'Ganesh', 'Josh'])

        # Test friend was added to second person item
        self.assertEqual(data['network'][4]['friends'], ['Fred'])
    
    # Function to test errors when adding a friend
    def test_add_error(self):
        # Test cannot add non-existing item
        payload = {"friend": "Josh"}
        response = self.app.put(MISSING_ITEM_URL,
                                data=json.dumps(payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # Test invalid friend field
        payload = {"person": "Josh"}
        response = self.app.put(EXISTING_ITEM_URL,
                                data=json.dumps(payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test same person
        payload = {"friend": "Fred"}
        response = self.app.put(EXISTING_ITEM_URL,
                                data=json.dumps(payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, 409)

        # Test exisiting friend 
        payload = {"friend": "Ganesh"}
        response = self.app.put(EXISTING_ITEM_URL,
                                data=json.dumps(payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, 409)

    # Function to test removal of friend
    def test_remove(self):
        payload = {"friend": "Ganesh"}
        response = self.app.delete(EXISTING_ITEM_URL,
                                data=json.dumps(payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())

        # Test friend was removed from first person item
        self.assertEqual(data['network'][2]['friends'], ['Alice'])

        # Test friend was removed from second person item
        self.assertEqual(data['network'][3]['friends'], [])

    # Function to test errors when removing a friend
    def test_remove_error(self):

        # Test friend that does not exist
        payload = {"friend": "Josh"}
        response = self.app.delete(EXISTING_ITEM_URL,
                                data=json.dumps(payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # Test cannot remove non-existing person
        payload = {"friend": "Josh"}
        response = self.app.delete(MISSING_ITEM_URL,
                                data=json.dumps(payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)

    # Function to test person id thats not available
    def test_item_not_exist(self):
        
        response = self.app.get(MISSING_ITEM_URL)
        self.assertEqual(response.status_code, 404)

    # Function to test friends of friends
    def test_friends_of(self):
        response = self.app.get(EXISTING_ITEM_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {'Fred': ['Bob']})

    # Function to reset state for the next test
    def tearDown(self):
        # reset app.network to initial state
        app.network = self.backup_network

if __name__ == "__main__":
    unittest.main()