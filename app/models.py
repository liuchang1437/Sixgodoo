# -*- coding: utf-8 -*-
from . import db
from datetime import datetime
from markdown2 import markdown
import bleach
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import login_manager

class Item(db.Model):
	__tablename__ = 'items'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String, index = True)
	tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
	timestamp = db.Column(db.DateTime,index=True,default=datetime.now)
	flags = db.Column(db.SmallInteger)								   # 16 bits integer, now 0 means not abandoned 2016.03.04 12:59:26
	text = db.Column(db.Text)


	def __repr__(self):
		return '<Item %d>' % self.id								   # return a readable string to represent the model, for debuging.

class Blog(db.Model):
	__tablename__ = 'blogs'
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String)
	timestamp = db.Column(db.Time)
	tag = db.Column(db.String, index = True)
	timestamp = db.Column(db.DateTime,index=True,default=datetime.now)
	text = db.Column(db.Text)
	abstract = db.Column(db.String)
	category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
	text_html = db.Column(db.Text)

	'''@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		target.text_html = markdown(target.text)
	'''
	def __repr__(self):
		return '<Blog %d>' % self.id


class Tag(db.Model):
	__tablename__ = 'tags'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String, unique = True)
	items = db.relationship('Item', backref = 'tag')

	def __repr__(self):
		return '<Tag %r>' % self.name

class Category(db.Model):
	__tablename__ = 'categorys'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String, unique = True)
	blogs = db.relationship('Blog', backref = 'category')

	def __repr__(self):
		return '<Category %r>' % self.name

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64))
	email = db.Column(db.String(64), unique = True)
	password_hash = db.Column(db.String(128))

	@property
	def password(self):
		return AttributeError('password is not a readble attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	def verify_password(self,password):
		return check_password_hash(self.password_hash, password)
	def __repr__(self):
		return '<User %r>' % self.name
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
