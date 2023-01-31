from flask import request, url_for
from sql_alchemy import banco
from requests import post

MAILGUN_DOMAIN =  'sandbox7e38f697444f4cb7a2cd65c1b4608d1f.mailgun.org'
MAILGUN_API_KEY = '9a51746845fe559bde1e9822a0c4f97a-75cd784d-5bf880c9'
FROM_TITLE = 'NO-REPLY'
FROM_EMAIL = 'no-replay@apiresthoteis.com'

class UserModel(banco.Model):

    __tablename__ = 'users'

    user_id = banco.Column(banco.Integer , primary_key = True)
    login = banco.Column(banco.String(40), nullable = False, unique = True)
    senha = banco.Column(banco.String(10), nullable = False)
    email = banco.Column(banco.String(80), nullable = False, unique = True)
    ativado = banco.Column(banco.Boolean, default = False)

    def __init__(self, login, senha, email, ativado):
        self.login = login
        self.senha = senha
        self.email = email
        self.ativado = ativado
    
    def send_confirmation_email(self):
        #http://127.0.0.1:5000/confirmacao/{user_id}
        link = request.url_root[:-1] + url_for('userconfirm', user_id = self.user_id)

        return post("https://api.mailgun.net/v3/{}/messages".format(MAILGUN_DOMAIN),
		auth=("api", MAILGUN_API_KEY),
		data={"from": '{} <{}>'.format(FROM_TITLE, FROM_EMAIL),
			"to": self.email,
			"subject": "Confirmação de Cadastro",
			"text": "Confirme seu cadastro clicando no link a seguir: {}".format(link),
            "html": "<html><p>\
            Confirme seu cadastro clicando no link a seguir: <a href='{}' > CONFIRMAR EMAIL </a>\
            </p></html>".format(link)
        })
                                     
        
    
    def json(self):
        return{
                'user_id': self.user_id,
                'login' : self.login,
                'email' : self.email,
                'ativado' : self.ativado
            }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id = user_id).first() #SELECT * FROM users WHERE user_id = $user_id
        if user:
            return user
        return None
    
    @classmethod
    def find_by_login(cls, login):
        login = cls.query.filter_by(login = login).first() #SELECT * FROM users WHERE login = $login
        if login:
            return login
        return None
    
    @classmethod
    def find_by_email(cls, email):
        email = cls.query.filter_by(email = email).first() #SELECT * FROM users WHERE login = $login
        if email:
            return email
        return None
    
    def save_user(self):
        banco.session.add(self)
        banco.session.commit()
    
    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
    
    
    