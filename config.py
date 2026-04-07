import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_NAME = os.environ.get('DB_NAME')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RECEBEDOR_DEFAULT = os.environ.get('RECEBEDOR_DEFAULT', 'Alexandre Fortes Torres')
    CPF_RECEBEDOR_DEFAULT = os.environ.get('CPF_RECEBEDOR_DEFAULT', '802.943.674-20')
    TELEFONE_RECEBEDOR_DEFAULT = os.environ.get('TELEFONE_RECEBEDOR_DEFAULT', '(82) 99184-7469')