import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import datetime


cred = credentials.Certificate("app.json")

firebase_admin.initialize_app(cred)
db = firestore.client()

# Helper function to batch insert data
def upload_collection(collection_name, data_list):
    batch = db.batch()
    for i, doc in enumerate(data_list, start=1):
        doc_ref = db.collection(collection_name).document(f"{collection_name}_{i}")
        batch.set(doc_ref, doc)
    batch.commit()
    print(f"✅ Uploaded {len(data_list)} docs to '{collection_name}' collection")

# ---------- Sample Data ----------

students = [
    {"name": "Alice", "grade": 95, "age": 17},
    {"name": "Bob", "grade": 82, "age": 18},
    {"name": "Charlie", "grade": 90, "age": 17},
    {"name": "David", "grade": 78, "age": 16},
    {"name": "Eva", "grade": 99, "age": 18}
]

library = [
    {"title": "1984", "author": "George Orwell", "year": 1949},
    {"title": "Animal Farm", "author": "George Orwell", "year": 1945},
    {"title": "Brave New World", "author": "Aldous Huxley", "year": 1932},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925}
]

store = [
    {"product_name": "Laptop", "price": 1200, "stock": 5},
    {"product_name": "Mouse", "price": 25, "stock": 0},
    {"product_name": "Keyboard", "price": 50, "stock": 10},
    {"product_name": "Monitor", "price": 300, "stock": 0}
]

employees = [
    {"name": "John", "department": "IT", "joinDate": "2024-02-10", "skills": ["python", "cloud", "sql"], "salary": 95000, "performance": {"score": 88}},
    {"name": "Maria", "department": "HR", "joinDate": "2023-08-15", "skills": ["communication", "management"], "salary": 65000, "performance": {"score": 92}},
    {"name": "Tom", "department": "IT", "joinDate": "2024-05-21", "skills": ["java", "python", "machine-learning"], "salary": 110000, "performance": {"score": 77}},
    {"name": "Nina", "department": "Finance", "joinDate": "2022-09-10", "skills": ["excel", "analysis"], "salary": 72000, "performance": {"score": 85}},
    {"name": "Leo", "department": "IT", "joinDate": "2024-09-01", "skills": ["python", "machine-learning", "cloud"], "salary": 125000, "performance": {"score": 95}}
]

orders = [
    {"orderId": "O1", "customer_id": "C1", "totalAmount": 450, "orderDate": "2025-10-01", "status": "pending"},
    {"orderId": "O2", "customer_id": "C2", "totalAmount": 1500, "orderDate": "2025-09-15", "status": "delivered"},
    {"orderId": "O3", "customer_id": "C3", "totalAmount": 2300, "orderDate": "2025-11-01", "status": "processing"},
    {"orderId": "O4", "customer_id": "C4", "totalAmount": 300, "orderDate": "2025-08-25", "status": "pending"},
    {"orderId": "O5", "customer_id": "C5", "totalAmount": 1200, "orderDate": "2025-10-20", "status": "shipped"}
]

users = [
    {"name": "Arjun", "account_type": "premium", "isActive": True, "last_login": "2025-11-01"},
    {"name": "Sophie", "account_type": "free", "isActive": True, "last_login": "2025-08-15"},
    {"name": "Ravi", "account_type": "premium", "isActive": False, "last_login": "2025-07-10"},
    {"name": "Linda", "account_type": "premium", "isActive": True, "last_login": "2025-10-25"}
]

cities = [
    {"name": "Toronto", "country": "Canada", "isCapital": False, "population": 2800000},
    {"name": "Ottawa", "country": "Canada", "isCapital": True, "population": 1000000},
    {"name": "Vancouver", "country": "Canada", "isCapital": False, "population": 675000},
    {"name": "Washington", "country": "USA", "isCapital": True, "population": 700000},
    {"name": "Los Angeles", "country": "USA", "isCapital": False, "population": 4000000}
]

# ---------- Upload All ----------
upload_collection("students", students)
upload_collection("library", library)
upload_collection("store", store)
upload_collection("employees", employees)
upload_collection("orders", orders)
upload_collection("users", users)
upload_collection("cities", cities)


"""Basic Queries

Retrieve all students whose grade is greater than or equal to 90.

Get all books from the library collection where the author is "George Orwell".

Find all products in the store collection that are out of stock (stock == 0).

Fetch all employees who joined after January 1, 2024.

Retrieve all cities where country is "Canada" and isCapital is True.


🔹 Advanced Queries

"""

