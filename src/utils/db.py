from pymongo import MongoClient
import os

print(os.environ.get("DATABASE_URL"))
#
client = MongoClient(os.environ.get("DATABASE_URL"))

print(os.environ.get("DB_NAME"))

db = client[os.environ.get("DB_NAME")]

user_collection = None
if not "user" in db.list_collection_names():
  user_collection = db.create_collection("user", validator={
    "$jsonSchema": {
      "bsonType": "object",
      "required": [ "username", "password" ],
      "properties": {
        "username": {
          "bsonType": "string",
          "minLength": 3,
          "maxLength": 20
        }
      },
    }
  })
  user_collection.create_index("username", unique=True)
else:
  user_collection = db["user"]

record = {
  "username": "testfussSss1",
  "password": "secret"
}

record = user_collection.insert_one(record).inserted_id

cursor = user_collection.find_one(record)
print(cursor)

cursor = user_collection.find({"_id": record, "username": "other user"})
for record in cursor:
  print(record)
