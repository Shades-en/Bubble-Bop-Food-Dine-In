from pymongo import MongoClient
from django.utils import timezone

client = MongoClient('mongodb+srv://IS081:msr123@cluster0.dl94m.mongodb.net/test', maxPoolSize=50, wTimeoutMS=2500)
db = client['DineinDB']
food_collection=db['FoodMenu']
user_collection=db['Users']
table_collection=db['Table']

# def insertFoodOps():
#     insert_result = food_collection.insert_one({"name": "Barbequeue Chicken", "type": "non-veg", "category": "Main Course", "price": 150, "description": "Chicken marinated in a spicy blend of spices, served with a side of salad and rice.", "image": "https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"})

def insertUser(name, email, table_id, otp):
    try:
        insert_result = user_collection.insert_one({"name": name, "email":email, "tableNo":table_id, "otp":otp, "otp_verified":False, "orders":[]})
    except Exception as e:
        print(e)

def insertTable(table_no):
    insert_result = table_collection.insert_one({"number": table_no, "status": "occupied", "capacity": "5", "order":None, "totalPrice":0, "order_payment_amount":0, "order_payment_status":None, "order_payment_id":None, "order_no":None, "order_time":None, "order_date":None, "order_status":None})
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
            
            # print(user.get("name"), user.get("email"), user.get("tableNo"), user.get("otp"), user.get("otp_verified"))
            table_no=user.get("tableNo")
            try:
                insert_result=insertTable(table_no)
                # print(insert_result)
            except Exception as e:
                return e
            return [True, user]
        else:
            return [False, user]
    except Exception as e:
        return e

def delete_user_table(table_no):
    try:
        delete_table_result = table_collection.delete_one({"number":table_no})
        delete_user_result = table_collection.delete_many({"otp_verified": False, "tableNo":table_no})
        return [delete_table_result, delete_user_result]
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
        # print(food_menu["deserts"])
        return food_menu
        # return [starters, main_course, deserts, drinks, combo, pizza, burger]
    except Exception as e:
        return e

def get_user(table_no):
    try:
        user = user_collection.find_one({"tableNo":table_no})
        return user
    except Exception as e:
        return e


def users_get_updated( id):
    try:
        user = user_collection.find_one({"_id":id})
        return user
    except Exception as e:
        return e
