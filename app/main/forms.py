# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField,SelectField,BooleanField,TextField
from wtforms.validators import Required,Length

class QueryItemForm(Form):
	item_name = StringField('',\
		validators=[Required()])

	submit = SubmitField(u'查询')
class NewTagForm(Form):
	name = StringField(u'新建标签',validators=[Required()])
	submit = SubmitField(u'提交')
class NewCatForm(Form):
	name = StringField(u'新建目录',validators=[Required()])
	submit = SubmitField(u'提交')
class NewItemForm(Form):
	name = StringField(u'新建备忘',validators=[Required()])
	text = TextAreaField(u'内容',validators=[Required()])
	tag_id = SelectField(u'标签',coerce=int)
	flag = BooleanField(u'已完成？')
	submit = SubmitField(u'提交')
class NewBlogForm(Form):
	title = StringField(u'标题',validators=[Required(),Length(0,64)])
	abstract = TextAreaField(u'摘要',validators=[Required(), \
		Length(0,140)])
	text = TextAreaField(u'正文',validators=[Required()])
	cat_id = SelectField(u'目录',coerce=int)
	tag = StringField(u'标签')
	submit = SubmitField(u'提交')
class TestForm(Form):
    name = TextField('name', validators = [Required()])
