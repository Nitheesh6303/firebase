import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import datetime

cred = credentials.Certificate("app.json")
firebase_admin.initialize_app(cred)
db = firestore.client()



# 1 Create a transaction that increments the population of the "NYC" document by 1.

def transaction1():
    transaction=db.transaction()
    city_ref=db.collection("cities").document("NYC")
    @firestore.transactional
    def increment_population(transaction,city_ref):
        snapshot=city_ref.get(transaction=transaction)
        population=snapshot.to_dict()["population"]
        transaction.update(city_ref,{"population":population+1})
        print("Transaction Successful")
    increment_population(transaction,city_ref)

# transaction1()
# 2 Write a transaction that checks if the population of "NYC" is below 10 million before updating it — otherwise, cancel the update.

def transaction2():
    transaction=db.transaction()
    city_ref=db.collection("cities").document("NYC")
    @firestore.transactional
    def update_condition(transaction,city_ref):
        snapshot=city_ref.get(transaction=transaction)
        if snapshot.to_dict()["population"]<1000000:
            transaction.update(city_ref,{"population":snapshot.to_dict()["population"]+1})
            print("Transaction Successfull")
        else:
            print("Transaction Unsuccessfull")
    update_condition(transaction,city_ref)
# transaction2()

# Perform a transaction that swaps the populations between two documents — "NYC" and "SF".

def transaction3():
    transaction=db.transaction()
    city_ref_1=db.collection("cities").document("NYC")
    city_ref_2=db.collection("cities").document("SF")
    @firestore.transactional
    def swap(transaction,city_ref_1,city_ref_2):
        snap1=city_ref_1.get(transaction=transaction)
        snap2=city_ref_2.get(transaction=transaction)
        transaction.update(city_ref_1,{"population":snap2.to_dict()["population"]})
        transaction.update(city_ref_2,{"population":snap1.to_dict()["population"]})
        print("swap done")
    swap(transaction,city_ref_1,city_ref_2)
 #transaction3()

"""4. Simulate a failed transaction by performing a read after a write operation.
Observe and handle the resulting error."""
def transaction4():
    transaction=db.transaction()
    city_ref=db.collection("cities").document("NYC")
    @firestore.transactional
    def read_after_write(transaction,city_ref):
        transaction.update(city_ref,{"population":1000000})
        snapshot=city_ref.get(transaction=transaction)
        print(snapshot.to_dict()["population"])
    read_after_write(transaction,city_ref)
 #transaction4()
"""raise ReadAfterWriteError(READ_AFTER_WRITE_ERROR)
google.cloud.firestore_v1._helpers.ReadAfterWriteError: Attempted read after write in a transaction."""

# 5 Create a batch write that:

'''Sets data for "NYC",

Updates the "SF" population, and

Deletes the "DEN" document.'''

def batch_write5():
    batch=db.batch()
    data={"name":"New York","state":"NY","country":"USA","population":8000000}
    batch.set(db.collection("cities").document("NYC"),data)
    batch.update(db.collection("cities").document("SF"),{"population":1000000})
    batch.delete(db.collection("cities").document("DEN"))
    batch.commit()
    print("Batch Write Successful")
# batch_write5()

# 6 Use a batch write to add three new cities: "Paris", "Berlin", and "Tokyo".

def batch_write6():
    batch=db.batch()
    data1={"name":"Paris","state":"Paris","country":"France","population":2000000}
    data2={"name":"Berlin","state":"Berlin","country":"Germany","population":3000000}
    data3={"name":"Tokyo","state":"Tokyo","country":"Japan","population":4000000}
    batch.set(db.collection("cities").document("Paris"),data1)
    batch.set(db.collection("cities").document("Berlin"),data2)
    batch.set(db.collection("cities").document("Tokyo"),data3)
    batch.commit()
    print("Batch Write Successful")
#batch_write6()

# Implement a transaction that transfers money between two account documents ("Alice" → "Bob").Ensure it checks balances before transferring.

