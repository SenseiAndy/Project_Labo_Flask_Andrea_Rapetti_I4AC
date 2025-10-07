from models.connection import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_login import UserMixin
from flask_migrate import Migrate



class Umore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stato = db.Column(db.String(80), unique=False, nullable=False)
    # timestamp = db.Column(db.DateTime, server_default=db.func.now())
    # non so se funziona con sqlite perché molti db usano in formato ISO
    # ISO = "YYYY-MM-DD HH:MM:SS"
    # in alternativa posso salvare il timestamp come UNIX timestamp (numero di secondi dal 1970)

    def __repr__(self):
        return f'<Umore id: {self.id} umore:{self.stato}>'
    
    def to_dict(self):
         # ritorna un dizionario con i campi dell'oggetto
         # attenzione al timestamp, se non lo converto in stringa da problemi con jsonify
         #perché json preferisce stringhe in formato ISO
         data = {'id':self.id,
                 'stato': self.stato
                 
                }
         return data



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))  # Campo per la password criptata
    umore_id = db.Column(db.Integer, db.ForeignKey('umore.id'))

    umore = db.relationship('Umore', backref=db.backref('user', lazy=True))


    def set_password(self, password):
            self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
    def __repr__(self):
        return f'<User id: {self.id} username:{self.username}>'
    
    def to_dict(self):
         data = {'id':self.id,
                 'username': self.username,
                 'email': self.email,
                 'umore_id': self.umore_id
                }
         return data
    

class Frase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    frase = db.Column(db.Text, nullable=True)
    umore_id = db.Column(db.Integer, db.ForeignKey('umore.id'), nullable=False)

    umore = db.relationship('Umore', backref=db.backref('frasi', lazy=True))

    def __repr__(self):
        return f'<Frase id: {self.id} frase: {self.frase}>'

    def to_dict(self):
        return {
            'id': self.id,
            'frase': self.frase,
            'umore_id': self.umore_id
        }



