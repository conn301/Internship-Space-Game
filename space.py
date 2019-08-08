import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
import mysql.connector
from kivy.properties import BooleanProperty, ObjectProperty
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.properties import NumericProperty, ObjectProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock
import math
kivy.require('1.11.0')



class Database():
    isAuthenticated = BooleanProperty(False)
    isError = BooleanProperty(False)
    isWrong = BooleanProperty(False)


    global connection
    connection = mysql.connector.connect(user='root', password='efsiRu1es',
                                         host='127.0.0.1',
                                         database='world')

    def connect_to_DB(self, username, password):

        c = connection.cursor()

        if username == "" and password == "":
                            exit()

        try:
            c.execute("SELECT * FROM persons WHERE FirstName = \"{}\"".format(username))

            for column in c:
                pass

            if password == column[3]:
                print("Correct Password")
                self.isAuthenticated = True
            else:
                print("Incorrect Password")
                self.isWrong = True

        except UnboundLocalError:
            self.isError = True
            print("ERROR")

        #connection.close()
        # print("You connected to the database successfully.")

    def user_account(self, first, last, username, password):

        c = connection.cursor()
        c.execute("INSERT INTO persons (PersonId, LastName, FirstName, Address) VALUES (%s, %s, %s, %s)", (first, last, username, password))
        connection.commit()
        print(first)
        print(last)
        print(username)
        print(password)


class LogIn(Screen, Database):
    pass


class Register(Screen, Database):
    pass


class GameMenu(Screen, Database):
    pass


class ScreenManagement(ScreenManager):
    pass



presentation = Builder.load_file("space.kv")


class SpaceApp(App):

    def build(self):
        return presentation

if __name__ == '__main__':
    SpaceApp().run()

