# -*- coding: utf-8 -*-
from . import db
from datetime import datetime
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

