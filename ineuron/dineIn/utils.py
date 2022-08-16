from functools import total_ordering
from pymongo import MongoClient
from django.utils import timezone
from bson.objectid import ObjectId

client = MongoClient('mongodb+srv://IS081:msr123@cluster0.dl94m.mongodb.net/test', maxPoolSize=50, wTimeoutMS=2500)
db = client['DineinDB']
food_collection=db['FoodMenu']
user_collection=db['Users']
table_collection=db['Table']
bill_collection=db['Bills']

# def insertFoodOps():
#     insert_result = food_collection.insert_one({"name": "Barbequeue Chicken", "type": "non-veg", "category": "Main Course", "price": 150, "description": "Chicken marinated in a spicy blend of spices, served with a side of salad and rice.", "image": "https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"})

def insertUser(name, email, table_id, otp):
    try:
        table = table_collection.find_one({"number":table_id})
        print(table)
        if table["status"]=="available":
            insert_result = user_collection.insert_one({"name": name, "email":email, "tableNo":table_id, "otp":otp, "otp_verified":False})
            return insert_result
        else:
            return False
    except Exception as e:
        print(e)

def insertTable(table_no):
    insert_result = table_collection.insert_one({"number": table_no, "status": "occupied", "capacity": "5"})
    return insert_result

def verify_otp(otp):
    try:
        user = user_collection.find_one({"otp":int(otp)})
        print(user)
        if user is not None:
            try:
                update_result = user_collection.update_one({"otp":int(otp)}, {"$set":{"otp_verified":True}}, upsert=True)
                # print(update_result.raw_result)
            except:
                print("Error in updating otp_verified")
            
            table_no=user.get("tableNo")
            try:
                update_result=table_collection.update_one({"number":table_no}, {"$set":{"status":"occupied"}})
            except Exception as e:
                return e
            return [True, user]
        else:
            return [False, user]
    except Exception as e:
        return e

def delete_unverified(email):
    try:
        print(email)
        delete_user_result = user_collection.delete_many({"otp_verified": False, "email":email})
        return delete_user_result
    except Exception as e:
        print(e)
        return e

def delete_user_table(table_no, user):
    try:
        update_result=table_collection.update_one({"number":table_no}, {"$set":{"status":"available"}})
        delete_user_result = user_collection.delete_many({"tableNo":table_no, "email":user["email"]})
        return [update_result, delete_user_result]
    except Exception as e:
        print(e)
        return e

def get_food_menu():
    try:
        starters = food_collection.find({"category": "starters"})
        main_course = food_collection.find({"category": "main_course"})
        deserts = food_collection.find({"category": "deserts"})
        drinks = food_collection.find({"category": "drinks"})
        combo = food_collection.find({"category": "combo"})
        pizza = food_collection.find({"category": "pizza"})
        burger = food_collection.find({"category": "burger"})

        food_menu = {
            "starters": list(starters),
            "main_course": list(main_course),
            "deserts": list(deserts),
            "drinks": list(drinks),
            "combo": list(combo),
            "pizza": list(pizza),
            "burger": list(burger),
        }
        return food_menu
    except Exception as e:
        return e

def get_user(table_no):
    try:
        user = user_collection.find_one({"tableNo":table_no})
        return user
    except Exception as e:
        return e 

def get_food(id):
    try:
        food_item = food_collection.find_one({"_id": ObjectId(id)})
        return food_item
    except Exception as e:
        return e

def generate_bill(orders):
    total=0
    for order in orders:
        total += int(order[1])*order[0]["price"]
    tax=0.1*total
    final_amt=total+tax
    return {"total" : total, "tax" : tax, "final_amt" : final_amt}

def save_bill(bill):
    bill["status"] = "unpaid"
    bill["time"] = timezone.now()
    try:
        insert_result = bill_collection.insert_one(bill)
        return insert_result
    except Exception as e:
        return e

