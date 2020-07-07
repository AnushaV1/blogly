from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///user_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

app.config['SECRET_KEY'] = "abc345ERQWST"
#app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
#debug = DebugToolbarExtension(app)

connect_db(app)
#db.create_all()

@app.route('/')
def homepage():
    """Show recent list of posts, most-recent first."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)


@app.route('/users')
def list_users():
    """ show list of users """
    
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("/users/list.html", users = users)


@app.route('/users/new', methods=["GET"])
def show_form():
    """ show new user form """
    return render_template("/users/form.html")

@app.route('/users/new', methods=["POST"])
def add_users():
    """ Add new user to database """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    # check if user already exist
    # user_exist = User.user_exist(first_name,last_name)
    # if user_exist:
    #     flash("User already Exist ")
    #     return redirect('/users/new')
    
    # else:
    new_user = User(first_name=first_name, last_name=last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """ show details of single user """
    user = User.query.get_or_404(user_id)
    return render_template("/users/details.html", user = user)

@app.route('/users/<int:user_id>/edit')
def edit_users(user_id):
    """ Show form to edit user details """ 
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """ update existing user with form submission"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """ Delete existing user """

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


############ POSTS route ####################

@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def new_post_form(user_id):
    """ Show form to create new post specific user with user id """
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('/posts/new_post.html', user=user, tags = tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """ Add post from form to post table """
    user = User.query.get_or_404(user_id)
    title=request.form['title']
    content=request.form['content']
    tag_id = [int(num) for num in request.form.getlist("tags")]
    print(f" Tag id {tag_id}")
    tags = Tag.query.filter(Tag.id.in_(tag_id)).all()
    print(f"tags {tags}")
    new_post = Post(title = title, content = content,                   
                    user_id=user_id, tags = tags)

    db.session.add(new_post)
    db.session.commit()
    flash(f" New post '{new_post.title}' added")
    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('/posts/show.html', post = post)


@app.route('/posts/<int:post_id>/edit')
def edit_posts(post_id):
    """ show form to edit post """
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit_post.html', post= post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """ update post in table """
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    flash(f" Post '{post.title}' edited")
    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """ Delete post from table """
    post = Post.query.get_or_404(post_id)
    
    post_exist = Post.post_exist(post_id)
    if post_exist:
        db.session.delete(post_id)
        db.session.commit()
        flash(f"Post '{post.title}' deleted")
        return redirect(f"/users/{post.user_id}")
    else:
        flash("post does not exist")
        return redirect('/users')


############# Tags routes #############
@app.route('/tags')
def tag_main():
    """ tags main """
    tags = Tag.query.all()
    return render_template('/tags/index.html', tags = tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """ show information on specific tag """
    tag = Tag.query.get_or_404(tag_id)
    return render_template('/tags/show.html', tag= tag)

@app.route('/tags/<int:tag_id>/edit')
def edit_form(tag_id):
    """ Show edit form """
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('/tags/edit.html', tag= tag, posts = posts)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def show_edit_form(tag_id):
    """ Handle form submission for update tag"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f" Tag '{tag.name}' is edited")
    return redirect("/tags")

@app.route('/tags/new')
def new_tags_form():
    """ show new tags form """
    posts = Post.query.all()
    return render_template('/tags/new.html', posts = posts)

@app.route('/tags/new', methods=["POST"])
def new_tags():
    """ Handle form submission for tag form """
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added ")
    return redirect("/tags") 


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """ Handle delete form for deleting a tag """
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f" '{tag.name}' deleted")
    return redirect("/tags")

@app.errorhandler(404)
def page_not_found(error):
    """Show 404 ERROR page if page NOT FOUND"""
    return render_template('error.html')
