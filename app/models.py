# -*- coding: utf-8 -*-
from . import db
from datetime import datetime,timedelta
from markdown2 import markdown
import bleach
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import login_manager
from math import ceil

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
class Plan(db.Model):
 	__tablename__ = 'plans'
 	id = db.Column(db.Integer, primary_key = True)
 	progress = db.Column(db.LargeBinary,default=0)
 	name = db.Column(db.String, unique = True, index=True)
 	is_finished = db.Column(db.Boolean)
 	description = db.Column(db.Text)
 	count = db.Column(db.Integer)
	timestamp = db.Column(db.DateTime,index=True,default=datetime.now)

 	def is_n(self,n):
 		return (not (self.progress & (1<<(n-1)) == 0))
 	def set_n(self,n):
 		self.progress |= 1<<(n-1)
 	def __repr__(self):
 		return '<Plan %r>' % self.name
class Plan2(db.Model):
	__tablename__ = 'plans2'
	id = db.Column(db.Integer, primary_key = True)
	progress = db.Column(db.String(100),default='^')
	name = db.Column(db.String, unique = True, index=True)
	is_finished = db.Column(db.Boolean)
	description = db.Column(db.Text)
	count = db.Column(db.Integer)
	now = db.Column(db.Integer,default=0)
	timestamp = db.Column(db.DateTime,index=True,default=datetime.now)

	def is_n(self,n):
		if n==1 and len(self.progress)==1:
			return False
		return self.progress[n]=='1'
	def set_n(self,n):
		self.now=n
		if n==len(self.progress):
			self.progress+='1'
		else:
			for i in range(0,(n-len(self.progress))):
				self.progress+='0'
			self.progress+='1'
	def __repr__(self):
		return '<Plan2 %r>' % self.name

	def cal_days(self,ed):
		oneday=timedelta(days=1)
		bd = datetime(self.timestamp.year,self.timestamp.month,self.timestamp.day)
		ed = datetime(ed.year,ed.month,ed.day)
		count=0
		while bd!=ed:
			ed=ed-oneday
			count=count+1
		return count

	def col_count(self):
		return ceil((float)(self.count)/7)
