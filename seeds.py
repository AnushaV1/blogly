from models import db, connect_db, User, Post, Tag, PostTag
from app import app

db.drop_all()
db.create_all()

# empty table 
User.query.delete()
Post.query.delete()

# Add sample data
d1 = User(first_name = "Sooraj", last_name = "Venkataraghavan", image_url="https://www.flaticon.com/free-icon/man_236831")

d2 = User(first_name ="Sahanna", last_name="Venkataraghavan" , image_url="https://www.flaticon.com/free-icon/girl_186037")

db.session.add(d1)
db.session.add(d2)
db.session.commit()

p1 = Post(title="ABCD", content="ddfsdfsdfsdfsd", created_at="2020-07-02 20:50:54.215402", user_id = 1)
p2 = Post(title="MSQQWABCD", content="Qwdadsafsdfsdfsd", created_at="2020-07-02 20:50:54.215402", user_id = 2)
p3 = Post(title="Best college list", content="Calpoly and Univ of penn", created_at="2020-07-02 20:50:54.215402", user_id = 1)
p4 = Post(title="C Practice", content= "sdasdas", created_at="2020-07-02 20:35:11.304844", user_id =2)
p5 = Post(title="Neural Network", content= "Good books", created_at= "2020-07-02 20:49:02.805551", user_id=2)
p6 = Post(title="Neural Network", content= "Great content", created_at= "2020-07-03 20:49:02.805551", user_id=1)
db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)
db.session.add(p5)
db.session.add(p6)

db.session.commit()

t1 = Tag(id=1, name="computer")
t2 = Tag(id=2, name="general")
t3 = Tag(id=3, name="college")
t4 = Tag(id=4, name="books")

db.session.add(t1)
db.session.add(t2)
db.session.add(t3)
db.session.add(t4)

db.session.commit()