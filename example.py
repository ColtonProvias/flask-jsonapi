from flask import Flask
from flask.ext.jsonapi import FlaskJSONAPI, SQLAlchemyEndpoint
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Unicode, UnicodeText, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy_jsonapi import JSONAPIMixin, as_relationship


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.sqlite'
app.config['SQLALCHEMY_ECHO'] = False
app.debug = True
api = FlaskJSONAPI(app)
db = SQLAlchemy(app)


class APIMixin(JSONAPIMixin):
    jsonapi_column_data_overrides = {
        'id': lambda self: str(self.id)
    }


class User(APIMixin, db.Model):
    __tablename__ = 'users'
    jsonapi_exclude_columns = ['password']
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(30))
    password = Column(Unicode(30))


class Post(APIMixin, db.Model):
    __tablename__ = 'posts'
    jsonapi_extra_relationships = ['my_relationship']
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(100))
    content = Column(UnicodeText)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', lazy='select',
                        backref=backref('posts', lazy='dynamic'))

    @as_relationship()
    def my_relationship(self):
        return User.query.first()


class Comment(APIMixin, db.Model):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(UnicodeText)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))

    user = relationship('User', lazy='joined',
                        backref=backref('comments', lazy='dynamic'))
    post = relationship('Post', lazy='joined',
                        backref=backref('comments', lazy='dynamic'))


api.add_endpoint(SQLAlchemyEndpoint(Post, db.session))
api.add_endpoint(SQLAlchemyEndpoint(User, db.session))
api.add_endpoint(SQLAlchemyEndpoint(Comment, db.session))


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    user = User(username='sampleuser', password='Secret')
    post = Post(title='Sample Post',
                content='Lorem ipsum dolor sit amet fakus latinus',
                user=user)
    comment = Comment(content='Sample comment',
                      user=user, post=post)
    db.session.add(user)
    db.session.commit()
    app.run()
