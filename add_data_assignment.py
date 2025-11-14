import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter


cred = credentials.Certificate("app.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

""" 🔰 Level 1 – Basic Write Operations

Create a users collection and add a document with your name, email, and age.

Create a document in cities collection with a custom ID "NYC" containing fields:

name: "New York"

state: "NY"

country: "USA"

Add another city to the same collection, but let Firestore auto-generate the document ID.

Overwrite the "NYC" document entirely with a new set of data (e.g., add a "population" field).

Try setting a document that doesn’t exist — what happens? """

def create1():
    db=firestore.Client()
    data={"name":"Nitheesh Kumar","email":"21am1a3130@svrec.ac.in","age":21}
    db.collection("users").document(data["name"]).set(data)
    print("Data Added Successfully")


def create_cities2():
    db=firestore.Client()
    data={"name":"New York","state":"NY","country":"USA"}
    db.collection("cities").document("NYC").set(data)
    print("Data Added Successfully")

def add_city3():
    db=firestore.Client()
    data={"name":"Mumbai","state":"Maharashtra","country":"India"}
    db.collection("cities").add(data)
    print("Data Added Successfully")

def overwritee4():
    db=firestore.Client()
    data={"name":"New York","state":"NY","country":"USA","population":8000000}
    db.collection("cities").document("NYC").set(data)
    print("Data Overwritten Successfully")

def not_exist5():
    db=firestore.Client()
    db.collection("cities").document().set({})
    print("Data Added Successfully")

"""create1()
create_cities2()
add_city3()
overwritee4()
not_exist5()"""

""" 🧩 Level 2 – Using Merge and Update

Use .set(..., merge=True) to add a new field (isCapital: False) to an existing document without overwriting it.

Update only the "population" field in "NYC" to a new value.

Add a "mayor" field to "NYC" using .update().

Try updating a field in a document that doesn’t exist — what error do you get?

Add a "founded" field with a server timestamp to track the document creation time."""


def meerge6():
    db=firestore.Client()
    data={"name":"New York","state":"NY","country":"USA","population":8000000}
    db.collection("cities").document("NYC").set(data,merge=True)
    print("Data Merge Successfully")

def update7():
    db=firestore.Client()
    data={"population":10000000}
    db.collection("cities").document("NYC").update(data)
    print("Data Updated Successfully")

def update8():
    db=firestore.Client()
    data={"mayor":"Nitheesh Kumar"}
    db.collection("cities").document("NYC").update(data)
    print("Data Updated Successfully")

'''def not_exist9():
    db=firestore.Client()
    data={"name":"New York","state":"NY","country":"USA","population":8000000}
    city_ref=db.collection("cities").document()
    city_ref.update(data)
    print("Data Updated Successfully")''' # not found errror

def update10():
    db=firestore.Client()
    data={"founded":firestore.SERVER_TIMESTAMP}
    db.collection("cities").document("NYC").update(data)
    print("Data Updated Successfully")

"""meerge6()
update7()
update8()

update10()"""

""" 🪄 Level 3 – Nested Maps & Dot Notation

Create a users document with a nested map:

{
  "name": "Alice",
  "address": {"city": "Denver", "zip": "80203"},
  "age": 25
}


Update only "address.city" to "Boulder" using dot notation.

Try updating "address" without dot notation — what happens to "zip"?

Add a nested map "employment": {"company": "Google", "position": "Engineer"} to "users/alice".

Merge additional nested fields into "employment" without overwriting the whole map."""


def query11():
    db=firestore.Client()
    data={"name":"Sakshi","address":{"city":"Denver","zip":"80203"},"age":25}
    db.collection("users").document("Sakshi").set(data)
    print("Data Added Successfully")

def update12():
    db=firestore.Client()
    data={"address.city":"Boulder"}
    db.collection("users").document("Sakshi").update(data)
    print("Data Updated Successfully")

"""def update13():
    db=firestore.Client()
    data={"address[zip]":"802033"}
    db.collection("users").document("Sakshi").update(data)
    print("Data Updated Successfully")""" # Invalid char error

def update14():
    db=firestore.Client()
    data={"employment":{"company":"Google","position":"Engineer"}}
    db.collection("users").document("Sakshi").update(data)
    print("Data Updated Successfully")

def update15():
    db=firestore.Client()
    data={"employment.salary":100000}
    db.collection("users").document("Sakshi").set(data,merge=True)
    print("Data Updated Successfully")

"""query11()
update12()
update14()
update15()"""

""" 📚 Level 4 – Arrays

Add an "interests" array to "users/alice" with values ["coding", "reading"].

Use ArrayUnion() to add "traveling" to the array.

Use ArrayRemove() to remove "reading" from the array.

Attempt to use ArrayUnion() to add "coding" again — does it duplicate?

Create a "skills" array and experiment with adding multiple elements at once."""

def array16():
    db=firestore.Client()
    data={"interests":["coding","reading"]}
    db.collection("users").document("Sakshi").update(data)
    print("Data Updated Successfully")

def array17():
    db=firestore.Client()
    data={"interests":firestore.ArrayUnion(["traveling"])}
    db.collection("users").document("Sakshi").update(data)
    print("Data Updated Successfully")

def array18():
    db=firestore.Client()
    data={"interests":firestore.ArrayRemove(["reading"])}
    db.collection("users").document("Sakshi").update(data)
    print("Data Updated Successfully")

def array19():
    db=firestore.Client()
    data={"interests":firestore.ArrayUnion(["coding"])}
    db.collection("users").document("Sakshi").update(data)
    print("Data Updated Successfully")

def array20():
    db=firestore.Client()
    data={"skills":["Python","Java","C++"]}
    db.collection("users").document("Sakshi").update(data)
    print("Data Updated Successfully")

'''array16()
array17()
array18()
array19()
array20()'''

"""⚙️ Level 5 – Numeric Operations & Counters

Add a "followers" field with value 100 to "users/alice".

Increment the "followers" count by 10 using Increment(10).

Decrement the "followers" count by 5.

Try incrementing a field that doesn’t exist — what value does it become?

Implement a small like counter field that increments each time you simulate a “like.”"""

def numeric21():
    db=firestore.Client()
    data={"followers":100}
    db.collection("users").document("Sakshi").update(data)
    print("Data Updated Successfully")

def numeric22():
    db=firestore.Client()
    data={"followers":firestore.Increment(10)}
    db.collection("users").document("Sakshi").update(data)
    print("Data Updated Successfully")

def numeric23():
    db=firestore.Client()
    data={"followers":firestore.Increment(-5)}
    db.collection("users").document("Sakshi").update(data)
    print("Data Updated Successfully")

def numeric24():
    db=firestore.Client()
    data={"following":firestore.Increment(50)}
    db.collection("users").document("Sakshi").update(data)
    print("Data Updated Successfully")
 
def numeric25():
    db=firestore.Client()
    data={"likes":firestore.Increment(1)}
    db.collection("users").document("Sakshi").update(data)
    print("Data Updated Successfully")

'''numeric25()
numeric24()
numeric23()
numeric22()
numeric21()'''

'''🧱 Level 6 – Subcollections

Create a subcollection comments inside "posts/post1" and add three comments.

Use .set() to create a document "post1" in "posts" and then add a comment in posts/post1/comments.

Retrieve and update one of the subcollection documents.

Try adding a nested field inside a subcollection document.

Use an auto-generated document ID inside a subcollection.'''

def subcollection26():
    db=firestore.Client()
    data={"comments":["comment1","comment2","comment3"]}
    post_ref=db.collection("posts")
    post_ref.document("post1").collection("comments").document("comment1").set(data)
    print("Data Updated Successfully")

def subcollection27():
    db=firestore.Client()
    data={"name":"post1"}
    post_ref=db.collection("posts").document("post1")
    post_ref.collection("comments").add(data)
    print("Data Updated Successfully")

def subcollection28():
    db=firestore.Client()
    post_ref=db.collection("posts").document("post1").collection("comments").document("comment1")
    data={"likes":firestore.Increment(1)}
    post_ref.update(data)
    print("Data Updated Successfully")

def subcollection29():
    db=firestore.Client()
    data={"following":firestore.Increment(1)}
    post_ref=db.collection("posts").document("post1").collection("comments").document("comment1")
    post_ref.set(data,merge=True)
    print("Data Updated Successfully")

def subcollection30():
    db=firestore.Client()
    data={"name":"post1"}
    post_ref=db.collection("posts").document("post1")
    post_ref.collection("comments").add(data)
    print("Data Updated Successfully")

'''subcollection26()
subcollection27()
subcollection28()
subcollection29()
subcollection30()'''

""" 🧩 Level 7 – Auto IDs, Classes, and Batch Writes (Queries 30–40) """

# 30️ Auto-generated document ID inside a subcollection
def query30():
    db = firestore.Client()
    data = {"comment": "This is an auto-ID comment", "likes": 2}
    post_ref = db.collection("posts").document("post1")
    post_ref.collection("comments").add(data)
    print("Auto-ID subcollection document added successfully")


# 31️ Define a City class
class City:
    def __init__(self, name, state, country, population, capital):
        self.name = name
        self.state = state
        self.country = country
        self.population = population
        self.capital = capital

    def to_dict(self):
        return {
            "name": self.name,
            "state": self.state,
            "country": self.country,
            "population": self.population,
            "capital": self.capital
        }


# 32️ Add a City object to Firestore
def query32():
    db = firestore.Client()
    ny = City("New York", "NY", "USA", 8800000, True)
    db.collection("cities").document("NYC").set(ny.to_dict())
    print("City object added successfully")


# 33️ Update one of the class fields (population)
def query33():
    db = firestore.Client()
    db.collection("cities").document("NYC").update({"population": 9000000})
    print("City population updated successfully")


# 34️ Add another City object with an auto-generated ID
def query34():
    db = firestore.Client()
    la = City("Los Angeles", "CA", "USA", 4000000, False)
    db.collection("cities").add(la.to_dict())
    print("Auto-ID City object added successfully")


# 35️ Batch write – add multiple City objects
def query35():
    db = firestore.Client()
    batch = db.batch()

    c1 = db.collection("cities").document("Chicago")
    c2 = db.collection("cities").document("Houston")
    c3 = db.collection("cities").document("Phoenix")

    batch.set(c1, {"name": "Chicago", "state": "IL", "country": "USA"})
    batch.set(c2, {"name": "Houston", "state": "TX", "country": "USA"})
    batch.set(c3, {"name": "Phoenix", "state": "AZ", "country": "USA"})

    batch.commit()
    print("Batch write completed successfully")


# 36️ Add or merge user data if exists
def query36():
    db = firestore.Client()
    data = {"name": "Sakshi", "email": "sakshi@example.com", "verified": True}
    db.collection("users").document("Sakshi").set(data, merge=True)
    print("User data merged or added successfully")


# 37️ Add any Python dictionary with auto-generated ID
def query37():
    db = firestore.Client()
    data = {"topic": "Firestore", "level": "Advanced", "duration": "2 hours"}
    db.collection("tutorials").add(data)
    print("Dictionary added successfully with auto-generated ID")


# 38️ Add multiple cities in a loop
def query38():
    db = firestore.Client()
    cities = [
        {"name": "San Francisco", "state": "CA", "country": "USA"},
        {"name": "Seattle", "state": "WA", "country": "USA"},
        {"name": "Boston", "state": "MA", "country": "USA"}
    ]
    for city in cities:
        db.collection("cities").add(city)
    print("Multiple city documents added with auto-generated IDs")


# 39️ Create nested subcollection structure
def query39():
    db = firestore.Client()
    emp_data = {"name": "John Doe", "role": "Engineer"}
    db.collection("companies").document("google") \
      .collection("departments").document("engineering") \
      .collection("employees").add(emp_data)
    print("Nested subcollection document added successfully")


# 40️ Create or update document with timestamps
def query40():
    db = firestore.Client()
    data = {
        "name": "Timestamp Example",
        "createdAt": firestore.SERVER_TIMESTAMP,
        "updatedAt": firestore.SERVER_TIMESTAMP
    }
    db.collection("meta").document("record1").set(data, merge=True)
    print("Document with timestamps added/updated successfully")

# query30()
# query32()
# query33()
# query34()
# query35()
# query36()
# query37()
# query38()
# query39()
# query40()



