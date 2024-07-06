import uuid
import boto3
from flask import Flask, render_template, request, redirect, url_for, session
import requests
import json

app = Flask(__name__)
app.secret_key = 'shilpa'

def set_global_username(username):
    session['username'] = username

def get_global_username():
    return session.get('username')

@app.route("/")
def home():
    return render_template('login.html')

# Login Logic
@app.route("/login", methods=['GET', 'POST'])
def login():
    response_data = {}
    if request.method == 'POST':
        login_url = 'https://quh3mswgoc.execute-api.us-east-1.amazonaws.com/Production/login'
        input_email = request.form['email']
        input_password = request.form['password']
       
        data = {
            'email': input_email,
            'password': input_password
        }
        response = requests.post(login_url, json=data)
        response_data = response.json()
        
        if response_data['statusCode'] == 200:
            username = response_data["body"]["user_name"]
            set_global_username(username)
            return redirect(url_for('main'))
        elif response_data['statusCode'] == 401:
            return render_template('login.html', error=response_data.get("body", ""))
    else:
        return render_template('login.html',error=response_data.get("body", ""))

# Registration Logic 
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        register_url = 'https://p413wciux5.execute-api.us-east-1.amazonaws.com/production/register'
        input_email = request.form['email']
        input_password = request.form['password']
        input_user_name = request.form['username']
        data = {
            "email": input_email,
            "password": input_password,
            "user_name": input_user_name
            }
        response = requests.post(register_url, json=data)
        response_data = response.json()
        
        if response_data.get('statusCode') == 200 :
            # Redirect to the login page after successful registration
            return redirect(url_for('login'))
        elif response_data['statusCode'] == 400:
            return render_template('register.html', error=response_data.get("body", ""))
    else:
        return render_template("register.html")

# Main Page Logic
@app.route("/main",methods=['GET','POST'])
def main():
    username = get_global_username()
    # Retrieve item details from the session
    item_details = session.get('item_details', [])

    subscribeDetails_url = 'https://ly5157l3s3.execute-api.us-east-1.amazonaws.com/Production/subscribedDetails'
    input_username = username
    data = {
            "user_name": input_username
            }
    response = requests.post(subscribeDetails_url, json=data)
    response_data = response.json()

    if response_data['statusCode'] == 200:
        subscribedDetails = response.json()["body"]
        return render_template("main.html", username=username,subscribed_music=subscribedDetails,item_details = item_details)
    else:
        return render_template('main.html', error=response_data['statusCode'])
    
# Unsubscribe Logic
@app.route("/unsubscribe", methods=["POST"])
def unsubscribe():
    username = get_global_username()
    title = request.form.get("title")
    if username and title:
        # Make a request to the unsubscribe endpoint
        unsubscribe_url = "https://me0x9678th.execute-api.us-east-1.amazonaws.com/Production/unsubscribe"
        data = {
            "user_name": username,
            "title": title
        }
        response = requests.post(unsubscribe_url, json=data)
        response_data = response.json()
        if response_data['statusCode'] == 200:
            return redirect(url_for('main'))
        elif response_data['statusCode'] == 404:
            return redirect(url_for('main'),error=response_data['statusCode'])
        
    return redirect(url_for('main'),error=response_data['statusCode'])

# Query Logic
@app.route("/query", methods=['POST'])
def query():
    title = request.form.get('title')
    year = request.form.get('year')
    artist = request.form.get('artist')

    data = {
        'title': title,
        'year': year,
        'artist': artist
    }

    response = requests.post('https://wgyhr8r646.execute-api.us-east-1.amazonaws.com/Production/queryDetails', json=data)
    response_data = response.json()
    item_details = response_data['body']
    session['item_details'] = item_details

    if response_data['statusCode'] == 200:
        return redirect(url_for('main'))
    elif response_data['statusCode'] == 404:
        return redirect(url_for('main'))
   
    
#Subscribe Logic
@app.route("/subscribe", methods=["POST"])
def subscribe():
    username = get_global_username()
    title = request.form.get("title")
    artist = request.form.get("artist")
    year = request.form.get("year")

    # Make a request to the unsubscribe endpoint
    subscribe_url = "https://p09wm42tc4.execute-api.us-east-1.amazonaws.com/Production/subscribe"
    data = {
        "user_name": username,
        "title": title,
        "artist": artist,
        "year": year,
    }
    response = requests.post(subscribe_url, json=data)
    response_data = response.json()
    if response_data['statusCode'] == 200:
        return redirect(url_for('main'))
    elif response_data['statusCode'] == 409:
        return redirect(url_for('main'))

#Logout Logic
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))  

#Creating the subscription table in dynamo Db logic
def create_subscribed_music_table():
    try:
        # Initialize DynamoDB client
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
        # Define table name
        table_name = 'subscribedMusicTable'

        # Create table if it doesn't exist
        if table_name not in dynamodb.tables.all():
            table = dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {
                        'AttributeName': 'id',
                        'KeyType': 'HASH'  # Partition key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'id',
                        'AttributeType': 'S'  # String type
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
            table.wait_until_exists()  # Wait until table is created
            
            print(f"Table '{table_name}' created successfully.")

    except Exception as e:
        print(f"Error creating table: {e}")
   
if __name__ == '__main__':
    create_subscribed_music_table()
    app.run(host='127.0.0.1', port=8080, debug=False)