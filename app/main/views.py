# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for, flash,\
	request,current_app
from . import main
from .forms import NewTagForm, NewCatForm, NewItemForm, NewBlogForm,\
	QueryItemForm,TestForm
from .. import db
from ..models import Blog, Item, Tag, Category
from random import randint
from markdown2 import markdown
from flask.ext.login import login_required

@main.route('/')
def index():
	fan_paras = Tag.query.filter_by(name=u'摘抄').first().items
	fan_para_length = len(fan_paras)
	fan_para = fan_paras[randint(0,fan_para_length-1)]
	return render_template('index.html',title=u'主页 ',fan_para=fan_para)

@main.route('/daily',methods=['GET','POST'])
def daily():
	form = QueryItemForm()
	page = request.args.get('page',1,type=int)
	if form.validate_on_submit():
		pagination = Item.query.filter_by(name=form.item_name.data).\
			order_by(Item.timestamp.desc()).\
			paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
		items = pagination.items
		return render_template('daily.html',title=u"检索",items=items,form=form,pagination=pagination)
	pagination = Item.query.order_by(Item.timestamp.desc()).paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
	items = pagination.items
	return render_template('daily.html',title=u"日常",items=items,form=form,pagination=pagination)

@main.route('/daily/item/<int:item_id>',methods=['GET','POST'])
def item(item_id):
	form = QueryItemForm()
	if form.validate_on_submit():
		page = request.args.get('page',1,type=int)
		pagination = Item.query.filter_by(name=form.item_name.data).\
			order_by(Item.timestamp.desc()).\
			paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
		items = pagination.items
		return render_template('daily.html',title=u"检索",items=items,form=form,pagination=pagination)
	items = Item.query.filter_by(id=item_id).all()
	return render_template('item.html',title=u"日常",items=items,form=form)

@main.route('/daily/<int:req_id>',methods=['GET','POST'])
def daily_req(req_id):
	form = QueryItemForm()
	page = request.args.get('page',1,type=int)
	if form.validate_on_submit():
		pagination = Item.query.filter_by(name=form.item_name.data).\
			order_by(Item.timestamp.desc()).\
			paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
		items = pagination.items
		return render_template('daily.html',title=u"检索",items=items,form=form,pagination=pagination)
	if req_id==1:
		pagination = Item.query.filter_by(flags=1).order_by(Item.timestamp.desc()).paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
	else:
		pagination = Item.query.filter_by(flags=0).order_by(Item.timestamp.desc()).paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
	items = pagination.items
	return render_template('daily_req.html',title=u"日常",items=items,form=form,pagination=pagination,req_id=req_id)


@main.route('/new_tag',methods=['GET','POST'])
@login_required
def new_tag():
	form = NewTagForm()
	if form.validate_on_submit():
		tag = Tag(name=form.name.data)
		db.session.add(tag)
		db.session.commit()
		return redirect(url_for('main.daily'))
	return render_template('new_tag.html',title= u'新建标签',form=form)

@main.route('/daily/edit/<int:item_id>',methods=['GET','POST'])
@login_required
def edit_item(item_id):
	item = Item.query.filter_by(id=item_id).first()
	form = NewItemForm()
	form.tag_id.choices = [(g.id, g.name) for g in \
		Tag.query.order_by('id')]
	if form.validate_on_submit():
		item.name=form.name.data
		item.text=form.text.data
		item.tag_id=form.tag_id.data
		item.flags=form.flag.data
		db.session.add(item)
		db.session.commit()
		return redirect(url_for('main.item',item_id=item_id))
	form.name.data = item.name
	form.text.data = item.text
	form.tag_id.data = item.tag_id
	form.flag.data = item.flags
	return render_template('new_item.html',title=u'修改备忘',form=form)

@main.route('/daily/tag/<int:tag_id>',methods=['GET','POST'])
def tag(tag_id):
	form = QueryItemForm()
	page = request.args.get('page',1,type=int)
	if form.validate_on_submit():
		pagination = Item.query.filter_by(name=form.item_name.data).\
			order_by(Item.timestamp.desc()).\
			paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
		items = pagination.items
		return render_template('daily.html',title=u"检索",items=items,form=form,pagination=pagination)
	pagination = Item.query.filter_by(tag_id=tag_id).order_by(Item.timestamp.desc()).paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
	items = pagination.items
	return render_template('tag.html',title=u"日常",tag_id=tag_id,items=items,form=form,pagination=pagination)

