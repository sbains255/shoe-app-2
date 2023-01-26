from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen


class SignCustomerPage(Screen):
    def sign_in(self, customer_id, password):
        customers = App.get_running_app().db.load_customers()
        if customers:
            for customer in customers:
                if customer[0] == customer_id and customer[1] == password:
                    app = App.get_running_app()
                    # store the current user id as app variable
                    app.current_user_id = customer_id
                    app.root.current = 'dashboard'
                    return
        error_pop_up = Popup(title='Error',
                             content=Label(
                                 text='Please type correct user name and password \nor try sign up if you do not '
                                      'have an account'),
                             size_hint=(None, None), size=(400, 200), )
        error_pop_up.open()
