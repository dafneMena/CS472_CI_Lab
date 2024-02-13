from flask import Flask
# we need to import the file that contains the status codes
from src import status

app = Flask(__name__)
COUNTERS = {}


# We will use the app decorator and create a route called slash counters.
# specify the variable in route <name>
# let Flask know that the only methods that is allowed to called
# on this function is "POST".
@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    app.logger.info(f"Request to create counter: {name}")
    global COUNTERS
    if name in COUNTERS:
        return {"Message": f"Counter {name} already exists"}, status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return {name: COUNTERS[name]}, status.HTTP_201_CREATED


@app.route('/counters/<name>', methods=['PUT'])
def update_counter(name):
    # Create a route for method PUT on endpoint /counters/<name>.
    app.logger.info(f"Request to update counter: {name}")
    global COUNTERS
    if name not in COUNTERS:
        return {"Message": f"Counter {name} does not exists"}, status.HTTP_409_CONFLICT
    # Increment the counter by 1.
    COUNTERS[name] = COUNTERS[name] + 1
    # Return the new counter and a 200_OK return code.
    return {name: COUNTERS[name]}, status.HTTP_200_OK


@app.route('/counters/<name>', methods=['GET'])
def read_counter(name):
    # Create a route for method GET on endpoint /counters/<name>.
    app.logger.info(f"Request to read counter: {name}")
    global COUNTERS
    # Checks the name is not in counters
    if name not in COUNTERS:
        return {"Message": f"Counter {name} does not exists"}, status.HTTP_409_CONFLICT

    # Return the counter and a 200_OK return code.
    return {"Count": f"{COUNTERS[name]}"}, status.HTTP_200_OK


@app.route('/counters/<name>', methods=['DELETE'])
def delete_counter(name):
    # Create a route for method DELETE on endpoint /counters/<name>.
    app.logger.info(f"Request to delete counter: {name}")
    global COUNTERS

    # Delete the counter
    del COUNTERS[name]

    # Return empty and a 204 no content code.
    return "", status.HTTP_204_NO_CONTENT
