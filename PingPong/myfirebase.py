import requests
import json
from kivymd.app import MDApp
import pyrebase

#configuring firebase database
firebaseConfig = {
    'apiKey': "AIzaSyAuAaFfZs3LZqw6jb6j5kXevW9xWELqVPU",
    'authDomain': "blood-1fd81.firebaseapp.com",
    'databaseURL': "https://blood-1fd81-default-rtdb.firebaseio.com",
    'projectId': "blood-1fd81",
    'storageBucket': "blood-1fd81.appspot.com",
    'messagingSenderId': "1087397314682",
    'appId': "1:1087397314682:web:5b2ee48960ab171d2bbbc3",
    'measurementId': "G-9HGF4NJD4L"
  }
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

FIREBASECONFIG = {
    'apiKey': "AIzaSyBSIUxEEr0eT99VZTULGvAm1lGwyp1Oon8",
    'authDomain': "appdev-582ff.firebaseapp.com",
    'databaseURL': "https://appdev-582ff-default-rtdb.firebaseio.com",
    'projectId': "appdev-582ff",
    'storageBucket': "appdev-582ff.appspot.com",
    'messagingSenderId': "280833851292",
    'appId': "1:280833851292:web:c2c3bfd15677ddceff9259",
    'measurementId': "G-MP0BG2GW7S"
}
firebase_app = pyrebase.initialize_app(FIREBASECONFIG)
database = firebase_app.database()

class MyFirebase():
    web_api = "AIzaSyBSIUxEEr0eT99VZTULGvAm1lGwyp1Oon8" #my database api

    #takes users email and password and sign the new users
    def SignUp(self, email, password, first_name, last_name, age, sex):
        app = MDApp.get_running_app()

        #sends the request to the google api and sends the email and password and receives a response
        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" +self.web_api
        sign_data = {"email": email, "password": password, "returnSecureToken": True}
        sign_request = requests.post(signup_url, data = sign_data)
        signup_data = json.loads(sign_request.content.decode())
        print(sign_request.ok)
        print(sign_request.content.decode())

        if sign_request.ok == True:
            #getting refresh token, local id and id token from response
            refresh_token = signup_data['refreshToken']
            localId = signup_data['localId']
            id_token = signup_data['idToken']
            with open("refershToken.txt", "w") as f:  #saving refresh token in a file
                f.write(refresh_token)
            app.local = localId             #saving local id and idToken to a variable in main.py
            app.idToken = id_token
            name = first_name + " " + last_name
            data = '{"Name": %s, "Age": %d, "Sex": %s}'%(name,age,sex)
            requests.post("https://appdev-582ff-default-rtdb.firebaseio.com/" + localId + ".json?auth=" + id_token, data = data)
            app.change_screen('home', 'forward')

        #if cannot sign in, show the error message
        if sign_request.ok == False:
            error = json.loads(sign_request.content.decode())
            error_msg = error["error"]["message"]
            app.root.ids['sign'].ids['error'].text = error_msg

    def ExchangeToken(self,refresh_token):
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.web_api
        refresh_data = '{"grant_type": "refresh_token", "refresh_token": "%s"}' % refresh_token
        refresh_req = requests.post(refresh_url, data = refresh_data)
        print("refresh ok?: ", refresh_req.ok)
        print(refresh_req.json())
        local_id = refresh_req.json()['user_id']
        id_token = refresh_req.json()['id_token']
        return id_token, local_id

    #to login existing user
    def Login(self, email, password):
        app = MDApp.get_running_app()
        login_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + self.web_api
        login_data = {"email": email, "password": password, "returnSecureToken": True}
        login_req = requests.post(login_url, data = login_data)
        log = json.loads(login_req.content.decode())

        if login_req.ok == True:
            refresh_token = log['refreshToken']
            localId = log['localId']
            id_token = log['idToken']
            with open("refershToken.txt", "w") as f:  #saving refresh token in a file
                f.write(refresh_token)
            result = requests.get("https://appdev-582ff-default-rtdb.firebaseio.com/" + localId + ".json?auth=" + id_token)
            print(result.json())
            app.change_screen('home', 'forward')

        if login_req.ok == False:
            error = json.loads(login_req.content.decode())
            error_msg = error["error"]["message"]
            app.root.ids['login'].ids['error'].text = error_msg

    def submit(self, name, category, email, phone, address):
        data={'Name': name, 'Category': category, 'email': email, 'phone': phone, 'Address': address}
        db.push(data)