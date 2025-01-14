from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Define metadata
metadata = MetaData()

# Initialize SQLAlchemy with custom metadata
db = SQLAlchemy(metadata=metadata)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(128), nullable=False)

# Tag Model
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)

# Todo Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    is_complete = db.Column(db.Boolean, default=False)

    # Foreign keys for relationships
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), nullable=False)