def transaction7():
    transaction=db.transaction()
    alice_ref=db.collection("accounts").document("Alice")
    bob_ref=db.collection("accounts").document("Bob")
    @firestore.transactional
    def transfer_money(transaction,alice_ref,bob_ref):
        alice_snapshot=alice_ref.get(transaction=transaction)
        bob_snapshot=bob_ref.get(transaction=transaction)
        if alice_snapshot.to_dict()["balance"]>0:
            transaction.update(alice_ref,{"balance":alice_snapshot.to_dict()["balance"]-1000})
            transaction.update(bob_ref,{"balance":bob_snapshot.to_dict()["balance"]+1000})
            print("Transaction Successful")
        else:
            print("Transaction Failed")
    transfer_money(transaction,alice_ref,bob_ref)
#transaction7()

# Write a batch delete that removes all users from the "users" collection where active == False.
def batch_delete8():
    batch=db.batch()
    users_ref=db.collection("users")
    users=users_ref.where(filter=FieldFilter("active","==","False")).stream()
    for doc in users:
        batch.delete(doc.reference)
    batch.commit()
    print("Batch Delete Successful")
#batch_delete8()

#9 Create a transaction that safely increments a "likes" counter on "posts/post1", ensuring concurrency safety.

def transaction9():
    transaction=db.transaction()
    post_ref=db.collection("posts").document("post1")
    @firestore.transactional
    def increment_likes(transaction,post_ref):
        snapshot=post_ref.get(transaction=transaction)
        transaction.update(post_ref,{"likes":snapshot.to_dict()["likes"]+1})
        print("Transaction Successful")
    increment_likes(transaction,post_ref)
#transaction9()

# 10 Use a batch write to update multiple department documents ("HR", "Engineering", "Sales") with a lastUpdated timestamp.

def batch_write10():
    batch=db.batch()
    departments_ref=db.collection("departments")
    departments=departments_ref.stream()
    for doc in departments:
        batch.update(doc.reference,{"lastUpdated":firestore.SERVER_TIMESTAMP})
    batch.commit()
    print("Batch Write Successful")
#batch_write10()

# 11 Create a transaction that decreases the stock of a product (products/product1) by a given quantity (e.g., 5) only if the stock is sufficient.
#If not enough stock exists, cancel the transaction and print a warning.
def transaction11():
    a=int(input("Enter the quantity: "))
    transaction=db.transaction()
    product_ref=db.collection("products").document("product1")
    @firestore.transactional
    def decrease_stock(transaction,product_ref):
        snapshot=product_ref.get(transaction=transaction)
        if snapshot.to_dict()["stock"]>a:
            transaction.update(product_ref,{"stock":snapshot.to_dict()["stock"]-1})
            print("Transaction Successful")
        else:
            print("Transaction Failed")
    decrease_stock(transaction,product_ref)
#transaction11()

## 12. Simultaneous Order Creation

#Use a batch write to:

#Create a new order document in the orders collection.

#Update the customer’s ordersCount field in customers/customer1.

#Set a timestamp in the analytics/orders document.

def batch_write12():
    batch=db.batch()
    order_ref=db.collection("orders").document()
    customer_ref=db.collection("customers").document("customer1")
    analytics_ref=db.collection("analytics").document("orders")
    batch.set(order_ref,{})
    batch.update(customer_ref,{"ordersCount":firestore.Increment(1)})
    batch.set(analytics_ref,{"timestamp":firestore.SERVER_TIMESTAMP})
    batch.commit()
    print("Batch Write Successful")
#batch_write12()

# Write a transaction that ensures all users in a groupMembers subcollection have a status of "active" before updating the parent groups/group1 document’s status field to "active".
def transaction13():
    transaction=db.transaction()
    group_ref=db.collection("groups").document("group1")
    members_ref=group_ref.collection("groupMembers")
    @firestore.transactional
    def update_status(transaction,group_ref,members_ref):
        members=members_ref.stream()
        for doc in members:
            if doc.to_dict()["status"]!="active":
                print("Transaction Failed")
                return
        transaction.update(group_ref,{"status":"active"})
        print("Transaction Successful")
    update_status(transaction,group_ref,members_ref)
#transaction13()

