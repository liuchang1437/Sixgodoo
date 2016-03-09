# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for, flash,\
	request,current_app
from . import main
from .forms import NewTagForm, NewCatForm, NewItemForm, NewBlogForm,\
	QueryItemForm
from .. import db
from ..models import Blog, Item, Tag, Category 
from random import randint

@main.route('/')
def index():
	fan_paras = Tag.query.filter_by(name=u'摘抄').first().items
	fan_para_length = len(fan_paras)
	fan_para = fan_paras[randint(0,fan_para_length-1)]
	return render_template('index.html',fan_para=fan_para)
	
@main.route('/daily',methods=['GET','POST'])
def daily():
	categories = Category.query.all()
	form = QueryItemForm()
	if form.validate_on_submit():
		items = Item.query.filter_by(name=form.item_name.data).order_by(Item.timestamp.desc()).all()
		return render_template('daily.html',items=items,form=form,categories = Category.query.all())
	page = request.args.get('page',1,type=int)
	pagination = Item.query.order_by(Item.timestamp.desc()).paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
	items = pagination.items
	return render_template('daily.html',items=items,form=form,pagination=pagination,categories = Category.query.all())

@main.route('/new_tag',methods=['GET','POST'])
def new_tag():
	form = NewTagForm()
	if form.validate_on_submit():
		tag = Tag(name=form.name.data)
		db.session.add(tag)
		flash('Add new tag successfully.')
		return redirect(url_for('main.daily'))
	return render_template('new_form.html',title= u'新建标签',form=form)
	
@main.route('/new_item',methods=['GET','POST'])
def new_item():
	form = NewItemForm()
	form.tag_id.choices = [(g.id, g.name) for g in \
		Tag.query.order_by('id')]
	if form.validate_on_submit():
		item = Item(name=form.name.data,text=form.text.data,flags=0,\
			tag_id=form.tag_id.data)
		db.session.add(item)
		flash('Add new item successfully.')
		return redirect(url_for('main.daily'))
	return render_template('new_form.html',title=u'新建备忘',form=form)

@main.route('/blogs/category/<int:cat_id>',methods=['GET','POST'])
def category(cat_id):
	categories = Category.query.all()
	page = request.args.get('page',1,type=int)
	if cat_id == 0:
		pagination = Blog.query.order_by(Blog.timestamp.desc()).paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
		title = 'Sixgodoo'
	else:
		title = Category.query.filter_by(id=cat_id).first().name
		pagination = Blog.query.filter_by(category_id=cat_id).order_by(Blog.timestamp.desc()).paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
	blogs = pagination.items
		
	return render_template('blogs.html',blogs=blogs,pagination=pagination,categories=categories,cat_id=cat_id,title=title)

@main.route('/blogs/article/<int:blog_id>',methods=['GET','POST'])
def article(blog_id):
	categories = Category.query.all()
	blog = Blog.query.filter_by(id=blog_id).first()
	cat_id = blog.category_id
	return render_template('blog.html',blog=blog,categories=categories,cat_id=cat_id)
	
@main.route('/blogs/new_cat',methods=['GET','POST'])
def new_cat():
	form = NewCatForm()
	if form.validate_on_submit():
		category = Category(name=form.name.data)
		db.session.add(category)
		flash('Add new category successfully.')
		return redirect(url_for('main.category',cat_id=0))
	return render_template('new_form.html',title=u'新建目录',form=form)
	
@main.route('/blogs/new_blog',methods=['GET','POST'])
def new_blog():
	form = NewBlogForm()
	form.cat_id.choices = [(g.id, g.name) for g in \
		Category.query.order_by('id')]
	if form.validate_on_submit():
		blog = Blog(title=form.title.data,text=form.text.data,\
			category_id=form.cat_id.data,tag=form.tag.data,\
			abstract=form.abstract.data)
		db.session.add(blog)
		flash('Add new blog successfully.')
		return redirect(url_for('main.category',cat_id=form.cat_id.data))
	return render_template('new_form.html',title=u'新建博客',form=form)

@main.route('/about')
def about():
	categories = Category.query.all()
	return render_template('about.html',categories=categories)
	
	
	


