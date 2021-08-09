from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivy.network.urlrequest import UrlRequest

class InfoScreen(Screen):
    def Get_Info(self, dic): #this gets the dictionary of the list that the user clicked
        app = MDApp.get_running_app()
        layout= app.root.ids['info'].ids['details'] #get the grid layout of id- 'detials'

        #formating the information and adding
        for key,value in dic.items():
            data = str(key) + ": " + str(value)
            label = MDLabel(text= data, halign= 'left', size_hint_y= 0.2)
            layout.add_widget(label)

        #removing spaces from the address given in the dictionary to get latitude and longitude of the place
        address = dic['Address']
        address = address.replace(" ","")
        self.get_lat_long(address)

    #this methods takes the address, sends it to geocoder api and in return gets the latitude and longitude of the address
    def get_lat_long(self, address):
        api = "tIyW4ub3gZiN_G6VXydONyxrarTRI6LiZ6wKTHfIU8s"
        url = "https://geocoder.ls.hereapi.com/6.2/geocode.json?searchtext=%s&apiKey=%s"%(address, api)
        UrlRequest(url, on_success=self.success, on_failure= self.failure, on_error= self.error)

    def success(self, urlrequest, result):
        print("success")
        app = MDApp.get_running_app()

        #get the latitude and longitude from response which is stored in result
        latitude = result['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Latitude']
        longitude = result['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Longitude']

        # get the map gridlayout and put latitude and longitude received and place a marker
        layout = app.root.ids['info'].ids['map']
        map = MapView(lat =latitude,lon=longitude, zoom=10 )
        marker = MapMarker()
        marker.source = "C:\\Users\\aakar\\Desktop\\VSCODE\\marker.png"
        marker.lat = latitude
        marker.lon=longitude
        map.add_widget(marker)
        layout.add_widget(map)
        print(latitude, longitude)

    def failure(self, urlrequest, result):
        print("fail")
        print(result)

    def error(self, urlrequest, result):
        print("error")
        print(result)