# 14. Points Transfer Between Users

# Implement a transaction that transfers 100 points from one user (users/Alice) to another (users/Bob).
# Make sure it checks if Alice has enough points before transferring.

def transaction14():
    transaction=db.transaction()
    alice_ref=db.collection("users").document("Alice")
    bob_ref=db.collection("users").document("Bob")
    @firestore.transactional
    def transfer_points(transaction,alice_ref,bob_ref):
        alice_snapshot=alice_ref.get(transaction=transaction)
        bob_snapshot=bob_ref.get(transaction=transaction)
        if alice_snapshot.to_dict()["points"]>100:
            transaction.update(alice_ref,{"points":alice_snapshot.to_dict()["points"]-100})
            transaction.update(bob_ref,{"points":bob_snapshot.to_dict()["points"]+100})
            print("Transaction Successful")
        else:
            print("Transaction Failed")
    transfer_points(transaction,alice_ref,bob_ref)
#transaction14()

# 15. Atomic Update for Inventory
#Use a batch write to:
#Increase stock for "item1", "item2", and "item3" by 10 each.
#Update their lastRestocked field with the current server timestamp.
def batch_write15():
    batch=db.batch()
    items_ref=db.collection("items")
    items=items_ref.stream()
    for doc in items:
        batch.update(doc.reference,{"stock":doc.to_dict()["stock"]+10})
        batch.update(doc.reference,{"lastRestocked":firestore.SERVER_TIMESTAMP})
    batch.commit()
    print("Batch Write Successful")
#batch_write5()

# 16. Post Like with Concurrency Safety

#Create a transaction that increments the likes count for posts/post1 safely (just like before),
# but also adds the user’s ID to a likedBy array using ArrayUnion.
def batch_write16():
    batch=db.batch()
    a=input("Enter the user ID: ")
    post_ref=db.collection("posts").document("post1")
    batch.update(post_ref,{"likes":firestore.Increment(1)})
    batch.update(post_ref,{"likedBy":firestore.ArrayUnion([a])})
    batch.commit()
    print("Batch Write Successful")
#batch_write5()

#17. Batch User Onboarding

#Using a batch write, add three new user documents:

#"userA", "userB", and "userC" with default fields {active: True, createdAt: SERVER_TIMESTAMP}.

def batch_write17():
    batch=db.batch()
    data1={"active":True,"createdAt":firestore.SERVER_TIMESTAMP}
    data2={"active":True,"createdAt":firestore.SERVER_TIMESTAMP}
    data3={"active":True,"createdAt":firestore.SERVER_TIMESTAMP}
    batch.set(db.collection("users").document("userA"),data1)
    batch.set(db.collection("users").document("userB"),data2)
    batch.set(db.collection("users").document("userC"),data3)
    batch.commit()
    print("Batch Write Successful")
#batch_write17()

# 18. Order Rollback Simulation

# Write a transaction that simulates order cancellation:

# Refunds the amount to the user’s wallet (users/user1.balance += order.total).

# Deletes the order document from orders/order123.
# Handle any errors gracefully.

def transaction18():
    transaction=db.transaction()
    user_ref=db.collection("users").document("user1")
    order_ref=db.collection("orders").document("order123")
    @firestore.transactional
    def rollback_order(transaction,user_ref,order_ref):
        user_snapshot=user_ref.get(transaction=transaction)
        order_snapshot=order_ref.get(transaction=transaction)
        transaction.update(user_ref,{"balance":user_snapshot.to_dict()["balance"]+order_snapshot.to_dict()["total"]})
        transaction.delete(order_ref)
        print("Transaction Successful")
    rollback_order(transaction,user_ref,order_ref)
#transaction18()

#19. Cascading Update

# Create a transaction that updates a city document and simultaneously updates the related country document’s lastUpdated timestamp (like the Firestore docs example).
def transaction19():
    transaction=db.transaction()
    city_ref=db.collection("cities").document("NYC")
    country_ref=db.collection("countries").document("USA")
    @firestore.transactional
    def update_cascade(transaction,city_ref,country_ref):
        transaction.update(city_ref,{"population":1000000})
        transaction.update(country_ref,{"lastUpdated":firestore.SERVER_TIMESTAMP})
        print("Transaction Successful")
    update_cascade(transaction,city_ref,country_ref)
