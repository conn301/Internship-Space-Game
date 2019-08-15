import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.properties import NumericProperty, BooleanProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics.context_instructions import PopMatrix, PushMatrix
from kivy.graphics import Rotate
from kivy.uix.behaviors import ButtonBehavior
import math
import time
# import mysql.connecter

kivy.require('1.11.0')


# ===================== CONFIG =======================#

Window.fullscreen = True
score = 0

# ===================== SCREENS ======================#


class Database():
    isAuthenticated = BooleanProperty(False)
    isError = BooleanProperty(False)
    isWrong = BooleanProperty(False)

    global connection
    # connection = mysql.connector.connect(user='root', password='efsiRu1es',
    #                                      host='127.0.0.1',
    #                                      database='world')

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

        connection.close()
        print("You connected to the database successfully.")

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


class YouLose(Screen):

    is_replay = BooleanProperty(False)
    is_score = BooleanProperty(False)

    def replay(self):
        is_replay = True
        is_replay = False
        # SpaceArena.replay(self)

    def quit(self):
        exit(1)


class YouWin(Screen):
    global score
    is_score = BooleanProperty(False)
    test = NumericProperty(0)
    test = score
    print("test:")
    print(score)

    def seescore(self):
        is_score = True
        self.is_score = True

    def quit(self):
        exit(1)


# ===================== DATABASE ======================#


class SpaceArena(Screen):
    global score
    global replay
    ship = ObjectProperty(None)
    bonus_1 = ObjectProperty(None)

    is_lose = BooleanProperty(False)
    is_win = BooleanProperty(False)
    myscore = NumericProperty(0)

    def setup(self):
        self.ship.fuel = 15
        self.ship.velocity = 0, 0
        self.ship.position = 0, 0

    def loss(self):
        pass
        # is_lose = True

    def win(self):
        pass
        # is_lose = False


    def update(self, dt):
        self.ship.move()
        # Bonus.gather(self.bonus_1)

        if self.ship.collide_widget(self.bonus_1):
            self.ship.fuel = 15
        # if self.ship.collide_widget(self.wall or self.wall2 or self.wall3) or :
        if self.ship.collide_widget(self.wall) or self.ship.collide_widget(self.wall2) or self.ship.collide_widget(self.wall3):
            self.ship.fuel = 0
            self.ship.velocity = 0, 0
            # event = Clock.schedule_once(self.loss(), 0)
            # Clock.unschedule(self.loss())
            self.is_lose = True
            self.is_lose = False
            # ScreenManager.current = "YouLose"
            # ScreenManager().next()

        if self.ship.collide_widget(self.portal):
            self.ship.velocity = 0, 0
            score = self.ship.fuel
            myscore = self.ship.fuel
            print("This is the score:")
            print(score)
            print(myscore)
            # YouWin.
            self.is_win = True



    def on_touch_up(self, touch):
        # if (touch.x)
        if self.ship.fuel > 0:
            old_x, old_y = self.ship.velocity
            new_x, new_y = (touch.x-self.ship.x)/100, (touch.y-self.ship.y)/100
            self.ship.velocity = Vector(old_x + new_x, old_y + new_y)
            x, y = self.ship.velocity
            theta = math.degrees(math.atan(x / y))
            self.ship.angle = float(theta)
            # self.ship.canvas.ask_()

            print()
            print(self.ship.angle)
            print(theta)
            print(self.ship.angle)

            self.ship.fuel -= ((touch.x-self.ship.x)**2 + (touch.y-self.ship.y)**2)**(1/2) / 400

        if self.ship.fuel < 0:
            self.ship.fuel = 0


    def quit(self):
        exit(1)

    def games(self):
        self.remove_widget(self.play)
        print("test2")

        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.setup()
        return self

    def replay(self):
        is_lose = False
        print("replay")
        self.setup()
        Clock.schedule_interval(self.update, 1.0 / 60.0)




# ===================== APP ======================#

class ApolloApp(App):
    replay = True

# ====================== WIDGETS ========================#


class Ship(ButtonBehavior, Widget):
    fuel = NumericProperty(0)
    vel_x = NumericProperty(0)
    vel_y = NumericProperty(0)
    velocity = ReferenceListProperty(vel_x, vel_y)


    # def __init__(self, angle=180, **kwargs):
    #     super(Ship, self).__init__(**kwargs)
    #
    #     self.rotate = Rotate(angle=angle)
    #
    #     self.canvas.before.add(PushMatrix())
    #     self.canvas.before.add(self.rotate)
    #     self.canvas.after.add(PopMatrix())

        # self.bind(pos=self.update_canvas)
        # self.bind(size=self.update_canvas)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        # print("moving")
        # print(self.velocity)


class Bonus(Widget):
    pass


class Wall(Widget):
    pass


class Objective(Widget):
    pass

# ====================== BUILD =======================#


class ScreenManagement(ScreenManager):
    sm = ScreenManager()


presentation = Builder.load_file("Apollo.kv")


if __name__ == '__main__':
    ApolloApp().run()
