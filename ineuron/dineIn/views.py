from django.shortcuts import render, redirect
from . import utils
import random
import smtplib, ssl
from email.message import EmailMessage

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "YOUR_SENDER_EMAIL" # Enter the sender email address
password = "APP_PASSWORD" #app password

def index(request, id):
    if(request.method == 'POST'):
        print(request.body)
        name=request.POST.get('name',False)
        email=request.POST.get('email',False)
        table_id=id
        user_otp=request.POST.get('otp-input',False)
        otp=random.randint(11111,99999)
        if not user_otp:
            print(otp)
            success = utils.insertUser(name, email, table_id, otp)
            if success is False:
                return render(request, 'dineIn/index.html', {'login':otp, 'error':'Table Occupied'})
            context = ssl.create_default_context()
            print("Certificate created")
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls(context=context)
                server.login(sender_email, password)
                msg = EmailMessage()
                message="""\
                        Subject: Bubble Bop - OTP

                        Your OTP is: """+str(otp)
                msg.set_content(message)
                msg['Subject'] = 'Bubble Bop - OTP'
                msg['From'] = sender_email
                msg['To'] = email
                server.send_message(msg)
            print("email sent")
            return render(request, 'dineIn/index.html', {'otp':otp})
        elif (not name) or (not email):
            verification=utils.verify_otp(user_otp)
            print(verification)
            if verification[0]:
                delete_result = utils.delete_unverified(verification[1].get("email"))
                return render(request ,'dineIn/order.html', {'user':verification[1]})
            else:
                return render(request, 'dineIn/index.html', {'login':otp, 'error':'Invalid OTP'})
    return render(request, 'dineIn/index.html', {'login':True, 'error':False})

def delete(request, id):
    user=utils.get_user(id)
    delete_result = utils.delete_user_table(id, user)
    return redirect('index', id)

def food_menu(request, id, otp, user_id):
    menu=utils.get_food_menu()
    user=utils.get_user(id)
    if(request.method == 'POST'):
        food_quantity = request.POST.dict()
        food_quantity.pop('csrfmiddlewaretoken')
        final_amt = request.POST.get('final_amt', False)
        tax = request.POST.get('tax', False)
        total = request.POST.get('total', False)
        if final_amt:
            food_quantity.pop('total')
            food_quantity.pop('tax')
            food_quantity.pop('final_amt')
            final_bill={}
            items={}
            virt_id = utils.generate_virt_id(utils.bill_collection)
            final_bill["id"] = virt_id
            for item_id in food_quantity:
                food_item = utils.get_food(item_id)
                food_name=food_item["name"]
                items[food_name]=food_quantity[item_id]+" * "+ str(food_item["price"])
            final_bill["total"]=total
            final_bill["tax"]=tax
            final_bill["final_amt"]=final_amt
            final_bill["items"]=items
            temp=utils.get_user(id)
            temp.pop("_id")
            final_bill["user"]=temp
            utils.save_bill(final_bill)     
        else:
            orders=[]
            for food_id in food_quantity:
                if food_quantity[food_id] != "0":
                    if food_quantity[food_id] != "":
                        food_item = utils.get_food(food_id)
                        orders.append([food_item, food_quantity[food_id]])
            bill=utils.generate_bill(orders)
            return render(request, 'dineIn/checkout.html', {'orders':orders, 'table_id':id, 'user':user, "bill":bill})
    return render(request, 'dineIn/food_menu.html', {'menu':menu, 'table_id':id, 'user':user})