#transaction19()    

# 20. Batch Cleanup

#Use a batch write to delete all documents in the collection logs where the timestamp is older than 7 days from now.

def batch_write20():
    batch=db.batch()
    logs_ref=db.collection("logs")
    logs=logs_ref.where(filter=FieldFilter("timestamp","<",datetime.datetime.now()-datetime.timedelta(days=7))).stream()
    for doc in logs:
        batch.delete(doc.reference)
    batch.commit()
    print("Batch Write Successful")
#batch_write20()

"""21. Atomic Multi-Collection Transaction

Write a transaction that:

Creates a new invoice document in invoices/.

Updates the related customer document’s totalSpent by the invoice’s amount.

Adds a reference to the invoice inside customers/{id}/invoicesList."""

def transaction21():
    transaction = db.transaction()
    invoice_ref = db.collection("invoices").document()
    customer_ref = db.collection("customers").document("customer1")

    @firestore.transactional
    def create_invoice(transaction, invoice_ref, customer_ref):
        customer_snapshot = customer_ref.get(transaction=transaction)
        amount = 500  # Example amount
        transaction.set(invoice_ref, {"amount": amount, "timestamp": firestore.SERVER_TIMESTAMP})
        transaction.update(customer_ref, {"totalSpent": firestore.Increment(amount)})
        transaction.set(customer_ref.collection("invoicesList").document(invoice_ref.id), {"invoiceRef": invoice_ref})
        print("Transaction Successful")

    create_invoice(transaction, invoice_ref, customer_ref)
#transaction21()

"""22. Transaction with Conditional Field Creation

Create a transaction that:

Checks if a profileCompletion field exists in users/user123.

If it doesn’t, set it to 0.

Then, increment it by 10 each time the transaction runs."""


def transaction22():
    transaction = db.transaction()
    user_ref = db.collection("users").document("user123")

    @firestore.transactional
    def update_profile_completion(transaction, user_ref):
        snapshot = user_ref.get(transaction=transaction)
        data = snapshot.to_dict()
        if "profileCompletion" not in data:
            transaction.update(user_ref, {"profileCompletion": 0})
        transaction.update(user_ref, {"profileCompletion": firestore.Increment(10)})
        print("Transaction Successful")

    update_profile_completion(transaction, user_ref)
#transaction22()

"""23. Transaction with Nested Data Validation

Implement a transaction that updates a projects/project1 document’s progress 
field to 100 only if all subtasks inside the projects/project1/subtasks subcollection have completed == True."""

def transaction23():
    transaction = db.transaction()
    project_ref = db.collection("projects").document("project1")
    subtasks_ref = project_ref.collection("subtasks")

    @firestore.transactional
    def complete_project(transaction, project_ref):
        subtasks = subtasks_ref.stream()
        for sub in subtasks:
            if not sub.to_dict().get("completed", False):
                print("Some subtasks incomplete — Transaction Cancelled")
                return
        transaction.update(project_ref, {"progress": 100})
        print("All subtasks done — Project marked complete")

    complete_project(transaction, project_ref)
#transaction23()

"""24. Cross-Collection Batch Write

Use a batch write to:

Update all documents in products collection where category == "electronics", adding the field discountApplied = True.

Update the analytics/discountStats document to record the current timestamp."""



def batch_write24():
    batch = db.batch()
    products = db.collection("products").where(filter=FieldFilter("category", "==", "electronics")).stream()
    for doc in products:
        batch.update(doc.reference, {"discountApplied": True})
    analytics_ref = db.collection("analytics").document("discountStats")
    batch.update(analytics_ref, {"lastUpdated": firestore.SERVER_TIMESTAMP})
    batch.commit()
    print("Batch Write Successful")
#batch_write24()

"""25. Conditional Delete Transaction

Create a transaction that:

Reads a comments/comment123 document.

Deletes it only if the flagCount field is greater than or equal to 3.

Otherwise, print "Not enough flags to delete"."""

