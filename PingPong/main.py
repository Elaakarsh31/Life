from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, NoTransition, CardTransition
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from kivymd.uix.button import MDFillRoundFlatButton
from myfirebase import MyFirebase
from SearchBox import SearchBox
from InfoScreen import InfoScreen
import requests
import json
from kivy.core.window import Window

Window.size = (400,560)

Builder.load_file("homescreen.kv")

class HomeScreen(Screen):
    pass

class FirstScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class SignScreen(Screen):
    pass

class Search(SearchBox):
    pass

class Details(InfoScreen):
    pass

class Others(Screen):
    pass

class Main(MDApp):
    search_menu = Search()
    data = Details()
    result = StringProperty()
    Not_text = StringProperty()

    def build(self):
        #self.theme_cls.theme_style= "Dark"
        self.my_firebase = MyFirebase()     #declaring a variable in main file of Myfirebase class to perform database operations
        GUI = Builder.load_file("main.kv")     #This Builder method loads the code written in 'main.kv' file
        return GUI                                  #and we are returning the main kv code

    def on_start(self):
        #This is for PERSISTENT LOGIN..so that everytime the user opens the app, he/she doesn't has to login again and again
        #on start of the application, try to open a file called 'refreshToken.txt' and check if it contains any refresh token
        try:
            with open("refershToken.txt", 'r') as f:
                refresh_token = f.read()
            id_token, local_id = self.my_firebase.ExchangeToken(refresh_token) #if refresh token is found, we use it to get the User's ID token
                                                                            #and local ID token using the variable we created above and using ExhchaneToken() method of firebase

            #we then use requests to get the data from firebase using the database url and user's local-id and id-token we got from above
            result = requests.get("https://appdev-582ff-default-rtdb.firebaseio.com/" + local_id + ".json?auth=" + id_token)

            self.change_screen("home", "None") #change the screen to home screen
            print("res ok: ", result.ok) #this gives True if the data got retrieved otherwise returns False

        except: pass

    #this is a method to change the screen
    def change_screen(self, screen_name, direction='left', mode=""):
        # Get the screen manager from the kv file
        screen_manager = self.root.ids['sm']
        #print(direction, mode)
        # If going backward, change the transition. Else make it the default
        # Forward/backward between pages made more sense to me than left/right
        if direction == 'forward':
            mode = "push"
            direction = 'left'
        elif direction == 'backward':
            direction = 'right'
            mode = 'pop'
        elif direction == "None":   #when no direction, do not do screen transition
            screen_manager.transition = NoTransition()
            screen_manager.current = screen_name
            return

        screen_manager.transition = CardTransition(direction=direction, mode=mode) #else do the default card transition

        screen_manager.current = screen_name

    def clear_info(self):       #this method clears the information on the Information Screen when the user presses "Back" button
        app = MDApp.get_running_app()
        details= app.root.ids['info'].ids['details']    #get the 'details' (stored in GridLayout) from the kv file
        map=app.root.ids['info'].ids['map']             #get the map (stored in GridLayout) from kv file
        d = list(details.children)
        m = list(map.children)
        for i in d: details.remove_widget(i)   #remove all the information
        for i in m: map.remove_widget(i)        #remove the map

    def clear_card(self, screen, id):   #this is the general clearing screen method for the cards in homescreen
        app = MDApp.get_running_app()
        layout =app.root.ids[screen].ids[id] #get the screen name and id of the widget
        l = list(layout.children)
        for i in l: layout.remove_widget(i)     #then remove all its children
        self.change_screen('home', 'backward')  #and change screen to home screen


Main().run()