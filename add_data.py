import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import datetime

cred=credentials.Certificate("app.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

def adding_empdata():
    db=firestore.client()
    emp_ref=db.collection("employees")
    data={"name":"Nitheesh","salary":20000,"department":"IT","location":"Hyd"}
    emp_ref.document("Nitheesh").set(data)
    print("Data Added Successfully")
adding_empdata()

def merge_data():
    db=firestore.client()
    emp_ref=db.collection("employees").document("Nitheesh")
    data={"status":"Married"}
    emp_ref.set(data,merge=True)
    print("Data Merged Successfully")
merge_data()

def data_types():
    db=firestore.client()
    emp_ref=db.collection("employees").document("data")
    data = {
        "numberExample":123,
        "stringExample":"Hello World",
        "BooleanExample":True,
        "nullExample":None,
        "arrayExample":[1,2,3,4,5],
        "objectExample":{"name":"Nitheesh","age":21},
        "dateExample":datetime.datetime.now()
    }
    emp_ref.set(data)
    print("Data Added Successfully")
data_types()


""" def add_method():
    db=firestore.client()
    
    data={"name":"Mahesh","salary":40000,"department":"NON-IT","location":"BLR"}
    update_time,emp_ref=db.collection("employees").add(data)
    print("Data Added Successfully with add method {}".format(emp_ref.id))
add_method() """

def update_document():
    db=firestore.client()
    emp_ref=db.collection("employees").document("Nitheesh")
    emp_ref.update({"status":"Single"})
    print("Data Updated Successfully")
update_document()

def update_timestamp():
    db=firestore.client()
    emp_ref=db.collection("employees").document("data")
    emp_ref.update({"timestamp":firestore.SERVER_TIMESTAMP})
    print("Timestamp Updated Successfully")
update_timestamp()

def update_fieldsin_nested():
    emp_ref=db.collection("employees").document("data")
    emp_ref.update({"BooleanExample":False,"objectExample.name":"Dimple"})
    print("Data Updated Successfully in nested field")
update_fieldsin_nested()

def update_array():
    emp_ref=db.collection("employees").document("data")
    emp_ref.update({"arrayExample":firestore.ArrayUnion([6,7,8])})
    print("Array Updated Successfully")
update_array()

def update_array_remove():
    emp_ref=db.collection("employees").document("data")
    emp_ref.update({"arrayExample":firestore.ArrayRemove([1,2,3])})
    print("Array Removed Successfully")
update_array_remove()

def Increment_value():
    emp_ref=db.collection("employees").document("data")
    emp_ref.update({"numberExample":firestore.Increment(10)})
    print("Value Incremented Successfully")
Increment_value()













