from flask import render_template

from blog import app
from database import session
from model import Post

import mistune
from flask import request, redirect, url_for

from flask import flash
from flask.ext.login import login_user
from werkzeug.security import check_password_hash
from model import User
from flask.ext.login import login_required

#setup logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
log.addHandler(console_handler)


@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Post).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts[start:end]

    return render_template("posts.html",
        posts=posts,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )

@app.route("/post/add", methods=["GET"])
@login_required
def add_post_get():
    return render_template("add_post.html")


@app.route("/post/add", methods=["POST"])
@login_required
def add_post_post():
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
    )
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))


#Allows you to view a single post
@app.route("/post/<int:post_id>")
def view_post(post_id):
    post = session.query(Post)
    post = post.get(post_id + 1)
    #log.info( "post = {}".format(post) )
    return render_template("post.html",
        post=post
        )

@app.route("/post/<int:post_id>/edit", methods = ["GET"])
def edit_post(post_id):
    post = session.query(Post).get(post_id + 1)
    post_title = post.title
    post_content = post.content
    return render_template("edit_post.html",
        post_title = post_title,
        post_content = post_content
        )

@app.route("/post/<int:post_id>/edit", methods = ["POST"])
def save_edit_post(post_id):
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
    )
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))

#can't figure this out
# @app.route("/post/<int:post_id>/delete", methods = ["POST"])
# def delete_post(post_id):
#     post = session.query(Post).get(post_id + 1)
#     post_title = post.title
#     return render_template("delete_post.html",
#         post=post,
#         post_title = post_title
#         )

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("posts"))







