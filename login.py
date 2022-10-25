# Creating the App
from imports import *
import main
Config.set('kivy', 'exit_on_escape', '0')


class MyWidget(MDScreen):
    """
    Construtor
    """
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.auth_usr = False


class LoginApp(MDApp):
    """
    Class responsible for creating the login screen
    """
    def build(self):
        """
        Method that builds the screen
        """
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('login.kv')
    

    def logger(self):
        if self.root.ids.user.text == 'mikin' and self.root.ids.password.text == '1242':
            self.root.ids.signin_label.text = f'Sup {self.root.ids.user.text}!'
            self.root.ids.signin_label.font_size = 18
            LoginApp().stop()
            self.auth_usr = True
        else:
            self.root.ids.signin_label.text = f'Authentication Failed!'
            self.auth_usr = False
        

LoginApp().run() 