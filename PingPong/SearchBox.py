from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineListItem
import pyrebase

#configuring firebase database for pyrebase
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
#intitialize firebase database with pyrebase
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
base = db.get()

#store all dictionary from firebase in a list
fire = []
for i in base: fire.append(i.val())

class SearchBox(Screen):
    def open(self):
        MDApp.get_running_app().root.ids['sm'].current = 'search'

    #takes the text that user writes and shows results accordingly
    def take(self, user_text):
        app = MDApp.get_running_app()

        layout = app.root.ids['search'].ids['grid']
        count = 0

        #iterates dictionary in firebase list
        for item in fire:
            if item != None:
                for key, val in item.items():
                    if isinstance(val, int) == False: #checks if the value is not an integer, because integer don't have objects cannot be iterated
                        if user_text.lower() in val.lower():
                            if user_text == "" : pass #if user writes nothing and presses search, do nothing
                            else:
                                #eshow the result of each data one time only
                                name= str(item['Name'])
                                category = str(item['Category'])

                                #show category and name in search result
                                #if user clicks the particular list, pass the name of organisation to change_screen function
                                line = TwoLineListItem(text= name, secondary_text= category, on_press= lambda x:self.change_screen(x.text))
                                layout.add_widget(line)
                                count = count - 1
                                break
                        else:
                            count = count + 1
                else:
                    #if user input not found in the data, shows "No result found"
                    if count/5 == len(list(item.values())):
                        app.Not_text = "No Result Found"

    #clears the screen, or removes the children from the widget
    def clear(self):
        app = MDApp.get_running_app()
        if app.root.ids['search'].ids['add'].text == "":
            layout = app.root.ids['search'].ids['grid']
            children = list(layout.children)
            for i in children: layout.remove_widget(i)
        app.Not_text = ""

    def change_screen(self, name):
        app = MDApp.get_running_app()
        for i in fire:
            if i!= None:
                #if name found in the firebase database, pass the dictionary to Get_Info function and change screen
                if name in i.values():
                    app.data.Get_Info(i)
        app.change_screen('info', 'forward')

    #if hospital card is clicked in home screen, open list of all hospitals
    def hospital(self):
        app = MDApp.get_running_app()
        layout = app.root.ids['hospital'].ids['hospital_layout']
        for i in fire:
            if i != None:
                for j in i:
                    if i[j] == 'Hospital':
                        name= str(i['Name'])
                        category = str(i['Category'])
                        line = TwoLineListItem(text= name, secondary_text= category, on_press= lambda x:self.change_screen(x.text))
                        layout.add_widget(line)
        app.change_screen('hospital', 'forward')

    def blood(self):
        app = MDApp.get_running_app()
        layout = app.root.ids['blood'].ids['blood_layout']
        for i in fire:
            if i != None:
                for j in i:
                    if i[j] == 'BloodBank':
                        name= str(i['Name'])
                        category = str(i['Category'])
                        line = TwoLineListItem(text= name, secondary_text= category, on_press= lambda x:self.change_screen(x.text))
                        layout.add_widget(line)
        app.change_screen('blood', 'forward')

    def vaccine(self):
        app = MDApp.get_running_app()
        layout = app.root.ids['vaccine'].ids['vaccine_layout']
        for i in fire:
            if i != None:
                for j in i:
                    if i[j] == 'Vaccine center':
                        name= str(i['Name'])
                        category = str(i['Category'])
                        line = TwoLineListItem(text= name, secondary_text= category, on_press= lambda x:self.change_screen(x.text))
                        layout.add_widget(line)
        app.change_screen('vaccine', 'forward')

    def NGO(self):
        app = MDApp.get_running_app()
        layout = app.root.ids['ngo'].ids['ngo_layout']
        for i in fire:
            if i != None:
                for j in i:
                    if i[j] == 'NGO':
                        name= str(i['Name'])
                        category = str(i['Category'])
                        line = TwoLineListItem(text= name, secondary_text= category, on_press= lambda x:self.change_screen(x.text))
                        layout.add_widget(line)
        app.change_screen('ngo', 'forward')