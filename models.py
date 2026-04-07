from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    iduser = Column(Integer, primary_key=True, autoincrement=True)
    nameuser = Column(String(50), nullable=False)
    loginuser = Column(String(50), nullable=False, unique=True)
    passworduser = Column(String(32), nullable=True)

    recibos = relationship('Recibo', backref='user', lazy=True)

class Recibo(db.Model):
    __tablename__ = 'recibo'
    idrecibo = Column(Integer, primary_key=True, autoincrement=True)
    valorRecibo = Column(Numeric(10, 2), nullable=True)
    dataRecibo = Column(Date, nullable=True)
    pagadorRecibo = Column(String(200), nullable=True)
    docPagRecibo = Column(String(18), nullable=True)
    campoRefRecibo = Column(String(300), nullable=True)
    recebedorRecibo = Column(String(200), nullable=True)
    docRecebRecibo = Column(String(18), nullable=True)
    foneRecebRecibo = Column(String(20), nullable=True)
    iduser = Column(Integer, ForeignKey('user.iduser'), nullable=True)