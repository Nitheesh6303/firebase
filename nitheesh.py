import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import datetime


cred = credentials.Certificate("app.json")

firebase_admin.initialize_app(cred)
db = firestore.client()

def setup_library_data():
    db = firestore.client()

    # --- BOOKS COLLECTION ---
    books_ref = db.collection("books")

    books = {
        "Gatsby": {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "genre": "Fiction",
            "published_year": 1925,
            "available_copies": 4,
            "rating": 4.5,
            "tags": ["classic", "american", "literature"]
        },
        "Mockingbird": {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "genre": "Fiction",
            "published_year": 1960,
            "available_copies": 2,
            "rating": 4.9,
            "tags": ["classic", "civil-rights", "bestseller"]
        },
        "Sapiens": {
            "title": "Sapiens: A Brief History of Humankind",
            "author": "Yuval Noah Harari",
            "genre": "Non-fiction",
            "published_year": 2011,
            "available_copies": 7,
            "rating": 4.7,
            "tags": ["history", "philosophy", "bestseller"]
        },
        "1984": {
            "title": "1984",
            "author": "George Orwell",
            "genre": "Fiction",
            "published_year": 1949,
            "available_copies": 1,
            "rating": 4.8,
            "tags": ["dystopian", "classic", "political"]
        },
        "AtomicHabits": {
            "title": "Atomic Habits",
            "author": "James Clear",
            "genre": "Self-help",
            "published_year": 2018,
            "available_copies": 5,
            "rating": 4.9,
            "tags": ["self-improvement", "bestseller"]
        },
        "Educated": {
            "title": "Educated",
            "author": "Tara Westover",
            "genre": "Memoir",
            "published_year": 2018,
            "available_copies": 3,
            "rating": 4.6,
            "tags": ["memoir", "inspirational", "bestseller"]
        }
    }

    for key, data in books.items():
        books_ref.document(key).set(data)

    # --- MEMBERS COLLECTION ---
    members_ref = db.collection("members")

    members = {
        "Alice": {
            "name": "Alice Johnson",
            "membership_type": "premium",
            "borrowed_books": ["The Great Gatsby", "1984"],
            "join_date": datetime.datetime(2023, 5, 10),
            "active": True
        },
        "Bob": {
            "name": "Bob Smith",
            "membership_type": "standard",
            "borrowed_books": ["To Kill a Mockingbird"],
            "join_date": datetime.datetime(2024, 1, 15),
            "active": True
        },
        "Charlie": {
            "name": "Charlie Davis",
            "membership_type": "basic",
            "borrowed_books": [],
            "join_date": datetime.datetime(2022, 9, 25),
            "active": False
        },
        "Diana": {
            "name": "Diana Lopez",
            "membership_type": "premium",
            "borrowed_books": ["Sapiens", "Atomic Habits", "Educated"],
            "join_date": datetime.datetime(2023, 3, 8),
            "active": True
        },
        "Ethan": {
            "name": "Ethan Brown",
            "membership_type": "standard",
            "borrowed_books": ["1984", "Sapiens"],
            "join_date": datetime.datetime(2024, 7, 1),
            "active": True
        }
    }

    for key, data in members.items():
        members_ref.document(key).set(data)

    print("✅ Library data has been successfully loaded into Firestore!")
setup_library_data()

def get_fiction_books():
    db=firestore.client()
    book_ref=db.collection("books")
    query=book_ref.where(filter=FieldFilter("genre","==","Fiction")).stream()
    print("1st Query: ")
    for doc in query:
        
        print(f"{doc.id}")
get_fiction_books()


def get_books_after_2000():
    db=firestore.client()
    book_ref=db.collection("books")
    query=book_ref.where(filter=FieldFilter("published_year",">=",2000)).stream()
    print("2nd Query: ")
    for doc in query:
        print(f"{doc.id}")
get_books_after_2000()


def get_classic_in_tags():
    db=firestore.client()
    book_ref=db.collection("books")
    query=book_ref.where(filter=FieldFilter("tags","array_contains","classic")).stream()
    print("3rd Query: ")
    for doc in query:
        print(f"{doc.id}")
get_classic_in_tags()

def top_3_order_by_rating():
    db=firestore.client()
    book_ref=db.collection("books")
    query=book_ref.order_by("rating",direction=firestore.Query.DESCENDING).limit(3).stream()
    print("4th Query: ")
    for doc in query:
        print(f"{doc.id}")
top_3_order_by_rating()

## Get all books with less than 5 copies available.

def books_lessthan_5copies():
    db=firestore.client()
    book_ref=db.collection("books")
    query=book_ref.where(filter=FieldFilter("available_copies","<",5)).stream()
    print("5th Query: ")
    for doc in query:
        print(f"{doc.id}")
books_lessthan_5copies()

#  Get all books where genre is either "Fiction" or "Non-fiction".

def genre_fiction_nonfiction():
    db=firestore.client()
    book_ref=db.collection("books")
    query=book_ref.where(filter=FieldFilter("genre","in",["Fiction","Non-fiction"])).stream()
    print("6th Query: ")
    for doc in query:
        print(f"{doc.id}")
genre_fiction_nonfiction()

## Get all books where rating is not equal to 5.

def rating_not_5():
    db=firestore.client()
    book_ref=db.collection("books")
    query=book_ref.where(filter=FieldFilter("rating","!=",5)).stream()
    print("7th Query: ")
    for doc in query:
        print(f"{doc.id}")
rating_not_5()

## Get all books where published_year > 1950 and rating > 4.

def book_year_greater_rating_greater():
    db=firestore.client()
    book_ref=db.collection("books")
    query=book_ref.where(filter=FieldFilter("published_year",">",1950)).where(filter=FieldFilter("rating",">",4)).stream()
    print("8th Query: ")
    for doc in query:
        print(f"{doc.id}")

book_year_greater_rating_greater()

##Paginate books by rating (3 per page).

def paginate_books_by_ratingperpage():
    db = firestore.client()
    books_ref = db.collection("books")
    query = books_ref.order_by("rating", direction=firestore.Query.DESCENDING).limit(3)
    docs = list(query.stream())
    print("9th Query:")

    print("📘 Page 1:")
    for doc in docs:
        print(f"{doc.id}: {doc.to_dict()['rating']}")

    # Return the last doc for pagination
    if docs:
        return docs[-1]
    else:
        return None
paginate_books_by_ratingperpage()


##Find all books where “tags” array contains any of ["award-winning", "bestseller"].

def _10thquery():
    db=firestore.client()
    book_ref=db.collection("books")
    query=book_ref.where(filter=FieldFilter("tags","array_contains_any",["award-winning","bestseller"])).stream()
    print("10th Query: ")
    for doc in query:
        print(f"{doc.id}")
_10thquery()
