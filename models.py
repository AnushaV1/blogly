from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://cdn1.iconfinder.com/data/icons/user-pictures/100/unknown-512.png"

def connect_db(app):
    db.app = app
    db.init_app(app)

# models go below !
class User(db.Model):
    """ User table """
    __tablename__ = "users"

    # def __repr__(self):
    #     u = self
    #     return f"<User id = {u.id} first_name= {u.first_name} last_name={u.last_name} image_url={u.image_url}>"
    

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(20),
                     nullable=False)

    last_name = db.Column(db.String(20),
                     nullable=False)

    image_url = db.Column(db.Text, nullable=False, default = DEFAULT_IMAGE_URL)
    
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    @classmethod
    def get_all_users(cls):
        return cls.query.all()

    @classmethod
    def user_exist(cls, first_name, last_name):
        return cls.query.filter_by(first_name =first_name, last_name= last_name).first()

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """ posts """
    __tablename__ = "posts"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text,
                     nullable=False)

    content = db.Column(db.Text,
                     nullable=False)
                     
    created_at = db.Column(db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    

    @classmethod
    def post_exist(cls, post_id):
        return cls.query.filter_by(id = post_id).first()

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%m/%d/%Y, %H:%M:%S")

    
class Tag(db.Model):
    """ Tag to posts """
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, nullable = False)
    posts = db.relationship('Post', secondary='posts_tags', backref = "tags")

class PostTag(db.Model):
    """ tag post """
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key= True)