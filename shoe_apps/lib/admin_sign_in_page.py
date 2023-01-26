from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen


class AdminSignInPage(Screen):
    def sign_in(self, admin_name, admin_password):
        if admin_name == "admin" and admin_password == "admin":
            # get app running instance
            app = App.get_running_app()
            # move to admin page if the password and username correct
            app.root.current = 'admin'
        else:
            # display pop up that information inputted is incorrect
            popup = Popup(title='Error',
                          content=Label(text='Please type correct user name and password'),
                          size_hint=(None, None), size=(400, 200), )
            popup.open()
