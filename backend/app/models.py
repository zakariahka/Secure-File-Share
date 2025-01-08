from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    files = db.relationship("File", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "files": [file.to_dict() for file in self.files],
        }
    
class File(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    encrypted_file = db.Column(db.LargeBinary, nullable=False)
    nonce = db.Column(db.LargeBinary, nullable=False)
    hmac_tag = db.Column(db.LargeBinary, nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="files")

    def __init__(self, name, encrypted_file, nonce, hmac_tag, user_id):
        self.name = name
        self.encrypted_file = encrypted_file
        self.nonce = nonce
        self.hmac_tag = hmac_tag
        self.user_id = user_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
        }