from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False, unique=False)
    password = db.Column(db.String(50), nullable=False, unique=False)

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name
        }