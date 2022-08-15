from distutils.log import error
from multiprocessing import context
from django.shortcuts import render, redirect
from . import utils
import random
import smtplib, ssl
from email.message import EmailMessage



port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "ayaan.ali.63621@gmail.com"
# receiver_email = "owaisiqbal2013@gmail.com"
password = "brrhqkjnzdechdns"


def index(request, id):
    if(request.method == 'POST'):
        print(request.body)
        name=request.POST.get('name',False)
        email=request.POST.get('email',False)
        table_id=id
        user_otp=request.POST.get('otp-input',False)
        # print(name, email, table_id)
        otp=random.randint(11111,99999)
        # print(user_otp)
        if not user_otp:
            print(otp)
            utils.insertUser(name, email, table_id, otp)
            context = ssl.create_default_context()
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
            return render(request, 'dineIn/index.html', {'otp':otp})
        elif (not name) or (not email):
            verification=utils.verify_otp(user_otp)
            # print(user_otp)
            if verification[0]:
                return render(request ,'dineIn/order.html', {'user':verification[1]})
            else:
                return render(request, 'dineIn/index.html', {'login':otp, 'error':'Invalid OTP'})

    return render(request, 'dineIn/index.html', {'login':True, 'error':False})



def delete(request, id):
    delete_result = utils.delete_user_table(id)
    return redirect('index', id)

def food_menu(request, id):
    menu=utils.get_food_menu()
    user=utils.get_user(id)

    if(request.method == 'POST'):
        food_quantity = request.POST.dict()
        food_quantity.pop('csrfmiddlewaretoken')
        print("inside chckout", food_quantity)
        order={}
        for food_id in food_quantity:
            if food_quantity[food_id] != "0":
                if food_quantity[food_id] != "":
                    order[food_id] = food_quantity[food_id]
        print(order)
        return render(request, 'dineIn/checkout.html', {'order':order, 'table_id':id})
    return render(request, 'dineIn/food_menu.html', {'menu':menu, 'table_id':id, 'user':user})


def checkout(request, id):
    return render(request, 'dineIn/checkout.html', {'table_id':id})