@main.route('/new_item',methods=['GET','POST'])
@login_required
def new_item():
	form = NewItemForm()
	form.tag_id.choices = [(g.id, g.name) for g in \
		Tag.query.order_by('id')]
	if form.validate_on_submit():
		item = Item(name=form.name.data,text=form.text.data,flags=form.flag.data,\
			tag_id=form.tag_id.data)
		db.session.add(item)
		db.session.commit()
		return redirect(url_for('main.daily'))
	return render_template('new_item.html',title=u'新建备忘',form=form)

@main.route('/blogs/category/<int:cat_id>')
def category(cat_id):
	categories = Category.query.all()
	page = request.args.get('page',1,type=int)
	if cat_id == 0:
		title=u'博客'
		pagination = Blog.query.order_by(Blog.timestamp.desc()).paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
	else:
		title=Category.query.filter_by(id=cat_id).first().name
		pagination = Blog.query.filter_by(category_id=cat_id).order_by(Blog.timestamp.desc()).paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
	blogs = pagination.items
	return render_template('blogs.html',cat_id=cat_id,blogs=blogs,pagination=pagination,categories=categories,title=title)

@main.route('/blogs/article/<int:blog_id>')
def article(blog_id):
	categories = Category.query.all()
	blogs = Blog.query.filter_by(id=blog_id).all()
	return render_template('blogs.html',blogs=blogs,categories=categories,title=blogs[0].category.name,single=True)

@main.route('/blogs/new_cat',methods=['GET','POST'])
@login_required
def new_cat():
	form = NewCatForm()
	categories = Category.query.all()
	if form.validate_on_submit():
		category = Category(name=form.name.data)
		db.session.add(category)
		db.session.commit()
		flash('New category!')
		return redirect(url_for('main.category',cat_id=0))
	return render_template('new_cat_form.html',title=u'新建目录',form=form,categories=categories)

@main.route('/blogs/new_blog',methods=['GET','POST'])
@login_required
def new_blog():
	categories = Category.query.all()
	form = NewBlogForm()
	form.cat_id.choices = [(g.id, g.name) for g in \
		Category.query.order_by('id')]
	if form.validate_on_submit():
		blog = Blog(title=form.title.data,text=form.text.data,\
			category_id=form.cat_id.data,tag=form.tag.data,\
			abstract=form.abstract.data,text_html=markdown(form.text.data))

		db.session.add(blog)
		db.session.commit()
		flash('new blog!')
		return redirect(url_for('main.category',cat_id=form.cat_id.data))
	return render_template('new_blog_form.html',title=u'新建博客',form=form,categories=categories)
@main.route('/blogs/delete/<int:blog_id>',methods=['GET','POST'])
@login_required
def del_blog(blog_id):
	blog = Blog.query.filter_by(id=blog_id).first()
	db.session.delete(blog)
	return redirect(url_for('main.category',cat_id=0))
@main.route('/blogs/edit/<int:blog_id>',methods=['GET','POST'])
@login_required
def edit_blog(blog_id):
	categories = Category.query.all()
	blog = Blog.query.filter_by(id=blog_id).first()
	form = NewBlogForm()
	form.cat_id.choices = [(g.id, g.name) for g in \
		Category.query.order_by('id')]
	if form.validate_on_submit():
		blog.title=form.title.data
		blog.text=form.text.data
		blog.category_id=form.cat_id.data
		blog.tag=form.tag.data
		blog.abstract=form.abstract.data
		blog.text_html = markdown(blog.text)
		db.session.add(blog)
		db.session.commit()
		return redirect(url_for('main.article',blog_id=blog_id))
	form.title.data=blog.title
	form.text.data=blog.text
	form.cat_id.data=blog.category_id
	form.tag.data=blog.tag
	form.abstract.data=blog.abstract
	return render_template('new_blog_form.html',title=u'修改博客',form=form,categories=categories)


@main.route('/plans')
def plans():
	return render_template('plans.html',title=u'计划')

@main.route('/about')
def about():
	return render_template('about.html',title=u'关于')

@main.route('/test',methods=['POST','GET'])
def test():
    form = TestForm()
    if form.validate_on_submit():
        flash('data_recieved is '+ form.name.data)
        return redirect('/test')
    return render_template('test.html',title = u'测试',form = form)
