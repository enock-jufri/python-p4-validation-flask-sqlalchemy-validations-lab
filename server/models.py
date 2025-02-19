from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('phone_number','name')
    def validator(self,key,value):
        if key == 'phone_number':
            if not value.isdigit():
                raise ValueError('phone number should be only digits')
            elif len(value) != 10:
                raise ValueError('Please Ener a valid phone number')
            else:
                return value
        elif key == 'name':
            if not value:
                raise ValueError('please enter a name')
            elif value in [author.name for author in Author.query.all()]:
                raise ValueError('name already exists')
            else:
                return value
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String,)
    category = db.Column(db.String)
    summary = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validates_content(self,key,value):
        if len(value) < 250:
            raise ValueError("content too short")
        else:
            return value
        
    @validates('category', 'title', 'summary')
    def validate_fields(self, key, value):
        if key == "category":
            if value not in ['Fiction', 'Non-Fiction']:
                raise ValueError("Invalid category. Choose 'Fiction' or 'Non-Fiction'.")
            return value
        
        if key == "title":
            clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
            if not any(phrase.lower() in value.lower() for phrase in clickbait_phrases):
                raise ValueError("Title must contain one of the following: 'Won't Believe', 'Secret', 'Top', 'Guess'.")
            return value
        
        if key == "summary":
            if not value or len(value) > 250:
                raise ValueError("Summary must be a maximum of 250 characters.")
            return value



    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
