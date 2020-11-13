import smtplib, ssl
from configparser import ConfigParser

class MailSender():
    def __init__(self, config_file_name):
        self.context = ssl.create_default_context()
        self.set_credentials(config_file_name)
    
    def set_credentials(self, config_file_name):
        config_object = ConfigParser()
        config_object.read("config.ini")
        userinfo = config_object["USERINFO"]
        self.password = userinfo["password"]
        self.mail = userinfo["mail"]
        self.port = int(config_object["SERVERCONFIG"]["port"])
    
    def send_mail(self, m):
        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=self.context) as server:
            server.login(self.mail, self.password)
            server.sendmail(self.mail, m, "message")

if __name__ == '__main__':
    ms = MailSender("config.ini")
    mail = "japaapa25@gmail.com"
    ms.send_mail(mail)
