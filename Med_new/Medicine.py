import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.audio import SoundLoader
from functools import partial
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.textinput import TextInput

import wrapper
import sms

from datetime import datetime
from threading import Timer
import smtplib

import pigpio
import sys
import time
import random

db = wrapper.Wrapper()

Window.clearcolor = get_color_from_hex("0066BA")

#root
class ServoControl"
    def servo_rotate(self, g):
        pi = pigpio.pi()
        pi.set_servo_pulsewidth(g[0], 1300)
        time.sleep(g[1])
        pi.set_servo_pulsewidth(g, 0)
        
        pi.stop

class MainScreen(BoxLayout):
    user = ""
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        
    def changeScreen(self, next_screen):

        if next_screen == "confirm":
            #user=wrapper.select()
            #if user.length > 0:
                #self.user = user.name()
            self.ids.kivy_screen_manager.current = "start_screen"

        if next_screen == "biogesic":
            self.ids.kivy_screen_manager.current = "first_screen"

        if next_screen == "buscopan":
            self.ids.kivy_screen_manager.current = "second_screen"

        if next_screen == "decolgen no-drowse":
            self.ids.kivy_screen_manager.current = "third_screen"

        if next_screen == "dolfenal":
            self.ids.kivy_screen_manager.current = "fourth_screen"

        if next_screen == "solmux":
            self.ids.kivy_screen_manager.current = "fifth_screen"

        if next_screen == "back to main screen":
            self.ids.kivy_screen_manager.current = "start_screen"


    def transaction(self, medName):
        result = db.select('medicine', **{'medName': medName})
        medID = result[0]['mid']
        medCount = int(result[0]['count']) - 1
        
        db.update('medicine', 'medName', medName, **{'count':medCount})
        transValues = {'uid':self.user, 'mid':medID, 'datetime':datetime.now(), 'presentCount':medCount}
        db.insert('medicine', **transValues)
        
        if medCount <= 5:
            text = "The medicine " + medName +" is near depletion, please refill."
            sms.send_msg(text)
            
        #medName':(pin, delay)
        pindelay = {'Biogesic':(4,4), 'Buscopan':(6,4), 'Decolgen':(), 'DecolgenND':(), 'Solmux': ()}
        self.dispense(pindelay[medName])
        
           
    def pop1(self):
        self.pop = Popup(title='Information', content=Image(source='biogesic.png'),
                    size_hint=(None, None), pos=(30,30) ,size=(650, 600))
        self.pop.open()

    def pop2(self):
        self.pop = Popup(title='Information', content=Image(source='buscopan.png'),
                    size_hint=(None, None), pos=(30,30) ,size=(650, 600))
        self.pop.open()

    def pop3(self):
        self.pop = Popup(title='Information', content=Image(source='decolgen.png'),
                    size_hint=(None, None), pos=(30,30) ,size=(650, 600))
        self.pop.open()

    def pop4(self):
        self.pop = Popup(title='Information', content=Image(source='dolfenal.png'),
                    size_hint=(None, None), pos=(30,30) ,size=(650, 600))
        self.pop.open()

    def pop5(self):
        self.pop = Popup(title='Information', content=Image(source='solmux.png'),
                    size_hint=(None, None), pos=(30,30) ,size=(650, 600))
        self.pop.open()
        

    def dispense(self, g):
        self.servocontrol.servo_rotate(g)
        self.popup.dismiss()
        self.changeScreen('back to main screen')
        
    def conpop1(self):
        content = BoxLayout(orientation="horizontal")
        self.popup = Popup(title="Confirm Biogesic", size_hint=(None, None),
                           size=(500, 200), auto_dismiss=False, content=content)
        servo1 = lambda x:self.transaction('Biogesic')
        yes_btn = Button(text="Yes", on_release = servo1)
        no_btn = Button(text="No", on_press=self.popup.dismiss)
        content.add_widget(yes_btn)
        content.add_widget(no_btn)
        self.popup.open()

    def conpop2(self):
        content = BoxLayout(orientation="horizontal")
        self.popup = Popup(title="Confirm Buscopan", size_hint=(None, None),
                           size=(500, 200), auto_dismiss=False, content=content)
        servo2 = lambda x:self.transaction('Buscopan')
        yes_btn = Button(text="Yes", on_release = servo2)
        no_btn = Button(text="No", on_press=self.popup.dismiss)
        content.add_widget(yes_btn)
        content.add_widget(no_btn)
        self.popup.open()

    def conpop3(self):
        content = BoxLayout(orientation="horizontal")
        self.popup = Popup(title="Confirm Decolgen No-Drowse", size_hint=(None, None),
                           size=(500, 200), auto_dismiss=False, content=content)
        servo3 = lambda x:self.transaction('DecolgenND')
        yes_btn = Button(text="Yes", on_release = servo3)
        no_btn = Button(text="No", on_press=self.popup.dismiss)
        content.add_widget(yes_btn)
        content.add_widget(no_btn)
        self.popup.open()

    def conpop4(self):
        content = BoxLayout(orientation="horizontal")
        self.popup = Popup(title="Confirm Dolfenal", size_hint=(None, None),
                           size=(500, 200), auto_dismiss=False, content=content)
        servo4 = lambda x:self.transaction('Dolfenal')
        yes_btn = Button(text="Yes", on_release = servo4)
        no_btn = Button(text="No", on_press=self.popup.dismiss)
        content.add_widget(yes_btn)
        content.add_widget(no_btn)
        self.popup.open()

    def conpop5(self):
        content = BoxLayout(orientation="horizontal")
        self.popup = Popup(title="Confirm Solmux", size_hint=(None, None),
                           size=(500, 200), auto_dismiss=False, content=content)
        servo5 = lambda x:self.transaction('Solmux')
        yes_btn = Button(text="Yes", on_release = servo5)
        no_btn = Button(text="No", on_press=self.popup.dismiss)
        content.add_widget(yes_btn)
        content.add_widget(no_btn)
        self.popup.open()

    def sound1(self):
        fname = 'Biogesic' + ".mp3"
        sound = SoundLoader.load(fname)
        sound.play()

    def sound2(self):
        fname = 'Buscopan' + ".mp3"
        sound = SoundLoader.load(fname)
        sound.play()

    def sound3(self):
        fname = 'Decolgen No-Drowse' + ".mp3"
        sound = SoundLoader.load(fname)
        sound.play()

    def sound4(self):
        fname = 'Dolfenal' + ".mp3"
        sound = SoundLoader.load(fname)
        sound.play()

    def sound5(self):
        fname = 'Solmux' + ".mp3"
        sound = SoundLoader.load(fname)
        sound.play()
        
        

#app object
class MedicineApp(App):

    def __init__(self, **kwargs):
        super(MedicineApp, self).__init__(**kwargs)
        x=datetime.today()
        y=x.replace(day=x.day, hour=0, minute=6, second=0, microsecond=0)
        delta_t=y-x
        secs=delta_t.seconds+1
        t = Timer(secs, mail)
        t.start()

    def build(self):
        self.title = 'Smart Medicine Dispenser'
        return MainScreen()
    
    def mail():
        gmail_user = 'smartdispenser0@gmail.com'
        gmail_pwd = 'abcd@12345_678'
        gmail_send = 'smartdispenser0@gmail.com'

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_pwd)

        message = 'Please be advised to check the status of the database. It can be accesed through local host'
        server.sendmail(gmail_user, gmail_send, message)
        server.quit()
            
if __name__== '__main__':
    MedicineApp().run()

#result = wrapper.select("Users", UserId = inp)