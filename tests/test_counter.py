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
        """It should update a counter by 1"""
        result = self.client.post("/counters/boo")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result.json['boo'], 0)

        originalValue = result.json['boo']
        updated = self.client.put("/counters/boo")
        self.assertEqual(originalValue + 1, updated.json['boo'])

        # should not exist, so resource shouldn't be found
        throwError = self.client.put("/counters/nonexistant")
        self.assertEqual(throwError.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_a_counter(self):
        """It should read the value of a counter"""
        result = self.client.post("/counters/foobar")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result.json['foobar'], 0) # inital starting count

        readValue = self.client.get("/counters/foobar")
        self.assertEqual(0, readValue.json['foobar'])

        # should not exist, so resource shouldn't be found
        throwError = self.client.get("/counters/nonexistant")
        self.assertEqual(throwError.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_a_counter(self):
        """It should delete a counter"""
        result = self.client.post("/counters/far")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        deleted = self.client.delete("/counters/far")
        self.assertEqual(deleted.status_code, status.HTTP_204_NO_CONTENT)

        # should already be deleted, so resource shouldn't be found
        throwError = self.client.delete("/counters/far")
        self.assertEqual(throwError.status_code, status.HTTP_404_NOT_FOUND)