"""
 Filler for testing
"""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///RedditDB.db'
db = SQLAlchemy(app)


class Subreddits(db.Model):
    """
        Table Subreddits from RedditDB.db
    """
    subreddit_id = db.Column(db.INTEGER, primary_key=True)  # Primary Key (Unique ID for db)
    subreddit_name = db.Column(db.TEXT, nullable=False)  # Text entered by user
    hate_level = db.Column(db.FLOAT, nullable=False)
    last_edited = db.Column(db.DATE)
    being_edited = db.Column(db.BOOLEAN)

    def __repr__(self):
        return '<%r>' % self.subreddit_id


class Posts(db.Model):
    subreddit_id = db.Column(db.INTEGER)
    post_id = db.Column(db.TEXT, primary_key=True)
    post_title = db.Column(db.TEXT)
    hate_level = db.Column(db.FLOAT)

    def __repr__(self):
        return '<%r>' % self.subreddit_id


class Comments(db.Model):
    subreddit_id = db.Column(db.INTEGER)
    post_id = db.Column(db.TEXT)
    comment_id = db.Column(db.TEXT, primary_key=True)
    date_added = db.Column(db.DATE)
    comment_text = db.Column(db.TEXT)
    comment_hate = db.Column(db.FLOAT)

    def __repr__(self):
        return '<%r>' % self.subreddit_id


subreddits = Subreddits.query.order_by(Subreddits.subreddit_id).all()


@app.route('/', methods=['GET'])
@app.route('/index')  # multiple routes to same page
def home():
    return render_template('index.html', subreddits=subreddits)


@app.route('/post/<subreddit_name>/<subreddit_id>', methods=['GET'])
def subreddit_posts(subreddit_id, subreddit_name):
    return render_template('subreddit_posts.html',
                           posts=Posts.query.order_by(Posts.post_title).filter(Posts.subreddit_id == subreddit_id,
                                                                               Posts.hate_level is not None),
                           subreddit_name=subreddit_name)


@app.route('/comment/<post_id>/<post_title>', methods=['GET'])
def subreddit_comments(post_id, post_title):
    return render_template('subreddit_comments.html',
                           comments=Comments.query.order_by(Comments.comment_id).filter(Comments.post_id == post_id),
                           post_title=post_title)


if __name__ == '__main__':
    app.run()
