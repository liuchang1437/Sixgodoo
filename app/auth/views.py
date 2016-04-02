# -*- coding: utf-8 -*-
from flask import render_template
from ..models import User
from .forms import LoginForm
from . import auth
from flask.ext.login import login_user,logout_user,login_required
from flask import render_template,redirect,request,url_for,flash

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(url_for('main.index'))
        flash(u'密码或者用户名错误。')
    return render_template('login.html',title=u'登录',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'用户已登出')
    return redirect(request.headers.get('Referer') or url_for('main.index'))
