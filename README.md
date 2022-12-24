# Bubble Bop - Food Dine In
A Hotel Management system that takes the orders for each table, based on scanning the QR code available at the table.

A project for a Hackathon conducted by https://ineuron.ai 


## Installation

```bash
git clone https://github.com/Shades-en/Bubble-Bop-Food-Dine-In.git
cd ineuron
pip install -r requirements.txt
```
    
## Usage

(Replace the caps words with appropriate paramenters in the files)

ineuron/settings.py
```python
DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'NAME': 'YOUR_DATABASE_NAME',
            'CLIENT': {
                'host': 'CONNECTION_LINK' #YOUR_MONGODB_CONNECTION_LINK
            }  
        }
}
```

dineIn/utils.py
```python
client = MongoClient('CONNECTION_LINK',maxPoolSize=50, wTimeoutMS=2500) #atlas connection
db = client['YOUR_DATABASE_NAME']
food_collection=db['DATABASENAME_foodmenu']
user_collection=db['DATABASENAME_user']
table_collection=db['DATABASENAME_table']
bill_collection=db['DATABASENAME_bill']
```

dineIn/views.py
```python
sender_email = "YOUR_SENDER_EMAIL" # Enter the sender email address
password = "APP_PASSWORD" #app password
```

BASH
```bash
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```

Load the .json files (table.json, foodmenu.json) into DATABASENAME_table and DATABASENAME_foodmenu.

## Contributors For Frontend
* [Adeeb K.M](https://github.com/adeebkm)
* [Aman Clement](https://github.com/Aman-Clement)
* [Lava Kumar Gowda M A](https://github.com/nameisluv)


## Tech Stack

**Client:** HTML, CSS, Javascript

**Server:** Python(Django), MongoDb
