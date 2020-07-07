from unittest import TestCase
from app import app
from models import db, User, Post, Tag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyTestCase(TestCase):
    """ Test cases for all routes """

    def setUp(self):
        """ clear tables and add sample use  """
        Tag.query.delete()
        Post.query.delete()
        user = User(first_name='user_firstname', last_name='user_lastname',  image_url="https://image.flaticon.com/icons/svg/236/236831.svg")
        post = Post(title="TestTitle", content="sample content", user_id=1)
        tag = Tag(name="TagName1")
        db.session.add_all([user, post, tag])
        db.session.commit()

        self.post_id = post.id
        self.user_id = user.id
        self.tag_id = tag.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_users_list(self):
        """ check the homepage route """
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text = True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('user_firstname', html)

    def test_show_user(self):
        """ Test show user details """
        with app.test_client() as client:
            response = client.get(f"/users/{self.user_id}")
            html = response.get_data(as_text = True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<p>user_firstname user_lastname</p>', html)

    def test_add_new_user(self):
        """  test follow redirect for new user post """

        with app.test_client() as client:
            user = {"first_name": "Test_firstname", "last_name": "Test_lastname", "image_url": "https://image.flaticon.com/icons/svg/236/236831.svg"}
            response = client.post("/users/new", data = user, follow_redirects = True)
            html = response.get_data(as_text = True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1 class="title">All Users</h1>',html)

    ################ Post route tests ################

    def test_list_post(self):
        """  Test list all posts """
        with app.test_client() as client:
            response = client.get(f"/posts/{self.post_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<p>sample content</p>',html)


    def test_show_post(self):
        """   Test show single post """
        with app.test_client() as client:
            response = client.get(f"/posts/{self.post_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1 class="title">TestTitle</h1>',html)


    def test_add_new_post(self):
        """  test follow redirect for new post """

        with app.test_client() as client:
            post_data = {"title": "TestTitle", "content": "sample content", "user_id": 1}
            response = client.post("/users/1/posts/new", data=post_data, follow_redirects=True)
            html = response.get_data(as_text = True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h2 class="title">Posts</h2>',html)


    ########## Tests for tags ################

    def test_list_tags(self):
        """  Test list all posts """
        with app.test_client() as client:
            response = client.get(f"/tags/{self.tag_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('TagName1',html)
    
    def test_show_tag(self):
        """   Test show single post """
        with app.test_client() as client:
            response = client.get(f"/tags/{self.tag_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>TagName1</h1>',html)

    def test_add_new_tag(self):
        """  test follow redirect for new post """

        with app.test_client() as client:
            post_data =  {"name":"TagName2"}
            response = client.post("/tags/new", data=post_data, follow_redirects=True)
            html = response.get_data(as_text = True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Tags</h1>',html)
