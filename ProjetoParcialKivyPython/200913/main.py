
# Rotina principal para a aplicação do PI_7sem. Renato de Lima Vitorasso.

# Para esta aplicação rodar são necessários os arquivos "main.py", "database.py", "my.kv" e "users.txt".


#  A bibliteca base deste código é a Kivy. 

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
from conecta_IBM_db import conecta
from Envia_email_anexo import enviaEmail
import datetime

# As classes "CreateAccountWindow", "LoginWindow" e "MainWindow" trazem as funcionalidades de cada tela da
# aplicação. O arquivo .kv é responsável pelo layout de cada item de cada tela.

class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)  # Estas chamadas são os item presentes no arquivo kv. No começo
    # de cada seção tem os nome e ids. Por exemplo, em um TextInput no arquivo kv, há um id: namee.
    
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    #O self deve ser usado para que as varáveis sejam do escopo de toda a classe.
    def submit(self):
        # Esta primeira parte verifica se tem @, e ponto.
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "login" # o sm.current é o responsável por selecionar qual activity/tela será exibida
            else:
                invalidForm() # Chama o método caso os dados de login não estejam corretos
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""

# Classe da tela de login
        
class LoginWindow(Screen):
    email = ObjectProperty(None) # Os dados aquisitados no login são email e password
    password = ObjectProperty(None)

    # Muito importante. No arquivo kv há um "root.loginBtn()" no " on_release:". Isto é, ao soltar o botão
    # criado, a função abaixo será executada.
    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text # Para pegar o email, por exemplo, usa-se o self e 
            #transforma-se em texto.
            self.reset()
            sm.current = "main" # Caso os dados seja validados, entra a página main.
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""

# Classe da activity principal.
class MainWindow(Screen):
    compra = ObjectProperty(None)
    gasto = ObjectProperty(None)
    
    current = ""

    def logOut(self):
        sm.current = "login"
        
    def imprime_dados(self):
        
        #self.total.text = "Saldo: " + str(float(self.ganho.text) - float(self.gasto.text) )
        compra_item=conecta(str(datetime.datetime.now()), 'User' ,  self.compra.text  , self.gasto.text)
        
        enviaEmail(compra_item.selecao)
        
        
    def on_enter(self, *args):
        
        self.total.text = " "


class WindowManager(ScreenManager):
    pass


def invalidLogin():
    #Popup  
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv") # Chama e constroi com o arquivo .kv

sm = WindowManager()
db = DataBase("users.txt") # Passa o arquivo de texto para o tratamento pela "geatabase.py"

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login" # Aqui indica qual é a tela inicial


class MyMainApp(App):
    def build(self):
        return sm # Roda o que o WindowManager() chamou


if __name__ == "__main__":
    MyMainApp().run() #Executa o código.
