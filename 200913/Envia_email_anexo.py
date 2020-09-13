# Rotina para envio de mensagem via python

# Como o Google, à princípio, não vai te permitir realizar o login via smtplib
# siga o link e habilite: https://www.google.com/settings/security/lesssecureapps
 

# conda install -c conda-forge aiosmtplib
#ou 
#pip install secure-smtplib


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import pandas as pd
import datetime


class enviaEmail:
    
    def __init__(self,dados):
        
        self.dados=dados
    
        # Criando uma instância de um objeto mensagem
        msg = MIMEMultipart()
         
         # A mensagem a ser enviada
        message = "Suas compras"
         
        # Ajustando os parâmetros da mensagem.
        password = "projetointegrador7sem"
        msg['From'] = "PI.7sem@gmail.com"
        msg['To'] = "renatovitorasso@hotmail.com"
        msg['Subject'] = "Assunto"
         
        
        msg.attach(MIMEText(message, 'plain'))
        
        
        
        #Este bloco é responsável pelo envio do documento
        if 1:
            # Nome ou endereço do arquivo a ser enviado
            format_str = "{data} compras.xlsx"
            date=str(datetime.datetime.now())
            filename = format_str.format(data=date[0:10])   
            
            #Criando um data Frame com os dados inseridos no programa para exportar em xlsx
            df = pd.DataFrame(self.dados) 
            df.to_excel(filename)
            
            attachment = open(filename,'rb')
            
            
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            
            msg.attach(part)
            
            attachment.close()
        
        
         
        #Criando o servidor
        server = smtplib.SMTP('smtp.gmail.com: 587')
         
        server.starttls()
         
        # Credenciais de Login
        server.login(msg['From'], password)
         
         
        # Enviando a mensagem via servidor
        server.sendmail(msg['From'], msg['To'], msg.as_string())
         
        server.quit()
         
        print ("successfully sent email to %s " % msg['To'])