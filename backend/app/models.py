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
    
    @staticmethod
    def get_all_files(user_id):
        return [{"id": file.id, "name": file.name} for file in File.query.with_entities(File.id, File.name).filter_by(user_id=user_id).all()]

    @staticmethod
    def get_file_id(file_id, user_id):
        file = File.query.with_entities(File.id).filter_by(id=file_id, user_id=user_id).first()
        return file[0] if file else None
    
    @staticmethod
    def get_file_by_id(user_id, file_id):
        return File.query.filter_by(user_id=user_id, id=file_id).first()
    
class File(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    encrypted_content = db.Column(db.LargeBinary, nullable=False)
    nonce = db.Column(db.LargeBinary, nullable=False)
    auth_tag = db.Column(db.LargeBinary, nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="files")

    def __init__(self, name, encrypted_content, nonce, auth_tag, user_id):
        self.name = name
        self.encrypted_content = encrypted_content
        self.nonce = nonce
        self.auth_tag = auth_tag
        self.user_id = user_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
        }