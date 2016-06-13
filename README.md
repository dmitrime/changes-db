Changes DB
====

A [pandas](http://pandas.pydata.org) powered object state explorer with a web front-end.


Setup
====
First install the necessary python packages:

        $ pip install -r requirements.txt

Next, run the server:

        $ python server.py

Then go to http://0.0.0.0:8080, upload a valid CSV file and start querying!


CSV format
====

Here is an example of a valid CSV file:

        object_id | object_type | timestamp | object_changes
         1        |  ObjectA    |  412351252 | {"property1": "value1", "property3": "value2"}
         1        |  ObjectB    |  456662343 | {"property1": "another value1"}
         1        |  ObjectA    |  467765765 | {"property1": "altered value1", "property2": "random value2"}
         2        |  ObjectA    |  451232123 | {"property2": "some value2"}

The first column is the object's ID of integer type.
The second column is the object's type, a string.
The third column is the object's modification time, a UNIX timestamp.
The fourth column is the object state, in JSON format.


Tests
====

To run the tests, execute the following from the root directory:

        $ py.test
