import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter


cred = credentials.Certificate("app.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


"""def simple_transaction():
    transaction=db.transaction()
    emp_ref=db.collection("employees").document("Nitheesh")
    @firestore.transactional
    def update_salary(transaction,emp_ref):
        snapshot=emp_ref.get(transaction=transaction)
        salary=snapshot.to_dict()["salary"]
        transaction.update(emp_ref,{"salary":salary+10000})
    update_salary(transaction,emp_ref)
    print("Transaction Successful")

simple_transaction()"""

def transac_on_condition():
    transaction=db.transaction()
    emp_ref=db.collection("employees").document("Nitheesh")
    @firestore.transactional
    def update_salary(transaction,emp_ref):
        snapshot=emp_ref.get(transaction=transaction)
        salary=snapshot.to_dict()["salary"]
        new_salary=salary+10000
        if new_salary<100000:
            transaction.update(emp_ref,{"salary":new_salary})
            print("Transaction Successful")
        else:
            print("Transaction Failed")
    update_salary(transaction,emp_ref)
transac_on_condition()

""" 🧩 Transaction Query 1 — Safe Book Borrow

Goal:
When a member borrows a book:

Check if the book has available_copies > 0

If yes → decrement available_copies by 1

Also add that book title to the member’s borrowed_books array

Requirements:

Use a transaction.

Print "Borrow successful" or "No copies available".

Hints:

Use firestore.transactional decorator.

Use firestore.ArrayUnion() for appending."""

def safe_book_borrow():
    transaction=db.transaction()
    member_ref=db.collection("members").document("Alice")
    book_ref=db.collection("books").document("1984")
    @firestore.transactional
    def borrow_book(transaction,member_ref,book_ref):
        member_snapshot=member_ref.get(transaction=transaction)
        book_snapshot=book_ref.get(transaction=transaction)
        if book_snapshot.to_dict()["available_copies"]>0:
            transaction.update(book_ref,{"available_copies":firestore.Increment(-1)})
            transaction.update(member_ref,{"borrowed_books":firestore.ArrayUnion([book_snapshot.to_dict()["title"]])})
            print("Borrow Successful")
        else:
            print("No copies available")
    borrow_book(transaction,member_ref,book_ref)


""" 🧩 Transaction Query 2 — Return Book Safely

Goal:
When a member returns a book:

Increment available_copies by 1 in books collection

Remove the book title from the member’s borrowed_books array

Requirements:

Use a transaction.

Ensure both updates happen atomically."""

def return_book_safely():
    transaction=db.transaction()
    book_ref=db.collection("books").document("1984")
    member_ref=db.collection("members").document("Alice")
    @firestore.transactional
    def return_book(transaction,book_ref,member_ref):
        book_snapshot=book_ref.get(transaction=transaction)
        member_snapshot=member_ref.get(transaction=transaction)
        if book_snapshot.to_dict()["title"] in member_snapshot.to_dict()["borrowed_books"]:
            transaction.update(book_ref,{"available_copies":firestore.Increment(1)})
            transaction.update(member_ref,{"borrowed_books":firestore.ArrayRemove([book_snapshot.to_dict()["title"]])})
            print("Return Successful")
        else:
            print("Return Failed")
    return_book(transaction,book_ref,member_ref)


"""🧩 Transaction Query 3 — Prevent Negative Copies

Goal:
You need to make sure no book ever has available_copies < 0.

Steps:

Read the book_ref.

If available_copies is already 0 → throw an exception.

Otherwise, decrement by 1.

Extra:
Try running the same transaction twice simultaneously to test Firestore’s retry logic.
One should succeed, the other should fail."""

def prevent_negative_copies():
    transaction=db.transaction()
    book_ref=db.collection("books").document("1984")
    @firestore.transactional
    def update_copies(transaction,book_ref):
        book_snapshot=book_ref.get(transaction=transaction)
        if book_snapshot.to_dict()["available_copies"]==0:
            raise Exception("No copies available")
        else:
            transaction.update(book_ref,{"available_copies":firestore.Increment(-1)})
            print("Transaction Successful")
    update_copies(transaction,book_ref)


""" 🧩 Transaction Query 4 — Borrow Count Update

Goal:
Each time a book is borrowed:

Increment a borrow_count field in the books document.

Also update the member’s last_activity to the current timestamp.

Requirements:

Use a single transaction for both operations."""

### Query number 4 is same as query 1

"""🧩 Transaction Query 5 — Transfer Book Copies

Goal:
Simulate transferring one available copy from one book to another (for testing atomic multi-doc updates).

Steps:

Read both book documents (e.g., "Gatsby" and "1984").

Decrement copies of Gatsby by 1

Increment copies of 1984 by 1

Commit the transaction atomically."""

def transfer_book_copies():
    transaction=db.transaction()
    gatsby_ref=db.collection("books").document("Gatsby")
    a1984_ref=db.collection("books").document("1984")
    @firestore.transactional
    def transfer_copies(transaction,gatsby_ref,a1984_ref):
        gatsby_snapshot=gatsby_ref.get(transaction=transaction)
        a1984_snapshot=a1984_ref.get(transaction=transaction)
        if gatsby_snapshot.to_dict()["available_copies"]>a1984_snapshot.to_dict()["available_copies"]:
            transaction.update(gatsby_ref,{"available_copies":firestore.Increment(-1)})
            transaction.update(a1984_ref,{"available_copies":firestore.Increment(1)})
            print("Transaction Successful")
        elif(gatsby_snapshot.to_dict()["available_copies"]<a1984_snapshot.to_dict()["available_copies"]):
            transaction.update(gatsby_ref,{"available_copies":firestore.Increment(1)})
            transaction.update(a1984_ref,{"available_copies":firestore.Increment(-1)})
            print("Transaction Successful")
        else:
            print("Transaction Failed as copies are same")
    transfer_copies(transaction,gatsby_ref,a1984_ref)


""" 🧩 Transaction Query 6 — Member Upgrade Rule

Goal:
Upgrade a member’s membership_type from "standard" to "premium" only if they have borrowed ≥ 3 books.

Steps:

Read the member doc

If len(borrowed_books) >= 3:
update "membership_type": "premium"

Else → print "Not eligible for upgrade"."""

def upgrade_member():
    @firestore.transactional
    def upgrade_member_inside(transaction,member_ref):
        member_snapshot=member_ref.get(transaction=transaction)
        if len(member_snapshot.to_dict()["borrowed_books"])>=3:
            transaction.update(member_ref,{"membership_type":"premium"})
            print("Transaction Successful")
        else:
            print("Not eligible for upgrade")
    
    member_ref=db.collection("members").stream()
    for doc in member_ref:
        transaction=db.transaction()
        upgrade_member_inside(transaction,doc.reference)
    

"""🧩 Transaction Query 7 — Borrow History Record

Goal:
When a book is borrowed:

Decrement available_copies

Add a record in a subcollection members/{member_id}/borrow_history
with { "book_title": <title>, "borrowed_at": server timestamp }

Requirements:

Must be done in one transaction

No external .add() calls outside the transaction"""


def borrow_history_record():
    @firestore.transactional
    def borrow_book(transaction,member_ref,book_ref):
        book_snapshot=book_ref.get(transaction=transaction)
        member_snapshot=member_ref.get(transaction=transaction)
        if book_snapshot.to_dict()["available_copies"]>0:
            transaction.update(book_ref,{"available_copies":book_snapshot.to_dict()["available_copies"]-1})
            borrow_history_ref=member_ref.collection("borrow_history").document()
            borrow_history_ref.set({"book_title":book_snapshot.to_dict()["title"],"borrowed_at":firestore.SERVER_TIMESTAMP})
            print("Transaction Successful")
        else:
            print("No copies available")
    transaction=db.transaction()
    member_ref=db.collection("members").document("Alice")
    book_ref=db.collection("books").document("1984")
    borrow_book(transaction,member_ref,book_ref)

"""🧩 Transaction Query 8 — Reset All Premium Members’ Activity

Goal:
For every premium member, reset their last_activity to None.

Steps:

Fetch all premium members.

For each one, run a transaction that sets last_activity = None.

(Hint: Firestore does not support multi-doc transactions across all docs at once; you must loop with per-doc transactions.)"""

def reset_all_premium_members_activity():
    @firestore.transactional
    def reset_activity(transaction,member_ref):
        transaction.update(member_ref,{"last_activity":None})
        print("Transaction Successful")
    
    member_ref=db.collection("members").where(filter=FieldFilter("membership_type","==","premium")).stream()
    for doc in member_ref:
        transaction=db.transaction()
        reset_activity(transaction,db.collection("members").document(doc.id))
reset_all_premium_members_activity()



"""🧩 Transaction Query 9 — Borrow Limit Enforcement

Goal:
Ensure no member borrows more than 5 books.

Steps:

In transaction:

Read member doc

Check len(borrowed_books)

If < 5 → add book to list

Else → raise exception "Borrow limit reached"""


def borrow_limit_enforcement():
    @firestore.transactional
    def borrow_book(transaction,member_ref,book_ref):
        member_snapshot=member_ref.get(transaction=transaction)
        book_snapshot=book_ref.get(transaction=transaction)
        if len(member_snapshot.to_dict()["borrowed_books"])<5:
            transaction.update(member_ref,{"borrowed_books":firestore.ArrayUnion([book_snapshot.to_dict()["title"]])})
            print("Transaction Successful")
        else:
            print("Borrow limit reached")
    members=db.collection("members").stream()
    for doc in members:
        member_ref = db.collection("members").document(doc.id)
        book_ref = db.collection("books").document("1984")
        transaction = db.transaction()
        borrow_book(transaction, member_ref, book_ref)



""" 🧩 Transaction Query 10 — Synchronize Available Copies

Goal:
Fix data inconsistencies automatically.
If a book’s available_copies is negative, set it to 0 in a transaction.

Steps:

Query all books

For each with negative copies, run a transaction that sets it to 0."""

def syncronize_available_copies():
    @firestore.transactional
    def sync_copies(transaction,book_ref):
        book_snapshot=book_ref.get(transaction=transaction)
        if book_snapshot.to_dict()["available_copies"]<0:
            transaction.update(book_ref,{"available_copies":0})
    
    books=db.collection("books").stream()
    for doc in books:
        transaction=db.transaction()
        book_ref=db.collection("books").document(doc.id)
        sync_copies(transaction,book_ref)




city_ref = db.collection("users").document("Nitheesh")
collections = city_ref.collections()
for collection in collections:
    for doc in collection.stream():
        print(f"{doc.id} => {doc.to_dict()}")




