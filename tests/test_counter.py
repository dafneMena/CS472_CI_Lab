"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status

class CounterTest(TestCase):
    """Counter tests"""
    def setUp(self):
        self.client = app.test_client()
    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        # Make a call to Create a counter.
        result = self.client.post('/counters/daf')

        # Ensure that it returned a successful return code.
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        # Check the counter value as a baseline.
        baseline = result.json['daf']
        self.assertEqual(baseline, 0)

        # Make a call to Update the counter that you just created.
        updatecounter = self.client.put('/counters/daf')

        # Ensure that it returned a successful return code.
        self.assertEqual(updatecounter.status_code, status.HTTP_200_OK)

        # Check that the counter value is one more than the baseline you measured in step 3
        self.assertEqual(updatecounter.json['daf'], baseline + 1)

        # Completes the coverage. Tests for a name not in counter
        testPut = self.client.put('/counters/tati')
        self.assertEqual(testPut.status_code, status.HTTP_409_CONFLICT)

    def test_readCounter(self):
        """It should read a counter"""
        # Makes a counter
        result = self.client.post('/counters/nom')

        # Ensure that it returned a successful return code.
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        # Gets the value of counter
        getResult = self.client.get('/counters/nom')
        self.assertEqual(getResult.json['Count'], "0")

        # Ensure that it returned a successful return code.
        self.assertEqual(getResult.status_code, status.HTTP_200_OK)

        # Get a test call that doesn't exist
        badTest = self.client.get('/counters/hii')

        # Ensure that it returned a unsuccessful return code.
        self.assertEqual(badTest.status_code, status.HTTP_409_CONFLICT)


    def test_deleteCounter(self):
        """It should delete a counter"""

        # Makes a counter
        result = self.client.post('/counters/delCntr')

        # Ensure that it returned a successful return code.
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        # Request to delete the counter
        deleteResult = self.client.delete('/counters/delCntr')

        # Ensure that it returned a successful return code.
        self.assertEqual(deleteResult.status_code, status.HTTP_204_NO_CONTENT)

        # Ensure that counter was actually deleted
        getResult = self.client.get('/counters/delCntr')
        self.assertEqual(getResult.status_code, status.HTTP_409_CONFLICT)