## Retrieve all students whose grade is greater than or equal to 90.
"""def student_greater_than90():
    doc_ref=db.collection("students")
    query=doc_ref.where(filter=FieldFilter("grade",">=",90)).stream()
    for doc in query:
        print(f"{doc.id}")
student_greater_than90()

### Get all books from the library collection where the author is "George Orwell".

def get_books():
    doc_ref=db.collection("library")
    query=doc_ref.where(filter=FieldFilter("author","==","George Orwell")).stream()
    for doc in query:
        print(f"{doc.id}")
get_books()

###3️ Find all products in the store collection that are out of stock (stock == 0).
def out_of_stock():
    doc_ref=db.collection("store")
    query=doc_ref.where(filter=FieldFilter("stock","==",0)).stream()
    for doc in query:
        print(f"{doc.id}")
out_of_stock()

## 4️⃣ Fetch all employees who joined after January 1, 2024.

def joining():
    doc_ref=db.collection("employees")
    query=doc_ref.where(filter=FieldFilter("joinDate",">","2024-01-01")).stream()
    for doc in query:
        print(f"{doc.id}")
joining()

##Retrieve all cities where country is "Canada" and isCapital is True.

def canada_country():
    doc_ref=db.collection("cities")
    query=doc_ref.where(filter=FieldFilter("country","==","Canada")).where(filter=FieldFilter("isCapital","==",True))
    for doc in query.stream():
        print(f"{doc.id}")
canada_country()

##Retrieve all products in the "store" collection where the price is between 50 and 200 (inclusive).

def price_50():
    doc_ref=db.collection("store")
    query=doc_ref.where(filter=FieldFilter("price",">=",50)).where(filter=FieldFilter("price","<=",200))
    for doc in query.stream():
        print(f"{doc.id}")
price_50()

# Retrieve all employees from the "employees" collection whose department is "IT" and experience is greater than 5 years.

def employee1():
    doc_ref=db.collection("employees")
    query=doc_ref.where(filter=FieldFilter("department","==","IT")).where(filter=FieldFilter("experience",">",5))
    for doc in query.stream():
        print(f"{doc.id}")
employee1()

# Retrieve all orders where the status is "delivered" and the deliveryDate is before "2024-12-31"

def order12():
    doc_ref=db.collection("orders")
    query=doc_ref.where(filter=FieldFilter("status","==","delivered")).where(filter=FieldFilter("deliveryDate","<","2024-12-31"))
    for doc in query.stream():
        print(f"{doc.id}")
order12()

# Retrieve all documents from the "students" collection where the subject array contains "Math".

def students12():
    doc_ref=db.collection("students")
    query=doc_ref.where(filter=FieldFilter("subject","array_contains","Math"))
    for doc in query.stream():
        print(f"{doc.id}")
students12()

## Retrieve all cities where the population is greater than 1,000,000 and the country is not equal to "USA".
def cities12():
    doc_ref=db.collection("cities")
    query=doc_ref.where(filter=FieldFilter("population",">",1000000)).where(filter=FieldFilter("country","!=","USA"))
    for doc in query.stream():
        print(f"{doc.id}")
cities12()


#Retrieve all books where the rating is greater than 4.5 and the genre is either "Fiction" or "Mystery".
def retrieve_books():
    doc_ref=db.collection("books")
    query=doc_ref.where(filter=FieldFilter("rating",">",4.5)).where(filter=FieldFilter("genre","in",["Fiction","Mystery"]))
    for doc in query.stream():
        print(f"{doc.id}")
retrieve_books()

# Retrieve all employees whose projects array contains any of the following values: "Alpha", "Beta", or "Gamma".
def retrieve_employees():
    doc_ref=db.collection("employees")
    query=doc_ref.where(filter=FieldFilter("projects","array_contains_any",["Alpha","Beta","Gamma"]))
    for doc in query.stream():
        print(f"{doc.id}")
retrieve_employees()

# Retrieve all orders where the totalAmount is greater than or equal to 500 and the paymentMethod is either "Credit Card" or "UPI".

def retrieve_orders():
    doc_ref=db.collection("orders")
    query=doc_ref.where(filter=FieldFilter("totalAmount",">=",500)).where(filter=FieldFilter("paymentMethod","in",["Credit Card","UPI"]))
    for doc in query.stream():
        print(f"{doc.id}")
retrieve_orders()

""""""Intermediate Queries

Get all users who have "premium" in their account_type field and isActive == True.

Retrieve the top 5 most expensive items in the inventory collection.

Query all blog posts that contain the tag "firebase" in their tags array.

Find all customers whose nested field address.zipcode starts with "9".

Get all orders placed in the last 30 days and sort them by orderDate descending.
"""
 # Get all users who have "premium" in their account_type field and isActive == True.
