from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
import re


class CustomerSignUpPage(Screen):
    def sign_up(self, customer_id, password):
        #validates the user input to check if there is an @ symbol
        if re.search('[@]', customer_id):
            success = App.get_running_app().db.customer_sign_up(customer_id, password)
            if success:
                App.get_running_app().current_user_id = customer_id
                App.get_running_app().root.current = 'dashboard'
            else:
                id_available_pop_up = Popup(title='Error',
                                            content=Label(text='This id is available try to sign in instead'),
                                            size_hint=(None, None), size=(400, 200), )
                id_available_pop_up.open()
        else:
            id_invalid_pop_up = Popup(title='Error',
                                        content=Label(text='This is an invalid email'),
                                        size_hint=(None, None), size=(400, 200), )
            id_invalid_pop_up.open()

