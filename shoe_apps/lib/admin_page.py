import datetime
import os
from collections import Counter

from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from plyer import filechooser


class AddProductDialog(Popup):
    product_name = StringProperty()
    product_size = StringProperty()
    product_image = StringProperty()

    def pick_image(self):
        filechooser.open_file(on_selection=self.handle_selection, filters=["*jpg", "*png", "*jpeg"])

    def handle_selection(self, selection):
        file_path = selection[0]
        self.product_image = file_path

    def add_to_database(self):
        # check if one or more of the required fields are empty
        if not self.product_size or not self.product_name or not self.product_image:
            # if so tell the admin to fill all of therm
            error_dialog = Popup(title='Error',
                                 content=Label(text='Please make sure filling all fields'), halign='center',
                                 valign='center',
                                 size_hint=(None, None), size=(300, 150))
            error_dialog.open()
        # check if image path is exists
        elif not os.path.exists(self.product_image):
            # if so tell the admin to correct the path or use image picker
            error_dialog = Popup(title='Error',
                                 content=Label(
                                     text='Please make sure image path\nis correct or use file\npicker instead',
                                     halign='center',
                                     valign='center'),
                                 size_hint=(None, None), size=(300, 200))
            error_dialog.open()
        # else save the product to database
        else:
            # trying to create images folder
            try:
                os.mkdir('db/images')
            except:
                pass
            product_id = str(datetime.datetime.now().strftime("%d%m%Y%H%M%S"))
            from shutil import copyfile
            # get the image extension
            filename, file_extension = os.path.splitext(self.product_image)
            # move the chosen image to the images folder
            copyfile(self.product_image, f"db/images/{product_id}{file_extension}")

            App.get_running_app().db.add_product(self.product_size, self.product_name, file_extension.replace('.', ''),
                                                 product_id)
            App.get_running_app().root.get_screen('admin').load_products()
            self.dismiss()


class AdminPage(Screen):
    add_product_dialog = AddProductDialog()
    product_data_list = ListProperty([])

    def open_add_product_pop_up(self):
        self.add_product_dialog.open()

    def on_pre_enter(self, *args):
        self.load_products()
        self.load_customers()

    def load_products(self):
        self.ids.products_page.clear_widgets()
        self.ids.products_page.add_widget(Label(text='loading data..'))
        data = App.get_running_app().db.load_products()
        if data:
            self.ids.products_page.clear_widgets()
            for product in data:
                product_box = BoxLayout(size_hint_y=None, height=dp(70), padding=dp(10))
                product_box.add_widget(Image(source=f"db/images/{product[0]}.{product[2]}"))
                product_box.add_widget(Label(text=product[3]))
                product_box.add_widget(Label(text=str(product[1])))
                product_data = {'name': product[3], 'size': product[1], 'image': f"db/images/{product[0]}.{product[2]}"}
                self.ids.products_page.add_widget(product_box)
                self.product_data_list.append(product_data)

    def load_customers(self):
        self.ids.customer_cart.clear_widgets()
        self.ids.customer_cart.add_widget(Label(text='No data to display'))
        customers = App.get_running_app().db.load_customers()
        if customers:
            for customer in customers:
                customer_cart_products = App.get_running_app().db.get_customer_cart_products(customer[0])
                if customer_cart_products:
                    cart_product_list = []
                    self.ids.customer_cart.clear_widgets()
                    for product in customer_cart_products:
                        cart_product_list.append(product[1])
                    # convert the cart products list to dictionary of the number of each product
                    product_dic = Counter(cart_product_list)
                    for i, (k, v) in enumerate(product_dic.items()):
                        products = App.get_running_app().db.load_products()
                        for product in products:
                            if product[0] == k:
                                product_box = BoxLayout(size_hint_y=None, height=dp(70), padding=dp(10))
                                product_box.add_widget(Image(source=f"db/images/{product[0]}.{product[2]}"))
                                # call add_to_cart method when we press this button
                                product_box.add_widget(Label(text=product[3]))
                                product_box.add_widget(Label(text=str(product[1])))
                                product_box.add_widget(Label(text=str(v)))
                                product_box.add_widget(Label(text=str(customer[0])))
                                self.ids.customer_cart.add_widget(product_box)
