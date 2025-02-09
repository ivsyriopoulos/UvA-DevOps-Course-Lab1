import os
from functools import reduce
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from bson import ObjectId

try:
    uri = "mongodb://mongo:27017/"
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    database = client["students_db"]
    students_collection = database["students_collection"]
    client.server_info()  # Force connection test
except ServerSelectionTimeoutError:
    print("MongoDB server is not available. Check connection settings.")


def add(student=None):
    print(f'searching for student {student}')
    query = {"first_name": student.first_name, "last_name": student.last_name}

    print("query database")
    dbnames = client.list_database_names()
    if 'students_db' in dbnames:
        list_of_collections = database.list_collection_names()
        if "students_db" in list_of_collections:
            res = students_collection.find_one(query)
            if res:
                return 'already exists', 409

    print(f'No student found, inserting')
    result = students_collection.insert_one(student.to_dict())
    print(f'inserted {result.inserted_id}')
    student.student_id = str(result.inserted_id)
    return student.student_id

def get_by_id(student_id=None, subject=None):
    try:
        student = students_collection.find_one({"_id": ObjectId(student_id)})
        if not student:
            return 'not found', 404
        student['student_id'] = str(student['_id'])
        del student['_id']  # Remove MongoDB's default _id field
        print(student)
        return student
    except Exception:
        return 'invalid ID', 400

def delete(student_id=None):
    try:
        result = students_collection.delete_one({"_id": ObjectId(student_id)})
        if result.deleted_count == 0:
            return 'not found', 404
        return student_id
    except Exception:
        return 'invalid ID', 400
