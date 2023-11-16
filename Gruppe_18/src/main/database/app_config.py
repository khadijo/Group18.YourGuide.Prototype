import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
'''Due to potential circular import issues, the configuration code for the Flask app, 
and the database was split into two files: app_config.py and create_data_db.py.'''

app = Flask(__name__, template_folder='../templates')

module_path = os.path.dirname(os.path.abspath(__file__))
database_name = os.path.join(module_path, "../YourGuide.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_name}'
db = SQLAlchemy(app)