"""def retrieve_premium():
    doc_ref=db.collection("users")
    query=doc_ref.where(filter=FieldFilter("account_type","==","premium")).where(filter=FieldFilter("isActive","==",True))
    for doc in query.stream():
        print(f"{doc.id}")
retrieve_premium()

# Retrieve the top 5 most expensive items in the inventory collection.

def retrieve_expensive():
    doc_ref=db.collection("inventory")
    query=doc_ref.order_by("price",direction=firestore.Query.DESCENDING).limit(5)
    for doc in query.stream():
        print(f"{doc.id}")
retrieve_expensive()

# Query all blog posts that contain the tag "firebase" in their tags array.
def retrieve_firebase():
    doc_ref=db.collection("blog_posts")
    query=doc_ref.where(filter=FieldFilter("tags","array_contains","firebase"))
    for doc in query.stream():
        print(f"{doc.id}")
retrieve_firebase() """



customers_data = [
    {
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "address": {"street": "123 Main St", "city": "Los Angeles", "zipcode": "90001"},
        "loyaltyPoints": 1200
    },
    {
        "name": "Bob Smith",
        "email": "bob@example.com",
        "address": {"street": "45 Pine Rd", "city": "San Francisco", "zipcode": "94107"},
        "loyaltyPoints": 850
    },
    {
        "name": "Charlie Brown",
        "email": "charlie@example.com",
        "address": {"street": "78 Elm St", "city": "Chicago", "zipcode": "60611"},
        "loyaltyPoints": 450
    },
    {
        "name": "David Miller",
        "email": "david@example.com",
        "address": {"street": "56 King Ave", "city": "New York", "zipcode": "10001"},
        "loyaltyPoints": 970
    },
    {
        "name": "Eva Green",
        "email": "eva@example.com",
        "address": {"street": "89 Sunset Blvd", "city": "San Diego", "zipcode": "92101"},
        "loyaltyPoints": 1020
    }
]

for customer in customers_data:
    db.collection("customers").add(customer)

# Find all customers whose nested field address.zipcode starts with "9".

def customers12():
    doc_ref=db.collection("customers")
    query=doc_ref.where(filter=FieldFilter("address.zipcode","starts_with","9"))
    for doc in query.stream():
        print(f"{doc.id}")
customers12()

#Get all orders placed in the last 30 days and sort them by orderDate descending.
def orders_placed():
    doc_ref=db.collection("orders")
    query=doc_ref.where(filter=FieldFilter("orderDate",">=",datetime.datetime.now()-datetime.timedelta(days=30))).order_by("orderDate",direction=firestore.Query.DESCENDING)
    for doc in query.stream():
        print(f"{doc.id}")
orders_placed()


""" Find all employees where skills array contains both "python" and "machine-learning".

Get all projects that are due in the next 10 days and whose progress is less than 50%.

Retrieve all movies that belong to genre "action" or "thriller" and have a rating above 8.

List all customers whose country is either "USA" or "Japan", using an in filter.

Query all cars where the features array contains any of ["sunroof", "navigation", "heated seats"]."""

def employees12():
    doc_ref=db.collection("employees")
    query=doc_ref.where(filter=FieldFilter("skills","array_contains_all",["python","machine-learning"]))
    for doc in query.stream():
        print(f"{doc.id}")
employees12()

# Get all projects that are due in the next 10 days and whose progress is less than 50%.

def projects12():
    doc_ref=db.collection("projects")
    query=doc_ref.where(filter=FieldFilter("dueDate",">=",datetime.datetime.now()+datetime.timedelta(days=10))).where(filter=FieldFilter("progress","<",50))
    for doc in query.stream():
        print(f"{doc.id}")
projects12()

#Retrieve all movies that belong to genre "action" or "thriller" and have a rating above 8.

def retrieve_movies():
    doc_ref=db.collection("movies")
    query=doc_ref.where(filter=FieldFilter("genre","in",["action","thriller"])).where(filter=FieldFilter("rating",">",8))
    for doc in query.stream():
        print(f"{doc.id}")
retrieve_movies()

# List all customers whose country is either "USA" or "Japan", using an in filter.

def retrieve_customers():
    doc_ref=db.collection("customers")
    query=doc_ref.where(filter=FieldFilter("country","in",["USA","Japan"]))
    for doc in query.stream():
        print(f"{doc.id}")
retrieve_customers()

## Query all cars where the features array contains any of ["sunroof", "navigation", "heated seats"].

def retrieve_cars():
    doc_ref=db.collection("cars")
    query=doc_ref.where(filter=FieldFilter("features","array_contains_any",["sunroof", "navigation", "heated seats"]))
    for doc in query.stream():
        print(f"{doc.id}")
retrieve_cars()

#