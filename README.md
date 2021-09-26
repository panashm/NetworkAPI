# NetworkAPI
API for "New Friend Network”, built with Python (3.7.4) and Flask (2.0.1)

Given a list of relationships: “Bob knows Alice”, “Alice knows Fred”, “Fred knows Ganesh”. 

Design an API to include:
- Adding friends
- Removing friends
- Listing Friends of friends. eg Bob  “friend of a friend”  is [“Fred”]

## Assumptions

- No duplicate entries in initial list
- Names are case sensitive
- If Bob knows Alice, this implies Alice knows Bob

## ⚙ Setup

Setup virtualenv (optional)

### Install Relevant python packages

    pip install -r requirements.txt

### To Run development server

    python app.py

### To Run unit tests

    python api_unit_tests.py


## Endpoints, Methods and Parameters

### Get all people in network 

**GET**  http://127.0.0.1:5000/api/v1/resources/network

### Add friend to person in network

**PUT** http://127.0.0.1:5000/api/v1/resources/network/{personId}

- #### Path parameters

  | Parameters | Description |
  |---------------------------|-------------|
  | personID (int) | The ID of the person to add a friend to. |

- #### Request body (JSON)

  ```JSON
  {
    "friend": string,
  }
  ```

### Remove friend from a person in network 

**DELETE**  http://127.0.0.1:5000/api/v1/resources/network/{personId}

- #### Path parameters

  | Parameters | Description |
  |---------------------------|-------------|
  | personID (int) | The ID of the person to add a friend to. |

- #### Request body (JSON)

  ```JSON
  {
    "friend": string,
  }
  ```

### Get friends of friends of person in network

GET  http://127.0.0.1:5000/api/v1/resources/network/{personId}

- #### Path parameters

  | Parameters | Description |
  |---------------------------|-------------|
  | personID (int) | The ID of the person to add a friend to. |


## Examples

### Get all people in network

````Bash
curl http://127.0.0.1:5000/api/v1/resources/network
````

Response
````Bash
{
  "network": [
    {
      "id": 1,
      "name": "Bob",
      "friends": [
        "Alice"
      ]
    },
    {
      "id": 2,
      "name": "Alice",
      "friends": [
        "Bob",
        "Fred"
      ]
    },
    ...
   ]
}

````

### Add friend (Karl) to person (Fred) in network
````Bash
curl -X PUT -H "Content-Type: application/json" -d "{\"friend\":\"Karl\"}" http://localhost:5000/api/v1/resources/network/3
````

Response
````Bash
{
  "status": 200,
  "message": "Requested friend added to person"
}
````

### Remove friend (Karl) from person (Fred) in network
````Bash
curl -X DELETE -H "Content-Type: application/json" -d "{\"friend\":\"Karl\"}" http://localhost:5000/api/v1/resources/network/3
````

Response
````Bash
{
  "status": 200,
  "message": "Requested friend removed from person"
}
````

### List friends of friends for Bob
````Bash
curl http://127.0.0.1:5000/api/v1/resources/network/1
````

Response
````Bash
{
  "Bob": [
    "Fred"
  ]
}
````

## Troubleshooting

If on windows double quotes for curl need to be escaped - https://mkyong.com/web/curl-post-json-data-on-windows/
