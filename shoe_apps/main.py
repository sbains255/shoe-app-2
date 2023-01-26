from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder

from db.database import SQLiteDataBase

Config.set('kivy', 'window_icon', 'assets/logo.ico')


class ShoesStoreApp(App):
    db = SQLiteDataBase()
    current_user_id = ''

    def build(self):
        self.icon = "assets/logo.ico"
        # load main page
        Builder.load_file('kv/main_page.kv')
        # load admin sign in  page
        Builder.load_file('kv/admin_sign_in_page.kv')
        # load customer sign in  page
        Builder.load_file('kv/customer_sign_in_page.kv')
        # load customer sign up  page
        Builder.load_file('kv/customer_sign_up_page.kv')
        # load dashboard page
        Builder.load_file('kv/dashboard_page.kv')

        # load admin page
        Builder.load_file('kv/admin_page.kv')
        # load root widget
        root = Builder.load_file('main.kv')

        return root

    def on_stop(self):
        self.db.db.close()


if __name__ == "__main__":
    ShoesStoreApp().run()
