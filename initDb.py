import firebase_admin
from firebase_admin import credentials, db, firestore
import json

cred = credentials.Certificate("smu-fo2024-smutopiabot-firebase-adminsdk-tt5im-6f3313e2ae.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
doc_ref = db.collection("books")

with open("book_info.json", "r") as f:
	file_contents = json.load(f)
doc_ref.set(file_contents)

