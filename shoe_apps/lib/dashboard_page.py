from collections import Counter

from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen


class SuggestionDialog(Popup):
    def open_suggestion_dialog(self, customer_size):
        if customer_size:
            data = App.get_running_app().db.load_products()
            if data:

                main_box = self.ids.main_box

                for product in data:
                    if float(customer_size) == product[1]:
                        product_box = BoxLayout(size_hint_y=None, height=dp(70), padding=dp(10))
                        product_box.add_widget(Image(source=f"db/images/{product[0]}.{product[2]}"))
                        # call add_to_cart method when we press this button
                        product_box.add_widget(Label(text=product[3]))
                        product_box.add_widget(Label(text=str(product[1])))
                        main_box.add_widget(product_box)
                if len(main_box.children) == 0:
                    not_found_pop_up = Popup(title='Error',
                                             content=Label(
                                                 text='Your size is missing right now try again later',
                                                 halign='center',
                                                 valign='center'),
                                             size_hint=(None, None), size=(500, 200))
                    not_found_pop_up.open()
                    return
                else:
                    self.open()
                    return

        error = Popup(title='Error',
                      content=Label(
                          text='Error Please type your size!',
                          halign='center',
                          valign='center'),
                      size_hint=(None, None), size=(500, 200))
        error.open()


class CartButton(Button):
    product_id = StringProperty()


class DashBoardPage(Screen):
    def on_pre_enter(self, *args):
        self.load_products()
        self.load_customer_cart()

    def load_products(self):
        self.ids.products_page.clear_widgets()
        self.ids.products_page.add_widget(Label(text='No products available'))
        data = App.get_running_app().db.load_products()
        if data:
            self.ids.products_page.clear_widgets()
            for product in data:
                product_box = BoxLayout(size_hint_y=None, height=dp(70), padding=dp(10))
                product_box.add_widget(Image(source=f"db/images/{product[0]}.{product[2]}"))
                add_to_cart_button = CartButton(text='Add to my cart', )
                add_to_cart_button.product_id = product[0]
                # call add_to_cart method when we press this button
                add_to_cart_button.bind(on_press=lambda x: self.add_to_cart(x.product_id))
                product_box.add_widget(Label(text=product[3]))
                product_box.add_widget(Label(text=str(product[1])))
                product_box.add_widget(add_to_cart_button)
                self.ids.products_page.add_widget(product_box)

    def suggest_shoes(self, customer_size):
        sp = SuggestionDialog()
        sp.open_suggestion_dialog(customer_size)

    def load_customer_cart(self):
        self.ids.customer_cart.clear_widgets()
        self.ids.customer_cart.add_widget(Label(text='Cart is empty'))
        data = App.get_running_app().db.get_customer_cart_products(App.get_running_app().current_user_id)
        if data:
            cart_product_list = []
            self.ids.customer_cart.clear_widgets()
            for product in data:
                cart_product_list.append(product[1])
            # convert the cart products list to dictionary of the number of each product
            product_dic = Counter(cart_product_list)
            for i, (k, v) in enumerate(product_dic.items()):
                products = App.get_running_app().db.load_products()
                for product in products:
                    if product[0] == k:
                        product_box = BoxLayout(size_hint_y=None, height=dp(70), padding=dp(10))
                        product_box.add_widget(Image(source=f"db/images/{product[0]}.{product[2]}"))
                        remove_from_cart_button = CartButton(text='Remove from my cart')
                        remove_from_cart_button.product_id = data[i - 1][0]
                        # call remove_from_cart method when we press this button
                        remove_from_cart_button.bind(on_press=lambda x: self.remove_from_cart(x.product_id))
                        product_box.add_widget(Label(text=product[3]))
                        product_box.add_widget(Label(text=str(product[1])))
                        product_box.add_widget(Label(text=str(v)))
                        product_box.add_widget(remove_from_cart_button)
                        self.ids.customer_cart.add_widget(product_box)

    def add_to_cart(self, product_id):
        App.get_running_app().db.add_product_to_customer_cart(App.get_running_app().current_user_id, product_id)
        self.load_customer_cart()
        notification = Popup(title='Success',
                             content=Label(
                                 text='The product has been added to your cart',
                                 halign='center',
                                 valign='center'),
                             size_hint=(None, None), size=(500, 200))
        notification.open()

    def remove_from_cart(self, order_date):
        App.get_running_app().db.remove_product_from_customer_cart(App.get_running_app().current_user_id, order_date)
        self.load_customer_cart()
        notification = Popup(title='Success',
                             content=Label(
                                 text='The product has been removed to your cart',
                                 halign='center',
                                 valign='center'),
                             size_hint=(None, None), size=(500, 200))
        notification.open()
