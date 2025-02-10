import os
from functools import reduce
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from bson import ObjectId

uri = "mongodb://mongo:27017/"
client = MongoClient(uri)
database = client["students_db"]
students_collection = database["students_collection"]


def add(student=None):
    query = {"first_name": student.first_name, "last_name": student.last_name}
    res = students_collection.find_one(query)
    if res:
        return 'already exists', 409

    result = students_collection.insert_one(student.to_dict())
    student.student_id = str(result.inserted_id)
    print(student)
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
