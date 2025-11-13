""" Get all active members.

Get members who joined before January 1, 2024.

Get members with membership_type == 'premium'.

Get all members who borrowed “The Great Gatsby”.

Get all members whose borrowed_books array contains any of ["1984", "Animal Farm"].

Get members who have borrowed more than 3 books. (Hint: use len(borrowed_books) logic in your client-side filter after fetching.)

Get members sorted by join_date (newest first).

Get all members who are not active.

Get members with membership_type in ['standard', 'premium'].

Get the first 5 members alphabetically by name. """

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import datetime


cred = credentials.Certificate("app.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Get all active members.
def get_active_members():
    db = firestore.Client()
    members_ref = db.collection("members")
    query = members_ref.where(filter=FieldFilter("active", "==", True)).stream()
    print ("--------Query 1--------")
    print("Active Members:")
    for doc in query:
        print(f"{doc.id}")
get_active_members()

# Get members who joined before January 1, 2024.

def get_members_before_jan_2024():
    db=firestore.Client()
    members_ref=db.collection("members")
    query=members_ref.where(filter=FieldFilter("join_date","<",datetime.datetime(2024,1,1))).stream()
    print("--------Query 2--------")
    print("Members who joined before January 1, 2024:")
    for doc in query:
        print(f"{doc.id}")
get_members_before_jan_2024()

# Get members with membership_type == 'premium'.

def get_members_premium():
    db=firestore.Client()
    members_ref=db.collection("members")
    query=members_ref.where(filter=FieldFilter("membership_type","==","premium")).stream()
    print("--------Query 3--------")
    print("Members with membership_type == 'premium':")
    for doc in query:
        print(f"{doc.id}")
get_members_premium()

# Get all members who borrowed “The Great Gatsby”.

def members_borrowed_gatsby():
    db=firestore.Client()
    members_ref=db.collection("members")
    query=members_ref.where(filter=FieldFilter("borrowed_books","array_contains","The Great Gatsby")).stream()
    print("--------Query 4--------")
    print("Members who borrowed 'The Great Gatsby':")
    for doc in query:
        print(f"{doc.id}")
members_borrowed_gatsby()

##  Get all members whose borrowed_books array contains any of ["1984", "Animal Farm"].
def members_borrowed_1984_animalfarm():
    db=firestore.Client()
    members_ref=db.collection("members")
    query=members_ref.where(filter=FieldFilter("borrowed_books","array_contains_any",["1984","Animal Farm"])).stream()
    print("--------Query 5--------")
    print("Members who borrowed '1984' or 'Animal Farm':")
    for doc in query:
        print(f"{doc.id}")
members_borrowed_1984_animalfarm()

# Get members who have borrowed more than 3 books.
def members_borrowed_morethan3():
    db=firestore.Client()
    members_ref=db.collection("members").stream()
    print("--------Query 6--------")
    print("Members who borrowed more than 3 books:")
    for doc in members_ref:
        if len(doc.to_dict()["borrowed_books"])>=3:
            print(f"{doc.id}")
members_borrowed_morethan3()

# Get members sorted by join_date (newest first).
def members_sorted_by_join_date():
    db=firestore.Client()
    members_ref=db.collection("members").order_by("join_date",direction=firestore.Query.DESCENDING).stream()
    print("--------Query 7--------")
    print("Members sorted by join_date (newest first):")
    for doc in members_ref:
        print(f"{doc.id}")
members_sorted_by_join_date()

##  Get all members who are not active.

def members_not_active():
    db = firestore.Client()
    members_ref = db.collection("members")
    query = members_ref.where(filter=FieldFilter("active", "!=", True)).stream()
    print ("--------Query 8--------")
    print("InActive Members:")
    for doc in query:
        print(f"{doc.id}")
members_not_active()

## Get members with membership_type in ['standard', 'premium']

def members_membership_standard_premium():
    db=firestore.Client()
    members_ref=db.collection("members")
    query=members_ref.where(filter=FieldFilter("membership_type","in",["standard","premium"])).stream() 
    print("--------Query 9--------")
    print("Members with membership_type in ['standard', 'premium']:")
    for doc in query:
        print(f"{doc.id}")
members_membership_standard_premium()

## Get the first 5 members alphabetically by name.

def first_5_members_alphabetically():
    db=firestore.Client()
    members_ref=db.collection("members")
    query=members_ref.order_by("name").limit(5).stream()
    print("--------Query 10--------")
    print("First 5 members alphabetically by name:")
    for doc in query:
        print(f"{doc.id}")
first_5_members_alphabetically()