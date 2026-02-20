from pymongo import MongoClient
from config import MONGO_URI, DB_NAME
from datetime import datetime
from bson import ObjectId
import bcrypt
import secrets

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_col = db["users"]
history_col = db["history"]

def create_user(name, email, password):
    if users_col.find_one({"email": email}):
        return False, "Email already registered"
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users_col.insert_one({"name": name, "email": email, "password": hashed, "created_at": datetime.utcnow()})
    return True, "Account created successfully"

def verify_user(email, password):
    user = users_col.find_one({"email": email})
    if user and bcrypt.checkpw(password.encode(), user["password"]):
        return user
    return None

def get_user_by_email(email):
    return users_col.find_one({"email": email})

def update_password(email, new_password):
    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    users_col.update_one({"email": email}, {"$set": {"password": hashed}})

def generate_otp(email):
    otp = secrets.randbelow(900000) + 100000
    users_col.update_one({"email": email}, {"$set": {"otp": str(otp), "otp_time": datetime.utcnow()}})
    return str(otp)

def verify_otp(email, otp):
    user = users_col.find_one({"email": email})
    if user and user.get("otp") == otp:
        return True
    return False

def save_history(user_email, language, original_code, review_data, rewritten_code):
    history_col.insert_one({
        "user_email": user_email,
        "language": language,
        "original_code": original_code,
        "review_data": review_data,
        "rewritten_code": rewritten_code,
        "created_at": datetime.utcnow()
    })

def get_history(user_email):
    records = list(history_col.find({"user_email": user_email}).sort("created_at", -1))
    for r in records:
        r["_id"] = str(r["_id"])
        r["created_at"] = r["created_at"].strftime("%Y-%m-%d %H:%M")
    return records

def get_history_by_id(record_id):
    try:
        r = history_col.find_one({"_id": ObjectId(record_id)})
        if r:
            r["_id"] = str(r["_id"])
            r["created_at"] = r["created_at"].strftime("%Y-%m-%d %H:%M")
        return r
    except:
        return None

def delete_history_by_id(record_id, user_email):
    try:
        result = history_col.delete_one({"_id": ObjectId(record_id), "user_email": user_email})
        return result.deleted_count > 0
    except:
        return False

def delete_all_history(user_email):
    result = history_col.delete_many({"user_email": user_email})
    return result.deleted_count