import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter


cred = credentials.Certificate("app.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

class City:
    def __init__(self, name, state, country, capital=False, population=0, regions=[]):
        self.name = name
        self.state = state
        self.country = country
        self.capital = capital
        self.population = population
        self.regions = regions

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        city = City(source["name"], source["state"], source["country"])

        if "capital" in source:
            city.capital = source["capital"]

        if "population" in source:
            city.population = source["population"]

        if "regions" in source:
            city.regions = source["regions"]

        return city


    def to_dict(self):
        # [START_EXCLUDE]
        dest = {"name": self.name, "state": self.state, "country": self.country}

        if self.capital:
            dest["capital"] = self.capital

        if self.population:
            dest["population"] = self.population

        if self.regions:
            dest["regions"] = self.regions

        return dest
        # [END_EXCLUDE]

    def __repr__(self):
        return f"City(\
                name={self.name}, \
                country={self.country}, \
                population={self.population}, \
                capital={self.capital}, \
                regions={self.regions}\
            )"


# [END firestore_data_custom_type_definition]


def add_example_data():
    db = firestore.Client()
    # [START firestore_data_get_dataset]
    cities_ref = db.collection("cities")
    cities_ref.document("BJ").set(
        City("Beijing", None, "China", True, 21500000, ["hebei"]).to_dict()
    )
    cities_ref.document("SF").set(
        City(
            "San Francisco", "CA", "USA", False, 860000, ["west_coast", "norcal"]
        ).to_dict()
    )
    cities_ref.document("LA").set(
        City(
            "Los Angeles", "CA", "USA", False, 3900000, ["west_coast", "socal"]
        ).to_dict()
    )
    cities_ref.document("DC").set(
        City("Washington D.C.", None, "USA", True, 680000, ["east_coast"]).to_dict()
    )
    cities_ref.document("TOK").set(
        City("Tokyo", None, "Japan", True, 9000000, ["kanto", "honshu"]).to_dict()
    )
    # [END firestore_data_get_dataset]
add_example_data()

def add_custom_class_with_ID():
    db = firestore.Client()
    data=City(name="Mumbai",state="Maharashtra",country="India")
    db.collection("cities").document("Mumbai").set(data.to_dict())
add_custom_class_with_ID()

def add_details_with_ID():
    db = firestore.Client()
    data={}
    db.collection("cities").document("New_city_ID").set(data)
add_details_with_ID()

""" def add_custom_class_generated_id():
    db = firestore.Client()
    city = {"name": "Beijing", "country": "China"}
    update_time,city_ref = db.collection("cities").add(city) ## Doubt 1 ##
    print(f"Added document with id {city_ref.id}")
add_custom_class_generated_id() """

""" def add_new_doc():
    db = firestore.Client()
    new_city_ref=db.collection("cities").document()
    new_city_ref.set({})
add_new_doc() """

def get_check_exists():
    db=firestore.Client()
    city_ref=db.collection("cities").document("Mumbai")
    doc=city_ref.get()
    if doc.exists:
        print(f"Document Exist: {doc.to_dict()}")
    else:
        print("Document does not exist")
get_check_exists()


def simple_query():
    db = firestore.Client()
    cities_ref = db.collection("cities")
    query = cities_ref.where(filter=FieldFilter("capital", "==", True))
    for doc in query.stream():
        print(f"{doc.id} : {doc.to_dict()}")
simple_query()

def query_with_cityname():
    db = firestore.Client()
    cities_ref = db.collection("cities")
    query = cities_ref.where(filter=FieldFilter("name", "==", "Mumbai")).stream()
    for doc in query:
        print(f"{doc.id} : {doc.to_dict()["country"]}")
    
query_with_cityname()


def update_doc_array():
    db = firestore.Client()
    db.collection("cities").document("DC").set(
        City("Washington D.C.", None, "USA", True, 680000, ["east_coast"]).to_dict()
    )

    # [START firestore_data_set_array_operations]
    city_ref = db.collection("cities").document("DC")

    # Atomically add a new region to the 'regions' array field.
    city_ref.update({"regions": firestore.ArrayUnion(["greater_virginia"])})

    # // Atomically remove a region from the 'regions' array field.
    city_ref.update({"regions": firestore.ArrayRemove(["east_coast"])})
    # [END firestore_data_set_array_operations]
    city = city_ref.get()
    print(f"Updated the regions field of the DC. {city.to_dict()}")
update_doc_array()