def transaction25():
    transaction = db.transaction()
    comment_ref = db.collection("comments").document("comment123")

    @firestore.transactional
    def delete_if_flagged(transaction, comment_ref):
        snapshot = comment_ref.get(transaction=transaction)
        if snapshot.to_dict()["flagCount"] >= 3:
            transaction.delete(comment_ref)
            print("Comment deleted")
        else:
            print("Not enough flags to delete")

    delete_if_flagged(transaction, comment_ref)
#transaction25()

"""26. Batch Write with Mixed Operations

Use a single batch to:

Create one new promo document.

Update an existing settings document.

Delete an old archive document.
(All three must commit together.)"""


def batch_write26():
    batch = db.batch()
    promo_ref = db.collection("promos").document()
    settings_ref = db.collection("config").document("settings")
    archive_ref = db.collection("archives").document("oldArchive")

    batch.set(promo_ref, {"active": True, "created": firestore.SERVER_TIMESTAMP})
    batch.update(settings_ref, {"version": firestore.Increment(1)})
    batch.delete(archive_ref)
    batch.commit()
    print("Batch Write Successful")
#batch_write26()

"""27. Transaction with Multiple Increment Fields

Implement a transaction that:

Reads a users/user456 document.

Increments both postsCount and likesCount by 1 atomically."""

def transaction27():
    transaction = db.transaction()
    user_ref = db.collection("users").document("user456")

    @firestore.transactional
    def update_counters(transaction, user_ref):
        transaction.update(user_ref, {
            "postsCount": firestore.Increment(1),
            "likesCount": firestore.Increment(1)
        })
        print("Transaction Successful")

    update_counters(transaction, user_ref)
#transaction27()

"""28. Batch Write with Dynamic Query Results

Use a batch write to:

Delete all orders where status == "cancelled".

Then, create a summary document in reports/cleanup with the number of deleted documents."""


def batch_write28():
    batch = db.batch()
    cancelled_orders = db.collection("orders").where(filter=FieldFilter("status", "==", "cancelled")).stream()
    count = 0
    for order in cancelled_orders:
        batch.delete(order.reference)
        count += 1
    report_ref = db.collection("reports").document("cleanup")
    batch.set(report_ref, {"deletedOrders": count, "timestamp": firestore.SERVER_TIMESTAMP})
    batch.commit()
    print("Batch Write Successful")
#batch_write28()

"""29. Transaction for Payment Validation

Write a transaction that:

Reads an orders/order789 document.

Verifies that paymentStatus == "pending".

If yes, updates it to "completed" and increases the sellerRevenue in sellers/seller1 by the order’s amount."""

def transaction29():
    transaction = db.transaction()
    order_ref = db.collection("orders").document("order789")
    seller_ref = db.collection("sellers").document("seller1")

    @firestore.transactional
    def process_payment(transaction, order_ref, seller_ref):
        order_snapshot = order_ref.get(transaction=transaction)
        if order_snapshot.to_dict()["paymentStatus"] == "pending":
            amount = order_snapshot.to_dict()["amount"]
            transaction.update(order_ref, {"paymentStatus": "completed"})
            transaction.update(seller_ref, {"sellerRevenue": firestore.Increment(amount)})
            print("Payment processed")
        else:
            print("Order already processed")

    process_payment(transaction, order_ref, seller_ref)
#transaction29()

"""30. Batch Write with Array Operations

Use a batch to:

Add a new tag (input from user) to all documents in the posts collection using ArrayUnion.

Also update an analytics/tags document to include that same tag in its usedTags array."""

def batch_write30():
    batch = db.batch()
    tag = input("Enter new tag: ")
    posts = db.collection("posts").stream()
    for post in posts:
        batch.update(post.reference, {"tags": firestore.ArrayUnion([tag])})
    analytics_ref = db.collection("analytics").document("tags")
    batch.update(analytics_ref, {"usedTags": firestore.ArrayUnion([tag])})
    batch.commit()
    print("Batch Write Successful")
#batch_write30()



    

