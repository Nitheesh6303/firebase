import firebase_admin
from firebase_admin import credentials, firestore
import time

cred = credentials.Certificate("app.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

sakshi_ref = db.collection("users").document("Sakshi")
Nitheesh_ref = db.collection("users").document("Nitheesh")
Dimple_ref = db.collection("users").document("Dimple")

collection_ref = db.collection("cities")

## collection Listener
def on_collection(col_snapshot, changes, read_time):
    print("\n Collection Change Detected:")
    for change in changes:
        if change.type.name == "ADDED":
            print(f"New Document Added: {change.document.id}")
        elif change.type.name == "MODIFIED":
            print(f"Document Modified: {change.document.id}")
        elif change.type.name == "REMOVED":
            print(f"Document Removed: {change.document.id}")


# document Listener
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print("\n Document Updated:")
        print(doc.id, "=>", doc.to_dict())

# Attach listener
sakshi_ref.on_snapshot(on_snapshot)
Nitheesh_ref.on_snapshot(on_snapshot)
Dimple_ref.on_snapshot(on_snapshot)
collection_ref.on_snapshot(on_collection)

# Listen for changes

print("Listening for document and Collection changes...")

# Keep script running
while True:
    time.sleep(1)
