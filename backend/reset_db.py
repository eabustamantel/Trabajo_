from models import db
from config import Config
from flask import Flask
from sqlalchemy import text

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    # Drop all tables with CASCADE
    with db.engine.connect() as conn:
        conn.execute(text('DROP TABLE IF EXISTS usuarios CASCADE'))
        conn.commit()
    db.drop_all()
    print('All tables dropped')

    # Create all tables
    db.create_all()
    print('All tables created successfully')
